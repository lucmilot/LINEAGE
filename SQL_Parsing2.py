# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:36:01 2018

@author: XT21586
"""

import ftplib
import os, sys
from sys import exc_info
import tkinter as tk

import winreg as winreg

import win32com.client as win32

from tkinter import messagebox

import pandas as pd

import re

import subprocess

global choice_return, file_list, listbox1,master
choice_return = ""
file_list = []

       
def connect_with_password():  

    def clicked_Entry_username():   
        global return_txt 
        return_txt = txt.get()
        window1.destroy()  
        

    window1 = tk.Tk()
    window1.title("Enter Username")
    window1.config(height=100, width=200, bg="#C2C2D6") 
    txt = tk.Entry(window1,width=40)
    txt.grid(column=1, row=1)
    btn = tk.Button(window1, text="Submit", bg="white", fg="green",  height = 2, width = 10, command=clicked_Entry_username)
    btn.grid(column=2, row=1)      
    window1.mainloop()
    user_name = return_txt
    

    window1 = tk.Tk()
    window1.title("Enter Password")
    window1.config(height=100, width=200, bg="#C2C2D6") 
    txt = tk.Entry(window1,width=40)
    txt.grid(column=1, row=1)
    btn = tk.Button(window1, text="Submit", bg="white", fg="green",  height = 2, width = 10, command=clicked_Entry_username)
    btn.grid(column=2, row=1)      
    window1.mainloop()
    user_password = return_txt  
       
    sess = ftplib.FTP('imftpb',user_name,user_password)
    return sess


 

def call_notepad(out_file,in_file,typex):    
    def append_newline(input):
        fhandle.write(input + "\n")    
        
    fhandle = open(out_file, 'w')
  
    print(sess.pwd())        
    if typex == "M": 
        sess.retrlines('RETR ' + mbr_sel, append_newline)
    elif typex == "S":
        main_dir = ""
        sess.cwd("'"+main_dir+"'") 
        sess.retrlines('RETR ' + dir_1, append_newline)
    #sess.retrlines('RETR ' + filename, lambda  )
    fhandle.close()
 
    retcode = subprocess.Popen(['notepad ', out_file ])


def call_mbr_to_df(file_sel,mbr_sel):  
    global acum_txt
    def append_newline(input):
        global acum_txt
        acum_txt = acum_txt + input + "\n"  
        
    acum_txt = ''
    sess.cwd("'" + file_sel + "'")
    print(sess.pwd())        
    sess.retrlines('RETR ' + mbr_sel, append_newline)
    
 
    return acum_txt


sess = connect_with_password()

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"

in_file = path+'SQL_Parsing_Input_Members.csv'



labels = [
'flag', 'mbr', 'file'
]
df_seed = pd.read_csv(in_file , names=labels , skiprows = 1)
# \w Any word character (letter, number, underscore )
df_seed  = df_seed[df_seed['flag'].str.contains(re.compile('\w'))] 

  

List_mbr = []
List_stmt = []

for row in df_seed.itertuples(): 
    n = 0
    file_sel = row.file     
    mbr_sel = row.mbr   
    txt_1 = call_mbr_to_df(file_sel,mbr_sel)
    
    out_file = path+ mbr_sel + '.csv'
    call_notepad(out_file,mbr_sel,'M')
    
    List_mbr.append(file_sel + "(" + mbr_sel + ")")
    List_stmt.append(txt_1 )
    
sess.quit    


'''
# put Seed and Level column on first 2 column 
if len (df_accum_tot) > 0 :     
    df_accum_tot = df_accum_tot[['seed'] + ['level'] + df_accum_tot.columns[:-2].tolist()]
    df_accum_tot.to_csv(out_file_asc, index = False)
    print (df_accum_tot.head())

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(out_file_asc)
    excel.Visible = True
    excel.ActiveSheet.Columns.AutoFit()
'''
