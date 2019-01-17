# -*- coding:utf-8 -*-
#imports 
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
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
GPIO.setwarnings(False)
#P4wnP1 essential const
hidpath = "/usr/local/P4wnP1/HIDScripts/"
sshpath = ":/usr/local/P4wnP1/scripts/"

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
brightness = 255 #Max
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
        1: "_SYSTEM RELATED",
        2: "_HID SCRIPTS",
        3: "_WIFI THINGS",
        4: "_TRIGGERS FEATURES",
        5: "_TEMPLATES FEATURES",
        6: "_USB THINGS",
        7: "_System information",
        8: "_OLED brightness",
        9: "_",
        10: "_Display OFF",
        11: "_Keys Test",
        12: "_Reboot GUI",
        13: "_System shutdown",
        14: "_RUN HID script",
        15: "_GAMEPAD",
        16: "_MOUSE",
        17: "_Typing Speed",
        18: "_",
        19: "_",
        20: "_",        
        21: "_WIFI settings",
        22: "_",
        23: "_",
        24: "_",
        25: "_",
        26: "_",
        27: "_",
        28: "_Trigger features",
        29: "_",
        30: "_",
        31: "_",
        32: "_",
        33: "_",
        34: "_",
        35: "_FULL SETTINGS",
        36: "_BLUETOOTH",
        37: "_USB",
        38: "_WIFI",
        39: "_TRIGGER ACTIONS",
        40: "_NETWORK",
        41: "_",
        42: "_USB features",
        43: "_",
        44: "_",
        45: "_",
        46: "_",
        47: "_",
        48: "_"         
}
    return switcher.get(argument, "Invalid")
def about():
    # simple sub routine to show an About
    DisplayText(
        "  : P4wnP1 A.L.O.A :",
        "P4wnP1 (c) @Mame82",
        "",
        "This GUI is developed",
        "       by BeBoX",
        "contact :",
        "depanet@gmail.com"
        )
    while GPIO.input(KEY_LEFT_PIN):
        #wait
        menu = 1
    page = 0
#system information sub routine
def sysinfos():
    while GPIO.input(KEY_LEFT_PIN):
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        today_date = now.strftime("%d %b %y")
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "hostname -I"
        IP2 = subprocess.check_output(cmd, shell = True ).split(" ")[1]
        IP3 = subprocess.check_output(cmd, shell = True ).split(" ")[2]
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )   
        DisplayText(
            "WIFI: " + str(IP),
            str(CPU),
            str(MemUsage),
            str(Disk),
            "BTH.: " + str(IP3),
            "USB.: " + str(IP2),
            today_date + " " + today_time
            )
    #page = 7
def OLEDContrast(contrast):
    #set contrast 0 to 255
    while GPIO.input(KEY_LEFT_PIN):
        #loop until press left to quit
        with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # button is released
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
            else: # button is pressed:
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                    contrast = contrast +5
                    if contrast>255:
                        contrast = 255

            if GPIO.input(KEY_DOWN_PIN): # button is released
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
            else: # button is pressed:
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                    contrast = contrast-5
                    if contrast<0:
                        contrast = 0
            device.contrast(contrast)
            draw.text((54, line4), "Value : " + str(contrast),  font=font, fill=255)
    return(contrast)
def splash():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'bootwhat.bmp'))
    splash = Image.open(img_path) \
        .transform((device.width, device.height), Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR) \
        .convert(device.mode)
    device.display(splash)
    time.sleep(5) #5 sec splash boot screen
def SreenOFF():
    #put screen off until press left
    while GPIO.input(KEY_LEFT_PIN):
        device.hide()
    device.show()
def KeyTest():
    while GPIO.input(KEY_LEFT_PIN):
        with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # button is released
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
            else: # button is pressed:
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled

            if GPIO.input(KEY_LEFT_PIN): # button is released
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
            else: # button is pressed:
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled

            if GPIO.input(KEY_RIGHT_PIN): # button is released
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
            else: # button is pressed:
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled

            if GPIO.input(KEY_DOWN_PIN): # button is released
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
            else: # button is pressed:
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled

            if GPIO.input(KEY_PRESS_PIN): # button is released
                    draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
            else: # button is pressed:
                    draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled

            if GPIO.input(KEY1_PIN): # button is released
                    draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
            else: # button is pressed:
                    draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled

            if GPIO.input(KEY2_PIN): # button is released
                    draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
            else: # button is pressed:
                    draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                    
            if GPIO.input(KEY3_PIN): # button is released
                    draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
            else: # button is pressed:
                    draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
def FileSelect(path,ext):
    cmd = "ls -F --format=single-column  " + path + "*" + ext
    listattack=subprocess.check_output(cmd, shell = True )
    listattack=listattack.replace(ext,"")
    listattack=listattack.replace(path,"")
    listattack=listattack.replace("*","")
    listattack=listattack.split("\n")
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    ligne[n] = listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]+ext
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")
def templateSelect(liste):
    # GetTemplateList("BLUETOOTH").split("\n")
    fichier = GetTemplateList(liste).split("\n")
    maxi = len(fichier)
    cur=1
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=1
        if maxi < 8:
            for n in range(1,8):
                if n<maxi:
                    if n == cur:
                        ligne[n-1] = ">"+fichier[n]
                    else:
                        ligne[n-1] = " "+fichier[n]
                else:
                    ligne[n-1] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<1:
                cur = 1
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = fichier[cur]
            return(retour)    
        # ----------
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
def runhid():
    #choose and run (or not) a script
    fichier = FileSelect(hidpath,".js")
    time.sleep(0.5)
    if  fichier == "":
        return()
    while GPIO.input(KEY_LEFT_PIN):
        answer = 0
        while answer == 0:
            DisplayText(
                "                 YES",
                "",
                "",
                fichier,
                "",
                "",
                "                  NO"
                )
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
        if answer == 2:
            return()
        time.sleep(0.5) #pause 
        answer = 0
        while answer ==0:
            DisplayText(
                "   Run Background job",
                "",
                "",
                "Method ?       CANCEL",
                "",
                "",
                "       Run direct job"
                )
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY2_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2  
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 3
        if answer == 2:
            return()
        DisplayText(
    "",
    "",
    "",
    "HID Script running...",
    "",
    "",
    ""
    )
        if answer == 1:
            # run as background job P4wnP1_cli hid job command
            cmd = "P4wnP1_cli hid job '" + fichier+"'"
            result=subprocess.check_output(cmd, shell = True )
            return()
        if answer == 3:
            # run hid script directly
            cmd = "P4wnP1_cli hid run '" + fichier+"'"
            result=subprocess.check_output(cmd, shell = True )
            return()
def restart():
    cmd="python /root/BeBoXGui/runmenu.py &"
    exe = subprocess.check_output(cmd, shell = True )
    return()
def GetTemplateList(type):
    # get list of template
    # Possible types : FULL_SETTINGS , BLUETOOTH , USB , WIFI , TRIGGER_ACTIONS , NETWORK
    cmd = "P4wnP1_cli template list"
    list = subprocess.check_output(cmd, shell = True )
    list = list.replace("Templates of type ","") #remove unwanted text
    list = list.replace(" :","")
    list = list.replace("------------------------------------\n","")
    list = list.split("\n")
    result = ""
    found = 0
    for n in range(0,len(list)):
        if list[n] == type:
            found = 1
        if list[n] == "":
            found = 0
        if found == 1:
            result = result + list[n] + "\n"
    return(result)   
def ApplyTemplate(template,section):
    while GPIO.input(KEY_LEFT_PIN):
        answer = 0
        while answer == 0:
            DisplayText(
                "                 YES",
                "",
                "",
                template,
                "",
                "",
                "                  NO"
                )
            if GPIO.input(KEY1_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 1
            if GPIO.input(KEY3_PIN): # button is released
                menu = 1
            else: # button is pressed:
                answer = 2
        if answer == 2:
            return()
        time.sleep(0.5) #pause
        cmd = "P4wnP1_cli template deploy -" +section + " '"+ template+"'"
        exe = subprocess.check_output(cmd, shell = True )
        return()
def Gamepad():
    while GPIO.input(KEY_PRESS_PIN):
        with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # button is released
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
            else: # button is pressed:
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"UP\")'", shell = True )

            if GPIO.input(KEY_LEFT_PIN): # button is released
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
            else: # button is pressed:
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"LEFT\")'", shell = True )

            if GPIO.input(KEY_RIGHT_PIN): # button is released
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
            else: # button is pressed:
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"RIGHT\")'", shell = True )

            if GPIO.input(KEY_DOWN_PIN): # button is released
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
            else: # button is pressed:
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"DOWN\")'", shell = True )

            #if GPIO.input(KEY_PRESS_PIN): # button is released
            #        draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
            #else: # button is pressed:
            #        draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled
            #        exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"ENTER\")'", shell = True )

            if GPIO.input(KEY1_PIN): # button is released
                    draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
            else: # button is pressed:
                    draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"Q\")'", shell = True )

            if GPIO.input(KEY2_PIN): # button is released
                    draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
            else: # button is pressed:
                    draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"W\")'", shell = True )
                    
            if GPIO.input(KEY3_PIN): # button is released
                    draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
            else: # button is pressed:
                    draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'press(\"E\")'", shell = True )
def Mouse():
    bouton1 = 0
    bouton2 = 0
    step = 10
    time.sleep(0.5)
    while GPIO.input(KEY2_PIN):
        with canvas(device) as draw:
            if GPIO.input(KEY_UP_PIN): # button is released
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
            else: # button is pressed:
                    draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(0,-"+str(step)+")'", shell = True )

            if GPIO.input(KEY_LEFT_PIN): # button is released
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
            else: # button is pressed:
                    draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(-"+str(step)+",0)'", shell = True )

            if GPIO.input(KEY_RIGHT_PIN): # button is released
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
            else: # button is pressed:
                    draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped("+str(step)+",0)'", shell = True )

            if GPIO.input(KEY_DOWN_PIN): # button is released
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
            else: # button is pressed:
                    draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                    exe = subprocess.check_output("P4wnP1_cli hid run -c 'moveStepped(0,"+str(step)+")'", shell = True )

            if GPIO.input(KEY_PRESS_PIN): # button is released
                    draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
            else: # button is pressed:
                    draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled
                    if step == 10:
                        #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT1)'", shell = True )
                        step = 100
                        time.sleep(0.2)
                    else:
                        #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                        step = 10
                        time.sleep(0.2)

            if GPIO.input(KEY1_PIN): # button is released
                    draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                    #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
            else: # button is pressed:
                    draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled
                    if bouton1 == 0:
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT1)'", shell = True )
                        bouton1 = 1
                        time.sleep(0.2)
                    else:
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                        bouton1 = 0
                        time.sleep(0.2)
            #if GPIO.input(KEY2_PIN): # button is released
            #        draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
            #else: # button is pressed:
            #        draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
            draw.text((64, line4), "Key2 : Exit",  font=font, fill=255)        
            if GPIO.input(KEY3_PIN): # button is released
                    draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                    #exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
            else: # button is pressed:
                    draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
                    if bouton2 == 0:
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BT2)'", shell = True )
                        bouton2 = 1
                        time.sleep(0.2)
                    else:
                        exe = subprocess.check_output("P4wnP1_cli hid run -c 'button(BTNONE)'", shell = True )
                        bouton2 = 0
                        time.sleep(0.2)
            #time.sleep(0.1)
#init vars 
curseur = 1
page=0  
menu = 1
ligne = ["","","","","","","",""]
selection = 0
splash()
#print("selected : " + FileSelect(hidpath,".js"))
while 1:
    if GPIO.input(KEY_UP_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur -1
        if curseur<1:
            curseur = 7     
    if GPIO.input(KEY_LEFT_PIN): # button is released
        menu = 1
    else: # button is pressed:
                # back to main menu on Page 0
        page = 0    
    if GPIO.input(KEY_RIGHT_PIN): # button is released
        menu = 1
    else: # button is pressed:
        selection = 1
    if GPIO.input(KEY_DOWN_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur + 1
        if curseur>7:
            curseur = 1
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
    if selection == 1:
        # une option du menu a ete validee on va calculer la page correspondante
            if page == 7:
                #system menu
                if curseur == 1:
                    sysinfos()
                if curseur == 2:
                    brightness = OLEDContrast(brightness)
                if curseur == 4:
                    SreenOFF()
                if curseur == 5:
                    KeyTest()
                if curseur == 6:
                    restart()
                if curseur == 7:
                    exit()
            if page == 14:
                #HID related menu
                if curseur == 1:
                    #run hid script
                    runhid()
                if curseur == 2:
                    #gamepad
                    Gamepad()
                if curseur == 3:
                    #mouse
                    Mouse()
            if page == 35:
                #template section menu
                if curseur == 1:
                    #FULL_SETTINGS
                    template = templateSelect("FULL_SETTINGS")
                    if template!="":
                        ApplyTemplate(template,"f")
                if curseur == 2:
                    #BLUETOOTH
                    template = templateSelect("BLUETOOTH")
                    if template!="":
                        ApplyTemplate(template,"b")
                if curseur == 3:
                    #USB
                    template = templateSelect("USB")
                    if template!="":
                        ApplyTemplate(template,"u")
                if curseur == 4:
                    #WIFI
                    template = templateSelect("WIFI")
                    if template!="":
                        ApplyTemplate(template,"w")
                if curseur == 5:
                    #TRIGGER_ACTIONS
                    template = templateSelect("TRIGGER_ACTIONS")
                    if template!="":
                        ApplyTemplate(template,"t")
                if curseur == 6:
                    #NETWORK
                    template = templateSelect("NETWORK")
                    if template!="":
                        ApplyTemplate(template,"n")
            if page == 0:
            #we are in main menu
                if curseur == 1:
                    # call about
                    about()
                if curseur == 2:
                    #system menu 
                    page = 7
                    curseur = 1
                if curseur == 3:
                #hid attacks menu
                    page = 14
                    curseur = 1
                if curseur == 4:
                    page = 21
                    curseur = 1
                if curseur == 5:
                    page = 28
                    curseur = 1
                if curseur == 6:
                    page = 35
                    curseur = 1
                if curseur == 7:
                    page = 42
                    curseur = 1
                print(page+curseur)
    ligne[1]=switch_menu(page)
    ligne[2]=switch_menu(page+1)
    ligne[3]=switch_menu(page+2)
    ligne[4]=switch_menu(page+3)
    ligne[5]=switch_menu(page+4)
    ligne[6]=switch_menu(page+5)
    ligne[7]=switch_menu(page+6)
    #add curser on front on current selected line
    for n in range(1,8):
        if page+curseur == page+n:
            ligne[n] = ligne[n].replace("_",">")
        else:
            ligne[n] = ligne[n].replace("_"," ")
    DisplayText(ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7])
    #print(page+curseur) #debug trace menu value
    time.sleep(0.1)
    selection = 0
GPIO.cleanup()
