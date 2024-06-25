from helperFunctions import DataFetcher
import pandas as pd

all_keywords =[
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "Bulldog",
    "Poodle",
    "Beagle",
    "Rottweiler",
    "Yorkshire Terrier",
    "Boxer",
    "Dachshund",
    "Shih Tzu",
    "Siberian Husky"
]
timeframes = ["today 5-y", "today 12-m", "today 3-m", "today 1-m"]

def main():
    dataFetcher = DataFetcher(all_keywords, timeframes)
    dataFetcher.processAllKeywords()
    sorted_keyword_data = dataFetcher.sort_and_rank(keyword_data)
    dataFetcher.saveToCsv("google_trends_data.csv")


if __name__ == "__main__":
    main()
