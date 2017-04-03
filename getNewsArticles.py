#!/usr/bin/env python3

import urllib3
import sys

http = urllib3.PoolManager()


def getNewsArticles(query, startDate, endDate):
  query = query.replace(' ', '%20')
  response = http.request(
    'GET',
    'https://api.nytimes.com/svc/search/v2/articlesearch.json?' +
	# API key not in public repo, put it here
    'api-key=' + '' +
    '&q=' + query +
    '&begin_date=' + startDate +
    '&end_date=' + endDate
  )
  outputResponse = None
  if (response.status != 200):
    # request failed for some reason, shouldn't happen
    outputResponse = "Error"
  else:
    # convert the response from bytes to text
    outputResponse = response.data.decode("utf-8")
  return outputResponse


def main():
  # search query, start date, end date (dates- YYYYMMDD)
  print(getNewsArticles(sys.argv[1], sys.argv[2], sys.argv[3]))


if __name__ == "__main__":
  main()
