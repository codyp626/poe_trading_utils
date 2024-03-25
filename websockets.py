# wss://www.pathofexile.com/api/trade/live/Affliction/D2blMW5T5

# HEADERS---------------------------------------------------------------------------

# GET wss://www.pathofexile.com/api/trade/live/Affliction/D2blMW5T5 HTTP/1.1
# Host: www.pathofexile.com
# Connection: Upgrade
# Pragma: no-cache
# Cache-Control: no-cache
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36
# Upgrade: websocket
# Origin: https://www.pathofexile.com
# Sec-WebSocket-Version: 13
# Accept-Encoding: gzip, deflate, br, zstd
# Accept-Language: en-US,en;q=0.9
# Cookie: _ga=GA1.1.1911120562.1710427136; POESESSID=22ac0e4ca3ff4ceaa54324c42e7d388b; _ga_R6TM1WQ9DW=GS1.1.1710427136.1.1.1710428387.0.0.0
# Sec-WebSocket-Key: wxSFP2o5Q4RIx6iLQso8Kw==
# Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits


# NeED ORIGIN HEADER
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