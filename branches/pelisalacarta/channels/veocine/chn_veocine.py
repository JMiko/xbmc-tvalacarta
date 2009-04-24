#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os
import urlparse, urllib, urllib2
#===============================================================================
# Make global object available
#===============================================================================
import common
import config
import controls
import contextmenu
import chn_class
import megavideo

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

register.channelRegister.append('chn_veocine.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="veocine")')


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
        self.icon = "veocine-icon.png"
        self.iconLarge = "veocine-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Veocine"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "www.veocine.es"
        self.moduleName = "chn_veocine.py"
        self.mainListUri = "http://www.veocine.es/"
        self.baseUrl = "http://www.veocine.es/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        self.episodeItemRegex = 'xxxyyyzz'

        self.videoSort = False

        # Los enlaces a megavideo son las peliculas
        patronvideos  = 'reproductor.php\?video=([^\&]+)\&(?:amp\;)?media=([^\&]+)\&(?:amp\;)?titulo=([^"]+)"'
        self.videoItemRegex  = patronvideos

        # Las carpetas son las peliculas
        patronvideos  = '<tr.*?'
        patronvideos += '<td.*?'
        patronvideos += '<a href="([^"]+)">'
        patronvideos += "<img src='([^']+)'.*?<a.*?>\s*(.*?)\s*<(.*?)"
        patronvideos += "<img .*? alt='([^']+)' />"
        self.folderItemRegex = patronvideos

        self.mediaUrlRegex = ''
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Peliculas", "http://www.veocine.es/peliculas.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Series", "http://www.veocine.es/series.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Documentales", "http://www.veocine.es/documentales.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Peliculas infantiles", "http://www.veocine.es/infantil.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Peliculas VOS", "http://www.veocine.es/peliculavos.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Anime", "http://www.veocine.es/anime.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        self.mainListItems = items

        return items

    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        try:
            titulo = unicode( resultSet[2], "utf-8" ).encode("iso-8859-1") + " (" + resultSet[4] + ")"
        except:
            titulo = resultSet[2] + " (" + resultSet[4] + ")"
        url = urlparse.urljoin("http://www.veocine.es/",resultSet[0])
        item = common.clistItem(titulo,url)
        try:
            descripcion = unicode( resultSet[3], "utf-8" ).encode("iso-8859-1")
        except:
            descripcion = resultSet[3]

        descripcion = descripcion.replace("/a>","\n")
        descripcion = descripcion.replace("<br />","\n")
        descripcion = descripcion.replace("<b>","")
        descripcion = descripcion.replace("</b>","")
        descripcion = descripcion.replace("<i>","")
        descripcion = descripcion.replace("</i>","")
        descripcion = descripcion.replace("<!--colorstart:#589BB9-->","")
        descripcion = descripcion.replace("<!--colorend-->","")
        descripcion = descripcion.replace("<!--/colorend-->","")
        descripcion = descripcion.replace("<!--/colorstart-->","")
        descripcion = descripcion.replace('<span style="color:#589BB9">',"")
        descripcion = descripcion.replace("</span>","")
        descripcion = descripcion.strip()
        descripcion = common.ConvertHTMLEntities(descripcion)

        item.description = descripcion
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumb = self.noImage
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        try:
            titulo = unicode( resultSet[2], "utf-8" ).encode("iso-8859-1") + " (" + resultSet[0] + ")"
        except:
            titulo = resultSet[2] + " (" + resultSet[0] + ")"
        item = common.clistItem( titulo , resultSet[0] )
        
        item.thumb = self.noImage
        item.description = ""
        item.date = resultSet[1]
        item.icon = "newmovie.png"
        item.type = 'video'
        item.complete = False
        logFile.info('item.mediaurl=' + item.mediaurl)

        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        logFile.info('Tipo de video='+item.date)
        item.mediaurl = megavideo.Megavideo(item.url)
        logFile.info('item.mediaurl=' + item.mediaurl)
        item.complete = True
        return item

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []

        try:
            # Primera página
            paginas = common.DoRegexFindAll("<a href='([^']+)'>Siguiente</a>", data)
            url = urlparse.urljoin("http://www.veocine.es/",paginas[0])
            paginaitem = common.clistItem("#Siguiente",url)
            paginaitem.description = paginaitem.name
            paginaitem.icon = self.folderIcon
            paginaitem.type = 'folder'
            #item.thumb = self.CacheThumb(resultSet[1])
            paginaitem.thumb = self.noImage
            paginaitem.complete = True
            _items.append(paginaitem)
        except:
            logFile.info("No encuentro la pagina...")

        return (data, _items)

    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnDownloadItem(self, selectedIndex):
        item = self.listItems[selectedIndex]
        logFile.info(item)
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
