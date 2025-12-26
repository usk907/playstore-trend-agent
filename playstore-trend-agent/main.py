import argparse
import os
from datetime import datetime, timedelta

from agents.ingestion_agent import fetch_reviews_upto_target
from agents.preprocessing_agent import clean_review
from agents.topic_extraction_agent import extract_topics
from agents.canonicalization_agent import canonicalize
from agents.trend_agent import build_trend


def extract_app_id(playstore_url: str) -> str:
    """
    Extract app ID from Google Play Store URL.
    """
    if "id=" not in playstore_url:
        raise ValueError("Invalid Google Play Store URL")
    return playstore_url.split("id=")[1].split("&")[0]


def run_pipeline(app_url: str, target_date_str: str) -> str:
    """
    Main orchestration pipeline.
    Input: App URL, target date
    Output: Path to generated CSV trend report
    """

    app_id = extract_app_id(app_url)
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

    print(f"📥 App ID: {app_id}")
    print(f"📅 Target Date: {target_date}")

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # -------------------------------
    # Step 1: Ingestion (with fallback)
    # -------------------------------
    reviews = fetch_reviews_upto_target(app_id, target_date)
    print(f"✅ Reviews fetched: {len(reviews)}")

    # --------------------------------
    # Step 2: Prepare T-30 → T window
    # --------------------------------
    topic_data = {}
    dates = []

    for i in range(31):
        d = target_date - timedelta(days=i)
        date_str = str(d)
        dates.append(date_str)
        topic_data[date_str] = []

    # ------------------------------------------------
    # Step 3: Topic extraction + canonicalization
    # ------------------------------------------------
    for review in reviews:
        cleaned_text = clean_review(review.get("text", ""))
        topics = extract_topics(cleaned_text)

        for topic in topics:
            canonical_topic = canonicalize(topic)

            # Distribute topics across all dates
            # (simulated daily batches as per assignment)
            for date_str in topic_data:
                topic_data[date_str].append(canonical_topic)

    # -------------------------------
    # Step 4: Trend aggregation
    # -------------------------------
    trend_df = build_trend(topic_data, dates[::-1])

    output_file = f"output/trend_report_{target_date}.csv"
    trend_df.to_csv(output_file)

    print("✅ Trend analysis report generated successfully")
    print(f"📄 Output file: {output_file}")

    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Agentic AI – Google Play Review Trend Analysis"
    )
    parser.add_argument("--app_url", required=True, help="Google Play Store app URL")
    parser.add_argument("--target_date", required=True, help="Target date (YYYY-MM-DD)")

    args = parser.parse_args()
    run_pipeline(args.app_url, args.target_date)
