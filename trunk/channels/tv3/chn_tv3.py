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

register.channelRegister.append('chn_tv3.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="tv3")')

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
        self.icon = "tv3-icon.png"
        self.iconLarge = "tv3-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "TV3"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "3alacarta"
        self.moduleName = "chn_tv3.py"
        self.mainListUri = ""
        self.baseUrl = "http://www.tv3.cat/seccio/3alacarta"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))

        self.requiresLogon = False
        
        # El primer nivel es fijo
        self.episodeItemRegex = 'nohaynadaquecumplaestaexpresionregular'
        
        #<li>
        #<div class="img_p_txt_mes_a">
        #<div class="img_left">
        #<a title="El cor - Capítol 1718" href="/videos/983419/El-cor---Capitol-1718">
        #<img src="http://www.tv3.cat/multimedia/jpg/2/9/1232710323192.jpg" alt="El cor - Capítol 1718" class="w_petita" />
        #</a>
        #<a href="#"></a>
        #</div>
        #<div class="titulars1">
        #<span class="avant">El cor de la ciutat - 30/01/2009</span>
        #<br />
        #<h2>
        #<a title="El cor - Capítol 1718" href="/videos/983419/El-cor---Capitol-1718">El cor - Capítol 1718</a>
        #</h2>
        #<p>Mal dia per a en Beni per culpa d'en "Joan", però un vell conegut pot fer que en Iago encara ho passi pitjor. La Pilar, desesperada amb la Roser, sembla que troba ajuda. A ca n'Orpinell agafen un professor particular per a en Juli, i ni s'imaginen qui els assignaran...</p>
        #</div>

        #self.videoItemRegex = '<li>\W*<div class="img_p_txt_mes_a">\W*<div class="img_left">\W*<a title="[^"]+" href="([^"]+)">\W*<img src="([^"]+)" alt="[^"]+" class="w_petita" />\W*</a>\W*<a href="#"></a>\W*</div>\W*<div class="titulars1">\W*<span class="avant">([^<]+)</span>\W*<br />\W*<h2>\W*<a title="[^"]+" href="[^"]+">([^<]+)</a>\W*</h2>\W*<p>([^"]+)</p>\W*</div>'
        self.videoItemRegex = '<li>\W*<div class="img_p_txt_mes_a">\W*<div class="img_left">\W*<a title="(?:")?[^"]+"(?:")? href="([^"]+)">\W*<img src="([^"]+)" [^>]+>\W*</a>\W*<a href="#"></a>\W*</div>\W*<div class="titulars1">\W*<span class="avant">([^<]+)</span>\W*<br />\W*<h2>\W*<a [^>]+>([^<]+)</a>\W*</h2>\W*<p>([^<]+)</p>\W*</div>'
        #self.videoItemRegex = '<li>[^<]+<div[^>]+>[^<]+<div[^>]+>[^<]+<a([^>]+)>' #(?:")?[^"]+"(?:")? href="([^"]+)">\W*<img src="([^"]+)" [^>]+>\W*</a>\W*<a href="#"></a>\W*</div>\W*<div class="titulars1">\W*<span class="avant">([^<]+)</span>\W*<br />\W*<h2>\W*<a [^>]+>([^<]+)</a>\W*</h2>\W*<p>([^"]+)</p>\W*</div>'
        
        # ir a página 2 (frmsearcher, 51)
        # http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=51&hiTarget=searchingVideos.jsp&acat=TSERIES&hiCategory=VID&textBusca=&startDate=&endDate=31%2F01%2F2009
        # if a página 3 (javascript:send('frmSearcher',101))
        # http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=101&hiTarget=searchingVideos.jsp&acat=TSERIES&hiCategory=VID&textBusca=&startDate=&endDate=31%2F01%2F2009
        #self.folderItemRegex = "javascript:send\('frmSearcher',(\d+)\)"
        self.folderItemRegex = ""
        self.mediaUrlRegex = '<location>([^<]+)</location>'    # used for the UpdateVideoItem
        self.pageNavigationRegex = '\?page=(\d+)'
        self.pageNavigationRegexIndex = 1 
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Sèries", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TSERIES" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Actualitat", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TACTUALITA" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Esports", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TESPORTS" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Cuina", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TCUINA" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Entretenimient", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TENTRETENI" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Divulgació", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TDIVULGACI" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Juvenil", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TJUVENIL" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Infantil", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TINFANTIL" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Música", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TMUSICA" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Gent TVC", "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?acat=TGENTTVC" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        self.mainListItems = items

        return items
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('******* NO SIRVE')
        item = common.clistItem( "null", "null" )
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug("###")
        logFile.debug(resultSet)
        
        # http://www.tv3.cat/videos/902809/El-cor---Capitol-1695    /videos/983419/El-cor---Capitol-1718
        # "La Franny i les sabates màgiques - 28/01/2009"
        titulo = resultSet[2][0:-13]
        logFile.debug("titulo="+titulo)
        fecha = resultSet[2][-10:]
        logFile.debug("fecha="+fecha)
        item = common.clistItem( titulo + " - " + resultSet[3] , "http://www.tv3.cat%s" % resultSet[0] )
        
        item.thumb = self.noImage
        item.thumbUrl = resultSet[1]
        
        item.date = fecha
        item.icon = "newmovie.png"
        item.description = resultSet[4]
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

        # Extrae el código (/videos/983419/El-cor---Capitol-1718)
        codigos = common.DoRegexFindAll("/videos/(\d+)/", item.url)
        logFile.info('item.url=' + item.url )
        logFile.info('codigos')
        logFile.info(codigos)
        codigo = codigos[0]
        
        urldetalle = "http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+codigo+"&QUALITY=H&FORMAT=FLV&rnd=481353"
        bodydetalle = uriHandler.Open(urldetalle, pb=False)
        logFile.info(bodydetalle)
        enlacevideo = common.DoRegexFindAll("(rtmp://[^\?]+)\?", bodydetalle)
        logFile.info(enlacevideo[0])
        #enlacevideo = 
        item.mediaurl = enlacevideo[0].replace('rtmp://flv-500-str.tv3.cat/ondemand/g/','http://flv-500.tv3.cat/g/')
        logFile.info(enlacevideo[0])
        item.complete = True
        return item

    
    #==============================================================================
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        logFile.info("Performing Pre-Processing")
        _items = []

        # Desde que numero debe empezar
        numeros = common.DoRegexFindAll("javascript:send\('frmSearcher',(\d+)\)", data)
        
        #<input type="hidden" name="acat" value="TINFANTIL"/>
        categoria = common.DoRegexFindAll('<input type="hidden" name="acat" value="([^"]+)"', data)
        
        #<input type="hidden" name="endDate" value="01/02/2009"/>
        fecha = common.DoRegexFindAll('<input type="hidden" name="endDate" value="([^"]+)"', data)

        logFile.debug(numeros)
        logFile.debug(categoria[0])
        logFile.debug(fecha[0])

        # Si hay 2, coger el primero
        # Si hay 4, coger los dos primeros
        if len(numeros) == 2:
            logFile.debug("hay 2 paginadores")
            txthiStartValue = numeros[0]
            urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
            logFile.debug(urlpaginador)
            nuevoitem = common.clistItem("Siguiente", urlpaginador )
            nuevoitem.description = ""
            nuevoitem.icon = self.folderIcon
            nuevoitem.thumb = self.noImage
            nuevoitem.complete = True
            nuevoitem.type = 'folder'
            _items.append(nuevoitem)
        else:
            logFile.debug("hay 4 paginadores")
            txthiStartValue = numeros[0]
            urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
            logFile.debug(urlpaginador)
            nuevoitem = common.clistItem("Anterior", urlpaginador )
            nuevoitem.description = ""
            nuevoitem.icon = self.folderIcon
            nuevoitem.thumb = self.noImage
            nuevoitem.complete = True
            nuevoitem.type = 'folder'
            _items.append(nuevoitem)
            
            txthiStartValue = numeros[1]
            urlpaginador = "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + txthiStartValue + "&hiTarget=searchingVideos.jsp&acat=" + categoria[0] + "&hiCategory=VID&textBusca=&startDate=&endDate=" + fecha[0].replace("/","%2F")
            logFile.debug(urlpaginador)
            nuevoitem = common.clistItem("Siguiente", urlpaginador )
            nuevoitem.description = ""
            nuevoitem.icon = self.folderIcon
            nuevoitem.thumb = self.noImage
            nuevoitem.complete = True
            nuevoitem.type = 'folder'
            _items.append(nuevoitem)
            
        return (data, _items)

    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        item = common.clistItem(resultSet, "http://www.tv3.cat/searcher/tvc/searchingVideos.jsp?hiPortal=tvc&hiSearchEngine=lucene&hiAdvanced=1&hiSearchIn=0&maxRowsDisplay=50&hiStartValue=" + resultSet + "&hiTarget=searchingVideos.jsp&acat=" + "TSERIES" + "&hiCategory=VID&textBusca=&startDate=&endDate=" + "31%2F01%2F2009")
        item.description = item.name
        item.icon = self.folderIcon
        item.thumb = self.noImage
        item.complete = True
        item.type = 'folder'
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

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("tv3.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("tv3.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " (" + item.date.replace("/","-") + ") [3alacarta]"
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
            outfile.write("<title>"+item.name+" ("+item.date+")</title>\n")
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
