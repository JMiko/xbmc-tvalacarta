#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import config
import controls
import contextmenu
import chn_class

import urllib2,urllib,urlparse

logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

#===============================================================================
# register the channels
#===============================================================================
if (sys.modules.has_key('progwindow')):
    register = sys.modules['progwindow']
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin']
#register.channelButtonRegister.append(108)

register.channelRegister.append('chn_rtvv.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="rtvv")')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """
    
    #===============================================================================
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        #self.guid = "3ac3d6d0-5b2a-11dd-ae16-0800200c9a66"
        self.icon = "rtvv-icon.png"
        self.iconLarge = "rtvv-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Valencia"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_rtvv.py"
        self.mainListUri = "http://www.rtvv.es/alacarta/princiv.asp"
        self.baseUrl = "http://www.rtvv.es/alacarta/princiv.asp"
        self.defaultPlayer = 'mplayer'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        self.episodeItemRegex = '<li><span><a href="(secciones.asp[^"]+)">([^<]+)<'
        self.videoItemRegex = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
        self.folderItemRegex = ''
        self.mediaUrlRegex = '<div id="reproductor">.*?<script.*?>.*?j_url="([^"]+)";.*?flashControl\("([^"]+)"'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s (trace)', self.channelName)
        return True

    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin(self.baseUrl,resultSet[0].replace("&amp;","&"))
        logFile.debug("url="+url)

        item = common.clistItem( titulo, url )
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        url = "http://www.rtvv.es/alacarta/secciones.asp"+resultSet[0].replace("&amp;","&")
        logFile.debug("url="+url)
        item = common.clistItem( titulo , url )
        
        descripcion = "%s" % resultSet[2]
        descripcion = descripcion.strip()
        descripcion = descripcion.replace("</a>","")
        descripcion = descripcion.replace("</p>","")
        descripcion = descripcion.replace("<p>","")
        item.description = common.ConvertHTMLEntities(descripcion)
        
        item.thumbUrl = urlparse.urljoin(self.baseUrl,resultSet[3]).replace(" ","%20")

        # TODO: Sacar la fecha de la descripcion
        matches = common.DoRegexFindAll("<p>Emissi&oacute;: ([^<]+)<", resultSet[2])
        item.date = "."
        if len(matches)>0:
            item.date = matches[0]
        item.icon = "newmovie.png"
        item.type = 'video'
        item.complete = False

        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)

        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # Averigua la URL
        body = uriHandler.Open(item.url, pb=False)
        matches = common.DoRegexFindAll(self.mediaUrlRegex, body)
        logFile.debug("matches")
        logFile.debug(matches)
        item.mediaurl = matches[0][1]+matches[0][0]
        logFile.debug("item.mediaurl="+item.mediaurl)
        
        # Completa la descripcion
        patronvideos = '<div id="encuesta">\s*<div class="cab">.*?</div>(.*?)</div>'
        matches=re.compile(patronvideos,re.DOTALL).findall(body)
        
        if len(matches)>0:
            descripcion = "%s" % matches[0]
            descripcion = descripcion.replace("<p>","")
            descripcion = descripcion.replace("</p>"," ")
            descripcion = descripcion.replace("<strong>","")
            descripcion = descripcion.replace("</strong>","")
            descripcion = descripcion.replace("<br />"," ")
            descripcion = descripcion.strip()
            descripcion = common.ConvertHTMLEntities(descripcion)
            item.description = descripcion

        item.complete = True

        return item

    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnDownloadItem(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.listItems[selectedIndex] = self.DownloadEpisode(item)

    def CtMnPlayMplayer(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, selectedIndex):
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item,"dvdplayer")    
    
    #============================================================================== 
    def DownloadEpisode(self, item):
        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            destFilename = item.name + ".flv"
            if item.mediaurl=="":
                logFile.error("Cannot determine mediaurl")
                return item
            logFile.info("Going to download %s", destFilename)
            downLoader = uriHandler.Download(item.mediaurl, destFilename)
            item.downloaded = True
            return item
        else:
            logFile.warning('Error determining folder/video type of selected item');
