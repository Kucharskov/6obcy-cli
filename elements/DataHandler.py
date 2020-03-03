#!/usr/bin/env python3


class DataHandler:

    def __init__(self) -> None:
        self.data = {}
        self.data["server"] = None
        self.data["proxy"] = None
        self.data["talking"] = False
        self.data["ceid"] = 1

    def get(self, key: str):
        """ Simple getter for elements in data dict, if requested element doesnt exist returns None """

        if key in self.data:
            return self.data[key]
        return None

    def set(self, key: str, value) -> None:
        """ Simple setter for elements in data dict """

        self.data[key] = value

    def handle(self, data: dict) -> None:
        """ Handle for receiving data as dict from parsed packets """

        type = data["ev_name"]
        if type == "cn_acc":
            """ Packet with server connection acceptation. Contains a hash for message signing """
            self.set("hash", data["ev_data"]["hash"])

        elif type == "talk_s":
            """ Packet with new stranger chat proposal which script always accept """
            print("[*] Połączono z obcym")
            self.set("idn", 0)
            self.set("talking", True)
            ckey = data["ev_data"]["ckey"]
            self.set("ckey", ckey)

            if ckey.startswith("F"):
                print("[!] Nawiązane połączenie wygląda na sztuczne, co świadczy o Twojej blokadzie!")
                print("[!] Rozmówca może nie być prawdziwy, a niektóre polecenia moga nie działać.")

        elif type == "sdis":
            """ Packet with information about disconnecting from conversation """
            print("[*] Rozmowa została zakończona")
            self.set("talking", False)
            self.set("ckey", None)

        elif type == "count":
            """ Packet with amount of connected strangers """
            self.set("count", data["ev_data"])

        elif type == "rmsg":
            """ Packet with received message """
            print("< {}".format(data["ev_data"]["msg"]))

        elif type == "rtopic":
            """ Packet type with a random topic for conversation """
            print("[*] Wylosowany temat: {}".format(data["ev_data"]["topic"]))

        elif type == "styp":
            """ Packet with info when stranger is typeing (or not) """
            pass

        elif type == "convended":
            """ Packet received when script sends a message to closed conversation """
            pass

        elif type == "r_svmsg":
            """ Packet with useless advertisement """
            pass

        else:
            """ Other unexpected packet """
            #print(data)
            pass

