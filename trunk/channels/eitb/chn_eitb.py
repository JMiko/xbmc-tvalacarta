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

import urllib2,urllib

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

register.channelRegister.append('chn_eitb.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="eitb")')

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
        self.icon = "eitb-icon.png"
        self.iconLarge = "eitb-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "EITB"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_eitb.py"
        self.mainListUri = 'http://www.eitb.com/videos/'
        self.baseUrl = 'http://www.eitb.com/videos/'
        self.defaultPlayer = 'mplayer'
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False

        self.episodeItemRegex = '<li><a href="(/videos/[^"]+)" title="[^"]+" class="">([^<]+)</a></li>'
        patronvideos  = '<li>[^<]*<a href="([^"]+)"[^>]+>[^<]*'
        patronvideos += '<span><img[^>]+></span>[^<]*'
        patronvideos += '<img src="([^"]+)".*?'
        patronvideos += '<div class="info_medio">[^<]*<h3[^<]+'
        patronvideos += '<a[^>]+>\s*([^<]+)</a>'
        patronvideos += '.*?<ul class="lst_info_extra">.*?</ul>'
        patronvideos += '(.*?)<ul class="lst_info_extra">.*?</ul>'
        self.videoItemRegex = patronvideos
        
        self.folderItemRegex = '<li><a href="(/videos/[^"]+)" title="[^"]+" class="">([^<]+)</a></li>'
        
        self.mediaUrlRegex = '(/commons/pet/getMedia.php\?id\=[^&]+)&'
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s (trace)', self.channelName)
        return True

    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        logFile.debug("url="+url)

        item = common.clistItem( titulo, url )
        item.icon = self.folderIcon
        item.complete = True
        return item
    
    #==============================================================================
    def PreProcessFolderList(self, data):
        logFile.info("PreProcessFolderList")
        _items = []

        #<li><a href="/videos/television/pagina/2/">Siguiente &raquo;</a></li>
        patronvideos  = '<li><a href="(/videos[^"]+)">(Siguiente)[^<]+</a></li>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        i=0
        for match in matches:
            logFile.info("Matches: %d %s" % (i , match))
            i = i + 1

        if len(matches)>0:
            nuevofolder = self.CreateFolderItem(matches[0])
            _items.append(nuevofolder)

        return (data, _items)

    #==============================================================================
    def CreateFolderItem(self, resultSet):
        logFile.debug('CreateFolderItem %s', self.channelName)
        logFile.debug(resultSet)

        try:
            titulo = unicode( resultSet[1], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        logFile.debug("url="+url)

        item = common.clistItem( titulo, url )
        item.description = item.name
        item.icon = self.folderIcon
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
        
        try:
            titulo = unicode( resultSet[2].strip(), "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[2].strip()
        logFile.debug("titulo="+titulo)
        url = urlparse.urljoin(self.baseUrl,resultSet[0])
        logFile.debug("url="+url)
        item = common.clistItem( titulo , url )
        
        descripcion = "%s" % resultSet[3]
        descripcion = descripcion.strip()
        descripcion = descripcion.replace("</p>","")
        descripcion = descripcion.replace("<p>","")
        descripcion = common.ConvertHTMLEntities(descripcion)
        try:
            item.description = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
        except:
            item.description = descripcion
        
        
        item.thumbUrl = urlparse.urljoin(self.baseUrl,resultSet[1])

        item.date = "."
        item.icon = "newmovie.png"
        item.type = 'video'
        item.complete = False

        return item

    #============================================================================= 
    def UpdateVideoItem(self, item):
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)

        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # Saca la URL que identifica el vídeo
        logFile.info("item.url="+item.url)
        req = urllib2.Request(item.url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        patronvideos = '(/commons/pet/getMedia.php\?id\=[^&]+)&'
        matches = re.compile(patronvideos,re.DOTALL).findall(link)
        url = urlparse.urljoin(item.url,matches[0])
        logFile.info("url="+url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        patronvideos  = '<media:content url="([^"]+)"'
        matches=re.compile(patronvideos,re.DOTALL).findall(link)
        item.mediaurl = matches[0]
        logFile.debug("item.mediaurl="+item.mediaurl)
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

        # Lee la ruta por configuración
        destFolder = parameters.getConfigValue("eitb.download.path",config.cacheDir)
        logFile.info("destFolder="+destFolder)

        dialog = xbmcgui.Dialog()
        destFolder = dialog.browse(3, 'Elige el directorio', 'files', '', False, False, destFolder)
        logFile.info("destFolder="+destFolder)

        # Actualiza la ruta en la configuración
        parameters.setConfigValue("eitb.download.path",destFolder)

        #check if data is already present and if video or folder
        if item.type == 'folder':
            logFile.warning("Cannot download a folder")
        elif item.type == 'video':
            if item.complete == False:
                logFile.info("Fetching MediaUrl for VideoItem")
                item = self.UpdateVideoItem(item)
            
            # Nombre del fichero
            baseFilename = item.name + " [eitb.com]"
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
