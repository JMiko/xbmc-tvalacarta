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

register.channelRegister.append('chn_a3.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="a3")')

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
        self.icon = "a3-icon.png"
        self.iconLarge = "a3-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Antena 3"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "antena3videos.com"
        self.moduleName = "chn_a3.py"
        self.mainListUri = "http://www.antena3videos.com/cooliris.rss"
        self.baseUrl = "http://www.antena3videos.com/"
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
        self.episodeItemRegex = '<item>[^<]+<title><\!\[CDATA\[([^\]]+)\]\]></title>[^<]+<link>([^<]+)</link>[^<]+<description><\!\[CDATA\[([^\]]+)\]\]></description>[^<]+<media:thumbnail url=\'([^\']+)\'/>[^<]+<media:content type=\'([^\']+)\' url=\'([^\']+)\'/>' # ([^<]+)</description>'
        #<embed width="393" height="344" align="middle" flashvars="&amp;video=http://rtva.ondemand.flumotion.com/rtva/ondemand/flash8/CAMINOS HIERRO_20OCT.flv" src="/tvcarta/html/nav/com/css/cssimg/video2.swf" quality="high" bgcolor="#016a32" menu="false" name="video" allowscriptaccess="always" allowfullscreen="true" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/>
        self.videoItemRegex = 'idvideo:\'(\d+)\''
#        self.folderItemRegex = '<a href="\.([^"]*/)(cat/)(\d+)"( style="color:\s*white;"\s*)*>([^>]+)</a><br'  # used for the CreateFolderItem
        #self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        self.mediaUrlRegex = '<location>([^<]+)</location>'    # used for the UpdateVideoItem
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
        
        try:
            titulo = unicode( resultSet[0], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[0]
        item = common.clistItem( titulo , "http://www.antena3videos.com" + resultSet[1] )
        try:
            descripcion = unicode( resultSet[2], "utf-8" ).encode("iso-8859-1")
        except:
            descripcion = resultSet[2]
        item.description = descripcion
        item.thumbUrl = "http://www.antena3videos.com" + resultSet[3]
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
        
        descripcion = self.mainListItems[self.elegido].description
        
        item = common.clistItem( self.mainListItems[self.elegido].name , 'http://antena3.ondemand.flumotion.com/a3webtv/ondemand/video/%s.flv?id=cooliris' % resultSet )

        item.thumb = self.noImage
        item.thumbUrl = self.mainListItems[self.elegido].thumbUrl
        item.date = "01/01/2009"
        item.icon = "newmovie.png"
        item.description = descripcion
        item.type = 'video'
        item.complete = False
        item.mediaurl = item.url
        logFile.debug('item.url=%s' % item.url)
        logFile.debug('item.mediaurl=%s' % item.mediaurl)
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
        #original: rtmp://stream.rtve.es/stream/resources/alacarta/flv/2/5/1231404096852.flv
        #original: http://www.rtve.es/resources/alacarta/flv/1/5/1230105693151.flv
        item.mediaurl = item.url
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


    #============================================================================== 
    def DownloadEpisode(self, item):

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("a3.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("a3.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " [antena3videos.com]"
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
