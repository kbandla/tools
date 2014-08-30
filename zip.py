#!/usr/bin/python
'''
Created on Feb 5, 2008

File Zipper with password
deps:
    pexpect
@author: kbandla
'''
import sys,os,glob,zipfile,pexpect
from time import strftime,gmtime,time

#if there is not tmp in current dir, make one
if not os.path.exists('tmp'):
    os.mkdir('tmp')
#delete everything inside tmp
os.system('rm tmp/*')
#delete older samples.zip
os.system('rm samples.zip')
args = ['-e','samples.zip']
#get a list of files in the tmp directory 
for file in glob.glob("tmp/*"):
    args.append(file)
q1 = "Enter password:"
q2 = "Verify password:"
password = 'virus'
p = pexpect.spawn('zip', args)
p.expect(q1)
p.sendline(password)
p.expect(q2)
p.sendline(password)
p.expect(pexpect.EOF)
print p.before
#zipping done.

#if the email module (submit) is in the same directory, email is sent out also 
os.system('python submit samples.zip')