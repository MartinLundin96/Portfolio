from helperFunctions import fetch_keyword_data, sort_and_rank, save_to_csv

def main():
    # List of all keywords
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

    # Fetch data
    keyword_data = fetch_keyword_data(all_keywords)

    # Sort and rank data
    sorted_keyword_data = sort_and_rank(keyword_data)

    # Save to CSV
    save_to_csv(sorted_keyword_data, "google_trends_data.csv")

if __name__ == "__main__":
    main()
