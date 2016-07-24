import os.path
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpclient
import urllib
import json
# import tornado.auth
# import tornado.gen
my_connections = dict()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r'/', ChatHandler),
            # (r'/ws', WebSocketHandler),
            (r'/ws/(?P<sender_id>\d+)&(?P<username>\w+)/', WebSocketHandler),
        ]
        # settings = dict(
        #     # cookie_secret="your_cookie_secret",
        #     template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        #     static_path=os.path.join(os.path.dirname(__file__), 'static'),
        #     # xsrf_cookies=True,
        #     # debug=True,
        # )
        tornado.web.Application.__init__(self, handlers)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    http_client = tornado.httpclient.AsyncHTTPClient()
    # connections = set()

    def check_origin(self, origin):
        return True

    def open(self, sender_id=0, username="system"):
        my_connections[sender_id] = {
            'socket': self,
            'username': username
        }
        # WebSocketHandler.connections.add(self)
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
        body = urllib.urlencode(post_data) #Make it into a post request
        self.http_client.fetch(
            "http://localhost:8000/rest/messages/",
            method='POST',
            auth_username='admin',
            auth_password='v12341234',
            headers=None,
            body=body
        )
        # url = "http://localhost:8000/rest/messages/"
        # tornado.requests.post(url, data={'sender':1, 'receiver':2, 'text':'curlyk'},auth=('anmekin','nicetry'))

        self.send_messages(data)
        # WebSocketHandler.conn[data['sender_id']].send_message(data['msg'])

    def send_messages(self, data):
        for key, value in my_connections.iteritems():
            if data["sender_id"] == int(key):
                data["sender"] = value["username"]
            if data["receiver_id"] == int(key):
                data["receiver"] = value["username"]

        for key, value in my_connections.iteritems():
            # print(key, value)
            if (data["sender_id"] == int(key)) or (data["receiver_id"] == int(key)):
                my_connections[key]['socket'].write_message(data)

        # for conn in my_connections:
        #     conn.write_message({'name': self.current_user, 'msg': json.dumps(msg)})


def main():
    # port = int(os.environ.get("PORT", 8888))
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()