import os

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, GeoUtils, Log, RegionUtils

log = Log("Deaths")


class Deaths:
    DIR_IMAGES = "images"

    @classmethod
    def by_district(cls):
        latest_weekly = NDCUWeekly.latest()
        deaths_by_district = latest_weekly.deaths_by_district_file.read()

        district_id_to_n_deaths = {}
        for d in deaths_by_district:
            district_id = d["district_id"][:5]
            n_deaths = int(d["n_deaths"])
            if district_id not in district_id_to_n_deaths:
                district_id_to_n_deaths[district_id] = 0
            district_id_to_n_deaths[district_id] += n_deaths

        return dict(
            date_str=latest_weekly.date_str,
            district_id_to_n_deaths=district_id_to_n_deaths,
        )

    @classmethod
    def chart_by_district(cls, force=True):
        data = cls.by_district()
        date_str = data["date_str"]
        region_id_to_population = RegionUtils.get_region_id_to_population()

        image_path = os.path.join(
            cls.DIR_IMAGES, f"deaths_by_district_{date_str}.png"
        )
        if os.path.exists(image_path) and not force:
            return image_path

        district_id_to_n_deaths = data["district_id_to_n_deaths"]

        deaths_lookup = {
            district_id: n_deaths
            for district_id, n_deaths in district_id_to_n_deaths.items()
        }
        name_lookup = RegionUtils.get_region_id_to_name()
        per_1000_lookup = {
            district_id: n_deaths
            / region_id_to_population[district_id]
            * 100_000
            for district_id, n_deaths in district_id_to_n_deaths.items()
            if n_deaths is not None
        }

        gdf = GeoUtils.get_all_gdf()
        gdf["n_deaths"] = gdf["id"].map(deaths_lookup).fillna(0).astype(int)
        gdf["n_deaths_per_100K"] = gdf["id"].map(per_1000_lookup)

        cmap = LinearSegmentedColormap.from_list(
            "white_red", ["white", "darkred"]
        )

        fig, ax = plt.subplots(1, 1, figsize=(8, 10))
        gdf.plot(
            column="n_deaths_per_100K",
            ax=ax,
            cmap=cmap,
            edgecolor="grey",
            linewidth=0.5,
            legend=True,
            legend_kwds={"label": "Deaths per 100,000 people", "shrink": 0.6},
            missing_kwds={"color": "lightgrey", "label": "No data"},
        )

        for _, row in gdf.iterrows():
            n_deaths = int(row["n_deaths"])
            if n_deaths == 0:
                continue
            centroid = row.geometry.centroid
            district_id = row["id"]
            name = name_lookup.get(district_id, district_id)
            gap_y = 7000
            ax.annotate(
                name,
                xy=(centroid.x, centroid.y + gap_y),
                ha="center",
                va="center",
                fontsize=6,
                color="black",
            )
            ax.annotate(
                f"{n_deaths}",
                xy=(centroid.x, centroid.y),
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )

        ax.set_title(f"Dengue Deaths in 2026 by District (as of {date_str})")
        ax.axis("off")
        plt.tight_layout()

        os.makedirs(cls.DIR_IMAGES, exist_ok=True)

        plt.savefig(image_path, dpi=300)
        plt.close("all")
        log.info(f"Wrote  {File(image_path)}")
        return image_path
