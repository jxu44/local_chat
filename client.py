import socket
import threading
import sys
import argparse


# TODO: Implement a client that connects to your server to chat with other clients here

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-pass', '--password') 
    parser.add_argument('-p', "--port")
    args = parser.parse_args()

    print(args)






if __name__ == "__main__":
    main()