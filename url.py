#!/usr/bin/python
'''
Created on Apr 26, 2011
URL Expander

@author: kbandla
'''

import sys
import httplib, urlparse, urllib

def main(url):
    if not url.startswith('http'):
        url = "http://"+url
    url = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(url.netloc,80)
    conn.request("GET",url.path)
    res = conn.getresponse()
    if res.status in [301,307]:
        x = res.getheader("Location")
        print "%s --> %s"%(url.geturl(),x)
        main(x)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'url <tiny-url>'
        exit(-1)
    main(sys.argv[1])