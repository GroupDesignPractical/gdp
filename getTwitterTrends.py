#!/usr/bin/env python3
import tweepy
import json
import string
import sys
import indicoio


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
  sortedTrends = sorted(trends,
                        key=lambda x: x['tweet_volume'],
                        reverse=True)
  return json.dumps(sortedTrends)


def getTweetsAbout(trendQuery, lang, api, maxCount):
  tweets = api.search(trendQuery, lang, count=maxCount)
  return tweets


def interpretSentimentAnalysis(value):
  if value < 0.40:
    return "Negative"
  if value > 0.60:
    return "Positive"
  return "Neutral"


def getSentimentAnalysis(tweetTextList):
  coeffs = indicoio.sentiment(tweetTextList, language='detect')
  interpretations = [interpretSentimentAnalysis(coeff) for coeff in coeffs]
  return (coeffs, interpretations)


def analyseTrend(trend, api):
  tweets = getTweetsAbout(trend['query'], "en", api, 5)
  tweetTexts = [tweet._json['text'] for tweet in tweets]
  (coeffs, interpretations) = getSentimentAnalysis(tweetTexts)

  # debugging
  # deal with non-bmp characters (e.g emojis) when printing for test
  non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
  print("\n    " + trend["name"] + "  -  " + str(trend["tweet_volume"]))
  for i in range(0, len(tweets)):
    print("Tweet text #" + str(i + 1) + ":   -- Sentiment Analysis: " +
          str(coeffs[i]) + "  - " + interpretations[i])
    print(tweetTexts[i].translate(non_bmp_map))

  mean = sum(coeffs) / len(coeffs)
  trend['sentiment_result'] = mean
  trend['sentiment_interpretation'] = interpretSentimentAnalysis(mean)
  return trend


def analyseTopTrends(trends, count, api):
  # add sentiment_result and sentiment_interpretation fields for
  # less popular trends too
  for trend in trends[count:]:
    trend['sentiment_result'] = None
    trend['sentiment_interpretation'] = None
  return [analyseTrend(trend, api)
          for trend in trends[:count]] + trends[count:]


def main():
  api = setOAuthConnection()
  trends = json.loads(getTrends(api))
  print(trends)
  trends = analyseTopTrends(trends, 5, api)
  print(trends)

if __name__ == '__main__':
  main()
