# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyodbc

import pandas as pd

import os

import re

import win32com.client as win32

from functools import reduce

from pandas import ExcelWriter


sql_base1 = """
select  

LVD.LVD_PGMNAME ,
LVD.LVD_MAJORNAME ,
LVD.LVD_OFF ,  
LVD.LVD_STMT_OFF, LVD.LVD_NAME ,LVD.LVD_DCLLEVEL ,
LVD.LVD_TYPE ,
LVD_FULLNAME ,

LVA_SRC.LVA_PGMNAME 		as LVA_SRC_PGMNAME,
LVA_SRC.LVA_OFF 		as LVA_SRC_OFF,
LVA_SRC.LVA_SRC_DCLSTMTOFF ,
LVA_SRC.LVA_SRC_DCLDICTOFF ,
LVA_SRC.LVA_ASS_VALUE 		as LVA_SRC_ASS_VALUE,

LVS_SRC.LVS_PGMNAME as LVS_SRC_PGMNAME,
LVS_SRC.LVS_OFF as LVS_SRC_OFF,
LVS_SRC.LVS_NAME as LVS_SRC_NAME,
LVS_SRC.LVS_BUFF as LVS_SRC_BUFF,

LVA_TGT.LVA_PGMNAME 		as LVA_TGT_PGMNAME,
LVA_TGT.LVA_OFF 		as LVA_TGT_OFF,
LVA_TGT.LVA_TGT_DCLSTMTOFF as LVA_TGT_DCLSTMTOFF,
LVA_TGT.LVA_TGT_DCLDICTOFF as LVA_TGT_DCLDICTOFF,
LVA_TGT.LVA_ASS_VALUE 		as LVA_TGT_ASS_VALUE,

LVS_TGT.LVS_PGMNAME as LVS_TGT_PGMNAME,
LVS_TGT.LVS_OFF as LVS_TGT_OFF,
LVS_TGT.LVS_NAME as LVS_TGT_NAME,
LVS_TGT.LVS_BUFF as LVS_TGT_BUFF


from  

RE.BKLVDICT as LVD 

left outer join 
RE.BKLVASS as LVA_SRC
on (
LVD.LVD_PGMNAME = LVA_SRC.LVA_PGMNAME
and LVD.LVD_OFF = LVA_SRC.LVA_SRC_DCLDICTOFF
)

left outer join 
RE.BKLVSTMT as LVS_SRC
on (
LVA_SRC.LVA_PGMNAME = LVS_SRC.LVS_PGMNAME
and LVA_SRC.LVA_SRC_DCLSTMTOFF = LVS_SRC.LVS_OFF
)

left outer join 
RE.BKLVASS as LVA_TGT
on (
LVD.LVD_PGMNAME = LVA_TGT.LVA_PGMNAME
and LVD.LVD_OFF = LVA_TGT.LVA_TGT_DCLDICTOFF
)

left outer join 
RE.BKLVSTMT as LVS_TGT
on (
LVA_TGT.LVA_PGMNAME = LVS_TGT.LVS_PGMNAME
and LVA_TGT.LVA_TGT_DCLSTMTOFF = LVS_TGT.LVS_OFF
)


where
LVD.LVD_PGMNAME  = '#PGM#'
and LVD_MAJORNAME = '#RCDWA#'
;

"""


    
t1 = "" 
try:
    t1 = re.match(r"(?:.*(?i)select)(.*)(?:(?i)from)", sql_base1,re.DOTALL).group(1)
except (TypeError, AttributeError):
    t1 = ""
t1 = str.strip(t1) + ','

#split line  with new line  
t2 = re.findall(r"(?:\n)(.*)(?:,)", t1)

#split line  with comma
t3 = []
for x in t2:
    x1 = re.split(r",",x)
    for x2 in x1:
        t3.append(str.strip(x2))    

#split line  with as
t4 = []
for x in t3:
    x1 = re.split(r"(?i)\sas\s",x)
    #and as is found when == 2
    if len(x1) == 2:
        t4.append(str.strip(x1[1]))  
    else:
        #split line  with .  we use x1[0] since we didnt split with as
        x2 = re.split(r"\.",x1[0])
        if len(x2) == 2:
            t4.append(str.strip(x2[1]))   
        else:
            t4.append(str.strip(x2[0])) 

#xxx = ",\n".join(["\'" + x + "\'" for x in t4])


labels1 = t4    # this is a refernce not a copy 




labels2 = [
'LVS_OWNERPGM',
'LVS_NUM',
'LVS_OWNERLABELTYPE',
'LVS_OWNERLABEL',
'LVS_SUBTYPE',
'LVS_LEVEL',
'LVS_NAME',
'LVS_BUFF'
]

sql_base2 = "select \n" + ",\n".join(labels2) + """
from  RE.BKLVSTMT  
where
LVS_PGMNAME = '#PGM#'
;
"""



#taking jobiteration_expand_lv2.csv 
#read cobol SELECT and READ statement produced  in 1-cobolstmt_sql_to_csv  in df2
#merge expanded record and add the ddname and wkname
#merge expanded record and add the ddname and wkname
#lookup in the cobol statement (i.e LVS_BUFF) to get the instruction that refer to the found dictionary
#write the result in excel 
# df1_total contains the seed file headee  info
# df_out_final_reduce contains the mapping
# df_out2 contains all the source of the used programed 

excel = win32.gencache.EnsureDispatch('Excel.Application')

def get_ddname(x):
    words = x.split()
    for index, word in enumerate(words, start=0):   
        if re.match('ASSIGN',word):
            break
    # to access after ASSIGN TO we use +2
    # to access after ASSIGN   we use +1
    if words[index+1] == 'TO':
        word1s = words[index+2].split('-')  
    else:
        word1s = words[index+1].split('-')   
    # access last element from UT-S-xxx or xxx  or VSAM-xxx etc
    x = word1s[len(word1s) - 1]
    x = x.replace('.','')
    return(x)
'''    
def get_ddname_ind(x):
    words = x.split()
    for word in words:
        if re.match('UT-',word):
            break
    word1s = word.split('-')  
    x = word1s[0]
    return(x)
'''
def get_wkname(x):
    words = x.split()
    x = words[0]
    return(x)
    
def get_into_wk(x):
    fstr = ''
    words = x.split()
    for index, word in enumerate(words, start=0):   
        if re.match('INTO',word):
            fstr = words[index+1]
            break 
    if len(fstr) == 0:
        x = ''
    else :
        x = fstr
    return(x)
    
def test(n):
    r = n * 2
    return r    
    

def get_sql1(sql_file, pgm, rcdwa) :
    global labels1, sql_base1
    rt_sql = sql_base1.replace('#PGM#',pgm)
    rt_sql = rt_sql.replace('#RCDWA#',rcdwa) 
    return rt_sql 



def get_sql2(sql_file, pgm) :
    global labels2, sql_base2       
    rt_sql = sql_base2.replace('#PGM#',pgm)
    return rt_sql 


#-----------------------------------------------
#global variable
#-----------------------------------------------
path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"

labels1 = []
in_sql1_r = ''

labels2 = []
in_sql2_r = ''
 

in_file_desc = path+'jobiteration_expand_descending.csv'


in_file_asc = path+'jobiteration_expand_ascending.csv'
#-----------------------------------------------
#read expand produced in 3-jobiteration_csv_to_expand  in df1
#-----------------------------------------------

labelf1 = [ 
'seed',
'level',
'DSN_x',
'JOBNAME',
'STEP_PROGR',
'PGM_NAME_x',
'N_PROGR_x',
'DDNAME_x',
'DISP1_x',
'DSN_y',
'PGM_NAME_y',
'N_PROGR_y',
'DDNAME_y',
'DISP1_y'
]
dfx1 = pd.read_csv(in_file_desc)


#take PGM_NAME_x
#sort and get rid of duplicate 

#dfx1['PGM_NAME_x'] = dfx1['PGM_NAME_x'].apply(lambda x : str(x).strip())
#dfx1['DDS_DDNAME_x'] = dfx1['DDS_DDNAME_x'].apply(lambda x : str(x).strip())


dfx1 = dfx1.apply(lambda x: x.apply(lambda y: y.strip() if type(y) == type('') else y), axis=0)
dfx2 = dfx1[['PGM_NAME_x']]
dfx3  = dfx2[~dfx2['PGM_NAME_x'].str.contains(re.compile("(IEBGENER)|(IKJEFT01)|(SORT)|(SYNCGENR)"))] 
dfx3.drop_duplicates(inplace = True)
dfx4 = dfx3.sort_values( ['PGM_NAME_x']) 
dfx4.reset_index(inplace=True, drop=True) 





df_out2 = pd.DataFrame()

cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF9;CURRENTSCHEMA=RE')

#   
#for index, row in df2_read.iterrows():
for x in dfx4['PGM_NAME_x']:
    in_sql2 = get_sql2(sql_base2, x)
    cursor1 = cnxn.cursor()
    cursor1.execute(in_sql2)  
    rows1 = cursor1.fetchall()
    df_sql2 = pd.DataFrame.from_records(rows1, columns=labels1)
    df_out2 = pd.concat([df_out2, df_sql2])
    cursor1.close()






#-----------------------------------------------
#read cobol SELECT and READ statement produced  in 1-cobolstmt_sql_to_csv  in df2
#-----------------------------------------------
in_file2 = path+'cobolstmt_sql.csv'
dfx2t= pd.read_csv(in_file2)



in_sql = '''
select
LVS_OWNERPGM,
LVS_OWNERLABEL,
LVS_NAME,
LVS_BUFF
from  RE.BKLVSTMT  
where
(
(LVS_OWNERLABEL = 'FILE-CONTROL' and LVS_NAME = 'SELECT')
or  ( LVS_NAME = 'READ')
)

;
'''






#get SELECT and READ only for program in the iteration list 
df1_pgm_list = pd.DataFrame(list(df1['PGM_NAME_x'])).drop_duplicates()
dfx2 = dfx2t.loc[list(dfx2t['LVS_OWNERPGM'].isin(list(df1_pgm_list[0])))].copy()

#create select file and parse to get wknmae and ddname
df2_select = dfx2[ dfx2['LVS_NAME'] == 'SELECT' ].copy()
df2_select['wkname'] = df2_select['LVS_BUFF'].apply(get_wkname)
df2_select['f_ddname'] = df2_select['LVS_BUFF'].apply(get_ddname)
df2_select.sort_values( [ 'LVS_OWNERPGM', 'f_ddname'], inplace = True) 
df2_select.drop_duplicates(inplace = True)

#create read file and parse to get wkname and into_wk only showing records when into_wk is not null 
df2_read = dfx2[ dfx2['LVS_NAME'] == 'READ' ].copy()
df2_read['wkname'] = df2_read['LVS_BUFF'].apply(get_wkname)
df2_read['into_wk'] = df2_read['LVS_BUFF'].apply(get_into_wk)
df2_read = df2_read[['LVS_OWNERPGM'] + ['wkname'] +['into_wk']]
df2_read = df2_read[ df2_read['into_wk'] != '' ]
df2_read.sort_values( [ 'LVS_OWNERPGM', 'wkname'], inplace = True) 
df2_read.drop_duplicates(inplace = True)

#get the list of used pgm
df2_pgm_list = df2_read[['LVS_OWNERPGM']].copy()
df2_pgm_list.drop_duplicates(inplace = True)
#df2_pgm_chk = df2_pgm.values.tolist()



#-----------------------------------------------
#merge expanded record and add the ddname and wkname
#-----------------------------------------------
#if pgm in df1 and not in df2 :  means found in job iter expansion and not in select 
df1a = pd.merge(df1, df2_select,
              left_on=['PGM_NAME_x', 'DDS_DDNAME_x'],
              right_on=['LVS_OWNERPGM', 'f_ddname'],
              how='left')
df1a.sort_values( labelf1, inplace = True) 

df1_total = pd.merge(df1a, df2_read,
              left_on=['PGM_NAME_x', 'wkname'],
              right_on=['LVS_OWNERPGM', 'wkname'],
              how='left')
df1_total.sort_values( labelf1, inplace = True) 


#-----------------------------------------------
#merge expanded record and add the ddname and wkname
#-----------------------------------------------
df_out1 = pd.DataFrame()
df_out2 = pd.DataFrame()

#join BKLVDICT and BKLVASS and BKLVSTMT for the SRC and TRG dictionary


cnxn = pyodbc.connect('DSN=LOCDB2K;UID=CNDWLMM;PWD=LCJCMHF9;CURRENTSCHEMA=RE')

#   
#for index, row in df2_read.iterrows():
for index, row in df2_read.iterrows():
    print ( 'Reading df1 for: ', row['LVS_OWNERPGM'], row['into_wk'])
    in_sql1 = get_sql1(sql_base1, row['LVS_OWNERPGM'], row['into_wk'])
    cursor1 = cnxn.cursor()
    cursor1.execute(in_sql1)  
    rows1 = cursor1.fetchall()
    df_sql1 = pd.DataFrame.from_records(rows1, columns=labels1)
    df_out1 = pd.concat([df_out1, df_sql1])
    cursor1.close()
  
#
for index, row in df2_pgm_list.iterrows(): 
    print ( 'Reading df2 for: ', row['LVS_OWNERPGM'])    
    in_sql2 = get_sql2(sql_base2, row['LVS_OWNERPGM'])
    cursor2 = cnxn.cursor()
    cursor2.execute(in_sql2)  
    rows2 = cursor2.fetchall()
    df_sql2 = pd.DataFrame.from_records(rows2, columns=labels2)
    df_out2 = pd.concat([df_out2, df_sql2])
    cursor2.close()
  
cnxn.close()   

#sort cobol source file and strip field that will be used later in loogkup
df_out2.sort_values(      [
'LVS_OWNERPGM',
'LVS_NUM'
], 
inplace = True) 
df_out2['LVS_OWNERPGM'] = df_out2['LVS_OWNERPGM'].apply(lambda x : str(x).strip())

#sort cobol source file and strip field that will be used later in loogkup
df_out1.sort_values(      [
'LVD_PGMNAME',
'LVD_MAJORNAME',
'LVD_OFF'
], 
inplace = True) 
df_out1['LVD_NAME'] = df_out1['LVD_NAME'].apply(lambda x : str(x).strip())
df_out1['LVD_PGMNAME'] = df_out1['LVD_PGMNAME'].apply(lambda x : str(x).strip())

#df_out1_r will contain the record with association . we will process only those record in the cum_stm logic
df_out1_chk1 = list(df_out1['LVA_SRC_PGMNAME'].map(lambda x: not( x is None)) | df_out1['LVA_TGT_PGMNAME'].map(lambda x:  not (x is None)) ) 
df_out1_r = df_out1.loc[df_out1_chk1].copy()

#we keep the line with no association we will take them back after the cum_stn logic to have a full picture
df_out1_chk2 = list(df_out1['LVA_SRC_PGMNAME'].map(lambda x: x is None) & df_out1['LVA_TGT_PGMNAME'].map(lambda x:  x is None) ) 
df_out1_r2 = df_out1.loc[df_out1_chk2].copy()

df_out1_r = df_out1_r.reset_index(drop=True)
df_out1_r_ix = df_out1_r.index.tolist()




#-----------------------------------------------
#lookup in the cobol statement (i.e LVS_BUFF) to get the instruction that refer to the found dictionary
#-----------------------------------------------
accum = ''
def cum_stm(i):
    global df_out1_r,  df_out2,  accum
    
    accum = ''
    dw1 = df_out2[['LVS_OWNERPGM','LVS_NUM','LVS_BUFF','accum']]
    l1 = list(dw1['LVS_OWNERPGM'] == df_out1_r['LVD_PGMNAME'].loc[i])
    dw2 = dw1[l1]
    l2 = list(dw2['LVS_BUFF'].str.contains(df_out1_r['LVD_NAME'].loc[i], na=False, regex=True))
    dw3 = dw2 [l2]
    
    dfx1 = dw3['accum']
    if len(dw3) == 0:
        accum = ''
    else:
        accum = reduce((lambda x,y: x + '\n' + y), dfx1)
 
    print ( i )
    return accum


df_out2['accum'] = df_out2['LVS_NUM'].apply(lambda x : str(x) + '!') + df_out2['LVS_NAME'].apply(lambda x : x + '!!') + df_out2['LVS_BUFF'].apply(lambda x : x + '\n')

df_out_ix = list(map(lambda x: cum_stm(x), df_out1_r.index.tolist() ) ) 
s1 = pd.Series(df_out_ix, name='stmt')
df_out_final1 =  pd.concat([df_out1_r, s1], axis = 1,ignore_index=True)  

New_Labels=df_out1_r.columns.values.tolist()
New_Labels.append('stmt')
df_out_final1.columns = New_Labels


df_out2['acum1'] = df_out2['LVS_NUM'].apply(lambda x : str(x) + '!') + df_out2['LVS_NAME'].apply(lambda x : x + '!!') + df_out2['LVS_BUFF'].apply(lambda x : x + '\n')



df_out1_r2['stmt'] = ''
df_out_final = pd.concat([df_out_final1, df_out1_r2 ])
df_out_final.sort_values( [ 'LVD_PGMNAME', 'LVD_MAJORNAME', 'LVD_OFF'], inplace = True) 
df_out_final = df_out_final.reset_index(drop=True)

df_out_final_reduce = df_out_final[
['LVD_PGMNAME' ,
'LVD_MAJORNAME',
'LVD_OFF',  
'LVD_NAME',
'LVD.LVD_DCLLEVEL' ,
'LVD.LVD_TYPE' ,
'LVD.LVD_FULLNAME' ,
'LVA_SRC_ASS_VALUE',
'LVS_SRC_NAME',
'LVS_SRC_BUFF',
'LVA_TGT_ASS_VALUE',
'LVS_TGT_NAME',
'LVS_TGT_BUFF',
'stmt'
]]



#-----------------------------------------------
#write the result in excel 
# df1_total contains the seed file headee  info
# df_out_final_reduce contains the mapping
# df_out2 contains all the source of the used programed 
#-----------------------------------------------
 
out_file = path+'jobiteration_field_mapping.xlsx'
if os.path.exists(out_file):
    print ('removing :', out_file)
    os.remove(out_file)     


print( 'calling excel....')    
writer = pd.ExcelWriter('jobiteration_field_mapping.xlsx', engine='xlsxwriter')
print( 'calling excel........')   
df1_total.to_excel(writer, sheet_name='seed', index = False)
print( 'calling excel.............')   
df_out_final_reduce.to_excel(writer, sheet_name='mapping', index = False)
print( 'calling excel.................')   
df_out2.to_excel(writer, sheet_name='source', index = False)
print( 'calling excel...............................before write')   
writer.save()
print( 'calling excel...............................after write')  

'''
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(out_file)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()
'''

print ('DONE')
