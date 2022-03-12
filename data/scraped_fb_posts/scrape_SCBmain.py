from facebook_scraper import get_posts, FacebookScraper
import newspaper
import pdb
import datetime
import pandas as pd
import io
import requests
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
from googlesearch import search
from newspaper import Config
import random, requests
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'  

fs = FacebookScraper()
fs.login('LOGIN','PASSWORD')

# try to bypass time out error
user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

data = {'summary':[], 'img_string':[], 'link':[], 'article':[], 'title':[], 'time':[]}

name = 'StopClickBaitOfficial'
for i,post in enumerate(get_posts(name, pages=10000)):
  print(i)
  try: 
      #print(post['image'])
      img_url = post['image']
      img_resp = requests.get(img_url, timeout=2)
      img = Image.open(io.BytesIO(img_resp.content))
      img_string = pytesseract.image_to_string(img)  
      if '.co' not in img_string.lower() and 'net' not in img_string.lower() and '.org' not in img_string.lower():
          print('no! '+img_string)
          continue
      data['img_string'].append(img_string)
      # google the text
      query = img_string.replace("\n", " ")
      print(query)
      for j in search(query, user_agent = random.choice(user_agent_list), tld="co.in", num=1, stop=1, pause=0):
          print(j)
          url1 = j
      print(post['post_text'])
      article = newspaper.Article(url=url1, language='en')
      article.download()
      article.parse()
      print(article.title)
      data['summary'].append(post['post_text'].replace('#StopClickBait','').replace('#SavedYouAClick',''))
      data['link'].append(url1)
      data['article'].append(article.text)
      data['title'].append(article.title)
      data['time'].append(post['time'])
      df = pd.DataFrame.from_dict(data)
      df.to_csv(f'{name}.csv')
#      print(df.summary)
#      pdb.set_trace()
  except:
      pass
#  print(df.summary)
#  pdb.set_trace()

