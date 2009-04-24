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
import megavideo, vreel, stagevu, tutv, wuapi

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

register.channelRegister.append('chn_pelis24.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="pelis24")')


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
        self.icon = "pelis24-icon.png"
        self.iconLarge = "pelis24-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Pelis24"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "www.pelis24.com"
        self.moduleName = "chn_pelis24.py"
        self.mainListUri = "http://pelis24.com/"
        self.baseUrl = "http://pelis24.com/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        # Los episiodios (nivel 1) están puestos a mano (menú de la página)
        self.episodeItemRegex = 'xxxyyyzz'
        
        # Las carpetas son cada una de las películas
        self.folderItemRegex = '<table class="contentpaneopen">[^<]+<tr[^<]+<td[^>]+>\s*([^<]+)</td>.*?<img src="([^"]+)"[^>]+>(.*?)</div>.*?<a href="([^#]+)#comment">.*?</table>'

        # Los enlaces a megavideo son las peliculas
        self.videoItemRegex  = 'xxxyyyzzz'

        # Aquí el vídeo sale directamente de la URL
        self.mediaUrlRegex = ''
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Peliculas", "http://pelis24.com/peliculas/" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Series", "http://pelis24.com/series/" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Novedades", "http://pelis24.com/" )
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
        titulo = resultSet[0]
        titulo = titulo.strip()
        url = urlparse.urljoin(self.baseUrl,resultSet[3])
        item = common.clistItem(titulo,url)
        
        descripcion = resultSet[2]
        descripcion = descripcion.strip()
        descripcion = descripcion.replace("<br />","")
        item.description = descripcion
        
        item.icon = self.folderIcon
        item.type = 'folder'
        
        #item.thumb = self.noImage
        item.thumbUrl = resultSet[1]
        item.complete = False
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        titulo = "Megavideo "+resultSet
        item = common.clistItem( titulo , resultSet )
        
        item.thumb = self.noImage
        item.description = ""
        item.date = "."
        item.icon = "newmovie.png"
        item.type = 'video'
        item.mediaurl = megavideo.Megavideo(resultSet)
        item.complete = True
        logFile.info('item.mediaurl=' + item.mediaurl)

        return item

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []

        try:
            # Primera página
            paginas = common.DoRegexFindAll('<a href="([^"]+)">Sigu', data)
            url = urlparse.urljoin(self.baseUrl,paginas[0])
            paginaitem = common.clistItem("#Siguiente",url)
            paginaitem.description = paginaitem.name
            paginaitem.icon = self.folderIcon
            paginaitem.type = 'folder'
            paginaitem.thumb = self.noImage
            paginaitem.complete = True
            _items.append(paginaitem)
        except:
            logFile.info("No encuentro la pagina...")

        encontrados = set()

        # STAGEVU
        logFile.info("1) stagevu...")
        #"http://stagevu.com/embed?width=465&height=232&uid=ovchyfbzzdvc"
        patronvideos  = '"http://stagevu.com.*?uid\=([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = "http://stagevu.com/video/"+match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Megavideo - Vídeos con título
        logFile.info("2) megavideo con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0] + " ("+match[1]+")"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("3) megavideo sin titulo...")
        patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("4) vreel con titulo...")
        patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0]
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("5) vreel con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0]
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("6) wuapi...")
        patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[23:]
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("7) wuapi...")
        patronvideos  = '(http://wuapi.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[23:]
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # STAGEVU
        logFile.info("8) stagevu...")
        patronvideos  = '"(http://stagevu.com/video/[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("9) tutv...")
        patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("10) tutv...")
        #<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
        patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Megavideo - Vídeos sin título
        logFile.info("11) megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("12) megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # STAGEVU
        logFile.info("13) stagevu...")
        patronvideos  = '(http://stagevu.com/video/[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
            
        # Vreel - Vídeos sin título
        logFile.info("14) vreel sin titulo...")
        patronvideos  = '"(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
            
        # Vreel - Vídeos sin título
        logFile.info("15) vreel sin titulo...")
        patronvideos  = '[^"](http://beta.vreel.net[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        return (data, _items)

    def nuevoVideoItem( self , titulo , url , tipo ):
        logFile.info("  Detectado vídeo "+tipo+" ("+titulo+") ("+url+")")
        item = common.clistItem( titulo , url )
        item.thumb = self.noImage
        item.description = ""
        item.date = tipo
        item.icon = "newmovie.png"
        item.type = 'video'
        item.mediaurl = url
        item.complete = False
        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        logFile.info('Tipo de video='+item.date)

        item.description = "Vídeo disponible"
        try:
            if item.date == "Megavideo":
                item.mediaurl = megavideo.Megavideo(item.url)
                if item.mediaurl == "":
                    item.description = "Este vídeo ya no está no disponible en " + item.date
                
            if item.date == "Wuapi":
                item.mediaurl = wuapi.Wuapi(item.url)
                if item.mediaurl == "":
                    item.description = "Este vídeo ya no está no disponible en " + item.date
                
            if item.date == "Vreel":
                item.mediaurl = vreel.Vreel(item.url)
                if item.mediaurl == "":
                    item.description = "Este vídeo ya no está no disponible en " + item.date

            if item.date == "Stagevu":
                item.mediaurl = stagevu.Stagevu(item.url)
                if item.mediaurl == "":
                    item.description = "Este vídeo ya no está no disponible en " + item.date
            
            if item.date == "tu.tv":
                item.mediaurl = tutv.Tutv(item.url)
                if item.mediaurl == "":
                    item.description = "Este vídeo ya no está no disponible en " + item.date
        except:
            item.description = "Este vídeo ya no está no disponible en " + item.date

        logFile.info('item.mediaurl='+item.mediaurl)
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
