# A script to retreive data of posts from Reddit's WallStreetBets subreddit regarding AMC and GME stocks around the time of the short squeeze.

import os
import praw
import json
from datetime import datetime

reddit = praw.Reddit(
    client_id='QKU9XbGvYaH4djTFMJOFuQ',
    client_secret='YcTUcHhpQoY0Iy3dPglOHHbI3_nmtw',
    user_agent='data scraper for sentiment analysis of WallStreetBets data',
    username='tyler_cartw',
    password='tylerreece1'
)

print(f"Authenticated as: {reddit.user.me()}")

subreddit = reddit.subreddit("wallstreetbets")

print(f"Searching Subreddit: {subreddit.display_name}")

# Define your query and time period (example dates)
query = ['GME', 'AMC', 'GameStop', 'AMC Entertainment']
print(f"Search query tags: {query}")

start_date = int(datetime(2021, 1, 1).timestamp())
end_date = int(datetime(2021, 2, 28).timestamp())
print(f"Search date range: {datetime.fromtimestamp(start_date)} to {datetime.fromtimestamp(end_date)}")

# Store posts data
posts_data = []

# Fetch and filter posts
total_post_counter = 0
relevant_post_counter = 0
for ticker in query:
    for post in subreddit.search(ticker, limit=1000):  # Adjust limit as needed
        total_post_counter += 1
        created_date = int(post.created_utc)
        if start_date <= created_date <= end_date:
            if post.selftext == '[removed]' or post.selftext == '[deleted]' or post.selftext == '':
                continue
            else:
                relevant_post_counter += 1
                posts_data.append({
                    "title": post.title,
                    "text": post.selftext,
                    "upvotes": post.score,
                    "num_comments": post.num_comments,
                    "post_url": post.url,
                    "created_utc": created_date
                })

print(f"Total posts found: {total_post_counter}")
print(f"Total relevant posts found: {relevant_post_counter}")

# Save data to a JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
os.makedirs(data_dir, exist_ok=True)
json_file_path = os.path.join(data_dir, 'wallstreetbets_posts.json')

with open(json_file_path, 'w') as json_file:
    json.dump(posts_data, json_file, indent=4)

print("Data extraction complete. Saved to wallstreetbets_posts.json")