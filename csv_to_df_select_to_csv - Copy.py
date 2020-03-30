# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

import os


path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")


in_file = path+'sql1_extract.csv'
out_file = path+'sql1_out1.csv'


if os.path.exists(out_file):
    os.remove(out_file)


labels = [
'xx',        
'DDS_DSN',
'DDS_DSN_X',           
'DDS_JOBNAME',
'DDS_STEP_PROGR',
'PGM_NAME',
'DDS_N_PROGR',
'DDS_DDNAME',
'DDS_DISP1'
        ]

print ( labels )
    
#df = pd.read_csv(in_file, names=labels, index_col=False )
df = pd.read_csv(in_file, names=labels )

#df.set_index('DDS_DSN_X', drop = False, inplace = True)



df_new = df[df.DDS_DISP1 == 'NEW']

df_notnew = df[df.DDS_DISP1 != 'NEW']


print ('DONE')