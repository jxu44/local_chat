import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta

#TODO: Implement all code for your server here

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count') 
    parser.add_argument('-p', "--port")
    args = parser.parse_args()

    print(args)






if __name__ == "__main__":
    main()