# ECE303 Communication Networks
# Project 1: Port Scanner
# Written by Jon Lu 03/09/2021

import sys 
import socket
from socket import getservbyport

def portscan(hostname, lowerbound, upperbound):
    try:
        for port in range(lowerbound, upperbound):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            check = s.connect_ex((hostname, port))

            if check == 0:
                print("{}:{}, service {}, is open.".format(hostname, port, getservbyport(port)))
            s.close()
    except:
        pass

def main():
    lowerbound = 1
    upperbound = 1024
    
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Correct program syntax is: python3 portscanner.py hostname [lowerport upperport].")
        print("Either [lowerport upperport] are both defined or they are both not; if they are not defined, the default is 1 and 1024.")
        quit()

    elif len(sys.argv) > 2 and len(sys.argv) <= 4:
        if not ((type(int(sys.argv[2])) is not int) or (int(sys.argv[2]) < 1)):
            lowerbound = int(sys.argv[2])
        if not ((type(int(sys.argv[3])) is not int) or (int(sys.argv[3]) < lowerbound)):
            upperbound = int(sys.argv[3])

    portscan(sys.argv[1], lowerbound, upperbound)

if __name__ == "__main__":
    main()