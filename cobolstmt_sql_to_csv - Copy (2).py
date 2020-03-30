# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
import pandas as pd

import os


import win32com.client as win32

excel = win32.gencache.EnsureDispatch('Excel.Application')

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")

#C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\jobiteration_sql_job.csv
sql_file = path+'cobolstmt_sql.sql'
out_file = path+'cobolstmt_sql.csv'


if os.path.exists(out_file):
    os.remove(out_file)


with open(sql_file, 'r') as f2:
    in_sql = f2.read()
f2.closed

print(in_sql)


cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF8;CURRENTSCHEMA=RE')
cursor = cnxn.cursor()


cursor.execute(in_sql)


line_count = 1

while True:
    rows = cursor.fetchmany(5000)

    if len(rows) == 0:
            break
        
    labels = [
'LVS_OWNERPGM',
'LVS_OWNERLABEL',           
'LVS_NAME',
'LVS_BUFF'
        ]
     
    df = pd.DataFrame.from_records(rows, columns=labels)
       
    if line_count == 1:
        df.to_csv(out_file,mode = 'a',header=True, index = False)
    else:
        df.to_csv(out_file,mode = 'a',header=False, index = False)
    
    line_count += len(rows)
    print(line_count)

cursor.close()

cnxn.close()



print( 'calling excel....')
wb = excel.Workbooks.Open(out_file)

excel.ActiveSheet.Columns.AutoFit()


print ('DONE')