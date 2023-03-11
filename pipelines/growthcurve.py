# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 22:55:24 2022

@author: cukelarter

Convert naming convention from plate reader into usable format.
Anyone who calls themself a data analyst should be able to do this.
Data sterilization and cleaning are critical in such a role.
But they can't, so now it's my problem.
"""

def process():
    import glob
    import pandas as pd
    import numpy as np
    import re
    import os
    from pathlib import Path
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
    
    # setup ui container
    root=Tk()
    root.withdraw() # we don't want to see root window

    # get input filepath manually through specification
    inpath = askdirectory(title="Select Project Directory (Growthcurve)") # show an "Open" dialog box and return the path to the selected file
    
    filenames=glob.glob(f'{inpath}/*.xlsx')

    def cleanfile(filename):
        """
        cleans the data as described
        first renaming will occur based on samples present in id
        pulling out the samples will be the trickiest part
        then we delete relevant cells and probably reindex
        A01-A04 CONTROl
        """
        sampleID=Path(filename).stem
        print(sampleID)
        # get sample list by separaors, cut off first and last
        samplenames=re.split('[,:(:)]{1}',sampleID)[1:-1]
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
        pd.concat([dfh,df]).to_excel(f'{Path(inpath).parent}/output/{sampleID}.xlsx',index=False,header=None)
        return None

    # iterate to clean files
    for file in filenames:
        cleanfile(file)