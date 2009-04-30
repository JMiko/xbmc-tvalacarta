#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os, os.path
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

register.channelRegister.append('chn_rtve.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="rtve")')

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
        self.icon = "rtve-icon.png"
        self.iconLarge = "rtve-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "RTVE"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "TVE a la carta"
        self.moduleName = "chn_rtve.py"
        self.mainListUri = "http://www.rtve.es/alacarta/index.html"
        self.baseUrl = "http://www.rtve.es/alacarta"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        
        #self.episodeItemRegex = '<li><a href="(/guide/season/[^"]+)">(\d+)</a></li>' # used for the ParseMainList
        #self.episodeItemRegex = '<a href="(/tvcarta/impe/web/contenido?id=[^"]+)" title="([^"])+">([^<]+)</a>'
        #self.episodeItemRegex = '<a href="(/tvcarta/impe/web/contenido\?id=[^"]+)" title="([^"]+)">'
        #
        #<div class="infoPrograma">
        #<h3 class="h3TituloProgramaCarta">
        #<a href="/tvcarta/impe/web/contenido?id=3643" title=" ARRAYAN">ARRAYAN</a>
        #</h3>
        #<p>Programa 21 Diciembre 2008</p><p>Serie de ficci&oacute;n</p>
        #</div>
        #<div class="enlacePrograma"><a href="/tvcarta/impe/web/contenido?id=3643" title=" "><img class="imgLista" src="http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/ARRAYAN_21DIC.00.00.00.00.png" alt="" title=""></a></div><div class="pie_bloq"></div></div>
        self.episodeItemRegex = 'nohaynadaquecumplaestaexpresionregular'
        #self.episodeItemRegex = '<li id="video-(\d+)">\W*<div>\W*<a rel="facebox" href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
        #<embed width="393" height="344" align="middle" flashvars="&amp;video=http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/CAMINOS HIERRO_20OCT.flv" src="/tvcarta/html/nav/com/css/cssimg/video2.swf" quality="high" bgcolor="#016a32" menu="false" name="video" allowscriptaccess="always" allowfullscreen="true" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/>
        #self.videoItemRegex = '<location>([^<]+)</location>'

        #<li id="video-379836">
        #<div>
        #<a rel="facebox" href="/alacarta/player/379836.html"><img src="/resources/jpg/6/8/1231688063086.jpg" alt="Coraz&oacute;n, coraz&oacute;n"><img alt="Reproducir" src="/css/i/mediateca/play.png" class="play_mini"></a>
        #<h3>
        #<a rel="facebox" href="/alacarta/player/379836.html">Coraz&oacute;n, coraz&oacute;n</a>
        #</h3>
        #
        #<p>Todas las novedades del mundo de la moda, el cine y la m&uacute;sica.</p>

        #self.videoItemRegex = '<li id="video-(\d+)">\W*<div>\W*<a rel="facebox" href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"><img alt="Reproducir" src="/css/i/mediateca/play.png" class="play_mini"></a>\W+<h3>\W+<a[^<]+</a>\W+</h3>\W+<p>([^<]+)</p>'
        self.videoItemRegex2 = '<li id="video-(\d+)">\W*<div>\W*<a rel="facebox" href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"><img alt="Reproducir" src="/css/i/mediateca/play.png" class="play_mini"></a>\W+<h3>\W+<a[^<]+</a>\W+</h3>\W+<p>([^<]+)</p>[^<]+<span>([^<]+)<'
        self.videoItemRegex = ''
        self.folderItemRegex = '<a href="(/alacarta/todos/[^"]+)">([^<]+)</a>'
        #self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        self.mediaUrlRegex = '<location>([^<]+)</location>'    # used for the UpdateVideoItem
        
        #<ul class="paginacion">
        #<li class="atras">
        #<a title="Atrás">
        #							Atrás
        #						</a>
        #</li>
        #<li>
        #<span id="contador">
        #		1
        #	
        #							de
        #							3</span>
        #</li>
        #<li class="adelante">
        #<a href="javascript:window.location.href = window.location.pathname + '?page=2'" title="Adelante">
        #							Adelante
        #						</a>
        #</li>
        #</ul>        
        #self.pageNavigationRegex = '<ul class="paginacion">\W*<li class="atras">\W*<a title="[^"]+">\W*[^<]+\W*</a>\W*</li>\W*<li>\W*<span id="contador">\W*(\d+)\W+de\W+(\d+)</span>\W*</li>\W*<li class="adelante">\W*<a title="[^"]+" href=[^\']\'([^\']+)\'' # # "
        #self.pageNavigationRegex = '\?page=(\d+)'
        #self.pageNavigationRegex = ''
        #self.pageNavigationRegexIndex = 1 
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        item = common.clistItem("%s" % resultSet[1], "http://www.rtve.es%s" % resultSet[0])
        item.description = item.name
        item.icon = self.folderIcon
        item.thumb = self.noImage
        item.complete = True
        if resultSet[1]=="Recomendados" or resultSet[1]=="Temas" or resultSet[1]=="Todos A-Z" or resultSet[1]=="Archivo TVE" or resultSet[1]=="Ultimos 7 dias":
            item.type = 'null'
        else:
            item.type = 'folder'
        return item
    
   #==============================================================================
    def ParseMainList(self):
        #get base items and add some other categories
        items = chn_class.Channel.ParseMainList(self)        

        items = []
        nuevoitem = common.clistItem("Recomendados", "http://www.rtve.es/alacarta/todos/recomendados/index.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Últimos 7 días", "http://www.rtve.es/alacarta/todos/ultimos/index.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)
        
        nuevoitem = common.clistItem("Temas", "http://www.rtve.es/alacarta/todos/temas/index.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Todos A-Z", "http://www.rtve.es/alacarta/todos/abecedario/index.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        nuevoitem = common.clistItem("Archivo TVE", "http://www.rtve.es/alacarta/archivo/index.html" )
        nuevoitem.icon = self.folderIcon
        items.append(nuevoitem)

        self.mainListItems = items

        return items
    
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
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        #item = common.clistItem( resultSet[1] , urlparse.urljoin(self.baseUrl, resultSet[0]))
        item = common.clistItem( resultSet[3], "http://www.rtve.es/alacarta/player/%s.xml" % resultSet[0] )
        #item = common.clistItem( resultSet[1] , resultSet[1])
        item.icon = self.icon
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)

        fechahora = common.DoRegexFindAll("Emitido:\s+([^\s]+)\s+\[\s+(\d+)\s+\:\s+(\d+)", resultSet[5])
        logFile.debug("fechahora")
        logFile.debug(fechahora)

        item = common.clistItem( resultSet[3] + " (" + fechahora[0][1]+"'"+fechahora[0][2]+"s)" , "http://www.rtve.es/alacarta/player/%s.xml" % resultSet[0] )
        
        #item.thumb = self.noImage
        item.thumbUrl = "http://www.rtve.es%s" % resultSet[2]
        
        item.date = fechahora[0][0]
        
        item.icon = "newmovie.png"
        item.description = common.ConvertHTMLEntities(resultSet[4])
        item.type = 'video'
        item.complete = False

        # Variante: Lee los xml en caliente y no espera a que lo selecciones - abre el xml para sacar la ruta del video
        #detallevideo = uriHandler.Open(item.url)
        #enlacevideo = common.DoRegexFindAll(self.mediaUrlRegex, detallevideo)
        #item.mediaurl = enlacevideo[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
        #item.complete = True

        # Variante: Lee y cachea los xml
        #localImageName = uriHandler.CorrectFileName(localImageName)
        #localCompletePath = os.path.join(config.cacheDir, localImageName)
        #try:
        #    if os.path.exists(localCompletePath): #check cache
        #            thumb = localCompletePath
        #    else: #  save them in cache folder
        #            logFile.debug("Downloading thumb. Filename=%s", localImageName)
        #            thumb = uriHandler.Download(remoteImage, localImageName, folder=config.cacheDir, pb=False)
        #except:
        #    logFile.error("Error opening thumbfile!", exc_info=True)
        #    return self.noImage            
        
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
        #item.thumb = self.CacheThumb(item.thumbUrl)
        #original: rtmp://stream.rtve.es/stream/resources/alacarta/flv/2/5/1231404096852.flv
        #original: http://www.rtve.es/resources/alacarta/flv/1/5/1230105693151.flv

        # abre el xml para sacar la ruta del video
        detallevideo = uriHandler.Open(item.url, pb=False)
        enlacevideo = common.DoRegexFindAll(self.mediaUrlRegex, detallevideo)
        item.mediaurl = enlacevideo[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')

        item.complete = True
        return item

    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("Performing Pre-Processing")
        _items = []

        # Primera página
        logFile.debug("***")
        logFile.debug("*** Pagina 1")
        logFile.debug("***")
        videos = common.DoRegexFindAll(self.videoItemRegex2, data)
        for video in videos:
            elvideo = self.CreateVideoItem(video)
            _items.append(elvideo)

        paginas = common.DoRegexFindAll('\?page=(\d+)', data)
        logFile.debug("*** Paginas siguientes")
        logFile.debug(paginas)

        # Hay al menos otra página
        if len(paginas)>0:
            pagina = paginas[ len(paginas)-1 ]
            logFile.debug("***")
            logFile.debug("*** Pagina " + pagina)
            logFile.debug("***")
            for mainlstitm in self.mainListItems:
                logFile.debug("mainlstitm.name=%s" % mainlstitm.name)
                
            urlpagina = '%s?page=%s' % (self.urlelegido , pagina)
            logFile.debug("urlpagina="+urlpagina)

            # Abre la segunda página
            datapagina = uriHandler.Open(urlpagina, pb=True)
            
            #extrae los vídeos
            videos = common.DoRegexFindAll(self.videoItemRegex2, datapagina)
            for video in videos:
                elvideo = self.CreateVideoItem(video)
                _items.append(elvideo)

            paginas = common.DoRegexFindAll('\?page=(\d+)', datapagina)
            logFile.debug("*** Paginas siguientes")
            logFile.debug(paginas)
            
            while len(paginas)>1:
                pagina = paginas[ len(paginas)-1 ]
                logFile.debug("***")
                logFile.debug("*** Pagina " + pagina)
                logFile.debug("***")
                urlpagina = '%s?page=%s' % (self.urlelegido , pagina)
                logFile.debug("urlpagina="+urlpagina)

                datapagina = uriHandler.Open(urlpagina, pb=True)

                #extrae los vídeos
                videos = common.DoRegexFindAll(self.videoItemRegex2, datapagina)
                for video in videos:
                    elvideo = self.CreateVideoItem(video)
                    _items.append(elvideo)

                paginas = common.DoRegexFindAll('\?page=(\d+)', datapagina)
                logFile.debug("*** Paginas siguientes")
                logFile.debug(paginas)

        return (data, _items)

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
            baseFilename = item.name + " (" + item.date.replace("/","-") + ") [rtve.es]"
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
