from datetime import date
from cnn import CNN

import time
import requests
import os
import json


with open('config.json') as config_file:
    data = config_file.read()

config = json.loads(data)

cnn_url = config["cnn_url"]
discord_webhooks = config["discord_webhooks"]

cnn = CNN(cnn_url)

def check_articles(new_articles, old_articles):
    added = []         
    if len(old_articles) == 0:
        return []

    for article in new_articles:
        found = False

        for old_article in old_articles:
            if article["id"] == old_article["id"]:
                found = True

        if found == False:
            added.append(article) 
    return added

def post_articles(articles):
    for article in articles:
        post_article(article)
        time.sleep(len(articles))

def post_article(article):
    data = {
        "content" : article["headline"],
        "username" : "CNN",
        "avatar_url" : "https://cdn.discordapp.com/avatars/946621745471836240/bf507dbbb7b59a01c976ccf39e3a71e2.webp?size=80",
        "embeds": [
            {
                "title": "New Article",
                "description": article["description"][:4096],
                "footer": {
                    "text": article["author"] + " | FlaringPhoenix#0001"
                },
                "url": cnn.getURL(),
                "color": 15158332
            }
        ]
    }
    for webhook in discord_webhooks:
        post_webhook(webhook, data)
        time.sleep(1)
        print("Posted article to webhook!")

def post_webhook(url, data):
    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

while True:
    print("Fetching articles...")
    old_articles = cnn.getArticles()
    # if len(old_articles) > 0:
    #     del old_articles[0]
    new_articles = cnn.fetchArticles()
    articles = check_articles(new_articles, old_articles)
    if len(articles) > 0:
        print("Found {} new articles!".format(len(articles)))
        post_articles(articles)
    else:
        print("No new articles found!")
    time.sleep(60)