import os, sys, urllib2, cookielib, re, threading, socket, time
import xbmcgui
#import urllib

#===============================================================================
class UriHandler:
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.uriOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        
        # change the user agent (thanks to VincePirez @ xbmc forums)
        self.user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6 Alexa Toolbar"
        self.uriOpener.addheaders = [('User-Agent', self.user_agent)]
        
        self.defaultLocation = config.cacheDir
        self.pbAnimation = ["-","\\","|","/"]
        self.blockSize = (1024/4)#*8
        self.bytesToMB = 1048576
        self.inValidCharacters = "[^a-zA-Z0-9!#$%&'()-.@\[\]^_`{}]"
        xbmc.output("UriHandler initialised")
        self.timerTimeOut = 2.0                     # used for the emergency canceler
        
        self.webTimeOutInterval = config.webTimeOut # max duration of request
        self.pollInterval = 0.1                     # time between polling of activity
                
    #===============================================================================
    def Download(self, uri, filename, folder="", pb=True ,params=""):    
        # assign things (PERHAPS CHECK FIRST IF NOT ASSIGNED)
        
        pbEnabled = pb
        pbTitle = ""
        pbLine1 = ""
        pbLine2 = ""
        if pbEnabled:
            uriPB = xbmcgui.DialogProgress()
        
        cancelled = False
        
        destFilename = self.CorrectFileName(filename)
        destFolder = folder
        
        blockMultiplier = 16*8 #to increase blockSize
                    
        # if no destination is given, get one via a dialog box
        if destFolder=="":
            dialog = xbmcgui.Dialog()
            destFolder = dialog.browse(3, 'Select download destination', 'files', '', False, False, self.defaultLocation)
        
        destComplete = os.path.join(destFolder, destFilename)    
                
        xbmc.output('Creating Downloader for url: %s. And filename %s.', uri, destComplete)
        try:
            #create progress dialog
            if pbEnabled:
                pbTitle = 'Downloading the requested url'
                pbLine1 = uri
                uriPB.create(pbTitle, pbLine1)
            if params == "":
                sourceHandle = self.uriOpener.open(uri)
            else:
                sourceHandle = self.uriOpener.open(uri, params)                
            destHandle = open(destComplete, 'wb')
            headers = sourceHandle.info()
        
            fileSize = -1
            read = 0
            blocknum = 0
            
            if "content-length" in headers:
                fileSize = int(headers["Content-Length"])
                
            while 1:
                block = sourceHandle.read(self.blockSize*blockMultiplier)
                if block == "":
                    break
                read += len(block)
                destHandle.write(block)
                blocknum += 1
                
                if pbEnabled:
                    cancelled = self.PBHandler(blocknum, self.blockSize*blockMultiplier, fileSize, uriPB, pbLine1, pbLine2)
                    #check to see if cancelled
                    if cancelled:
                        break

            # clean up things
            sourceHandle.close()
            destHandle.close()
            
            if pbEnabled:
                uriPB.close()
            
            # delete parts if cancelled
            if cancelled:
                if os.path.exists(destComplete):
                    os.remove(destComplete)
                xbmc.output("Download Cancelled")
                rtrn = ""
            else:
                xbmc.output("Url %s downloaded succesfully.", uri)
                rtrn = destComplete
                
            return rtrn
            
        except:
            xbmc.output("Error caching file",exc_info=True)
            if os.path.exists(destComplete):
                os.remove(destComplete)
            if pbEnabled:
                uriPB.close()
            
            try:
                sourceHandle.close()
            except UnboundLocalError:
                pass
            try:
                destHandle.close()
            except UnboundLocalError:
                pass
            
            return ""

    #===============================================================================
    def Open(self, uri, pb=True, params=""):
        """
        Open an URL Async using a thread
        """
        try:
            
            progressbarEnabled = pb
            parameters = params
            targetUrl = uri
            pbTitle = ''
            pbLine1 = ''
            pbLine2 = ''
            blocks = 0
            filesize = 0
            canceled = False
            timeOut = False
            
            xbmc.output("Opening requested uri Async: %s (already %s threads)", targetUrl, threading.activeCount())
                    
            if progressbarEnabled:
                pbTitle = 'Opening request url'
                pbLine1 = targetUrl
                uriPB = xbmcgui.DialogProgress()
                uriPB.create(pbTitle, pbLine1)

            # set the start time in seconds
            startTime = time.time()
            
            openThread = AsyncOpener(targetUrl, self.uriOpener, self.blockSize, action='open',  params=parameters)
            openThread.start()
            #time.sleep(0.1)
            
            count = 0
            while not openThread.isCompleted and not canceled:
                if progressbarEnabled:
                    blocks = openThread.blocksRead
                    filesize = openThread.fileSize
                    #xbmc.output("%s van %s", blocks, filesize)
                    canceled = self.PBHandler(blocks, self.blockSize, filesize, uriPB, pbLine1, pbLine2)                          
                
                count += 1
                openThread.join(self.pollInterval)
                
                # the join call should block the calling method for the interval. No sleep needed.
                #time.sleep(self.pollInterval)                
                
                if time.time() > startTime + self.webTimeOutInterval:
                #if self.pollInterval * count > self.webTimeOutInterval:
                    timeOut = True
                    break                
            
            # we are finished now
            if progressbarEnabled:
                uriPB.update(100, pbLine1 ,pbLine2)
                uriPB.close()
            
            if canceled:                
                xbmc.output("Opening of %s was cancelled", targetUrl)
                data = ""
            if timeOut:
                xbmc.output("The URL lookup did not respond within the TimeOut (%s s)", self.webTimeOutInterval)
                data = ""
            else:
                xbmc.output("Url %s was opened successfully", targetUrl)                            
                data = openThread.data
            return data
        except:
            if progressbarEnabled:
                uriPB.close()
            
            xbmc.output("Error in threading", exc_info=True)
            return ""
        
    #===============================================================================
    def OpenSeq(self, uri, pb=True, params=""):
        raise DeprecationWarning() 
        # assign things (PERHAPS CHECK FIRST IF NOT ASSIGNED)
        pbEnabled = pb
        pbTitle = ""
        pbLine1 = ""
        pbLine2 = ""
        if pbEnabled:
            uriPB = xbmcgui.DialogProgress()
            #enable the timer for emergency canceling. Checks every 2 seconds
            self.PBEmergencyCanceler(pb=uriPB)
        
        cancelled = False
        
        try:
            xbmc.output("Opening requested uri: %s", uri)
            #xbmc.output("Number of open threads %s", threading.activeCount())
            if pbEnabled:
                pbTitle = 'Opening request url'
                pbLine1 = uri
                uriPB.create(pbTitle, pbLine1)
        
            # Check for posts
            if params=='':
                sourceHandle = self.uriOpener.open(uri)
            else:
                sourceHandle = self.uriOpener.open(uri, params)
            
            xbmc.output("Determining which Progessbar to use....")
            data = sourceHandle.info()
            
            if data.get('Content-length'):
                fileSize = int(data.get('Content-length'))
                xbmc.output('Using Calculated Progressbar (fileSize=' + str(fileSize) +')')
            else:
                fileSize = -1
                xbmc.output('Using Non-Calculated Progressbar')
            
            read = 0
            blocknum = 0
            data = ''
            
            while 1:
                block = sourceHandle.read(self.blockSize)
                if block == "":
                    break
                read += len(block)
                data = data + block
                blocknum += 1
                
                if pbEnabled:
                    cancelled = self.PBHandler(blocknum, self.blockSize, fileSize, uriPB, pbLine1, pbLine2)
                    #check to see if cancelled
                    if cancelled:
                        break

            if pbEnabled:
                uriPB.close()
                try:
                    self.timerUpDown.cancel()
                except:
                    # no timer exists
                    pass
                
            sourceHandle.close()
            
            if cancelled:
                xbmc.output("Opening of %s was cancelled", uri)
            else:
                xbmc.output("Url %s was opened successfully", uri)
            
            return data
        except:
            xbmc.output("Error Opening url %s", uri, exc_info=True)
            if pbEnabled:
                uriPB.close()
                self.timerUpDown.cancel()
            try:
                sourceHandle.close()
            except UnboundLocalError:
                pass
            
            return ""
        
    #===============================================================================
    def Header(self, uri, params=""):
        xbmc.output("Retreiving Header info for %s", uri)
        #uri = uri
        #params = params
                
        try:
            if params == "":
                uriHandle = self.uriOpener.open(uri)
            else:
                uriHandle = self.uriOpener.open(uri, params)
            
            data = uriHandle.info()
            realUrl = uriHandle.geturl()
            #xbmc.output(data)
            data = data.get('Content-Type')
            uriHandle.close()
            xbmc.output("Header info retreived: %s for realUrl %s", data, realUrl)
            return (data, realUrl)
        except:
            xbmc.output("Header info not retreived", exc_info=True)
            return ("","")

    #===============================================================================
    def CookieCheck(self, cookieName):
        retVal = False
        
        for cookie in self.cj:
            if cookie.name == cookieName:
                xbmc.output("Found cookie: %s", cookie.name)
                retVal = True
                break

        return retVal
    
    #===============================================================================
    def CookiePrint(self):
        for cookie in self.cj:
            xbmc.output("cookieName=%s; cookieValue=%s", cookie.name, cookie.value)        
        return
    
    #===============================================================================
    def CorrectFileName(self, filename):
        filename = re.sub(self.inValidCharacters,"",filename)
        if len(filename)>42:
            (base, ext) = os.path.splitext(filename)
            baseLength = 42 - len(ext)
            regex = "^.{1,%s}" % (baseLength) 
            base = re.compile(regex).findall(base)[-1]
            filename = "%s%s" % (base, ext)
        return filename

    #===============================================================================
    def PBHandler(self, blocknum, blocksize, totalsize, uriPB, pbLine1, pbLine2):
        """
        add information to the Progressbar and returns true if it is canceled
        """
        if uriPB.iscanceled()==False:
            try:
                retrievedsize = blocknum*blocksize
                if totalsize != 0:
                    perc = 100*retrievedsize/totalsize
                else:
                    perc = 0
                
                retrievedsizeMB = 1.0*retrievedsize/self.bytesToMB
                totalsizeMB = 1.0*totalsize/self.bytesToMB
                
                if totalsize > 0:
                    pbLine2 = '%i%% (%.1f of %.1f MB)' % (perc, retrievedsizeMB, totalsizeMB)
                    animation = blocknum % len(self.pbAnimation)
                    uriPB.update(int(perc), pbLine1 + " - " + self.pbAnimation[animation] ,pbLine2)
                return False
            except:
                xbmc.output("PBHandle error", exc_info=True)
                return True
        else:
            return True
    
    #==============================================================================
    def PBEmergencyCanceler(self, *args, **kwargs):
        xbmc.output("Emergency Canceller Check.....")
        uriPB = kwargs["pb"]
        if uriPB.iscanceled():
            uriPB.close()
            xbmc.output("Emerency Canceling of UriOpener")
        else:
            try:
                self.timerUpDown.cancel()
            except:
                xbmc.output("Emerengy Cancel timer not active. Activating")
                pass
            self.timerUpDown = threading.Timer(self.timerTimeOut, self.PBEmergencyCanceler, kwargs={'pb':uriPB})
            self.timerUpDown.start()
        return 

#===============================================================================    
class AsyncOpener(threading.Thread):
    def __init__(self, uri, handler, blocksize, action=None, params="", filePath=""):
        """ constructor, setting initial variables 
        
        """
        self.uri = uri
        self.uriHandler = handler
        self.params = params        
        self.blockSize = blocksize        
        self.savePath = filePath
        
        self.isCompleted = False
        self.fileSize = 0
        self.blocksRead = 0
        self.data = ""
        
        if action=='open':     
            threading.Thread.__init__(self, name='UriOpenerThread', target=self.Open)
        else:
            raise Exception()
            return

    #===============================================================================
    def Open(self):
        try:
            # Check for posts
            if self.params=='':
                sourceHandle = self.uriHandler.open(self.uri)
            else:
                sourceHandle = self.uriHandler.open(self.uri, self.params)
            
            xbmc.output("Determining which Progessbar to use....")
            data = sourceHandle.info()
            
            if data.get('Content-length'):
                self.fileSize = int(data.get('Content-length'))
                xbmc.output('FileSize is known (fileSize=' + str(self.fileSize) +')')
            else:
                self.fileSize = -1
                xbmc.output('FileSize is unknown')
            
            data = ""
            
            #time.sleep(2)
            
            self.blocksRead = 0
            while 1:
                block = sourceHandle.read(self.blockSize)
                if block == "":
                    break
                data = data + block
                self.blocksRead += 1
                
                #need a sleep to allow reading of variables
                #time.sleep(0.0005)
                
            sourceHandle.close()
            
            self.data = data
            self.isCompleted = True
        except:
            xbmc.output("Error Opening url %s", self.uri, exc_info=True)
            try:
                sourceHandle.close()
            except UnboundLocalError:
                pass
            
            self.data = ""
            self.isCompleted = True            