#!/usr/bin/env python3

import urllib3
import certifi
import json
import datetime
import sys

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# All arguments but valCode are strings
# strtDate and endDate have the format "yyyy-mm-dd"
# Possible timeSplits: "daily", "weekly", "monthly", "quarterly", "yearly"
# Possible valCodes: -1 - entire table, 0 - Date,           1 - Open,
#                     2 - High,         3 - Low,            4 - Close,
#                     5 - Volume,       6 - Ex-Dividend,    7 - Split Ratio,
#                     8 - Adj. Open,    9 - Adj. High,     10 - Adj. Low,
#                    11 - Adj. Close,  12 -'Adj. Volume'

def getStockValues(ticker, strtDate, endDate, timeSplit, valCode):
  response = http.request('GET','https://www.quandl.com/api/v3/datasets/WIKI/'
    + ticker + '.json?start_date=' + strtDate + '&end_date=' + endDate
    + '&collapse=' + timeSplit)
  outputResponse = None
  if (response.status != 200):
    outputResponse = json.dumps('Error')
  else:
    listResponse = json.loads(response.data.decode('utf-8'))
    fltrlistResponse = None
    if (valCode == -1):
      fltrlistResponse = listResponse['dataset']['data']
    else:
      fltrlistResponse = [(elem[0], elem[valCode]) 
        for elem in listResponse['dataset']['data']]
    outputResponse = json.dumps(fltrlistResponse)
  return outputResponse

def main():
  print(getStockValues(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
    int(sys.argv[5])))

  if __name__ == '__main__' : main()

