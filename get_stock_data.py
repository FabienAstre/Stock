import os
import datetime
import urllib.request  # <- Python 3 version of urllib2
from dateutil.parser import parse
import threading

# Ensure the Quandl API key is set in your environment
assert 'QUANDL_KEY' in os.environ
quandl_api_key = os.environ['QUANDL_KEY']

class Nasdaq:
    def __init__(self):
        self.output = './stock_data'
        self.company_list = './companylist.csv'

    def build_url(self, symbol):
        url = f'https://www.quandl.com/api/v3/datasets/WIKI/{symbol}.csv?api_key={quandl_api_key}'
        return url

    def symbols(self):
        symbols = []
        with open(self.company_list, 'r') as f:
            next(f)  # skip header
            for line in f:
                symbols.append(line.split(',')[0].strip())
        return symbols

def download(i, symbol, url, output):
    print(f'Downloading {symbol} {i}')
    try:
        with urllib.request.urlopen(url) as response:
            quotes = response.read().decode('utf-8')  # decode bytes to string
            lines = quotes.strip().split('\n')
        # Ensure output directory exists
        if not os.path.exists(output):
            os.makedirs(output)
        # Save CSV
        with open(os.path.join(output, f"{symbol}.csv"), 'w') as f:
            for line in lines:
                f.write(line + '\n')
    except Exception as e:
        print(f'Failed to download {symbol}')
        print(e)

def download_all():
    nas = Nasdaq()
    for i, symbol in enumerate(nas.symbols()):
        url = nas.build_url(symbol)
        download(i, symbol, url, nas.output)

if __name__ == '__main__':
    download_all()
