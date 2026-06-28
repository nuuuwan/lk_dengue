from dengue import NDCUDaily, NDCUWeekly, ReadMe

if __name__ == "__main__":
    NDCUDaily.build_all(force=True)
    NDCUWeekly.build_all(force=True)
    ReadMe.build()
