import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta

users = {}
#:Msg handled seperately
commands = [":)", ":(", ":Exit", ":mytime", ":+1hr", ":Users"]


#listen thread mainloop
def run(client_socket, passcode):

    #check password first
    login = client_socket.recv(1024).decode()
    i = 0
    while login[i] != "%":
        i += 1
    
    if login[:i] != passcode:
        print("user not validated")
        sys.stdout.flush()
        client_socket.close()
        return
    
    #parse username
    while login[i] == "%":
        i += 1

    username = login[i:]
    users[username] = client_socket
    join_msg = f"{username} joined the chatroom"
    print(join_msg)
    sys.stdout.flush()
    for s in users.values():
        if s != client_socket:
            s.send(join_msg.encode())

    #main loop
    while True:
        formatted = ""
        msg = client_socket.recv(1024).decode()
        if not msg:
            break

        if msg[:5] == ":Msg ":
            #handle it
            i = 5
            j = 5
            while msg[j] != " ":
                j += 1

            target = users.get(msg[i:j], 0)
            if not target:
                client_socket.send(f"User {msg[i:j]} not found".encode())
                continue           

            dm = msg[j+1:]
            formatted = f"[Message from {username}]: " + dm
            
            target.send(formatted.encode())
            print(f"{username}: send message to {msg[i:j]}")
            sys.stdout.flush()
            continue

        #for commands that request info
        sendBack = False

        #handle special input
        if msg in commands:
            match(msg):
                case ":)":
                    msg = "[feeling happy]"
                case ":(":
                    msg = "[feeling sad]"

                case ":Users":
                    msg = "searched up active users"

                    #return message
                    request = "Active Users: "
                    for u in users.keys():
                        request += f"{u}, "
                    request = request[:-2]
                    client_socket.send(request.encode())

                case ":mytime":
                    sendBack = True
                    time = datetime.now()
                    msg = time.strftime("%c")
                    
                case ":+1hr":
                    sendBack = True
                    time = datetime.now() + timedelta(hours=1)
                    msg = time.strftime("%c")

                case ":Exit":
                    msg = f"{username} left the chatroom"
                    for s in users.values():
                        if s != client_socket:
                            s.send(msg.encode())

                    client_socket.close()
                    return


        formatted = f"{username}: " + msg
            
        print(formatted)
        sys.stdout.flush()
        if sendBack:
            client_socket.send(formatted.encode())
        for s in users.values():
            if s != client_socket:
                s.send(formatted.encode())



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', action='store_true')
    parser.add_argument('-passcode', '--passcode', type=str) 
    parser.add_argument('-port', "--port", type=int)
    args = parser.parse_args()

    if not args.port:
        print("Please provide a port.")
        sys.stdout.flush()
        return
    if not args.passcode or len(args.passcode) > 5:
        print("Incorrect passcode")
        sys.stdout.flush()
        return

    passcode = args.passcode
    port = args.port


    

    mySocket = socket.socket()
    mySocket.bind(('127.0.0.1', port))
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()
    mySocket.listen(5)
    while True:
        (client_socket, address) = mySocket.accept()
        ct = threading.Thread(args=(client_socket, passcode), target=run)
        ct.start()



if __name__ == "__main__":
    main()