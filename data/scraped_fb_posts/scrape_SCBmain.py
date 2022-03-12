from facebook_scraper import get_posts
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

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'  


# df = pd.DataFrame(columns=['summary','link','article'])
data = {'summary':[], 'link':[], 'article':[], 'title':[], 'time':[]}

name = 'StopClickBaitOfficial'
for i,post in enumerate(get_posts(name, pages=200000)):
  print(i)
  #print(post['image'])
  img_url = post['image']
  img_resp = requests.get(img_url)
  img = Image.open(io.BytesIO(img_resp.content))
  img_string = pytesseract.image_to_string(img)  
  if '.co' not in img_string.lower() and 'net' not in img_string.lower() and '.org' not in img_string.lower():
      print('no! '+img_string)
      continue
  # google the text
  query = img_string.replace("\n", " ")
  for j in search(query, tld="co.in", num=1, stop=1, pause=0):
      url1 = j
  print(post['post_text'])
  article = newspaper.Article(url=url1, language='en')
  try:
    article.download()
    article.parse()
  except Exception as e:
    print(e)
    continue
  print(article.title)
  data['summary'].append(post['post_text'].replace('#StopClickBait','').replace('#SavedYouAClick',''))
  data['link'].append(url1)
  data['article'].append(article.text)
  data['title'].append(article.title)
  data['time'].append(post['time'])
  df = pd.DataFrame.from_dict(data)
  df.to_csv(f'{name}.csv')
#  print(df.summary)
#  pdb.set_trace()

