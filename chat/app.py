import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpclient
import urllib
import json

DJANGO_PORT = os.getenv("DJANGO_PORT", 8000)
DJANGO_HOST = os.getenv("DJANGO_HOST", "0.0.0.0")
TORNADO_PORT = os.getenv("TORNADO_PORT", 8888)
TORNADO_HOST = os.getenv("TORNADO_HOST", "0.0.0.0")

my_connections = dict()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws/(?P<sender_id>\d+)&(?P<username>\w+)&(?P<token>\w+)/', WebSocketHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    http_client = tornado.httpclient.AsyncHTTPClient()

    def check_origin(self, origin):
        return True

    def open(self, sender_id=0, username="system", token=None):
        my_connections[sender_id] = {
            'socket': self,
            'username': username,
            'token': token
        }
        online = list()
        for key, value in my_connections.iteritems():
            online.append({'id': key, 'username': value['username']})
        for key, value in my_connections.iteritems():
            my_connections[key]['socket'].write_message({'online': online, 'name': 'system', 'text': 'connection complete'})

    def on_close(self):
        for key, value in my_connections.iteritems():
            if value['socket'] == self:
                my_connections.pop(key)
                break
        online = list()
        for key, value in my_connections.iteritems():
            online.append({'id': key, 'username': value['username']})
        for key, value in my_connections.iteritems():
            my_connections[key]['socket'].write_message({'online': online, 'name': 'system', 'text': 'disconnect'})

    def on_message(self, data):
        data = json.loads(data)
        post_data = {
            'sender': data['sender_id'],
            'receiver': data['receiver_id'],
            'text': data['text']
        }
        # curl -X POST -H "Content-Type: application/json" -H 'Authorization: Token 9bbf74d9b6372b55adda17670109ec76f3fcd5a9' -d '{"sender":"7", "receiver":"7", "text":"bwahaha"}' 127.0.0.1:8000/rest/messages/

        # body = urllib.urlencode(post_data) #Make it into a post request
        self.http_client.fetch(
            'http://%s:%s/rest/messages/' % (str(DJANGO_HOST), str(DJANGO_PORT)),
            # "http://0.0.0.0:"+str(DJANGO_PORT)+"/rest/messages/",
            method='POST',
            headers={
                'Authorization': 'Token '+my_connections[str(data['sender_id'])]['token'],
                'Content-Type': 'application/json',
                },
            body=json.dumps(post_data)
        )

        self.send_messages(data)

    def send_messages(self, data):
        for key, value in my_connections.iteritems():
            if data["sender_id"] == int(key):
                data["sender"] = value["username"]
            if data["receiver_id"] == int(key):
                data["receiver"] = value["username"]

        for key, value in my_connections.iteritems():
            if (data["sender_id"] == int(key)) or (data["receiver_id"] == int(key)):
                my_connections[key]['socket'].write_message(data)


def main():
    app = Application()
    app.listen(TORNADO_PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()