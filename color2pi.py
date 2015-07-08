
from PIL import Image, ImageStat

import picamera 
import serial
from time import sleep

ser=serial.Serial('/dev/ttyAMA0',9600)
newline='\n'



while 1:
	with picamera.PiCamera() as camera:
		sleep(0.2)
		
		camera.resolution = (80,60)
		camera.brightness=50
		camera.saturation=90
		#camera.start_preview()
		camera.capture('image.png',resize=(30,20))

	#all this would be beteer of using a stream
	im=Image.open('image.png')
	left=10
	top=7
	im2 = im.crop((left,top,left+5,top+5))
	im2.save("temp"+".png")
	avg =  ImageStat.Stat(im2).median
	print(avg)
	r,g,b,s=avg
	mesg=str(r)+','+str(g)+','+str(b)+newline
	ser.write(mesg)

