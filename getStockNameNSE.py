from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import sys

with open('NSEStocks.json') as json_file:
    listNSE = json.load(json_file)

listCompanies = [i['Name'] for i in listNSE]


def getStockNameNSE(input_str):
    listApproxMatches = process.extract(input_str, listCompanies)
    listResponse = [{k: v for (k, v) in j.items()
                    if k in ["Name", "Symbol", "Exchange"]}
                    for i in listApproxMatches for j in listNSE
                    if j["Name"] == i[0]]
    outputResponse = json.dumps(listResponse)
    return outputResponse


def main():
    print(getStockNameNSE(sys.argv[1]))

if __name__ == '__main__': main()
