import json

with open("FTSE350.json") as json_file:
    listFTSE = json.load(json_file)

listParameters = list(listFTSE[0].keys())
weights = {"Company Market Cap Percentile": 0,      "Market": 1,
           "International Issuer": 1,               "Name": 0,
           "World Region": 1,                       "Exchange": 0,
           "ICB Super-Sector": 3,                   "Country of Incorporation": 1,
           "ICB Industry": 2,                       "Company Market Cap": 0,
           "Symbol": 0}


def percent_diff(tranche1, tranche2):
    # Magic Number 35 as the 350 stocks have been divided into 35 tranches of 10
    # each.
    return (abs(tranche1 - tranche2)/35)


# Takes a list of company symbols as the argument
# and gives 5 similar recommendations based on various attributes
# For eg: ["BARC", "HSBA"] should be passed if the graph currently shows the
# stocks for Barclays and HSBC.
def getRecommendationsFTSE(listCurrCompanies):
    listCurrCompaniesFull = [i for i in listFTSE if (i["Symbol"] in listCurrCompanies)]
    fltrlistFTSE = [i for i in listFTSE if not (i["Symbol"] in listCurrCompanies)]

    # Calculate the likelihood score
    for i in fltrlistFTSE:
        score = 0
        for j in listCurrCompaniesFull:
            curr_score = 0
            for k in listParameters:
                curr_score = curr_score + (weights[k]*int(j[k] == i[k]))
            score = score + (curr_score * (1 - percent_diff(
                                                i["Company Market Cap Percentile"],
                                                j["Company Market Cap Percentile"])
                                          )
                            )
        i["Score"] = score

    # Sort in descending order and output the top 5 recommendations
    listTopRes = sorted(fltrlistFTSE, key=lambda i: i["Score"], reverse=True)
    listResponse = []
    for i in listTopRes[: 5]:
        dictRes = {k: v for (k, v) in i.items() if k in ["Name", "Symbol", "Exchange"]}
        listResponse.append(dictRes)
    return json.dumps(listResponse)
