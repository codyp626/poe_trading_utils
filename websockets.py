# wss://www.pathofexile.com/api/trade/live/Affliction/D2blMW5T5


# Need ORIGIN HEADER
# 401 = bad POESESSIONID
# 404 = bad header somewhere
# ------------------------------------------------------------------------------------------------------------------------------------------------------

import pricing
import whisper

import json
import requests
import websocket
import _thread
import time
import rel

# lots of expensive uniques
# bMBOQaLfL
headers = pricing.getHeaders()

def on_message(ws, message):
    # print("MESSAGE STR=", message)
    message = json.loads(message)
    if message['new']:
        # print("PRICING ITEM")
        # print("got hash:", message['new'])
        results = pricing.getItemResults(message['new'])
        for result in results:
            print("found", result['item']['name'], "@", result['listing']['price']['amount'], result['listing']['price']['currency'])
            whisper.sendWhisper(result['listing']['whisper_token'])
            
def on_error(ws, error):
    print(error)
    # return
    if error == 'new':
        return
    else:
        return
        # print("error:",end='')
        # print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    # websocket.enableTrace(True)
    # print("\n\n")
    # print("headers:", headers)
    # print("\n\n")
    ws = websocket.WebSocketApp("wss://www.pathofexile.com/api/trade/live/Affliction/bMBOQaLfL",
                              header=headers,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()