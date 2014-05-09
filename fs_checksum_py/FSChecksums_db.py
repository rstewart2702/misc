import os
import stat
import hashlib
import anydbm
import datetime
import sqlite3

# The following module is needed to to properly handle Windows unicode-based
# file name strings.  We need a way to convert unicode strings into "standard"
# ASCII strings that can be used as keys into our associative array or hash file.
import codecs

"""
In order to compute checksums over an entire filesystem,
or over a filesystem tree, starting from a root directory,
we must recursively(?) traverse the filesystem tree.
"""

def try_to_dump():
    for item in (os.listdir("c:\\")):
        # print "%30s: %10s"%(item, stat.S_ISDIR(os.stat(item).st_mode))
        print "%30s:  %10s"%(item,
                             (os.path.isdir(item) and not os.path.islink(item)))
        # print "Is this the path to the file? %40s"%(os.path.abspath(item))
        # print 

def printAction(filename):
    print "%s"%(os.path.abspath(filename))


class digestStorage(object):
##This is intended to be an abstract base class.  Some expected methods are
##left for implementation by descendants in a class hierarchy.
##
##Manages storage for calculated file digest values.
##The intention is to store (filename, digest) pairs into an
##associative store.
##
##We have switched to a SQLite-based datastore, which is a kind
##of relational database engine.  This choice seems to be a less
##volatile pick than some of those hash-file storage libraries...
    def __init__(self, storeName,mode):
        self.__initLocals__()
        self.__initStore__(storeName,mode)

    def __initLocals__(self):
        self.localFile = None
        self.mesgDigest = None
        self.computedDigest = None
        self.bufSize = 16384  # eventually want to expose this field as an "attribute
        
##    def __initFile__(self,fileName,mode="w"):
##        self.fileRef = open(fileName,mode,1)

##    def setFile(self, fileRef):
##        self.fileRef = fileRef

##    def fileWriteAction(self, item):
##        self.fileRef.write(item)
##        #
##        self.fileRef.write(";")
##        self.fileRef.write(self.fileChkSum(item))
##        #
##        self.fileRef.write("\n")

##    def finishFile(self):
##        self.fileRef.flush()
##        self.fileRef.close()

    def fileChkSum(self, item):
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

class rdbmsDigestStorage(digestStorage):
    def __init__(self, storeName, mode):
        super(rdbmsDigestStorage,self).__init__(self,storeName,mode)

    def __initStore__(storeName, mode):
        # This is one of the abstracted methods, made concrete in this
        # class:
        self.lConn = sqlite3.connect(storeName)

    @staticmethod        
    def sqlite3Test():
        # Intended to be a "static method..."
        os.chdir(u"\\\\?\\c:\\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
        lConn = sqlite3.connect('fs_digests_container.db')
        lCur = lConn.cursor()
##        lCur.execute("create table if not exists file_digests(file_path text primary key, digest text)")
##        lCur.execute(\
##            """insert or replace into file_digests
##               values ('dummy_filename','DUMMY-DIGEST')
##            """ \
##            )
        lCur.execute("select count(*) from file_digests order by file_path")
        for lRow in lCur:
            print lRow
        #
        lCur.close()
        lConn.close()
        
class actorObj2(digestStorage):
    # We shall not try to provide our own initialization, and let
    # the base class provide it instead.
    #
    # Other methods shall be overridden, as this class provides
    # a different implementation of the output file.
    def __initFile__(self,fileName,mode='c'):
        self.fileRef = anydbm.open(fileName,mode)
        print "actorObj2.__initFile__:  opened file %s in mode \"%s\""%(fileName,mode)

    # We override the __initLocals__ method so that we can add in a
    # "field" or instance member that points to a useful decoder
    # needed so that unicode strings can be transformed into an ASCII
    # representation:
    def __initLocals__(self):
        # First, get the fields from the base class initialized:
        super(actorObj2,self).__initLocals__()
        #
        # Next, initialize the special fields needed for this
        # particular kind of actorObject, an actorObj2:
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
            # locItem=self.ucEncoder(item[4:])[0]
            # locItem=str(item)[4:]
            # self.fileRef[locItem] = self.fileChkSum(item)
##            self.fileRef[self.ucEncoder(item[4:],"backslashreplace")[0]] = self.fileChkSum(item)
            (encodedName,nameLen) = \
                self.ucEncoder(item[4:],"backslashreplace")
            self.fileRef[encodedName] = self.fileChkSum(item)
        except: # Error as (errno, strerror):
            print str(item)
            print item
            self.finishFile()
            raise

    def finishFile(self):
        # Reimplementation of the checksum store closure method:
        self.fileRef.close()

# def fileWriteAction(p_file, item):
#     p_file.write(os.path.abspath(p_file))

class CompareAgainst(actorObj2):
    """
Don't know what costs so much here, yet, but checking an existing database's
digests against computed digests from the same files in the filesystem is
very slow, very expensive.

Need to understand why.

Could it be filesystem caching, or the lack thereof, biting me?
Is it possible that, due to the "randomness" in the way that files
are chosen by the hash-file key-iterator is working against us,
by thwarting the "natural" read-ahead caching that the system
tries to do?  Nothing is clear yet, only unproved conjectures.

It would seem that when we traverse the filesystem in the order
provided by the os.walk() method, then we can check a directory tree
against a database in about the same amount of time that it cost to
create the database of computed digests in the first place.
    """
    def __init__(self,fileName,mode):
        super(CompareAgainst,self).__init__(fileName,mode)
        self.storedDigest=None

    def __initLocals__(self):
        super(CompareAgainst,self).__initLocals__()
        self.ucDecoder=codecs.getdecoder("unicode_escape")
        # self.ucEncoder=codecs.getencoder("ascii")
        
    def __initFile__(self,fileName,mode='r'):
        self.fileRef = anydbm.open(fileName,mode)
        print "Opened dbm file %s, mode %s"%(fileName,mode)

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
    ##        fileName=self.ucDecoder("\\\\\\\\?\\\\"+item.replace("\\","\\\\"))[0]
            (fileName,nameLen) \
              = self.ucDecoder("".join(("\\\\\\\\?\\\\",item.replace("\\","\\\\"))))
            # print "Trying to read:\n  %s"%fileName
            self.computedDigest=self.fileChkSum(fileName)
        except KeyError:
            # We've been asked to retrieve a digest for a file that
            # has not had a pre-computed digest created for it in the past.
            self.storedDigest="NOT PRESENT IN DATABASE"
            self.computedDigest="NO DIGEST CREATED"
        #
        if (self.storedDigest != self.computedDigest):
            print str(item)
            print "%7s:  %s"%("Earlier",self.storedDigest)
            print "%7s:  %s"%("Now",self.computedDigest)
            print
##        else:
##            print str(item)
##            print "SAME"
##            print
            
    def checkFiles(self):
        for fileKey in self.fileRef.iterkeys():
            self.fileAction(fileKey)

    def fileWriteAction(self, item):
        """Overrides method from the base class in order to fiddle with file names
        and invoke the fileAction method."""
        (encodedName,nameLen) = \
            self.ucEncoder(item[4:],"backslashreplace")
        self.fileAction(encodedName)
        

# l_file = open("file_listing.txt","wb",1)
# os.chdir("c:\\")
# os.chdir("c:\\Python26")

# walkTree("c:\\Python26",printAction)
# fileActionObj = actorObject("file_listing.txt")

def walkTree(dirName, itemAction):
    locFname=""
    for dirPath, dirs, files in os.walk(dirName):
        for name in files:
            locFname = u"\\".join((dirPath,name))
            # print locFname
            itemAction.fileWriteAction(locFname)

# One test case:  just put the checksums out to a plain text file:
def testCase1():
    # Much more primitive test case, less abstract.
    fileActionObj = actorObject("windows_listing.txt")
    walkTree("c:\\windows",fileActionObj)
    fileActionObj.finishFile()

def testCase(dirName,actionObj):
    # More abstract test-case driver, just expects an actionObj which has
    # finishFile, fileWriteAction methods...
    walkTree(dirName,actionObj)

def testRunPopulate(dirName,actionObj):
    startDT=datetime.datetime.now()
    print "%20s:  %20s"%("Started at:",str(startDT))
    # testCase(dirName,actionObj)
    walkTree(dirName,actionObj)
    timeDelta=datetime.datetime.now() - startDT
    print "%20s:  %20s"%("Finished at",str(datetime.datetime.now()))
    print "%20s:  %20s"%("Runtime",str(timeDelta))

def testPop1():
    # If we do it "unicode-style" maybe the long-filename support
    # will be used?
    # Plus, on Windows, when using long-filename support, all paths must
    # be absolute, or Windows will stubbornly refuse to find and open files
    # with extraordinarily long names.  Good grief.  What a hacked-up system.
    os.chdir(u"\\\\?\\c:\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    fileActionObj = actorObj2("big_listing.db","c")
      # "w" implies that the file must already exist.
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\Richard.Stewart\My Documents",fileActionObj)
    testRunPopulate(u"\\\\?\\c:\scc\Conversion_full",fileActionObj)
    fileActionObj.finishFile()

def testCompare():
    os.chdir(u"\\\\?\\c:\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    fileActionObj=CompareAgainst("big_listing.db","r")
    startDT=datetime.datetime.now()
    print "%20s:  %20s"%("Started at:",str(startDT))
    fileActionObj.checkFiles()
    timeDelta=datetime.datetime.now() - startDT
    print "%20s:  %20s"%("Finished at",str(datetime.datetime.now()))
    print "%20s:  %20s"%("Runtime",str(timeDelta))
    fileActionObj.finishFile()

def testPop2():
    os.chdir(u"\\\\?\\c:\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    fileActionObj=actorObj2("big_listing.db","w")
      # "w" implies that the file must already exist.
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\Richard.Stewart\Application Data",fileActionObj)
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\e3ccbry.NAMCK.000",fileActionObj)
    fileActionObj.finishFile()

def testPop3():
    os.chdir("c:\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    fileActionObj=actorObj2("big_listing.db","w")
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\e3ccbry.NAMCK.000",fileActionObj)
    fileActionObj.finishFile()

def testCompare2():
    os.chdir(u"\\\\?\\c:\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    fileActionObj=CompareAgainst("big_listing.db","r")
    startDT=datetime.datetime.now()
    print "%20s:  %20s"%("Started at:",str(startDT))
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\Richard.Stewart\Application Data",fileActionObj)
    # fileActionObj.checkFiles()
    timeDelta=datetime.datetime.now() - startDT
    print "%20s:  %20s"%("Finished at",str(datetime.datetime.now()))
    print "%20s:  %20s"%("Runtime",str(timeDelta))
    #   
    startDT=datetime.datetime.now()
    print "%20s:  %20s"%("Started at:",str(startDT))
    testRunPopulate(u"\\\\?\\c:\Documents and Settings\e3ccbry.NAMCK.000",fileActionObj)
    # fileActionObj.checkFiles()
    timeDelta=datetime.datetime.now() - startDT
    print "%20s:  %20s"%("Finished at",str(datetime.datetime.now()))
    print "%20s:  %20s"%("Runtime",str(timeDelta))
    #    
    fileActionObj.finishFile()

def testCompare3(filename,dirname):
    # os.chdir(dirname)
    fileActionObj=CompareAgainst(filename,"r")
    startDT=datetime.datetime.now()
##    print "%20s:  %20s"%("Started at:",str(startDT))
    testRunPopulate(dirname,fileActionObj)
    timeDelta=datetime.datetime.now() - startDT
##    print "%20s:  %20s"%("Finished at",str(datetime.datetime.now()))
##    print "%20s:  %20s"%("Runtime",str(timeDelta))
    #
    fileActionObj.finishFile()

def fileDirTally(filename,levels):
    """
    Tallies up the directories which have been examined to build the
    associative array/database-file, by trying to examine the keys,
    which are assumed to be "slash-separated" filesystem paths...
    """
    thisH=anydbm.open(filename,"r")
    tallyH=dict()
    # Derive the drive-letter plus the first three directories in the path, at the most.
    # I have to wonder how efficient this expression will really be, but, oh well...
    for filePath in thisH.iterkeys():
        pathKey = "\\".join(filePath.split("\\")[0:levels])
        tallyH[pathKey]=tallyH.get(pathKey,0) + 1
    thisH.close()
    #
    sortedKeys=tallyH.keys()
    sortedKeys.sort()
    for pathKey in sortedKeys:
        print "%-100s => %10d entries.\n"%(pathKey,tallyH[pathKey])

def sqlite3Test():
    os.chdir(u"\\\\?\\c:\\Documents and Settings\\Richard.Stewart\\My Documents\\Filesystem_checksum")
    lConn = sqlite3.connect('fs_digests_container.db')
    lCur = lConn.cursor()
    lCur.execute("create table if not exists file_digests(file_path text primary key, digest text)")
    lCur.execute("begin transaction")
    lCur.execute(\
        """insert or replace into file_digests
           values ('dummy_filename','DUMMY-DIGEST')
        """ \
        )
    # lCur.execute("commit")
    lConn.commit()
    lCur.close()
    #
    lCur.execute("select * from file_digests order by file_path")
    for lRow in lCur:
        print lRow
    #
    lCur.close()
    lConn.close()
    

# fileActionObj = actorObj2("windows_listing.db")
# fileActionObj = actorObj2("big_listing.db")
## fileActionObj = actorObj2("big_listing.db","w")

# os.chdir("c:\\Documents and Settings\\Richard.Stewart")

# os.chdir(u"\\\\?\\c:\Documents and Settings\Richard.Stewart")

# The following has already been done:
# testCase(u"\\\\?\\c:\Documents and Settings\Richard.Stewart\My Documents",fileActionObj)

# testCase(u"\\\\?\\c:\scc\Conversion_full",fileActionObj)
# testRunPopulate(u"\\\\?\\c:\Documents and Settings\\e3ccbry.NAMCK.000\\",fileActionObj)



"""
import os
import hashlib
m=hashlib.sha256()
f=open("c:\\Documents and Settings\\e3ccbry.NAMCK.000\\Local Settings\\Application Data\\Microsoft\\Outlook\\archive.pst","rb",65536)
buf=f.read(65536)
while (buf):
    m.update(buf)
    buf=f.read(65536)
"""

"""
Wanna build something that lets me send feedback to the foreground thread, right?
I want the background thread to be able to send messages to the foreground, and I don't want to be
forced to put all kinds of details into the background code that couples it to the way the foreground
code is written.

So, the background needs to be able to put its responses into a queue?  But those "responses" need to
be capsules of:
  procedure in the foreground which needs to be invoked,
  AND
  the arguments which need to be passed to that procedure?

Both of those things need to be packaged up into a single structure, object?
And that thing would be placed into a queue to be consumed by the foregound thread?

Ways to do this:
+ closure:  a def statement inside the background thread's code, using references to the
  foreground thread's objects through a reference passed into the background thread object
  when it was created by the foreground thread's object, right before the background thread
  gets launched...
+ "deferred procedure call":
  This is akin to the "closure" idea, except that we're not necessarily creating a new procedure
  at runtime (which means that the parser and compiler machinery won't be needed, and that
  dynamically created procedure objects won't be floating around, leaking memory, hopefully...)
  It will be cheaper to avoid creating new procedure bodies every time one wants the foreground
  thread to execute a change on its objects' internal state.
  Instead, we provide background with a reference to a foreground object which is able to either
  reach into background object state to get what it needs, or take parameter input from the
  background object, to create/generate "deferred-procedure-call" objects and put them into
  the queue.
  Then, the foreground objects periodically retrieve these deferred-procedure-calls from the
  queue to execute them:  these procedures make changes to foreground object state by a simple
  interface which is general and applicable to a wide variety of situations.
"""


'''
>>> import sqlite3
>>> conn = sqlite3.connect("fs_digests_container.db")
>>> \
  for f in os.listdir(os.getcwdu()):
	print f

big_listing.db
big_listing_bk.db
big_listing_flawed.db
file_listing.txt
file_listing_puked_early.txt
FSChecksums.py
FSChecksumsGUI.py
FSChecksumsGUI.pyc
FSChecksumsGUI.py~
FSChecksumsGUI2.rpj
FSChecksumsGUI_closures.py
FSDigests.py
FSDigests.pyc
FSDigests.py~
fs_digests_container.db
new_listing.db
run_transcript_20110915.txt
Tix_gui_test.py
ttk_tutorial_file1.py
windows_listing.db
windows_listing.txt
>>> c=conn.cursor()
>>> c.execute("""
create table file_digests (file_path varchar(2000), digest text);
"""
	  )
<sqlite3.Cursor object at 0x012D8950>
>>> c.execute("select * from file_digests")
<sqlite3.Cursor object at 0x012D8950>
>>> for row in c:
	print row

>>> c.execute("""drop table file_digests""")
<sqlite3.Cursor object at 0x012D8950>
>>> c.execute("""select * from file_digests""")

Traceback (most recent call last):
  File "<pyshell#42>", line 1, in <module>
    c.execute("""select * from file_digests""")
OperationalError: no such table: file_digests
>>> c.execute("""create table file_digests (file_path text primary key, digest text)""")
<sqlite3.Cursor object at 0x012D8950>
>>> c.execute("insert into file_digests values ('dummy_filename','DUMMY-DIGEST')")
<sqlite3.Cursor object at 0x012D8950>
>>> c.execute("select * from file_digests")
<sqlite3.Cursor object at 0x012D8950>
>>> for row in c:
	print row

(u'dummy_filename', u'DUMMY-DIGEST')
>>> c.close()
>>> conn.close()
'''
