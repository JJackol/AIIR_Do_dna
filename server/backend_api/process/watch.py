import sys
import time
from watchdog.observers import Observer
import os
from watchdog.events import RegexMatchingEventHandler


class ImagesEventHandler(RegexMatchingEventHandler):
    FILE_REGEX = [r"/server/o$"]
    def __init__(self, callback):
        super().__init__(self.FILE_REGEX)
        self.callback = callback

    def on_modified(self, event):
        self.process(event)

    def process(self, event):
        print(event)
        self.callback()


class FileWatcher:
    def __init__(self, src_path, callback):
        self.__src_path = src_path
        self.__event_handler = ImagesEventHandler(callback)
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )

