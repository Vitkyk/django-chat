import os.path
# from tornado import websocket, web, ioloop

import tornado.ioloop
import tornado.web
import tornado.websocket
import urllib
# import tornado.auth
# import tornado.gen


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', ChatHandler),
            (r'/ws', WebSocketHandler),
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
        http_client = tornado.httpclient.AsyncHTTPClient()
        post_data = {'sender': 1, 'receiver': 1, 'text': msg} #A dictionary of your post data
        body = urllib.urlencode(post_data) #Make it into a post request
        http_client.fetch("http://localhost:8000/rest/messages/", method='POST', auth_username='admin', auth_password='v12341234', headers=None, body=body) #Send it off!
        # url = "http://localhost:8000/rest/messages/"
        # tornado.requests.post(url, data={'sender':1, 'receiver':2, 'text':'curlyk'},auth=('anmekin','nicetry'))
        self.send_messages(msg)

    def send_messages(self, msg):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg})


def main():
    # port = int(os.environ.get("PORT", 8888))
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()