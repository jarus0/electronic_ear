
import RPi.GPIO as GPIO
import time
import picamera
import requests
import pyttsx3

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

def image_to_sound():
	print ('in function')

	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top), "identification starts",  font=font, fill=255)
	draw.text((x, top+8), "initializing server",  font=font, fill=255)
	draw.text((x, top+16), "connection",  font=font, fill=255)
	draw.text((x, top+25), "------------",  font=font, fill=255)
	disp.image(image)
	disp.display()

	image_path = 'captured.jpg'
	api_key = 'acc_e15bbd9253e0d4d'
	api_secret = 'e684959c19ae4ba53ddcb758b3e89035'
	print('image uploading')
	response = requests.post('https://api.imagga.com/v2/uploads',auth=(api_key, api_secret),files={'image': open(image_path, 'rb')})
	replyJson = response.json()
	key_uploadID = replyJson['result']['upload_id']
	print('image identifying')

 	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top), "image",  font=font, fill=255)
	draw.text((x, top+8), "identifying",  font=font, fill=255)
	draw.text((x, top+16), "started",  font=font, fill=255)
	draw.text((x, top+25), "------------",  font=font, fill=255)
	disp.image(image)
	disp.display()

	response = requests.get('https://api.imagga.com/v2/tags?image_upload_id=%s' % key_uploadID, auth=(api_key, api_secret))
	replyJson = response.json()
	nameList = replyJson['result']['tags']
	name1 = nameList[0]['tag']['en']
	name2 = nameList[1]['tag']['en']
	name3 = nameList[2]['tag']['en']
	print('image deleteing from server')


 	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top), "image",  font=font, fill=255)
	draw.text((x, top+8), "deleting",  font=font, fill=255)
	draw.text((x, top+16), "from",  font=font, fill=255)
	draw.text((x, top+25), "server",  font=font, fill=255)
	disp.image(image)
	disp.display()

	response = requests.delete('https://api.imagga.com/v2/uploads/%s' % (key_uploadID),auth=(api_key, api_secret))
 	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top), "object look like:-",  font=font, fill=255)
	draw.text((x, top+8), name1,  font=font, fill=255)
	draw.text((x, top+16), name2,  font=font, fill=255)
	draw.text((x, top+25), name3,  font=font, fill=255)
	disp.image(image)
	disp.display()

	#engine.setProperty('rate', 100)
	#engine.setProperty('voice', voices[1].id)
	engine.say("object name " + name1 + " or " + name2)
	engine.runAndWait()
	engine.say("object name " + name1 + " or " + name2)
	engine.runAndWait()
	engine.say("object name " + name1 + " or " + name2)
	engine.runAndWait()
	engine.stop()
	print (name1)
	print (name2)




RST = None     # on the PiOLED this pin isnt used
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()

engine = pyttsx3.init()
butPin = 4
irSen = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(irSen, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while 1:
	if GPIO.input(butPin):
		print ('high')
		if not GPIO.input(irSen):
			print("button got")
			engine.say("obstacle detect in front of user")
			engine.runAndWait()
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell = True )
		cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell = True )
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell = True )
		cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell = True )
		draw.text((x, top),       "IP- " + str(IP),  font=font, fill=255)
		draw.text((x, top+8),     str(CPU), font=font, fill=255)
		draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
		draw.text((x, top+25),    str(Disk),  font=font, fill=255)
		disp.image(image)
		disp.display()
	else :
		disp.clear()
		print ('capturing image')
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		#draw.text((x, top), "identification starts",  font=font, fill=255)
		draw.text((x, top+8), "        image ",  font=font, fill=255)
		draw.text((x, top+16), "        capturing",  font=font, fill=255)
		#draw.text((x, top+25), "------------",  font=font, fill=255)
		disp.image(image)
		disp.display()
		with picamera.PiCamera() as camera:
			camera.resolution = (1024, 768)
			time.sleep(2)
			camera.capture('captured.jpg')
			image_to_sound()
	time.sleep(0.075)
