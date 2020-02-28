#!/usr/bin/env python3

from elements.DataHandler import *
from elements.ConnectionHandler import *
from cmd import Cmd
from time import sleep
from requests import get


class Client(Cmd):

    intro = '''[*] 6obcy-cli with love by M. Kucharskov (http://kucharskov.pl)\n[*] Wpisz ".help" po listę dostępnych poleceń\n'''
    prompt = "> "
    use_rawinput = False

    def __init__(self) -> None:
        super(Client, self).__init__()

        connData = get("https://6obcy.org/ajax/addressData").json()
        urlBase = "{}:{}".format(connData["host"], connData["port"])

        url = "wss://{}/6eio/?EIO=3&transport=websocket".format(urlBase)
        self.intro += "[*] Adres serwera: {}".format(urlBase)

        self.dataHandler = DataHandler()
        self.connection = ConnectionHandler(url, self.dataHandler)
        self.connection.connect()

    def preloop(self) -> None:
        """
        Inherited command from Cmd object
        Its initiate connection with server through socket
        """

        hash = self.dataHandler.get("hash")
        data = {
            "cvdate": "2017-08-01",
            "mobile": False,
            "cver": "v2.5",
            "adf": "ajaxPHP",
            "hash": hash,
            "testdata": {
                "ckey": 0,
                "recevsent": False
            }
        }
        self.connection.writeData("_cinfo", data)
        self.connection.writeData("_owack")

    def postloop(self) -> None:
        """
        Inherited command from Cmd object
        Its closes connection after exiting from cmdloop
        """

        self.connection.disconnect()

    def sendMessage(self, msg: str) -> None:
        """ Sends a prepared packet if its connected with stranger """

        if not self.dataHandler.get("talking"):
            print("[!] Nie jesteś połączony!")
            return

        #msg = msg.replace("E", "Ε")
        ckey = self.dataHandler.get("ckey")
        idn = self.dataHandler.get("idn")
        data = {
            "ckey": ckey,
            "msg": msg,
            "idn": idn
        }
        self.connection.writeData("_pmsg", data, True)
        self.dataHandler.set("idn", idn + 1)

    def joinTalk(self) -> None:
        """ Sends a prepared packet to search a stranger """

        if self.dataHandler.get("talking"):
            print("[!] Jesteś już połączony!")
            return

        data = {
            "channel": "main",
            "myself": {
                "sex": 0,
                "loc": 0
            },
            "preferences": {
                "sex": 0,
                "loc": 0
            }
        }
        self.connection.writeData("_sas", data, True)
        print("[*] Oczekiwanie na rozmówcę...")

        while not self.dataHandler.get("talking"):
            sleep(0.25)

        ckey = self.dataHandler.get("ckey")
        data = {
            "ckey": ckey
        }
        self.connection.writeData("_begacked", data, True)

    def quitTalk(self) -> None:
        """ Sends a prepared packet to quit from conversation """

        if not self.dataHandler.get("talking"):
            print("[!] Nie jesteś połączony!")
            return

        ckey = self.dataHandler.get("ckey")
        data = {
            "ckey": ckey
        }
        self.connection.writeData("_distalk", data, True)

        while self.dataHandler.get("talking"):
            sleep(0.25)

    def reportTalk(self) -> None:
        """ Sends a prepared packet to report actual stranger """

        if not self.dataHandler.get("talking"):
            print("[!] Nie jesteś połączony!")
            return

        ckey = self.dataHandler.get("ckey")
        data = {
            "ckey": ckey
        }
        self.connection.writeData("_reptalk", data, True)
        print("[*] Rozmówca został zgłoszony")

    def randomizeTopic(self) -> None:
        """ Sends a prepared to use server-side magic which randomize topics to talk """

        if not self.dataHandler.get("talking"):
            print("[!] Nie jesteś połączony!")
            return

        ckey = self.dataHandler.get("ckey")
        data = {
            "ckey": ckey
        }
        self.connection.writeData("_randtopic", data, True)

    def default(self, line: str) -> bool:
        """
        Inherited command from Cmd object
        Overrided to handle commands which starts from dot, rest is interpreted as message
        To exit cmdloop it returns True
        """

        if line.startswith("."):
            line = line[1:]
            cmd = line.split(" ")[0]

            if cmd == "join":
                self.joinTalk()

            elif cmd == "quit":
                self.quitTalk()

            elif cmd == "next":
                if self.dataHandler.get("talking"):
                    self.quitTalk()

                self.joinTalk()

            elif cmd == "report":
                self.reportTalk()

            elif cmd == "topic":
                self.randomizeTopic()

            elif cmd == "count":
                print("[*] Aktualnie połączonych: {}".format(self.dataHandler.get("count")))

            elif cmd == "help":
                self.do_help(None)

            elif cmd == "exit":
                if self.dataHandler.get("talking"):
                    self.quitTalk()

                print("[*] Zamykanie połączenia...")
                return True

            else:
                print("[!] Nierozpoznana komenda")

        else:
            self.sendMessage(line)


    def do_help(self, arg) -> None:
        """
        Inherited command from Cmd object
        Its overriden to hide strange help content and show my implementation
        """
        
        print('''[*] Lista dostępnych poleceń:
.join\t\trozpoczyna kolejną rozmowę
.quit\t\tkończy aktualną rozmowę
.next\t\ttechnicznie to quit&join
.report\t\tzgłoszenie aktualnego rozmówcy
.topic\t\twylosowanie tematu rozmowy
.count\t\twyświetla ilość użytkowników na 6obcy
.exit\t\tzamyka aplikację
.help\t\twyświetla to okno listy poleceń''')

    def emptyline(self) -> None:
        """
        Inherited command from Cmd object
        Prevend sending the same message few times
        """
        pass
