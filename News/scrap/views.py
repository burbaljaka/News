from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def base(request):
    page = requests.get('https://pasmi.ru/cat/news/')
    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.find_all('article')
