#!/usr/bin/python
import glob
'''
 A basic HTTP server for sharing files over the browser
 Very useful to xfer files to a VM while analyzing. Default port 8888
 kbandla@in2void.com

 deps:
     Cherrypy >= 3.0
     http://download.cherrypy.org/cherrypy/3.1.2/CherryPy-3.1.2.tar.gz
'''
import os.path
import sys
import cherrypy
from cherrypy.lib.static import serve_file
SERVER  = "0.0.0.0"
PORT = 8888

class Root:
    def index(self, directory="."):
    html_ = ''
        html = """<html><body><h2>files in  %s:</h2>
        <a href="index?directory=%s">Up</a><br />
        """ % (directory,os.path.dirname(os.path.abspath(directory)))

        for filename in glob.glob(directory + '/*'):
            absPath = os.path.abspath(filename)
            if os.path.isdir(absPath):
                html += '[<a href="/index?directory=' + absPath + '">' + os.path.basename(filename) + "</a>] <br />"
            else:
                html_ += '<a href="/download/?filepath=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
                
        html += html_
    html += """</body></html>"""
        return html
    index.exposed = True

class Download:
    
    def index(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
    index.exposed = True

cherrypy.tree.mount(Root())
if __name__ == '__main__':
    root = Root()
    root.download = Download()
    if len(sys.argv) == 2:
        SERVER = sys.argv[1]
    cherrypy.config.update({'server.socket_host': SERVER,
                        'server.socket_port': PORT,
                       })
    cherrypy.quickstart(root)