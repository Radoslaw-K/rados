#! /usr/bin/python

PLATFORM =  "rpi"


import sys
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import subprocess
import time
import json

if PLATFORM == "rpi":
    import RPi.GPIO as GPIO
    from picamera import PiCamera

    from signboard_Rversion import signboard

    #Global Camera Object
    camera = PiCamera()
    camera.resolution = (300, 300)
    camera.framerate = 30

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    signboard = signboard()


#Public list of clients
clients = []
#http_users = {"users" : 0 } 
#http_clients = []
users = 0


#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
)

# class JSON_Handler(tornado.web.RequestHandler):
   # def get(self):
       # for c in http_clients:
       #     c.write(json.dumps(http_users))
       # print "JSON Handler activated"


class DownloadHandler(tornado.web.RequestHandler):
  def get(self):
	print "[HTTP](DownloadHandler) User requests to download a file."
	file_name = "file.example"
	buf_size = 4096
	self.set_header('Content-Type', 'application/octet-stream')
	self.set_header('Content-Disposition', 'attachment; filename=' + file_name)
	with open(file_name, 'r') as f:
		while True:
			data = f.read(buf_size)
			if not data:
				break
			self.write(data)
	self.finish()
	
	
class MainHandler(tornado.web.RequestHandler):
  def get(self):
   # http_clients.append(self)
     print "[HTTP](MainHandler) User Connected."
   # http_users["users"] = http_users["users"] + 1
     print "total users =", users
     self.render("index.html")

  def post(self):
	print "[HTTP](MainHandler) POST Request"
	file1 = self.request.files['file1'][0]
	original_fname = file1['filename']

	output_file = open("uploads/" + original_fname, 'wb')
	output_file.write(file1['body'])

	self.finish("file " + original_fname + " is uploaded")

	
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print '[WS] Connection was opened.'
    self.write_message("{Welcome to my websocket!")
    clients.append(self)
    global users
    users += 1
 
  def on_message(self, message):
    print '[WS] Incoming message:', message
    self.write_message("{You said: " + message)
    if message == "on_g":
      GPIO.output(16, True)
    if message == "off_g":
      GPIO.output(16, False)
    if message == "on_r":
      GPIO.output(18, True)
    if message == "off_r":
      GPIO.output(18, False)
    if message[0:5] == "sbrd_":
      signboard.display_message(message[5:])

  def on_close(self):
    print '[WS] Connection was closed.'
    clients.remove(self)
    global users
    users -= 1
 
application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  (r'/downloads', DownloadHandler),
 # (r'/json', JSON_Handler),

], **settings)


class ContentHandler():
  def PI_temp(self):
    for c in clients:
      p = subprocess.Popen(["/opt/vc/bin/vcgencmd" , "measure_temp"],
                           stdout=subprocess.PIPE)
      (output, err) = p.communicate()
      print "[WS](ContentHandler) Sending temperature : ",output
      c.write_message("{"+output)

  def img(self):
	#print "[WS](ContentHandler) Video stream running..."
	print "Video stream running..."
	frames = 1
	camera.capture_sequence(['/home/pi/Desktop/TornadoIO_Websockets/image_buff/image%02d.jpg' % i for i in range(frames)], use_video_port=True)

	for i in range(frames):
		filename = '/home/pi/Desktop/TornadoIO_Websockets/image_buff/image%02d.jpg' % i
		with open( filename, "rb") as f:
			data = f.read()
			for c in clients:
				c.write_message(data.encode("base64"))      
				f.close()

  def users_connected(self):
    for c in clients:
        global users
        c.write_message("{"+ "users " + str(users)) 

 
if __name__ == "__main__":
  try:

    http_server = tornado.httpserver.HTTPServer(application)

    if PLATFORM == "rpi":
        http_server.listen(80)
    else:
        http_server.listen(8000)

    main_loop = tornado.ioloop.IOLoop.instance()


    if PLATFORM == "rpi":
        test = ContentHandler()
        temp_loop = tornado.ioloop.PeriodicCallback(test.PI_temp,
                                                    2000,
                                                    io_loop = main_loop)
        provider_loop = tornado.ioloop.PeriodicCallback(test.img,
                                                    250,
                                                    io_loop = main_loop)
        user_count_loop = tornado.ioloop.PeriodicCallback(test.users_connected, 1000, io_loop = main_loop)
        provider_loop.start()
        temp_loop.start()
        user_count_loop.start()

    print "Tornado started"
    main_loop.start()

  except:
    print "-----Exception triggered-----"

    if PLATFORM == "rpi":
        GPIO.cleanup()
        camera.close()
        signboard.close_serial()







  #End of Program
