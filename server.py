import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta


def run(client, address):
    while True:
        msg = client.recv(1024)
        if not msg:
            break

        #handle special input

        print(msg.decode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-passcode', '--passcode') 
    parser.add_argument('-port', "--port", type=int)
    args = parser.parse_args()

    if not args.port:
        print("Please provide a port.")
        return
    if not args.passcode or len(args.passcode) > 5:
        print("Please provide a valid passcode.")
        return

    passcode = args.passcode
    port = args.port


    

    mySocket = socket.socket()
    mySocket.bind(('127.0.0.1', port))
    mySocket.listen(5)
        
     
    while True:
        (client, address) = mySocket.accept()
        ct = threading.Thread(args=(client, address), target=run)
        ct.start()
        



if __name__ == "__main__":
    main()