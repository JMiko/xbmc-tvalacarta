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

register.channelRegister.append('chn_tvmallorca.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="tvmallorca")')

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
        self.icon = "tvmallorca-icon.png"
        self.iconLarge = "tvmallorca-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "TV Mallorca"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_tvmallorca.py"
        self.mainListUri = "http://tvmallorca.net/pages/tv_a_la_carta"
        self.baseUrl = "http://tvmallorca.net/pages/tv_a_la_carta"
        self.defaultPlayer = 'mplayer'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        self.episodeItemRegex = '<option\W*value="(\d+)">([^<]+)</option>'

        #<tr class='row1'>
        #<td class="t1">2009-02-01 </td>
        #<td class="t2">20:30:00 </td>
        #<td class="t3"><h3>Méteo</h3>
        #Televisió de Mallorca vol oferir un tractament diferenciat sobre la informació meteorològica.     </td>  
        #<td class="t4"><a href="/pages/verclip/8828">veure</a></td>
        self.videoItemRegex = '<tr[^>]+>[^<]*<td class="t1">([^<]+)</td>[^<]*<td class="t2">([^<]+)</td>[^<]*<td class="t3"><h3>[^<]+</h3>([^<]+)</td>[^<]*<td class="t4"><a href="([^"]+)"'
        self.folderItemRegex = ''
        self.mediaUrlRegex = ''    # used for the UpdateVideoItem
        self.pageNavigationRegex = 'ssssssssssssssssssss'
        self.pageNavigationRegexIndex = 1 
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s', self.channelName)
        return True

    #==============================================================================
    def ParseMainList(self):
        items = chn_class.Channel.ParseMainList(self)        
        
        nuevo = common.clistItem("(Buscador)", "searchSite" )
        nuevo.icon = self.folderIcon
        items.insert(0, nuevo)
        
        return items

    #==============================================================================
    def SearchSite(self):
        items = []
        
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)>0:
                tecleado = tecleado.replace(" ", "+")
                searchUrl = 'http://tvmallorca.net/pages/tv_a_la_carta?programa=0&monthDay=&month=&year=&q='+tecleado+'&submit=cercar'
                return self.ProcessFolderList(searchUrl,"GET")
                
        return items
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = ""
        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        laurl = "http://tvmallorca.net/pages/tv_a_la_carta?programa=" + resultSet[0] + "&monthDay=&month=&year=&q=Escrigui+les+paraules+de+recerca&submit=cercar"
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
        urlfinal = "http://tvmallorca.net" + resultSet[3]
        logFile.debug("urldetalle="+urlfinal)
        item = common.clistItem( resultSet[0] + " " + resultSet[1] , urlfinal )
        
        item.thumb = self.noImage
        item.date = "."
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
        
        # <div id="descTVCarta"><p>En aquest capítol, coneixerem quins són els millors aliments i com cuinar-los, segons els seguidors de l’alimentació energètica. A l’entrevista, vos explicarem un projecte innovador, de la mà de Rosa Masdeu, on les dones jubilades són les protagonistes. També vos parlarem del massatge quàntic, una tècnica on la energia i las mans tenen molt a dir. I per últim caminarem, amb l’ONG Treball Solidari, per l’averany de la solidaritat d’una manera diferent, agermanar dones a través del microcrèdits.</p>
        descripcion = common.DoRegexFindAll('<div id="descTVCarta">[^<]+<p>([^<]+)</p>', detallevideo)
        item.description = ""
        try:
            item.description = unicode( descripcion[0], "utf-8" ).encode("iso-8859-1")
        except:
            item.description = descripcion[0]
        
        # <a href="http://stream.tvmallorca.net/clip/tv/200902/20090201_1329_camins__cap._3_.ogg" >
        urlvideo = common.DoRegexFindAll('<a href="(http://stream.tvmallorca.net[^"]+)"', detallevideo)
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

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("tvmallorca.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("tvmallorca.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " (" + item.date.replace("/","-") + ") [tvmallorca]"
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

            destFilename = baseFilename+".ogg"
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
