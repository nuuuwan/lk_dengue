import os

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

from dengue.analysis.DataGetter import DataGetter
from utils_future import File, GeoUtils, Log, RegionUtils

log = Log("Chart")


class Chart:
    DIR_IMAGES = "images"
    FIG_SIZE = (10, 10)
    DPI = 90

    @staticmethod
    def chart_metric_by_region(
        Doc,
        get_file_from_latest,
        get_metric,
        metric_label,
        positive_color,
        negative_color,
        force=False,
    ):
        metric_id = metric_label.lower().replace(" ", "-")
        data = DataGetter.generic(Doc, get_file_from_latest, get_metric)
        date_str = data["date_str"]
        id_to_metric = data["id_to_metric"]

        image_path = os.path.join(
            Chart.DIR_IMAGES, f"{metric_id}_by_region.png"
        )
        if os.path.exists(image_path) and not force:
            return image_path

        id_to_name = RegionUtils.get_region_id_to_name()
        id_to_population = RegionUtils.get_region_id_to_population()
        id_to_metric_per_100k = {
            district_id: metric / id_to_population[district_id] * 100_000
            for district_id, metric in id_to_metric.items()
            if metric is not None
        }

        gdf = GeoUtils.get_all_gdf()
        gdf["metric"] = gdf["id"].map(id_to_metric).fillna(0).astype(int)
        gdf["metric_per_100k"] = gdf["id"].map(id_to_metric_per_100k)

        metric_values = [
            v for v in id_to_metric_per_100k.values() if v is not None
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

        fig, ax = plt.subplots(1, 1, figsize=Chart.FIG_SIZE)
        gdf.plot(
            column="metric_per_100k",
            ax=ax,
            cmap=cmap,
            norm=norm,
            edgecolor="grey",
            linewidth=0.5,
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

        for _, row in gdf.iterrows():
            metric = int(row["metric"])
            if metric == 0:
                continue
            centroid = row.geometry.centroid
            region_id = row["id"]
            name = id_to_name.get(region_id, region_id)
            gap_y = 4000
            ax.annotate(
                (
                    f"{metric:,}"
                    if "Additional" not in metric_label
                    else f"{metric:+,}"
                ),
                xy=(centroid.x, centroid.y + gap_y),
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
            ax.annotate(
                name,
                xy=(centroid.x, centroid.y - gap_y),
                ha="center",
                va="center",
                fontsize=6,
                color="black",
            )

        ax.annotate(
            metric_label,
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

        os.makedirs(Chart.DIR_IMAGES, exist_ok=True)

        plt.savefig(image_path, dpi=Chart.DPI)
        plt.close("all")
        log.info(f"Wrote  {File(image_path)}")
        return image_path
