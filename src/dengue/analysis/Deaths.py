import os

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from dengue.ndcu_weekly import NDCUWeekly
from utils_future import File, Log, RegionUtils

log = Log("Deaths")


class GeoUtils:
    URL = (
        "https://raw.githubusercontent.com"
        + "/nuuuwan/lk_admin_regions/refs/heads/main"
        + "/data/geo/topojson/e3_small/districts.topojson"
    )

    @staticmethod
    def get_all_gdf():
        gdf = gpd.read_file(GeoUtils.URL)
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
        return gdf.to_crs(epsg=3857)

    @staticmethod
    def get_gdf(district_id):
        gdf = GeoUtils.get_all_gdf()
        return gdf[gdf["id"] == district_id]


class Deaths:
    DIR_IMAGES = "images"

    @classmethod
    def by_district(cls):
        latest_weekly = NDCUWeekly.latest()
        deaths_by_district = latest_weekly.deaths_by_district_file.read()

        expanded = []
        for d in deaths_by_district:
            district_id = d["district_id"]
            n_deaths = d["n_deaths"]
            population = RegionUtils.get_region_id_to_population().get(
                district_id, None
            )
            n_deaths_per_100K = (
                int(n_deaths) / population * 100_000 if population else None
            )
            d["n_deaths_per_100K"] = n_deaths_per_100K
            expanded.append(d)

        return dict(
            date_str=latest_weekly.date_str,
            deaths_by_district=expanded,
        )

    @classmethod
    def chart_by_district(cls, force=True):
        data = cls.by_district()
        date_str = data["date_str"]

        image_path = os.path.join(
            cls.DIR_IMAGES, f"deaths_by_district_{date_str}.png"
        )
        if os.path.exists(image_path) and not force:
            return image_path

        deaths_by_district = data["deaths_by_district"]

        deaths_lookup = {
            d["district_id"]: int(d["n_deaths"]) for d in deaths_by_district
        }
        name_lookup = {
            d["district_id"]: d["district_name"] for d in deaths_by_district
        }
        per_1000_lookup = {
            d["district_id"]: d["n_deaths_per_100K"]
            for d in deaths_by_district
            if d["n_deaths_per_100K"] is not None
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
                fontsize=7,
                color="black",
            )
            ax.annotate(
                f"{n_deaths} deaths" if n_deaths > 1 else f"{n_deaths} death",
                xy=(centroid.x, centroid.y),
                ha="center",
                va="center",
                fontsize=9,
                color="black",
            )
            ax.annotate(
                f"({row['n_deaths_per_100K']:.1f}/100K)",
                xy=(centroid.x, centroid.y - gap_y),
                ha="center",
                va="center",
                fontsize=7,
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
