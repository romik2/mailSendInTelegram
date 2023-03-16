import requests

url = "https://api.telegram.org/bot"

def send_messages(token, params):
    res = requests.get(('{}{}/sendMessage').format(url, token), params=params)
    print(res.json())
    return res.json()