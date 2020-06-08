import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import inotify.adapters
#
import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
#
# class Watcher:
#     DIRECTORY_TO_WATCH = "/server/o"
#
#     def __init__(self, callback):
#         self.observer = Observer()
#         self.callback = callback
#
#     def run(self):
#         event_handler = Handler(self.callback)
#         self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
#         self.observer.start()
#         try:
#             while True:
#                 time.sleep(5)
#         except:
#             self.observer.stop()
#             print("Error")
#
#         self.observer.join()
#
#
# class Handler(FileSystemEventHandler):
#     callback = None
#
#     def __init__(self, callback):
#         Handler.callback = callback
#
#     @staticmethod
#     def on_any_event(event):
#         if event.is_directory:
#             return None
#
#         elif event.event_type == 'created':
#             # Take any action here when a file is first created.
#             print("Received created event - %s." % event.src_path)
#
#         elif event.event_type == 'modified':
#             # Taken any action here when a file is modified.
#             f = open('/server/out', 'r')
#
#             for line in f:
#                 name = line.split(',')[0]
#
#
#             res = {"message": "msg"}
#             Handler.callback(res)
#             print ("Received modified event - %s." % event.src_path)


class ProgressConsumer(WebsocketConsumer):
    # def __new__(cls):
    #     i = inotify.adapters.Inotify()
    #     i.add_watch('/server/search')
    #
    #     with open('/server/search', 'w'):
    #         pass
    #
    #     for event in i.event_gen(yield_nones=False):
    #         (_, type_names, path, filename) = event
    #
    #         print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
    #               path, filename, type_names))

    def connect(self):
        print("CONNECTED")
        self.tracker_name = self.scope['url_route']['kwargs']['tracker_name']
        self.tracker_group_name = 'tracker_%s' % self.tracker_name



        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.tracker_group_name,
            self.channel_name
        )

        self.accept()


        # i = inotify.adapters.Inotify()
        # i.add_watch('/server/o')
        # FileWatcher("/server/o", self.progress_update)
        # for event in i.event_gen(yield_nones=False):
        #     (_, type_names, path, filename) = event
        #
        #     print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
        #           path, filename, type_names))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.tracker_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.tracker_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    def progress_update(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
