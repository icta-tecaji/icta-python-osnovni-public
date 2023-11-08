import requests


def get_my_ip():
    response = requests.get("http://ipinfo.io/json")
    return response.json()["ip"]
