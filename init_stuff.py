import requests
import my_secrets
import pricing
import time
import csv
import re

header_dict = {
  'Content-Type': 'application/json',
  'Cookie': ('POESESSID=%s') % (my_secrets.getSessID()),
  'Origin': 'https://www.pathofexile.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def getHeaders():
    return header_dict

def getLeagueName():
    url = "https://api.pathofexile.com/league"
    response = requests.get(url, headers=header_dict)
    if response == "<Response [401]>":
        return response.json()['leagues'][8]['id'] #8 is historically trade league
    else:
        # print("error:", response.text)
        return "Affliction"


#return list of div cards from poe.ninja
#6 new gem cards were added this patch
#2 scarab cards were removed
# plus 4 total
def ninjaDivObject():
    params = {
        'league': getLeagueName(),
        'type': 'DivinationCard'       
    }
    url = "https://poe.ninja/api/data/itemoverview"
    response = requests.get(url, headers=header_dict, params=params)
    response = response.json()
    cards = response['lines']
    # print(len(cards))
    return cards

def toCSV(cards):
    card_dict_array = []
    
    
    for card in cards:
        #inits
        implicits = 0
        corrupt_bool = False
        curr_count = 1
        quality = 0
        
        
        # print("writing", card['baseType'])
        if "stackSize" in card:
            stackSize = card['stackSize']
        else:
            stackSize = 1
            
        result_str = card['explicitModifiers'][0]['text']
        
        # clean up result string
        result_str = result_str.replace("\n", '')
        result_str = result_str.replace("<divination>", '')
        result_str = re.sub(r'\{Item Level:} <.+>{\d{1,}}', '', result_str)
        result_str = result_str.replace("<default>", '')
        result_str = result_str.replace("<enchanted>", '')
        result_str = result_str.replace("<augmented>", '')
        result_str = result_str.replace("<gemitem>", '')
        result_str = re.sub(r'\{Quality:\} \{\+\d{1,}%\}', '', result_str)
        result_str = re.sub(r'\{Area Level:} <normal>\{\d{1,}}', '', result_str)
        result_str = re.sub(r'\{Map Tier:} <normal>\{\d{1,}}', '', result_str)
        result_str = re.sub(r'<size:.+>', '', result_str)
        
        
        if "<uniqueitem>" in result_str:
            result_str = result_str.replace("<uniqueitem>", '')
            rarity = "unique"
        elif "<whiteitem>" in result_str:
            result_str = result_str.replace("<whiteitem>", '')
            rarity = "white"
        elif "<rareitem>" in result_str:
            result_str = result_str.replace("<rareitem>", '')
            rarity = "rare"
        elif "<magicitem>" in result_str:
            result_str = result_str.replace("<magicitem>", '')
            rarity = "magic"
        elif "<currencyitem>" in result_str:
            result_str = result_str.replace("<currencyitem>", '')
            if re.search(r'\d{1,}x', result_str):
                curr_count = re.search(r'\d{1,}x', result_str).group()[:-1]
                result_str = re.sub(r'\d{1,}x ', '', result_str)
            rarity = "currency"
            
            
        # add corrupted tag to card result
        if "<corrupted>" in result_str or "{corrupted}" in result_str or "{Corrupted}" in result_str:
            result_str = result_str.replace("<corrupted>", '')
            result_str = result_str.replace("{corrupted}", '')
            result_str = result_str.replace("{Corrupted}", '')
            corrupt_bool = True
            
        if "{Two-Implicit}" in result_str:
            implicits = 2
            result_str = result_str.replace("{Two-Implicit}", '')
            
        if "{Three-Implicit}" in result_str:
            implicits = 3
            result_str = result_str.replace("{Three-Implicit}", '')
            
        # TODO QUALITY

        card_dict = {
            'name': card['baseType'],
            'resultTag': result_str,
            'stackSize': stackSize,
            # 'otherTags': otherTags,
            'corrupted': corrupt_bool,
            'rarity': rarity,
            'quality': quality,
            'implicits': implicits,
            'count': curr_count
        }
        card_dict_array.append(card_dict)
        
    keys = card_dict_array[0].keys()
    with open('cards.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(card_dict_array)
    
def priceCards():
    with open('cards.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        for card in data:
            if card['rarity'] == "unique":
                card_price = pricing.PriceItem('', card['name'])
                result_price = pricing.PriceItem(card['resultTag'][1:-1])
            
                time.sleep(10)
if __name__ == "__main__":
    # print(getLeagueName())
#    toCSV(ninjaDivObject())
    priceCards()
    