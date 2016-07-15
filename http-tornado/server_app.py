#! /usr/bin/python

import tornado.ioloop
import tornado.web
import os.path
import time
import RPi.GPIO as GPIO



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")
		print "User Connected"
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(18, GPIO.OUT)

	def post(self):
		event = self.get_argument("voter")
		self.render("index.html")
		print "Event Happened: ", event
		if event == "on_g":
			GPIO.output(16, True)
		if event == "off_g":
			GPIO.output(16, False)
		if event == "on_r":
			GPIO.output(18, True)
		if event == "off_r":
			GPIO.output(18, False)		

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static")
)

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
		], **settings)

if __name__ == "__main__":
	app = make_app()
	app.listen(80)
	tornado.ioloop.IOLoop.instance().start()
	GPIO.cleanup()


