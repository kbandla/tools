#!/bin/python
'''
Created on Aug 18, 2009
VirusTotal and Threatexpert Reports

@author: kbandla@in2void.com
'''
from BeautifulSoup import BeautifulSoup
import re,urllib,httplib

class report():
    def __init__(self,hash,debug = False):
        self.hash = hash
        self.debug = debug
        self.vendors = ["a-squared",
                        "AhnLab-V3",
                        "AntiVir",
                        "Antiy-AVL",
                        "Authentium",
                        "Avast",
                        "AVG",
                        "BitDefender",
                        "CAT-QuickHeal",
                        "ClamAV",
                        "Comodo",
                        "DrWeb",
                        "eSafe",
                        "eTrust-Vet",
                        "F-Prot",
                        "F-Secure",
                        "Fortinet",
                        "GData",
                        "Ikarus",
                        "Jiangmin",
                        "K7AntiVirus",
                        "Kaspersky",
                        "McAfee",
                        #"McAfee+Artemis",    #bug, unicode?
                        "McAfee-GW-Edition",
                        "Microsoft",
                        "NOD32",
                        "Norman",
                        "nProtect",
                        "Panda",
                        "PCTools",
                        "Prevx",
                        "Rising",
                        "Sophos",
                        "Sunbelt",
                        "Symantec",
                        "TheHacker",
                        "TrendMicro",
                        "VBA32",
                        "ViRobot",
                        "VirusBuster"]
        
    def getVirusTotal(self):
        hash = self.hash 
        x = 152
        y = 23
        params = urllib.urlencode({'hash': hash, 'x':x, 'y':y})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Referer": "http://www.virustotal.com/buscaHash.html"}
        u = httplib.HTTPConnection("www.virustotal.com")
        u.request('POST', '/vt/en/consultamd5', params, headers)
        result =  u.getresponse()
        u.close()
        if not (result.getheader('location') == "/buscaHash.html?notfound"):
            return 'http://www.virustotal.com'+result.getheader('location')
        else:
            return False
        
    def getScanner(self):
        hash = self.hash
        link = self.getVirusTotal()
        if not link:
            return False
        results = {}
        data = urllib.urlopen(link).read()
        soup = BeautifulSoup(data)
        for av in ["eTrust-Vet","Kaspersky","McAfee", "Microsoft","Symantec"]: #for all scanners, use self.vendors. See below. 
        #for av in self.vendors: #for whole list
            comment = soup.find(text=re.compile(av))
            res = {}
            try:
                #a complete mess, but it works for now.
                res['version'] = comment.next.next.next
                res['date'] = comment.next.next.next.next.next.next
                res['detect'] = str(comment.next.next.next.next.next.next.next.next.contents[0])
            except:
                version,date,detect = '','',''
            if self.debug:
                print ('[VTOTAL] %s %s %s %s' %(av,res['version'],res['date'],res['detect']))
            results[av] = res
        return results 
  
    def getThreatExpert(self):
        hash = self.hash
        u = httplib.HTTPConnection("www.threatexpert.com")
        u.request('GET', '/report.aspx?md5=%s'%(hash))
        result =  u.getresponse()
        u.close()
        if (result.status == 200):
            return 'http://www.threatexpert.com/report.aspx?md5=%s'%(hash)
        else:
            return False
  
    
if __name__ == "__main__":
    import sys
    from hashlib import md5
    hash = md5(file(sys.argv[1]).read()).hexdigest()
    x = report(hash)
    print '-----------------------------------------'
    print 'MD5 : %s'%(hash)
    print ''
    print x.getThreatExpert()
    print x.getVirusTotal()
    print ''
    if x.getScanner():
        print 'VirusTotal Results:'
        for av,result in  x.getScanner().items():
            print '%20s %15s %10s %10s'%(av,result['version'],result['date'],result['detect'])
    print '-----------------------------------------'