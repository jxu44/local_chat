import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta

sockets = []
users = {}
commands = [":)", ":(", ":Exit", ":mytime", ":+1hr", ":Users", ":Msg"]


#listen thread mainloop
def run(client_socket, address, passcode):

    #check password first
    verified = False
    login = client_socket.recv(1024)
    print(login)
    if login.decode() != passcode:
        print("user not validated")
        client_socket.close()
        return
    
    #receive client username - more efficient to store here than send repeatedly from client
    username = client_socket.recv(1024).decode()
    users[address] = username
    join_msg = f"<{username}> joined the chatroom"
    print(join_msg)
    for s in sockets:
        if s != client_socket:
            s.send(join_msg)

    #main loop
    while True:
        msg = client_socket.recv(1024).decode()
        if not msg:
            break

        if msg[:4] == ":Msg":
            #handle it
            i = 5
            j = 5
            while msg[j] != " ":
                j += 1

            user = msg[i:j]
            dm = msg[j+1:]
            
            continue

        
        #handle special input
        '''
        if msg in commands:
            match(msg):
                case ":)":
                case ":(":
                case ":Users":
                case ":mytime":
                case ":+1hr":
                case ":Exit":


'''

        formatted = f"<{username}>: " + msg.decode()
        print(formatted)
        for s in sockets:
            if s != client_socket:
                s.send(formatted)



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
        (client_socket, address) = mySocket.accept()
        print(address)
        ct = threading.Thread(args=(client_socket, address, passcode), target=run)
        ct.start()
        sockets.append(client_socket)



if __name__ == "__main__":
    main()