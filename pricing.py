import requests
import json
import init_stuff
DEBUG = False

def getDivPrice():
    return 155.0

#gets item hashes from poe api
def getItemHashes(search_name, search_basetype):
    url = "https://www.pathofexile.com/api/trade/search/Affliction"

    if search_name == "":
        payload = json.dumps(
            {"query":{"status":{"option":"online"},"type":search_basetype,"stats":[{"type":"and","filters":[]}],"filters":{"trade_filters":{"disabled":False,"filters":{"price":{"option":"chaos_divine"}}},"misc_filters":{"disabled":False,"filters":{"corrupted":{"option":"false"}}}}},"sort":{"price":"asc"}}
            )
    else:
        payload = json.dumps(
            {"query":{"status":{"option":"online"},"name":search_name,"type":search_basetype,"stats":[{"type":"and","filters":[]}],"filters":{"trade_filters":{"disabled":False,"filters":{"price":{"option":"chaos_divine"}}},"misc_filters":{"disabled":False,"filters":{"corrupted":{"option":"false"}}}}},"sort":{"price":"asc"}}
            )
    
     


    response = requests.request("POST", url, headers=init_stuff.getHeaders(), data=payload)
    # if response != "<Response [200]>":
    #     print(response.text)
    #     return None
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
    for i in range(10 if (len(hashes)>10) else len(hashes)):
        url += hashes[i] + ','
    url = url[:-1] #remove trailing comma
    payload = {}
    response = requests.request("GET", url, headers=init_stuff.getHeaders(), data=payload)
    resp_obj = response.json()
    item_results = resp_obj['result']
    
    if DEBUG:
        print(response)
        print (response.text)
    return item_results

def returnPriceAvg(results):
    max_count = 2
    count = 0
    sum = 0
    sum_divisor = 0
    for result in results:
        if count > max_count:
            break
        curr_string = result['listing']['price']['currency']
        amount = result['listing']['price']['amount']
        if curr_string == "divine":
            sum += amount
            sum_divisor += 1
        elif curr_string == "chaos":
            sum += amount/getDivPrice()
            sum_divisor += 1
        if DEBUG:
            print("price:", amount, curr_string)
        count += 1
            
    return "%0.1f" % ((sum*1.0)/sum_divisor)

def PriceItem(search_name, search_basetype):
    #name is for unique names ex: search_name = "Mageblood", search_basetype = "Heavy Belt"
    #currency is a base type
    
    hashes = getItemHashes(search_name, search_basetype)
    if hashes == False:
        print("hash FAIL")
        return
    results = getItemResults(hashes)
    if len(results) < 1:
        print("result FAIL")
        return
    return returnPriceAvg(results)
    # printResults(results)
    
if __name__ == "__main__":
    print("Mirror =", PriceItem("","Mirror of Kalandra"))
    # print("Mirror house =", PriceItem("","House of Mirrors"))
    # print("Mageblood =", PriceItem("Mageblood","Heavy Belt"))
    # print("Headhunter =", PriceItem("Headhunter","Leather Belt"))
