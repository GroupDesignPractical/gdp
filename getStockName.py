import urllib3
import json
import sys


http = urllib3.PoolManager()

def getStockNames(input_str):
	search_str = input_str.replace(' ','%20')
	response = http.request('GET','http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search_str)
	if (response.status == 400) :
		outputResponse = json.dumps("Error")
	else:
		strResponse = response.data.decode("utf-8")
		listResponse = json.loads(strResponse)
		fltrlistResponse = sorted([elem for elem in listResponse if elem['Exchange'] in ['NYSE', 'NASDAQ']],key = lambda f : f['Exchange'])
		outputResponse = json.dumps(fltrlistResponse)
	return outputResponse

def main() :
	print(getStockNames(sys.argv[1]))

if __name__ == "__main__" : main()
