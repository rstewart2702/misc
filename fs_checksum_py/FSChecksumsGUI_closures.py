# from Tkinter import *
# from Tix import *
import ttk
from ttk import *
from Tkinter import *

import FSDigests
import Queue

class CompareWrapper(object):
    """Simple wrapper around a Frame so that a uniform interface is presented to the
background thread."""
    def __init__(self,frameObj):
        self.frameObj=frameObj
    def update(self):
        self.frameObj.compareUpdate()
    
class Application(ttk.Frame):
    """
    This is written as an "old-style" class
    """
    def __init__(self, master=None):
        # We have to use old-style super-class method invocation because
        # of the antiquated way in which the Tkinter GUI code was built.
        ttk.Frame.__init__(self, master)
        # super(Application,self).__init__(master)
        self.mainFrame=ttk.Frame(master,padding='3 3 12 12')
        self.mainFrame.grid(column=0,row=0\
                            ,sticky=(N,W,E,S)\
                            # , sticky=W\
                            )
        self.mainFrame.columnconfigure(0,weight=0)
        self.mainFrame.columnconfigure(1,weight=1)
        self.mainFrame.rowconfigure(0,weight=0)
        self.mainFrame.rowconfigure(1,weight=0)
        self.mainFrame.rowconfigure(2,weight=0)
        self.mainFrame.rowconfigure(3,weight=0)
        self.mainFrame.rowconfigure(4,weight=0)
        self.mainFrame.rowconfigure(5,weight=1)
        # self.mainFrame.rowconfigure(6,weight=1)
        #
        self.master=master
        self.master.rowconfigure(0,weight=1)
        self.master.columnconfigure(0,weight=1)
        self.master.grid()
        # self.pack()
        #
        ## For the startButton's states:
        self.startButtonStates = ['Start','Stop']
        self.startButtonStateCurr = 0
        self.statusLabelStates = ['Stopped','Running']
        self.statusLabelStateCurr = 0
        ##
        #
        self.createWidgets()
        self.bkComparer=None
        #
        self.resultsQueue=None
        #
        self.bkThreadFinished=True
        self.qFetches=0
        self.guiThreshold=500
        

    def _startButtonToggle(self):
        self.startButtonStateCurr = (self.startButtonStateCurr + 1) % 2
        self.startButtonVar.set(self.startButtonStates[self.startButtonStateCurr])
        self.statusLabelStateCurr = (self.statusLabelStateCurr + 1) % 2
        self.statusLabelVar.set(self.statusLabelStates[self.statusLabelStateCurr])
        #
        if self.statusLabelStates[self.statusLabelStateCurr] == 'Running':
            self.bkThreadFinished=False  # The background processing has been started.
            self.startCompare()
            # Schedule the wretched foreground to check the queue periodically,
            # and execute the callbacks found there?
            # self.setupGUIPolling()
            self.fetchAndExec()
        elif self.statusLabelStates[self.statusLabelStateCurr] == 'Stopped':
            self.bkThreadFinished=True
            # We no longer wish to schedule callbacks, right?
        #

    def createWidgets(self):
        ## self.upperFrame=ttk.Frame(self)
        ## self.upperFrame.pack({"side":"top","fill":"x"})
        # The mainFrame Frame should already exist, right?
        self.statusLabelVar=StringVar()
        self.statusLabelVar.set(self.statusLabelStates[self.statusLabelStateCurr])
        self.statusLabel=ttk.Label(self.mainFrame,textvariable=self.statusLabelVar)
        self.statusLabel.grid(row=0,column=0 \
                              , sticky=(W,E) \
                              #, anchor='w'
                              #, padx='0 15' \
                              )
        #
        self.startButtonVar=StringVar()
        self.startButtonVar.set(self.startButtonStates[self.startButtonStateCurr])
        self.startButton=ttk.Button(self.mainFrame,textvariable=self.startButtonVar)
        self.startButton.grid(row=0,column=1 \
                              ,sticky= W \
                              # , anchor='e'
                              )
        # self.startButton['command']=lambda : self._startButtonToggle()
        self.startButton['command']=self._startButtonToggle
        # Eventually, we must add in a command!
        # self.startButton['command']=
        #
        #########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame)
        self.innerFrame.grid(row=1,column=0 \
                              ,columnspan=2 \
                              ,sticky=(W,E,N,S) \
                              # ,sticky=E
                             )
        self.innerFrame.rowconfigure(0,weight=1)
        self.innerFrame.columnconfigure(0,weight=0)
        self.innerFrame.columnconfigure(1,weight=0)
        self.fileNameLabel=ttk.Label(self.innerFrame \
                                     ,text='File:' \
                                     ,width='10' \
                                     # ,relief='groove'
                                     # ,justify='right' \
                                     # ,anchor='nw' \
                                     , anchor='w'
                                     )
        self.fileNameLabel.grid(row=0,column=0 \
                                ,sticky=W \
                                # ,sticky=E
                                # ,padx='32pt 0pt' \
                                )
        self.fileNameVar=StringVar()
        self.fileNameVar.set('No File yet...')
        self.fileNameResultLabel=ttk.Label(self.innerFrame \
                                           ,relief='groove' \
                                           ,textvariable=self.fileNameVar \
                                           ,anchor='w'\
                                           # ,width=20
                                           )
        self.fileNameResultLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame)
        self.innerFrame.grid(row=2,column=0,columnspan=2 \
                             , sticky=(W,E,N,S) \
                             )
        self.innerFrame.rowconfigure(0,weight=1)
        self.innerFrame.columnconfigure(0,weight=0)
        self.innerFrame.columnconfigure(1,weight=0)
        self.storedLabel=ttk.Label(self.innerFrame \
                                   ,text='Stored:' \
                                   # ,justify='right' \
                                   ,anchor='w' \
                                   ,width='10' \
                                   )
        self.storedLabel.grid(row=0,column=0 \
                              ,sticky=W \
                              # ,padx='20pt 0pt' \
                              )
        self.storedVar=StringVar()
        self.storedVar.set('Nothing yet...')
        self.storedResultLabel=ttk.Label(self.innerFrame \
                                         ,textvariable=self.storedVar \
                                         ,relief='groove' \
                                         ,anchor='w'
                                         )
        self.storedResultLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame)
        self.innerFrame.grid(row=3,column=0,columnspan=2 \
                             , sticky=(W,E,N,S) \
                             )
        self.innerFrame.rowconfigure(0,weight=1)
        self.innerFrame.columnconfigure(0,weight=0)
        self.innerFrame.columnconfigure(1,weight=0)
        self.calculatedLabel=ttk.Label(self.innerFrame \
                                   ,text='Calculated:' \
                                   # ,justify='right' \
                                   ,anchor='w' \
                                   ,width='10' \
                                   )
        self.calculatedLabel.grid(row=0,column=0 \
                              ,sticky=W \
                              # ,padx='20pt 0pt' \
                              )
        self.calculatedVar=StringVar()
        self.calculatedVar.set('Nothing calculated yet.')
        self.calculatedResultLabel=ttk.Label(self.innerFrame \
                                         ,textvariable=self.calculatedVar \
                                         ,relief='groove' \
                                         ,anchor='w'
                                         )
        self.calculatedResultLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
##        self.calculatedLabel=ttk.Label(self.mainFrame,text='Calculated:')
##        self.calculatedLabel.grid(row=3,column=0,sticky=(W,E),padx='15pt 0pt')
##        self.calculatedVar=StringVar()
##        self.calculatedVar.set('Nothing Calculated yet.')
##        self.calculatedResultLabel=ttk.Label(self.mainFrame,textvariable=self.calculatedVar)
##        self.calculatedResultLabel.grid(row=3,column=1,sticky=(W,E))
        #
        #
        ########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame)
        self.innerFrame.grid(row=4,column=0,columnspan=2 \
                             , sticky=(W,E,N,S) \
                             )
        self.innerFrame.rowconfigure(0,weight=1)
        self.innerFrame.columnconfigure(0,weight=0)
        self.innerFrame.columnconfigure(1,weight=0)
        self.compareResultLabel=ttk.Label(self.innerFrame \
                                   ,text='Result:' \
                                   # ,justify='right' \
                                   ,anchor='w' \
                                   ,width='10' \
                                   )
        self.compareResultLabel.grid(row=0,column=0 \
                              ,sticky=W \
                              # ,padx='20pt 0pt' \
                              )
        self.compareResultOutVar=StringVar()
        self.compareResultOutVar.set('No result yet.')
        self.compareResultOutLabel=ttk.Label(self.innerFrame \
                                         ,textvariable=self.compareResultOutVar \
                                         ,relief='groove' \
                                         ,anchor='w'
                                         )
        self.compareResultOutLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
##        self.compareResultLabel=ttk.Label(self.mainFrame,text='Result:')
##        self.compareResultLabel.grid(row=4,column=0,sticky=W)
##        self.compareResultOutVar=StringVar()
##        self.compareResultOutLabel=ttk.Label(self.mainFrame,textvariable=self.compareResultOutVar)
##        self.compareResultOutLabel.grid(row=4,column=1,sticky=E)
        #
        self.innerFrame=ttk.Frame(self.mainFrame,relief='groove')
        self.innerFrame.grid(row=5,column=0,columnspan=2,sticky=(N,S,E,W))
        self.transcriptText=Text(self.innerFrame \
                                 ,width=40 \
                                 ,height=20 \
                                 ,relief='groove' \
                                 )
        # self.transcriptText['font']=ttk.TkTextFont
        self.innerFrame.rowconfigure(0,weight=1)
        self.innerFrame.columnconfigure(0,weight=1)
        self.transcriptText.grid(row=0 \
                                 ,column=0 \
                                 # ,columnspan=2 \
                                 ,sticky=(N,S,E,W) \
                                 )
        #
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx=3, pady=3)


    def startCompare(self):
        self.resultsQueue=Queue.Queue(10000)
        self.bkComparer = \
          FSDigests.BkCompareThread(
            fileName='big_listing.db',
            dirName=u'\\\\?\\c:\\scc\\Conversion_full',
            # This gives the background thread access to
            # the update() method herein, which permits a
            # general mechanism to insert deferred gui calls
            # into a fifo queue...
#!            fgObject=CompareWrapper(self)
            fgCall=self.compareUpdate
          )
        self.bkComparer.start()

    def compareUpdate(self):
        """General mechanism to update the GUI, as it is an observer.
Indended to be called by a background process."""
#!        print self.bkComparer.stateDict
        if self.bkComparer.stateDict['stateName']=='compareStarted':
            # Must create a local copy of the thread's state, as it will
            # be passed on to the foreground GUI's processing:
            locFname=self.bkComparer.stateDict['fileName']
            #
            # Define some sort of closure which will invoke
            # the GUI mutator method?
            def locGUICompareStart():
                # This copies what is stored in the background object's
                # stateDict (a dictionary) into items needed to update
                # the GUI:
##                self.fNameTextBox['text']=locFname
                if self.qFetches % self.guiThreshold == 0:
                    self.fileNameVar.set(locFname)
                # The following will not work properly, right?
                #   self.fNameTextBox['text']=self.bkComparer.stateDict['fileName']
                # It will not work because it will set the text to whatever
                #   self.bkComparer.stateDict['fileName']
                # is at the time the GUI gets around to invoking the
                # locGUIChange closure, and that is not necessarily the same thing
                # as what the background thread had stored into that part of the
                # state dictionary at the time the enclosing procedure, compareUpdate,
                # is invoked by the background thread.  Oh!  Complicated!
            #
            # The above "closure" must be placed into the queue, so that
            # the foreground GUI code may retrieve it and execute it later.
            # This call is designed to block the current thread of control
            # (assumed to be the background) until another thread frees up
            # some of the queue by consuming some of the data therein:
            self.resultsQueue.put(locGUICompareStart,True,None)
        elif self.bkComparer.stateDict['stateName']=='compareEnded':
            locFname=self.bkComparer.stateDict['fileName']
            locStoredDigest = self.bkComparer.stateDict['storedDigest']
            locCompDigest = self.bkComparer.stateDict['computedDigest']
            #
            def locGUICompareEnd():
                # Must do something with locFname, locStoredDigest, locCompDigest
                # which updates the user interface
##                self.fileNameVar.set(locFname)
##                self.storedVar.set(locStoredDigest)
##                self.calculatedVar.set(locCompDigest)
                #
                if locStoredDigest == locCompDigest and self.qFetches % self.guiThreshold == 0:
                    self.fileNameVar.set(locFname)
                    self.storedVar.set(locStoredDigest)
                    self.calculatedVar.set(locCompDigest)
                    self.compareResultOutVar.set('FILE IS THE SAME')
                elif locStoredDigest != locCompDigest:
                    self.fileNameVar.set(locFname)
                    self.storedVar.set(locStoredDigest)
                    self.calculatedVar.set(locCompDigest)
                    #
                    self.compareResultOutVar.set('FILE HAS CHANGED.')
                    #
                    self.transcriptText['state']='normal'
                    if locCompDigest == 'FILE NOT FOUND' or locCompDigest == 'DENIED' or locCompDigest == 'NO DIGEST CREATED':
                        self.transcriptText.insert( \
                            'end' \
                            ,''.join(('Compare attempted for '\
                                      ,self.fileNameVar.get() \
                                      ,'\n' \
                                      , '  FILE NOT PRESENT in filesystem or filesystem access DENIED or file is new.' \
                                      , '\n')) \
                            )
                    else:
                        self.transcriptText.insert( \
                            'end' \
                            ,''.join(('Finished comparing ' \
                                      ,self.fileNameVar.get() \
                                      ,'\n' \
                                      , '  ', self.compareResultOutVar.get(), '\n'))
                            )
                    self.transcriptText.yview('end')
                    self.transcriptText['state']='disabled'
#!                print 'locGUICompareEnd closure:'
#!                print 'locFname: %s\nlocStoredDigest: %s\nlocCompDigest: %s'% \
#!                      (locFname,locStoredDigest,locCompDigest)
                #
                # self._startButtonToggle()
            #
            self.resultsQueue.put(locGUICompareEnd,True,None)
        elif self.bkComparer.stateDict['stateName']=='compareError':
            # This is an error-condition which we'll handle, for now, by spitting
            # out an error message to the console:
            locFname=self.bkComparer.stateDict['fileName']
            locAtTime=self.bkComparer.stateDict['atTime']
            locErrorInfo=self.bkComparer.stateDict['errorInfo']
            #
            def locErrorOutput():
                self.transcriptText['state']='normal'
                self.transcriptText.insert( \
                    'end' \
                    ,''.join(('HIT AN ERROR!!!!\n' \
                              , 'File:  ', locFname, '\n' \
                              , 'At time:  ', locAtTime, '\n' \
                              , 'Error Info:  ', locErrorInfo, '\n\n' \
                              ))
                    )
                self.transcriptText.yview('end')
                self.transcriptText['state']='disabled'
            #
            self.resultsQueue.put(locErrorOutput,True,None)
            #
        elif self.bkComparer.stateDict['stateName']=='traversalFinished':
            locAtTime=self.bkComparer.stateDict['atTime']
            #
            def locTraversalFinished():
                self.transcriptText['state']='normal'
                self.transcriptText.insert( \
                    'end' \
                    ,''.join(('\n======================\n' \
                              , 'Job finished!!!!\n' \
                              , 'At time:  ', str(locAtTime), '\n' \
                              ))
                    )
                self.transcriptText.yview('end')
                self.transcriptText['state']='disabled'
            #
            self.resultsQueue.put(locTraversalFinished,True,None)
        elif self.bkComparer.stateDict['stateName']=='traversalStarted':
            locAtTime=self.bkComparer.stateDict['atTime']
            #
            def locTraversalStarted():
                self.transcriptText['state']='normal'
                self.transcriptText.insert( \
                    'end' \
                    ,''.join(('\n=======================\n' \
                              , 'Job Started at time:  ', str(locAtTime), '\n' \
                              ))
                    )
                self.transcriptText.yview('end')
                self.transcriptText['state']='disabled'
            #
            self.resultsQueue.put(locTraversalStarted,True,None)

    def fetchAndExec(self):
        """Fetches calls from the "command queue" and executes them to update the GUI.
Designed to be invoked by Tkinter on our behalf via scheduled calls."""
        # Fetch reference to update procedure from the command queue, if there is
        # anything to fetch.  If there is not, we nonetheless wish to schedule
        # a call to this routine again.
        if not self.resultsQueue.empty():
            callRef=self.resultsQueue.get(True,None)
            callRef()
            self.qFetches=self.qFetches+1
        # Finally, schedule Tkinter to invoke this routine again:
        self.mainFrame.after(50,self.fetchAndExec)


def testApplication():
    root = Tk()
    app = Application(master=root)
    # Got the idea for the next three calls directly from the
    # source code for Tkinter._test() procedure, the test procedure
    # of the Tkinter module.  It's a quick-and-dirty way to guarantee
    # that the new window shows up on top of all others.
    root.iconify()  # Shrink down to an icon?
    root.update()   # Go ahead and get Tk to execute the "iconfication" event?
    root.deiconify() # Tell Tk, really, to schedule a "deiconification" event?
    # 
    app.mainloop()   # Now that the mainloop is started, the "deiconification"
                     # will be executed eventually.
    #
    # Now the mainloop is finished and the "root" window may be destroyed:
    # root.destroy()

