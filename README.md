# Simple HTTP Proxy Tester with Geolocation support

- accept single or multiple input 'IP:PORT' pair separated by space

## Usage:

1. Clone or Download as Zip
2. Navigate to this folder
3. Create python venv
4. Install dependencies from requirements.txt
5. python app.py "IP:PORT" or python app.py "list.txt"

*see list.txt for example of input file format

Linux / MacOS X
```sh
cd proxy_tester
python3 -m venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows
```sh
cd proxy_tester
python3 -m venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

Using [IP Geolocation by DB-IP](https://db-ip.com) lite version
