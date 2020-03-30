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


"^(>[^\r\n]*).*?Length\s=\s(\d+)"
The first capturing group will match everything up to first line break after > 
(independently of your operating system). 
Then the .*? will match any characters until the first Length encountered. 

text = " asdfsad ; adddddd,  aaaa"

# "semicolon or (a comma followed by a space)"
pattern = re.compile(r";|, ")

# "(semicolon or a comma) followed by a space"
pattern = re.compile(r"[;,] ")

print (pattern.split(text))



s = '(twoplusthree)plusfour'
l = re.split(r"(plus|\(|\))", s)
a = [x for x in l if x != '']
print (a)

t1 = re.split(r"((?i)select|(?i)from)", str.strip(sql_base1),re.DOTALL)
t2 = [str.strip(x) for x in t1 if x != '']


t3x = re.split(r"(\n)", t2[1],re.DOTALL)

t3x = re.split(r"((?i)as|\.)", t2[1],re.DOTALL)

t3 = re.split(r"((?i)as|\n|\.|,)", t2[1],re.DOTALL)

#--------------------------
t1 = "" 
try:
    t1 = re.match(r"(?:.*(?i)select)(.*)(?:(?i)from)", sql_base1,re.DOTALL).group(1)
except (TypeError, AttributeError):
    t1 = ""
t1 = str.strip(t1) + ','

#split line  with new line  
t2 = re.findall(r"(?:\n)(.*)(?:,)", t1)


t3 = []

for x in t2:
    x1 = re.split(r"(?i)\sas\s",x)
    # as found if len == 2
    if len(x1) == 2 :
        t3.append(str.strip(x1[1]))
    # split with . 
    else:
        x2 = re.split(r"\.",x)
        # . found if len == 2
        if len(x2) == 2 : 
            t3.append(str.strip(x2[1]))
        # no . found keep all 
        else :
            t3.append(str.strip(x))






ttt = re.split('; |, |\*|\n',a)




yyy = re.findall(r"(?:^)(.*)(?:,)(.*)(?:$)", t2[2])  

#find if comma return 2 group if no comma return 1 group 
t3a = [re.findall(r"(?:^)(.*)(?:,)(.*)(?:$)", x) for x in t2 ]
t3b = [re.findall(r"(?:^)(.*)(?:$)", x) for x in t2 ]

t4 = []
i = 0
for x in t3a:
    if len(x) == 0 :
        t4.append(str.strip(t3b[i][0]))
    else:
        for y in t3a[i][0]:
            t4.append(str.strip(y))
    i = i + 1


t4a = [re.findall(r"(?:\.)(.*)(?:$)", x) for x in t4x ]
t4b = [re.findall(r"(?:(?i)as)(.*)(?:$)", x) for x in t4x ]

















