# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 20:42:39 2021
But finished on 9/29/2021

@author: Luke
"""

import re
import pandas as pd
import os

#fullpath=r'C:/Users/cukel/OneDrive/Documents/PyScripts/jessie/cerner reports/'

# get infile
infiles   = os.listdir('input')
outfiles  = [os.path.splitext(infile)[0]+'.xlsx' for infile in infiles]
file_objs = [open('input/'+infile,'r') for infile in infiles]

# if infile empty cancel the whole operation, to prevent
# file from getting lost in "old" if ran twice
class Error(OSError):
    pass
if len(infiles)==0:
    raise Error("No input files found in input folder")


# first remove old OUTPUTS into "old" folder
import shutil
    
source_dir = 'output'
target_dir = 'old'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    try:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        os.remove(os.path.join(source_dir, file_name))

# stripping
def linestripper(line):
    if line==[""]:
        return None
    # strips a line for useful information
    splitline_raw=re.split(': |   ',line)
    splitline=[i for i in splitline_raw if i] # remove none entries ("")
    splitline=[x.strip(" ") for x in splitline]
    return splitline

# recursively run it on each file
for ii in range(len(file_objs)):
    # extraction part
    file_obj=file_objs[ii]
    with file_obj as listfile:
        listlines=listfile.readlines()
        #listlines.append([""])# removes 'last entry' problem using nextline
        output=[]
        keys=['MRN/Age/Sex','Source','Collect Date','Accession','Panel', 'Name']
        scriptdata=dict.fromkeys(keys)
        lastline=''
        for lineno, line in enumerate(listlines):
            
            keysleft=[key for key in scriptdata.keys() if scriptdata[key]==None]
            splitline=linestripper(line)
            for key in keysleft:
                if key in splitline:
                    if key=='Panel':
                        scriptdata[key]=splitline[0]
                    else:
                        idx=splitline.index(key)
                        idx=idx+1
                        scriptdata[key]=splitline[idx]
            # set up a catch for nextline when lineno is too high
            if lineno+2>len(listlines):
                break
            nextline=listlines[lineno+1]
            # determine if the line is a continuation or a not by looking at next line
            if "===" in line and scriptdata['Name']!=None:
                if scriptdata['Name'] not in nextline:
                    output.append(scriptdata)
                    # enter it into the new dict
                    scriptdata=dict.fromkeys(keys)
            
            
            lastline=line
    
    # reformat and export
    out_df=pd.DataFrame(output)
    out_df=out_df.rename(columns={'Panel':'Result Date','Name':'Patient Name','MRN/Age/Sex':'MRN'})
    out_df['Site']='HUP'
    out_df['Location']=""
    out_df['Species']='MRSA'
    out_df['Sample Type']='bacterial isolate'
    out_df['Notes']=''
    
    out_df.to_excel('output/'+outfiles[ii])

# now remove old INPUTS into "old" folder
import shutil
    
source_dir = 'input'
target_dir = 'old'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    try:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        os.remove(os.path.join(source_dir, file_name))