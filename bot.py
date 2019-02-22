import tweepy
import headline
import marketcap
import math
import random
import json


verbs = {1: 'up', 2: 'rises', 3: 'jumps', 4: 'hikes', 5: 'climbs', 6: 'spikes', 7: 'surges',
         8: 'leaps', 9: 'booms', 10: 'charges', 11: 'moons', -1: 'down', -2: 'falls', -3: 'sags',
         -4: 'sinks', -5: 'slumps', -6: 'drops', -7: 'dives', -8: 'tumbles', -9: 'crashes',
         -10: 'plummets', -11: 'is dead af', 0: 'just chills'}

fillers = ['as', 'due to', 'cuz', '-', 'as a consequence of', 'as a result of']


class TwitterBot:
    def __init__(self, **account_info):
        self.consumer_key = account_info['consumer_key']
        self.consumer_secret = account_info['consumer_secret']
        self.access_token = account_info['access_token']
        self.access_token_secret = account_info['access_token_secret']

        self.setup_and_refresh()

    def setup_and_refresh(self):
        # Builds twitter api object using user keys and tokens
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def save_used_article(self, article_info):
        # Saves used articles to database.json to avoid posting duplicate articles
        # article_info = (title, url) tuple
        with open('database.json', 'r') as database:
            data = json.load(database)
            data['posted'].append(article_info)
            final_data = json.dumps(data, sort_keys=True, indent=4)

        with open('database.json', 'w') as database:
            database.write(final_data)

    def read_saved_from_database(self):
        # Remeber that json list data needs to be type casted to tuple
        with open('database.json', 'r') as database:
            data = json.load(database)['posted']
            tupled_list = [tuple(value) for value in data]
            return tupled_list

    def update_status(self, status):
        # Updates the status of the Twitter account
        try:
            self.api.update_status(status)
            return True
        except:
            print('Problem with func update_status. Twitter Status prob wasnt updated')
            raise

    def get_verb(self, btc_change):
        # Gets verb from verb dict based on btc_change value
        btc_change = marketcap.get_btc_change()

        if btc_change < 0:
            change = math.floor(btc_change)
        else:
            change = math.ceil(btc_change)

        if change > 11:
            verb = 'moons'
        elif change < -11:
            verb = 'is dead af'
        else:
            verb = verbs[change]

        return verb

    def post_news_from_sources(self, source_urls):
        # Posts final formatted product to Twitter using given source_url
        filtered_articles = []
        used_articles = self.read_saved_from_database()
        """Test_new_articles list below is for testing"""
        # test_new_articles = []

        for url in source_urls:
            article = headline.Newspaper(url)
            article.build_article_titles_urls()
            new_articles = article.article_titles_urls
            """Uncomment line below for testing"""
            # test_new_articles += new_articles
            filtered_articles += list(set(new_articles).difference(set(used_articles)))

        """Unccoment below for testing"""
        # for value in filtered_articles:
        #     print(value)

        # for value in filtered_articles:
        #     if value in used_articles:
        #         print('True***********')
        #     else:
        #         print('False')
        #
        # print("Filtered articles: {}".format(len(filtered_articles)))
        # print("New articles: {}".format(len(test_new_articles)))

        the_headline, url = random.choice(filtered_articles)

        btc_change = marketcap.get_btc_change()

        verb = self.get_verb(btc_change)

        filler = random.choice(fillers)

        content = "Bitcoin {} {}% {} {}\n{}".format(verb, btc_change, filler, the_headline, url)

        if self.update_status(content):
            self.save_used_article([the_headline, url])
