from pprint import pprint
from getjson import getjson
import requests

# Hardwired defaults

CONFIG_URL = 'http://config.microprediction.org/config.json'
FAILOVER_CONFIG_URL = 'http://stableconfig.microprediction.org/config.json'
API_URL = 'http://api.microprediction.org'
FAILOVER_API_URL = 'http://stableapi.microprediction.org'


def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def api_url():
    return API_URL


def failover_api_url():
    return FAILOVER_API_URL


def get_config():
    return getjson(CONFIG_URL)


if __name__ == "__main__":
    answer = get_config()
    pprint(answer)
