# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
import pandas as pd

import os, sys


import win32com.client as win32




#get all the job info for all jobs formating YMMDD etc with FFFF

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"


out_file = path+'jobiteration_sql_job.csv'


if os.path.exists(out_file):
    os.remove(out_file)



in_sql = '''
select

trim(dds_dsn) as dsn,
trim(DDS_JOBNAME) as JOBNAME,
trim(DDS_STEP_PROGR) as STEP_PROGR,
trim(stp.STP_PGMMVS)  as pgmname,
trim(DDS_N_PROGR) as N_PROGR,
trim(DDS_DDNAME) as DDNAME,
trim(DDS_DISP1) as DISP1

from re.bjdds as dds


left outer join 
RE.BJSTEPS as stp
on
(
dds.dds_jobname = stp.stp_jobname and
dds.dds_step_progr = stp.stp_n_progr
)

where dds_dsn <> ''
order by
dsn,
jobname, 
STEP_PROGR,
N_PROGR
;
'''
print(in_sql)


'''

OPTIONS = [
"Jan",
"Feb",
"Mar"
] #etc

master = tk.Tk()

variable = tk.StringVar(master)
variable.set(OPTIONS[0]) # default value

w = tk.OptionMenu(master, variable, *OPTIONS)
w.pack()

def ok():
    print ("value is:" + variable.get())

button = tk.Button(master, text="OK", command=ok)
button.pack()

tk.mainloop()
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

 
fen1 = tk.Tk()   ## Fenêtre principale
 
def Ouvrir():
    filedialog.askopenfilename()
def Enregistrer(): 
    messagebox.showinfo("Enregistrer")
def EnregistrerSous(): 
    messagebox.showinfo("Enregistrer sous ...")
def Option(): 
    messagebox.showinfo("Option")
def Aide(): 
    messagebox.showinfo("Aide")
def Apropos(): 
    messagebox.showinfo("A propos")
 
mainmenu = tk.Menu(fen1)
 
menuFichier = tk.Menu(mainmenu)  ## Menu Fils
menuFichier.add_command(label = "Ouvrir", command = Ouvrir)
menuFichier.add_separator()
menuFichier.add_command(label = "Enrtegistrer" , command = Enregistrer)
menuFichier.add_command(label = "Enregistrer sous ..." , command = EnregistrerSous)
menuFichier.add_separator()
menuFichier.add_command(label = "Quitter" , command = fen1.quit)
 
menuEdition = tk.Menu(mainmenu) ## Menu Fils
menuEdition.add_command(label = "Option", command = Option)
 
menuAide = tk.Menu(mainmenu) ## Menu Fils
menuAide.add_command(label = "Aide" , command = Aide)
menuAide.add_separator()
menuAide.add_command(label = "A propos" , command = Apropos)
 
mainmenu.add_cascade(label = "Fichier", menu = menuFichier)
mainmenu.add_cascade(label = "Edition", menu = menuEdition)
mainmenu.add_cascade(label = "Aide", menu = menuAide)
 
fen1.config(menu = mainmenu)
 
fen1.mainloop()

fen1.destroy()

'''
root = tk.Tk()   ## Fenêtre principale

def Affiche(): tk.tkMessageBox.showinfo("Exemple d'un Menu Tkinter")
def About(): tk.tkMessageBox.showinfo("A propos", "Version 1.0")
    
mainmenu = tk.Menu(root)  ## Barre de menu
menuExample = tk.Menu(mainmenu)  ## Menu fils menuExample
menuExample.add_command(label="Affiche", command=Affiche)  ## Ajout d'une option au menu fils menuFile
menuExample.add_command(label="Quitter", command=root.quit)

menuHelp = tk.Menu(mainmenu) ## Menu Fils
menuHelp.add_command(label="A propos", command=About)

mainmenu.add_cascade(label = "Exemple", menu=menuExample)
mainmenu.add_cascade(label = "Aide", menu=menuHelp)

root.config(menu = mainmenu)

root.mainloop()
'''


cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF9;CURRENTSCHEMA=RE')
cursor = cnxn.cursor()

cursor.execute(in_sql)

labels = [
'DSN',        
'JOBNAME',
#step position within the job
'STEP_PROGR',
'PGM_NAME',
#dd position within the step
'N_PROGR',
'DDNAME',
'DISP1'
        ]


df_out = pd.DataFrame()
line_count = 0

while True:
    rows = cursor.fetchmany(10000)

    if len(rows) == 0:
            break
        
    df = pd.DataFrame.from_records(rows, columns=labels)
    df_out = pd.concat([df_out, df])
    if line_count == 1:
        df.to_csv(out_file,mode = 'a',header=True, index = False)
    else:
        df.to_csv(out_file,mode = 'a',header=False, index = False)
    
    line_count += len(rows)
    print(line_count)


cursor.close()
cnxn.close()


df_out.sort_values( ['JOBNAME','STEP_PROGR'])      
df_out.to_csv(out_file, mode = 'w',header=True, index = False)

print( 'calling excel....')

excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(out_file)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()


print ('DONE')