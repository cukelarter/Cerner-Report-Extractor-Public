# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 22:55:24 2022

@author: cukelarter

Convert naming convention from plate reader into usable format.
Anyone who calls themself a data analyst should be able to do this.
Data sterilization and cleaning are critical in such a role.
But they can't, so now it's my problem.
"""

import glob
import pandas as pd
import numpy as np
import re
import os

def cleanfile(filename):
    """
    cleans the data as described
    first renaming will occur based on samples present in id
    pulling out the samples will be the trickiest part
    then we delete relevant cells and probably reindex
    A01-A04 CONTROl
    """
    # get sample list by separaors, cut off first and last
    samplenames=re.split('[,:(:)]{1}',filename)[1:-1]
    # set up array that will be used to set df column
    out=['CONTROL']*12
    # separate unique sample names
    for sample in samplenames:
        if '-' in sample:
            upper=sample[-1] # upper sample number
            lower=sample[-3] # lower sample number
            for i in range(int(lower),int(upper)+1):
                out=out+4*[sample[:-3]+str(i)]
        else:
            out=out+4*[sample]
    # import dataframe
    df = pd.read_excel(filename,header=10)
    # set specific rows to output
    df.loc[7:78,'Content']=out
    # get header and add to output
    dfh = pd.read_excel(filename,nrows=10,names=df.columns)
    # delete unwanted rows
    df=df.drop(df.index[79:97])
    df=df.drop(df.index[11:19])
    # merge header and file for output
    pd.concat([dfh,df]).to_excel('output/'+os.path.basename(filename),index=False,header=None)
    return None

if __name__=='__main__':
    filenames=glob.glob('input/*.xlsx')
    for file in filenames:
        print(f"Loading file: {file}")
        cleanfile(file)