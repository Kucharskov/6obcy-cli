#!/usr/bin/env python3

from json import loads, dumps
from urllib.parse import urlencode
from requests import get


class APIHelpers:

    def getConnectionData() -> dict:
        try:
            url = "https://6obcy.org/ajax/addressData"
            data = get(url).json()
            adress = "{}:{}".format(data["host"], data["port"])

        except:
            return None

        url = "wss://{}/6eio/?".format(adress)
        params = {
            "EIO": 3,
            "transport": "websocket"
        }
        url += urlencode(params)

        return {
            "adress": adress,
            "url": url
        }

    def getProxy() -> dict:
        try:
            url = "https://api.getproxylist.com/proxy?"
            params = {
                "allowsHttps": 1,
                "protocol[]": "http"
            }
            url += urlencode(params)
            data = get(url).json()
            adress = "{}:{}".format(data["ip"], data["port"])

        except:
            return None

        return {
            "adress": adress,
            "ip": data["ip"],
            "port": int(data["port"])
        }
