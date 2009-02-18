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

register.channelRegister.append('chn_plus.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="plus")')

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
        self.icon = "plus-icon.png"
        self.iconLarge = "plus-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Canal Plus TV"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "Lo mejor de Canal+"
        self.moduleName = "chn_plus.py"
        self.mainListUri = "http://www.plus.es/tv/canales.html"
        self.baseUrl = "http://www.plus.es/tv/canales.html"
        #self.defaultPlayer = 'mplayer'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        #<li class="canales estirar">
        #<h2><a href="index.html?idList=PLTVCN">Cine </a></h2>
        #<a href="index.html?idList=PLTVCN"><img alt="imagen Cine " src="/images/plustv/categorias/PLTVCN.jpg"/></a>
        #<ul>
        #<li><span><a title="A los Oscar pongo por testigo: Polémica por el oscar de Heath Ledger" href="index.html?idList=PLTVCN&amp;idVid=767275&amp;pos=0">A los Oscar pongo por testigo: Polémica por el oscar de Heath Ledger</a></span></li><li><span><a title="Canal+ en Hollywood: Premios del Sindicato de Actores" href="index.html?idList=PLTVCN&amp;idVid=718639&amp;pos=1">Canal+ en Hollywood: Premios del Sindicato de Actores</a></span></li>
        #<li class="sinPlay"><a title="ver mas" href="emisiones.html?id=PLTVCN">Más ...</a></li>
        #</ul>
        #</li>
        self.episodeItemRegex = '<li class="canales estirar[^"]*">[^<]+<h2><a href="([^"]+)">([^<]+)</a>'

        #<li class="video estirar">
        #<div class="imagen">
        #<a title="Encuentros en el fin del mundo" href="index.html?idList=PLTVDO&amp;idVid=725903&amp;pos=0">
        #<img alt="" src="http://canalplus.ondemand.flumotion.com/canalplus/ondemand/plustv/NF754356.jpg">
        #<span>Play</span>
        #</a>
        #</div>
        #<div class="tooltip" title="El director Werner Herzog se adentra en la Antártida para retratar, por primera vez, las relaciones cotidianas que se establecen entre los habitantes de la estación (desde biólogos hasta conductores de camión) y la naturaleza que los rodea.">
        #<div class="textos">
        #<p class="titulo"><a href="index.html?idList=PLTVDO&amp;idVid=725903&amp;pos=0">Encuentros en el fin del mundo</a></p>
        self.videoItemRegex = '<li class="video estirar">[^<]+<div class="imagen">[^<]+<a title="[^"]+" href="([^"]+)">[^<]+<img alt="" src="([^"]+)">[^<]+<span>[^<]+</span>[^<]+</a>[^<]+</div>[^<]+<div class="tooltip" title="([^"]+)">[^<]+<div class="textos">[^<]+<p class="titulo"><a href="[^"]+">([^<]+)</a></p>'

        self.folderItemRegex = ''
        self.mediaUrlRegex = ''    # used for the UpdateVideoItem
        self.pageNavigationRegex = 'ssssssssssssssssssss'
        self.pageNavigationRegexIndex = 1 
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = ""
        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        laurl = "http://www.plus.es/tv/" + resultSet[0].replace("index.html?idList","emisiones.html?id")
        logFile.debug("laurl="+laurl)

        item = common.clistItem( titulo, laurl )
        #item = common.clistItem( resultSet[1] , resultSet[1])
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
        
        urlfinal = "http://www.plus.es/tv/" + resultSet[0]
        logFile.debug("urldetalle="+urlfinal)
        item = common.clistItem( resultSet[3] , urlfinal )
        
        item.thumbUrl = resultSet[1]
        item.date = "."
        item.icon = "newmovie.png"
        item.description = resultSet[2]
        item.type = 'video'
        item.complete = False

        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)

        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True
        
        # Averigua la URL
        # URL Detalle: http://www.plus.es/tv/index.html?idList=PLTVDO&amp;idVid=725903&amp;pos=0
        # URL XML vídeo: http://www.plus.es/tv/bloques.html?id=0&idList=PLTVDO&idVid=725903
        #<?xml version="1.0" encoding="iso-8859-1"?>
        #<bloque modo="U">
        #<video tipo="P" url="http://canalplus.ondemand.flumotion.com/canalplus/ondemand/plustv/GF755806.flv" title=""></video>
        #<video tipo="T" url="http://canalplus.ondemand.flumotion.com/canalplus/ondemand/plustv/NF754356.flv" title="Encuentros en el fin del mundo"></video>
        #</bloque>
        idCategoria = common.DoRegexFindAll("idList=([^&]+)&", item.url)
        logFile.info('idCategoria='+idCategoria[0])
        idVideo = common.DoRegexFindAll("idVid=(\d+)", item.url)
        logFile.info('idVideo='+idVideo[0])
        urldetalle = "http://www.plus.es/tv/bloques.html?id=0&idList=" + idCategoria[0] + "&idVid=" + idVideo[0]
        bodydetalle = uriHandler.Open(urldetalle, pb=False)
        logFile.info(bodydetalle)
        enlacevideo = common.DoRegexFindAll('<video tipo="T" url="([^"]+)"', bodydetalle)
        logFile.info("enlacevideo="+enlacevideo[0])
        #enlacevideo = 
        item.mediaurl = enlacevideo[0]

        return item

     #==============================================================================
    def CreatePageItem(self, resultSet):
        """
        Accepts an resultset
        """
        logFile.debug("Starting CreatePageItem")
        logFile.debug(resultSet)
        logFile.debug(self.mainListItems[self.elegido].url)
        
        item = common.clistItem("Pg%s" % resultSet, '%s?page=%s' % (self.mainListItems[self.elegido].url , resultSet) )
        item.type = "page"
        logFile.debug("Created '%s' for url %s", item.name, item.url)
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

