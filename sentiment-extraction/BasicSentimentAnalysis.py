import os
import json
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

# Analyse the sentiment of the posts using the VADER sentiment analysis tool

sia = SentimentIntensityAnalyzer()

# Save data to a JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
json_file_path = os.path.join(script_dir, 'wallstreetbets_posts.json')

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

for post in data:
    # Analyze sentiment of the post
    post_text = post.get('text', '')
    post['sentiment'] = sia.polarity_scores(post_text)['compound']

    # Check if comments exist and analyze their sentiment
    if 'comments' in post:
        for comment in post['comments']:
            comment_text = comment.get('body', '')
            comment['sentiment'] = sia.polarity_scores(comment_text)['compound']

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)