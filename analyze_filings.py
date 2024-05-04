import openai
import os
from pathlib import Path
from sec_edgar_downloader import Downloader
import matplotlib.pyplot as plt
import json
import re

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

all_out = []


def download_10k_filings(tickers, start_year=1995, end_year=2023):
    email = "kashyapnathan2@gmail.com"  # Replace with your actual email address
    dl = Downloader(os.path.expanduser("~/sec_filings"), email)
    for ticker in tickers:
        for year in range(start_year, end_year + 1):
            dl.get("10-K", ticker,
                   after=f"{year}-01-01", before=f"{year}-12-31")


def analyze_text(text):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="As a skilled financial analyst, you are adept at interpreting financial documents. "
            "Please analyze the text below and assign a sentiment score between -100 (very negative) "
            "and +100 (very positive), based strictly on the financial implications mentioned in the text. "
            "Conclude with a numeric sentiment score followed by a brief explanation of why this insight is "
            "valuable for an investor or financial analyst. Here's the text: " +
            text,  # Added text to the prompt
            max_tokens=300  # Increased max tokens for more content analysis
        )
        output = response.choices[0].text.strip()
        print(output)
        all_out.append(output)

        # Improved regex to capture both floats and integers
        match = re.search(r"(-?\d+\.?\d*)", output)
        if match:
            return match.group(1)  # Return the first numeric match
        else:
            print("No numeric score found in the output.")
            return None
    except Exception as e:
        print(f"Failed to analyze text: {e}")
        return None


def load_and_analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # Adjusted limit for more content analysis
        return analyze_text(content[:5000])
    except Exception as e:
        print(f"Error loading or analyzing file {file_path}: {e}")
        return None


def plot_sentiment(sentiment_data, file_name):
    try:
        # Convert string keys to integers if they are supposed to represent numerical values
        sections = list(range(len(sentiment_data)))
        # Extract sentiment values if they are between -100 and 100 if not, set to x % 100 or x % -100 respectively
        sentiments = [float(sentiment_data[key]) if -100 <= float(sentiment_data[key]) <= 100 else float(
            sentiment_data[key]) % 100 if float(sentiment_data[key]) > 100 else float(sentiment_data[key]) % -100 for key in sentiment_data]

        # Diagnostic print
        print("Sections (x):", sections)
        print("Sentiments (y):", sentiments)

        plt.figure(figsize=(10, 5))
        plt.plot(sections, sentiments, marker='o', linestyle='-',
                 color='blue')  # Explicitly setting color and line style
        plt.title('Sentiment Trend in 10-K Filing')
        plt.xlabel('Year')
        plt.ylabel('Sentiment Score')

        # Check if the axes ranges are appropriate for the data
        plt.xlim(0, max(sections)+1)
        plt.ylim(min(sentiments)-0.01, max(sentiments)+0.01)

        image_path = f"{file_name}_sentiment.png"
        plt.savefig(f"{file_name}_sentiment.png")
        plt.close()
        return image_path
    except Exception as e:
        print(f"Error in plotting sentiment: {e}")


def analyze_ticker_data(ticker):
    base_path = Path("./sec-edgar-filings")  # Base path to the filings
    # Path to the 10-K filings for the ticker
    ticker_path = base_path / ticker / "10-K"

    if not ticker_path.exists() or not ticker_path.is_dir():
        download_10k_filings([ticker])
        analyze_ticker_data(ticker)

    sentiment_scores = {}

    # Loop through each year's folder under the ticker's 10-K directory
    for year_dir in ticker_path.iterdir():
        if year_dir.is_dir():
            for filing in year_dir.glob("full-submission.txt"):
                sentiment_result = load_and_analyze_file(filing)
                if sentiment_result:
                    sentiment_scores[year_dir.name] = float(sentiment_result)
                else:
                    sentiment_scores[year_dir.name] = 0.0

    if not sentiment_scores:
        return {"error": "Failed to analyze any filings for this ticker."}

    return sentiment_scores, ticker


# if __name__ == "__main__":
#     result = analyze_ticker_data("PLTR")
#     # print(json.dumps(result, indent=2))
#     plot_sentiment(result, 'AAPL_10K_Sentiment')
