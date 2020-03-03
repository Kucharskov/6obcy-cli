#!/usr/bin/env python3

from json import loads, dumps


class PacketParser:

    def unpack(data: str) -> dict:
        """ Trims packet type number and unpack to dict containing data """

        if data == "":
            return None

        data = data[1:]

        if data == "":
            return None

        return loads(data)

    def pack(type: str, data: dict = None, ceid: int = None) -> str:
        """ Pack a string with know type of event. Regarding to reversed protocol - eventually adds a data and counter """

        packet = {}
        packet["ev_name"] = type

        if data is not None:
            packet["ev_data"] = data

        if ceid is not None:
            packet["ceid"] = ceid

        return str(4) + dumps(packet)
