import json

with open("NSEStocks.json") as json_file:
    listNSE = json.load(json_file)

listParameters = list(listNSE[0].keys())
weights = {"Mkt Cap Percentile": 0,             "Mkt Cap (Rs cr)": 0,
           "Name": 0,                           "Exchange": 0,
           "Super Sector": 3,                   "Symbol": 0,
           "Sector": 2}


def percent_diff(tranche1, tranche2):
    # Magic Number 30 as the 1532 stocks have been divided into 30 tranches.
    return (abs(int(tranche1) - int(tranche2))/30)


# Takes a list of company symbols as the argument
# and gives 5 similar recommendations based on various attributes
def getRecommendationsNSE(listCurrCompanies):
    listCurrCompaniesFull = [i for i in listNSE if (i["Symbol"] in listCurrCompanies)]
    fltrlistNSE = [i for i in listNSE if not (i["Symbol"] in listCurrCompanies)]

    # Calculate the likelihood score
    for i in fltrlistNSE:
        score = 0
        for j in listCurrCompaniesFull:
            curr_score = 0
            for k in listParameters:
                curr_score = curr_score + (weights[k]*int(j[k] == i[k]))
            score = score + (curr_score * (1 - percent_diff(
                                                i["Mkt Cap Percentile"],
                                                j["Mkt Cap Percentile"])
                                          )
                            )
        i["Score"] = score

    # Sort in descending order and output the top 5 recommendations
    listTopRes = sorted(fltrlistNSE, key=lambda i: i["Score"], reverse=True)
    listResponse = []
    for i in listTopRes[: 5]:
        dictRes = {k: v for (k, v) in i.items() if k in ["Name", "Symbol", "Exchange"]}
        listResponse.append(dictRes)
    return json.dumps(listResponse)
