import sys
import time
import serial
import picamera
import logbook
import zmq
from PIL import Image, ImageStat

# Server related constants.
DEFAULT_SERVER_IP = '127.0.0.1'
DEFAULT_SERVER_PORT = '5556'
STOP_MESSAGE = 'STOP'
OK_REPLY = 'OK'
COLORS_DELIMITER = ','

SLEEP_PERIOD = 0.2

log = logbook.Logger('Color2Pi')


def main():
	"""
	Picks up the dominant color from the camera and sends it to the web server.
	Usage: color2pi.py [SERVER_IP] [SERVER_PORT]
	"""
	# Validate input parameters.
	server_ip = DEFAULT_SERVER_IP
	port = DEFAULT_SERVER_PORT
	if len(sys.argv) > 1:
		server_ip =  sys.argv[1]
	if len(sys.argv) > 2:
		port =  sys.argv[2]
	server_address = '{0}:{1}'.format(server_ip, port)
	# Connect to the server.
	context = zmq.Context()
	log.info('Connecting to server ({0})...'.format(server_address))
	socket = context.socket(zmq.REQ)
	socket.connect ('tcp://{0}'.format(server_address))
	# Set up serial port.
	ser = serial.Serial('/dev/ttyAMA0',9600)
	# Start working!
	try:
		while True:
			with picamera.PiCamera() as camera:
				sleep(SLEEP_PERIOD)
				camera.resolution = (80, 60)
				camera.brightness = 50
				camera.saturation = 90
				camera.capture('image.png', resize=(30, 20))

			# All this would be better than using a stream.
			im = Image.open('image.png')
			left = 10
			top = 7
			im2 = im.crop((left, top, left + 5, top + 5))
			avg = ImageStat.Stat(im2).median
			r, g, b, s = avg
			message = '{0}{1}{2}{3}{4}'.format(r, COLORS_DELIMITER, g, COLORS_DELIMITER, b)
			log.info('Colors are: {0}'.format(message))
			# Send to server.
			socket.send(message)
			# Get the reply.
			message = socket.recv()
			if message != OK_REPLY:
				log.info('Got an unknown message: {0}. Stopping...'.format(message))
				socket.send(STOP_MESSAGE)
				break
			# Send to serial.
			ser.write(message + '\n')
	except KeyboardInterrupt:
		try:
			# Tell the server to stop as well.
			socket.send(STOP_MESSAGE)
		except zmq.core.error.ZMQError:
			# Wrong state, we have to receive the OK message first.
			socket.recv()
			socket.send(STOP_MESSAGE)
	

if __name__ == '__main__':
	main()