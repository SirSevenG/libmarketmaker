# libmarketmaker
Python3 library to proxy marketmaker2 rp calls.

This lib intended to be used in python-based applications,
 if you need python mm2 interface for personal usage, check smk'762s PytomicDEX:
 https://github.com/smk762/pytomicDEX

API reference: https://developers.atomicdex.io/basic-docs/atomicdex/atomicdex-api.html

## Variants:

`mm2_rpclib_req` based on requests library https://requests.kennethreitz.org/en/master/

Deps:

    pip install requests ujson

`mm2_rpclib_curl` based on slick-bitcoinrpc https://github.com/barjomet/slick-bitcoinrpc

Deps:

    pip install ujson pycurl itertools
    or
    pip install slick-bitcoinrpc

### Usage example:

```python
    from mm2rpclib_req import MarketMaker2Proxy
    
    host = {
        'userpass': 'yyVdXlv1sdcmEhd9',
        'rpchost': '95.217.236.53',
        'rpcport': 7783
    }
    proxy = MMProxy(host)
    
    proxy.version()
```

RPC params should be passed as **kwargs:

```shell script
    curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"orderbook\",\"base\":\"KMD\",\"rel\":\"BTC\"}
```

Will be:

```python
    proxy.orderbook(base='KMD', rel='BTC')
```

All RPC methods will return dictionary with server's response,
 errors are returned as is, AE:

```python
    coin = 'KMD'  # str
    electrum_url = "example.domain.net:0000"  # domain:port
    r = proxy.electrum(coin=coin, servers=[{'url': electrum_url, 'protocol': 'TCP'}], mm2='1')
    print(r)
    print(type(r))
    r = proxy.electrum(coin=coin, servers=[{'url': electrum_url, 'protocol': 'TCP'}], mm2='1')
    print(r)
    print(type(r))
```

```text
    {'address': '0000000000000000000000000000000000', 'balance': '0', 'coin': 'KMD',
     'locked_by_swaps': '0', 'required_confirmations': 1, 'result': 'success'}
    <class 'dict'>
    {'error': 'rpc:339] lp_commands:85] lp_coins:643] Coin KMD already initialized'}
    <class 'dict'>
```

### Batch requests:

Batch requests should be passed as dictionary via batch() method.

Example to batch 10 identical setprice calls:

```python
    req = {
        "method": "setprice", "base": base, "rel": rel, "price": price, "volume": volume, "cancel_previous": False
    }
    rec_d = {}
    for i in range(10):
        rec_d.update({str(i): req})
    res = proxy.batch(**rec_d)
```
