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

register.channelRegister.append('chn_cinetube.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="cinetube")')


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
        self.icon = "cinetube-icon.png"
        self.iconLarge = "cinetube-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Cinetube"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "www.cinetube.es"
        self.moduleName = "chn_cinetube.py"
        self.mainListUri = "http://www.cinetube.es/subindices/iserienovedades.html"
        self.baseUrl = "http://www.cinetube.es/"
        self.baseUrlLevel2 = "http://www.cinetube.es/subindices/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        self.episodeItemRegex = 'xxxyyyzz'

        self.videoSort = False

        patronvideos  = '<tr>[^<]*<td(?: class="top")?>'
        patronvideos += '<img src="([^"]+)".*?'
        patronvideos += '<a href="([^"]+)".*?>(.*?)</a>(.*?)</tr>'
        self.folderItemRegex = patronvideos

        #self.videoItemRegex  = patronvideos
        self.videoItemRegex  = ""

        self.mediaUrlRegex = '<a href="http\:\/\/www.megavideo.com/\?v\=([0-9A-Z]+)'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Peliculas", "http://www.cinetube.es/subindices/inovedades.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Series", "http://www.cinetube.es/subindices/iserienovedades.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Documentales", "http://www.cinetube.es/subindices/idocumentalesnovedades.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Anime - Series", "http://www.cinetube.es/subindices/ianimeseries.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Anime - Peliculas", "http://www.cinetube.es/subindices/ianimepeliculas.html" )
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
            titulo = unicode( resultSet[2], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[2]

        url = urlparse.urljoin(self.baseUrlLevel2,resultSet[1])
        item = common.clistItem(titulo,url)
        
        # procesa el resto
        item.description = ""
        resto = resultSet[3]
        #logFile.debug("resto="+resto)
        
        item.description = ""
        argumento = common.DoRegexFindAll("SINOPSIS:(.*?)</div>", resto)
        if len(argumento)>0:
            logFile.info('argumento[0]=' + argumento[0])
            try:
                item.description = unicode( argumento[0], "utf-8" ).encode("iso-8859-1")
            except:
                item.description = argumento[0]
        
        matches = common.DoRegexFindAll('<img.*?alt="([^"]+)"', resto)
        conectores = ""
        for match in matches:
            logFile.debug("conector="+match)
            conectores = conectores + match + "/"
        if len(matches)>0:
            item.name = item.name + " (" + conectores[:-1] + ")"
        
        item.icon = self.folderIcon
        item.type = 'folder'
        item.thumbUrl = resultSet[0]
        item.complete = False
        return item

    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        return common.clistItem("vacio","")

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []
        
        # Busca los enlaces a los mirrors
        patronvideos  = '<iframe src="(.*?/subindices/[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        for match in matches:
            logFile.info("Encontrado iframe mirrors "+matches[0])
            # Lee el iframe
            url = urlparse.urljoin(self.baseUrlLevel2,matches[0].replace(" ","%20"))
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            
            # saca los enlaces
            patronvideos  = '<a href="(../[^"]+)"[^>]+>([^<]+)</a>'
            matches2 = re.compile(patronvideos,re.DOTALL).findall(data)
            
            # Los añade como folders
            for match2 in matches2:
                logFile.info("Encontrado mirror "+match2[0])
                item = common.clistItem(match2[1],urlparse.urljoin(self.baseUrlLevel2,match2[0]).replace(" ","%20"))
                item.description = ""
                item.icon = self.folderIcon
                item.type = 'folder'
                item.thumb = self.noImage
                item.complete = True
                _items.append( item )

        encontrados = set()

        # Megavideo - Vídeos con título
        logFile.info("1) Megavideo con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            titulo = titulo + " (id "+match[1]+")"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("2) Megavideo sin titulo...")
        patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin título (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("3) Vreel con título...")
        patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Vreel - Vídeos con título
        logFile.info("4) Vreel con titulo...")
        patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = match[0].strip()
            if titulo == "":
                titulo = "Sin título"
            url = match[1]
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("5) wuapi sin título")
        patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match[23:]+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # WUAPI
        logFile.info("6) wuapi sin título...")
        patronvideos  = '(http://wuapi.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match[23:]+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Wuapi" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # STAGEVU
        logFile.info("7) Stagevu sin título...")
        patronvideos  = '"(http://stagevu.com[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("8) Tu.tv sin título...")
        patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # TUTV
        logFile.info("9) Tu.tv sin título...")
        #<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
        patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin título ("+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "tu.tv" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        # Megavideo - Vídeos sin título
        logFile.info("10 ) Megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # Megavideo - Vídeos sin título
        logFile.info("11) Megavideo sin titulo...")
        patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Megavideo" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)

        # STAGEVU
        logFile.info("12) Stagevu...")
        patronvideos  = '(http://stagevu.com[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Stagevu" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
            
        # Vreel - Vídeos sin título
        logFile.info("13) Vreel sin titulo...")
        patronvideos  = '(http://beta.vreel.net[^<]+)<'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        for match in matches:
            titulo = "Sin titulo (id "+match+")"
            url = match
            if url not in encontrados:
                _items.append( self.nuevoVideoItem( titulo , url , "Vreel" ) )
                encontrados.add(url)
            else:
                logFile.info("  url duplicada="+url)
        
        return (data, _items)

    def nuevoVideoItem( self , titulo , url , tipo ):
        logFile.info("  Detectado vídeo "+tipo+" (titulo=#"+titulo+"#) (url=#"+url+"#)")
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

        if item.date == "Megavideo":
            item.mediaurl = megavideo.Megavideo(item.url)
            
        if item.date == "Wuapi":
            item.mediaurl = wuapi.Wuapi(item.url)
            
        if item.date == "Vreel":
            item.mediaurl = vreel.Vreel(item.url)

        if item.date == "Stagevu":
            item.mediaurl = stagevu.Stagevu(item.url)
        
        if item.date == "tu.tv":
            item.mediaurl = tutv.Tutv(item.url)

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
