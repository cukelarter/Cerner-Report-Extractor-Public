# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 20:18:22 2022

@author: Luke
"""

# open necessary files
import pandas as pd
import glob

# labvantage output
df_lv = pd.read_excel(glob.glob('input/IDSample*.xlsx')[0])

# ID_Stevo Mapping
df_id = pd.read_excel(glob.glob('input/id *.xlsx')[0], names=['tube barcode'],header=None)

# normalize subject/tube mapping
df_id['tube barcode']=df_id['tube barcode'].str.lower()
df_lv['tube barcode']=df_lv['tube barcode'].str.lower()

# drop nan values
df_id=df_id.dropna()

# Inner join mapping on labvantage output.
df_mapped=pd.merge(df_id,df_lv, how='left')

#%% Remap to new header
columns={
    'tube barcode':'SampleID',
    'subject_id':'subject.id',
    'Collection Date':'datetime',
    'Identifier':'label',
    'Location':'location',
    }

df_mapped.rename(columns=columns, inplace=True)

#%% Format for output file
# split datetime
df_mapped[['date.collected','time.collected']] = df_mapped.datetime.astype(str).str.split(' ', expand=True)

# convert military time to AM/PM
timesplit=df_mapped['time.collected'].str.split(':', expand=True)

# retreive indices above PM mark (12 noon)
am_pm = ['' if type(h)!=type('') else 'AM' if int(h)<12 else 'PM' for h in timesplit[0]] # am/pm
timesplit[0] = [0 if type(h)!=type('') else int(h) if int(h)<=12 else int(h)-12 for h in timesplit[0]] # hour modifier

# insert datetime columns
df_mapped['time.collected']=timesplit.astype(str).agg(':'.join,axis=1) # rejoin as strings
df_mapped['AM/PM']=am_pm

# insert static columns
df_mapped['investigator']='Micheal David'
df_mapped['study']='ID_STEVO'
df_mapped['cd']='ctio'
df_mapped['status']='In Circulation'
df_mapped['host.species']='Human'
df_mapped['sample.type']='Cell Lysate'
df_mapped['parent.sample.type']='Microbial culture'
df_mapped['tube-barcode']=df_mapped['SampleID']
df_mapped['david.plate']=''

#%% Reorder to desired output
df_out = df_mapped[[
    'SampleID',
    'investigator',
    'study',
    'cd',
    'status',
    'host.species',
    'subject.id',
    'sample.type',
    'parent.sample.type',
    'date.collected',
    'time.collected',
    'AM/PM',
    'david.plate',
    'label',
    'location',
    'tube-barcode'
     ]]

#%% Export
df_out.to_excel('output/CHOP.xlsx', index=False)