import requests
import maxminddb
import re
import traceback
from sys import argv

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

def is_valid(proxy):
    RE_EXP = r'(^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]))\:\d{2,5}'
    if (re.match(RE_EXP, proxy)):
        return True
    return False

def geo_db_reader(proxy):
    ip = proxy.split(':')[0]
    try:
        reader = maxminddb.open_database('dbip-country-lite-2020-02.mmdb')
        result = reader.get(ip)
        print(result['continent']['names']['en'])
    except Exception as err:
        print(traceback.format_exc())

def process_ip(proxy):
    if is_valid(proxy):
        geo_db_reader(proxy)
        test_proxy(proxy)
    else: 
        print('Invalide proxy:', proxy)

if __name__ == "__main__":
    input_args = argv[1:]
    for item in input_args:
        if item.endswith('.txt'):
            print('This is a text file')
        else:
            process_ip(item)
    