from django.shortcuts import render
from .models import Post
import requests
from bs4 import BeautifulSoup
import datetime

def base(request):

    page = requests.get('https://pasmi.ru/cat/news/')
    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all('article')

    check_date = Post.objects.filter().order_by('post_date').last()
    posts = Post.objects.all()[:50]
    posts_names = []
    for new in posts:
        posts_names.append(new.post_title)

    if check_date:
        print('@@@@@@@@@@@@@')
        for article in articles:
            post_date = article.find('span').get_text()
            post_date_time = datetime.datetime.strptime(post_date[:10], '%d.%m.%Y').date()
            post_title = article.find('h1').get_text()
            post_link = article.find('a')['href']

            if post_date_time < check_date.post_date:
                break

            elif post_date_time > check_date.post_date:
                new_post = Post(post_date = post_date_time, post_title = post_title, post_link = post_link)
                new_post.save()

            elif post_date_time == check_date.post_date:
                if post_title in posts_names:
                    continue
                else:
                    new_post = Post(post_date = post_date_time, post_title = post_title, post_link = post_link)
                    new_post.save()
        print(posts)
    else:
        print("!!!!!!!!!!!")
        for article in articles:
            post = {}
            post_date = article.find('span').get_text()
            post_date_time = datetime.datetime.strptime(post_date[:10], '%d.%m.%Y').date()
            post_title = article.find('h1').get_text()
            post_link = article.find('a')['href']
            new_post = Post(post_date = post_date_time, post_title = post_title, post_link = post_link)
            new_post.save()

    try:
        period = int(request.GET['period'])
    except:
        q = Post.objects.all().order_by('post_date')[::-1][:20]
    else:
        q = Post.objects.all().order_by('post_date')[::-1][:period]

    print(q)

    return render (request, 'scrap/base.html', context= {'q':q})
