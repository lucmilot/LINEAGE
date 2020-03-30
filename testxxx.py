# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 07:41:19 2018

@author: XT21586
"""
import re

sql_base1 = """
SELECT 

LVD.LVD_PGMNAME ,
LVD.LVD_MAJORNAME ,
LVD.LVD_OFF ,  
LVD.LVD_STMT_OFF, LVD.LVD_NAME ,
LVD.LVD_DCLLEVEL ,
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
LVA_TGT.LVA_TGT_DCLSTMTOFF as ,
LVA_TGT.LVA_TGT_DCLDICTOFF as ,
LVA_TGT.LVA_ASS_VALUE 		as LVA_TGT_ASS_VALUE,

LVS_TGT.LVS_PGMNAME as LVS_TGT_PGMNAME,
LVS_TGT.LVS_OFF as LVS_TGT_OFF,
LVS_TGT.LVS_NAME as LVS_TGT_NAME,
LVS_TGT.LVS_BUFF as LVS_TGT_BUFF


FROM

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

yyy = re.findall(r"(?:^)(.*)(?:,)(.*)(?:$)", t2[2])  

#find if comma return 2 group if no comma return 1 group 
t3a = [re.findall(r"(?:^)(.*)(?:,)(.*)(?:$)", x) for x in t2 ]
t3b = [re.findall(r"(?:^)(.*)(?:$)", x) for x in t2 ]

t4x = []
i = 0
for x in t3a:
    if len(x) == 0 :
        t4x.append(str.strip(t3b[i][0]))
    else:
        for y in t3a[i][0]:
            t4x.append(str.strip(y))
    i = i + 1


t4a = [re.findall(r"(?:\.)(.*)(?:$)", x) for x in t4x ]
t4b = [re.findall(r"(?:as)(.*)(?:$)", x) for x in t4x ]

















