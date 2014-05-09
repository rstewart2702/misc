# from Tkinter import *
# from Tkinter import ttk
import ttk
from ttk import *
from Tkinter import *

def calculate(*args):
    # global locText
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    # N.B. Python is dynamic, so locText is an object which will be
    # "looked up" in this procedure's local environment first, and
    # then in the enclosing "global" environment?  So, this code
    # "compiles," and then at execution time, it tries to locate
    # the locText object?
##    locText['state']='normal'
##    locText.insert('end','\nResult was calculated: %s'%meters.get())
##    locText.yview('end') # Guarantee that the user can always see the most
##                         # recently added text.
##    locText['state']='disabled'

# root = ttk.Tkinter.Tk()
root = Tk()
root.title("Feet to Meters")

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

feet=StringVar()
meters=StringVar()

feet_entry=Entry(mainframe,width=7,textvariable=feet)
feet_entry.grid(column=2,row=1,sticky=(W,E))

ttk.Label(mainframe,text="feet").grid(column=3, row=1, sticky=W)

ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)

innerPairFrame=ttk.Frame(mainframe)
innerPairFrame.grid(column=2,row=2,columnspan=3,sticky=(N,S,W,E))

##ttk.Label(innerPairFrame,
##          text="is equivalent to").grid(column=1, row=1, sticky=E)
ttk.Label(innerPairFrame,
          textvariable=meters).grid(column=1,row=1,sticky=E)
ttk.Label(innerPairFrame, text="meters").\
                     grid(column=2, row=1, sticky=W)
##ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
##ttk.Label(mainframe, textvariable=meters).grid(column=2,row=2,sticky=W)
##ttk.Label(mainframe, text="meters").\
##                     grid(column=2,columnspan=1, row=2, sticky=E,
##                          padx=(20,0))

##locButton=ttk.Button(mainframe, text="Calculate")
##locButton.grid(column=3, row=3, sticky=W)
##locButton['command']=calculate

##locText = Text(mainframe)
##locText.grid(column=2, row=4, sticky=E, columnspan=2)
# locText['state']='disabled'


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)
##locText.insert('end','Nothing calculated yet...')
##locText.yview('end')
##locText['state']='disabled'

root.mainloop()
