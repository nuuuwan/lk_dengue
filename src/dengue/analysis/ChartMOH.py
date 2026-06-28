import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

from utils_future import File, Log, RegionUtils

log = Log("ChartMOH")

MOH_GEO_PATH = os.path.join("moh_data", "geo", "moh.topojson")
MOH_ENT_PATH = os.path.join("moh_data", "ent", "moh.json")


class ChartMOH:
    DIR_IMAGES = "images"
    FIG_SIZE = (10, 10)
    DPI = 300

    @staticmethod
    def _get_moh_id_to_population():
        with open(MOH_ENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {
            d["region_id"]: d["population"]
            for d in data
            if d.get("population")
        }

    @staticmethod
    def _get_moh_name_to_id():
        with open(MOH_ENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {d["region_name"].upper(): d["region_id"] for d in data}

    @staticmethod
    def _get_moh_id_to_district_id():
        with open(MOH_ENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return {d["region_id"]: d["district_id"] for d in data}

    @staticmethod
    def _get_moh_gdf():
        gdf = gpd.read_file(MOH_GEO_PATH)
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
        return gdf.to_crs(epsg=3857)

    @staticmethod
    def _build_id_to_metric(d_list, get_metric):
        id_to_metric = {}
        for d in d_list:
            moh_id = d["moh_id"]
            n = get_metric(d)
            if moh_id not in id_to_metric:
                id_to_metric[moh_id] = 0
            id_to_metric[moh_id] += n
        return id_to_metric

    @staticmethod
    def _build_metric_data(d_list, get_metric):
        id_to_metric = ChartMOH._build_id_to_metric(d_list, get_metric)
        id_to_population = ChartMOH._get_moh_id_to_population()
        id_to_metric_per_100k = {
            moh_id: metric / id_to_population[moh_id] * 100_000
            for moh_id, metric in id_to_metric.items()
            if metric is not None and moh_id in id_to_population
        }
        id_to_name = {d["moh_id"]: d["moh_area_name"] for d in d_list}
        return id_to_metric, id_to_metric_per_100k, id_to_name

    @staticmethod
    def _build_annotated_gdf(id_to_metric, id_to_metric_per_100k, id_to_name):
        gdf = ChartMOH._get_moh_gdf()
        moh_name_to_id = ChartMOH._get_moh_name_to_id()
        gdf["moh_id"] = gdf["MOH_N"].str.upper().map(moh_name_to_id)
        moh_id_to_district_id = ChartMOH._get_moh_id_to_district_id()
        gdf["district_id"] = gdf["moh_id"].map(moh_id_to_district_id)
        gdf["metric"] = gdf["moh_id"].map(id_to_metric).fillna(0).astype(int)
        gdf["metric_per_100k"] = gdf["moh_id"].map(id_to_metric_per_100k)
        gdf["moh_name"] = gdf["moh_id"].map(id_to_name)
        return gdf

    @staticmethod
    def _build_cmap_norm(metric_values, positive_color, negative_color):
        max_val = max(metric_values, default=1) or 1
        min_val = min(metric_values, default=-1) or -1
        has_positive, has_negative = max_val > 0, min_val < 0
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
            return cmap, Normalize(vmin=min_val, vmax=max_val)
        if has_positive:
            cmap = LinearSegmentedColormap.from_list(
                "custom", ["white", positive_color]
            )
            return cmap, Normalize(vmin=0, vmax=max_val)
        cmap = LinearSegmentedColormap.from_list(
            "custom", [negative_color, "white"]
        )
        return cmap, Normalize(vmin=min_val, vmax=0)

    @staticmethod
    def _annotate_moh_areas(ax, district_gdf, metric_label, gap_y):
        for _, row in district_gdf.iterrows():
            metric = int(row["metric"])
            if metric == 0:
                continue
            centroid = row.geometry.centroid
            value_str = (
                f"{metric}"
                if "Additional" not in metric_label
                else f"{metric:+}"
            )
            moh_name = row["moh_name"].replace(" & ", " \n& ")
            ax.annotate(
                value_str,
                xy=(centroid.x, centroid.y + gap_y),
                ha="center",
                va="bottom",
                fontsize=8,
                color="black",
            )
            ax.annotate(
                moh_name,
                xy=(centroid.x, centroid.y - gap_y),
                ha="center",
                va="top",
                fontsize=6,
                color="black",
            )

    @staticmethod
    def _add_chart_labels(
        ax, metric_label, district_name, date_str, source_url
    ):
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
            f"Source: {source_url}",
            xy=(0.5, 0.01),
            xycoords="axes fraction",
            ha="center",
            va="bottom",
            fontsize=12,
            color="grey",
        )

    @staticmethod
    def _chart_district(
        district_gdf,
        district_name,
        cmap,
        norm,
        metric_label,
        date_str,
        source_url,
        image_path,
    ):
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
            sm, ax=ax, shrink=0.6, label=f"{metric_label} per 100,000 people"
        )

        bounds = district_gdf.total_bounds
        gap_y = (bounds[3] - bounds[1]) * 0.001
        ChartMOH._annotate_moh_areas(ax, district_gdf, metric_label, gap_y)
        ChartMOH._add_chart_labels(
            ax, metric_label, district_name, date_str, source_url
        )

        ax.axis("off")
        plt.tight_layout()
        plt.savefig(image_path, dpi=ChartMOH.DPI)
        plt.close("all")
        log.info(f"Wrote  {File(image_path)}")

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

        id_to_metric, id_to_metric_per_100k, id_to_name = (
            ChartMOH._build_metric_data(d_list, get_metric)
        )

        gdf = ChartMOH._build_annotated_gdf(
            id_to_metric, id_to_metric_per_100k, id_to_name
        )
        metric_values = [
            v for v in id_to_metric_per_100k.values() if v is not None
        ]
        cmap, norm = ChartMOH._build_cmap_norm(
            metric_values, positive_color, negative_color
        )

        os.makedirs(ChartMOH.DIR_IMAGES, exist_ok=True)
        image_paths = []
        district_totals = (
            gdf.groupby("district_id")["metric"]
            .sum()
            .sort_values(ascending=False)
        )
        id_to_name_map = RegionUtils.get_region_id_to_name()

        for district_id in district_totals.index:
            district_gdf = gdf[gdf["district_id"] == district_id].copy()
            if district_gdf["metric"].sum() == 0:
                log.warning(f"No data for district: {district_id}")
                continue
            district_name = id_to_name_map.get(district_id, district_id)
            district_slug = district_id.lower()
            image_path = os.path.join(
                ChartMOH.DIR_IMAGES, f"{metric_id}_by_moh_{district_slug}.png"
            )
            if os.path.exists(image_path) and not force:
                image_paths.append(image_path)
                continue
            ChartMOH._chart_district(
                district_gdf,
                district_name,
                cmap,
                norm,
                metric_label,
                date_str,
                Doc.get_source_url(),
                image_path,
            )
            image_paths.append(image_path)

        return image_paths
