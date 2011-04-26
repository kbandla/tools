#!/usr/bin/python
'''
Created on Apr 26, 2011
URL Expander

@author: kbandla
'''

import sys
import httplib, urlparse, urllib

headers = {"Accept":"application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
           "Accept-Charset" : "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
           "Accept-Language" : "en-US,en;q=0.8",
           "User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"
           }

def main(url):
    if not url.startswith('http://'):
        url = "http://"+url
    url = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(url.netloc,80)
    conn.request("GET",url.path,headers=headers)
    res = conn.getresponse()
    if res.status in [301,307]:
        x = res.getheader("Location")
        print "%s --> %s"%(url.geturl(),x)
        main(x)

if __name__ == "__main__":
    main(sys.argv[1])