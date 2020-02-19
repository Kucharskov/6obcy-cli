#!/usr/bin/env python3

from elements.DataHandler import *
from elements.ConnectionHandler import *
from cmd import Cmd
from time import sleep


class Client(Cmd):

    prompt = "> "

    def __init__(self, url) -> None:
        super(Client, self).__init__()
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

                sleep(0.25)
                self.joinTalk()

            elif cmd == "report":
                self.reportTalk()

            elif cmd == "topic":
                self.randomizeTopic()

            elif cmd == "count":
                print("[*] Aktualnie połączonych: {}".format(self.dataHandler.get("count")))

            elif cmd == "exit":
                print("[*] Zamykanie połączenia...")
                return True

            else:
                print("[!] Nierozpoznana komenda")

        else:
            self.sendMessage(line)

    def emptyline(self) -> None:
        """
        Inherited command from Cmd object
        Prevend sending the same message few times
        """
        pass
