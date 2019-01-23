# P4wnP1_ALOA_OLED_MENU_V2
on the road P4wnP1 ALOA menu 

Installation instructions 
on boot partition edit config.txt to set I2C and SPI to active
in termnial you can type 
nano /boot/config.txt
find the section far away down and set : 
## i2c_arm
##     Enable the ARM's i2c interface
##
##     Default off.
##
dtparam=i2c_arm=on
dtparam=i2c1=on

and find and set spi section 
## spi
##     Set to "on" to enable the spi interfaces
##
##     Default off.
##
dtparam=spi=on

note : for the waveshare hat i used (and all gui.py is set like this) the inteface is SPI and not I2C
if you have a I2C oled edit gui.py file and set on line 72
USER_I2C = 1 #set to 1 if your oled is I2C

GPIO 8 keys are default waveshare hat

you can edit to set to your hat if different
#GPIO define
KEY_UP_PIN     = 6  #stick up
KEY_DOWN_PIN   = 19 #stick down
KEY_LEFT_PIN   = 5  #sitck left
KEY_RIGHT_PIN  = 26 #stick right
KEY_PRESS_PIN  = 13 #stick center button
KEY1_PIN       = 21 #key 1
KEY2_PIN       = 20 #key 2
KEY3_PIN       = 16 #key 3

Remember this menu is in alpha version, not all function are ready 
