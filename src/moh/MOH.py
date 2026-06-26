import os
from dataclasses import dataclass
from functools import cache

from rapidfuzz import fuzz

from utils_future import JSONFile


@dataclass
class MOH:
    region_id: str
    region_name: str
    district_id: str
    centroid_lat: float
    centroid_lng: float
    population: int

    MOH_LIST_PATH = os.path.join("moh_data", "ent", "moh.json")

    @classmethod
    def from_dict(cls, d: dict) -> "MOH":
        return cls(
            region_id=d["region_id"],
            region_name=d["region_name"],
            district_id=d["district_id"],
            centroid_lat=float(d["centroid_lat"]),
            centroid_lng=float(d["centroid_lng"]),
            population=int(d["population"]),
        )

    @classmethod
    @cache
    def list(cls):
        d_list = JSONFile(cls.MOH_LIST_PATH).read()
        return [cls.from_dict(d) for d in d_list]

    @classmethod
    @cache
    def idx(cls) -> dict[str, "MOH"]:
        return {moh.region_id: moh for moh in cls.list()}

    @classmethod
    @cache
    def from_name_fuzzy(cls, name: str) -> "MOH":
        name_lower = name.lower()
        moh_and_ration = []
        for moh in cls.list():
            ratio = fuzz.ratio(name_lower, moh.region_name.lower())
            if ratio > 80:
                moh_and_ration.append((moh, ratio))
        if not moh_and_ration:
            return None
        moh_and_ration.sort(key=lambda x: -x[1])
        return moh_and_ration[0][0]
