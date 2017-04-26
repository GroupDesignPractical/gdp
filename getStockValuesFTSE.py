#!/usr/bin/env python3
import urllib3
import certifi
import json
import sys

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
outputResponse = None

# All arguments but valCode are strings.
# Input_str is the stock symbol, dates are in the format 'yyyy-mm-dd'
# Possible valCodes: -1 - entire table, 0 - Date,           1 - Price,
#                     2 - High,         3 - Low,            4 - Volume,
#                     5 - Last Close,   6 - Change,         7 - Var%


def getStockValuesFTSE(input_str, strt_date, end_date, valCode):
    outputResponse = None
    response = http.request('GET',
                            'https://www.quandl.com/api/v3/datasets/LSE/'
                            + input_str + '.json')
    if (response.status != 200):
        outputResponse = json.dumps('Error')
    else:
        strResponse = response.data.decode('utf-8')
        listResponse = json.loads(strResponse)['dataset']['data']
        if (valCode == -1):
            fltrlistResponse = [elem for elem in listResponse
                                if (strt_date <= elem[0] <= end_date)]
        else:
            fltrlistResponse = [(elem[0], elem[valCode])
                                for elem in listResponse
                                if (strt_date <= elem[0] <= end_date)]
        outputResponse = json.dumps(fltrlistResponse)
    return outputResponse


def main():
    print(getStockValuesFTSE(sys.argv[1], sys.argv[2], sys.argv[3],
          int(sys.argv[4])))

if __name__ == '__main__': main()
