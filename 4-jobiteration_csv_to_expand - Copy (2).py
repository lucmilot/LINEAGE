# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd


import os

import win32com.client as win32


#taking the seed information from in_seed.csv
#with a n_limit = x  where x is the number of level that we go dons in the recursive tree
#we take the main info of job  and step from jobiteration_sql_job.csv and recursively build the lineage of steps. 

excel = win32.gencache.EnsureDispatch('Excel.Application')

path = "C:\\Users\\XT21586\\Documents\\document\\_DOSSET\\lineage\\"
#dirs = os.listdir( path )
#print(*dirs, sep="\n")

#>>>>>>>>>>>>>>>>>>>>>>>>
n_limit = 9


out_file_desc = path+'jobiteration_expand_descending.csv'
if os.path.exists(out_file_desc):
    os.remove(out_file_desc)

out_file_asc = path+'jobiteration_expand_ascending.csv'
if os.path.exists(out_file_asc):
    os.remove(out_file_asc)


in_file = path+'jobiteration_sql_job_trans.csv'
labels = [ 
'DSN',        
'JOBNAME',
'STEP_PROGR',
'PGM_NAME',
'N_PROGR',
'DDNAME',
'DISP1'
        ]

df = pd.read_csv(in_file, names=labels  , skiprows = 1)
#df = dfr.drop(columns = ['xx'],axis = 1)

#del dfr

df_not_new =  df[ (df['DISP1'] != 'NEW') & (df['DISP1'] != 'MOD') ]
df_new =  df[ (df['DISP1'] == 'NEW') | (df['DISP1'] == 'MOD') ]

seed_str = ''


      

#  keep end record and flag_end  --keep_end_rcd
def keep_end_nonend_rcd(act_flag,dfm,dfw2,seed_str):
    dfwx = pd.DataFrame()
    
    dfwx1 = dfw2[dfw2['JOBNAME'].str.match("NA")][['DSN']]
     
    if len(dfwx1) > 0 :       
        #   get then _y info from dfm that fits the DSN in dfwx, put it in _x and NA the _y 
        dfwx2 = pd.merge(dfm, dfwx1, 
          left_on=['DSN_y'],
          right_on=['DSN'],
          how='left' ,
          indicator=True)
        
        if act_flag == 'end':
            dfwx3  = dfwx2[dfwx2['_merge'].str.match("both")]
            dfwx  = dfwx3.drop(columns = ['_merge','DSN'])
            dfwx['seed'] = seed_str
            dfwx['level'] = str(n) + " - END"
        else :
            dfwx3  = dfwx2[~dfwx2['_merge'].str.match("both")]
            dfwx  = dfwx3.drop(columns = ['_merge','DSN'])
            dfwx['seed'] = seed_str
            dfwx['level'] = str(n)  
            
    else :
        if act_flag == 'nonend':
            dfwx  = dfm
            dfwx['seed'] = seed_str
            dfwx['level'] = str(n) 
        
    return dfwx
              
   
            

#---------------------------------------------------------------------------------
#df_in      : file wiht disp = new
#df_not_new : all dataset with disp <> new
#dfm        : we look in df_not_new to find the dataset that are source to the df_in, i.e disp = old or mod and on the same step
#lets do the search from disp = new  to  disp= shr or old  on the same jcl step  i.e. going backward i.e ascending
#disp= shr or old is the source file
#---------------------------------------------------------------------------------
def merge_asc(df_in):
    
    global seed_str, df_new, df_not_new, df_accum, n, n_limit

    #print ('TEST',seed_str,n)
    
    #when fiwt called df_accum need to be empty
    # and seed_str contains the seed 
    # n = 0 when first call
    
    # first time we search in the  new  with the seed
    if n == 0 :
        pattern = seed_str.replace('.','\.') 
        df1w = df_new[df_new['DSN'].str.match(pattern)]
        if len (df1w) == 0:
            # if the search is NO HIT we return df_accum empty
            df_accum = df1w
            return 
        else:
            # when HIT we call the merge with df1w containing records to merge with df_new
            # df_accum is still empty
            n += 1
            #df_accum['n'] = [n]
            merge_asc(df1w)
        
    else :
        #with the new file in df_in we search the in file (i.e with disp not_new )  on coresponding step      
        dfm_1 = pd.merge(df_in, df_not_new,
              left_on=['JOBNAME', 'STEP_PROGR'],
              right_on=['JOBNAME', 'STEP_PROGR'],
              #left_on=['JOBNAME', 'STEP_PROGR'],
              #right_on=['JOBNAME', 'STEP_PROGR'],
              how='left')        
        dfm_1 = dfm_1.fillna('')
        
        # if DSN_x already in df_accum we end the search passing comment 'ALREADY PROCESSED EARLIER'
        if len(df_accum) > 0 :
            # merege with indicator = true
            dfm_2 = pd.merge(dfm_1, df_accum,
                left_on=['DSN_x', 'JOBNAME', 'PGM_NAME_x'],
                right_on=['DSN_x', 'JOBNAME', 'PGM_NAME_x'],
                #left_on=['JOBNAME', 'STEP_PROGR'],
                #right_on=['JOBNAME', 'STEP_PROGR'],
                how='left',
                indicator=True)  
            
            # if not already found we pass it thru
            dfm_3  = dfm_2[~dfm_2['_merge'].str.match("both")]
            # keep only needed column 
            dfm = dfm_3[['DSN_x','JOBNAME','STEP_PROGR_x','PGM_NAME_x','N_PROGR_x_x','DDNAME_x_x','DISP1_x_x','DSN_y_x','PGM_NAME_y_x','N_PROGR_y_x','DDNAME_y_x','DISP1_y_x']]    
            # rename columns 
            dfm.columns = ['DSN_x','JOBNAME','STEP_PROGR','PGM_NAME_x','N_PROGR_x','DDNAME_x','DISP1_x','DSN_y','PGM_NAME_y','N_PROGR_y','DDNAME_y','DISP1_y']          

            # if already found we dont pass into the process but we flag 
            dfchk_1 = dfm_2[dfm_2['_merge'].str.match("both")]
            # keep only needed column 
            dfchk = dfchk_1[['DSN_x','JOBNAME','STEP_PROGR_x','PGM_NAME_x','N_PROGR_x_x','DDNAME_x_x','DISP1_x_x','DSN_y_x','PGM_NAME_y_x','N_PROGR_y_x','DDNAME_y_x','DISP1_y_x']]    
            # rename columns 
            dfchk.columns = ['DSN_x','JOBNAME','STEP_PROGR','PGM_NAME_x','N_PROGR_x','DDNAME_x','DISP1_x','DSN_y','PGM_NAME_y','N_PROGR_y','DDNAME_y','DISP1_y']          

            if len(dfchk) > 0 :
                dfchk['seed'] = seed_str
                dfchk['level'] = str(n) + ' - ALREADY PROCESSED EARLIER'
                df_accum = pd.concat([df_accum, dfchk])
            
        else :
            dfm = dfm_1        
        
           
        
        dfw = pd.DataFrame()
        
        if len (dfm) > 0 :

 
            # we get rid of record that have duplicate duplicate DSN_y
            dfm_dsn_y = dfm.drop_duplicates(['DSN_y'])
                 
            # find coresponding source dataset   (i.e looking in the dataset with new disp)   
            dfw1 = pd.merge(dfm_dsn_y, df_new, 
              left_on=['DSN_y'],
              right_on=['DSN'],
              how='left' )
            

            dfw2 = dfw1[['DSN_y','JOBNAME_y','STEP_PROGR_y','PGM_NAME','N_PROGR','DDNAME','DISP1']]
            dfw2.columns = ['DSN','JOBNAME','STEP_PROGR','PGM_NAME','N_PROGR','DDNAME','DISP1']

            dfw2 = dfw2.fillna('NA')
            
            dfw = dfw2[~dfw2['JOBNAME'].str.match("NA")]


            # accumulate tree info when NA found 
            
            
            
            #  keep end record and flag_end  --keep_end_rcd
            
            #  keep non end record  --keep_non_end_rcd
            
            #   to do  find all info in dfm with NA 
            '''
            dfwx1 = dfw2[dfw2['JOBNAME'].str.match("NA")][['DSN']]
            
            #   get then _y info from dfm that fits the DSN in dfwx, put it in _x and NA the _y 
            dfwx2 = pd.merge(dfm, dfwx1, 
              left_on=['DSN_Y'],
              right_on=['DSN'],
              how='left' ,
              indicator=True)
            
            dfwx3  = dfwx2[dfwx2['_merge'].str.match("both")]
            dfwx3 = dfwx3.drop(columns = ['_merge']
            dfwx  = dfwx3[level]
            
            dfwx ['seed'] = seed_str
            dfwx ['level'] = str(n) + "END"
            
            '''
            
            dfwx = pd.DataFrame()
            dfwx = keep_end_nonend_rcd('nonend',dfm,dfw2,seed_str)           
            if len(dfwx) > 0 :
                df_accum = pd.concat([df_accum, dfwx])    
                
            dfwx = pd.DataFrame()
            dfwx = keep_end_nonend_rcd('end',dfm,dfw2,seed_str)           
            if len(dfwx) > 0 :
                df_accum = pd.concat([df_accum, dfwx])
            
        
                        # accumulate tree info
            #df_accum = pd.concat([df_accum, dfm])
            
            # dont pass thru if NA found 
            
                    
    
        if len (dfw) == 0:
            return 
        else :
            # if some df1w entry are already in dfm dont process 
            #dfm = dfm[]
            #df1  = df1[~df1['PGM_NAME'].str.contains(re.compile('IDCAMS'))]  
            
            
            n += 1
            if n > n_limit :
                print ('n_limit ', n_limit, ' reached for : ' , seed_str )
                return
            else:
                merge_asc(dfw)
    
     


#---------------------------------------------------------------------------------
#lets do the search from disp= shr or old to disp = new i.e. going backward  i.e ascending 
#---------------------------------------------------------------------------------
def merge_desc(df_in):
    
    global seed_str, df_new, df_not_new, df_accum, n, n_limit

    #print ('TEST',seed_str,n)
    
    #when fiwt called df_accum need to be empty
    # and seed_str contains the seed 
    # n = 0 when first call
    
    # first time we search in the  not new  with the seed
    if n == 0 :
        pattern = seed_str.replace('.','\.') 
        df1w = df_not_new[df_not_new['DSN'].str.match(pattern)]
        if len (df1w) == 0:
            # if the search is NO HIT we return df_accum empty
            df_accum = df1w
            return 
        else:
            # when HIT we call the merge with df1w containing records to merge with df_new
            # df_accum is still empty
            n += 1
            #df_accum['n'] = [n]
            merge_desc(df1w)
        
    else :
        #with the not new file in df_in we search the out file (i.e with disp new)  on coresponding step 
        dfm = pd.merge(df_in, df_new,
              left_on=['JOBNAME', 'STEP_PROGR'],
              right_on=['JOBNAME', 'STEP_PROGR'],
              #left_on=['JOBNAME', 'STEP_PROGR'],
              #right_on=['JOBNAME', 'STEP_PROGR'],
              how='left')
        
        dfm = dfm.fillna('')
        
        
        '''        
        print (seed_str, n)
        print ('_dfm: ',dfm.shape)
        print ('_df_accum: ',df_accum.shape)
        print ('_dfm.columns: ',dfm.columns)
        print ('_df_accum.columns: ',df_accum.columns)
        '''
        
        df1w = pd.DataFrame()
        if len (dfm) > 0 :
            dfm['seed'] = seed_str
            dfm['level'] = str(n)
            df_accum = pd.concat([df_accum, dfm])

            # with the  new disp in _y we we search in the not_new
            for str1 in dfm['DSN_y']:
                
                if (len(str1) > 0):
                    pattern = str1.replace('.','\.') 
                    df_wrk = df_not_new[df_not_new['DSN'].str.match(pattern)]
                    df1w = pd.concat([df_wrk, df1w])
                    print ( 'tata')
    
        if len (df1w) == 0:
            return 
        else :
            n += 1
            if n > n_limit :
                print ('n_limit ', n_limit, ' reached for : ' , seed_str )
                return
            else:
                merge_desc(df1w)
    


#----------
                         
in_seed = path+'in_seed.csv'
wb1 = excel.Workbooks.Open(in_seed)


excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()  

input("Save Excel and quit excel before pressing enter? ") 

labels = [
'selection',
'seed'
]
df_seed = pd.read_csv(in_seed , names=labels , skiprows = 1)



#-------------------------------------------------------------------------------------------------------------------
#lets do the search from disp = new  to  disp= shr or old  on the same jcl step  i.e. going backward i.e ascending
#-------------------------------------------------------------------------------------------------------------------

df_accum_tot = pd.DataFrame()

for row in df_seed.itertuples():
    if row.selection == 'x':
        n = 0
        seed_str = row.seed
        df_in = pd.DataFrame()
        df_accum = pd.DataFrame()
        merge_asc(df_in)
        if len(df_accum) > 0:
            df_accum_tot = pd.concat([df_accum_tot, df_accum])
 
        print (seed_str, 'n=: ',n - 1, df_accum_tot.shape)

    else :
        print ('x:',seed_str)



df_accum_tot = df_accum_tot[['seed'] + ['level'] + df_accum_tot.columns[:-2].tolist()]
df_accum_tot.to_csv(out_file_desc, index = False)
print (df_accum_tot.head())


wb = excel.Workbooks.Open(out_file_desc)


excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()


#-------------------------------------------------------------------------------------------------------------------
#lets do the search from shr ord old to new     i.e. going bacward  i.e ascending 
#-------------------------------------------------------------------------------------------------------------------
# filex  shr
'''
df_accum_tot = pd.DataFrame()

for row in df_seed.itertuples():
    if row.selection == 'x':
        n = 0
        seed_str = row.seed
        df_in = pd.DataFrame()
        df_accum = pd.DataFrame()
        #merge_desc(df_in)
        if len(df_accum) > 0:
            df_accum_tot = pd.concat([df_accum_tot, df_accum])
 
        print (seed_str, 'n=: ',n - 1, df_accum_tot.shape)

    else :
        print ('x:',seed_str)



df_accum_tot = df_accum_tot[['seed'] + ['level'] + df_accum_tot.columns[:-2].tolist()]
df_accum_tot.to_csv(out_file_asc, index = False)
print (df_accum_tot.head())


wb = excel.Workbooks.Open(out_file_asc)
excel.Visible = True
excel.ActiveSheet.Columns.AutoFit()

'''



print ('DONE ')
