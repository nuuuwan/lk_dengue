import datetime
import os

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import MaxNLocator

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
        annotation_formatter=None,
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
        gdf["metric_raw"] = gdf["id"].map(id_to_metric).fillna(0)
        gdf["metric"] = gdf["metric_raw"].astype(int)
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
            metric_raw = row["metric_raw"]
            metric = int(row["metric"])
            if metric_raw == 0:
                continue
            centroid = row.geometry.centroid
            region_id = row["id"]
            name = id_to_name.get(region_id, region_id)
            gap_y = 4000
            if annotation_formatter is not None:
                label_text = annotation_formatter(metric_raw)
            elif "Additional" not in metric_label:
                label_text = f"{metric:,}"
            else:
                label_text = f"{metric:+,}"
            ax.annotate(
                label_text,
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

    @staticmethod
    def _get_daily_district_totals():
        """Return sorted list of (date_str, {district_id_5: total_cases})."""
        from dengue.ndcu_daily import NDCUDaily

        docs = NDCUDaily.list()
        docs.sort(key=lambda d: d.date_str)

        results = []
        for doc in docs:
            try:
                rows = doc.district_data_file.read()
            except Exception:
                continue
            district_totals = {}
            for r in rows:
                dist_id = r["district_id"][:5]
                district_totals[dist_id] = district_totals.get(
                    dist_id, 0
                ) + int(r["n_cases"])
            results.append((doc.date_str, district_totals))
        return results

    @staticmethod
    def chart_daily_cases_by_week(force=False):
        """Line chart of weekly new cases (national) from NDCUDaily data."""
        from dengue.ndcu_daily import NDCUDaily

        image_path = os.path.join(
            Chart.DIR_IMAGES, "daily_cases_by_week_national.png"
        )
        if os.path.exists(image_path) and not force:
            return image_path

        daily = Chart._get_daily_district_totals()

        # Group by ISO week, keeping the last reading per week (highest cumulative)
        week_to_last = {}  # week_str -> (date_str, national_total)
        for date_str, district_totals in daily:
            d = datetime.date.fromisoformat(date_str)
            week_str = d.strftime("%G-W%V")
            national_total = sum(district_totals.values())
            week_to_last[week_str] = (date_str, national_total)

        sorted_weeks = sorted(week_to_last.keys())
        if len(sorted_weeks) < 2:
            return None

        x_labels = []
        weekly_new = []
        prev_total = 0
        for week_str in sorted_weeks:
            date_str, total = week_to_last[week_str]
            x_labels.append(date_str)
            weekly_new.append(max(0, total - prev_total))
            prev_total = total

        # Skip the first week if it looks like an incomplete partial week
        if len(weekly_new) > 1:
            x_labels = x_labels[1:]
            weekly_new = weekly_new[1:]

        latest_date = daily[-1][0]

        fig, ax = plt.subplots(figsize=(14, 6))
        x = range(len(x_labels))
        ax.fill_between(x, weekly_new, alpha=0.25, color="darkorange")
        ax.plot(
            x,
            weekly_new,
            marker="o",
            color="darkorange",
            linewidth=2,
            markersize=5,
        )
        ax.set_xticks(list(x))
        ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=9)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("Week (last day of reporting)", fontsize=11)
        ax.set_ylabel("New cases", fontsize=11)
        ax.set_title(
            f"Weekly Dengue Cases – Sri Lanka\nas of {latest_date}",
            fontsize=14,
        )
        plt.tight_layout()
        fig.text(
            0.5,
            0.01,
            f"Source: {NDCUDaily.get_source_url()}",
            ha="center",
            fontsize=9,
            color="grey",
        )
        plt.subplots_adjust(bottom=0.18)
        os.makedirs(Chart.DIR_IMAGES, exist_ok=True)
        plt.savefig(image_path, dpi=Chart.DPI)
        plt.close("all")
        log.info(f"Wrote  {File(image_path)}")
        return image_path

    @staticmethod
    def chart_daily_cases_per_100k_by_district(force=False):
        """Multi-line chart of weekly new cases per 100k by district."""
        image_path = os.path.join(
            Chart.DIR_IMAGES, "daily_cases_per_100k_by_district.png"
        )
        if os.path.exists(image_path) and not force:
            return image_path

        from dengue.ndcu_daily import NDCUDaily

        daily = Chart._get_daily_district_totals()
        id_to_population = RegionUtils.get_region_id_to_population()
        id_to_name = RegionUtils.get_region_id_to_name()

        # Only include the 25 standard districts (5-char IDs, no sub-areas)
        district_ids = sorted(
            k for k in id_to_population.keys() if len(k) == 5
        )

        # Group by ISO week per district
        week_to_district_cumulative = {}
        for date_str, district_totals in daily:
            d = datetime.date.fromisoformat(date_str)
            week_str = d.strftime("%G-W%V")
            if week_str not in week_to_district_cumulative:
                week_to_district_cumulative[week_str] = (date_str, {})
            _, dist_map = week_to_district_cumulative[week_str]
            for dist_id, total in district_totals.items():
                dist_map[dist_id] = total
            week_to_district_cumulative[week_str] = (date_str, dist_map)

        sorted_weeks = sorted(week_to_district_cumulative.keys())
        if len(sorted_weeks) < 2:
            return None

        # Build per-district weekly new-case series
        x_labels = []
        district_weekly = {dist_id: [] for dist_id in district_ids}
        prev_dist_total = {dist_id: 0 for dist_id in district_ids}

        for week_str in sorted_weeks:
            date_str, dist_map = week_to_district_cumulative[week_str]
            x_labels.append(date_str)
            for dist_id in district_ids:
                cum = dist_map.get(dist_id, prev_dist_total[dist_id])
                new_cases = max(0, cum - prev_dist_total[dist_id])
                pop = id_to_population.get(dist_id, 1)
                district_weekly[dist_id].append(new_cases / pop * 100_000)
                prev_dist_total[dist_id] = cum

        # Drop first week (partial)
        if len(x_labels) > 1:
            x_labels = x_labels[1:]
            district_weekly = {k: v[1:] for k, v in district_weekly.items()}

        latest_date = daily[-1][0]

        # Rank districts by max weekly value for styling
        district_max = {
            dist_id: max(vals) if vals else 0
            for dist_id, vals in district_weekly.items()
        }
        top_districts = sorted(district_ids, key=lambda d: -district_max[d])[
            :8
        ]

        fig, ax = plt.subplots(figsize=(14, 7))
        x = range(len(x_labels))

        for dist_id in district_ids:
            vals = district_weekly[dist_id]
            name = id_to_name.get(dist_id, dist_id)
            if dist_id in top_districts:
                ax.plot(
                    x, vals, linewidth=2, label=name, marker="o", markersize=4
                )
            else:
                ax.plot(x, vals, linewidth=0.8, alpha=0.35, color="grey")

        ax.set_xticks(list(x))
        ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=9)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("Week (last day of reporting)", fontsize=11)
        ax.set_ylabel("New cases per 100,000 people", fontsize=11)
        ax.set_title(
            f"Weekly Dengue Cases per 100k – Sri Lanka by District\nas of {latest_date}",
            fontsize=14,
        )
        ax.legend(
            loc="upper left",
            fontsize=8,
            framealpha=0.7,
            title="Top 8 Districts",
            title_fontsize=8,
        )
        plt.tight_layout()
        fig.text(
            0.5,
            0.01,
            f"Source: {NDCUDaily.get_source_url()}",
            ha="center",
            fontsize=9,
            color="grey",
        )
        plt.subplots_adjust(bottom=0.2)
        os.makedirs(Chart.DIR_IMAGES, exist_ok=True)
        plt.savefig(image_path, dpi=Chart.DPI)
        plt.close("all")
        log.info(f"Wrote  {File(image_path)}")
        return image_path
