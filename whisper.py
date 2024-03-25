#https://www.pathofexile.com/api/trade/whisper

#headers
import json
import requests
import pricing

def sendWhisper(token):
    url = "https://www.pathofexile.com/api/trade/whisper"
    payload = {"token": token}
    headers = pricing.getHeaders()
    headers['x-requested-with'] = "XMLHttpRequest"
    
    # print(headers)
    print("sending whisper... (fake)")
    return True
    # response = requests.post(url, headers=headers, data=payload)
    # print("response:", response, "\n")
    # print(response.text)
    # if "200" in response:
    #     return True
    # else:
    #     return False


if __name__ == "__main__":
    test_token = {"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzMzE1NmZjYTQwNWJmZGQwYTUyZTRhN2M1MWZmYmI5ZSIsImlzcyI6ImJNQk9RYUxmTCIsImF1ZCI6IjE1NjMzYWEwLTk2NmQtNGYxNS05YjhjLWQ2MzI3MDQxYzJlNyIsImRzdCI6IlBsYXRpbnVtRmF0aGVyT0ciLCJsb2MiOiJlbl9VUyIsInRvayI6Iml0ZW0iLCJzdWIiOiI5OTljNGY2NjI5N2IxOGI0ZjExMTAzNGFhZTNkMTkzZTQyOGQ5OGJkMDhiODIyNjYyYTA3ZGM4YzAyZDA1N2FhIiwiZGF0IjoiZDU3ZDFkMjRhOWVhODViZWRhYjNiMjExNzY5NThhZWEiLCJpYXQiOjE3MTA1Mjc3OTIsImV4cCI6MTcxMDUyODA5Mn0.qGnoai0QgiEFWvDnvDxHfQMqXvaEArCk3So0HNY863U"}
    sendWhisper(test_token)
    
    
