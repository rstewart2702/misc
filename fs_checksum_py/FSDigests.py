import os
import stat
import hashlib
import anydbm
import datetime
import threading

# The following module is needed to to properly handle Windows unicode-based
# file name strings.  We need a way to convert unicode strings into "standard"
# ASCII strings that can be used as keys into our associative array or hash file.
import codecs

class ActorObject(object):
    """Basic mechanism to calculate message digests, write them to an output file.

Base class which provides basic mechanisms to:
calculate a message digest,
write filename and message digest to a simple text file.
    """
    def __init__(self, fileName,mode):
        self.__initLocals__()
        self.__initFile__(fileName,mode)

    def __initLocals__(self):
        self.localFile = None
        self.mesgDigest = None
        self.computedDigest = None
        self.bufSize = 16384  # eventually want to expose this field as an "attribute
        
    def __initFile__(self,fileName,mode="w"):
        self.fileRef = open(fileName,mode,1)

    def setFile(self, fileRef):
        self.fileRef = fileRef

    def fileWriteAction(self, item):
        self.fileRef.write(item)
        #
        self.fileRef.write(";")
        self.fileRef.write(self.fileChkSum(item))
        #
        self.fileRef.write("\n")

    def finishFile(self):
        self.fileRef.flush()
        self.fileRef.close()

    def fileChkSum(self, item):
        """Calculates sha512 hexadecimal message digest string for a given file.

It may be possible to pass relative filenames to this method, but our habit
has been to pass in absolute filenames.
Calls to this method can be expensive, if the file in question is large.
A 3GB file takes about 1.5 to 2 minutes to process.
        """
        # print "Checksum for :%s"%item
        try:
            self.localFile = open(item,"rb",self.bufSize)
            self.mesgDigest = hashlib.sha512()
            # In an earlier version of this program, I had written:
            #   self.localBuf = self.localFile.read()
            # which will read in the ENTIRE FILE and store it in self.localBuf.
            # Which explains why I hit a "MemoryError" or some such, when
            # trying to calculate checksums for *everything* on my local drive?
            #
            self.localBuf = self.localFile.read(self.bufSize)
            while (self.localBuf):
                self.mesgDigest.update(self.localBuf)
                self.localBuf = self.localFile.read(self.bufSize)
            #
            # The client code requires a string representation of the calculated
            # message digest.
            self.computedDigest=self.mesgDigest.hexdigest()
            #
            self.mesgDigest=None # destroy the digest calculator?
            self.localFile.close()
            #
        except IOError as (errno, strerror):
            if errno == 13:
                self.computedDigest = "DENIED"
            elif errno == 22:
                self.computedDigest = "DENIED"
            elif errno == 2:
                self.computedDigest = "FILE NOT FOUND"
            else:
                # self.fileRef.flush()
                # self.fileRef.close()
                raise
        #        
        return self.computedDigest

class ActorObj2(ActorObject):
    """This is a version of the ActorObject which uses an associative array file, a hash file,
to store the results of calculating message digests.  The key to this file is the file's name.
"""
    # We shall not try to provide our own initialization, and let
    # the base class provide it instead.
    #
    # Other methods shall be overridden, as this class provides
    # a different implementation of the output file.
    def __initFile__(self,fileName,mode='c'):
        self.fileRef = anydbm.open(fileName,mode)
        print "ActorObj2.__initFile__:  opened file %s in mode \"%s\""%(fileName,mode)

    # We override the __initLocals__ method so that we can add in a
    # "field" or instance member that points to a useful decoder
    # needed so that unicode strings can be transformed into an ASCII
    # representation:
    def __initLocals__(self):
        # First, get the fields from the base class initialized:
        super(ActorObj2,self).__initLocals__()
        #
        # Next, initialize the special fields needed for this
        # particular kind of ActorObject, an ActorObj2:
        self.ucEncoder=codecs.getencoder("ascii")

    # We must also redefine the fileWriteAction:
    def fileWriteAction(self, item):
        # In this implementation, the fileRef refers to a db-hashfile.
        # Therefore, this expression stores, under the key which is
        # passed in parameter item, the computed checksum as a string,
        # using the method fileChkSum(), which is re-used from the
        # base class.
        #
        # We must do some fancy manipulation on the file names,
        # since, in Windows, we must use unicode file name paths,
        # and always use absolute filenames.
        # Therefore, paths always start with:
        #    \\?\
        # which forces windows to use long filename API, and prevents
        # the directory tree traversal from failing.
        try:
            (encodedName,nameLen) = \
                self.ucEncoder(item[4:],"backslashreplace")
            self.fileRef[encodedName] = self.fileChkSum(item)
        except: # Error as (errno, strerror):
#!            print str(item)
#!            print item
            self.finishFile()
            raise

    def finishFile(self):
        # Reimplementation of the checksum store closure method:
        self.fileRef.close()

class BkThread(threading.Thread):
    """This is an abstract base class, because it doesn't provide an implementation
of the run() method.  Descendant classes do.
"""
    def walkTree(self, dirName, itemAction):
        # This invokes a walkAction() method which much be defined in
        # a descendant class!
        locFname=''; # dirPath=''; dirs=None; files=None; name=''
        for dirPath, dirs, files in os.walk(dirName):
            for name in files:
                if self.isStopped():
                    break
                #
                locFname = u'\\'.join((dirPath,name))
                self.walkAction(locFname,itemAction)
            if self.isStopped():
                break

    def isStopped(self):
        self.stopLock.acquire()
        locStopped = self.stopWalking
        self.stopLock.release()
        #
        return locStopped

    def requestToStop(self):
        self.stopLock.acquire()
        self.stopWalking=True
        self.stopLock.release()

#!    def __init__(self,fileName,dirName,fgObject):
    def __init__(self,fileName,dirName,fgCall):
        super(BkThread,self).__init__()
        self.fileName=fileName
        self.dirName=dirName
        # fgObject is the "foreground object" which is the observer?
#!        self.fgObject=fgObject
        self.fgCall=fgCall
        # The stateDict is an associative array which is used to store
        # the state information local to this thread which will be interrogated
        # to "interested observers."
        self.stateDict={}
        #
        # This is a lock used to protect the "kill-switch" flag variable.
        # This kill-switch is used to tell the thread to stop walking
        # the file system tree (in the walkTree method...)
        self.stopLock = threading.Lock()
        self.stopWalking = False

    def _stateChange(self,newStates):
        self.stateDict.clear()
        for stateVal in newStates:
            self.stateDict[stateVal]=newStates[stateVal]
        # We assume that the fgObject.update() is designed to access
        # the self.stateDict, correct?
#!        self.fgObject.update()
        self.fgCall()
        # Now, presumably, the fgObject.update() will already know about
        # any communication data structures needed, etc.  This means that
        # we don't have to bury lots of unrelated functionality about
        # "interprocess communication" into these classes?


class BkDigestThread(BkThread):
    """Spawns a background thread, using a "foreground object" as an "observer."
"""
    def computeDigest(self, name, itemAction):
        locFname = u"\\".join((dirPath,name))
        #
        # The update method of the foreground object must
        # already know how to interrogate local state within the
        # objects managed by this thread in order to do its job.
        # And that update method is invoked by self._stateChange:
        self._stateChange( \
            dict(stateName="digestStarted",
                 fileName=locFname,
                 atTime=datetime.datetime.now())
            )
        try:
            itemAction.fileWriteAction(locFname)
        except Exception as actionException:
            self._stateChange( \
                dict(stateName="digestError",
                     fileName=locFname,
                     atTime=datetime.datetime.now(),
                     errorInfo=actionException.args)
                )
            raise actionException  # LEAVE THE LOOP.
        #
        self._stateChange( \
            dict(stateName="digestEnded",
                 fileName=locFname,
                 atTime=datetime.datetime.now())
            )

    def walkAction(self,name,itemAction):
        # This implements the walkAction method required by the base
        # class definition.
        self.computeDigest(name,itemAction)

    def run(self):
        # Must create the appropriate "actor" object, pointing it to
        # use the file named in self.fileName:
        locActionObj=ActorObj2(self.fileName,"w")
        # Must invoke the walkTree method using that object and
        # the directory specified in self.dirName:
        try:
            self.walkTree(self.dirName,locActionObj)
        except Exception as walkTreeExcep:
            raise walkTreeExcep # this should terminate the thread, right?



class CompareAgainst(ActorObj2):
    """Used to compare the value of the current message digest against that which
was stored earlier in the hash-file.
"""
##Don't know what costs so much here, yet, but checking an existing database's
##digests against computed digests from the same files in the filesystem is
##very slow, very expensive.
##
##Need to understand why.
##
##Could it be filesystem caching, or the lack thereof, biting me?
##Is it possible that, due to the "randomness" in the way that files
##are chosen by the hash-file key-iterator is working against us,
##by thwarting the "natural" read-ahead caching that the system
##tries to do?  Nothing is clear yet, only unproved conjectures.
##
##It would seem that when we traverse the filesystem in the order
##provided by the os.walk() method, then we can check a directory tree
##against a database in about the same amount of time that it cost to
##create the database of computed digests in the first place.
    def __init__(self,fileName,mode):
        super(CompareAgainst,self).__init__(fileName,mode)
        self.storedDigest=None

    def __initLocals__(self):
        super(CompareAgainst,self).__initLocals__()
        self.ucDecoder=codecs.getdecoder("unicode_escape")
        # ucEncoder field is already set by the base-class
        # initialization method, right?
        # self.ucEncoder=codecs.getencoder("ascii")
        
    def fileAction(self, item):
        try:
            # check the item against the checksum stored in the database file:
            self.storedDigest=self.fileRef[item]
            #
            # fileName=unicode("\\\\?\\"+item)
            # This expression converts the ascii string in item back into
            # a unicode filename, making sure that it begins with the
            #   \\?\
            # sequence so that Windows will know that it is a "generalized
            # unicode pathname" of "arbitrary length," and handle it correctly.
            # print "Filename before transformation:\n   %s"%item
            (fileName,nameLen) \
              = self.ucDecoder("".join(("\\\\\\\\?\\\\",item.replace("\\","\\\\"))))
            self.computedDigest=self.fileChkSum(fileName)
        except KeyError:
            # We've been asked to retrieve a digest for a file that
            # has not had a pre-computed digest created for it in the past.
            self.storedDigest="NOT PRESENT IN DATABASE"
            self.computedDigest="NO DIGEST CREATED"
            
    def checkFiles(self):
        for fileKey in self.fileRef.iterkeys():
            self.fileAction(fileKey)

    def fileWriteAction(self, item):
        """Overrides method from the base class in order to fiddle with file names
        and invoke the fileAction method."""
        (encodedName,nameLen) = \
            self.ucEncoder(item[4:],"backslashreplace")
        self.fileAction(encodedName)


class BkCompareThread(BkThread):
    def walkAction(self,name,itemAction):
        # This implements the walkAction method required by the base
        # class definition.
#!        print 'BkCompareThread.walkAction:\n  name:  %s\n'%(name)
        self.compStoredToPresent(name,itemAction)

    def compStoredToPresent(self,name,itemAction):
#!        locFname = u"\\".join((dirPath,name))
        locFname=name
        #
        # The update method of the foreground object must
        # already know how to interrogate local state within the
        # objects managed by this thread in order to do its job.
        # And that update method is invoked by self._stateChange:
        self._stateChange( \
            dict(stateName="compareStarted",
                 fileName=locFname,
                 atTime=datetime.datetime.now())
            )
        try:
            itemAction.fileWriteAction(locFname)
        except Exception as actionException:
            self._stateChange( \
                dict(stateName="compareError",
                     fileName=locFname,
                     atTime=datetime.datetime.now(),
                     errorInfo=actionException.args)
                )
            raise actionException  # LEAVE THE LOOP.
        #
        self._stateChange( \
            dict(stateName="compareEnded",
                 fileName=locFname,
                 atTime=datetime.datetime.now(),
                 storedDigest=itemAction.storedDigest,
                 computedDigest=itemAction.computedDigest)
            )

    def run(self):
        # locActorObj=CompareAgainst(self.fileName,"w")
        self._stateChange( \
            dict(stateName='traversalStarted' \
                 , atTime=datetime.datetime.now() \
                 )
            )
        myCA=CompareAgainst(self.fileName,'r')
#!        self.walkTree(self.dirName, CompareAgainst(self.fileName,'w'))
        self.walkTree(self.dirName, myCA)
        myCA.finishFile()
        #
        self._stateChange( \
            dict(stateName='traversalFinished' \
                 , atTime=datetime.datetime.now() \
                 )
            )
        self.requestToStop()
        print "Background: finished..."
##        try:
##            self.walkTree(self.dirName,CompareAgainst(self.fileName,"w"))
##        except Exception as walkTreeExcep:
##            raise walkTreeExcep
        
