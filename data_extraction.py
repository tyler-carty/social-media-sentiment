import os
import praw
import csv
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

start_date = int(datetime(2021, 1, 1).timestamp())
end_date = int(datetime(2021, 8, 31).timestamp())
print(f"Search date range: {datetime.fromtimestamp(start_date)} to {datetime.fromtimestamp(end_date)}")

posts_data = []

for post in subreddit.search(limit=None):
    created_date = int(post.created_utc)
    if start_date <= created_date <= end_date:
        if post.selftext == '[removed]' or post.selftext == '[deleted]' or post.selftext == '':
            continue
        post_data = [
            post.title,
            post.score,
            post.id,
            post.url,
            post.num_comments,
            datetime.fromtimestamp(post.created_utc),
            post.selftext,
            post.created_utc
        ]
        posts_data.append(post_data)

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
csv_file_path = os.path.join(script_dir, 'wallstreetbets_posts.csv')

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['title', 'score', 'id', 'url', 'comms_num', 'created', 'body', 'timestamp'])
    csv_writer.writerows(posts_data)

print(f"Total posts found: {len(posts_data)}")
print("Data extraction complete. Saved to reddit_wsb.csv")