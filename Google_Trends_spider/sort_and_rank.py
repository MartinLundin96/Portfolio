def sort_and_rank(keyword_data):
    sorted_keyword_data = sorted(keyword_data, key=lambda x: x["Last year vs. last 5 years trend change (%)"], reverse=True)
    return sorted_keyword_data
