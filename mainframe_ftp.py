# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:47:14 2018

@author: XT21586
"""

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\"
filename = path+'test.txt'
if os.path.exists(filename):
    os.remove(filename)

from ftplib import FTP
ftp = FTP('imftpb')
ftp.login(user='CNDWLMM',passwd='LCJCMHF8')

ftp.cwd("'CHANGEI.CNDWPROD.JCLMASTR'")

ftp.dir()


#to redirect console output 
import sys
from contextlib import contextmanager
@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout
        
        
with open(filename, "w") as f:
    with stdout_redirected(f):
        ftp.dir()
        #print ("Hello world")       



import subprocess

process = subprocess.Popen(['dir'], stdout=subprocess.PIPE)

process = subprocess.Popen(['ls'], stdout=subprocess.PIPE)






ll = []

ll = ftp.dir()

ftp.dir('CHANGEI.CNDWPROD.JCLMASTR')

ftp.cwd('''CHANGEI.CNDWPROD.JCLMASTR.''')

ftp.cwd('''CHANGEI.CNDWPROD.JCLMASTR''')

ftp.cd('''CHANGEI.CNDWPROD.JCLMASTR''')

ftp.dir()

ftp.retrlines('LIST')

ftp.retrlines('NLST')


ftp.retrlines('dir')

ftp.cwd("'CHANGEI.CNDWPROD.JCLMASTR'")


import ftplib
import os
from sys import exc_info


sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF8')

filelist = sess.nlst()

print(ftp.ls)

ftplib.list

sess.quit()


ftp.retrlines("File To be Downloaded")





I am trying to parse / download some of the files from Mainframe using ftplib but it's unsuccesful after few attempts. 

My code Till now is :
import ftplib
ftp = ftplib.FTP('host','username','password')
ftp.retrlines("File To be Downloaded")


sess = ftplib.FTP("imftpb", "CNDWLMM", "LCJFMHF8")
sess.sendcmd("site sbd=(IBM-1047,ISO8859-1)")
for dir in ["ASM", "ASML", "ASMM", "C", "CPP", "DLLA", "DLLC", "DLMC", "GEN", "HDR", "MAC"]:
    sess.cwd("'ZLTALM.PREP.%s'" % dir)
    try:
        filelist = sess.nlst()
    except ftplib.error_perm as x:
        if (x.args[0][:3] != '550'):
            raise
    else:
        try:
            os.mkdir(dir)
        except:
            continue
        for hostfile in filelist:
            lines = []
            sess.retrlines("RETR "+hostfile, lines.append)
            pcfile = open("%s/%s"% (dir,hostfile), 'w')
            for line in lines:
                pcfile.write(line+"\n")
            pcfile.close()
        print ("Done: " + dir)
sess.quit()