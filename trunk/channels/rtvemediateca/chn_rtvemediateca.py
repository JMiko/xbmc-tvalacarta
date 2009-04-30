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
import parameters

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

register.channelRegister.append('chn_rtvemediateca.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="rtvemediateca")')

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
        self.icon = "rtvemediateca-icon.png"
        self.iconLarge = "rtvemediateca-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "RTVE Mediateca"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "Todos los vídeos de TVE"
        self.moduleName = "chn_rtvemediateca.py"
        self.mainListUri = 'http://www.rtve.es/mediateca/videos/'
        self.baseUrl = 'http://www.rtve.es/mediateca/video/'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))

        self.requiresLogon = False

        # Canales
        self.episodeItemRegex = '<span onclick="loadVideos\(\'([^\']+)\'\);" class="closed">([^<]+)</span>'

        # Subcanales
        self.folderItemRegex = '<a href="javascript://" onclick="loadVideos\(\'([^\']+)\'\);" class="inf">([^<]+)</a>'

        # Vídeos
        self.videoItemRegex = '<div class="vthumb">.*?<a href="([^"]+)"><img src="[^>]+><img src="([^"]+)[^>]+>.*?<a href=[^>]+>([^<]+)<'

        # FLV
        self.mediaUrlRegex = 'addVariable\("file","([^"]+)"\)'

        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s (trace)', self.channelName)
        return True

   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Noticias", "http://www.rtve.es/mediateca/video/noticias/medialist.inc" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Deportes", "http://www.rtve.es/mediateca/video/deportes/medialist.inc" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Programas", "http://www.rtve.es/mediateca/video/programas/medialist.inc" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Archivo", "http://www.rtve.es/mediateca/video/archivo/medialist.inc" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        self.mainListItems = items

        return items
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        logFile.debug('CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        logFile.debug("urlelegido="+self.urlelegido)
        
        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        
        url = "http://www.rtve.es/mediateca/video/"+resultSet[0]+"/pagines_ajax/pagina1.html"
        logFile.debug("url="+url)

        item = common.clistItem(titulo,url)
        item.description = item.name
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumbUrl = resultSet[1]
        item.thumb = self.noImage
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        logFile.debug('CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)
        logFile.debug("urlelegido="+self.urlelegido)

        try:
            titulo = unicode( resultSet[2], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[2]

        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        logFile.debug("url="+url)
        item = common.clistItem( titulo , url )

        descripcion = resultSet[2]
        try:
            item.description = unicode( descripcion , "utf-8" ).encode("iso-8859-1")
        except:
            item.description = descripcion

        item.thumbUrl = urlparse.urljoin(self.baseUrl,resultSet[1])
        logFile.debug("item.thumbUrl="+item.thumbUrl)

        item.date = "."
        item.icon = "newmovie.png"
        item.type = 'video'
        item.mediaurl = ""
        item.complete = False

        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        logFile.info('item.url='+item.url)

        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)
        #logFile.debug("item.mediaurl="+item.mediaurl)
        
        # Averigua la URL
        body = uriHandler.Open(item.url, pb=False)
        matches = common.DoRegexFindAll(self.mediaUrlRegex, body)
        logFile.info('matches[0]='+matches[0])
        item.mediaurl = urlparse.urljoin(self.baseUrl,matches[0])
        logFile.info('item.mediaurl='+item.mediaurl)

        item.complete = True

        return item

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []
        logFile.debug("urlelegido="+self.urlelegido)
        
        if self.urlelegido.endswith("pagina1.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 2",self.urlelegido.replace("pagina1","pagina2"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        if self.urlelegido.endswith("pagina2.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 3",self.urlelegido.replace("pagina2","pagina3"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        if self.urlelegido.endswith("pagina3.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 4",self.urlelegido.replace("pagina3","pagina4"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        if self.urlelegido.endswith("pagina4.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 5",self.urlelegido.replace("pagina4","pagina5"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        if self.urlelegido.endswith("pagina5.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 6",self.urlelegido.replace("pagina5","pagina6"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        if self.urlelegido.endswith("pagina6.html"):
            logFile.debug("Añade nueva página")
            siguiente = common.clistItem("Página 7",self.urlelegido.replace("pagina6","pagina7"))
            siguiente.description = siguiente.name
            siguiente.icon = self.folderIcon
            siguiente.type = 'folder'
            siguiente.thumb = self.noImage
            siguiente.complete = True
            _items.append( siguiente )

        return (data, _items)
        
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

    def CtMnDownloadItem(self, selectedIndex):
        item = self.listItems[selectedIndex]
        logFile.info(item)
        self.listItems[selectedIndex] = self.DownloadEpisode(item)


    #============================================================================== 
    def DownloadEpisode(self, item):

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("rtve.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("rtve.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " [rtve.es]"
            baseFilename = baseFilename.replace("á","a")
            baseFilename = baseFilename.replace("é","e")
            baseFilename = baseFilename.replace("í","i")
            baseFilename = baseFilename.replace("ó","o")
            baseFilename = baseFilename.replace("ú","u")
            baseFilename = baseFilename.replace("ñ","n")
            baseFilename = baseFilename.replace("\"","")
            baseFilename = baseFilename.replace("\'","")
            baseFilename = baseFilename.replace(":","")
            
            if item.mediaurl=="":
                logFile.error("Cannot determine mediaurl")
                return item

            # Genera el fichero .NFO
            if parameters.getConfigValue("all.use.long.filenames","true")!="true":
                baseFilename = uriHandler.CorrectFileName(baseFilename)

            destFilename = baseFilename+".flv"
            configfilepath = os.path.join(destFolder,baseFilename+".nfo")
            logFile.info("outfile="+configfilepath)
            outfile = open(configfilepath,"w")
            outfile.write("<movie>\n")
            outfile.write("<title>"+item.name+"</title>\n")
            outfile.write("<originaltitle></originaltitle>\n")
            outfile.write("<rating>0.000000</rating>\n")
            outfile.write("<year>2009</year>\n")
            outfile.write("<top250>0</top250>\n")
            outfile.write("<votes>0</votes>\n")
            outfile.write("<outline>"+item.description+"</outline>\n")
            outfile.write("<plot>"+item.description+"</plot>\n")
            outfile.write("<tagline>"+item.description+"</tagline>\n")
            outfile.write("<runtime></runtime>\n")
            outfile.write("<thumb>"+item.thumbUrl+"</thumb>\n")
            outfile.write("<mpaa>Not available</mpaa>\n")
            outfile.write("<playcount>0</playcount>\n")
            outfile.write("<watched>false</watched>\n")
            outfile.write("<id>tt0432337</id>\n")
            outfile.write("<filenameandpath>"+os.path.join(destFolder,destFilename)+"</filenameandpath>\n")
            outfile.write("<trailer></trailer>\n")
            outfile.write("<genre></genre>\n")
            outfile.write("<credits></credits>\n")
            outfile.write("<director></director>\n")
            outfile.write("<actor>\n")
            outfile.write("<name></name>\n")
            outfile.write("<role></role>\n")
            outfile.write("</actor>\n")
            outfile.write("</movie>")
            outfile.flush()
            outfile.close()
            
            logFile.info("Going to download %s", destFilename)
            downLoader = uriHandler.Download(item.mediaurl, destFilename, destFolder)

            item.downloaded = True
            return item
        else:
            logFile.warning('Error determining folder/video type of selected item');
