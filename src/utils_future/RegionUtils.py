class RegionUtils:

    @staticmethod
    def get_region_name_to_id() -> dict[str, str]:
        return {
            "Colombo": "LK-11",
            "Gampaha": "LK-12",
            "Kalutara": "LK-13",
            "Kandy": "LK-21",
            "Matale": "LK-22",
            "Nuwara Eliya": "LK-23",
            "Galle": "LK-31",
            "Matara": "LK-32",
            "Hambantota": "LK-33",
            "Jaffna": "LK-41",
            "Kilinochchi": "LK-42",
            "Mannar": "LK-43",
            "Vavuniya": "LK-44",
            "Mullaitivu": "LK-45",
            "Batticaloa": "LK-51",
            "Ampara": "LK-52",
            "Trincomalee": "LK-53",
            "Kurunegala": "LK-61",
            "Puttalam": "LK-62",
            "Anuradhapura": "LK-71",
            "Polonnaruwa": "LK-72",
            "Badulla": "LK-81",
            "Moneragala": "LK-82",
            "Ratnapura": "LK-91",
            "Kegalle": "LK-92",
            #
            "CMC": "LK-11-CMC",
            "NIHS": "LK-13-NIHS",
            "NIHS Kalutara": "LK-13-NIHS",
            "Kalmunai": "LK-52-Kalmunai",
        }

    @staticmethod
    def get_region_id_to_name() -> dict[str, str]:
        return {v: k for k, v in RegionUtils.get_region_name_to_id().items()}

    @staticmethod
    def get_region_id_from_name(name: str):
        name = {
            "Monaragala": "Moneragala",
            "Nuwaraeliya": "Nuwara Eliya",
        }.get(name, name)
        return RegionUtils.get_region_name_to_id().get(name, name)

    @staticmethod
    def get_region_id_to_population():
        return {
            "LK-11": 2375415,
            "LK-12": 2436142,
            "LK-13": 1305784,
            "LK-21": 1461895,
            "LK-22": 526870,
            "LK-23": 725280,
            "LK-31": 1097372,
            "LK-32": 837889,
            "LK-33": 671418,
            "LK-41": 594751,
            "LK-42": 123756,
            "LK-43": 172312,
            "LK-44": 122619,
            "LK-45": 136710,
            "LK-51": 595918,
            "LK-52": 744551,
            "LK-53": 442745,
            "LK-61": 1768156,
            "LK-62": 818816,
            "LK-71": 960080,
            "LK-72": 447530,
            "LK-81": 872307,
            "LK-82": 527585,
            "LK-91": 1145423,
            "LK-92": 870476,
        }
