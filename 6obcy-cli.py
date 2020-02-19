#!/usr/bin/env python3

from elements.Client import Client

url = "wss://server.6obcy.pl:7003/6eio/?EIO=3&transport=websocket"
client = Client(url)
client.cmdloop()
