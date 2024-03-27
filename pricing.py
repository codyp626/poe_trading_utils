import requests
import json
import init_stuff
DEBUG = False


def getDivPrice():
    return 290

# gets item hashes from poe api (corrupted items not yet suported)


def getItemHashes(search_name=None, search_basetype=None, implicits=None, itemlvl=None, quality=None, corrupted=None):
    url = "https://www.pathofexile.com/api/trade/search/Standard"

    payload = {
        "query":
        {"status": {"option": "online"},
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
                    # "corrupted": {"option": None},
                    # "ilvl": {"min": itemlvl}
                }
            },
            "trade_filters":
            {
                "disabled": False,
                    "filters":
                        {
                            "price":
                                {
                                    "option":"chaos_divine"
                                }
                        }
            }
        }
        },
        "sort": {"price": "asc"}
    }

    # payload = json.dumps({"query": {"status": {"option": "online"}, "name": "Mageblood","type": "Heavy Belt", "stats": [{"type": "and", "filters": []}]}, "sort": {"price": "asc"}})

    if search_name is not None:
        payload["query"]["name"] = search_name
    if search_basetype is not None:
        payload["query"]["type"] = search_basetype
    if implicits is not None:
        payload["query"]["stats"] = [{"type":"and","filters":[{"id":"pseudo.pseudo_number_of_implicit_mods","value":{"min":implicits},"disabled":False}]}]
    if corrupted is not None:
        payload["query"]["filters"]["misc_filters"]["filters"]["corrupted"]["option"] = corrupted
        
    # set corrupted or not
    payload = json.dumps(payload)
    print(payload)
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


def PriceItem(search_name = None, search_basetype = None, implicits = None, itemlvl = None, quality = None, corrupted = None):
    # name is for unique names ex: search_name = "Mageblood", search_basetype = "Heavy Belt"
    # currency is a base type

    hashes = getItemHashes(search_name, search_basetype, implicits, itemlvl, quality, corrupted)
    if not hashes:
        print("hash FAIL")
        return
    results = getItemResults(hashes)
    if not results:
        print("result FAIL")
        return
    return returnPriceAvg(results)
    # printResults(results)


if __name__ == "__main__":
    print("Mirror =", PriceItem(search_basetype="Mirror of Kalandra"))
    # print("Mirror house =", PriceItem("","House of Mirrors"))
    # print("AVG PRICE =", PriceItem(search_basetype="The Apothecary"))
    # print("Headhunter =", PriceItem("Headhunter","Leather Belt"))
    # print(PriceItem(search_name="Voices", corrupted=True))
    # print(PriceItem(search_name="Mageblood", corrupted=True, implicits=2))
