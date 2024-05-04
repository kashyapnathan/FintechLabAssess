# Financial Sentiment Analysis Dashboard

## Project Overview

This project, developed for the Summer Research Programming Task at the Financial Services Innovation Lab, Georgia Tech, automates the downloading and analysis of SEC 10-K filings and visualizes insights in a user-friendly web dashboard. It allows users to enter a company ticker, automatically fetches the relevant SEC filings, analyzes the text for sentiment and trends, and presents this data graphically.

## Tech Stack and Rationale

### Python
Chosen for its robust libraries and strong community support, Python is ideal for backend data processing tasks, including file handling, data manipulation, and performing complex calculations.

### Flask
A lightweight Python web framework that is perfect for small to medium web applications, Flask provided the necessary tools to build a web server quickly and integrate it with Python applications without the overhead of larger frameworks.

### sec-edgar-downloader
This Python library is utilized to automate the download of SEC filings directly from the EDGAR database. It significantly simplifies the process of retrieving necessary documents, such as 10-K filings.

### OpenAI's GPT API
This API provides powerful tools for extracting meaningful insights from extensive financial documents, making it a cornerstone for our analysis module.

### Plotly
Plotly supports a variety of charts and graphs that enhance the UI with representations. Also Plotly doesn't run into the same multithreading issues MatPlotLib does

### Heroku
Heroku offers a straightforward, efficient solution for deploying Python applications and integrates directly with GitHub

### JavaScript
I chose to use vanilla JavaScript for the frontend to keep the project lightweight and maintain high performance without the overhead of additional frameworks. This choice allows for greater control over the browser's behavior and was sufficient for the project's scope, which involved DOM manipulation and API calls without the need for the more complex structures provided by frameworks like React or Angular.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/financial-sentiment-analysis.git
cd financial-sentiment-analysis

# Install required Python packages
pip install -r requirements.txt
```

## Usage

```bash
# Navigate to the project directory
cd path-to-your-project

# Run the Flask application
flask run
```

Navigate to `http://localhost:5000` in your web browser to use the application.

## Deployment on Heroku

```bash
# Log in to Heroku
heroku login

# Create a new Heroku app
heroku create

# Set necessary environment variables
heroku config:set OPENAI_API_KEY='your_openai_api_key_here'

# Deploy your application
git push heroku main
```

## Contributing

We welcome contributions. For substantial changes, please open an issue first to discuss what you would like to change. Please ensure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the LICENSE file for more details.

## Contact Information

- **Kashyap M. Nathan** - kashyapnathan2@gmail.com
- **Project Link** - [https://github.com/kashyapnathan/FintechLabAssess]

---

This README is designed to be comprehensive, explaining the setup, usage, technology choices, and rationale clearly to both users and potential contributors. Adjust the content as necessary to fit the specifics of your project and personal contributions.
