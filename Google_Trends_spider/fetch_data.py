from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError, TooManyRequestsError
import time

def fetch_keyword_data(keywords):
    pytrends = TrendReq(hl="en-US")
    cat = "0"
    geo = ""
    timeframes = ["today 5-y", "today 12-m", "today 3-m", "today 1-m"]
    gprop = ""
    
    keyword_data = []
    
    for kw in keywords:
        attempt = 0
        while attempt < 3:  # Retry up to 3 times
            try:
                pytrends.build_payload([kw], cat, timeframes[0], geo, gprop)
                data = pytrends.interest_over_time()
                
                if kw not in data.columns:
                    print(f"No data found for keyword: {kw}")
                    break  # Skip this keyword and proceed to the next one
                
                mean = round(data.mean(), 2)
                avg = round(data[kw][-52:].mean(), 2)  # Last Year Average
                avg2 = round(data[kw][:52].mean(), 2)  # Yearly Average of 5 years ago.
                trend = round(((avg / mean[kw]) - 1) * 100, 2)
                trend2 = round(((avg / avg2) - 1) * 100, 2)

                if mean[kw] > 75 and abs(trend) <= 5:
                    trendiness = "Stable"
                elif mean[kw] > 75 and trend > 5:
                    trendiness = "Increasing"
                elif mean[kw] > 75 and trend < -5:
                    trendiness = "Decreasing"
                elif mean[kw] > 60 and abs(trend) <= 15:
                    trendiness = "Relatively stable"
                elif mean[kw] > 20 and abs(trend) <= 15:
                    trendiness = "Seasonal/Cyclical"
                elif mean[kw] > 20 and trend > 15:
                    trendiness = "Trending"
                elif mean[kw] > 0 and trend > 15:
                    trendiness = "New and trending"
                elif mean[kw] > 0 and trend < -15:
                    trendiness = "Declining"
                else:
                    trendiness = "Undefined"

                keyword_data.append({
                    "Keyword": kw,
                    "Average 5 years interest": mean[kw],
                    "Last year vs. last 5 years trend change (%)": trend,
                    "Trendiness": trendiness
                })
                
                # If successful, break out of the retry loop
                break

            except TooManyRequestsError:
                print(f"Too many requests. Retry attempt {attempt + 1}/3...")
                time.sleep(30)  # Wait for 30 seconds before retrying
                attempt += 1

            except ResponseError as e:
                if "HTTP 400" in str(e):
                    print("Received a 400 error from Google for keyword:", kw)
                    break  # Break out of retry loop for this keyword
                else:
                    raise e

            time.sleep(1)  # Add a small delay between requests to avoid rate limiting

    return keyword_data
