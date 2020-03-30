# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
import pandas as pd

import os

import csv



path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")


sql_file = path+'sql1_extract.sql'
out_file = path+'sql1_extract.csv'


if os.path.exists(out_file):
    os.remove(out_file)



with open(in_file, 'r') as f1:
    reader = csv.reader(f1)
    in_list = list(reader)
f1.closed

print(*in_list, sep="\n")

with open(sql_file, 'r') as f2:
    in_sql = f2.read()
f2.closed

print(in_sql)




cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF8;CURRENTSCHEMA=RE')
cursor = cnxn.cursor()


cursor.execute(in_sql)


while True:
    rows = cursor.fetchmany(100)
    if len(rows) == 0:
            break
        
    labels = [
'dds_dsn',
'dds_dsn_x',           
'DDS_JOBNAME',
'DDS_STEP_PROGR',
'pgmname',
'DDS_N_PROGR',
'DDS_DDNAME',
'DDS_DISP1'
        ]
    df = pd.DataFrame.from_records(rows, columns=labels)
        #print ( df )

cursor.close()

cnxn.close()

print ('DONE')