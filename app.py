import requests
import maxminddb
import re

PROXY = '207.246.78.249:80'
PING_URL = 'https://www.google.com'
HEADER = ''

def test_proxy(proxy = None):
    if not proxy:
        proxies = {}
    else:
        proxies = {'http': proxy, 'https': proxy,}
    try:
        res = requests.get(PING_URL, proxies=proxies, timeout=60)
        if (res.status_code == 200):
            print('Proxy is working')
            print('Response time', res.elapsed.total_seconds(), 'seconds')
    except Exception as err:
        print('The proxy is down')
        # print(err)

def is_valid(proxy):
    RE_EXP = r'(^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]))\:\d{2,5}'
    if (re.match(RE_EXP, proxy)):
        return True
    return False

def geo_db_reader(proxy):
    ip = proxy.split(':')[0]
    # print(ip)
    reader = maxminddb.open_database('dbip-country-lite-2020-02.mmdb')
    result = reader.get(ip)
    print(result['continent']['names']['en'])

    
if __name__ == "__main__":
    if(is_valid(PROXY)):
        geo_db_reader(PROXY)
        test_proxy(PROXY)
    