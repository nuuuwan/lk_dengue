import geopandas as gpd


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
