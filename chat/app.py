import os.path
# from tornado import websocket, web, ioloop

import tornado.ioloop
import tornado.web
import tornado.websocket
# import tornado.auth
# import tornado.gen


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', ChatHandler),
            (r'/ws', WebSocketHandler),
            (r'/ws2', SocketHandler),
        ]
        settings = dict(
            # cookie_secret="your_cookie_secret",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            # xsrf_cookies=True,
            # debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass
    # def get_current_user(self):
    #     user = self.get_secure_cookie("username")
    #     if user:
    #         user = user.decode("utf-8")
    #     return user


class ChatHandler(BaseHandler):
    def get(self):
        self.render('index.html', user=self.current_user)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        # self.connections.write_message()
        WebSocketHandler.connections.add(self)

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):
        self.send_messages(msg)

    def send_messages(self, msg):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg})


cl = []


class SocketHandler(tornado.websocket.WebSocketHandler):
    # def check_origin(self, origin):
    #     return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)


def main():
    # port = int(os.environ.get("PORT", 8888))
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()