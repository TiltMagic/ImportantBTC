import bot
import schedule
import time

news_sources = ['http://cnn.com',
                'https://jezebel.com',
                'https://mashable.com',
                'https://www.npr.org']


# Account keys and tokens from twitter API
important_btc = {'consumer_key': None,
                 'consumer_secret': None',
                 'access_token': None,
                 'access_token_secret': None}

bot = bot.TwitterBot(**important_btc)
bot.post_news_from_sources(news_sources)


def tweet():
    # Refreshes Twitter API opject for bot class and posts final content
    bot.setup_and_refresh()
    try:
        bot.post_news_from_sources(news_sources)
    except:
        pass
        raise

    print("\nPosted to Twitter")


def main():
    # Runs program based on schedule
    schedule.every().hour.do(tweet)

    while True:
        schedule.run_pending()


main()
