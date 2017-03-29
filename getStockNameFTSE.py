#!/usr/bin/env python3
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import sys

with open('FTSE350.json') as json_file:
    listFTSE350 = json.load(json_file)

listCompanies = [i['Name'] for i in listFTSE350]


def getStockNameFTSE(input_str):
    listApproxMatches = process.extract(input_str, listCompanies)
    listResponse = [j for i in listApproxMatches for j in listFTSE350
                    if j['Name'] == i[0]]
    outputResponse = json.dumps(listResponse)
    return outputResponse


def main():
    print(getStockNameFTSE(sys.argv[1]))

if __name__ == '__main__': main()
