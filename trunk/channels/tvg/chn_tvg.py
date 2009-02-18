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

register.channelRegister.append('chn_tvg.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="tvg")')

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
        self.icon = "tvg-icon.png"
        self.iconLarge = "tvg-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "TV Galicia"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "á carta"
        self.moduleName = "chn_tvg.py"
        self.mainListUri = "http://www.crtvg.es/TVGacarta/"
        self.baseUrl = "http://www.crtvg.es/TVGacarta/"
        self.httpmethod = "POST"
        self.onUpDownUpdateEnabled = True
        self.defaultPlayer = 'mplayer'

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        #<option>DIVULGATIVOS
        self.episodeItemRegex = '<option>([^<]+)'
        
        #<table class="video" onmouseover="this.style.cursor='pointer';this.style.backgroundColor='#F0F0F0';TagToTip('18444',BGCOLOR, '#FFFFFF',OFFSETY,20, BORDERCOLOR, '#555555',FADEIN,500,FADEOUT,1000, WIDTH, 500, PADDING, 10, TITLE, 'ALALÁ (03/02/2009)',FONTCOLOR,'#555555',FONTFACE,'Arial,helvetica',SHADOWCOLOR,'#D4D4D4',TITLEALIGN,'center',CENTERMOUSE,false,SHADOW,true,BORDERSTYLE, 'solid',TITLEBGCOLOR,'#555555',TITLEFONTSIZE,'14px')" onmouseout="this.style.backgroundColor='#FFFFFF'" onclick="javascript:AbreReproductor('/reproductor/inicio.asp?canal=tele&amp;hora=08/02/2009 21:35:16&amp;fecha=03/02/2009&amp;arquivo=1&amp;programa=ALALÁ&amp;id_programa=7','ventanamapa')" >
        #<tr>
        #<td rowspan="2" class="foto"><img src="/TVG/fotos/alala_p.jpg"></td>
        #<td class="texto">O "Alalá" de hoxe fainos coñecer a <b>Coral Voces da Louriña</b>, un colectivo con moitos valores engadidos, como a diversión e a terapia, pois vén sendo un grupo de mozos e mozas do Porriño de entre setenta e noventa anos que descubriu desde hai ano...</td>
        #</tr>
        #<tr>
        #<td class="pe">
        #<span class="data">&nbsp;03/02/2009&nbsp;-&nbsp;21:35 h.&nbsp;</span>
        #</td>
        #</tr>
        #</table>
        self.videoItemRegex = '[^<]+<table class="video" onmouseover="[^"]+" onmouseout="[^"]+" onclick="javascript:AbreReproductor\(\'([^\']+)\'[^"]+" >[^<]+<tr>[^<]+<td rowspan="2" class="foto"><img src="([^"]+)"></td>[^<]+<td class="texto">([^<]+)<'

        #<table align="center" id="prog_front">
        #<tr>
        #<th class="cab">
        #<strong>VINTE NA GALEGA</strong><br>
        self.folderItemRegex = '<table align="center" id="prog_front">[^<]+<tr>[^<]+<th class="cab">[^<]+<strong>([^<]+)</strong>'
        
        self.mediaUrlRegex = ''    # used for the UpdateVideoItem
        #self.mediaUrlRegex = 'href="([^"]+)"'    # used for the UpdateVideoItem
        #self.pageNavigationRegex = '<ul class="paginacion">\W*<li class="atras">\W*<a title="[^"]+">\W*[^<]+\W*</a>\W*</li>\W*<li>\W*<span id="contador">\W*(\d+)\W+de\W+(\d+)</span>\W*</li>\W*<li class="adelante">\W*<a title="[^"]+" href=[^\']\'([^\']+)\'' # # "
        self.pageNavigationRegex = ''
        self.pageNavigationRegexIndex = 1 
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        
        '''
        urldetalleget = "http://www.crtvg.es/tvgacarta/index.asp?tipo=DIVULGATIVOS&procura="
        urldetallepost = "http://www.crtvg.es/tvgacarta/index.asp"

        detalleget = uriHandler.Open(urldetalleget, pb=False)
        logFile.debug('***')
        logFile.debug('detalleget')
        logFile.debug(detalleget)
        logFile.debug('***')
        videosporget = common.DoRegexFindAll( self.folderItemRegex , detalleget)
        detallepost = uriHandler.Open( urldetallepost , pb=False , params="tipo=DIVULGATIVOS&procura=" )
        logFile.debug('***')
        logFile.debug('detallepost')
        logFile.debug(detallepost)
        logFile.debug('***')
        videosporpost = common.DoRegexFindAll( self.folderItemRegex , detallepost)
        logFile.debug('*** videosporget')
        logFile.debug(videosporget)
        logFile.debug(len(videosporget))
        logFile.debug('*** videosporpost')
        logFile.debug(videosporpost)
        logFile.debug(len(videosporpost))
        logFile.debug('***')
        '''
        
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
        item = common.clistItem( resultSet.rstrip(), "http://www.crtvg.es/tvgacarta/index.asp?tipo=" + resultSet.rstrip().replace(" ","+") + "&procura=" )
        #item = common.clistItem( resultSet[1] , resultSet[1])
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        categoria = self.mainListItems[self.elegido].name
        logFile.debug("categoria="+categoria)

        # TODO: Añadir al item un nuevo elemento "Parámetros POST" para poder controlar el envio por post
        item = common.clistItem( resultSet.rstrip(), "http://www.crtvg.es/tvgacarta/index.asp?tipo=" + categoria.replace(" ","+") + "&procura=" + resultSet.replace(" ","+") )
        item.description = item.name
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
        
        #/reproductor/inicio.asp?canal=tele&amp;hora=09/02/2009 21:35:16&amp;fecha=03/02/2009&amp;arquivo=1&amp;programa=ALAL\xc1&amp;id_programa=7
        urldetalle = resultSet[0].replace("&amp;","&")
        urldetalle = urldetalle.replace(" ","%20")
        urldetalle = "http://www.crtvg.es" + urldetalle

        titulo = common.DoRegexFindAll("programa=([^&]+)&", resultSet[0])
        item = common.clistItem( titulo[0] , urldetalle )
        
        #item.thumb = self.noImage
        item.thumbUrl = "http://www.crtvg.es"+resultSet[1]
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        fechavideo = common.DoRegexFindAll("fecha=([^&]+)&", resultSet[0])
        item.date = fechavideo[0]
        item.icon = "newmovie.png"
        item.description = resultSet[2]
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
        logFile.info('url=%s', item.url)
        
        #<frame src="laterali.asp?canal=tele&amp;arquivo=1&amp;Programa=ALALÁ&amp;hora=09/02/2009 21:35:16&amp;fecha=03/02/2009&amp;id_Programa=7" name="pantalla" frameborder="0" scrolling="NO" noresize>
        bodyprimerframe = uriHandler.Open(item.url, pb=False)
        enlacesprimerframe = common.DoRegexFindAll('<frame src="(laterali.asp[^"]+)"', bodyprimerframe)
        enlaceprimerframe = enlacesprimerframe[0].replace("&amp;","&")
        enlaceprimerframe = enlaceprimerframe.replace(" ","%20")
        enlaceprimerframe = "http://www.crtvg.es/reproductor/"+enlaceprimerframe
        logFile.info('enlaceprimerframe=', enlaceprimerframe)
        
        #<frame src="ipantalla.asp?canal=tele&amp;arquivo=1&amp;Programa=ALALÁ&amp;hora=09/02/2009 21:35:16&amp;fecha=03/02/2009&amp;opcion=pantalla&amp;id_Programa=7" name="pantalla" frameborder="0" scrolling="NO" noresize>
        bodysegundoframe = uriHandler.Open(enlaceprimerframe, pb=False)
        enlacessegundoframe = common.DoRegexFindAll('<frame src="(ipantalla.asp[^"]+)"', bodysegundoframe)
        enlacesegundoframe = enlacessegundoframe[0].replace("&amp;","&")
        enlacesegundoframe = enlacesegundoframe.replace(" ","%20")
        enlacesegundoframe = "http://www.crtvg.es/reproductor/"+enlacesegundoframe
        logFile.info('enlacesegundoframe=', enlacesegundoframe)
        
        #<param name='url' value='http://www.crtvg.es/asfroot/acarta_tvg/ALALA_20090203.asx' />
        #<PARAM NAME="URL" value="http://www.crtvg.es/asfroot/acarta_tvg/ALALA_20090203.asx" />
        bodyvideo = uriHandler.Open(enlacesegundoframe, pb=False)
        logFile.info('bodyvideo=', bodyvideo)
        #item.description=bodyvideo
        #enlacevideo = common.DoRegexFindAll("<param name='url' value='([^']+)'", bodyvideo)
        enlacevideo = common.DoRegexFindAll('<PARAM NAME="URL" value="([^"]+)"', bodyvideo)
        if len(enlacevideo) == 0:
            logFile.info("probando e.r. alternativa")
            enlacevideo = common.DoRegexFindAll("<param name='url' value='([^']+)'", bodyvideo)
        logFile.info('enlacevideo=', enlacevideo[0])
        
        #<ASX VERSION="3.0"><TITLE>Televisi¾n de Galicia - ALAL-</TITLE><ENTRY><REF HREF="mms://media2.crtvg.es/videos_f/0007/0007_20090203.wmv"/><STARTTIME VALUE="0:00:00" />
        bodyasx = uriHandler.Open(enlacevideo[0], pb=False)
        urlvideo = common.DoRegexFindAll('HREF="([^"]+)"', bodyasx)
        logFile.info('urlvideo=%s' % urlvideo[0])

        item.mediaurl = urlvideo[0]

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

