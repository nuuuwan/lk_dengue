from dengue.ndcu_daily.NDCUDaily import NDCUDaily
from dengue.ndcu_weekly.NDCUWeekly import NDCUWeekly
from utils_future import Time, TimeFormat


class NDCUScraperBackpopulator:
    @classmethod
    def backpopulate_daily(cls):
        for days_ago in range(1, 30):
            for time_format_str in ["%Y-%m-%d", "%Y.%m.%d", "%Y.-%m.-%d"]:
                t = Time(Time.now().ut - 86400 * days_ago)
                date_str = TimeFormat(time_format_str).format(t)
                year_str = TimeFormat("%Y").format(t)
                month_str = TimeFormat("%m").format(t)
                url = (
                    "https://www.dengue.health.gov.lk"
                    + f"/wp-content/uploads/{year_str}/{month_str}/Daily-Update-{date_str}.pdf"
                )
                try:
                    NDCUDaily.from_pdf_url_hot(pdf_url=url)
                    break
                except Exception:
                    pass

    @classmethod
    def backpopulate_weekly(cls):
        for weeks_ago in range(1, 13):
            t = Time(Time.now().ut - 604800 * weeks_ago)
            year_str = TimeFormat("%Y").format(t)
            month_str = TimeFormat("%m").format(t)
            week = int(TimeFormat("%U").format(t))
            week_str = f"{week - weeks_ago:02d}"
            url = (
                "https://www.dengue.health.gov.lk"
                + "/wp-content/uploads"
                + f"/{year_str}/{month_str}"
                + f"/Weekly-Dengue-Update-{year_str}-Week-{week_str}.pdf"
            )
            try:
                NDCUWeekly.from_pdf_url_hot(pdf_url=url)
            except Exception:
                pass

    @classmethod
    def backpopulate(cls):
        cls.backpopulate_weekly()
        cls.backpopulate_daily()
