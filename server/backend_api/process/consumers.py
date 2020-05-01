import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ProgressConsumer(WebsocketConsumer):
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