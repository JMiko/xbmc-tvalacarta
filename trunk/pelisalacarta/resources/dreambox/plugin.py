# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta launcher for dreambox
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Based on Multi-Mediathek Plugin for Enigma2 Dreamboxes

from Components.config import config, configfile, getConfigListEntry, ConfigSubsection, ConfigYesNo, ConfigText, ConfigEnableDisable, ConfigSelection, NoSave
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Network import iNetwork
from Components.PluginComponent import plugins
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Slider import Slider
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBar import MoviePlayer
from Screens.InputBox import PinInput
from Screens.Standby import TryQuitMainloop
from Screens.TaskView import JobView
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools import Notifications, ASCIItranslit
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor

from enigma import ePicLoad, eTimer, getDesktop, eConsoleAppContainer, eBackgroundFileEraser, eServiceReference, iServiceInformation, iPlayableService
from os import stat as os_stat, listdir as os_listdir, path as os_path, readlink as os_readlink, system as os_system
from time import time
from twisted.web.client import getPage, downloadPage
from urllib import urlencode, unquote, quote_plus
from urllib2 import Request, urlopen
from xml.dom.minidom import parse, parseString
from xml.sax.saxutils import unescape

import xml.etree.cElementTree

try:
    from Plugins.Extensions.VlcPlayer.VlcPlayer import VlcPlayer
    from Plugins.Extensions.VlcPlayer.VlcServerConfig import vlcServerConfig
    from Tools.BoundFunction import boundFunction
    VLCSUPPORT = True
except Exception, e:
    VLCSUPPORT = False

##############################
#####  CONFIG SETTINGS   #####
##############################

config.plugins.pelisalacarta = ConfigSubsection()
config.plugins.pelisalacarta.storagepath = ConfigText(default="/media/hdd", fixed_size=False)
config.plugins.pelisalacarta.imagecache = ConfigEnableDisable(default=True)
config.plugins.pelisalacarta.imagescaling = ConfigSelection(default="1", choices = [("0", _("simple")), ("1", _("better"))])
config.plugins.pelisalacarta.imagescaler = ConfigSelection(default="0", choices = [("0", _("decodePic()")), ("1", _("getThumbnail()"))])
config.plugins.pelisalacarta.showadultcontent = ConfigYesNo(default=False)
config.plugins.pelisalacarta.showsecretcontent = ConfigYesNo(default=False)
config.plugins.pelisalacarta.version = NoSave(ConfigText(default="282"))

config.plugins.pelisalacarta.mocosoftxaccount = ConfigYesNo(default=False)
config.plugins.pelisalacarta.mocosoftxuser = ConfigText(default="", fixed_size=False)
config.plugins.pelisalacarta.mocosoftxpassword = ConfigText(default="", fixed_size=False)
config.plugins.pelisalacarta.serieslyaccount = ConfigYesNo(default=False)
config.plugins.pelisalacarta.serieslyuser = ConfigText(default="", fixed_size=False)
config.plugins.pelisalacarta.serieslypassword = ConfigText(default="", fixed_size=False)

default = config.plugins.pelisalacarta.storagepath.value + "/pelisalacarta/movies"
tmp = config.movielist.videodirs.value
if default not in tmp:
    tmp.append(default)
config.plugins.pelisalacarta.moviedir = ConfigSelection(default=default, choices=tmp)

#################################
###    Download Movie Task    ###
#################################

class downloadJob(Job):
    def __init__(self, toolbox, cmdline, filename, filetitle):
        print "[pelisalacarta] downloadJob.__init__"
        Job.__init__(self, _("Download Movie"))
        self.filename = filename
        self.toolbox = toolbox
        self.retrycount = 0
        downloadTask(self, cmdline, filename, filetitle)

    def retry(self):
        assert self.status == self.FAILED
        self.retrycount += 1
        self.restart()

    def cancel(self):
        self.abort()
        os_system("rm -f %s" % self.filename)
        
class downloadTask(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
    def __init__(self, job, cmdline, filename, filetitle):
        print "[pelisalacarta] downloadTask.__init__"
        Task.__init__(self, job, filetitle)
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filename = filename
        self.toolbox = job.toolbox
        self.error = None
        self.lasterrormsg = None
        
    def processOutput(self, data):
        try:
            if data.endswith('%)'):
                startpos = data.rfind("sec (")+5
                if startpos and startpos != -1:
                    self.progress = int(float(data[startpos:-4]))
            elif data.find('%') != -1:
                tmpvalue = data[:data.find("%")]
                tmpvalue = tmpvalue[tmpvalue.rfind(" "):].strip()
                tmpvalue = tmpvalue[tmpvalue.rfind("(")+1:].strip()
                self.progress = int(float(tmpvalue))
            else:
                Task.processOutput(self, data)
        except Exception, errormsg:
            print "Error processOutput: " + str(errormsg)
            Task.processOutput(self, data)

    def processOutputLine(self, line):
        line = line[:-1]
        #print "[DownloadTask STATUS MSG] %s" % line
        self.lasterrormsg = line
        if line.startswith("ERROR:"):
            if line.find("RTMP_ReadPacket") != -1:
                self.error = self.ERROR_RTMP_ReadPacket
            elif line.find("corrupt file!") != -1:
                self.error = self.ERROR_CORRUPT_FILE
                os_system("rm -f %s" % self.filename)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith("wget:"):
            if line.find("server returned error") != -1:
                self.error = self.ERROR_SERVER
        elif line.find("Segmentation fault") != -1:
            self.error = self.ERROR_SEGFAULT
            
    def afterRun(self):
        pass
        #FIXME: Only show when we saved movie in background!
        #if self.getProgress() == 0 or self.getProgress() == 100:
        #    Notifications.AddNotification(MessageBox, _("Movie successfully transfered to your HDD!") +"\n"+self.filename, MessageBox.TYPE_INFO, timeout=10)

class downloadTaskPostcondition(Condition):
    RECOVERABLE = True
    def check(self, task):
        if task.returncode == 0 or task.error is None:
            return True
        else:
            return False

    def getErrorMessage(self, task):
        return {
            task.ERROR_CORRUPT_FILE: _("Video Download Failed!\n\nCorrupted Download File:\n%s" % task.lasterrormsg),
            task.ERROR_RTMP_ReadPacket: _("Video Download Failed!\n\nCould not read RTMP-Packet:\n%s" % task.lasterrormsg),
            task.ERROR_SEGFAULT: _("Video Download Failed!\n\nSegmentation fault:\n%s" % task.lasterrormsg),
            task.ERROR_SERVER: _("Video Download Failed!\n\nServer returned error:\n%s" % task.lasterrormsg),
            task.ERROR_UNKNOWN: _("Video Download Failed!\n\nUnknown Error:\n%s" % task.lasterrormsg)
        }[task.error]

###################################################

class PelisalacartaMoviePlayer(MoviePlayer):
    def __init__(self, session, service, movieinfo=None):
        print "[pelisalacarta] PelisalacartaMoviePlayer.__init__"
        MoviePlayer.__init__(self, session, service)
        self.skinName = "MoviePlayer"
        self.movieinfo = movieinfo

        self.__event_tracker = ServiceEventTracker(screen=self, eventmap=
            {
                iPlayableService.evUser+10: self.__evAudioDecodeError,
                iPlayableService.evUser+11: self.__evVideoDecodeError,
                iPlayableService.evUser+12: self.__evPluginError
            })

    def leavePlayer(self):
        print "[pelisalacarta] PelisalacartaMoviePlayer.leavePlayer"
        self.leavePlayerConfirmed(True)

    def leavePlayerConfirmed(self, answer):
        print "[pelisalacarta] PelisalacartaMoviePlayer.leavePlayerConfirmed"
        if answer:
            self.close()

    def doEofInternal(self, playing):
        print "[pelisalacarta] PelisalacartaMoviePlayer.doEofInternal"
        self.leavePlayerConfirmed(True)

    def showMovies(self):
        print "[pelisalacarta] PelisalacartaMoviePlayer.showMovies"
        pass

    def __evAudioDecodeError(self):
        currPlay = self.session.nav.getCurrentService()
        sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
        print "[__evAudioDecodeError] audio-codec %s can't be decoded by hardware" % (sTagAudioCodec)
        self.session.open(MessageBox, _("This Dreambox can't decode %s streams!") % sTagAudioCodec, type=MessageBox.TYPE_INFO, timeout=20)

    def __evVideoDecodeError(self):
        currPlay = self.session.nav.getCurrentService()
        sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
        print "[__evVideoDecodeError] video-codec %s can't be decoded by hardware" % (sTagVideoCodec)
        self.session.open(MessageBox, _("This Dreambox can't decode %s streams!") % sTagVideoCodec, type=MessageBox.TYPE_INFO, timeout=20)

    def __evPluginError(self):
        currPlay = self.session.nav.getCurrentService()
        message = currPlay.info().getInfoString(iServiceInformation.sUser+12)
        print "[__evPluginError]" , message
        if VLCSUPPORT and self.movieinfo is not None:
            self.session.openWithCallback(self.VLCcallback, MessageBox, _("Your Dreambox can't decode this video stream!\n%s\nDo you want to stream it via VLC Server from your PC?") % message[17:], MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Your Dreambox can't decode this video stream!\n%s") % message, type=MessageBox.TYPE_INFO, timeout=20)

    def VLCcallback(self, answer):
        if answer is True:
            self.close(self.movieinfo)
        else:
            self.close()

#------------------------------------------------------------------------------------------

class Pelisalacarta(Screen):
    def __init__(self, session, feedurl="http://www.dreambox-plugins.de/feeds/mediathek/main.xml", feedtitle="Canales", feedtext=""):
        print "[pelisalacarta] __init__ (feedurl="+feedurl+")"
        # Get Screen Resolution
        size_w = getDesktop(0).size().width()
        size_h = getDesktop(0).size().height()

        if size_w == 1280:
            self.spaceTop = 200
            self.spaceLeft = 50
            self.spaceX = 35
            self.spaceY = 40
            self.picX = 200
            self.picY = 180
        else:
            self.spaceTop = 160
            self.spaceLeft = 15
            self.spaceX = 30
            self.spaceY = 35
            self.picX = 160
            self.picY = 144

        # Workaround for UserAgent Settings when MediaPlayer not installed
        try:
            config.mediaplayer.useAlternateUserAgent.value = False
            config.mediaplayer.alternateUserAgent.value = ""
        except Exception, errormsg:
            config.mediaplayer = ConfigSubsection()
            config.mediaplayer.useAlternateUserAgent = ConfigYesNo(default=False)
            config.mediaplayer.alternateUserAgent = ConfigText(default="")

        # Set some default values
        self["titletext"] = StaticText(feedtitle)
        self["titlemessage"] = StaticText(feedtext)
        self["pageinfo"] = StaticText("Downloading feeds from webserver ...")

        self.feedurl = feedurl
        self.feedtitle = feedtitle
        self.feedtext = feedtext
        self.textcolor = "#F7F7F7"
        self.bgcolor = "#000000"
        self.textsize = 20

        # Create Thumblist
        self.thumbsX = (size_w - self.spaceLeft) / (self.spaceX + self.picX) # thumbnails in X
        self.thumbsY = (size_h - self.spaceTop) / (self.spaceY + self.picY) # thumbnails in Y
        self.thumbsC = self.thumbsX * self.thumbsY # all thumbnails

        self.positionlist = []
        skincontent = ""

        posX = -1
        #print "self.thumbsC=%s" % self.thumbsC
        for x in range(self.thumbsC):
            posY = x / self.thumbsX
            posX += 1
            if posX >= self.thumbsX:
                posX = 0

            absX = self.spaceLeft + self.spaceX + (posX*(self.spaceX + self.picX))
            absY = self.spaceTop + self.spaceY + (posY*(self.spaceY + self.picY))
            self.positionlist.append((absX, absY))
            skincontent += "<widget source=\"label" + str(x) + "\" render=\"Label\" position=\"" + str(absX+2) + "," + str(absY+self.picY-self.textsize-10) + "\" size=\"" + str(self.picX - 10) + ","  + str((self.textsize*2)+10) + "\" halign=\"center\" font=\"Regular;" + str(self.textsize) + "\" zPosition=\"4\" transparent=\"1\" foregroundColor=\"" + self.textcolor + "\" />"
            skincontent += "<widget name=\"thumb" + str(x) + "\" position=\"" + str(absX)+ "," + str(absY+5) + "\" size=\"" + str(self.picX -10) + "," + str(self.picY - (self.textsize*2)) + "\" zPosition=\"4\" transparent=\"1\" alphatest=\"on\" />"

        # Screen, backgroundlabel and MovingPixmap
        self.skin = "<screen position=\"0,0\" size=\"" + str(size_w) + "," + str(size_h) + "\" flags=\"wfNoBorder\" title=\"pelisalacarta\"> \
            <ePixmap name=\"dp_logo\" position=\"25,8\" zPosition=\"2\" size=\"250,200\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/pelisalacarta/images/logopelis.jpg\" /> \
            <ePixmap name=\"dp_logo2\" position=\"1050,30\" zPosition=\"2\" size=\"130,134\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/pelisalacarta/images/tododream.jpg\" /> \
            <eLabel position=\"75,200\" zPosition=\"1\" size=\"1140,2\" backgroundColor=\"#FF9900\" /> \
            <widget source=\"titletext\" transparent=\"1\" render=\"Label\" zPosition=\"2\" position=\"295,105\" size=\"600,45\" font=\"Regular;40\" backgroundColor=\"" + self.bgcolor + "\" foregroundColor=\"" + self.textcolor + "\" /> \
            <widget source=\"titlemessage\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"center\" halign=\"left\" position=\"295,150\" size=\""+ str(size_w) + ",30\" font=\"Regular;25\" foregroundColor=\"" + self.textcolor + "\" /> \
            <eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\"" + self.bgcolor + "\" /> \
            <widget source=\"pageinfo\" position=\"0,667\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"center\" halign=\"center\" size=\"" + str(size_w) + ",30\" font=\"Regular;14\" foregroundColor=\"" + self.textcolor + "\" /> \
            <widget name=\"frame\" position=\"" + str(size_w) + "," + str(size_h) + "\" size=\"190,200\" pixmap=\"pic_frame.png\" zPosition=\"5\" alphatest=\"on\" />"  + skincontent + "</screen>"

        Screen.__init__(self, session)

        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "MovieSelectionActions"],
        {
            "cancel": self.Exit,
            "ok": self.key_ok,
            "left": self.key_left,
            "right": self.key_right,
            "up": self.key_up,
            "down": self.key_down,
            "blue": self.selectBookmark,
            "contextMenu": self.key_menu,
            "showEventInfo": self.key_info
        }, -1)

        self.maxPage = 0
        self.maxentry = 1
        self.index = 0
        self.itemlist = False

        self["frame"] = MovingPixmap()
        for x in range(self.thumbsC):
            self["label"+str(x)] = StaticText()
            self["thumb"+str(x)] = Pixmap()

        # Get FrameBuffer Scale for ePicLoad()
        sc = AVSwitch().getFramebufferScale()
        
        # Init Thumb PicLoad
        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.showThumbPixmap)
        self.picload.setPara((self.picX-10, self.picY-(self.textsize*2), sc[0], sc[1], config.plugins.pelisalacarta.imagecache.value, int(config.plugins.pelisalacarta.imagescaling.value), "#00000000"))

        # Init eBackgroundFileEraser
        self.BgFileEraser = eBackgroundFileEraser.getInstance()

        # Check if plugin-update is available
        if self.feedtitle == "Startseite":
            self.onLayoutFinish.append(self.checkforupdate)

        self.onFirstExecBegin.append(self.loadFrame)

    def loadFrame(self):
        print "[pelisalacarta] loadFrame"
        if self.feedtitle == "Startseite":
            if not self.createMediaFolders():
                return

        if self.feedtitle == "Bookmarks":
            self.getBookmarks()
        elif self.feedurl.startswith("pelisalacarta"):
            self.getpelisalacartaitems()
        else:
            self.getxmlfeed()

    def createMediaFolders(self):
        print "[pelisalacarta] createMediaFolders"
        # Check if cache folder is on a mountable device and not inside flash-memory
        tmppath = config.plugins.pelisalacarta.storagepath.value
        if tmppath != "/tmp" and tmppath != "/media/ba":
            if os_path.islink(tmppath):
                tmppath = os_readlink(tmppath)
            loopcount = 0
            while not os_path.ismount(tmppath):
                loopcount += 1
                tmppath = os_path.dirname(tmppath)
                if tmppath == "/" or tmppath == "" or loopcount > 50:
                    self["pageinfo"].setText(_("Error: Can not create cache-folders inside flash memory. Check your Cache-Folder Settings!"))
                    return False

        # Create Cache Folders ...
        os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta")
        os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images")
        os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/movies")
        os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/tmp")

        # Check if Cache Folders were created successfully
        if not os_path.exists(config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta"):
            self["pageinfo"].setText(_("Error: No write permission to create cache-folders. Check your Cache-Folder Settings!"))
            return False
        else:
            return True

    def checkforupdate(self):
        try:
            self["pageinfo"].setText(_("Checking for updates ..."))
            getPage("http://www.dreambox-plugins.de/downloads/MultiMediathek/version.txt").addCallback(self.gotUpdateInfo).addErrback(self.getxmlfeedError)
        except Exception, error:
            print "[pelisalacarta]: Could not download HTTP Page\n" + str(error)

    def gotUpdateInfo(self, html):
        tmp_infolines = html.splitlines()
        remoteversion = tmp_infolines[0]
        self.updateurl = tmp_infolines[1]
        '''
        FIXME: Desactivada actualizacion automatica
        if config.plugins.pelisalacarta.version.value < remoteversion:
            self.session.openWithCallback(self.startPluginUpdate,MessageBox,_("An update is available for Mediathek Plugin!\nDo you want to download and install now?"), MessageBox.TYPE_YESNO)
        '''

    def startPluginUpdate(self, answer):
        if answer is True:
            self.container=eConsoleAppContainer()
            self.container.appClosed.append(self.finishedPluginUpdate)
            self.container.execute("opkg install --force-overwrite " + str(self.updateurl))

    def finishedPluginUpdate(self,retval):
        self.session.openWithCallback(self.restartGUI, MessageBox,_("pelisalacarta plugin successfully updated!\nDo you want to restart Enigma2 GUI now?"), MessageBox.TYPE_YESNO)

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def getxmlfeed(self):
        print "[pelisalacarta] getxmlfeed"
        feedurl = self.feedurl
        if self.feedtitle == "Startseite" and (config.plugins.pelisalacarta.showadultcontent.value == True or config.plugins.pelisalacarta.showsecretcontent.value == True):
            feedurl = feedurl + "?"
            if config.plugins.pelisalacarta.showadultcontent.value:
                feedurl = feedurl + "&showadult=1"
            if config.plugins.pelisalacarta.showsecretcontent.value:
                feedurl = feedurl + "&showsecret=1"
        
        '''
        if '-->' in feedurl:
            # Request to download external page
            tmpurls = feedurl.split("-->")
            getpageurl = unquote(tmpurls[1])
            self.postpageurl = unquote(tmpurls[0])
            getPage(getpageurl, agent="Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)").addCallback(self.ForwardExternalPage).addErrback(self.getxmlfeedError)
        else:
            getPage(feedurl).addCallback(self.gotxmlfeed).addErrback(self.getxmlfeedError)
        '''
        self.gotxmlfeed("")

    def getpelisalacartaitems(self):
        print "[pelisalacarta] getpelisalacartaitems"
        '''
        from core import config
        print "config done"
        from core import logger
        print "logger done"
        from core import scrapertools
        print "scrapertools done"
        from servers import servertools
        print "servertools done"
        '''

        # Lee el canal
        print "feedtitle="+self.feedtitle
        print "feedurl="+self.feedurl
        print "feedtext="+self.feedtext

        #from channels import seriematic 
        from core.item import Item
        from core import downloadtools
        from servers import servertools
        
        partes = self.feedurl.split("|")
        canal = partes[1]
        print "canal="+canal
        accion = partes[2]
        print "accion="+accion
        urlx = partes[3]
        print "url="+urlx
        serverx = partes[4]
        print "server="+serverx
        item = Item(title=self.feedtitle,url=urlx,channel=canal,action=accion, server=serverx)

        self["pageinfo"].setText("Cargando elementos del canal...")
        if accion=="play":
            try:
                exec "from pelisalacarta.channels import "+canal
                exec "itemlista = "+canal+"."+accion+"(item)"
                item = itemlista[0]
            except:
                pass

            exec "from servers import "+item.server+" as servermodule"
            video_urls = servermodule.get_video_url( item.url )
            
            itemlista = []
            for video_url in video_urls:
                itemvideo = Item(title=video_url[0], url=video_url[1], action="__movieplay")
                itemlista.append(itemvideo)

        elif accion=="findvideos":
            try:
                exec "from pelisalacarta.channels import "+canal
                exec "itemlista = "+canal+"."+accion+"(item)"
                for item in itemlista:
                    item.folder=False
            except:
                from core import scrapertools
                data = scrapertools.cache_page(urlx)
                
                # Busca los enlaces a los videos
                listavideos = servertools.findvideos(data)
                
                itemlista = []
                for video in listavideos:
                    scrapedtitle = item.title.strip() + " - " + video[0]
                    scrapedurl = video[1]
                    server = video[2]
                    
                    itemlista.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=True) )
        else:
            exec "from pelisalacarta.channels import "+canal
            exec "itemlista = "+canal+"."+accion+"(item)"
            print "%d elementos" % len(itemlista)

        index = 0
        framePos = 0
        Page = 0

        self.Thumbnaillist = []
        self.itemlist = []
        self.currPage = -1
        self.maxPage = 0
        
        for item in itemlista:
            if item.action=="__movieplay":
                print "item __movieplay"
                type = "movie"
                name = item.title
                imgurl = ""
                url = item.url
            else:
                print "item normal"
                type = "cat"
                name = item.title
                name = name.replace("á","a")
                name = name.replace("é","e")
                name = name.replace("í","i")
                name = name.replace("ó","o")
                name = name.replace("ú","u")
                name = name.replace("ñ","n")
                name = name.replace("Á","A")
                name = name.replace("É","E")
                name = name.replace("Í","I")
                name = name.replace("Ó","O")
                name = name.replace("Ú","U")
                name = name.replace("Ñ","N")
                name = downloadtools.limpia_nombre_excepto_1(name)
                #name = unicode(item.title,"utf-8",errors="ignore").encode("iso-8859-1")
                imgurl = ""
                url = "pelisalacarta" + "|" + canal + "|" + item.action + "|" + item.url + "|" + item.server

            # APPEND ITEM TO LIST
            self.itemlist.append((index, framePos, Page, name, imgurl, url, type, "item"))
            index += 1
            framePos += 1

            if framePos == 1:
                self.maxPage += 1
            elif framePos > (self.thumbsC-1):
                framePos = 0
                Page += 1

        self.maxentry = len(self.itemlist)-1

        self["pageinfo"].setText("")
        self.paintFrame()
        self["frame"].show()

    def ForwardExternalPage(self, html):
        # We send the received page directly to my webserver and parse it there ...
        getPage(url=self.postpageurl, method='POST', headers={'Content-Type':'application/x-www-form-urlencoded'}, postdata=urlencode({'pagedata' : html})).addCallback(self.gotxmlfeed).addErrback(self.getxmlfeedError)
        
    def getxmlfeedError(self, error=""):
        self["pageinfo"].setText("Error downloading XML Feed!\n\n" + str(error))
        print error
        
    def gotxmlfeed(self, page=""):
        print "[pelisalacarta] gotxmlfeed"
        print page

        '''        
        self["pageinfo"].setText("Parsing XML Feeds ...")
        xml = parseString(page)
        '''

        index = 0
        framePos = 0
        Page = 0

        self.Thumbnaillist = []
        self.itemlist = []
        self.currPage = -1
        self.maxPage = 0

        # Anade los canales de pelisalacarta
        from core.item import Item
        import channelselector
        itemlist = channelselector.channels_list()

        for item in itemlist:
            if item.type=="generic" and item.channel!="tengourl":
                type = "cat"
                name = item.title
                imgurl = "http://pelisalacarta.mimediacenter.info/dreambox/"+item.channel+".png"
                url = "pelisalacarta|"+item.channel+"|mainlist|none|"
                self["pageinfo"].setText(imgurl)

                # APPEND ITEM TO LIST
                self.itemlist.append((index, framePos, Page, name, imgurl, url, type, "item"))
                index += 1
                framePos += 1
    
                if framePos == 1:
                    self.maxPage += 1
                elif framePos > (self.thumbsC-1):
                    framePos = 0
                    Page += 1

        self.maxentry = len(self.itemlist)-1

        self["pageinfo"].setText("")
        self.paintFrame()
        self["frame"].show()

    def getBookmarks(self):
        self["pageinfo"].setText("Parsing Bookmarks ...")

        index = 0
        framePos = 0
        Page = 0

        self.Thumbnaillist = []
        self.itemlist = []
        self.currPage = -1
        self.maxPage = 0

        bookmarkfile = "/etc/enigma2/pelisalacarta.bookmarks"
        if fileExists(bookmarkfile, 'r'):
            bookmarklist = []
            bookmarkcount = 0
            tmpfile = open(bookmarkfile, "r")
            for line in tmpfile:
                if ':::' in line:
                    bookmarkcount += 1
                    tmpline = line.split(":::")
                    id = bookmarkcount
                    type = str(tmpline[0])
                    name = str(tmpline[1])
                    url  = str(tmpline[2])
                    imgurl = str(tmpline[3])

                    # APPEND ITEM TO LIST
                    self.itemlist.append((index, framePos, Page, name, imgurl, url, type, "bookmark"))
                    index += 1
                    framePos += 1

                    if framePos == 1:
                        self.maxPage += 1
                    elif framePos > (self.thumbsC-1):
                        framePos = 0
                        Page += 1

        self.maxentry = len(self.itemlist)-1

        self["pageinfo"].setText("")
        self.paintFrame()
        self["frame"].show()

    def getThumbnail(self):
        self.thumbcount += 1
        self.thumburl = self.Thumbnaillist[self.thumbcount][2]
        self.thumbfile = config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images/"+str(self.Thumbnaillist[self.thumbcount][3])

        if fileExists(self.thumbfile, 'r'):
            self.gotThumbnail()
        else:
            downloadPage(self.thumburl, self.thumbfile, agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.2) Gecko/2008091620 Firefox/3.0.2").addCallback(self.gotThumbnail).addErrback(self.showThumbError)

    def gotThumbnail(self, data=""):
        if config.plugins.pelisalacarta.imagescaler.value == "0":
            self.picload.startDecode(self.thumbfile)
        elif self.picload.getThumbnail(self.thumbfile) == 1:
            if self.thumbcount+1 < len(self.Thumbnaillist):
                self.getThumbnail()
        
    def showThumbPixmap(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr != None:
            self["thumb" + str(self.thumbcount)].instance.setPixmap(ptr.__deref__())
            self["thumb" + str(self.thumbcount)].show()

        if self.thumbcount+1 < len(self.Thumbnaillist):
            self.getThumbnail()

    def showThumbError(self, error):
        if self.thumbcount+1 < self.thumbsC:
            self.getThumbnail()

    def paintFrame(self):
        if self.maxentry < self.index or self.index < 0 or not self.itemlist:
            return

        pos = self.positionlist[self.itemlist[self.index][1]]
        self["frame"].moveTo(pos[0], pos[1], 1)
        self["frame"].startMoving()

        if self.currPage != self.itemlist[self.index][2]:
            self.currPage = self.itemlist[self.index][2]
            self.newPage()

    def newPage(self):
        self.Thumbnaillist = []
        if self.maxPage > 1:
            self["pageinfo"].setText("Page "+str(self.currPage+1)+" of "+str(self.maxPage))
        else:
            self["pageinfo"].setText("")

        #clear Labels and Thumbnail
        for x in range(self.thumbsC):
            self["label"+str(x)].setText("")
            self["thumb"+str(x)].hide()

        #paint Labels and fill Thumbnail-List
        for x in self.itemlist:
            print "x="+str(x)
            if x[2] == self.currPage:
                self["label"+str(x[1])].setText(x[3])
                self["thumb"+str(x[1])].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/Extensions/pelisalacarta/images/item.png")
                self["thumb"+str(x[1])].show()
                self.Thumbnaillist.append([0, x[1], x[4], ASCIItranslit.legacyEncode(x[3]+"."+x[4].split('.')[-1]).lower()])

        #Get Thumbnails
        self.thumbcount = -1
        self.getThumbnail()

    def selectBookmark(self):
        self.session.open(Pelisalacarta, self.itemlist[self.index][5], "Bookmarks", "Bookmarks from your favorite Movies")

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.maxentry
        self.paintFrame()

    def key_right(self):
        self.index += 1
        if self.index > self.maxentry:
            self.index = 0
        self.paintFrame()

    def key_up(self):
        self.index -= self.thumbsX
        if self.index < 0:
            self.index = self.maxentry
        self.paintFrame()

    def key_down(self):
        self.index += self.thumbsX
        if self.index-self.thumbsX == self.maxentry:
            self.index = 0
        elif self.index > self.maxentry:
            self.index = self.maxentry
        self.paintFrame()

    def key_info(self):
        self.session.open(MessageBox,("Coming soon ..."), MessageBox.TYPE_INFO, timeout=10)

    def key_menu(self):
        if self.feedtitle == "Startseite":
            self.session.openWithCallback(self.loadFrame, Pelisalacarta_Settings)
        elif self.itemlist:
            self.session.openWithCallback(self.loadFrame, Pelisalacarta_MenuOptions, self.itemlist[self.index])

    def key_ok(self):
        if not self.itemlist:
            return

        if self.itemlist[self.index][6] == "cat":
            self.session.open(Pelisalacarta, self.itemlist[self.index][5], self.itemlist[self.index][3], self.feedtext + " - " + self.itemlist[self.index][3])
        elif self.itemlist[self.index][6] == "movie":
            self.session.open(MovieInfoScreen, self.itemlist[self.index][5])
        elif self.itemlist[self.index][6] == "switchpage":
            self.feedurl = self.itemlist[self.index][5]
            self.index = 0
            self.getxmlfeed()
        elif self.itemlist[self.index][6] == "search":
            self.searchurl = self.itemlist[self.index][5]
            self.session.openWithCallback(self.SendSearchQuery, VirtualKeyBoard, title = (_("Enter Search Term:")), text = "")

    def SendSearchQuery(self, query):
        if query is not None:
            searchurl = self.itemlist[self.index][5] + "&searchquery=" + quote_plus(str(query))
            self.session.open(Pelisalacarta, searchurl, self.itemlist[self.index][3], self.feedtext + " - " + self.itemlist[self.index][3] + ": " + query)

    def Exit(self):
        if self.feedtitle == "Startseite":
            # Restart old service
            self.session.nav.playService(self.oldService)

            # Clean TEMP Folder
            if os_path.isdir(config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/tmp"):
                for filename in os_listdir(config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/tmp"):
                    filelocation = "%s/pelisalacarta/tmp/%s" % (config.plugins.pelisalacarta.storagepath.value,filename)
                    self.BgFileEraser.erase(filelocation)

            # Clean Image Cache
            if os_path.isdir(config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images"):
                for filename in os_listdir(config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images"):
                    filelocation = "%s/pelisalacarta/images/%s" % (config.plugins.pelisalacarta.storagepath.value,filename)
                    statinfo = os_stat(filelocation)
                    if statinfo.st_mtime < (time()-86400.0):
                        self.BgFileEraser.erase(filelocation)

        del self.picload
        self.close()

#------------------------------------------------------------------------------------------

class MovieInfoScreen(Screen):
    def __init__(self, session, movieurl):
        print "[pelisalacarta] MovieInfoScreen.__init__(movieurl="+movieurl+")"
        Screen.__init__(self, session)

        size_w = getDesktop(0).size().width()
        size_h = getDesktop(0).size().height()

        if size_w == 1280:
            self.skin = "<screen position=\"0,0\" size=\"" + str(size_w) + "," + str(size_h) + "\" flags=\"wfNoBorder\" title=\"pelisalacarta\" > \
                <eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\"#000000\" /> \
                <eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\"#000000\" /> \
                <eLabel position=\"75,200\" zPosition=\"1\" size=\"1140,2\" backgroundColor=\"#FF9900\" /> \
                <widget name=\"trailerimg\" position=\"128,238\" zPosition=\"2\" size=\"270,350\" alphatest=\"on\" /> \
                <widget source=\"trailertitle\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"center\" halign=\"left\" position=\"128,127\" size=\"1000,60\" font=\"Regular;30\" backgroundColor=\"#080B0A\" foregroundColor=\"#F7F7F7\" /> \
                <widget source=\"trailertext\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"top\" halign=\"left\" position=\"430,225\" size=\"500,400\" font=\"Regular;20\" backgroundColor=\"#080B0A\" foregroundColor=\"#F7F7F7\" /> \
                <widget name=\"key_red\" position=\"350,630\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/red.png\" zPosition=\"2\" position=\"350,630\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_green\" position=\"500,630\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/green.png\" zPosition=\"2\" position=\"500,630\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_yellow\" position=\"650,630\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/yellow.png\" zPosition=\"2\" position=\"650,630\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_blue\" position=\"800,630\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/blue.png\" zPosition=\"2\" position=\"800,630\" size=\"140,40\" alphatest=\"on\" /> \
                </screen>"
        else:
            self.skin = "<screen position=\"0,0\" size=\"" + str(size_w) + "," + str(size_h) + "\" flags=\"wfNoBorder\" title=\"pelisalacarta\" > \
                <eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\"#000000\" /> \
                <eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\"#000000\" /> \
                <eLabel position=\"25,110\" zPosition=\"1\" size=\"670,2\" backgroundColor=\"#FF9900\" /> \
                <widget name=\"trailerimg\" position=\"40,120\" zPosition=\"2\" size=\"270,350\" alphatest=\"on\" /> \
                <widget source=\"trailertitle\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"center\" halign=\"left\" position=\"50,48\" size=\"600,60\" font=\"Regular;28\" backgroundColor=\"#080B0A\" foregroundColor=\"#F7F7F7\" /> \
                <widget source=\"trailertext\" transparent=\"1\" render=\"Label\" zPosition=\"2\" valign=\"top\" halign=\"left\" position=\"320,200\" size=\"375,400\" font=\"Regular;20\" backgroundColor=\"#080B0A\" foregroundColor=\"#F7F7F7\" /> \
                <widget name=\"key_red\" position=\"80,520\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/red.png\" zPosition=\"2\" position=\"80,520\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_green\" position=\"220,520\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/green.png\" zPosition=\"2\" position=\"220,520\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_yellow\" position=\"360,520\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/yellow.png\" zPosition=\"2\" position=\"360,520\" size=\"140,40\" alphatest=\"on\" /> \
                <widget name=\"key_blue\" position=\"500,520\" zPosition=\"3\" size=\"140,40\" font=\"Regular;18\" halign=\"center\" valign=\"center\" backgroundColor=\"#1f771f\" transparent=\"1\" /> \
                <ePixmap pixmap=\"/usr/share/enigma2/skin_default/buttons/blue.png\" zPosition=\"2\" position=\"500,520\" size=\"140,40\" alphatest=\"on\" /> \
                </screen>"

        self["trailertitle"] = StaticText("")
        self["trailertext"] = StaticText("")
        self["trailerimg"] = Pixmap()

        self["key_red"] = Button(_("Save on HDD"))
        self["key_green"] = Button(_("Direct Play"))
        self["key_yellow"] = Button(_("Cached Play"))
        self["key_blue"] = Button(_("Bookmark"))

        self.url = movieurl
        self.action = None
        self.movieinfo = None

        self.useragent = "QuickTime/7.6.2 (qtver=7.6.2;os=Windows NT 5.1Service Pack 3)"
        config.mediaplayer.useAlternateUserAgent.value = True
        config.mediaplayer.alternateUserAgent.value = self.useragent
        config.mediaplayer.useAlternateUserAgent.save()
        config.mediaplayer.alternateUserAgent.save()
        config.mediaplayer.save()

        self.moviefolder = config.plugins.pelisalacarta.moviedir.value
        self.imagefolder = config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images"

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
        {
            "cancel": self.Exit,
            "red": self.keyRed,
            "green": self.keyGreen,
            "yellow": self.keyYellow,
            "blue": self.keyBlue
        }, -1)

        # Get FrameBuffer Scale for ePicLoad()
        sc = AVSwitch().getFramebufferScale()
        
        # Init ePicLoad
        self.picload = ePicLoad()
        self.picload.PictureData.get().append(self.showPosterPixmap)
        self.picload.setPara((270, 350, sc[0], sc[1], config.plugins.pelisalacarta.imagecache.value, int(config.plugins.pelisalacarta.imagescaling.value), "#00000000"))
        
        self.onFirstExecBegin.append(self.GetMovieInfo)

    def keyRed(self):
        self.action = "savemovie"
        self.GetMovieList()

    def keyGreen(self):
        self.action = "directplayback"
        self.GetMovieList()

    def keyYellow(self):
        self.action = "cachedplayback"
        self.GetMovieList()

    def keyBlue(self):
        if self.movieinfo is not None:
            os_system("echo 'movie:::%s:::%s:::%s\n' >> /etc/enigma2/pelisalacarta.bookmarks" % (self.movieinfo[0], self.url, self.movieinfo[3]))
            self.session.open(MessageBox, _("Bookmark added!"), MessageBox.TYPE_INFO, timeout=5)

    def GetMovieInfo(self):
        print "[pelisalacarta] GetMovieInfo(self.url="+self.url+")"
        try:
            if '-->' in self.url:
                # Request to download external page
                tmpurls = self.url.split("-->")
                getpageurl = unquote(tmpurls[1])
                self.postpageurl = unquote(tmpurls[0])
                getPage(getpageurl, agent="Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)").addCallback(self.ForwardExternalPage).addErrback(self.error)
            else:
                getPage(self.url).addCallback(self.GotMovieInfo).addErrback(self.error)
        except Exception, error:
            self.session.open(MessageBox,("GetMovieInfo() ERROR:\n%s") % (error), MessageBox.TYPE_ERROR)

    def ForwardExternalPage(self, html):
        # We send the received page directly to my webserver and parse it there ...
        getPage(url=self.postpageurl, method='POST', headers={'Content-Type':'application/x-www-form-urlencoded'}, postdata=urlencode({'pagedata' : html})).addCallback(self.GotMovieInfo).addErrback(self.error)
    
    def GotMovieInfo(self, html):
        self.movieinfo = html.splitlines()

        self["trailertitle"].setText(self.movieinfo[0])
        self["trailertext"].setText(self.movieinfo[2])

        # Get Custom UserAgent from feed
        try:
            if self.movieinfo[4] != "":
                self.useragent = self.movieinfo[4]
            else:
                self.useragent = ""
            config.mediaplayer.alternateUserAgent.value = self.useragent
            config.mediaplayer.alternateUserAgent.save()
        except Exception, error:
            print "[pelisalacarta] Getting UserAgent String failed. Using default ..."
        
        # Download Image
        downloadPage(self.movieinfo[3], self.imagefolder+"/poster.jpg", agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.2) Gecko/2008091620 Firefox/3.0.2").addCallback(self.downloadPosterCallback)

    def downloadPosterCallback(self, txt=""):
        self.picload.startDecode(self.imagefolder+"/poster.jpg")

    def showPosterPixmap(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr != None:
            self["trailerimg"].instance.setPixmap(ptr.__deref__())
            self["trailerimg"].show()

    def GetMovieList(self):
        print "[pelisalacarta] GetMovieList"
        try:
            if '-->' in self.movieinfo[1]:
                # Request to download external page
                tmpurls = self.movieinfo[1].split("-->")
                getpageurl = tmpurls[1]
                self.postpageurl = tmpurls[0]
                getPage(getpageurl, agent="Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)").addCallback(self.ForwardExternalMovieList).addErrback(self.error)
            else:
                getPage(self.movieinfo[1]).addCallback(self.GotMovieList).addErrback(self.error)
        except Exception, error:
            print "[pelisalacarta] Could not download Movie-List\n%s" % (error)
            self.GotMovieList("Streaming video<-->"+self.url+"<-->filename.flv\n")

    def ForwardExternalMovieList(self, html):
        # We send the received page directly to my webserver and parse it there ...
        getPage(url=self.postpageurl, method='POST', headers={'Content-Type':'application/x-www-form-urlencoded'}, postdata=urlencode({'pagedata' : html})).addCallback(self.GotMovieList).addErrback(self.error)

    def GotMovieList(self, html):
        print "[pelisalacarta] GotMovieList(html="+html+")"
        content = html.split("\n")
        entrylist = []
        filecount = 0

        for line in content:
            print line
            if '<-->' in line:
                tmpline = line.split("<-->")
                title = tmpline[0]
                url = tmpline[1]
                filename = tmpline[2]

                if url and url != "":
                    filecount += 1
                    entrylist.append((title,url,filename,filecount))

        if filecount == 0:
            print "[pelisalacarta] filecount==0"
            self.session.open(MessageBox, _("Sorry, no supported videos found here."), MessageBox.TYPE_ERROR, timeout=10)
        elif filecount == 1:
            print "[pelisalacarta] filecount==1"
            tmpanswer = []
            tmpanswer.append((title))
            tmpanswer.append((url))
            tmpanswer.append((filename))
            tmpanswer.append((filecount))
            print "[pelisalacarta] tmpanswer="
            print tmpanswer
            self.movieSelectCallback(tmpanswer)
        else:
            print "[pelisalacarta] filecount>1"
            self.session.openWithCallback(self.movieSelectCallback, ChoiceBox, title=_("Select a Movie:"), list=entrylist)

    def ForwardExternalMoviePage(self, html):
        # We send the received page directly to my webserver and parse it there ...
        getPage(url=self.postpageurl, method='POST', headers={'Content-Type':'application/x-www-form-urlencoded'}, postdata=urlencode({'pagedata' : html})).addCallback(self.GotMoviePage).addErrback(self.error)

    def GotMoviePage(self, html):
        content = html.split("\n")
        filecount = 0

        for line in content:
            if '<-->' in line:
                tmpline = line.split("<-->")
                title = tmpline[0]
                url = tmpline[1]
                filename = tmpline[2]

                if url and url != "":
                    filecount += 1
                    self.selmovieinfo[1]

        if filecount == 1:
            self.movieSelectCallback(self.selmovieinfo)
        else:
            self.session.open(MessageBox, _("Sorry, no supported videos found here."), MessageBox.TYPE_ERROR, timeout=10)
            
    def movieSelectCallback(self, movieinfo):
        self.selmovieinfo = movieinfo
        if movieinfo is not None:
            if '-->' in self.selmovieinfo[1]:
                # Request to download external page
                tmpurls = self.selmovieinfo[1].split("-->")
                getpageurl = tmpurls[1]
                self.postpageurl = tmpurls[0]
                getPage(getpageurl, agent="Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)").addCallback(self.ForwardExternalMovieList).addErrback(self.error)
                return
            
            if self.action == "cachedplayback":
                self.session.open(PlayMovie, movieinfo, self.movieinfo[0], self.useragent)
            elif self.action == "directplayback":
                if movieinfo[1][0:4].lower() == "rtmp":
                    self.session.openWithCallback(self.switchToCPBCallback, MessageBox, _("%s:// Streams can not get played directly (yet)!\n\nDo you want to use cached-playback?") % movieinfo[1][0:4], MessageBox.TYPE_YESNO)
                    return

                sref = eServiceReference(0x1001, 0, movieinfo[1])
                #sref.setName(self.movieinfo[0])
                sref.setName(movieinfo[0])
                self.session.openWithCallback(self.MoviePlayerCallback, PelisalacartaMoviePlayer, sref, movieinfo)
            elif self.action == "vlcplayback" and VLCSUPPORT:
                try:
                    if vlcServerConfig.getDefaultServer() is None:
                        self.session.open(MessageBox, _("No Default Server configured in VLC Settings"), MessageBox.TYPE_ERROR)
                    else:
                        vlcServerConfig.getDefaultServer().play(self.session, media=movieinfo[1], name=self.movieinfo[0], currentList=None, player=boundFunction(VlcPlayer))
                except Exception, error:
                    self.session.open(MessageBox, _("VLC Plugin Error") % error, MessageBox.TYPE_ERROR)

            elif self.action == "savemovie":
                self.saveMovie(movieinfo[0], movieinfo[1], movieinfo[2], movieinfo[3])

    def switchToCPBCallback(self, answer):
        if answer is True:
            self.action = "cachedplayback"
            self.movieSelectCallback(self.selmovieinfo)

    def MoviePlayerCallback(self, response=None):
        if response is not None:
            tmpinfo = []
            tmpinfo.append((response[0]))
            tmpinfo.append((response[1]))
            tmpinfo.append((response[2]))
            tmpinfo.append((response[3]))
            self.action = "vlcplayback"
            self.movieSelectCallback(tmpinfo)

    def saveMovie(self, title, url, filename, fileid):
        if '(VLC)' in title and VLCSUPPORT:
            try:
                if vlcServerConfig.getDefaultServer() is None:
                    self.session.open(MessageBox, _("No Default Server configured in VLC Settings"), MessageBox.TYPE_ERROR)
                else:
                    url = vlcServerConfig.getDefaultServer().playFile(url, 0x44, 0x45)
            except Exception, error:
                self.session.open(MessageBox,("VLC Plugin Error: %s") % error, MessageBox.TYPE_ERROR)

        if self.movieinfo[0]:
            if fileid > 1:
                addfilenumber = "_"+str(fileid)
            else:
                addfilenumber = ""
            filename = ASCIItranslit.legacyEncode(self.movieinfo[0]+addfilenumber+"."+filename.split('.')[-1]).lower()

        if url[0:4] == "http" or url[0:3] == "ftp":
            if config.mediaplayer.useAlternateUserAgent.value:
                useragentcmd = "--header='User-Agent: %s'" % self.useragent
            else:
                useragentcmd = ""
                
            JobManager.AddJob(downloadJob(self, "wget %s -c '%s' -O '%s/%s'" % (useragentcmd, url, self.moviefolder, filename), self.moviefolder+"/"+filename, self.movieinfo[0]))
            self.LastJobView()
        elif url[0:4] == "rtmp":
            JobManager.AddJob(downloadJob(self, "rtmpdump -r '%s' -o '%s/%s' -e" % (url, self.moviefolder, filename), self.moviefolder+"/"+filename, self.movieinfo[0]))
            self.LastJobView()
        else:
            self.session.open(MessageBox, _("Sorry, this Video can not get saved on HDD.\nOnly HTTP, FTP and RTMP streams can get saved on HDD!"), MessageBox.TYPE_ERROR)

    def LastJobView(self):
        currentjob = None
        for job in JobManager.getPendingJobs():
            currentjob = job

        if currentjob is not None:
            self.session.open(JobView, currentjob)

    def error(self, error):
        self.session.open(MessageBox, _("Unexpected Error:\n%s") % (error), MessageBox.TYPE_ERROR)

    def Exit(self):
        del self.picload
        self.close()

#------------------------------------------------------------------------------------------


class PlayMovie(Screen):
    skin = """
        <screen position="center,center" size="400,240" title="Caching Video ..." >
            <widget source="label_filename" transparent="1" render="Label" zPosition="2" position="10,10" size="380,20" font="Regular;19" />
            <widget source="label_destination" transparent="1" render="Label" zPosition="2" position="10,35" size="380,20" font="Regular;19" />
            <widget source="label_speed" transparent="1" render="Label" zPosition="2" position="10,60" size="380,20" font="Regular;19" />
            <widget source="label_timeleft" transparent="1" render="Label" zPosition="2" position="10,85" size="380,20" font="Regular;19" />
            <widget source="label_progress" transparent="1" render="Label" zPosition="2" position="10,110" size="380,20" font="Regular;19" />
            <widget name="activityslider" position="10,150" size="380,30" zPosition="3" transparent="0" />
            <widget name="key_green" position="50,200" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
            <widget name="key_red" position="200,200" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
            <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/green.png" position="50,200" size="140,40" alphatest="on" />
            <ePixmap pixmap="/usr/share/enigma2/skin_default/buttons/red.png" position="200,200" size="140,40" alphatest="on" />
        </screen>"""

    def __init__(self, session, movieinfo, movietitle, useragent):
        self.skin = PlayMovie.skin
        Screen.__init__(self, session)

        self.url = movieinfo[1]
        self.title = movieinfo[0]
        self.filename = movieinfo[2]
        self.movietitle = movietitle
        self.movieinfo = movieinfo
        self.destination = config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/tmp/"
        self.useragent = useragent

        self.streamactive = False

        self.container=eConsoleAppContainer()
        self.container.appClosed.append(self.copyfinished)
        self.container.stdoutAvail.append(self.progressUpdate)
        self.container.stderrAvail.append(self.progressUpdate)
        self.container.setCWD(self.destination)

        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()

        self.BgFileEraser = eBackgroundFileEraser.getInstance()

        try:
            req = Request(self.url)
            req.add_header('User-agent',self.useragent)
            usock = urlopen(req)
            filesize =  usock.info().get('Content-Length')
        except Exception, e:
            filesize = 0

        if filesize is None:
            filesize = 0

        self.filesize = float(filesize) # in bytes

        self.dummyfilesize = False
        self.lastcmddata = None
        self.lastlocalsize = 0

        self["key_green"] = Button(_("Play now"))
        self["key_red"] = Button(_("Cancel"))

        self["label_filename"] = StaticText("File: %s" % (self.filename))
        self["label_destination"] = StaticText("Destination: %s" % (config.plugins.pelisalacarta.storagepath.value))
        self["label_progress"] = StaticText("Progress: N/A")
        self["label_speed"] = StaticText("Speed: N/A")
        self["label_timeleft"] = StaticText("Time left: N/A")

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
        {
            "cancel": self.exit,
            "ok": self.okbuttonClick,
            "red": self.exit,
            "green": self.playfile
        }, -1)

        self.StatusTimer = eTimer()
        self.StatusTimer.callback.append(self.UpdateStatus)

        self.activityslider = Slider(0, 100)
        self["activityslider"] = self.activityslider

        self.onFirstExecBegin.append(self.firstExecBegin)

    def firstExecBegin(self):
        self.progressperc = 0
        self.copyfile()

    def okbuttonClick(self):
        self.StatusTimer.start(5000, True)
        self.UpdateStatus()

    def UpdateStatus(self):
        if fileExists(self.destination + self.filename, 'r'):
            self.localsize = os_path.getsize(self.destination + self.filename)
        else:
            self.localsize = 0

        if self.filesize > 0 and not self.dummyfilesize:
            self.progressperc = round((self.localsize / self.filesize) * 100, 2)

        if int(self.progressperc) > 0:
            self["activityslider"].setValue(int(self.progressperc))

        if self.lastlocalsize != 0:
            transferspeed = round(((self.localsize - self.lastlocalsize) / 1024.0) / 5, 0)
            kbytesleft = round((self.filesize - self.localsize) / 1024.0,0)
            if transferspeed > 0:
                timeleft = round((kbytesleft / transferspeed) / 60,2)
            else:
                timeleft = 0
        else:
            transferspeed = 0
            kbytesleft = 0
            timeleft = 0

        self.lastlocalsize = self.localsize

        self["label_speed"].setText("Speed: " + str(transferspeed) + " KBit/s")
        self["label_progress"].setText("Progress: " + str(round(((self.localsize / 1024.0) / 1024.0), 2)) + "MB of " + str(round(((self.filesize / 1024.0) / 1024.0), 2)) + "MB (" + str(self.progressperc) + "%)")
        self["label_timeleft"].setText("Time left: " + str(timeleft) + " Minutes")
        self.StatusTimer.start(5000, True)

    def copyfile(self):
        if self.url[0:4] == "http" or self.url[0:3] == "ftp":
            if config.mediaplayer.useAlternateUserAgent.value:
                useragentcmd = "--header='User-Agent: %s'" % self.useragent
            else:
                useragentcmd = ""
            cmd = "wget %s -q '%s' -O '%s/%s' &" % (useragentcmd, self.url, self.destination, self.filename)
        elif self.url[0:4] == "rtmp":
            cmd = "rtmpdump -r '%s' -o '%s/%s'" % (self.url, self.destination, self.filename)
        else:
            self.session.openWithCallback(self.exit, MessageBox, _("This stream can not get saved on HDD\nProtocol %s not supported :(") % self.url[0:5], MessageBox.TYPE_ERROR)
            return

        if fileExists(self.destination + self.filename, 'r'):
            self.localsize = os_path.getsize(self.destination + self.filename)
            if self.localsize > 0 and self.localsize >= self.filesize:
                cmd = "echo File already downloaded! Skipping download ..."
            elif self.localsize == 0:
                self.BgFileEraser.erase(self.destination + self.filename)

        self.StatusTimer.start(1000, True)
        self.streamactive = True

        print "[pelisalacarta] execute command: " + cmd
        self.container.execute(cmd)

    def progressUpdate(self, data):
        self.lastcmddata = data
        if data.endswith('%)'):
            startpos = data.rfind("sec (")+5
            if startpos and startpos != -1:
                self.progressperc = int(float(data[startpos:-4]))

                if self.lastlocalsize > 0 and self.progressperc > 0:
                    self.filesize = int(float(self.lastlocalsize/self.progressperc)*100)
                    self.dummyfilesize = True

    def copyfinished(self,retval):
        self.streamactive = False
        self["label_progress"].setText("Progress: 100%")
        self["activityslider"].setValue(100)
        self.playfile()

    def playfile(self):
        if self.lastlocalsize > 0:
            self.StatusTimer.stop()
            sref = eServiceReference(0x1001, 0, self.destination + self.filename)
            sref.setName(self.movietitle)
            self.session.openWithCallback(self.MoviePlayerCallback, PelisalacartaMoviePlayer, sref, self.movieinfo)
        else:
            self.session.openWithCallback(self.exit, MessageBox, _("Error downloading file:\n%s") % self.lastcmddata, MessageBox.TYPE_ERROR)

    def MoviePlayerCallback(self, response=None):
        self.UpdateStatus()
        if response is not None and VLCSUPPORT:
            try:
                ipaddress = self.convertIP(iNetwork.getAdapterAttribute("eth0", "ip"))
                streamurl = "http://" + ipaddress + ":" + str(config.plugins.Webinterface.http.port.value) + "/file?file=" + self.destination + self.filename
                #self.session.openWithCallback(self.exit, MessageBox, _("START VLC-STREAM:\n%s") % streamurl, MessageBox.TYPE_INFO)
                if vlcServerConfig.getDefaultServer() is None:
                    self.session.openWithCallback(self.exit, MessageBox, _("No Default Server configured in VLC Settings"), MessageBox.TYPE_ERROR)
                else:
                    vlcServerConfig.getDefaultServer().play(self.session, media=streamurl, name=self.movietitle, currentList=None, player=boundFunction(VlcPlayer))
            except Exception, error:
                self.session.openWithCallback(self.exit, MessageBox, _("VLC Plugin Error: %s") % error, MessageBox.TYPE_ERROR)

    def convertIP(self, list):
        if len(list) == 4:
            retstr = "%s.%s.%s.%s" % (list[0], list[1], list[2], list[3])
        else:
            retstr = "0.0.0.0"
        return retstr

    def exit(self, retval=None):
        self.container.kill()
        self.BgFileEraser.erase(self.destination + self.filename)

        self.StatusTimer.stop()
        self.session.nav.playService(self.oldService)
        self.close()

#------------------------------------------------------------------------------------------

class Pelisalacarta_MenuOptions(Screen):
    def __init__(self, session, movieinfo):
        Screen.__init__(self, session)

        self.skin = """
            <screen position="center,center" size="400,200" title="pelisalacarta - Menu Options">
                <widget source="itemname" transparent="1" render="Label" zPosition="2" position="10,180" size="380,20" font="Regular;16" />
                <widget source="menu" render="Listbox" zPosition="5" transparent="1" position="10,10" size="380,160" scrollbarMode="showOnDemand" >
                    <convert type="StringList" />
                </widget>
            </screen>"""

        list = []
        self.movieinfo = movieinfo
        if self.movieinfo[7] == "bookmark":
            list.append(("Delete selected bookmark", "delbookmark", "menu_delbookmark", "50"))
        elif self.movieinfo[6] == "movie":
            list.append(("Bookmark selected movie", "addbookmark", "menu_addbookmark", "50"))
        elif self.movieinfo[6] == "cat":
            list.append(("Bookmark selected category", "addbookmark", "menu_addbookmark", "50"))
        list.append(("View Bookmarks", "viewbookmarks", "menu_viewbookmarks", "50"))
        list.append(("View Downloads", "viewdownloads", "menu_viewdownloads", "50"))
        list.append(("pelisalacarta Settings", "settingsmenu", "menu_settings", "50"))

        self["menu"] = List(list)
        self["itemname"] = StaticText(self.movieinfo[3])

        self["actions"] = ActionMap(["OkCancelActions"],
        {
            "cancel": self.Exit,
            "ok": self.okbuttonClick
        }, -1)

    def okbuttonClick(self):
        selection = self["menu"].getCurrent()
        if selection:
            if selection[1] == "addbookmark":
                os_system("echo '%s:::%s:::%s:::%s' >> /etc/enigma2/pelisalacarta.bookmarks" % (self.movieinfo[6], self.movieinfo[3], self.movieinfo[5], self.movieinfo[4]))
                self.Exit()
            if selection[1] == "delbookmark":
                bookmarkfile = "/etc/enigma2/pelisalacarta.bookmarks"
                if fileExists(bookmarkfile, 'r'):
                    tmpdata = ""
                    tmpfile = open(bookmarkfile, "r")
                    for line in tmpfile:
                        if self.movieinfo[5] not in line:
                            tmpdata = tmpdata + line + "\n"

                    tmpfile.close()
                    os_system("echo '%s' > %s" % (tmpdata,bookmarkfile))
                self.Exit()
            elif selection[1] == "viewbookmarks":
                self.session.open(Pelisalacarta, self.movieinfo[5], "Bookmarks", "Bookmarks from your favorite Movies")
            elif selection[1] == "viewdownloads":
                self.session.openWithCallback(self.Exit, Pelisalacarta_TaskViewer)
            elif selection[1] == "settingsmenu":
                self.session.openWithCallback(self.Exit, Pelisalacarta_Settings)
            else:
                self.Exit()
        else:
            self.Exit()

    def Exit(self, retval=None):
        self.close()


#------------------------------------------------------------------------------------------


class Pelisalacarta_TaskViewer(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        self.skin = """
            <screen name="MediathekTasksScreen" position="center,center" size="700,550" title="pelisalacarta - Active Downloads">
                <widget source="tasklist" render="Listbox" position="30,120" size="640,370" zPosition="7" scrollbarMode="showOnDemand" transparent="1" >
                    <convert type="TemplatedMultiContent">
                        {"template": [
                                MultiContentEntryText(pos = (0, 1), size = (200, 24), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 1 is the name
                                MultiContentEntryText(pos = (210, 1), size = (150, 24), font=1, flags = RT_HALIGN_RIGHT, text = 2), # index 2 is the state
                                MultiContentEntryProgress(pos = (370, 1), size = (100, 24), percent = -3), # index 3 should be progress 
                                MultiContentEntryText(pos = (480, 1), size = (100, 24), font=1, flags = RT_HALIGN_RIGHT, text = 4), # index 4 is the percentage
                            ],
                        "fonts": [gFont("Regular", 22),gFont("Regular", 18)],
                        "itemHeight": 25
                        }
                    </convert>
                </widget>
                <ePixmap position="220,500" zPosition="4" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
                <widget name="key_red" position="220,500" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
            </screen>"""
        
        self["shortcuts"] = ActionMap(["SetupActions", "ColorActions"],
        {
            "ok": self.keyOK,
            "cancel": self.keyClose,
            "red": self.keyClose
        }, -1)

        self["tasklist"] = List([])
        self["key_red"] = Button(_("Close"))
        
        self.Timer = eTimer()
        self.Timer.callback.append(self.TimerFire)

        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)
        
    def __onClose(self):
        del self.Timer

    def layoutFinished(self):
        self.Timer.startLongTimer(2)

    def TimerFire(self):
        self.Timer.stop()
        self.rebuildTaskList()
    
    def rebuildTaskList(self):
        self.tasklist = []
        for job in JobManager.getPendingJobs():
            self.tasklist.append((job, job.name, job.getStatustext(), int(100*job.progress/float(job.end)) ,str(100*job.progress/float(job.end)) + "%" ))
        self['tasklist'].setList(self.tasklist)
        self['tasklist'].updateList(self.tasklist)
        self.Timer.startLongTimer(2)

    def keyOK(self):
        current = self["tasklist"].getCurrent()
        if current:
            job = current[0]
            self.session.openWithCallback(self.JobViewCB, JobView, job)
    
    def JobViewCB(self, why):
        pass

    def keyClose(self):
        self.close()

#------------------------------------------------------------------------------------------

class Pelisalacarta_Settings(Screen, ConfigListScreen):
    skin = """
        <screen name="MultiMediathekSettings" position="center,center" size="560,330" title="pelisalacarta - Settings">
            <widget name="config" position="10,10" size="540,250" scrollbarMode="showOnDemand" />
            <ePixmap name="red"    position="0,280"   zPosition="4" size="140,40" pixmap="/usr/share/enigma2/skin_default/buttons/red.png" transparent="1" alphatest="on" />
            <ePixmap name="green"  position="140,280" zPosition="4" size="140,40" pixmap="/usr/share/enigma2/skin_default/buttons/green.png" transparent="1" alphatest="on" />
            <ePixmap name="yellow" position="280,280" zPosition="4" size="140,40" pixmap="/usr/share/enigma2/skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
            <ePixmap name="blue"   position="420,280" zPosition="4" size="140,40" pixmap="/usr/share/enigma2/skin_default/buttons/blue.png" transparent="1" alphatest="on" />
            <widget name="key_red" position="0,280" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
            <widget name="key_green" position="140,280" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
            <widget name="key_yellow" position="280,280" zPosition="5" size="140,40" valign="center" halign="center"  font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
            <widget name="key_blue" position="420,280" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)

        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("OK"))
        self["key_yellow"] = Button("")
        self["key_blue"] = Button("")

        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
        {
            "ok": self.keySave,
            "green": self.keySave,
            "red": self.keyCancel,
            "cancel": self.keyCancel
        }, -2)

        self.setTitle("pelisalacarta v%s - Settings" % config.plugins.pelisalacarta.version.value)

        self.oldadultcontentvalue = config.plugins.pelisalacarta.showadultcontent.value
        self.oldstoragepathvalue = config.plugins.pelisalacarta.storagepath.value

        self.cfglist = []
        self.cfglist.append(getConfigListEntry(_("Thumbnail Caching:"), config.plugins.pelisalacarta.imagecache))
        self.cfglist.append(getConfigListEntry(_("Thumbnail Scaling Mode:"), config.plugins.pelisalacarta.imagescaling))
        self.cfglist.append(getConfigListEntry(_("Thumbnail Scaler:"), config.plugins.pelisalacarta.imagescaler))
        self.cfglist.append(getConfigListEntry(_("Show Adult Content:"), config.plugins.pelisalacarta.showadultcontent))
        #self.cfglist.append(getConfigListEntry(_("Show Secret Content:"), config.plugins.pelisalacarta.showsecretcontent))
        self.cfglist.append(getConfigListEntry(_("Download Directory:"), config.plugins.pelisalacarta.moviedir))
        self.cfglist.append(getConfigListEntry(_("Cache Folder:"), config.plugins.pelisalacarta.storagepath))


        self.cfglist.append(getConfigListEntry(_("Cuenta MocosoftX:"), config.plugins.pelisalacarta.mocosoftxaccount))
        self.cfglist.append(getConfigListEntry(_("Login:"), config.plugins.pelisalacarta.mocosoftxuser))
        self.cfglist.append(getConfigListEntry(_("Password:"), config.plugins.pelisalacarta.mocosoftxpassword))
        self.cfglist.append(getConfigListEntry(_("Cuenta Series.ly:"), config.plugins.pelisalacarta.mocosoftxaccount))
        self.cfglist.append(getConfigListEntry(_("Login:"), config.plugins.pelisalacarta.serieslyuser))
        self.cfglist.append(getConfigListEntry(_("Password:"), config.plugins.pelisalacarta.serieslypassword))

        ConfigListScreen.__init__(self, self.cfglist, session)

    def keySave(self):
        config.plugins.pelisalacarta.save()

        if config.ParentalControl.configured.value and config.plugins.pelisalacarta.showadultcontent.value and config.plugins.pelisalacarta.showadultcontent.value != self.oldadultcontentvalue:
            pinList = self.getPinList()
            self.session.openWithCallback(self.pinEntered, PinInput, pinList=pinList, triesEntry=config.ParentalControl.retries.setuppin, title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))

        if not os_path.isdir(config.plugins.pelisalacarta.storagepath.value):
            self.session.open(MessageBox, "The directory %s does not exist!" % config.plugins.pelisalacarta.storagepath.value, MessageBox.TYPE_ERROR)
            return

        if config.plugins.pelisalacarta.storagepath.value != self.oldstoragepathvalue:
            os_system("rm -rf "+self.oldstoragepathvalue+"/pelisalacarta")
            os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta")
            os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/images")
            os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/movies")
            os_system("mkdir -p "+config.plugins.pelisalacarta.storagepath.value+"/pelisalacarta/tmp")

        configfile.save()
        self.close()

    def keyCancel(self):
        for item in self.cfglist:
            item[1].cancel()
        self.close()

    def getPinList(self):
        pinList = []
        pinList.append(config.ParentalControl.setuppin.value)
        for x in config.ParentalControl.servicepin:
            pinList.append(x.value)
        return pinList

    def pinEntered(self, result):
        if result is None:
            config.plugins.pelisalacarta.showadultcontent.value = False
            config.plugins.pelisalacarta.save()
        elif not result:
            config.plugins.pelisalacarta.showadultcontent.value = False
            config.plugins.pelisalacarta.save()

#------------------------------------------------------------------------------------------

def main(session, **kwargs):
    print "[pelisalacarta] main"
    session.open(Pelisalacarta)

def Plugins(**kwargs):
    print "[pelisalacarta] Plugins"
    return [
        PluginDescriptor(name = "pelisalacarta", description = "pelisalacarta 3.2.24 para Dreambox", icon="plugin-icon.png", where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main),
        PluginDescriptor(name = "pelisalacarta", description = "pelisalacarta 3.2.24 para Dreambox", icon="plugin-icon.png", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]
