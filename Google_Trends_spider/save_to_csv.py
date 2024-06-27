# save_to_csv.py

import csv

def save_to_csv(sorted_keyword_data, filename):
    # Sort by Average 5 years interest (descending)
    sorted_keyword_data = sorted(sorted_keyword_data, key=lambda x: x["Average 5 years interest"], reverse=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Keyword", "Average 5 years interest", "Last year vs. last 5 years trend change (%)", "Trendiness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for keyword in sorted_keyword_data:
            writer.writerow({
                "Keyword": keyword["Keyword"],
                "Average 5 years interest": f"{keyword['Average 5 years interest']:.2f}%",  # Format as percentage with 2 decimal places
                "Last year vs. last 5 years trend change (%)": f"{keyword['Last year vs. last 5 years trend change (%)']:.2f}%",  # Format as percentage with 2 decimal places
                "Trendiness": keyword["Trendiness"]
            })

    print(f"Data saved to {filename}")
