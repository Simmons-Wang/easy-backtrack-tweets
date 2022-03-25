import datetime
import pickle
import tweepy as tp
import pandas as pd
import time


def lookUpDetail(ids):
    """
    :param ids: the list of tweets ids, the maximum length is 100 at a time.
    :return: dataframe which include 'tweet_id', 'favorite_count', 'retweet_count', 'lang',
    'hashtags', 'url', 'user_id'
    """
    statuses = api.lookup_statuses(ids)
    details = [[i.id, i.favorite_count, i.retweet_count, i.lang,
                i.entities['hashtags'], i.entities['urls'],
                i.author.id] for i in statuses]
    df = pd.DataFrame(details, columns=['tweet_id', 'favorite_count', 'retweet_count', 'lang',
                                        'hashtags', 'urls', 'user_id'])

    df.hashtags = df.hashtags.apply(lambda x: [i['text'] for i in x] if x else [])
    df.urls = df.urls.apply(lambda x: x[0]['url'] if x else None)
    return df


def get_following(my_name):
    user1 = api.get_friends(screen_name=my_name, cursor=-1, count=200)  # 200 is the limit
    user = user1[0]
    while user1[0]:
        user1 = api.get_friends(screen_name=my_name, cursor=user1[1][1], count=200)
        user = user + user1[0]
        time.sleep(2)
    friendsScreenName = [i.screen_name for i in user]  # change this line to collect other attribute of friends
    return friendsScreenName


def get_history(f, start_time):
    tws = api.user_timeline(screen_name=f, count=200)  # one crawl limit is 200
    userTws = tws.copy()
    while tws and (tws[-1].created_at > start_time):
        tws = api.user_timeline(screen_name=f, count=200, max_id=tws.max_id)
        userTws = userTws + tws
    details = [[i.created_at, i.id, i.text, i.favorite_count, i.retweet_count, i.lang,
                i.entities['hashtags'], i.entities['urls'],
                i.author.id, f] for i in userTws]
    return details


if __name__ == '__main__':
    # replace the following attributions with yours
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    auth = tp.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tp.API(auth)

    test_ids = [
        1481194503650549761,
        1481194425170956292,
        1480951940389371914,
        1480942056365252610,
        1480888363011903491,
        1480886828072718337,
        1480848873627086849,
        1480844751880351745,
        1480823233267920897]

    test_result1 = lookUpDetail(test_ids)
    test_result2 = get_following('')  # replace it with your name
    test_result3 = get_history('')  # replace it with your name
