#!/usr/bin/env python3

from elements.StoppableThread import *
from elements.ConnectionHandler import *
from elements.DataHandler import *


class Receiver(StoppableThread):

    def __init__(self, connection, dataHandler) -> None:
        super(Receiver, self).__init__()
        self.connection = connection
        self.dataHandler = dataHandler

    def run(self) -> None:
        """ Main thread to receive all data and pass it into data handler """

        while not self.stopped():
            try:
                data = self.connection.readData()

                if data is not None:
                    self.dataHandler.handle(data)
            except:
                pass
