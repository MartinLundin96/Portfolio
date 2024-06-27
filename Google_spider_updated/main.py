from helperFunctions import DataFetcher
import pandas as pd

all_keywords =[
     "SEO", 
    "PPC", 
    "Content Marketing", 
    "Social Media Marketing", 
    "Email Marketing", 
    "Conversion Rate Optimization", 
    "Digital Analytics", 
    "Influencer Marketing", 
    "Mobile Marketing", 
    "Marketing Automation"
]
timeframes = ["today 5-y", "today 12-m", "today 3-m", "today 1-m"]

def main():
    dataFetcher = DataFetcher(all_keywords, timeframes)
    dataFetcher.processAllKeywords()
    dataFetcher.saveToCSV("google_trends_data.csv") #.xlsl for excel file 


if __name__ == "__main__":
    main()