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


def getAvgPrice(results, sum):
    price = 0
    count = 0
    if results == None:
        return -1
    for result in results:
        if count < sum:
            if result[3] == "divine":
                price += result[2] * pricing.getDivPrice()
            elif result[3] == "chaos":
                price += result[2]
            else:
                print("error: got bad currency type", result[3])
                return -1
        count += 1
            
    return price / (sum*1.0)


def writeToDatabase():
    with open('cards_unique.csv', 'r') as file:
        reader = csv.reader(file)
        with open('card_price.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["name", "stackSize", "cardPrice", "result", "resultPrice", "profit"])
            for card in reader:
                if card[NAME] == "name":
                    continue
                
                stackSize = int(card[STACK_SIZE])
                print("Trying to find:", card[RESULT])
                results = pricing.priceAndNameFromResults(pricing.PriceItem(search_name=card[RESULT], corrupted=card[CORRUPTED]))
                result_price = getAvgPrice(results, 2)
                time.sleep(20)
                
                print("Trying to find:", card[NAME])
                cards = pricing.priceAndNameFromResults(pricing.PriceItem(search_basetype=card[NAME]))
                card_price = getAvgPrice(cards, stackSize/2)
                time.sleep(20)
                
                print(card[NAME], "=", card_price, '\t', card[RESULT], "=", result_price)
                profit = result_price-(card_price*stackSize)
                print("profit:", profit)
                
                row = [card[NAME], stackSize, card_price, card[RESULT], result_price, profit]
                writer.writerow(row)
                
if __name__ == "__main__":
    # pretty_results = pricing.priceAndNameFromResults(pricing.PriceItem(search_basetype="Divine Orb"))
    # pretty_results = pricing.priceAndNameFromResults(pricing.PriceItem(search_name="Machina Mitts", corrupted=False))
    # print(pretty_results)
    # print(getAvgPrice(pretty_results, 4))
    writeToDatabase()
    # results = pricing.priceAndNameFromResults(pricing.PriceItem(search_name="Yoke of Suffering"))
    # print(getAvgPrice(results, 2))