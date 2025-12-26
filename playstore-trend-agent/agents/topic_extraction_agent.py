def extract_topics(review_text: str):
    """
    Offline fallback topic extractor.
    Deterministic, high-recall, no external API dependency.
    """

    if not review_text:
        return ["general feedback"]

    topics = []
    text = review_text.lower()

    if "late" in text or "delay" in text:
        topics.append("delivery delay")

    if "rude" in text or "impolite" in text or "badly" in text:
        topics.append("delivery partner rude")

    if "stale" in text or "spoiled" in text or "bad food" in text:
        topics.append("food quality issue")

    if "map" in text or "location" in text:
        topics.append("maps not working properly")

    if "price" in text or "costly" in text or "expensive" in text:
        topics.append("pricing issue")

    if not topics:
        topics.append("general feedback")

    return topics
