class Markdown:
    @staticmethod
    def table(d_list: list[dict]) -> str:
        if not d_list:
            return ""
        headers = list(d_list[0].keys())
        is_numeric = {
            h: all(isinstance(d.get(h), (int, float)) for d in d_list)
            for h in headers
        }
        sep = ["---:" if is_numeric[h] else "---" for h in headers]
        lines = (
            ["| " + " | ".join(headers) + " |"]
            + ["| " + " | ".join(sep) + " |"]
            + [
                "| " + " | ".join(str(d.get(h, "")) for h in headers) + " |"
                for d in d_list
            ]
        )
        lines.append("")
        return "\n".join(lines)
