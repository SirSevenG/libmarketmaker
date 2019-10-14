import json
import requests
import ast


class MarketMaker2Proxy:

    def __init__(self, node="", userpass=""):
        self.node = node
        self.userpass = userpass

    @staticmethod
    def type_convert(bytez):
        """convert json to dictionary"""
        r = ast.literal_eval(bytez.decode("utf-8"))
        return r

    def send_requset(self, json_in):
        r = requests.post(self.node, json=json.dumps(json_in))
        return self.type_convert(r.content)

    def buy(self, base, rel, price, volume):
        request = {
                   "userpass": self.userpass,
                   "method": "buy",
                   "base": base,
                   "rel": rel,
                   "price": price,
                   "volume": volume
                  }
        r = self.send_requset(request)
        return r

    def cancel_all_orders(self, cancel_by_type="", cancel_by_data_base="",
                          cancel_by_data_rel="", cancel_by_data_ticker=""):
        request = {
                   "userpass": self.userpass,
                   "method": "cancel_all_orders",
                  }
        if cancel_by_type:
            if str(cancel_by_type).lower() == "all":
                request.update({"cancel_by": {
                    "type": "All"
                }}
                               )
            if str(cancel_by_type).lower() == "pair":
                if cancel_by_data_base and cancel_by_data_rel:
                    request.update({"cancel_by": {
                                                 "type": "Pair",
                                                 "data": {
                                                          "base": cancel_by_data_base,
                                                          "rel": cancel_by_data_rel
                                                         }
                                                }
                                    })
                if cancel_by_data_base and not cancel_by_data_rel:
                    request.update({"cancel_by": {
                                                 "type": "Pair",
                                                 "data": {
                                                          "base": cancel_by_data_base
                                                         }
                                                }
                                    })
                if cancel_by_data_rel and not cancel_by_data_base:
                    request.update({"cancel_by": {
                                                 "type": "Pair",
                                                 "data": {
                                                          "rel": cancel_by_data_rel
                                                         }
                                                }
                                    })
                else:
                    raise Exception("Invalid request:", cancel_by_type, cancel_by_data_rel, cancel_by_data_base)
            if str(cancel_by_type).lower() == "coin":
                if cancel_by_data_ticker:
                    request.update({"cancel_by": {
                                                 "type": "Coin",
                                                 "data": {"ticker": cancel_by_data_ticker}
                                                }
                                    })
                else:
                    raise Exception("Invalid request:", cancel_by_type, cancel_by_data_ticker)
        else:
            raise Exception("Invalid request:", cancel_by_type)
        r = self.send_requset(request)
        return r

    def cancel_order(self, uuid=""):
        request = {
                   "userpass": self.userpass,
                   "method": "cancel_order",
                   "uuid": uuid
                  }
        r = self.send_requset(request)
        return r

    def coins_needed_for_kick_start(self):
        request = {
                  "userpass": self.userpass,
                  "method": "coins_needed_for_kick_start"
                  }
        r = self.send_requset(request)
        return r

    def disable_coin(self, coin):
        request = {
                   "userpass": self.userpass,
                   "method": "disable_coin",
                   "coin": coin
                   }
        r = self.send_requset(request)
        return r

    def electrum(self, coin, servers_url="", servers_protocol="TCP",
                 servers_disablecert=False, mm2=1, tx_history=True):
        request = {
                   "userpass": self.userpass,
                   "method": "electrum",
                   "coin": coin,
                   "mm2": mm2,
                   "tx_history": tx_history
                  }
        if servers_url:
            serverlist = []
            for url in servers_url:
                serverlist.append({
                    "url": url,
                    "protocol": servers_protocol,
                    "disable_cert_verification": servers_disablecert
                })
            request.update({"servers": serverlist})
        r = self.send_requset(request)
        return r

    def enable(self, coin, urls, swap_contract_addr="0x7Bc1bBDD6A0a722fC9bffC49c921B685ECB84b94",
               gas_station_url='https://ethgasstation.info/json/ethgasAPI.json', mm2=1, tx_history=True):
        request = {
                   "userpass": self.userpass,
                   "method": "enable",
                   "coin": coin,
                   "mm2": mm2,
                   "tx_history": tx_history
                  }
        for url in urls:
            request.update({"urls": [url]})
        request.update({
                        "swap_contract_address": swap_contract_addr,
                        "gas_station_url": gas_station_url,
                       })
        r = self.send_requset(request)
        return r

    def get_enabled_coins(self):
        request = {
                   "userpass": self.userpass,
                   "method": "get_enabled_coins"
                   }
        r = self.send_requset(request)
        return r

    def get_trade_fee(self, coin):
        request = {
                   "userpass": self.userpass,
                   "method": "get_trade_fee",
                   "coin": coin
                   }
        r = self.send_requset(request)
        return r

    def import_swaps(self, swaps_data):
        request = {
                   "userpass": self.userpass,
                   "method": "import_swaps",
                   "swaps": swaps_data
                   }
        r = self.send_requset(request)
        return r

    def my_balance(self, coin):
        request = {
                   "userpass": self.userpass,
                   "method": "my_balance",
                   "coin": coin
                   }
        r = self.send_requset(request)
        return r

    def my_orders(self):
        request = {
                   "userpass": self.userpass,
                   "method": "my_orders"
                   }
        r = self.send_requset(request)
        return r

    def my_recent_swaps(self, limit, from_uuid):
        request = {
                   "userpass": self.userpass,
                   "method": "my_recent_swaps",
                   "limit": limit,
                   "from_uuid": from_uuid
                   }
        r = self.send_requset(request)
        return r

    def my_swap_status(self, uuid_str):
        request = {
                   "userpass": self.userpass,
                   "method": "my_swap_status",
                  }
        for uuid in uuid_str:
            request.update({"params": {"uuid": uuid}})
        r = self.send_requset(request)
        return r

    def my_tx_history(self, coin, limit, from_id):
        request = {
                   "userpass": self.userpass,
                   "method": "my_tx_history",
                   "coin": coin,
                   "limit": limit,
                   "from_id": from_id
                   }
        r = self.send_requset(request)
        return r

    def order_status(self, uuid):
        request = {
                   "userpass": self.userpass,
                   "method": "order_status",
                   "uuid": uuid
                   }
        r = self.send_requset(request)
        return r

    def orderbook(self, base, rel):
        request = {
                   "userpass": self.userpass,
                   "method": "orderbook",
                   "base": base,
                   "rel": rel
                   }
        r = self.send_requset(request)
        return r

    def recover_funds_of_swap(self, params_uuid):
        request = {
                   "userpass": self.userpass,
                   "method": "recover_funds_of_swap",
                   "params": {"uuid": params_uuid}
                   }
        r = self.send_requset(request)
        return r

    def sell(self, base, rel, price, volume):
        request = {
                   "userpass": self.userpass,
                   "method": "sell",
                   "base": base,
                   "rel": rel,
                   "price": price,
                   "volume": volume
                   }
        r = self.send_requset(request)
        return r

    def send_raw_tx(self, coin, tx_hex):
        request = {
                   "userpass": self.userpass,
                   "method": "send_raw_tx",
                   "coin": coin,
                   "tx_hex": tx_hex
                   }
        r = self.send_requset(request)
        return r

    def setprice(self, base, rel, price, volume, set_max=False, cancel_previous=False):
        request = {
                   "userpass": self.userpass,
                   "method": "setprice",
                   "base": base,
                   "rel": rel,
                   "price": price,
                   "volume": volume,
                   "max": set_max,
                   "cancel_previous": cancel_previous
                   }
        r = self.send_requset(request)
        return r

    def set_required_confirmations(self, coin, confirmations):
        request = {
                   "userpass": self.userpass,
                   "method": "set_required_confirmations",
                   "coin": coin,
                   "confirmations": confirmations
                   }
        r = self.send_requset(request)
        return r

    def stop(self):
        request = {
                   "userpass": self.userpass,
                   "method": "stop"
                  }
        r = self.send_requset(request)
        return r

    def version(self):
        request = {
                   "userpass": self.userpass,
                   "method": "version"
                  }
        r = self.send_requset(request)
        return r

    def withdraw(self, coin, to, amount, fee_type="", fee_amount="",
                 fee_gas_price="", fee_gas="", smax="false"):
        request = {
                   "userpass": self.userpass,
                   "method": "withdraw",
                   "coin": coin,
                   "to": to,
                   "amount": amount,
                   "max": smax
                  }
        if fee_type == "UtxoFixed" or fee_type == "UtxoPerKbyte":
            request.update(
                  {"fee": {
                         "type": fee_type,
                         "amount": fee_amount,
                        }})
        elif fee_type == "EthGas":
            request.update(
                   {"fee": {
                         "gas_price": fee_gas_price,
                         "gas": fee_gas
                        }})
        else:
            raise Exception("Unknown fee type: ", fee_type)
        r = self.send_requset(request)
        return r
