import requests
import json
import init_stuff
import time
DEBUG = False
# DEBUG = True


def getDivPrice():
    return 141

# gets item hashes from poe api (corrupted items not yet suported)


def getItemHashes(search_name=None, search_basetype=None, implicits=None, itemlvl=None, quality=None, corrupted=False):
    url = "https://www.pathofexile.com/api/trade/search/Necropolis"

    payload = {
        "query":
        # {"status": {"option": "online"},
        {"status": {"option": "any"},
         # "name":search_name,
         # "type":search_basetype,
         "stats": [],
         "filters":
         {
            "misc_filters":
            {
                "disabled": False,
                "filters":
                {
                    # "quality": {"min": quality},
                    # "corrupted": {},
                    # "ilvl": {"min": itemlvl}
                }
            },
            "trade_filters":
            {
                "disabled": False,
                    "filters":
                        {
                            # "price":
                            #     {
                            #         # "option":"chaos_divine"
                            #         "option":"any"
                            #     },
                            "sale_type":
                                {
                                    # "option":"chaos_divine"
                                    "option":"any"
                                }
                        }
            }
        }
        },
        # "sort": {"price": "asc"}
        "sort": {"stack_size": "desc"}
    }

    # payload = json.dumps({"query": {"status": {"option": "online"}, "name": "Mageblood","type": "Heavy Belt", "stats": [{"type": "and", "filters": []}]}, "sort": {"price": "asc"}})

    if search_name is not None:
        payload["query"]["name"] = search_name
    else:
        corrupted = None
        
    if search_basetype is not None:
        payload["query"]["type"] = search_basetype
    if implicits is not None:
        payload["query"]["stats"] = [{"type":"and","filters":[{"id":"pseudo.pseudo_number_of_implicit_mods","value":{"min":implicits},"disabled":False}]}]
    if corrupted is not None:
        payload["query"]["filters"]["misc_filters"]["filters"] = {"corrupted": {"option": corrupted},}
        # payload["query"]["filters"]["misc_filters"]["filters"]["corrupted"]["option"] = corrupted
        
    # set corrupted or not
    payload = json.dumps(payload)
    # print(payload)
    response = requests.request("POST", url, headers=init_stuff.getHeaders(), data=payload)
    resp_obj = response.json()
    if 'error' in response.text:
        print(resp_obj)
        return None
    if resp_obj['result']:
        result_strings = resp_obj['result']
    else:
        print("error: no items found")
        return False

    if DEBUG:
        print("Searching for...[", search_name + " " + search_basetype, "]")
        print(response)
        print("Query ID:", resp_obj['id'])
        print("Complexity:", resp_obj['complexity'])
        print("Results:", resp_obj['total'])
        print(result_strings)

    return result_strings

# getting results from result hashes


def getItemResults(hashes):
    url = "https://www.pathofexile.com/api/trade/fetch/"
    if hashes is None:
        print("Error: got no hashes")
        return False
    for i in range(10 if (len(hashes) > 10) else len(hashes)):
        url += hashes[i] + ','
    url = url[:-1]  # remove trailing comma
    payload = {}
    response = requests.request(
        "GET", url, headers=init_stuff.getHeaders(), data=payload)
    resp_obj = response.json()
    item_results = resp_obj['result']

    if DEBUG:
        print(response)
        print(response.text)
    return item_results


def returnPriceAvg(results):
    max_count = 4
    count = 0
    sum = 0
    sum_divisor = 0
    for result in results:
        if count > max_count:
            break
        curr_string = result['listing']['price']['currency']
        amount = result['listing']['price']['amount']
        # print("price:", amount, curr_string, sep='\t')
        if curr_string == "divine":
            sum += amount*getDivPrice()
            sum_divisor += 1
        elif curr_string == "chaos":
            sum += amount
            sum_divisor += 1
        # else:
            # print("error got bad currency type")
        if DEBUG:
            print("price:", amount, curr_string, sep='\t')
        count += 1

    return "%0.1f" % ((sum*1.0)/sum_divisor)


#returns lowest x prices of all items
def PriceItem(search_name = None, search_basetype = None, implicits = None, itemlvl = None, quality = None, corrupted = None):
    # name is for unique names ex: search_name = "Mageblood", search_basetype = "Heavy Belt"
    # currency is a base type
    if search_name == None and search_basetype == None:
        print("ERROR: name and base can't be None")
        return None

    hashes = getItemHashes(search_name, search_basetype, implicits, itemlvl, quality, corrupted)
    if not hashes:
        print("hash FAIL")
        return
    results = getItemResults(hashes)
    if not results:
        print("result FAIL")
        return
    # return returnPriceAvg(results)
    return results
    # printResults(results)
    
def priceAndNameFromResults(results):
    if results == None:
        print("error: got no results")
        return
    priceAmount = []
    currencyName = []
    name = []
    baseType = []
    rowList = []
    for result in results:
        try:
            currencyName.append(result['listing']['price']['currency'])
        except:
            currencyName.append("null")
            # print("price error")
        try:
            priceAmount.append(result['listing']['price']['amount'])
        except:
            priceAmount.append(-1)
            # print("price error")
        
        name.append(result['item']['name'])
        baseType.append(result['item']['baseType'])
        try:
            lastCharName = result['listing']['account']['lastCharacterName']
        except:
            lastCharName = "null"
        try:
            print("got stack size:", result['item']['stackSize'], "Acc name:", result['listing']['account']['name'], '//', lastCharName)
        except:
            print("no stack size")
    for x in range(len(results)):
        rowList.append([name[x], baseType[x], priceAmount[x], currencyName[x]])
        
    # print/(rowList)
    return rowList


if __name__ == "__main__":
    # print(priceAndNameFromResults(PriceItem(search_name="Starforge", corrupted=False)))
    print(priceAndNameFromResults(PriceItem(search_basetype="The Patient")))
