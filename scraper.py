import re
import csv
import json
import requests
from bs4 import BeautifulSoup

def get_news(file):
    urls=[]
    with open(file) as fh :
        csv_urls = csv.reader(fh, delimiter=' ', quotechar='|')
        for url in csv_urls:
            urls.append(url[0])
    return urls
        

def get_html(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error:{response.status_code}")
    

def scrape_post(html):
        soup = BeautifulSoup(html, 'html.parser')

        post_title = soup.select_one('div.container.single-post > h2').text
        post_image = soup.select_one('div.container.single-post > div.img_16x9 > figure')['data-href']
        post_content = soup.select_one('div.container.single-post > div.inner-container > div.post-content.single-post-content').text

        return  {'title': post_title, 'image': post_image, 'content':post_content}
    
def get_posts(urls):
    posts = []
    if len(urls) == 0:
        raise Exception('URLs list is empty!')
    
    for url in urls:
        try:
            html = get_html(url)
            post = scrape_post(html)
            posts.append(post)
        except Exception as e:
            print(e)

    return posts

def save_posts(posts, file):
    if len(posts)== 0:
        raise Exception('Post list is empty!')
    
    with open(file, 'w') as fh:
        json.dump(posts, fh)
    
    print('Done')


try:
    urls= get_news('news.csv')
    posts = get_posts(urls)
    save_posts(posts,'posts.json')


except Exception as e :
    print(e)




