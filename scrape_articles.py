
# make sure to install: pip install newspaper3k
# see https://www.geeksforgeeks.org/scraping-websites-with-newspaper3k-in-python/

# Import required module
import newspaper
import csv
from newspaper import Config
from newspaper import Article
from os.path import exists
import pandas as pd

# TODO What is this
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10
 
# get URL's from the scraped reddit data
df = pd.read_csv("data/scraped_posts/scraped_reddit_posts.csv", usecols = ['url'])
list_of_urls= df['url'].values.tolist()

# modified from https://stackoverflow.com/questions/69711582/newspaper3k-export-to-csv-on-first-row-only
index=0
for url in list_of_urls:
    print(index)
    index+=1
    try:
        article = newspaper.Article(url,config=config)
        article.download()
        article.parse()
        article_meta_data = article.meta_data
    except:
        article.text = None #TODO not sure what to put if it fails
    
    #Write to file [url, article text]
    file_exists = exists('data/scraped_posts/scraped_articles.csv')
    if not file_exists:
        with open('data/scraped_posts/scraped_articles.csv', 'w', newline='',encoding='utf-8') as file:
            headers = ['URL' , 'article text']
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            writer.writerow({'URL': url,
                             'article text': article.text})
    else:
        with open('data/scraped_posts/scraped_articles.csv', 'a', newline='',encoding='utf-8') as file:
            headers = ['URL' , 'article text']
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writerow({'URL': url,
                             'article text': article.text})