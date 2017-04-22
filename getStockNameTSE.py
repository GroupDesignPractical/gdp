from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import sys

with open('TSEStocks.json') as json_file:
    listTSE = json.load(json_file)

listCompanies = [i['Name'] for i in listTSE]


def getStockNameTSE(input_str):
    listApproxMatches = process.extract(input_str, listCompanies)
    listResponse = [j for i in listApproxMatches for j in listTSE
                    if j['Name'] == i[0]]
    outputResponse = json.dumps(listResponse)
    return outputResponse


def main():
    print(getStockNameTSE(sys.argv[1]))

if __name__ == '__main__': main()
