import requests


def get_game_info(app_id):
    # Fetch game details from Steam API
    steam_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(steam_url)

    if response.status_code != 200:
        print("Failed to retrieve app details.")
        return None

    data = response.json().get(str(app_id), {}).get("data", {})
    if not data:
        print("Game data not found.")
        return None

    # Extract basic information
    title = data.get("name", "N/A")
    price_info = data.get("price_overview", {})
    price = price_info.get("final_formatted", "Free" if data.get("is_free") else "N/A")

    # Fetch review counts and score from SteamSpy API
    steamspy_url = f"https://steamspy.com/api.php?request=appdetails&appid={app_id}"
    steamspy_response = requests.get(steamspy_url)

    if steamspy_response.status_code != 200:
        print("Failed to retrieve review data from SteamSpy.")
        return {
            "title": title,
            "price": price,
            "positive_reviews": "Unavailable",
            "negative_reviews": "Unavailable",
            "total_reviews": "Unavailable",
            "overall_score": "Unavailable"
        }

    review_data = steamspy_response.json()

    
    positive_reviews = review_data.get("positive", 0)
    negative_reviews = review_data.get("negative", 0)
    total_reviews = positive_reviews + negative_reviews
    overall_score = (positive_reviews / total_reviews) * 100 if total_reviews > 0 else 0

    return {
        "title": title,
        "price": price,
        "positive_reviews": positive_reviews,
        "negative_reviews": negative_reviews,
        "total_reviews": total_reviews,
        "overall_score": f"{overall_score:.2f}%"
    }


