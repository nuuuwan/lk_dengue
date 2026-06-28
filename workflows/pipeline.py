from dengue import NDCUDaily, NDCUScraper, NDCUWeekly, ReadMe

if __name__ == "__main__":
    NDCUScraper.scrape()
    NDCUWeekly.build_all(force=False)
    NDCUDaily.build_all(force=False)
    ReadMe.build()
