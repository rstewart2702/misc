import ttk
from ttk import *
from Tkinter import *

import FSDigests
import Queue

class CompareApp(ttk.Frame):
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
        # Needed for "inter-thread communication" between this
        # "foreground" thread and the "background" thread which
        # is spawned by the startCompare method of this
        # class.
        # The queue is created *once*, in this initialization
        # method, because it is possible for multiple background
        # threads to exist and to be putting data into the queue:
        # self.resultsQueue=None
        self.resultsQueue=Queue.Queue(10000)
        #
        self.bkThreadFinished=False
        self.qFetches=0
        self.guiThreshold=500
        #

    def _startButtonToggle(self):
        self.startButtonStateCurr = (self.startButtonStateCurr + 1) % 2
        self.startButtonVar.set(self.startButtonStates[self.startButtonStateCurr])
        self.statusLabelStateCurr = (self.statusLabelStateCurr + 1) % 2
        self.statusLabelVar.set(self.statusLabelStates[self.statusLabelStateCurr])
        #
        if self.statusLabelStates[self.statusLabelStateCurr] == 'Running':
            if self.bkComparer == None or self.bkComparer.isStopped():
                self.bkThreadFinished=False  # The background processing has been started.
                self.startCompare()
                # Schedule the wretched foreground to check the queue periodically,
                # and execute the callbacks found there?
                # self.setupGUIPolling()
                self.fetchAndExec()
        #
        elif self.statusLabelStates[self.statusLabelStateCurr] == 'Stopped':
            self.bkThreadFinished=True
            self.bkComparer.requestToStop()
            # We no longer wish to schedule callbacks, right?
        #

    def startCompare(self):
        # We no longer create the commands-queue anew for each
        # call to this method.
        # self.resultsQueue=Queue.Queue(10000)
        #
        # This spawns an entirely new instance of a background thread
        # to try and traverse the filesystem and compare it against
        # the database of checksums.  It is possible for there to
        # be multiple other instances of such a thread, trying to
        # check against the database, and this present version of
        # the program will dutifully read all of the output such threads
        # cram into the queue, regardless of how many other threads
        # have been started afterwards.
        self.bkComparer = \
          FSDigests.BkCompareThread(
            fileName='big_listing.db',
            dirName=u'\\\\?\\c:\\scc\\Conversion_full\\Source\\com\\techrx\\app\\trexone',
            # This gives the background thread access to
            # the "update" method herein, which permits a
            # general mechanism to insert deferred gui calls
            # into a fifo queue.  N.B. This method is invoked
            # by the background thread, and should only access
            # members of the background thread object, yes?
            fgCall=self.compareUpdate
          )
        self.bkComparer.start()
            

    def fetchAndExec(self):
        """Fetches calls from the "command queue" and executes them to update the GUI.
Designed to be invoked by Tkinter on our behalf via scheduled calls."""
        # The idea here is that, once the background thread has finished,
        # there may still be results which must be fetched from the queue.
        # This is true even when the background thread was told to stop
        # before it finished.
        # Therefore, it shouldn't be necessary to schedule more calls if
        # the queue is empty.
        # 
        # Fetch reference to update procedure from the command queue, if there is
        # anything to fetch.  If there is not, we nonetheless wish to schedule
        # a call to this routine again.
        if self.resultsQueue.full():
            self.transcriptText['state']='normal'
            self.transcriptText.insert( \
                'end' \
                ,'UGH!!! Queue is full!!!!\n'
                )
            self.transcriptText.yview('end')
            self.transcriptText['state']='disabled'
        #
        if not self.resultsQueue.empty():
            callPair=self.resultsQueue.get(True,None)
            callPair[0](**callPair[1])
            self.qFetches=self.qFetches+1
            # We desire for the queue to be emptied before things
            # finish up, so schedule another call to this procedure:
            self.mainFrame.after(50,self.fetchAndExec)
        elif not self.bkComparer.isStopped():
            # If the queue is empty, and yet the background thread is
            # still at work, then we want to schedule another UI update:
            # pass
            self.mainFrame.after(50,self.fetchAndExec)
        elif self.bkComparer.isStopped() and not self.bkThreadFinished:
            # The background thread has reached a conclusion on its own,
            # without a user request to stop, so this program automatically
            # "toggles" the start button to appropriately update the GUI:
            self._startButtonToggle()
        elif self.bkThreadFinished:
            self.mainFrame.after(50,self.fetchAndExec)
        # Finally, schedule Tkinter to invoke this routine again.
        # self.mainFrame.after(50,self.fetchAndExec)

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
        self.innerFrame=ttk.Frame(self.mainFrame,width=80)
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
                                           # ,relief='groove' \
                                           # ,background='white' \
                                           ,textvariable=self.fileNameVar \
                                           ,anchor='w'\
                                           # ,width=20
                                           )
        self.fileNameResultLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame,width=80)
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
                                         # ,relief='groove' \
                                         ,anchor='w'
                                         )
        self.storedResultLabel.grid(row=0,column=1,sticky=(W,E))
        #
        ########################################################################################
        self.innerFrame=ttk.Frame(self.mainFrame,width=80)
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
                                         # ,relief='groove' \
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
        self.innerFrame=ttk.Frame(self.mainFrame,width=80)
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
                                         # ,relief='groove' \
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
        self.innerFrame=ttk.Frame(self.mainFrame,relief='groove',width=80)
        self.innerFrame.grid(row=5,column=0,columnspan=2,sticky=(N,S,E,W))
        self.transcriptText=Text(self.innerFrame \
                                 ,width=80 \
                                 ,height=20 \
                                 # ,relief='groove' \
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


    def locGUICompareStart(self,locFname):
#!        if self.qFetches % self.guiThreshold == 0:
#!            self.fileNameVar.set(locFname)
        self.fileNameVar.set(locFname)
    #
    def locGUICompareEnd(self,locFname,locCompDigest,locStoredDigest):
#!        if locStoredDigest == locCompDigest and self.qFetches % self.guiThreshold == 0:
        if locStoredDigest == locCompDigest:
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
##                self.transcriptText.insert( \
##                    'end' \
##                    ,''.join(('Compare attempted for '\
##                              ,self.fileNameVar.get() \
##                              ,'\n' \
##                              , '  FILE NOT PRESENT in filesystem or filesystem access DENIED or file is new.' \
##                              , '\n')) \
##                    )
                pass
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
            
    def locErrorOutput(self,locFname,locAtTime,locErrorInfo):
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

    def locTraversalStarted(self,locAtTime):
        self.transcriptText['state']='normal'
        self.transcriptText.insert( \
            'end' \
            ,''.join(('\n=======================\n' \
                      , 'Job Started at time:  ', str(locAtTime), '\n' \
                      ))
            )
        self.transcriptText.yview('end')
        self.transcriptText['state']='disabled'
        
    def locTraversalFinished(self,locAtTime):
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


    def compareUpdate(self):
        """General mechanism to update the GUI, as it is an observer.
Indended to be called by a background process."""
#!        print self.bkComparer.stateDict
        if self.bkComparer.stateDict['stateName']=='compareStarted':
            # Must create a local copy of the thread's state, as it will
            # be passed on to the foreground GUI's processing:
## Haw! For now I only want results passed on to the GUI when a difference is detected.
## It seems that the GUI spends an inordinate amount of time just fetching-and-updating,
## while the background thread races ahead of it?
## AND the dead giveaway of this reality was the fact that the wretched background
## thread generated a finishing timestamp which stated that it had finished processing
## about 45 minutes after the timestamp of the starting message timestamp.
## The lesson here is that if you have a buttload of information to propagate to
## a GUI, you'd better be prepared to wait for the GUI to finish updating.
##
## This also explained why I saw the disk i/o suddenly stop:  of course it stopped!
## The background thread had finished what it was doing!  Haw!  Poor old slow foreground
## GUI updater had not finished catching up by emptying out the message queue yet!
## Good grief.  So, we had a background thread finishing its work within about 45 minutes,
## and it took the foreground thread about another 180 minutes to work to empty the
## message queue and update the user interface.  That's just too slow.  The first thing
## to try is to force considerably less work down the poor GUI updater thread's throat
## by only inserting a message into the queue when a change in a file has been detected.
##            locFname=self.bkComparer.stateDict['fileName']
##            self.resultsQueue.put( \
##                (self.locGUICompareStart \
##                 ,{  'locFname' : self.bkComparer.stateDict['fileName'] }) \
##                ,True
##                ,None
##                )
            pass
        elif self.bkComparer.stateDict['stateName']=='compareEnded':
            if self.bkComparer.stateDict['storedDigest'] != \
               self.bkComparer.stateDict['computedDigest']    :
                self.resultsQueue.put( \
                    (self.locGUICompareEnd \
                     ,{  'locFname'        : self.bkComparer.stateDict['fileName'] \
                        ,'locStoredDigest' : self.bkComparer.stateDict['storedDigest'] \
                        ,'locCompDigest'   : self.bkComparer.stateDict['computedDigest'] }) \
                    ,True
                    ,None
                    )
        elif self.bkComparer.stateDict['stateName']=='compareError':
            # This is an error-condition which we'll handle, for now, by spitting
            # out an error message to the console:
            self.resultsQueue.put( \
                (self.locErrorOutput \
                 ,{  'locFname'     : self.bkComparer.stateDict['fileName'] \
                    ,'locAtTime'    : self.bkComparer.stateDict['atTime'] \
                    ,'locErrorInfo' : self.bkComparer.stateDict['errorInfo'] } ) \
                ,True
                ,None
                )
            #
        elif self.bkComparer.stateDict['stateName']=='traversalFinished':
            self.resultsQueue.put( \
                (self.locTraversalFinished \
                 , {  'locAtTime' : self.bkComparer.stateDict['atTime'] } ) \
                ,True
                ,None
                )
            #
        elif self.bkComparer.stateDict['stateName']=='traversalStarted':
            self.resultsQueue.put( \
                (self.locTraversalStarted \
                 , {  'locAtTime' : self.bkComparer.stateDict['atTime'] } ) \
                ,True
                ,None
                )


def testApplication():
    sys.setcheckinterval(200)
    root = Tk()
    app = CompareApp(master=root)
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

