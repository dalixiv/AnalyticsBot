# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


# Parsing Yandex.News
def get_news_results(token):
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'referer': 'https://www.google.com/'}

    r = requests.get(f"https://newssearch.yandex.ru/news/search?from=tabbar&text={token}", headers=headers).text
    soup = BeautifulSoup(r, "lxml")

    for el in soup.find_all("article", class_='news-search-story'):
        try:
            result = {'title': el.find("h3", class_="mg-snippet__title").text,
                      'text': el.find("span", class_="mg-snippet__text").text,
                      'url': el.find("a", class_="mg-snippet__url")['href']}
            results.append(result)
        except AttributeError:
            pass

    return results


# Creating hyperlinks and messages to send
def get_messages(news_result):
    messages = []
    if not news_result:
        return None
    else:
        for news in news_result[:min(len(news_result), 2)]:
            msg = f"<a href='{news['url']}'>{news['title']}</a>\n\n{news['text']}\n\n"
            messages.append(msg)

    return messages


def find_by_token(token):
    return get_messages(get_news_results(token))

