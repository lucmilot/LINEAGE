# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
import pandas as pd

import os



path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")


sql_file = path+'sql1_extract.sql'
out_file = path+'sql1_extract.csv'


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