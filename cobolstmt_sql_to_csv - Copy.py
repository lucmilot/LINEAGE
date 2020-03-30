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
in_file = path+'jobiteration_sql_job.csv'

wb = excel.Workbooks.Open(r'C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\jobiteration_sql_job.csv')

#wb = excel.Workbooks.Open(in_file)

#from win32com.client import constants
#appExcel = win32com.client.Dispatch("Excel.Application")

'''
import win32com.client as win32
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open('my_sheet.xlsm')

doc = appExcel.Documents.Add("ttt.xls")

doc = appExcel.Documents.Add(r'C:\Users\XT21586\Documents\document\_DOSSET\lineage\tttt.csv')


appExcel.Documents.Open(r'C:\Users\XT21586\Documents\document\_DOSSET\lineage\xx.csv')

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
in_file = path+'xx.csv'

print (in_file)

xlapp = win32com.client.DispatchEx("Excel.Application") 

xlapp.workbooks.open(r'C:\Users\XT21586\Documents\document\_DOSSET\lineage\xx.csv')


path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")


sql_file = path+'jobiteration_sql_job.sql'
out_file = path+'jobiteration_sql_job.csv'


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
    rows = cursor.fetchmany(10000)

    if len(rows) == 0:
            break
        
    labels = [
'DDS_DSN',
'DDS_DSN_X',           
'DDS_JOBNAME',
#step position within the job
'DDS_STEP_PROGR',
'PGM_NAME',
#dd position within the step
'DDS_N_PROGR',
'DDS_DDNAME',
'DDS_DISP1'
        ]
    
    df = pd.DataFrame.from_records(rows, columns=labels)
    if line_count == 1:
        df.to_csv(out_file,mode = 'a',header=True)
    else:
        df.to_csv(out_file,mode = 'a',header=False)
    
    line_count += len(rows)
    print(line_count)

cursor.close()

cnxn.close()

print ('DONE')
'''
