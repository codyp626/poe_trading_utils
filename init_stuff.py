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
        implicits = None
        corrupt_bool = False
        curr_count = None
        quality = None
        influenced = None
        synth = None
        links = None
        itemLevel = None
        
        
        # print("writing", card['baseType'])
        if "stackSize" in card:
            stackSize = card['stackSize']
        else:
            stackSize = 1
            
        result_str = card['explicitModifiers'][0]['text']
        
        # clean up result string
        result_str = result_str.replace("\n", '')
        result_str = result_str.replace("<divination>", '')
        # result_str = re.sub(r'\{Item Level:} <.+>{\d{1,}}', '', result_str)
        result_str = result_str.replace("<default>", '')
        result_str = result_str.replace("<enchanted>", '')
        result_str = result_str.replace("<augmented>", '')
        result_str = re.sub(r'\{Quality:\} \{\+\d{1,}%\}', '', result_str)
        result_str = re.sub(r'\{Area Level:} <normal>\{\d{1,}}', '', result_str)
        result_str = re.sub(r'\{Map Tier:} <normal>\{\d{1,}}', '', result_str)
        # result_str = re.sub(r'<size:.+>', '', result_str)
        
        
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
            
        if "<gemitem>" in result_str:
                rarity = "gem"
                result_str = result_str.replace("<gemitem>", '')
            
        if "{Item Level:}" in result_str:
            match = re.search(r'\{Item Level:} <normal>{\d{1,}\}', result_str)
            itemLevel = int(match.group()[23:-1])
            result_str = re.sub(r'\{Item Level:} <normal>{\d{1,}}', '', result_str) # clean up item level
            
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
            
        if "{Influenced Item}" in result_str:
            result_str = result_str.replace("{Influenced Item}", '')
            influenced = 1
        
        if "{Double-Influenced Item}" in result_str:
            result_str = result_str.replace("{Double-Influenced Item}", '')
            influenced = 2
            
        if "{Synthesised}" in result_str:
            result_str = result_str.replace("{Synthesised}", '')
            synth = True
        # TODO QUALITY
        
        if "{Item}" in result_str:
            continue

        result_str = re.sub(r'<size:.+>', '', result_str)
        result_str = result_str.replace("{", '')
        result_str = result_str.replace("}", '')
        card_dict = {
            'name': card['baseType'],
            'stackSize': stackSize,
            'resultTag': result_str,
            'resultBaseType': None,
            'corrupted': corrupt_bool,
            'rarity': rarity,
            'quality': quality,
            'implicits': implicits,
            'resultCurrencyCount': curr_count,
            'influenced': influenced,
            'synthesised': synth,
            'links': links,
            'itemLevel': itemLevel
        }
        if rarity == "unique":
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
                # card_price = pricing.PriceItem('', card['name'])
                print("pricing:", card['resultTag'][1:-1], card['resultBaseType'])
                # result_price = pricing.PriceItem(card['resultTag'][1:-1], '')
                # print(result_price)
                # time.sleep(5)
if __name__ == "__main__":
    # print(getLeagueName())
   toCSV(ninjaDivObject())
    # priceCards()
    