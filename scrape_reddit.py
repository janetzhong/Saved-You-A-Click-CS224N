# EXPORTS CSV FILE WITH ALL SPECIFIED REDDIT POSTS 
# outputs to data > scraped_posts 
# expect runtime of ~30 minutes per 1000 posts scraped
# Modified from bilsun/reddit-scraper

import json
import praw
import pandas as pd
import datetime as dt
import requests
import time
import re 
import csv
start_time = time.time()

# load Reddit authentication for PRAW
# reference: https://www.storybench.org/how-to-scrape-reddit-with-python/
credentials = {}
with open('pwd.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        credentials[row[0]]=row[1]
reddit = praw.Reddit(client_id=credentials['client_id'], 
                     client_secret=credentials['client_secret'],
                     user_agent=credentials['user_agent'],
                     username=credentials['username'],
                     password=credentials['password'])

# building the Pushshift API request for data collection
keywords = ''
subreddits = 'savedyouaclick' 
submission_fields = 'id,score,full_link,subreddit,title,selftext,created_utc,author,num_comments,url' 
earliest_date = 1643784604 # 1 Feb 2022 @ 12am | https://www.unixtimestamp.com/index.php
# Will need to change this to earlier once we have figured out the entire workflow

# specify file name for exported csv (change between runs to prevent overwriting existing data)
exported_file_name = 'scraped_reddit_posts'

# -----------------------------------------------

# function that formats text for readability 

def clean_text(text):
    text = text.strip()
    text = re.sub('\n+', '\n', text)
    text = re.sub('&amp;', '&', text)
    text = re.sub('&lt;', '<', text)
    text = re.sub('&gt;', '>', text)
    text = re.sub('&#x200B;', '', text)
    text = re.sub('&nbsp;', ' ', text)
    return text

# -----------------------------------------------

# search Reddit submissions (posts) using Pushshift
# reference: https://github.com/pushshift/api#searching-submissions
url = f"https://api.pushshift.io/reddit/search/submission/?q={keywords}&subreddit={subreddits}&fields={submission_fields}&after={earliest_date}&size=1000&sort=desc&metadata=true"
print(url)
# paginating results (collect 1000 posts at a time to work around Pushshift's size limit)
start_from = ''
first_pass = True
data = []
while True:
    if first_pass: 
        print("collecting Reddit data...")
        request = requests.get(url+start_from)
        posts = request.json()
        print("keywords: " + keywords + " | " + str(posts['metadata']['total_results']) + " posts found")
        first_pass = False
    else:
        request = requests.get(url+start_from)
        posts = request.json()
    
    # make sure Pushshift is gathering all Reddit data (IMPORTANT IF SCRAPING FOR RESEARCH)
    #print(posts['metadata']['shards']["total"])
    #assert(posts['metadata']['shards']["successful"]==posts['metadata']['shards']["total"]) 
    
    data.extend(posts["data"])
    if len(posts["data"]) == 0:
		    break # stop collecting data once there's nothing left to collect
    last_utc = data[-1]['created_utc']
    start_from = '&before=' + str(last_utc)

print("successful data collection!\n")

# -----------------------------------------------

# clean/format data and update scores with PRAW for more up-to-date stats
print("cleaning and formatting data...\n")
i = 0
for d in data:

    if (i%10==0):
        print(i)
    i+=1

    # get data from PRAW based on unique post ID from Pushshift
    submission = reddit.submission(id=d['id'])
    submission.comment_sort = 'top'
    d.update({'url': submission.url})
    d.update({'score': submission.score})
    d.update({'post keywords': keywords}) # for reference in csv
    d.update({'date': dt.datetime.fromtimestamp(d['created_utc']).date()})
    try:
        d.update({'comment_score': submission.comments[0].score})
        d.update({'top_comment': clean_text(submission.comments[0].body)})
    except:
        d.update({'comment_score': "N/A"})
        d.update({'top_comment': "N/A"})
    d.update({'title': clean_text(d.get("title","N/A"))})
    d.update({'selftext': clean_text(d.get("selftext","N/A"))})

# -----------------------------------------------
    
# final formatting and exporting scraped posts to csv
column_order = ['title', 'url', 'full_link', 'id', 'date', 'score', 'num_comments', 'author', 'selftext', 'top_comment', 'comment_score']
df = pd.DataFrame.from_records(data, columns=column_order).drop_duplicates()
df = df.sort_values(['score', 'comment_score'], ascending=False) # sort by updated scores in csv
df.to_csv(f'./data/scraped_posts/{exported_file_name}.csv', index=False, header=True)

# -----------------------------------------------

runtime = '{:.0f}'.format(time.time() - start_time)
print(f"--- DONE! runtime: {runtime} seconds ---")
print("see data > scraped_posts for exported csv \n")
