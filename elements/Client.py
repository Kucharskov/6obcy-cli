#!/usr/bin/env python3

from elements.DataHandler import *
from elements.ConnectionHandler import *
from elements.APIHelpers import *
from cmd import Cmd
from time import sleep
from requests import get


class Client(Cmd):

    intro = '''[*] 6obcy-cli with love by M. Kucharskov (http://kucharskov.pl)\n[*] Wpisz ".help" po listę dostępnych poleceń\n'''
    prompt = "> "
    use_rawinput = False

    def __init__(self) -> None:
        super(Client, self).__init__()
        self.dataHandler = DataHandler()
        self.connection = ConnectionHandler(self.dataHandler)

        connectionData = APIHelpers.getConnectionData()
        self.intro += "[*] Adres serwera: {}".format(connectionData["adress"])

        self.connection.connect(connectionData["url"])
        self.dataHandler.set("server", connectionData["adress"])

    def reconnect(self, impersonate: bool = False) -> None:
        if self.dataHandler.get("talking"):
            print("[!] Najpierw zakończ rozmowę!")
            return

        connectionData = APIHelpers.getConnectionData()

        if impersonate:
            proxy = APIHelpers.getProxy()
            if proxy is None:
                print("[!] Wystąpił problem pobierania danych proxy!")
                return

            ip = proxy["ip"]
            port = proxy["port"]

            print("[*] Próba łączenia przez proxy: {} (Ctrl+C aby przerwać)".format(proxy["adress"]))

            if self.connection.connect(connectionData["url"], (ip, port)):
                print("[*] Pomyślnie połączono przez serwer pośredniczący")
                self.dataHandler.set("proxy", proxy["adress"])

                print("[*] Adres serwera: {}".format(connectionData["adress"]))
                self.dataHandler.set("server", connectionData["adress"])

            else:
                print("[!] Wystapił problem podczas łączenia!")

        else:
            self.connection.connect(connectionData["url"])

            print("[*] Adres serwera: {}".format(connectionData["adress"]))
            self.dataHandler.set("server", connectionData["adress"])
            self.dataHandler.set("proxy", None)

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

        if self.dataHandler.get("obfuscation"):
            msg = msg.replace("a", "а")
            msg = msg.replace("A", "Α")
            msg = msg.replace("e", "е")
            msg = msg.replace("E", "Ε")
            msg = msg.replace("i", "і")
            msg = msg.replace("I", "Ι")
            msg = msg.replace("d", "ԁ")
            msg = msg.replace("h", "һ")
            msg = msg.replace("H", "Н")

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
            params = line.split(" ")[1:]

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
                count = self.dataHandler.get("count")
                if count is None:
                    count = "Brak danych"

                print("[*] Aktualnie połączonych: {}".format(count))

            elif cmd == "impersonate":
                self.reconnect(True)

            elif cmd == "reconnect":
                self.reconnect(False)

            elif cmd == "obfuscate":
                obfuscation = self.dataHandler.get("obfuscation")
                if obfuscation:
                    self.dataHandler.set("obfuscation", False)
                    print("[*] Obfuskacja wyrazów: Wyłączona")

                else:
                    self.dataHandler.set("obfuscation", True)
                    print("[*] Obfuskacja wyrazów: Włączona")

            elif cmd == "help":
                self.do_help(None)

            elif cmd == "exit":
                if self.dataHandler.get("talking"):
                    self.quitTalk()

                print("[*] Zamykanie połączenia...")
                return True

            elif cmd == "debug":
                print("[*] Dane techniczne:")
                print("[*] - server: {}".format(self.dataHandler.get("server")))
                print("[*] - hash: {}".format(self.dataHandler.get("hash")))
                print("[*] - ckey: {}".format(self.dataHandler.get("ckey")))
                print("[*] - proxy: {}".format(self.dataHandler.get("proxy")))

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
[*] Polecenia zwykłe
.help\t\t\twyświetla to okno listy poleceń
.join\t\t\trozpoczyna kolejną rozmowę
.quit\t\t\tkończy aktualną rozmowę
.next\t\t\ttechnicznie to quit&join
.count\t\t\twyświetla ilość użytkowników na 6obcy
.report\t\t\tzgłoszenie aktualnego rozmówcy
.topic\t\t\twylosowanie tematu rozmowy
.exit\t\t\tzamyka aplikację
[*] Polecenia dodatkowe
.impersonate\t\tnawiązuje połączenie przez zaufany losowy serwer pośredniczący
.reconnect\t\tnawiązuje ponownie połączenie bezpośrednie
.obfuscate\t\twłącza/wyłącza obfuskację wyrazów metodą homoglifów
.debug\t\t\twyświetla dane techniczne''')

    def emptyline(self) -> None:
        """
        Inherited command from Cmd object
        Prevend sending the same message few times
        """
        pass
