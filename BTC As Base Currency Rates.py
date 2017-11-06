import hashlib
import hmac
import json
import requests
import multiprocessing as mp
from functools import partial
import pandas as pd
from datetime import datetime as dt


API_URL = 'https://api.changelly.com'
API_KEY = 'Your Key Here' #Log onto changelly.com -- Go to tools & select "API for Developers" -- The Key and Secret will be on this page
API_SECRET = 'Your Secret here Here'


def getrate(Counter, Base):
    message = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getExchangeAmount',
        'params': {
            "from": Base,
            "to": Counter,
            "amount": "1"
        },
    }
    serialized_data = json.dumps(message)

    sign = hmac.new(API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()

    headers = {'api-key': API_KEY, 'sign': sign, 'Content-type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=serialized_data)
    pair = str(Base + "/" + Counter)
    return(pair,(response.json())['result'])

def main():
    Counter = ['1st', 'adx', 'amp', 'ant', 'ardr', 'bat', 'bcc', 'bcn', 'bnt', 'btc', 'cfi', 'cvc', 'dash', 'dcr', 'dct', 'dgd', 'doge', 'edg', 'eos', 'etc', 'eth', 'exp', 'fcn', 'fun', 'game', 'gbg', 'gbyte', 'gno', 'gnt', 'golos', 'gup', 'hmq', 'lbc', 'lsk', 'ltc', 'lun', 'maid', 'mco', 'mln', 'mtl', 'myst', 'nav', 'nbt', 'neo', 'nlg', 'nmr', 'nxt', 'omg', 'pay', 'pivx', 'pot', 'ptoy', 'qcn', 'rads', 'rep', 'rlc', 'salt', 'sbd', 'sngls', 'snt', 'steem', 'storj', 'str', 'strat', 'swt', 'sys', 'time', 'tkn', 'trst', 'usdt', 'waves', 'wings', 'xaur', 'xdn', 'xem', 'xmr', 'xrp', 'zec', 'zrx']
    Base = "btc"
    P = mp.Pool(8)
    func = partial(getrate,Base = Base)
    x = (P.map(func,Counter))
    P.close()
    P.join()
    ind = []
    data = []
    for each in x:
        ind.append(each[0])
        data.append(each[1])
    df = pd.DataFrame(data=data,index = ind,columns=[dt.utcnow()])
    print (df)

if __name__ == '__main__':
    main()