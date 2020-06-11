import requests
import maxminddb
import re
import traceback
from sys import argv

# PROXY = '207.246.78.249:80'
# TODO: 
# - [x] test local speed as baseline
# - [ ] accept custom url
# - [ ] accept custom header
# - [ ] output result to file

PING_URL = 'https://www.google.com'
HEADER = ''

def test_proxy(proxy = None):
    print('testing proxy:', proxy)
    if not proxy: proxies = {}
    else: proxies = {'http': proxy, 'https': proxy,}
    try:
        res = requests.get(PING_URL, proxies=proxies, timeout=60)
        if (res.status_code == 200):
            # print('Proxy is working')
            # print('Response time', res.elapsed.total_seconds(), 'seconds')
            return { 'working': True, 'response_time': res.elapsed.total_seconds()}
    except Exception as err:
        # print('The proxy is down')
        return { 'working': False, 'response_time': None }

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
        # print(result['continent']['names']['en'])
        return { 'region': result['continent']['names']['en'] }
    except Exception as err:
        # print(traceback.format_exc())
        return { 'region': 'error' }

def process_ip(proxy):
    status = {'proxy': proxy }
    if is_valid(proxy):
        status.update(geo_db_reader(proxy))
        status.update(test_proxy(proxy))
        return status
    else: 
        print('Invalid proxy:', proxy)
        return { 'invalid': True, 'proxy': proxy}

def file_handler(input_file):
    data_string = ''
    validated = []
    with open(input_file, 'r') as myfile:
        data_string = myfile.read()
    # print(data_string)
    if data_string:
        data_string = data_string.replace('\n', ' ')
        data_array = data_string.split(' ')
        data_array = list(dict.fromkeys(data_array))
        print(f'Processing {len(data_array)} unique proxy...')
        for item in data_array:
            result = process_ip(item)
            if 'invalid' not in result:
               validated.append(result)
        return validated

def test_local():
    status = {'proxy': None}
    status.update(test_proxy())
    return status

def generate_report(result = []):
    for item in result:
        print(item)


if __name__ == "__main__":
    try:
        input_args = argv[1:]
        result = []
        result.append(test_local())
        for item in input_args:
            if item.endswith('.txt'):
                print('This is a text file')
                result.extend(file_handler(item))
                generate_report(result)
            else:
                print('Processing')
            print(process_ip(item))
    except Exception as err:
        print(traceback.format_exc())
