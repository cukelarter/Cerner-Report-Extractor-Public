# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 20:18:22 2022

@author: Luke
"""

# open necessary files
import pandas as pd
import glob
import itertools

# merge labvantage outputs
df_lv = pd.concat([pd.read_excel(lv_file) for lv_file in glob.glob('input/id*.xlsx')])

# ID Mapping
df_id = pd.read_excel(glob.glob('input/isolate*.xlsx')[0], names=['Sample'], header=None)

# sterilize subject/tube mapping
df_id['Sample'] = df_id['Sample'].str.upper()
df_lv['Sample'] = df_lv['Sample'].str.upper()

# drop nan values
df_id = df_id.dropna()

# Inner join mapping on labvantage output.
df_mapped = df_id.merge(df_lv, how='left', on='Sample')

print(len(df_mapped))

# %% Remap to new header
columns = {
    'Sample': 'SampleID',
    'Collection Date': 'datetime',
    'Identifier': 'label',
    'Location': 'location',
    'Study': 'project_name',
    'External Participant ID': 'subject_id'
}

df_mapped.rename(columns=columns, inplace=True)

# %% Format for output file
# split datetime
df_mapped[['date_collected', 'time_collected']] = df_mapped.datetime.astype(str).str.split(' ', expand=True)

# apply mask for ID_MRSA labels
mask0 = (df_mapped['project_name']=='ID_MRSA')
df_mapped.loc[mask0, 'label'] = df_mapped.loc[mask0, 'subject_id']

#df_mapped.mask(df_mapped.loc(['project_name']=='ID_MRSA',other=df_mapped['subject_id'])

# convert military time to AM/PM
# timesplit = df_mapped['time_collected'].str.split(':', expand=True)
# retreive indices above PM mark (12 noon)
# am_pm = ['' if type(h)!=type('') else 'AM' if int(h)<12 else 'PM' for h in timesplit[0]] # am/pm
# timesplit[0] = [0 if type(h)!=type('') else int(h) if int(h)<=12 else int(h)-12 for h in timesplit[0]] # hour modifier
# # insert datetime columns
# df_mapped['time_collected']=timesplit.astype(str).agg(':'.join,axis=1) # rejoin as strings
# df_mapped['AM/PM']=am_pm

# insert static columns
df_mapped['investigator'] = 'Micheal David'
df_mapped['tube_barcode'] = df_mapped['SampleID']
df_mapped['status'] = 'In Circulation'
df_mapped['host_species'] = 'Human'
df_mapped['sample_type'] = 'Microbial culture'
df_mapped['study_group'] = 'N/A'
df_mapped['current_antibiotics'] = 'N/A'
df_mapped['mouse_strain'] = 'N/A'
df_mapped['sex'] = 'N/A'
df_mapped['date_of_birth'] = 'N/A'
df_mapped['study_day'] = 'Day 0'

# generate static column for box positions (should be separate function?)
box_pos = []
for prefix in range(ord('A'), ord('J') + 1):
    # start at unicode for 'A' and go to 'J'
    max_position = 10 if prefix < ord('J') else 6
    # calculate box_position column
    box_pos = box_pos + [f'{chr(prefix)}{pos}' for pos in range(1, max_position + 1)]

# remove blanks (C3, G7)
box_pos.remove('C3')
box_pos.remove('G7')

# get initial box_id
id_init = int(input('Starts with box_id : '))
box_ids = []
for box_id in range(id_init, id_init + 4):
    # append box id according to number of positions
    box_ids = box_ids + [box_id] * len(box_pos)

# insert generated box id columns
df_mapped['box_id'] = box_ids
df_mapped['box_position'] = box_pos * 4

# %% Reorder to desired output
df_out = df_mapped[[
    'SampleID',
    'investigator',
    'project_name',
    'tube_barcode',
    'box_id',
    'box_position',
    'sample_type',
    'subject_id',
    'host_species',
    'study_day',
    'study_group',
    'current_antibiotics',
    'date_collected',
    'time_collected',
    'mouse_strain',
    'sex',
    'date_of_birth',
    'label'
]]

# %% Export
df_out.to_excel('output/CHOP.xlsx', index=False)
