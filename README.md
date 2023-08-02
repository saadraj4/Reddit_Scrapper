# Reddit_Scrapper
Reddit Scraper - Extract data from Reddit with Python. Efficient, customizable, and API-compliant. Parse and store data for analysis. Community-supported. Open-source license.


## Overview
This Python script scrapes Reddit for posts related to specified stocks and sectors. It uses PRAW library to interact with Reddit API and performs sentiment analysis using NLTK's SentimentIntensityAnalyzer. The extracted data is stored in CSV files.

## Requirements
- Internet connection is required to install necessary libraries.
- Ensure you have Python and pip installed.

## Installation
1. Clone the repository.
2. Navigate to the project folder.
3. Run the script: `python main.py`

## Configuration
- Set `client_id` and `client_secret` with your Reddit API credentials.
- Adjust `sectors`, `locations`, `start_date`, and `end_date` as needed.

## Output
- Data without post text: `data without post text.csv`
- Data with post text: `data with post text.csv`

## Note
- Running the script may take some time due to rate limiting by Reddit API.
- Make sure you have NLTK data downloaded (`nltk.download('vader_lexicon')`) before running the script.

## Disclaimer
This script is for educational and research purposes only. Use responsibly and in compliance with Reddit's API terms of service.