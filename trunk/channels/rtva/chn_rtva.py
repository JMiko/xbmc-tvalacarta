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

register.channelRegister.append('chn_rtva.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="rtva")')

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
        self.icon = "rtva-icon.png"
        self.iconLarge = "rtva-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Andalucia"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "RTVA a la carta"
        self.moduleName = "chn_rtva.py"
        self.mainListUri = "http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada"
        self.baseUrl = "http://www.radiotelevisionandalucia.es/"
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
        self.episodeItemRegex = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
        #<embed width="393" height="344" align="middle" flashvars="&amp;video=http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/CAMINOS HIERRO_20OCT.flv" src="/tvcarta/html/nav/com/css/cssimg/video2.swf" quality="high" bgcolor="#016a32" menu="false" name="video" allowscriptaccess="always" allowfullscreen="true" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/>
        self.videoItemRegex = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
        #self.videoItemRegex = '<param name="flashvars" value="&amp;video=(http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8[^"]+)"'
#        self.folderItemRegex = '<a href="\.([^"]*/)(cat/)(\d+)"( style="color:\s*white;"\s*)*>([^>]+)</a><br'  # used for the CreateFolderItem
        #self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        self.mediaUrlRegex = '<param name="flashvars" value="&amp;video=(http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8[^"]+)"'
        #self.mediaUrlRegex = '<embed width="393" height="344" align="middle" flashvars="&amp;video=([^"]+)"'
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True
      
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

    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s %s', self.channelName , resultSet[1])
        #logFile.debug(self)
        #logFile.debug(resultSet)
        
        titulo = resultSet[1].replace("á","Á")
        titulo = titulo.replace("é","É")
        titulo = titulo.replace("í","Í")
        titulo = titulo.replace("ó","Ó")
        titulo = titulo.replace("ú","Ú")
        titulo = titulo.replace("ñ","Ñ")
        titulo = titulo.replace('&Aacute;','Á')
        titulo = titulo.replace('&Eacute;','É')
        titulo = titulo.replace('&Iacute;','Í')
        titulo = titulo.replace('&Oacute;','Ó')
        titulo = titulo.replace('&Uacute;','Ú')
        titulo = titulo.replace('&ntilde;','ñ')
        titulo = titulo.replace('&Ntilde;','Ñ')
        
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        #item = common.clistItem( resultSet[1] , urlparse.urljoin(self.baseUrl, resultSet[0]))
        item = common.clistItem( titulo , 'http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada' )
        #item = common.clistItem( resultSet[1] , resultSet[1])
        item.complete = True
        item.icon = self.folderIcon
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        # if el titulo no coincide con el del programa, no lo añade a la lista
        # la pagina de resultados de RTVA contiene todos los programas, no solo el resultado de la busqueda
        #logFile.debug('starting CreateVideoItem for %s %s %s', self.channelName , resultSet[1] , resultSet[2] )
        #logFile.debug(resultSet)
        #logFile.debug('**** elegido=%s' , self.elegido)
        programa = self.mainListItems[self.elegido].name
        
        titulo = resultSet[1].replace('&Aacute;','Á')
        titulo = titulo.replace('&Eacute;','É')
        titulo = titulo.replace('&Iacute;','Í')
        titulo = titulo.replace('&Oacute;','Ó')
        titulo = titulo.replace('&Uacute;','Ú')
        titulo = titulo.replace('&Ntilde;','Ñ')

        #logFile.debug( titulo )
        #logFile.debug( programa )
        #logFile.debug('--- folderHistory')
        #logFile.debug(len(self.folderHistory))
        #logFile.debug(self.folderHistory)
        #logFile.debug(len(self.folderHistory[0].items))
        #logFile.debug(len(self.folderHistory[-1].items))
        #logFile.debug('--- folderHistorySelectedPosition')
        #logFile.debug(self.folderHistorySelectedPosition)
        #logFile.debug('--- listItems')
        #logFile.debug(len(self.listItems))
        #logFile.debug(self.listItems)
        #logFile.debug('--- mainListItems')
        #logFile.debug(len(self.mainListItems))
        #logFile.debug(self.mainListItems)
        #logFile.debug('--- self.currentPosition')
        #logFile.debug(self.currentPosition)
        #logFile.debug(self.getCurrentListPosition())
        
        titulocapitulo =  ( "%s %s %s %s" % (resultSet[2],resultSet[3],resultSet[4],resultSet[5]))
        titulocapitulo = titulocapitulo.replace('&Aacute;','Á')
        titulocapitulo = titulocapitulo.replace('&Eacute;','É')
        titulocapitulo = titulocapitulo.replace('&Iacute;','Í')
        titulocapitulo = titulocapitulo.replace('&Oacute;','Ó')
        titulocapitulo = titulocapitulo.replace('&Uacute;','Ú')
        titulocapitulo = titulocapitulo.replace('&ntilde;','ñ')
        titulocapitulo = titulocapitulo.replace('&Ntilde;','Ñ')

        item = common.clistItem( titulocapitulo , urlparse.urljoin(self.baseUrl, resultSet[0]) )
        item.thumb = self.noImage
        item.thumbUrl = resultSet[6]
        item.date = "01/01/2009"
        item.icon = "newmovie.png"
        item.description = ( "%s %s %s %s" % (resultSet[2],resultSet[3],resultSet[4],resultSet[5]))
        item.complete = False
        if titulo == programa:
            item.type = 'video'
            logFile.debug( 'item.url=%s' , item.url )
        else:
            item.type = 'null'
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('---------------------------------------------------------------------------------')
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        logFile.info('item.mediaurl=%s', item.mediaurl)
        
        logFile.info('---------------------------------------------------------------------------------')
        logFile.info('item.url=%s', item.url)
        logFile.info('self.mediaUrlRegex=%s', self.mediaUrlRegex)
        detallevideo = uriHandler.Open(item.url, pb=False)
        encontrado = common.DoRegexFindAll(self.mediaUrlRegex, detallevideo)
        logFile.info(encontrado)
        logFile.info(encontrado[0])
        #logFile.info(encontrado[1])
        item.mediaurl = encontrado[0]
        logFile.info('item.mediaurl=%s', item.mediaurl)
        
        #argumento = common.DoRegexFindAll('<div class="contenido"><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div>', detallevideo)
        argumento = common.DoRegexFindAll('<div class="zonaContenido"><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div>', detallevideo)
        logFile.info(argumento)
        argumentofull = ""
        if len(argumento) > 0:
            if len(argumento[0]) >= 4:
                argumentofull = ("%s\n%s\n%s\n%s\n%s" % (item.description , argumento[0][0] , argumento[0][1] , argumento[0][2] , argumento[0][3] ))
            elif len(argumento[0]) >= 3:
                argumentofull = ("%s\n%s\n%s\n%s" % (item.description , argumento[0][0] , argumento[0][1] , argumento[0][2] ))
            elif len(argumento[0]) >= 2:
                argumentofull = ("%s\n%s\n%s" % (item.description , argumento[0][0] , argumento[0][1] ))
            elif len(argumento[0]) >= 1:
                argumentofull = ("%s\n%s" % (item.description , argumento[0][0] ))
        #argumentofull = ("%s\n%s" % (item.description , argumento[0][0] ))
        argumentofull = argumentofull.replace('&Aacute;','Á')
        argumentofull = argumentofull.replace('&Eacute;','É')
        argumentofull = argumentofull.replace('&Iacute;','Í')
        argumentofull = argumentofull.replace('&Oacute;','Ó')
        argumentofull = argumentofull.replace('&Uacute;','Ú')
        argumentofull = argumentofull.replace('&aacute;','á')
        argumentofull = argumentofull.replace('&eacute;','é')
        argumentofull = argumentofull.replace('&iacute;','í')
        argumentofull = argumentofull.replace('&oacute;','ó')
        argumentofull = argumentofull.replace('&uacute;','ú')
        argumentofull = argumentofull.replace('&ntilde;','ñ')
        argumentofull = argumentofull.replace('&Ntilde;','Ñ')
        item.description = argumentofull
        
        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl.replace(' ','%20'))        
        item.mediaurl = item.mediaurl.replace(' ','%20')
        logFile.info('---------------------------------------------------------------------------------')
        item.complete = True
        return item


    #============================================================================== 
    def DownloadEpisode(self, item):

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("rtva.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("rtva.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " [rtva]"
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
