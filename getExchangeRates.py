#!/usr/bin/env python3
import urllib3
import certifi
import json
import sys

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
outputResponse = None

# list containing country names, currency short hand, and API codes
country_conversion = [
                        ('Australia', 'AUD', 'XUDLADD', 'XUDLADS'),
                        ('Canada', 'CAD', 'XUDLCDD', 'XUDLCDS'),
                        ('China', 'CNY', 'XUDLBK73', 'XUDLBK89'),
                        ('CzechRepublic', 'CZK', 'XUDLBK27', 'XUDLBK25'),
                        ('England', 'GBP', 'XUDLGBD', ''),
                        ('EU', 'EUR', 'XUDLERD', 'XUDLERS'),
                        ('Denmark', 'DKK', 'XUDLDKD', 'XUDLDKS'),
                        ('Hong Kong', 'HKD', 'XUDLHDD', 'XUDLHDS'),
                        ('Hungary', 'HUF', 'XUDLBK35', 'XUDLBK33'),
                        ('India', 'INR', 'XUDLBK64', 'XUDLBK97'),
                        ('Japan', 'JPY', 'XUDLJYD', 'XUDLJYS'),
                        ('Malaysia', 'MYR', 'XUDLBK66', 'XUDLBK83'),
                        ('NewZealand', 'NZD', 'XUDLNDD', 'XUDLNDS'),
                        ('Norway', 'NOK', 'XUDLNKD', 'XUDLNKS'),
                        ('Poland', 'PLN', 'XUDLBK49', 'XUDLBK47'),
                        ('Russia', 'RUB', 'XUDLBK69', 'XUDLBK85'),
                        ('Singapore', 'SGD', 'XUDLSGD', 'XUDLSGS'),
                        ('SouthAfrica', 'ZAR', 'XUDLZRD', 'XUDLZRS'),
                        ('SouthKorea', 'KRW', 'XUDLBK74', 'XUDLBK93'),
                        ('Sweden', 'SEK', 'XUDLSKD', 'XUDLSKS'),
                        ('Switzerland', 'CHF', 'XUDLSFD', 'XUDLSFS'),
                        ('Thailand', 'THB', 'XUDLBK72', 'XUDLBK87'),
                        ('Turkey', 'TRY', 'XUDLBK75', 'XUDLBK95'),
                        ('USA', 'USD', '', 'XUDLUSS')
                     ]


# All arguments but val are strings.
# input_str is the name of country, dates are in the format 'yyyy-mm-dd'
# val encodes the currency you want to convert from
# Possible values for val: 0 : USD,    1 : GBP,    2 : EUR
def getExchangeRate(input_str, strt_date, end_date, val):
  if (val == 0):
    # finds the appropriate API code, and constructs the url
    curr_str = [i[2] for i in country_conversion if input_str == i[0]][0]
    api_url = 'https://www.quandl.com/api/v3/datasets/BOE/' + curr_str \
        + '.json'
  elif (val == 1):
    curr_str = [i[3] for i in country_conversion if input_str == i[0]][0]
    api_url = 'https://www.quandl.com/api/v3/datasets/BOE/' + curr_str \
      + '.json'
  else:
    curr_str = [i[1] for i in country_conversion if input_str == i[0]][0]
    api_url = 'https://www.quandl.com/api/v3/datasets/ECB/EUR' + curr_str \
      + '.json'

    response = http.request('GET', api_url)
    if (response.status != 200):
      outputResponse = json.dumps('Error')
    else:
      strResponse = response.data.decode('utf-8')
      listResponse = json.loads(strResponse)['dataset']['data']
      fltrlistResponse = [i for i in listResponse
        if (strt_date <= i[0] <= end_date)]
      outputResponse = json.dumps(fltrlistResponse)
    return outputResponse


def main():
  print(getExchangeRate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))

if __name__ == '__main__': main()
