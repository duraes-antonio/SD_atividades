import tornado.ioloop
from tornado import websocket

SIMB_ACAO = "-->"


class EchoWebSocket(websocket.WebSocketHandler):

	def check_origin(self, origin):
		return True

	def open(self):
		print(f"{SIMB_ACAO} Websocket aberto!\n")

	def on_message(self, message):
		self.write_message(u"%s" % message.upper())

	def on_close(self):
		print(f"{SIMB_ACAO} Websocket finalizado!\n")


application = tornado.web.Application([(r"/", EchoWebSocket), ])

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.instance().start()
