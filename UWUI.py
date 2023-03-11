"""
Created on Sat Mar 11 15:01:22 2023

@author: Luke
Merge all ARIES functions into one executable file that has cute graphics.
"""

from pipelines import cerner,metadata,growthcurve
from tkinter import Tk, Canvas, PhotoImage, Button    # from tkinter import Tk for Python 3.x

# make a cute GUI!
class UWUI(object):
    def __init__(self, root):
        # make buttons for pipeline access
        self.button_cerner = Button(root,
                                    command=self.process_cerner, 
                                    text='Cerner Reports')
        self.button_cerner.pack(pady=10)
        self.button_metadata = Button(root,
                                    command=self.process_metadata, 
                                    text='Metadata')
        self.button_metadata.pack(pady=10)
        self.button_growthcurve = Button(root,
                                    command=self.process_growthcurve, 
                                    text='Growthcurve')
        self.button_growthcurve.pack(pady=10)
    # define functions for button presses
    def process_cerner(self):
        self.disable_buttons()
        # process report
        try:
            cerner.process()
        except:
            print('Error: Failed to process cerner.')
        # enable button presses
        self.enable_buttons()
    def process_metadata(self):
        self.disable_buttons()
        # process report
        try:
            metadata.process()
        except:
            print('Error: Failed to process metadata.')
        # enable button presses
        self.enable_buttons()
    def process_growthcurve(self):
        self.disable_buttons()
        # process report
        #try:
        growthcurve.process()
        #except:
        #print('Error: Failed to process growthcurve.')
        # enable button presses
        self.enable_buttons()
    # enable buttons
    def enable_buttons(self):
        # enable button presses
        self.button_cerner['state']="normal"
        self.button_metadata['state']="normal"

    # disable buttons
    def disable_buttons(self):
        # disable button presses
        self.button_cerner['state']="disabled"
        self.button_metadata['state']="disabled"

    # Animation sucks, I'm over it (archived)
    """
    # initialize frames
    def setup_gif(self):
        self.NFRAMES=6 # number of frames of 
        self.delay=5
        # initialize all photoimages
        self.frames=[PhotoImage(file=self.IMAGEFILE,format=f"gif -index {frameindex}") for frameindex in range(0,self.NFRAMES)]
        # set current index
        self.frameindex=0
        
    # update gif index
    def update_gif(self):
        if self.frameindex>5:
            self.frameindex=0
        else:
            self.frameindex+=1
        return self.frames[self.frameindex]
    """
#%% run it!

if __name__=="__main__":
    root=Tk()
    root.title("(✿◠‿◠)")
    # display attributes
    canvas=Canvas(root, width=256, height=256)
    # import static gif frame
    IMAGEFILE='src/scienceloop.gif'
    image=PhotoImage(file=IMAGEFILE,
                     format=f"gif -index 0")
    # create image on canvas? idk whatever
    canvas.create_image(0,0,anchor="nw",image=image)
    canvas.pack()
    # call app
    app=UWUI(root)
    # lock size
    root.resizable(False,False)
    # define main loop
    root.mainloop()
    