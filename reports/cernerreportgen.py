# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 20:42:39 2021
But finished on 9/29/2021

@author: Luke
"""

import re
import pandas as pd
from pathlib import Path
from tkinter import Tk , Canvas, PhotoImage    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, askdirectory

# make a cute picture!
root=Tk()
root.title("Cerner Report Default")
# display attributes
canvas=Canvas(root, width=256, height=256)
canvas.pack()
# import gif - doesnt animate yet
image=PhotoImage(file='C:/Users/Luke/OneDrive/Pictures/me/scigif/scienceloop.gif',format="gif -index 0")
canvas.create_image(0,0,anchor="nw",image=image)
#root.withdraw() # we don't want a full GUI, so keep the root window from appearing

# get input file manually through specification
infile = askopenfilename(title="Select Input File (Cerner Report)") # show an "Open" dialog box and return the path to the selected file
print(f'Infile: {infile}')

# get input file from folder in cwd (archived)
"""
#fullpath=r'C:/Users/cukel/OneDrive/Documents/PyScripts/jessie/cerner reports/'
# get infile
infiles   = os.listdir('input')
outfiles  = [os.path.splitext(infile)[0]+'.xlsx' for infile in infiles]
file_objs = [open('input/'+infile,'r') for infile in infiles]
"""

# if infile empty cancel the whole operation (archived, cancelling does the same thing)
# prevents any accidental operations (manual archiving)
"""
class Error(OSError):
    pass
if len(infile)==0:
    raise Error("No input files found in input folder")
"""
# remove old OUTPUTS into "old" folder (archived, this can be done manually)
"""
import shutil
    
source_dir = 'output'
target_dir = 'old'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    try:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        os.remove(os.path.join(source_dir, file_name))
"""

# recursively run it on each file (archived)
"""
#for ii in range(len(file_objs)):
    # extraction part
    #file_obj=file_objs[ii]
    #with file_obj as listfile:
"""

# Open file
file_obj = open(infile,'r')
listlines=file_obj.readlines()

# Define keywords
#listlines.append([""])# removes 'last entry' problem using nextline
output=[]
keys=['MRN/Age/Sex','Source','Collect Date','Accession','Panel', 'Name']
scriptdata=dict.fromkeys(keys)
lastline=''

# define stripper function
def linestripper(line):
    if line==[""]:
        return None
    # strips a line for useful information
    splitline_raw=re.split(': |   ',line)
    splitline=[i for i in splitline_raw if i] # remove none entries ("")
    splitline=[x.strip(" ") for x in splitline]
    return splitline

# Iterate over each line 
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

# ask for directory of output folder
out_location=askdirectory(initialdir=f"{Path(infile).parent}/output", 
                          title="Select Output Directory")

# format output into folder
out_filename = Path(infile).stem
out_df.to_excel(f"{out_location}/{out_filename}.xlsx")

# now remove old INPUTS into "old" folder (archived, can do manually)
"""
import shutil
    
source_dir = 'input'
target_dir = 'old'
    
file_names = os.listdir(source_dir)
    
for file_name in file_names:
    try:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        os.remove(os.path.join(source_dir, file_name))
"""

# destroy root window
#root.destroy()