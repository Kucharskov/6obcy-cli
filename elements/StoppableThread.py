#!/usr/bin/env python3

from threading import Thread, Event


class StoppableThread(Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = Event()

    def stop(self) -> None:
        """ Method to stop thread """

        self._stop_event.set()

    def stopped(self) -> bool:
        """
        Getter for checking if thread should stop
        Usage:
        while self.stopped():
            do_stuff()
        """

        return self._stop_event.is_set()
