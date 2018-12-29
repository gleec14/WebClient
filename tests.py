import sys
import socket
from http_clients import HttpClient, HttpsClient
from urlparser import UrlParser

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

def test_request_http(domains):
    """ tests the request function of http and https Client

    Params:
    domains -- a list of domain names
    """
    print('Testing the HttpClient request()')
    c = HttpClient()
    c.request(domain)
    print(c.data)

def test_request_https(domain):
    """ tests the request function of https Client

    Params:
    domains -- a list of domain names
    """
    print('Testing the HttpsClient request()')
    c = HttpsClient()
    c.request(domain)

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as fo:
        for line in fo:
            #test_connection(domains)
            #test_request_http(domains)
            test_request_https(line[:-1]) #Get rid of newline at end
    sys.exit()

if __name__ == '__main__':
    main()
