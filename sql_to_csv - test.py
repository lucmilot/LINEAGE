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



in_sql = """
select
case 

when locate_in_string(dds.dds_dsn,'2016',-1) > 0 then locate_in_string(dds.dds_dsn,'2016',-1)
when locate_in_string(dds.dds_dsn,'2017',-1) > 0 then locate_in_string(dds.dds_dsn,'2017',-1)
when locate_in_string(dds.dds_dsn,'2018',-1) > 0 then locate_in_string(dds.dds_dsn,'2018',-1)
when locate_in_string(dds.dds_dsn,'160',-1) > 0 then locate_in_string(dds.dds_dsn,'160',-1)
when locate_in_string(dds.dds_dsn,'170',-1) > 0 then locate_in_string(dds.dds_dsn,'170',-1)
when locate_in_string(dds.dds_dsn,'180',-1) > 0 then locate_in_string(dds.dds_dsn,'180',-1)
when locate_in_string(dds.dds_dsn,'161',-1) > 0 then locate_in_string(dds.dds_dsn,'161',-1)
when locate_in_string(dds.dds_dsn,'171',-1) > 0 then locate_in_string(dds.dds_dsn,'171',-1)
when locate_in_string(dds.dds_dsn,'181',-1) > 0 then locate_in_string(dds.dds_dsn,'181',-1)
when locate_in_string(dds.dds_dsn,'162',-1) > 0 then locate_in_string(dds.dds_dsn,'162',-1)
when locate_in_string(dds.dds_dsn,'172',-1) > 0 then locate_in_string(dds.dds_dsn,'172',-1)
when locate_in_string(dds.dds_dsn,'182',-1) > 0 then locate_in_string(dds.dds_dsn,'182',-1)
when locate_in_string(dds.dds_dsn,'163',-1) > 0 then locate_in_string(dds.dds_dsn,'163',-1)
when locate_in_string(dds.dds_dsn,'173',-1) > 0 then locate_in_string(dds.dds_dsn,'173',-1)
when locate_in_string(dds.dds_dsn,'183',-1) > 0 then locate_in_string(dds.dds_dsn,'183',-1)
else 0 end as pos,
trim(dds_dsn) as dds_dsn,
trim(DDS_JOBNAME) as DDS_JOBNAME,
trim(DDS_STEP_PROGR) as DDS_STEP_PROGR,
trim(DDS_N_PROGR) as DDS_N_PROGR,
trim(DDS_DDNAME) as DDS_DDNAME,
trim(DDS_DISP1) as DDS_DISP1

from re.bjdds as dds

fetch first 500 rows only
;
"""




print(in_sql)


cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF8;CURRENTSCHEMA=RE')
cursor = cnxn.cursor()


cursor.execute(in_sql)


while True:
    rows = cursor.fetchmany(100)
    if len(rows) == 0:
            break
        
    labels = [
'pos',
'dds_dsn',
'DDS_JOBNAME',
'DDS_STEP_PROGR',
'DDS_N_PROGR',
'DDS_DDNAME',
'DDS_DISP1'
        ]

    df = pd.DataFrame.from_records(rows, columns=labels)
        #print ( df )

cursor.close()

cnxn.close()

print ('DONE')