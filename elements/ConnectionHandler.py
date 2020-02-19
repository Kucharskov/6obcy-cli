#!/usr/bin/env python3

from elements.PacketParser import *
from elements.DataHandler import *
from elements.Heartbeat import *
from elements.Receiver import *
from websocket import create_connection


class ConnectionHandler:

    def __init__(self, url: str, dataHandler: DataHandler) -> None:
        self.url = url
        self.ws = None
        self.dataHandler = dataHandler
        self.receiver = Receiver(self, self.dataHandler)
        self.heartbeat = Heartbeat(self)

    def connect(self) -> None:
        """ Create a connection to websocket, also waits for first '0' config packet """

        self.ws = create_connection(self.url, enable_multithread=True)

        packet = self.readRawData()
        data = PacketParser.unpack(packet)

        self.receiver.start()
        self.heartbeat.setTimeout(data["pingInterval"])
        self.heartbeat.start()

    def disconnect(self) -> None:
        """ Disconnects websocket and stops all threads """

        self.ws.close()
        self.receiver.stop()
        self.receiver.join()
        self.heartbeat.stop()
        self.heartbeat.join()

    def writeData(self, type: str, data: dict = None, count: bool = False) -> None:
        """ Sends a prepared packet with known type, optional data as dict and counter as 'ceid' element in packet """

        ceid = self.dataHandler.get("ceid")
        packet = ""

        if count:
            packet = PacketParser.pack(type, data, ceid)
            self.dataHandler.set("ceid", ceid + 1)

        else:
            packet = PacketParser.pack(type, data)

        self.ws.send(packet)

    def readData(self) -> dict:
        """ Receive and return one parsed packet """

        packet = self.ws.recv()
        data = PacketParser.unpack(packet)
        return data

    def writeRawData(self, data: str) -> None:
        """ Sends to socket one raw string """

        self.ws.send(data)

    def readRawData(self) -> str:
        """ Reads and returns from socket one raw data string """

        return self.ws.recv()