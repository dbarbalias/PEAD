import requests
import pandas as pd
import json
from datetime import datetime

api = 'https://financialmodelingprep.com/api/v3/company/stock/list'
response = requests.get(api).content.decode('utf-8')
symbol_list = json.loads(response)['symbolsList']
symbol_list = [i['symbol'] for i in symbol_list]

if __name__ == '__main__':
    x = pd.DataFrame(symbol_list)
    run_date = datetime.now().date()
    x.to_csv(f'tic_list_{run_date}.csv')
