<<<<<<< HEAD
import tweepy
import json
import string
import time
import sys


def setOAuthConnection():
    # credentials are confidential and should not be shared in the
    # public repository
    f = open('credentials.txt', 'r')
    content = f.readlines()
    consumer_token = content[0].strip()
    consumer_secret = content[1].strip()
    access_token = content[2].strip()
    access_secret = content[3].strip()

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    # if authentication was successful, account name will be printed
    print(api.me().name)

    return api


def containsLatinLetter(str):
    for l in str:
        if l in string.ascii_letters:
            return True
    return False


def getTrends(api):  # consider adding location as parameter
    trends = (api.trends_place(1))  # 1 for worldwide;
    trends = [trend for trend in trends[0]['trends'] if
              trend['tweet_volume'] is not None and
              containsLatinLetter(trend['name'])]
    return json.dumps(trends)


def getTweetsAbout(trendQuery, lang, api):
    tweets = api.search(trendQuery, lang) # [ SearchResults object ]
    return tweets;


def main():
    api = setOAuthConnection()
    trends = json.loads(getTrends(api))
    print(trends)
    tweets = [getTweetsAbout(trend['query'], "en", api) for trend in trends

    # deal with non_bmp characters (e.g emojis) when printing for test
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    
    for tweet in tweets[0][:5]:
        print(str(tweet._json['text']).translate(non_bmp_map))
    print("\n");

    # print(tweets[0][0])

if __name__ == "__main__":
    main()
=======
#!/usr/bin/env python3
import tweepy
import json
import string

def setOAuthConnection():
  # credentials are confidential and should not be shared in the
  # public repository
  f = open('credentials.txt', 'r')
  content = f.readlines()
  consumer_token = content[0].strip()
  consumer_secret = content[1].strip()
  access_token = content[2].strip()
  access_secret = content[3].strip()

  auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  api = tweepy.API(auth)

  # if authentication was successful, account name will be printed
  print(api.me().name)

  return api

def containsLatinLetter(str):
  for l in str:
    if l in string.ascii_letters:
      return True
  return False

def getTrends(api):  # consider adding location as parameter
  trends = (api.trends_place(1))  # 1 for worldwide;
  trends = [trend for trend in trends[0]['trends'] if
            trend['tweet_volume'] is not None and
            containsLatinLetter(trend['name'])]
  return json.dumps(trends)

def main():
  api = setOAuthConnection()
  print(getTrends(api))

if __name__ == '__main__':
  main()
>>>>>>> refs/remotes/origin/master
