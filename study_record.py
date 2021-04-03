import tweepy
from os import environ as env
from pixela import Pixela
from datetime import datetime


def get_twitter_api():
    api_key = env.get("TWITTER_API_KEY")
    api_secret_key = env.get("TWITTER_API_SECRET_KEY")
    access_token = env.get("TWITTER_ACCESS_TOKEN")
    access_secret_token = env.get("TWITTER_ACCESS_SECRET_KEY")

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret_token)
    return tweepy.API(auth)


def get_studyrecord_num(twitter, date):
    my_id = env.get("TWITTER_MY_ID")
    my_tweets = twitter.user_timeline(my_id)
    date_str = date.strftime("%Y%m%d")

    study_record_num = 0
    for tweet in my_tweets:
        tweet_date = tweet.created_at.strftime("%Y%m%d")
        if ((date_str == tweet_date) and ("勉強記録" in tweet.text)):
            study_record_num += 1

    return study_record_num


def creat_pixel(quantity, date):
    pixela = Pixela(username='box16', token=env.get('PIXELA_TOKEN'))

    pixela.create_pixel(
        graph_id="study-record",
        quantity=quantity,
        date=date)

    return pixela.graph_url("study-record")


def tweet_study_record_result(twitter, study_record_num, graph_url):
    twitter.update_status(f"本日の記録数 : {study_record_num} \n {graph_url}.html")


if __name__ == "__main__":
    today = datetime.today()

    twitter_api = get_twitter_api()
    study_record_num = get_studyrecord_num(twitter_api, today)
    graph_url = creat_pixel(study_record_num, today)
    tweet_study_record_result(twitter_api, study_record_num, graph_url)
