#!/usr/bin/env python
import socket
import sys

class HTTPClient:

    def __init__(self, host=""):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 80
        self.target = host

    def set_target(self, host):
        self.target = host

    def connect(self):
        try:
            host_ip = socket.gethostbyname(self.target)
            self.socket.connect((host_ip, self.port))
            print("the socket has successfully connected on port {}".format(self.port))
        except socket.gaierror:
            print("there was an error resolving the host")
            print("target_host: {}".format(self.target))
            sys.exit

    def close(self):
        self.socket.close()
        print("Client has closed the connection")

    def socket_info(self):
        print("socket is: {}".format(self.socket))
        print("port is: {}".format(self.port))
        print("target ip is: {}".format(self.target))

target_host = input("enter the targethostname: \n")
client = HTTPClient(target_host)
client.socket_info()
client.connect()
client.close()
