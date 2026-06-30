from dengue import NDCUDaily, NDCUScraper, NDCUWeekly, ReadMe

if __name__ == "__main__":
    NDCUScraper.scrape()
    NDCUDaily.update_latest()
    NDCUWeekly.update_latest()
    ReadMe.build()
