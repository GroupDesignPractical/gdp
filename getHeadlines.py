#!/usr/bin/env python3

import urllib3
import sys
import json

http = urllib3.PoolManager()


def getHeadlines(source):
  response = http.request(
    'GET',
    'https://newsapi.org/v1/articles?' +
    'source=' + source +
	# API key not in public repo, put it here
    '&apiKey=' + ''
  )
  output = None
  if (response.status != 200):
    # request failed for some reason, shouldn't happen
    output = "Error"
  else:
    # trim response to one article
    stringData = response.data.decode("utf-8")
    jsonData = json.loads(stringData)
    output = {}
    output['news_source_name'] = jsonData['source']
    article = jsonData['articles'][0]
    output['date'] = article['publishedAt']
    output['headline'] = article['title']
    output['link'] = article['url']
  return output


def main():
  # source
  # bbc-news
  # business-insider
  # the-guardian
  # the-new-york-times
  # the-wall-street-journal
  print(getHeadlines(sys.argv[1]))


if __name__ == "__main__":
  main()
