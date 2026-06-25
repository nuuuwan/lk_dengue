class RegionUtils:
    @staticmethod
    def get_region_id_from_name(name: str) -> str:
        name = {
            "Monaragala": "Moneragala",
            "Nuwaraeliya": "Nuwara Eliya",
        }.get(name, name)
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
            "Kalmunai": "LK-52-Kalmunai",
        }.get(name, name)
