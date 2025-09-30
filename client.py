import socket
import threading
import sys
import argparse



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
        mySocket.send(bytes(f"<{username} joined>", "UTF-8"))
    except:
        print("failed")
        return

    while True:
        text = input("> ")
        #handle special input here
        msg = f"<{username}> " + text

        mySocket.send(bytes(msg, "UTF-8"))

        






if __name__ == "__main__":
    main()