from dengue.ndcu_daily.NDCUDaily import NDCUDaily
from dengue.ndcu_weekly.NDCUWeekly import NDCUWeekly
from utils_future import WWW, Log, Time, TimeDelta, TimeFormat, TimeUnit

log = Log("NDCUScraper")


class NDCUScraper:
    URL = "https://www.dengue.health.gov.lk/#latest-update"

    @classmethod
    def build_all(cls) -> str:
        soup = WWW(cls.URL).soup()
        pdf_links = soup.find_all(
            "a", href=lambda href: href and href.endswith(".pdf")
        )
        weekly_update_links = [
            link for link in pdf_links if "weekly" in link["href"].lower()
        ]
        NDCUWeekly.from_pdf_url_hot(pdf_url=weekly_update_links[0]["href"])

        daily_update_links = [
            link for link in pdf_links if "daily" in link["href"].lower()
        ]
        NDCUDaily.from_pdf_url_hot(pdf_url=daily_update_links[0]["href"])

    @classmethod
    def backpopulate(cls):
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
