from channels.generic.websocket import WebsocketConsumer

class NotificacionesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    