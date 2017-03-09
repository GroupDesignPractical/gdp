#!/usr/bin/env python3
import urllib3
import json
import sys

http = urllib3.PoolManager()

def getStockNames(input_str):
  search_str = input_str.replace(' ', '%20')
  response = http.request('GET',
    'http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search_str)
  if (response.status != 200):
    # unlikely to go into this branch (only if API changes)
    outputResponse = json.dumps("Error")
  else:
    # convert the response from bytes to text		
    strResponse = response.data.decode("utf-8")
    listResponse = json.loads(strResponse)
    # filter the list based on the exchanges, and sort the output using the
    # exchange as key
    fltrlistResponse = sorted(
      [elem
        for elem in listResponse if elem['Exchange']
        in ['NYSE', 'NASDAQ']],
      key = lambda f : f['Exchange'])
    outputResponse = json.dumps(fltrlistResponse)
    return outputResponse

def main() :
  print(getStockNames(sys.argv[1]))

if __name__ == "__main__" : main()
