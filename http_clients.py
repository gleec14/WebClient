#!/usr/bin/env python
import socket
import ssl
import sys
from abc import ABC, abstractmethod
from urlparser import UrlParser

class Client(ABC):
    @abstractmethod
    def request(self, url):
        """ Request the resource indicated by the url. """
        pass

    @abstractmethod
    def __str__(self):
        pass

class HttpClient(Client):

    """Interface for user to request and receive web resources from web servers using HTTP

    Attributes:
        socket: socket from which the client will communicate
        port: set to 80 so client can send and receive from Web servers
        target: target domain name
        data: data received from the server will be stored here
    """

    def __init__(self):
        self.sock = 0
        self.port = 80
        self.target = ''
        self.data = ''

    def connect(self, sock, host):
        """ Attempt connection with host at domain name.

        Params:
        sock -- socket from which we connect to the host
        host -- domain name that we wish to connect to
        """
        try:
            host_ip = socket.gethostbyname(host)
            sock.connect((host_ip, self.port))
            self.target = host
            print('the socket has successfully connected on port {}'.format(self.port))
            return 1
        except socket.gaierror:
            print('there was an error resolving the host {}'.format(host))
            return 0

    def request(self, url, params={}):
        #Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Clear data from previous request
        self.data = ''

        #Parse url and connect to host
        host, path = UrlParser.parse_url(url)
        if not self.connect(self.sock, host):
            return

        #Send HTTP request
        req = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)
        print('HTTP request\n{}'.format(req))
        self.sock.send(req.encode())
        print('sent HTTP request')

        #Receive and store response
        buffer = ''
        data = self.sock.recv(1024)
        while data:
            try:
                buffer += data.decode('utf-8')
            except UnicodeDecodeError:
                print("Could not decode a block of data using utf-8")
            data = self.sock.recv(1024)
        self.data = buffer

        #Close the connection now that you have everything
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print("connection closed")

    def __str__(self):
        print("HTTPClient connected with DomainName {} on port {}.".format(self.target, self.port))

class HttpsClient(Client):

    """Interface for user to request and receive web resources from web servers using HTTPS

    Attributes:
        socket: socket from which the client will communicate
        port: set to 443 so client can send and receive from Web servers
        target: target domain name
        data: data received from the server will be stored here
    """

    def __init__(self):
        self.sock = 0
        self.port = 443
        self.target = ''
        self.data = ''

    def request(self, url):
        #Create default ssl context to allow HTTPS connections
        context = ssl.create_default_context()

        #Parse url and connect to host
        host, path = UrlParser.parse_url(url)

        #Connect to host and return if host does not exist
        try:
            sock = socket.create_connection((host, self.port))
            ssock = context.wrap_socket(sock, server_hostname=host)
        except socket.gaierror:
            print('there was an error resolving the host {}'.format(host))
            return
        else:
            with ssock:
                self.sock = ssock
                #Send HTTP request
                req = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, host)
                print('HTTP request\n{}'.format(req))
                self.sock.send(req.encode())
                print('sent HTTP request')

                #Receive and store response
                buffer = ''
                data = self.sock.recv(1024)
                while data:
                    try:
                        print(data.decode('utf-8'),flush=True)
                        buffer += data.decode('utf-8')
                    except UnicodeError:
                        print("Could not decode a block of data using utf-8")
                    data = self.sock.recv(1024)
                self.data = buffer
                print("\n\ndone")

    def __str__(self):
        print("HTTPClient connected with DomainName {} on port {}.".format(self.target, self.port))

def http_test(url):
    ''' tests if the HttpClient works '''
    #Are all abstract methods implemented?
    c = HttpClient()
    print("HttpClient instantiated", flush=True)
    #Does the parser separate the domain name and path?
    host, path = UrlParser.parse_url(url)
    print("host:{}, path:{}".format(host, path), flush=True)
    #Does connect() behave correctly
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(sock, host)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print("connect() tested", flush=True)
    #Can data be requested and received?
    c.request(url)
    print("request() tested", flush=True)
    c.__str__()
    print(c.data)
    sys.exit()

def https_test(url):
    c = HttpsClient()
    c.request(url)
    c.__str__()
    sys.exit()

def main():
    url = 'http://www.postgresqltutorial.com/'
    http_test(url)
    #https_test(url)

if __name__ == "__main__":
    main()
