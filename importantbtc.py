import bot
import schedule
import time
import json

news_sources = ['http://cnn.com',
                'https://jezebel.com',
                'https://mashable.com',
                'https://www.npr.org',
                'https://www.wired.com']

# Get api keys from file named api_keys.json in parent directory
with open('../api_keys.json') as keys:
    btc_keys = json.load(keys)
    important_btc_keys = btc_keys


bot = bot.TwitterBot(**important_btc_keys)
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
