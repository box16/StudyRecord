import tweepy
from os import environ as env
from pixela import Pixela
from datetime import datetime


def get_twitter_api(
        api_key,
        api_secret_key,
        access_token,
        access_secret_token):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_secret_token)
    return tweepy.API(auth)


def get_target_str_num(twitter_api, user_id, date, target_str):
    user_tweets = twitter_api.user_timeline(user_id)
    date_str = date.strftime("%Y%m%d")

    target_str_num = 0
    for tweet in user_tweets:
        tweet_date = tweet.created_at.strftime("%Y%m%d")
        if ((date_str == tweet_date) and (target_str in tweet.text)):
            target_str_num += 1

    return target_str_num


def create_pixel(user_name, token, graph_id, quantity, date):
    pixela = Pixela(username=user_name, token=token)

    pixela.create_pixel(
        graph_id=graph_id,
        quantity=quantity,
        date=date)


if __name__ == "__main__":
    pixela_user_name = "box16"
    pixela_graph_id = "study-record"
    graph_url = "https://pixe.la/v1/users/box16/graphs/study-record.html"
    target_str = "勉強記録"
    today = datetime.today()

    twitter_api = get_twitter_api(env.get("TWITTER_API_KEY"),
                                  env.get("TWITTER_API_SECRET_KEY"),
                                  env.get("TWITTER_ACCESS_TOKEN"),
                                  env.get("TWITTER_ACCESS_SECRET_KEY"))

    target_str_num = get_target_str_num(twitter_api,
                                        env.get("TWITTER_MY_ID"),
                                        today,
                                        target_str)

    create_pixel(pixela_user_name,
                 env.get('PIXELA_TOKEN'),
                 pixela_graph_id,
                 target_str_num,
                 today)

    twitter_api.update_status(
        f"本日の記録数 : {target_str_num} \n {graph_url}")
