import requests


def get_my_public_ip():
    response = requests.get("https://ipinfo.io/json")
    if response.status_code == 200:
        return (response.status_code, response.json()["ip"])
    else:
        return (response.status_code, None)
