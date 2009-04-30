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

import urllib2,urllib

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

register.channelRegister.append('chn_terratv.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="terratv")')

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
        self.icon = "terratv-icon.png"
        self.iconLarge = "terratv-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "terra.tv"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_terratv.py"
        self.mainListUri = 'http://www.terra.tv/'
        self.baseUrl = 'http://www.terra.tv/'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using ExtPlayer", "CtMnPlayExtPlayer", itemTypes="video", completeStatus=True))

        self.requiresLogon = False

        # Canales
        patronvideos  = '<li class="(?:subMenu|first|)"><a.*?href="([^"]+)".*?><span[^>]+>([^<]+)</span></a>'
        self.episodeItemRegex = patronvideos

        # Submenu
        self.folderItemRegex = '<ul class="paginacao">.*?<li><a class="bt" title="pr.ximo" style="cursor:pointer" onclick="ajaxManagerCache.Add\(\'([^\']+)\''

        # Vídeos
        self.videoItemRegex = '<li>[^<]+<div class="img">[^<]+<a href="([^"]+)"[^>]+>[^<]+<img src="([^"]+)".*?<a[^>]+>([^<]+)<.*?<a[^>]+>([^<]+)<'

        # FLV
        self.mediaUrlRegex = "'(http\:\/\/www\.terra\.tv\/templates\/getVideo\.aspx[^']+)'"
        #mi.urlWm            = 'http://www.terra.tv/templates/getVideo.aspx?contentid=101330&highdef=False&ts=20090417134150&country=es&service=GEOLOC_TVC-GEO&hash=38582BE7FB35AB1DA414213675B20221&flash=False';

        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s (trace)', self.channelName)
        return True

    #==============================================================================
    def ParseMainList(self):
        items = chn_class.Channel.ParseMainList(self)        
        
        nuevo = common.clistItem("(Buscador)", "searchSite" )
        nuevo.icon = self.folderIcon
        items.insert(0, nuevo)
        
        return items

    #==============================================================================
    def SearchSite(self):
        items = []
        
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)>0:
                tecleado = tecleado.replace(" ", "+")
                searchUrl = 'http://www.terra.tv/templates/searchResult.aspx?keyword='+tecleado
                return self.ProcessFolderList(searchUrl,"GET")
                
        return items
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        logFile.debug('CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        url = url.replace("&amp;","&")
        logFile.debug("url="+url)
        
        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        
        item = common.clistItem( titulo, url )
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = "(Página siguiente)"
        url = 'http://www.terra.tv/templates/'+resultSet.replace("&amp;","&")
        item = common.clistItem(titulo,url)
        
        item.description = ""
        item.icon = self.folderIcon
        item.type = 'folder'
        item.complete = True
        return item

    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        logFile.debug('CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        try:
            titulo = unicode( resultSet[2] + " " + resultSet[3], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[2] + " " + resultSet[3]

        logFile.debug("titulo="+titulo)
        url = resultSet[0]
        logFile.debug("url="+url)
        item = common.clistItem( titulo , url )
        
        descripcion = titulo
        item.description = descripcion
        
        item.thumbUrl = resultSet[1]
        item.date = "."
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
        logFile.info('matches')
        logFile.info(matches)
        
        url = matches[0]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()

        patronvideos  = '<ref href="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        item.mediaurl = matches[ 0 ]
        logFile.debug("item.mediaurl="+item.mediaurl)

        item.complete = True

        return item

    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnPlayMplayer(self, selectedIndex):
        logFile.debug('Reproduce usando mplayer')
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, selectedIndex):
        logFile.debug('Reproduce usando dvdplayer')
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item,"dvdplayer")    
    
    def CtMnPlayExtPlayer(self, selectedIndex):
        logFile.debug('Reproduce usando extplayer')
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item,"extplayer")
