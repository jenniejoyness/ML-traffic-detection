import os
import socket, sys
from operator import itemgetter

BUFFER_SIZE = 1024


def user_mode(TCP_IP, TCP_PORT):
    # make connection with server to ask for file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("connected")
    # waiting for user input
    request = b'2,sunny\tsunday\tno\t11:30-13:30\r\n'
    #todo
    s.sendall(request)
    # receive a string of all file names and info
    response = s.recv(BUFFER_SIZE)
    print(response)
        # if request == s:
        #     break

if __name__ == "__main__":

    #TCP_IP = '52.201.126.29'
    TCP_IP = '127.0.0.1'
    TCP_PORT = 3001
    user_mode(TCP_IP, TCP_PORT)