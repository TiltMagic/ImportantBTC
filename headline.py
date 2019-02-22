import newspaper
import random
from newspaper import Article


class Newspaper:
    article_titles_urls = []
    article_urls = []

    def __init__(self, source_url):
        # Builds newspaper object without caching
        self.newspaper = newspaper.build(source_url, memoize_articles=False)

    def build_article_titles_urls(self, max=20):
        # Retrive and store article info for class attributes
        for article in self.newspaper.articles[:max]:
            article_url = article.url
            self.article_urls.append(article_url)
            article = Article(article_url)
            try:
                article.download()
                article.parse()
                self.article_titles_urls.append((article.title, article_url))
            except:
                continue

    def get_random_article_title_url(self):
        if self.article_titles_urls:
            return random.choice(self.article_titles_urls)

    def show_articles(self):
        for article in self.article_titles_urls:
            print(article)
