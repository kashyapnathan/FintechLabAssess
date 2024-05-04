# file: download_filings.py
from sec_edgar_downloader import Downloader
import os


def download_10k_filings(tickers, start_year, end_year):
    email = "kashyapnathan2@gmail.com"  # Replace with your actual email address
    dl = Downloader(os.path.expanduser("~/sec_filings"), email)
    for ticker in tickers:
        for year in range(start_year, end_year + 1):
            dl.get("10-K", ticker,
                   after=f"{year}-01-01", before=f"{year}-12-31")


if __name__ == "__main__":
    companies = ['AAPL', 'MSFT', 'AMZN']  # Example companies
    download_10k_filings(companies, 1995, 2023)
