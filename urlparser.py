#!/usr/bin/env python

class UrlParser:
    """
    A utilities class to help parse requests and responses
    """
    @classmethod
    def parse_url(cls, url):
        ''' Separate protocol HTTP(S) from url '''
        s = url.split('//')
        if len(s) > 1:
            s = s[1]
        else:
            s = s[0]
        ''' Separate domain name from path '''
        ret = s.find('/')
        host = s
        path = '/'
        if ret != -1:
            host = s[:ret]
            path = s[ret:]
        print('host is: {}'.format(host))
        print('path is: {}'.format(path))
        return host, path
