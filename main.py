# You need an Internet connection to run this script as it also installs the necessary libraries to run the script

import subprocess
import os
import platform
import nltk
import time
from datetime import datetime
import socket

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def is_internet_connected():
    try:
        # Attempt to create a socket connection to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        print('Internet connection is established')
        return True
    except OSError:
        # If the connection attempt fails, it means the internet is not connected
        print("\033[31mInternet is not connected,Please try again!\033[0m")
        return False

if is_internet_connected():
    clear_screen()
    # Installing required packages and Libraries
    required_packages = ['praw', 'nltk', 'pandas', 'numpy']
    for package in required_packages:
        try:
            subprocess.check_call(['pip', 'install', package], bufsize=0)
            print(f"Successfully installed {package}")
            # Clear the screen after installation
            clear_screen()
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
    nltk.download('vader_lexicon')
else:
    exit()


import pandas as pd
import praw
from nltk.sentiment import SentimentIntensityAnalyzer
clear_screen()



# Initialize the Reddit API wrapper
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='MyRedditScraper',
                     )

# Define the stock keywords and sectors
technology_stocks = {'AAPL': 'Apple', 'MSFT': 'Microsoft', 'AMZN': 'Amazon'}
financial_stocks = {'JPM': 'JP Morgan', 'BAC': 'Bank of America', 'V': 'Visa'}
healthcare_stocks = {'JNJ': 'Johnson & Johnson', 'PFE': 'Pfizer', 'MRK': 'Merck & Co'}

sectors = {
    'Technology': technology_stocks,
    'Financial': financial_stocks,
    'Healthcare': healthcare_stocks
}
# Specify the geographical locations
locations = ['Americas', 'Europe', 'Africa', 'Asia', 'Other','']


# Specify the time range for data retrieval
start_date = 1262286000  # January 1, 2010, in Unix timestamp
end_date = 1672513140  # December 31, 2022, in Unix timestamp

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# creating list to store the data
data = []
data_text = []
# Retrieve posts and perform sentiment analysis
iterator = 1
for sector, stocks in sectors.items():
    for stock_symbol, stock_name in stocks.items():
        for location in locations:
            query = f'{stock_name}'        # Query to extract the data
            subreddit_posts = reddit.subreddit('all').search(query, syntax='cloudsearch')
            for post in subreddit_posts:
                post_text = post.title + ' ' + post.selftext            # Combine post title and selftext
                date = datetime.fromtimestamp(post.created_utc)         # Getting time of post was made
                formatted_date = date.strftime("%m/%d/%Y")              # Format: "mm-dd-yyyy"
                formatted_time = date.strftime("%H:%M:%S")              # Format: "hh:mm:ss"
                title = post.title                                      # Getting title of the post
                text = title +' '+ post.selftext                        # Taking the content of the post
                post_url = post.url                                     # Getting link to the post
                author_name = post.author.name                          # Getting username of author
                comments = post.num_comments                            # Getting number of comment on the post
                print(iterator)
                iterator = iterator+1
                # Perform sentiment analysis
                sentiment_scores = sia.polarity_scores(post_text)
                sentiment_negative = sentiment_scores['neg']        # Negative sentiment score
                sentiment_neutral = sentiment_scores['neu']         # Neutral sentiment score
                sentiment_positive = sentiment_scores['pos']        # Positive sentiment score
                sentiment_compound = sentiment_scores['compound']   # Compound sentiment score

                # Append the extracted data withOUT post text to the list data
                data.append({
                    'Stock': stock_name,
                    'Post Title': title,
                    'Sentiment Negative': sentiment_compound,
                    'Sentiment Neutral':  sentiment_compound,
                    'Sentiment Positive': sentiment_compound,
                    'Sentiment Compound': sentiment_compound,
                    'Post URL': post_url,
                    'Date': formatted_date,
                    'Time': formatted_time,
                    'Post author': author_name,
                    'Comments': comments,
                    'Location': location,
                })

                # Append the extracted data with post text to the list data_text
                data_text.append({
                    'Stock': stock_name,
                    'Post Title': title,
                    'Post Text': text,
                    'Sentiment Negative': sentiment_compound,
                    'Sentiment Neutral':  sentiment_compound,
                    'Sentiment Positive': sentiment_compound,
                    'Sentiment Compound': sentiment_compound,
                    'Post URL': post_url,
                    'Date': formatted_date,
                    'Time': formatted_time,
                    'Post author': author_name,
                    'Comments': comments,
                    'Location': location,
                })
            time.sleep(2)


# Converting the data to dataframe
dataframe = pd.DataFrame(data)
# Save to csv file
dataframe.to_csv('data without post text.csv', index = False)
dataframe = pd.DataFrame(data_text)
dataframe.to_csv('data with post text.csv', index = False)


print("\033[32mExtracted Data stored to CSV file.\033[0m")

