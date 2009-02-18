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

register.channelRegister.append('chn_barcelonatv.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="barcelonatv")')

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
        self.icon = "btv-icon.png"
        self.iconLarge = "btv-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "BarcelonaTV"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_barcelonatv.py"
        self.mainListUri = "http://www.barcelonatv.cat/alacarta/default.php"
        self.baseUrl = "http://www.barcelonatv.cat/alacarta/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        #<option value="0">Qualsevol</option>
        self.episodeItemRegex = '<option value=\'(\d+)\'\W*>([^<]+)</option>'
        #<li>
        #    <div class="pro"><strong>01</strong>
        #    <a href="player.php?idProgVSD=3385&cercaProgrames=37&fInici=01/01/2008&fFin=31/12/2009" title="Telemonegal">
        #    <img src="http://vodstr.barcelonatv.com/2008/76-1/repr_1500.jpg" width="80" height="58" alt="Telemonegal" />
        #    </a>
        #    <h4>Telemonegal</h4><span>30 de desembre de 2008</span></div>
        #    <div class="desc"><p> &nbsp;</p></div>
        #    <div class="clear"></div>
        #</li>
        self.videoItemRegex = '<li>\W*<div class="pro"><strong>\d+</strong>\W*<a href="([^"]+)" title="([^"]+)">\W*<img src="([^"]+)" width="\d+" height="\d+" alt="[^"]+" />\W*</a>\W*<h4>[^<]+</h4><span>([^<]+)</span></div>'
        self.folderItemRegex = '<a href="(/alacarta/todos/[^"]+)">([^<]+)</a>'
        self.mediaUrlRegex = '<PARAM NAME="url" VALUE="([^"]+)">'    # used for the UpdateVideoItem
        #self.mediaUrlRegex = 'href="([^"]+)"'    # used for the UpdateVideoItem
        #self.pageNavigationRegex = '<ul class="paginacion">\W*<li class="atras">\W*<a title="[^"]+">\W*[^<]+\W*</a>\W*</li>\W*<li>\W*<span id="contador">\W*(\d+)\W+de\W+(\d+)</span>\W*</li>\W*<li class="adelante">\W*<a title="[^"]+" href=[^\']\'([^\']+)\'' # # "
        self.pageNavigationRegex = '\?page=(\d+)'
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
        item = common.clistItem( resultSet[1], "http://www.barcelonatv.cat/alacarta/cerca.php?cercaProgrames=%s&txt_fInici=01/01/2008&txt_fFin=31/12/2009&Cercar_x=17&Cercar_y=18" % resultSet[0] )
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
        
        item = common.clistItem( resultSet[1] , "http://www.barcelonatv.cat/alacarta/%s" % resultSet[0] )
        
        #item.thumb = self.noImage
        item.thumbUrl = resultSet[2]
        
        item.date = resultSet[3]
        item.icon = "newmovie.png"
        item.description = "test"
        item.type = 'video'
        item.complete = False

        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        item.thumb = self.CacheThumb(item.thumbUrl)
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)

        # abre el xml para sacar la ruta del video
        logFile.info('url=%s', item.url)
        logFile.info('er=%s', self.mediaUrlRegex)
        detallevideo = uriHandler.Open(item.url, pb=False)
        enlacevideo = common.DoRegexFindAll(self.mediaUrlRegex, detallevideo)
        logFile.info('enlacevideo=%s' % enlacevideo[0])
        
        #<PARAM NAME="url" VALUE="http://www.barcelonatv.cat/alacarta/generarPubli.php?idVSD=3385&idPrograma=37">
        descriptorvideo = uriHandler.Open(enlacevideo[0], pb=False)
        urlvideo = common.DoRegexFindAll('href="([^"]+)"', descriptorvideo)
        logFile.info('urlvideo=%s' % urlvideo[0])

        item.mediaurl = urlvideo[0]

        detallecompleto = common.DoRegexFindAll('so.addVariable\("sinopsis", "([^"]+)"',detallevideo)
        #logFile.info(detallecompleto)
        item.description = detallecompleto[0]

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

