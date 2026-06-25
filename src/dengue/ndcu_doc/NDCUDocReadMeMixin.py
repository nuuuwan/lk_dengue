class NDCUDocReadMeMixin:
    @classmethod
    def get_lines_for_source_reports(cls) -> list[str]:
        lines = [
            f"### [{cls.get_full_name()}]({cls.get_dir_class()})",
            "",
        ]
        docs = cls.list()
        for doc in docs:
            lines.append(f"- [{doc.date_str}]({doc.dir_data})")
        if docs:
            lines.append("")
        return lines
