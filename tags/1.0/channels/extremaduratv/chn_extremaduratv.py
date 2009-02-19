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

register.channelRegister.append('chn_extremaduratv.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="extremaduratv")')

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
        self.icon = "extremaduratv-icon.png"
        self.iconLarge = "extremaduratv-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Extremadura"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_extremaduratv.py"
        self.mainListUri = "http://extremaduratv.canalextremadura.es/tv-a-la-carta"
        self.baseUrl = "http://extremaduratv.canalextremadura.es/tv-a-la-carta"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        #$<option value="50">Actualidad</option>
        self.episodeItemRegex = '<option value="(\d+)">([^<]+)</option>'
        #<div class="item_busqueda"> <div class="foto"> <img src="http://tv.canalextremadura.es/sites/rtvex/files/imagecache/video_busqueda/sites/rtvex/files/aire 5 enero 09_0001.jpg" alt="" title=""  />                </div> <div class="datos"> <div class="titulo"><a href="/tv-a-la-carta/videos/extremadura-desde-el-aire-un-reflejo-de-belleza"><span class="color_1">extremadura</span><span class="miniespacio"> </span><span class="color_2">desde</span><span class="miniespacio"> </span><span class="color_3">el</span><span class="miniespacio"> </span><span class="color_1">aire:</span><span class="miniespacio"> </span><span class="color_2">un</span><span class="miniespacio"> </span><span class="color_1">reflejo</span><span class="miniespacio"> </span><span class="color_3">de</span><span class="miniespacio"> </span><span class="color_1">belleza</span><span class="miniespacio"> </span></a></div>
        self.videoItemRegex = '<div class="item_busqueda">\W*<div class="foto">\W*<img src="([^"]+)" alt="" title=""\W*/>\W*</div>\W*<div class="datos">\W*<div class="titulo"><a href="([^"]+)">'
        self.folderItemRegex = '<a href="(/alacarta/todos/[^"]+)">([^<]+)</a>'
        #<param name="FileName" value="http://mfile.akamai.com/47586/wmv/corporacion.download.akamai.com/47589/StreamVideo/cita+16+ene.asx ">
        #20090121 00:21:50 - INFO     - uriopener.py     - 194 - Url http://tv.canalextremadura.es/tv-a-la-carta/videos/planeta-extremadura-23-diciembre was opened successfully
        self.mediaUrlRegex = '<param name="FileName" value="([^"]+)">'    # used for the UpdateVideoItem
        #self.mediaUrlRegex = 'href="([^"]+)"'    # used for the UpdateVideoItem
        #self.pageNavigationRegex = '<ul class="paginacion">\W*<li class="atras">\W*<a title="[^"]+">\W*[^<]+\W*</a>\W*</li>\W*<li>\W*<span id="contador">\W*(\d+)\W+de\W+(\d+)</span>\W*</li>\W*<li class="adelante">\W*<a title="[^"]+" href=[^\']\'([^\']+)\'' # # "
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
        
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        #item = common.clistItem( resultSet[1] , urlparse.urljoin(self.baseUrl, resultSet[0]))
        #logFile.debug("tituloantes="+resultSet[1])
        #titulounicode = unicode( resultSet[1], "utf-8" )
        #logFile.debug("titulounicode="+titulounicode)
        #titulo = titulounicode.encode("iso-8859-1")
        titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        logFile.debug("titulo="+titulo)
        laurl = "http://extremaduratv.canalextremadura.es/search/videos/programa%3A" + resultSet[0] + "+categoria%3A0"
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
        urlfinal = "http://tv.canalextremadura.es%s" % resultSet[1]
        urlfinal = urlfinal.replace("#","%")
        logFile.debug("urldetalle="+urlfinal)
        item = common.clistItem( "Video" , urlfinal )
        
        #item.thumb = self.noImage
        item.thumbUrl = resultSet[0].replace(" ","%20")
        logFile.debug("item.thumbUrl="+item.thumbUrl)
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        item.date = "01/01/2009"
        item.icon = "newmovie.png"
        item.description = "Loading..."
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

        # abre el xml para sacar la ruta del video
        logFile.info('urldetalle=%s', item.url)
        detallevideo = uriHandler.Open(item.url, pb=False)
        enlacevideo = common.DoRegexFindAll(self.mediaUrlRegex, detallevideo)
        logFile.info('urlasx=%s' % enlacevideo )
        descripcion1 = common.DoRegexFindAll("<div class=\"view-field view-data-title\">([^<]+)<", detallevideo)
        descripcion2 = common.DoRegexFindAll("<div class=\"view-field view-data-body\">([^<]+)<", detallevideo)
        descripcion3 = common.DoRegexFindAll("<div class=\"view-field view-data-created\">([^<]+)<", detallevideo)
        descripcion4 = common.DoRegexFindAll("<div class=\"view-field view-data-duracion\">([^<]+)<", detallevideo)
        logFile.info('descripcion1=%s' % descripcion1)
        logFile.info('descripcion2=%s' % descripcion2)
        logFile.info('descripcion3=%s' % descripcion3)
        logFile.info('descripcion4=%s' % descripcion4)
        descripcioncompleta = descripcion1[0].strip() + " " + descripcion2[0].strip() + " " + descripcion3[0].strip() + " " + descripcion4[0].strip()
        descripcioncompleta = descripcioncompleta.replace("\t","");
        descripcioncompleta = unicode( descripcioncompleta, "utf-8" ).encode("iso-8859-1")
        #<PARAM NAME="url" VALUE="http://www.barcelonatv.cat/alacarta/generarPubli.php?idVSD=3385&idPrograma=37">
        descriptorvideo = uriHandler.Open(enlacevideo[0].strip().replace(" ","+"), pb=False)
        urlvideo = common.DoRegexFindAll('href="([^"]+)"', descriptorvideo)
        logFile.info('urlvideo=%s' % urlvideo[0])

        item.mediaurl = urlvideo[0]
        item.description = descripcioncompleta

        item.complete = True
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

