import requests
import json
import codecs
from bs4 import BeautifulSoup as soup
from datetime import date
from article import Article

class CNN:
    def __init__(self, url):
        self.url = url
        self.articles = []

    def getURL(self):
        return self.url.replace("%DATE%", self.getTime())

    def getTime(self):
        return date.today().strftime("%m-%d-%y")

    def getArticles(self):
        return self.articles

    def fetchArticles(self):
        # Clear articles list
        self.articles = []

        # Request the page
        html = requests.get(self.getURL())
        bsobj = soup(html.content, "html.parser")

        # Find the articles
        for news in bsobj.find_all("article", {"class": "sc-bwzfXH sc-eXEjpC iGQwpp"}):
            id = news.get("id")
            headline = self._find(news, "h2", {"class": "sc-dfVpRl kvaBeP"})
            author = self._find(news, "p", {"class": "sc-gzOgki ixpUvU"})
            # Parse the descriptions
            for description in news.findAll("div", {"class": "sc-bdVaJa post-content-rendered render-stellar-contentstyles__Content-sc-9v7nwy-0 erzhuK"}):
                article = Article(id, headline, author, description.text.strip())
                self.articles.append(article.raw())
                if "has moved here" in description.text.strip():
                    try:
                        self.url = description.find_all('a')[0].get('href')
                        with open('config.json', 'r+') as f:
                            data = json.load(f)
                            data['cnn_url'] = self.url
                            f.seek(0)
                            f.write(json.dumps(data))
                            f.truncate()
                    except BaseException as err:
                        print(f"Unexpected {err=}, {type(err)=} while trying to write to config.json")   
        self.storeArticles()
        return self.articles

    def fetchArticle(self, id):
        for article in self.articles:
            if article.id == id:
                return article

    def storeArticles(self):
        today = date.today()
        formatted_date = today.strftime("%m-%d-%y")

        with open('articles.json'.format(formatted_date), 'wb') as f:
            json.dump({ "articles": self.articles }, codecs.getwriter('utf-8')(f), ensure_ascii=False)
        return

    def _find(self, html, type, args):
        result = html.find(type, args)
        return result.text if result else "N/A"
