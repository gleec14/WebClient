#!/usr/bin/env python

import sys
import socket
from http_clients import HttpClient, HttpsClient
from urlparser import UrlParser

'''
def test_connection(domains):
    """ Tests the connection function of http client.

    Params:
    domains -- a list of domain names
    """
    #Test the HttpClient
    print('Testing the HttpClient connect()')
    c = HttpClient()
    for domain in domains:
        host, path =  UrlParser.parse_url(domain)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(sock, host)
        print('Connected with {}'.format(host))
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
'''
def test_request_http(domain, filename):
    """ tests the request function of http Client.

    Params:
    domains -- domain name to send request to
    filename -- filename to write response to
    """
    print('Testing the HttpClient request()')
    c = HttpClient()
    c.request(domain)
    with open('{}'.format(filename), 'w') as fo:
        fo.write(c.data)

def test_request_https(domain, filename):
    """ tests the request function of https Client.

    Params:
    domain -- domain name to send request to
    filename -- filename to write response to
    """
    print('Testing the HttpsClient request()')
    c = HttpsClient()
    c.request(domain)
    print("Opening file",flush=True)
    with open('{}'.format(filename), 'w+') as fo:
        print("Writing to file",flush=True)
        fo.write(c.data)

def main():
    #Check if file with urls is included
    if len(sys.argv) < 2:
        print("usage: tests.py <file with urls>")
        sys.exit()
    urls = sys.argv[1]
    #Read urls line by line and run tests. The results of each test will be written to its own file
    with open(urls, 'r') as fo:
        count = 0
        for line in fo:
            filename, path = UrlParser.parse_url(line)
            filename = filename.split('.')[0]

            filename = filename + str(count) + '.txt'
            test_request_http(line[:-1], filename)
            count += 1
            filename = filename[:-5] + str(count) + '.txt' #works up to single digit count
            test_request_https(line[:-1], filename) #Get rid of newline at end
            #filename = filename + str(count) + '.txt'
            #test_request_https(line[:-1], filename) #Get rid of newline at end
            count += 1
    sys.exit()

if __name__ == '__main__':
    main()
