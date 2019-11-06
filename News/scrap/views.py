from django.shortcuts import render
from .models import Post
import requests
from bs4 import BeautifulSoup
import datetime

def base(request):

    page = requests.get('https://pasmi.ru/cat/news/')
    soup = BeautifulSoup(page.content, 'html.parser')

    posts = []

    articles = soup.find_all('article')

    try:
        check_date = Post.objects.order_by('post_date').first()
        print(check_date)
    except:
        print("!!!!!!!!!!!")
        for article in articles:
            post = {}
            post_date = article.find('span').get_text()
            post_date_time = datetime.datetime.strptime(post_date, '%d.%m.%Y / %H:%M')
            post_title = article.find('h1').get_text()
            post_link = article.find('a')['href']
            posts.append(Post(post_date = post_date_time, post_title = post_title, post_link = post_link))
    else:
        print('@@@@@@@@@@@@@')
        for article in articles:
            post = {}
            post_date = article.find('span').get_text()
            post_date_time = datetime.datetime.strptime(post_date, '%d.%m.%Y / %H:%M')
            print(post_date_time)
            if post_date_time < check_date.post_date:
                break
            else:
                post_title = article.find('h1').get_text()
                post_link = article.find('a')['href']
                posts.append(Post(post_date = post_date_time, post_title = post_title, post_link = post_link))

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

    Post.objects.bulk_create(posts, ignore_conflicts = True)

    try:
        period = int(request.GET['period'])
    except:
        q = Post.objects.all().order_by('post_date')[:20]
    else:
        q = Post.objects.all().order_by('post_date')[:period]

    return render (request, 'scrap/base.html', context= {'q':q})
