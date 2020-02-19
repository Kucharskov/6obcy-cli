#!/usr/bin/env python3

from elements.StoppableThread import *
from elements.ConnectionHandler import *
from time import sleep


class Heartbeat(StoppableThread):

    def __init__(self, connHandler) -> None:
        super(Heartbeat, self).__init__()
        self.connHandler = connHandler
        self.timeOut = 30

    def setTimeout(self, timeOut: int) -> None:
        """ Timeout setter """

        self.timeOut = int(timeOut / 1000)

    def run(self) -> None:
        """ Regarding to reversed protocol - heartbeat thread which keeps connection  """

        while not self.stopped():
            try:
                self.connHandler.writeRawData("2")
                for _ in range(0, self.timeOut, 1):
                    if self.stopped():
                        return
                    sleep(1)
            except:
                pass
