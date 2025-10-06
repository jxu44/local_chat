import socket
import threading
import sys
import argparse


#threads for concurrent read/write
def write(mySocket, username, passcode, host, port):

    #send passcode and username first
    mySocket.send(f"{passcode}%%%{username}".encode())




    print(f"Connected to {host} on port {port}")
    while True:
        text = input()
        mySocket.send(text.encode())


def read(mySocket):
    while True:
        msg = mySocket.recv(1024)
        if not msg:
            print('Disconnected from Server')
            sys.stdout.flush()
            return
        print(msg.decode())
        sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', action='store_true')
    parser.add_argument('-port', "--port", type=int)
    parser.add_argument('-host', "--host")
    parser.add_argument('-username', '--username')
    parser.add_argument('-passcode', '--passcode', type=str) 
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
        print("Incorrect passcode")
        return


    host = args.host
    port = args.port
    username = args.username
    passcode = args.passcode
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
        


    return



if __name__ == "__main__":
    main()