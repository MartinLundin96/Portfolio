import pandas as pd
import time
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError, TooManyRequestsError

class DataFetcher:
    def __init__(self, keywords, timeframes):
        self.timeframes = timeframes
        self.__cat = "0"
        self.__geo = ""
        self.__gprop = ""
        self.keywords = keywords
        self.kwDf = pd.DataFrame(columns=[
            "Keyword", 
            "Average 5 years interest", 
            "Last year vs. last 5 years trend change (%)", 
            "Trendiness"
        ])
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def fetchData(self, keyword, maxAttempts=3, wait_time=30):
        attempt = 0
        data = None
      
        while attempt < maxAttempts:
            try:
                self.pytrends.build_payload([keyword], cat=self.__cat, timeframe=self.timeframes[0], geo=self.__geo, gprop=self.__gprop)
                data = self.pytrends.interest_over_time()
                if data.empty:
                    print(f"No data found for keyword: {keyword}")
                break


            except TooManyRequestsError:
                attempt += 1
                if attempt < maxAttempts:
                    print(f"Too many requests. Retry attempt {attempt}/{maxAttempts}...")
                    time.sleep(wait_time)
                else:
                    print(f"Failed to fetch data for '{keyword}' after {maxAttempts} attempts due to too many requests.")
                    break

            except ResponseError as e:
                if "HTTP 400" in str(e):
                    print(f"Received a 400 error for: {keyword}. Skipping this keyword.")
                    break
                else:
                    raise e
                  
        return data
    

    @staticmethod
    def trendTag(trend, mean):
        trendiness = "Undefined"
        
        if mean > 75 and abs(trend) <= 5:
            trendiness = "Stable"
        elif mean > 75 and trend > 5:
            trendiness = "Increasing"
        elif mean > 75 and trend < -5:
            trendiness = "Decreasing"
        elif mean > 60 and abs(trend) <= 15:
            trendiness = "Relatively stable"
        elif mean > 20 and abs(trend) <= 15:
            trendiness = "Seasonal/Cyclical"
        elif mean > 20 and trend > 15:
            trendiness = "Trending"
        elif mean > 0 and trend > 15:
            trendiness = "New and trending"
        elif mean > 0 and trend < -15:
            trendiness = "Declining"

        return trendiness

    def processKeyword(self, keyword):
        data = self.fetchData(keyword)
        if data is None or data.empty:
            print(f"No data found for keyword: {keyword}")
            return
        # Calcs
        mean = round(data[keyword].mean(), 2)
        avgLastYear = round(data[keyword][-52:].mean(), 2)
        trend_change = round(((avgLastYear / mean) - 1) * 100, 2)

        trendiness = self.trendTag(trend_change, mean)

        new_row = {
                "Keyword": keyword,
                "Average 5 years interest": mean,
                "Last year vs. last 5 years trend change (%)": trend_change,
                "Trendiness": trendiness
        }
        self.kwDf = self.kwDf.append(new_row, ignore_index=True)
    
    def processAllKeywords(self):
        for keyword in self.keywords:
            self.processKeyword(keyword)

    def saveToCSV(self, filename):
        self.kwDf.to_csv(filename, index=False)
        
    @staticmethod        
    def sort_and_rank(keyword_data):
        sorted_keyword_data = sorted(keyword_data, key=lambda x: x["Last year vs. last 5 years trend change (%)"], reverse=True)
        return sorted_keyword_data
