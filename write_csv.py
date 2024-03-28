import csv
import pricing
import schedule
import time

def writeMirrorDivineData():
    with open('mirror_data.csv', 'a', newline='') as file:
        baseType = "Divine Orb"
        writer = csv.writer(file)
        rows = pricing.priceAndNameFromResults(pricing.PriceItem(search_basetype="Mirror of Kalandra"))
        rows += pricing.priceAndNameFromResults(pricing.PriceItem(search_basetype="Divine Orb"))
        result = writer.writerows(rows)
        print("WROTE CURRENCY DATA", "@", time.ctime())
    return True
        

if __name__ == "__main__":
    schedule.every(10).minutes.do(job_func=writeMirrorDivineData) 
    print("starting...", time.ctime())
    while True:
        schedule.run_pending() 
        time.sleep(1) 
    # writeMirrorDivineData()