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

