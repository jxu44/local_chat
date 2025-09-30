import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-passcode', '--passcode') 
    parser.add_argument('-port', "--port")
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

    print(args)






if __name__ == "__main__":
    main()