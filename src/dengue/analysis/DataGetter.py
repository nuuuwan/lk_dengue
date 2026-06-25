class DataGetter:
    @staticmethod
    def generic(Doc, get_file_from_latest, metric_key):
        latest = Doc.latest()
        d_list = get_file_from_latest(latest).read()

        id_to_metric = {}
        for d in d_list:
            region_id = d["district_id"][:5]
            n = int(d[metric_key])
            if region_id not in id_to_metric:
                id_to_metric[region_id] = 0
            id_to_metric[region_id] += n

        return dict(
            date_str=latest.date_str,
            id_to_metric=id_to_metric,
        )
