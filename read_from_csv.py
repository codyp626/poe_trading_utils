import csv
import pricing
import time

NAME = 0
STACK_SIZE = 1
RESULT = 2
CORRUPTED = 3
RARITY = 4
QUALITY = 5
IMPLICITS = 6
IINFLUENCED = 8
SYNTH	= 9
LINKS = 10
ILVL = 11
PRIMORDIAL = 12


with open('cards_unique.csv', 'r') as file:
    reader = csv.reader(file)
    with open('card_price.csv', mode='w') as outfile:
        for card in reader:
            result_price = pricing.PriceItem(search_name=card[RESULT], corrupted=CORRUPTED, itemlvl=ILVL)
            print(card[RESULT], "\t\t=\t\t", result_price)
            time.sleep(10)
            card_price = pricing.PriceItem(search_basetype=card[NAME])
            print(card[NAME], "\t\t=\t\t", card_price)
            time.sleep(10)
            writer = csv.writer(outfile)
            row = [card[NAME], card[STACK_SIZE], card_price, card[RESULT], result_price]
            writer.writerow(row)
            
        