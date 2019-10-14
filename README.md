# libmarketmaker
Python3 library to proxy marketmaker2 rp calls.

This lib intended to be used in python-based tests/applications,
 if you need python mm2 interface for personal usage, check smk'762s PytomicDEX:
 https://github.com/smk762/pytomicDEX

API reference: https://developers.atomicdex.io/basic-docs/atomicdex/atomicdex-api.html

Based on requests library https://requests.kennethreitz.org/en/master/

    pip install requests

Usage example:

    from mm2rpclib import MarketMaker2Proxy
    
    # node = http(s)://domian/or/ip:port
    node = http://127.0.0.1:7783
    userpas = YourRPCPassword
    rpc = MarketMaker2Proxy(node, userpass)
    
    rpc.version()

All RPC methods will return dictionary with server's response, AE:

    coin = 'KMD'  # str
    electrum_url = 'electrum.example.net:10001'  # domain:port
    r = rpc.electrum(coin, electrum_url)
    print(r)
    print(type(r))
###
    {'address': '0000000000000000000000000000000000', 'balance': '0', 'coin': 'KMD',
     'locked_by_swaps': '0', 'required_confirmations': 1, 'result': 'success'}
    <class 'dict'>