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

class RegEntry(object):
    def __init__(self,pathx,namex):
        super(RegEntry,self).__init__
        self.path = pathx
        self.name = namex
        try:
            key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE)   
        except:  # BI_LUM is not there we create it
            try:
                self.path = r'Software'
                self.name = r'BI_LUM' 
                self.create_sub_key()
                key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE) 
            except: 
                print ('bizarre1')  
                
        #reference list stored in namex and call list_entry         
        self.path = pathx
        self.name = namex
        values = self.list_entry()
        if values is None :
            self.clear_entry()
        

    def create_sub_key(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE)
        winreg.CreateKeyEx(key, self.name, 0, winreg.KEY_WRITE)
        winreg.CloseKey(key)

    def list_entry(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_READ)
        try:
            values = winreg.QueryValueEx(key, self.name)
            winreg.CloseKey(key)
            return values[0]
        except:
            print('bizarre2')
            return None

    def clear_entry(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, self.name, 0, winreg.REG_MULTI_SZ, [])
        winreg.CloseKey(key)
        
    def add_entry(self, hid):
        values = self.list_entry()
        
        if (values is not None) and (hid not in values):
            values.append(hid)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, self.name, 0, winreg.REG_MULTI_SZ, values)
            winreg.CloseKey(key)

       
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


 
       
def select_level_1_or_123(path, name):  
    global choice_return, file_list, listbox1, master, txt 


    def clicked_List_Submit_lv1(e):     
        global choice_return 
        choice_returnx = file_list[listbox1.curselection()[0]]
        choice_return = (choice_returnx, '1')
        master.destroy()  
    
    def clicked_Entry_Submit_lv1():   
        global choice_return 
        choice_returnx = txt.get()
    #    lbl.configure(text= "")
    
        path = r'Software\BI_LUM'
        name = "maiframe_lv1"
        tt = RegEntry(path,name)
        tt.add_entry(choice_returnx)     
        choice_return = (choice_returnx, '1')
        window1.destroy()  
        
    def clicked_List_Submit_lv3(e):     
        global choice_return 
        choice_returnx = file_list[listbox1.curselection()[0]]
        choice_return = (choice_returnx, '3')
        master.destroy()     
        
    #get the sorted Lv1_2_3 entries    
    pathx = r'Software\BI_LUM'
    namex = "maiframe_lv1_2_3"
    tt = RegEntry(pathx,namex)
    file_list = tt.list_entry()    

   
    #if a list of Lv1_2_3 entry is in the window registry we present a list selection GUI
    if (file_list != []) and (file_list is not None) :
        master = tk.Tk()  
        listbox1 = tk.Listbox(master, height = 40, width = 40)
        
        for line in file_list:
           listbox1.insert(tk.END, str(line))
        listbox1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        listbox1.bind("<Double-1>", clicked_List_Submit_lv3)   
        scroll1 = tk.Scrollbar(master)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)   
        scroll1.configure(command=listbox1.yview)
        listbox1.configure(yscrollcommand=scroll1.set)     
        master.mainloop()        



    # if a lvl 1 2 3 is selected 
    if not ((choice_return is None) or  (choice_return == "")) :
        return choice_return        

    #get the sotre Lv1 entries    
    #path = r'Software\BI_LUM'
    #name = "maiframe_lv1"
    tt = RegEntry(path,name)
    file_list = tt.list_entry()    

   
    #if a list of Lv1 entry is in the window registry we present a list selection GUI
    if (file_list != []) and (file_list is not None) :
        master = tk.Tk()
    
        listbox1 = tk.Listbox(master, height = 40, width = 40)
        for line in file_list:
           listbox1.insert(tk.END, str(line))
        listbox1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        listbox1.bind("<Double-1>", clicked_List_Submit_lv1)
    #    listbox1.bind("<<ListboxSelect>>", clicked_List_Submit)    
    
        scroll1 = tk.Scrollbar(master)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)
    
        scroll1.configure(command=listbox1.yview)
        listbox1.configure(yscrollcommand=scroll1.set)    
    
        master.mainloop()
        
        
    # if no entry saved as of yet or the user pressed the 'X' button selecting no Lv1 entry, we show a Text Gui to enter Lvl1
    if (choice_return is None) or  (choice_return == "") :
        window1 = tk.Tk()
        window1.title("Enter Level1")
        #window.geometry('100x200')
        window1.config(height=100, width=200, bg="#C2C2D6")
            
        txt = tk.Entry(window1,width=40)
        txt.grid(column=1, row=1)
        #txt.pack(padx=100, pady=100, side = 'bottom')
        
        #clicked_Entry_Submit will show the text GUI   AND  save the entry in the window registery 
        btn = tk.Button(window1, text="Submit", bg="white", fg="green",  height = 2, width = 10, command=clicked_Entry_Submit_lv1)
        btn.grid(column=2, row=1)
        
        window1.mainloop()
       
    return choice_return
        
 
    

def select_level_2_3():  
    global choice_return, file_list, listbox1, master 
    
    
    def clicked_List_Submit(e):
        global choice_return         
        choice_return = file_list[listbox1.curselection()[0]]
  
        master.destroy()     

    
    choice_return = "" 
    
    master = tk.Tk()
    
    listbox1 = tk.Listbox(master, height = 40, width = 40)
    for line in file_list:
       listbox1.insert(tk.END, str(line))
    listbox1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    listbox1.bind("<Double-1>", clicked_List_Submit)
#    listbox1.bind("<<ListboxSelect>>", clicked_List_Submit)    

    scroll1 = tk.Scrollbar(master)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    scroll1.configure(command=listbox1.yview)
    listbox1.configure(yscrollcommand=scroll1.set)    

    master.mainloop()
    
    return choice_return  

        

def select_mbr():  
    global choice_return, mbr_list, listbox1,master 
    
    
    def clicked_List_Submit(e):
        global choice_return         
        choice_return = mbr_list[listbox1.curselection()[0]]
        
        #tt = mylist.curselection()[0]
        #choice_return = 'tata'
        master.destroy()      
    
    choice_return = "" 
    
    master = tk.Tk()
    
    listbox1 = tk.Listbox(master, height = 40, width = 40)
    for line in mbr_list:
       listbox1.insert(tk.END, str(line))
    listbox1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    listbox1.bind("<Double-1>", clicked_List_Submit)
#    listbox1.bind("<<ListboxSelect>>", clicked_List_Submit)    

    scroll1 = tk.Scrollbar(master)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    scroll1.configure(command=listbox1.yview)
    listbox1.configure(yscrollcommand=scroll1.set)    

    master.mainloop()
    
  
    return choice_return  



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

def call_mbr_to_df(mbr_sel):  
    global acum_txt
    def append_newline(input):
        global acum_txt
        acum_txt = acum_txt + input + "\n"  
        
    acum_txt = ''
  
    print(sess.pwd())        
    sess.retrlines('RETR ' + mbr_sel, append_newline)
    
 
    return acum_txt


#------------------------------------------------------------------------

#sess = ftplib.FTP('imftpb','CNDWLMM','LCJCMHF9')
sess = connect_with_password()

path = r'Software\BI_LUM'
name = "maiframe_lv1"
tup1 = select_level_1_or_123(path, name) 
if tup1[1] == '1' :
    lvl_1 = tup1[0]
    sess.cwd("'"+lvl_1+"'")
    file_list = sess.nlst()
    

    lvl_2_3 = select_level_2_3()
    # if a lvl 1 2 3 is selected 
    if (lvl_2_3 is None) or  (lvl_2_3 == "") :
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Warning ", "Nothing selected" )
        root.destroy()
        sys.exit() 
         
    path = r'Software\BI_LUM'
    name = "maiframe_lv1_2_3"
    dir_1 = lvl_1 + "." + lvl_2_3
    tt = RegEntry(path,name)
    tt.add_entry(dir_1)
    
else :
    dir_1 = tup1[0]


print(dir_1)

sess.cwd("'"+dir_1+"'")


try:
    mbr_list = sess.nlst()
except:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "NO member or NO permission to access: "+ dir_1 )
    root.destroy()
    sys.exit(0)



path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"

in_file = path+'SQL_Parsing_Input_Members.csv'

if os.path.exists(in_file):
    os.remove(in_file)	
     
df_tot_wrk = pd.DataFrame(list(zip([' '] * len(mbr_list),mbr_list,[dir_1] * len(mbr_list))), columns=['flag', 'mbr','file'])
df_tot_wrk.to_csv(in_file,mode = 'w',header=True, index = False)    


    
    
print( 'calling excel....')

excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(in_file)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()
 
    


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
