from dengue.ndcu_daily.NDCUDaily import NDCUDaily
from dengue.ndcu_weekly.NDCUWeekly import NDCUWeekly
from utils_future import WWW, Log

log = Log("NDCUScraper")


class NDCUScraper:
    URL = "https://www.dengue.health.gov.lk/#latest-update"

    @classmethod
    def get_soup(cls):
        return WWW(cls.URL, t_selenium_wait=10).soup(with_selenium=True)

    @classmethod
    def scrape(cls) -> str:
        soup = cls.get_soup()
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
