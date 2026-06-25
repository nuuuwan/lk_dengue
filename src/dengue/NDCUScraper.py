from dengue.NDCUDailyUpdate import NDCUDailyUpdate
from dengue.NDCUWeeklyUpdate import NDCUWeeklyUpdate
from utils_future import WWW, Log

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
        NDCUWeeklyUpdate.from_pdf_url(pdf_url=weekly_update_links[0]["href"])

        daily_update_links = [
            link for link in pdf_links if "daily" in link["href"].lower()
        ]
        NDCUDailyUpdate.from_pdf_url(pdf_url=daily_update_links[0]["href"])
