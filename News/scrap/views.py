from django.shortcuts import render
from .models import Post
import requests
from bs4 import BeautifulSoup
import datetime

def get_news(date):


def base(request):

    check_date = Post.objects.latest('post_date')

    page = requests.get('https://pasmi.ru/cat/news/')
    soup = BeautifulSoup(page.content, 'html.parser')

    posts = []

    articles = soup.find_all('article')
    for article in articles:
        post = {}
        post_date = article.find('span').get_text()
        post_date_time = datetime.datetime.strptime(post_date, '%d.%m.%Y / %H:%M')
        post_title = article.find('h1').get_text()
        post_link = article.find('a')['href']

        if post_date_time > check_date.post_date or check_date == NULL:
            posts.append(Post(post_date = post_date_time, post_title = post_title, post_link = post_link))

        elif post_date_time < check_date.post_date:
            break
        # print("заголовок", post_title)
        # print("дата", post_date)
        # print("ссылка", post_link)
        #
        # post_page = requests.get(post_link)
        # page_soup = BeautifulSoup(post_page.content, 'html.parser')
        #
        # content = page_soup.find("div", class_='content')
        # paragraphs = content.find_all('p')
        #
        # for i in range(len(paragraphs)-2):
        #     paragraph = paragraphs[i].get_text()
        #     print(paragraph)
        #     print()

    Post.objects.bulk_create(posts)

    q = Post.objects.all().order_by('post_date')[:int(requests.GET['period'])]

    return render (request, 'scrap/base.html', q)
