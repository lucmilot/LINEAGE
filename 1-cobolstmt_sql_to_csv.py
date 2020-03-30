# -*- coding: utf-8 -*-
"""

"""

import pyodbc
import pandas as pd

import os


import win32com.client as win32



#get all the SELECT and READ info from BKLVSTMT.LVS_NAME  for all programs



path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")
#C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\jobiteration_sql_job.csv
sql_file = path+'cobolstmt_sql.sql'
out_file = path+'cobolstmt_sql.csv'
# while debuging we bypass password entry
#pssw = input('Password for DB2K: ')
pssw = 'LCJCMHF9'


if os.path.exists(out_file):
    os.remove(out_file)
notepad = "notepad " + sql_file
os.system(notepad) 
# while debuging we bypass the warning message 
#input("Save Notepad  and quit Notepad before pressing enter? ") 
with open(sql_file, 'r') as f2:
    in_sql = f2.read()
f2.closed

cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD='+pssw+';CURRENTSCHEMA=RE')
cursor = cnxn.cursor()
cursor.execute(in_sql)
print('Starting fetchall.......')
rows = cursor.fetchall()
cursor.close()
cnxn.close()

labels = [
'LVS_OWNERPGM',
'LVS_OWNERLABEL',           
'LVS_NAME',
'LVS_BUFF'
]
df = pd.DataFrame.from_records(rows, columns=labels) 
df['LVS_NAME'] = df['LVS_NAME'].apply(lambda x : str(x).strip())
df['LVS_OWNERPGM'] = df['LVS_OWNERPGM'].apply(lambda x : str(x).strip())
df.sort_values( ['LVS_OWNERPGM','LVS_NAME','LVS_BUFF'], inplace = True)         
df.to_csv(out_file,mode = 'w',header=True, index = False)
print( 'calling excel....')
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(out_file)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()


print ('DONE')