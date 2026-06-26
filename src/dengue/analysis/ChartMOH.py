import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

from utils_future import File, Log

log = Log("ChartMOH")

MOH_GEO_PATH = os.path.join("moh_data", "geo", "moh.topojson")
MOH_ENT_PATH = os.path.join("moh_data", "ent", "moh.json")


class ChartMOH:
    DIR_IMAGES = "images"
    FIG_SIZE = (10, 10)
    DPI = 300

    @staticmethod
    def _get_moh_name_to_population():
        with open(MOH_ENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {
            d["region_name"].upper(): d["population"]
            for d in data
            if d.get("population")
        }

    @staticmethod
    def _get_moh_gdf():
        gdf = gpd.read_file(MOH_GEO_PATH)
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
        return gdf.to_crs(epsg=3857)

    @staticmethod
    def _build_name_to_metric(d_list, get_metric):
        name_to_metric = {}
        for d in d_list:
            moh_name = d["moh_area_name"].upper()
            n = get_metric(d)
            if moh_name not in name_to_metric:
                name_to_metric[moh_name] = 0
            name_to_metric[moh_name] += n
        return name_to_metric

    @staticmethod
    def chart_metric_by_moh(
        Doc,
        get_file_from_latest,
        get_metric,
        metric_label,
        positive_color,
        negative_color,
        force=True,
    ):
        metric_id = metric_label.lower().replace(" ", "-")
        latest = Doc.latest()
        d_list = get_file_from_latest(latest).read()
        date_str = latest.date_str

        name_to_metric = ChartMOH._build_name_to_metric(d_list, get_metric)
        name_to_population = ChartMOH._get_moh_name_to_population()
        name_to_metric_per100k = {
            name: metric / name_to_population[name] * 100_000
            for name, metric in name_to_metric.items()
            if metric is not None and name in name_to_population
        }

        gdf = ChartMOH._get_moh_gdf()
        # MOH_N is uppercase in the topojson; match using uppercase
        # moh_area_name
        gdf["metric"] = gdf["MOH_N"].map(name_to_metric).fillna(0).astype(int)
        gdf["metric_per_100k"] = gdf["MOH_N"].map(name_to_metric_per100k)

        # Global color scale so all district charts are comparable
        metric_values = [
            v for v in name_to_metric_per100k.values() if v is not None
        ]
        max_val = max(metric_values, default=1) or 1
        min_val = min(metric_values, default=-1) or -1

        has_positive = max_val > 0
        has_negative = min_val < 0

        if has_positive and has_negative:
            zero_frac = (-min_val) / (max_val - min_val)
            cmap = LinearSegmentedColormap.from_list(
                "custom",
                [
                    (0.0, negative_color),
                    (zero_frac, "white"),
                    (1.0, positive_color),
                ],
            )
            norm = Normalize(vmin=min_val, vmax=max_val)
        elif has_positive:
            cmap = LinearSegmentedColormap.from_list(
                "custom", ["white", positive_color]
            )
            norm = Normalize(vmin=0, vmax=max_val)
        else:
            cmap = LinearSegmentedColormap.from_list(
                "custom", [negative_color, "white"]
            )
            norm = Normalize(vmin=min_val, vmax=0)

        os.makedirs(ChartMOH.DIR_IMAGES, exist_ok=True)
        image_paths = []

        for district_name in sorted(gdf["DISTRICT_N"].unique()):
            district_gdf = gdf[gdf["DISTRICT_N"] == district_name].copy()

            # Skip districts with no data
            if district_gdf["metric"].sum() == 0:
                continue

            district_slug = district_name.lower().replace(" ", "-")
            image_path = os.path.join(
                ChartMOH.DIR_IMAGES,
                f"{metric_id}_by_moh_{district_slug}.png",
            )
            if os.path.exists(image_path) and not force:
                image_paths.append(image_path)
                continue

            _, ax = plt.subplots(1, 1, figsize=ChartMOH.FIG_SIZE)
            district_gdf.plot(
                column="metric_per_100k",
                ax=ax,
                cmap=cmap,
                norm=norm,
                edgecolor="grey",
                linewidth=0.3,
                missing_kwds={"color": "lightgrey", "label": "No data"},
            )

            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            plt.colorbar(
                sm,
                ax=ax,
                shrink=0.6,
                label=f"{metric_label} per 100,000 people",
            )

            bounds = district_gdf.total_bounds  # [minx, miny, maxx, maxy]
            gap_y = (bounds[3] - bounds[1]) * 0.03

            for _, row in district_gdf.iterrows():
                metric = int(row["metric"])
                if metric == 0:
                    continue
                centroid = row.geometry.centroid
                moh_name = row["MOH_N"].title()
                ax.annotate(
                    (
                        f"{metric}"
                        if "Additional" not in metric_label
                        else f"{metric:+}"
                    ),
                    xy=(centroid.x, centroid.y + gap_y),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="black",
                )
                ax.annotate(
                    moh_name,
                    xy=(centroid.x, centroid.y - gap_y),
                    ha="center",
                    va="center",
                    fontsize=6,
                    color="black",
                )

            ax.annotate(
                f"{metric_label} - {district_name.title()}",
                xy=(0.5, 1.04),
                xycoords="axes fraction",
                ha="center",
                va="bottom",
                fontsize=18,
            )
            ax.annotate(
                f"as of {date_str}",
                xy=(0.5, 1.01),
                xycoords="axes fraction",
                ha="center",
                va="bottom",
                fontsize=12,
                color="grey",
            )
            ax.annotate(
                f"Source: {Doc.get_source_url()}",
                xy=(0.5, 0.01),
                xycoords="axes fraction",
                ha="center",
                va="bottom",
                fontsize=12,
                color="grey",
            )
            ax.axis("off")
            plt.tight_layout()

            plt.savefig(image_path, dpi=ChartMOH.DPI)
            plt.close("all")
            log.info(f"Wrote  {File(image_path)}")
            image_paths.append(image_path)

        return image_paths
