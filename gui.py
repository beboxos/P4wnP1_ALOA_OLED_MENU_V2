# -*- coding:utf-8 -*-
#imports
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib
from luma.oled.device import sh1106
import RPi.GPIO as GPIO
import datetime
import time
import subprocess
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import base64
# Load default font.
font = ImageFont.load_default()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
line1 = top
line2 = top+8
line3 = top+16
line4 = top+25
line5 = top+34
line6 = top+43
line7 = top+52
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
RST = 25
CS = 8		
DC = 24
USER_I2C = 0
#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16
#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
screensaver = 0
#SPI
serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)
device = sh1106(serial, rotate=2) #sh1106  
def DisplayText(l1,l2,l3,l4,l5,l6,l7):
	# simple routine to display 7 lines of text
	with canvas(device) as draw:
		draw.text((0, line1), l1,  font=font, fill=255)
		draw.text((0, line2), l2, font=font, fill=255)
		draw.text((0, line3), l3,  font=font, fill=255)
		draw.text((0, line4), l4,  font=font, fill=255)
		draw.text((0, line5), l5, font=font, fill=255)
		draw.text((0, line6), l6, font=font, fill=255)
		draw.text((0, line7), l7, font=font, fill=255)	

#vars
def switch_menu(argument):
    switcher = {
		0: "_  P4wnP1 A.L.O.A",
        1: "_SYSTEM COMMANDS",
        2: "_HID ATTACKS",
        3: "_WIFI SETTINGS",
        4: "_TRIGGERS FEATURES",
        5: "_TEMPLATES FEATURES",
        6: "_USB FEATURES",
        7: "_July",
        8: "_August",
        9: "_September",
        10: "_October",
        11: "_November",
        12: "_December",
		13: "_END"
    }
    return switcher.get(argument, "Invalid")
#menuprincipal = ['  .:: P4wnP1 A.L.O.A ::. ',' SYSTEM COMMANDS',' HID ATTACKS',' WIFI SETTINGS',' TRIGGERS FEATURES',' TEMPLATES FEATURES',' USB FEATURES']
curseur = 1
page=0	
menu = 1
ligne = ["","","","","","","",""]
while 1:
	if GPIO.input(KEY_UP_PIN): # button is released
		#draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
		menu = 1
	else: # button is pressed:
		#draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
		curseur = curseur -1
		if curseur<1:
			curseur = 1		

	if GPIO.input(KEY_LEFT_PIN): # button is released
		#draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
		menu = 1
	else: # button is pressed:
		#draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
		page = page - 7
		if page<0 :
			page = 0	
	if GPIO.input(KEY_RIGHT_PIN): # button is released
		#draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
		menu = 1
	else: # button is pressed:
		#draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
		page = page +7
		if page >7:
			page = 7
	if GPIO.input(KEY_DOWN_PIN): # button is released
		#draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
		menu = 1
	else: # button is pressed:
		#draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
		curseur = curseur + 1
		if curseur>7:
			curseur = 7
	#if GPIO.input(KEY_PRESS_PIN): # button is released
		#draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
	#else: # button is pressed:
		#draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled

	#if GPIO.input(KEY1_PIN): # button is released
		#draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
	#else: # button is pressed:
		#draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled

	#if GPIO.input(KEY2_PIN): # button is released
		#draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
	#else: # button is pressed:
		#draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
		
	#if GPIO.input(KEY3_PIN): # button is released
		#draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
	#else: # button is pressed:
		#draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
	#-----------
	ligne[1]=switch_menu(page)
	ligne[2]=switch_menu(page+1)
	ligne[3]=switch_menu(page+2)
	ligne[4]=switch_menu(page+3)
	ligne[5]=switch_menu(page+4)
	ligne[6]=switch_menu(page+5)
	ligne[7]=switch_menu(page+6)
	for n in range(1,8):
		if page+curseur == page+n:
			ligne[n] = ligne[n].replace("_",">")
		else:
			ligne[n] = ligne[n].replace("_"," ")
	DisplayText(ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7])
	#console debugger
	print(page+curseur)
	time.sleep(0.1)
GPIO.cleanup()
