import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ClientHandler(tornado.web.RequestHandler):
    def get(self, event):
        self.write(event)


def makeApp():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/(\w+)', ClientHandler)
    ])


if __name__ == "__main__":
    application = makeApp()
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
