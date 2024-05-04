from flask import Flask, render_template, jsonify
from analyze_filings import analyze_ticker_data
import plotly.graph_objects as go

app = Flask(__name__)

# Global variables to store the sentiment data and ticker
global_sentiment_scores = {}
global_ticker = None

# Route to the home page


@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze the sentiment of a given ticker


@app.route('/analyze/<ticker>')
def analyze(ticker):
    global global_sentiment_scores, global_ticker
    try:
        sentiment_scores, global_ticker = analyze_ticker_data(ticker)
        if not sentiment_scores:
            return "No sentiment data available.", 404

        # Normalize sentiment scores to be between -100 and 100
        normalized_scores = {key: float(sentiment_scores[key]) if -100 <= float(sentiment_scores[key]) <= 100 else float(
            sentiment_scores[key]) % 100 if float(sentiment_scores[key]) > 100 else float(sentiment_scores[key]) % -100 for key in sentiment_scores}
        global_sentiment_scores = normalized_scores

        # Return the sentiment scores as JSON
        return jsonify(normalized_scores)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

# Route to plot the sentiment data for a given ticker


@app.route('/plot/<ticker>')
def plot(ticker):
    global global_sentiment_scores, global_ticker

    try:
        # Just get the sentiment scores and ticker values from the above call
        if not global_sentiment_scores or not global_ticker:
            return "Data not analyzed yet.", 400

        # Convert string keys to integers if they are supposed to represent numerical values
        years = list(global_sentiment_scores.keys())
        sentiment_values = list(global_sentiment_scores.values())
        print("Years:", years)
        print("Sentiment values:", sentiment_values)

        fig = go.Figure(data=go.Scatter(
            x=years, y=sentiment_values, text=years))

        fig.update_layout(
            title=f'Sentiment Analysis for {global_ticker}',
            xaxis_title='Document ID',
            yaxis_title='Sentiment Score',
            # Treats the x-axis data as categorical
            xaxis=dict(type='category')
        )

        chart_json = fig.to_json()
        # print(chart_json)  # Check the JSON structure

        return chart_json
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
