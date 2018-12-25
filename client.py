#!/usr/bin/env python
import socket
import sys

class HttpParser:
    """
    A utilities class to help parse requests and responses
    """
    @classmethod
    def parse_url(cls, url):
        s = url.split('//')
        if len(s) > 1:
            s = s[1]
        ret = s.find('/')
        host = s
        path = '/'
        if ret != -1:
            host = s[:ret]
            path = s[ret:]
        print('host is: {}'.format(host))
        print('path is: {}'.format(path))
        return host, path

class HTTPClient:
    """Interface for user to create HTTP requests and receive HTTP responses

    Attributes:
        socket: socket from which the client will communicate
        port: set to 80 so client can send and receive from Web servers
        target: target domain name
        data: data received from the server will be stored here
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 80
        self.target = ''
        self.data = ''

    def set_target(self, host):
        self.target = host

    def connect(self, host=''):
        self.target = host
        try:
            host_ip = socket.gethostbyname(self.target)
            self.socket.connect((host_ip, self.port))
            print('the socket has successfully connected on port {}'.format(self.port))
        except socket.gaierror:
            print('there was an error resolving the host')
            print('target_host: {}'.format(self.target))
            sys.exit()

    def request(self, url, params={}):
        host, path = HttpParser.parse_url(url)
        self.connect(host)
        req = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)
        print('HTTP request\n{}'.format(req))
        self.socket.send(req.encode())
        print('sent HTTP request')

        buffer = ''
        data = self.socket.recv(1024)
        while data:
            print(data.decode)
            buffer += data.decode()
            data = self.socket.recv(1024)
        self.data = buffer

    def print_data(self):
        print(self.data)

    def close(self):
        self.socket.close()
        print('Client has closed the connection')

    def socket_info(self):
        print('socket is: {}'.format(self.socket))
        print('port is: {}'.format(self.port))
        print('target ip is: {}'.format(self.target))

client = HTTPClient()
client.socket_info()
client.request('http://www.google.com/')
client.print_data()
client.close()
sys.exit()
