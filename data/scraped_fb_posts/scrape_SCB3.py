from facebook_scraper import get_posts, FacebookScraper
import newspaper
import pdb
import datetime
import pandas as pd

# df = pd.DataFrame(columns=['summary','link','article'])
data = {'summary':[], 'link':[], 'article':[], 'title':[], 'time':[]}

name = 'SCBLifestyle'
try:
  # for i,post in enumerate(get_posts(name, pages=20000, credentials=('lbc45123@hotmail.com','54lbc123'))):
  for i,post in enumerate(fs.get_posts(name, pages=20000)):
    if post['link'] is None or len(post['post_text'])==0:
      continue
    # print(i,post['text'][:50])
    # if i==19:
    # pdb.set_trace()
    print(i)
    print(post['post_text'])
    print(post['link'])
    article = newspaper.Article(url=post['link'], language='en')
    try:
      article.download()
      article.parse()
    except Exception as e:
      print(e)
      continue
    # print(article.text)
    data['summary'].append(post['post_text'].replace('#StopClickBait','').replace('#SavedYouAClick',''))
    data['link'].append(post['link'])
    data['article'].append(article.text)
    data['title'].append(article.title)
    data['time'].append(post['time'])
    # pdb.set_trace()
  df = pd.DataFrame.from_dict(data)
  df.to_csv(f'{name}.csv')
  print(df.summary)
  pdb.set_trace()
except:
  df = pd.DataFrame.from_dict(data)
  df.to_csv(f'{name}.csv')
