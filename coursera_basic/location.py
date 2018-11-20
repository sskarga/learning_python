import requests

# geoip */

def get_location_info():
    return requests.get("https://ipstack.com/ipstack_api.php?ip=146.120.215.166&language=ru").json()

if __name__ == "__main__":
    print(get_location_info())