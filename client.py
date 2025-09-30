import socket
import threading
import sys
import argparse


#threads for concurrent read/write
def write(mySocket, username, passcode, host, port):

    #send passcode first
    mySocket.send(bytes(passcode, 'utf-8'))

    #then username
    mySocket.send(bytes(username, 'utf-8'))

    print(f"Connected to {host} on port {port}")
    while True:
        text = input()
        #handle special input here
        if text in commands:
            pass

        mySocket.send(bytes(text, "UTF-8"))


def read(mySocket):
    while True:
        msg = mySocket.recv(1024)
        if not msg:
            print('server disconnected')
            return
        print(msg.decode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', "--port", type=int)
    parser.add_argument('-host', "--host")
    parser.add_argument('-username', '--username')
    parser.add_argument('-passcode', '--passcode') 
    args = parser.parse_args()

    if not args.port:
        print("Please provide a port.")
        return
    if not args.host:
        print("Please provide a host.")
        return
    if not args.username or len(args.username) > 8:
        print("Please provide a valid username.")
        return
    if not args.passcode or len(args.passcode) > 5:
        print("Please provide a valid passcode.")
        return


    host = args.host
    port =args.port
    username = args.username
    passcode = args.passcode

    print(host)

    mySocket = socket.socket()
    try:
        mySocket.connect((host, port))
    except:
        print("failed")
        return

    read_t = threading.Thread(target=read, args= [mySocket])

    write_t = threading.Thread(target=write, args=(mySocket, username, passcode, host, port))

    read_t.start()
    write_t.start()
        






if __name__ == "__main__":
    main()