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

register.channelRegister.append('chn_turbonick.Channel("uzg-channelwindow.xml", config.rootDir, config.skinFolder, channelCode="turbonick")')

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
        self.icon = "turbonick-icon.png"
        self.iconLarge = "turbonick-main.png"
        self.noImage = "noimage.gif"
        self.channelName = "Turbonick"
        self.maxXotVersion = "3.2.0"
        self.channelDescription = "a la carta"
        self.moduleName = "chn_turbonick.py"
        self.mainListUri = 'http://es.turbonick.nick.com/dynamo/turbonick/locale/common/xml/dyn/getGateways.jhtml'
        self.baseUrl = "http://es.turbonick.nick.com/"
        self.onUpDownUpdateEnabled = True

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        patronvideos  = '<gateway cmsid="([^"]+)"\s+title="([^"]+)"\s+urlAlias="[^"]+"\s+iconurl="[^"]+"\s+iconurljpg="([^"]+)"'
        self.episodeItemRegex = patronvideos
        
        patronvideos  = '<content.*?'
        patronvideos += 'cmsid="([^"]+)"'
        patronvideos += '(?:\s+iconurl="([^"]+)")?.*?'
        patronvideos += '<title>([^<]+)</title>.*?'
        patronvideos += '<description>([^<]+)</description>.*?'
        patronvideos += '(?:<iconurl>([^<]+)</iconurl>)?'
        self.videoItemRegex = patronvideos
        
        patronvideos  = '<src>([^<]+)</src>'
        self.mediaUrlRegex = patronvideos
        
        self.folderItemRegex = ''
        
        logFile = sys.modules['__main__'].globalLogFile
        logFile.debug('InitialiseVariables %s (trace)', self.channelName)
        return True

    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        titulo = resultSet[1]
        logFile.debug("titulo="+titulo)
        url = 'http://es.turbonick.nick.com/dynamo/turbonick/xml/dyn/getIntlGatewayByID.jhtml?id='+resultSet[0]
        logFile.debug("url="+url)

        item = common.clistItem( titulo, url )
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
        
        try:
            titulo = unicode( resultSet[2] + " - " + resultSet[3], "utf-8" ).encode("iso-8859-1")
        except:
            titulo = resultSet[2] + " - " + resultSet[3]
        logFile.debug("titulo="+titulo)
        url = 'http://es.turbonick.nick.com/dynamo/turbonick/xml/dyn/flvgenPT.jhtml?vid='+resultSet[0]+'&hiLoPref=hi'
        logFile.debug("url="+url)
        
        item = common.clistItem( titulo , url )
            
        if self.dictionaryurl.has_key(url):
            logFile.debug("YA AÑADIDA")
            item.type='null'
        else:
            self.dictionaryurl[url] = True
            item.description = titulo
            
            item.thumbUrl = resultSet[1]
            if item.thumbUrl == "":
                item.thumbUrl = resultSet[4]
            if item.thumbUrl == "":
                item.thumb = self.noImage

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
        
        # Averigua la URL
        body = uriHandler.Open(item.url, pb=False)
        matches = common.DoRegexFindAll(self.mediaUrlRegex, body)
        logFile.info('matches[0]='+matches[0])
        item.mediaurl = matches[0]
        #rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv

        #item.mediaurl = 'rtmp://fl1.c00928.cdn.qbrick.com/00928/definst?slist=kluster/20081228/0812292020_GJKLS332'
        #                rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv
        #item.mediaurl = 'rtmp://cp35019.edgefcs.net?slist=ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv'
        logFile.debug("item.mediaurl="+item.mediaurl)
        
        item.complete = True

        return item

    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnUpdateItem(self, selectedIndex):
        logFile.debug('Updating item (Called from ContextMenu)')
        self.onUpDown(ignoreDisabled = True)
    
    def CtMnPlayMplayer(self, selectedIndex):
        logFile.debug('Reproduce usando mplayer')
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, selectedIndex):
        logFile.debug('Reproduce usando dvdplayer')
        item = self.listItems[selectedIndex]
        self.PlayVideoItem(item,"dvdplayer")    
'''
    #============================================================================== 
    def PlayVideoItem(self, item, player=""):
        logFile.debug('PlayVideoItem player=#'+player+'#')

        #http://www.plus.es/tv/bloques.html?id=0&idList=PLTVDO&idVid=725903
        #rtmp://od.flash.plus.es/ondemand/14314/plus/plustv/NF754356.flv
        logFile.debug('aaa')
        nuevoitem = xbmcgui.ListItem("aaa")
        #liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        #liz.setInfo( type="Video", infoLabels={ "Title": name } )
        nuevoitem.setProperty("SWFPlayer", "http://www.plus.es/tv/carcasa.swf")
        #nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        #nuevoitem.setProperty("app", "ondemand")
        nuevoitem.setProperty("PlayPath", "plus/plustv/NF754356.flv")
        #nuevoitem.setProperty("PageURL", pageURL)
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://od.flash.plus.es/ondemand/14314/plus/plustv/NF754356.flv", nuevoitem)

        nuevoitem = xbmcgui.ListItem("svt video")
        nuevoitem.setProperty("SWFPlayer", "http://svt.se/svt/road/Classic/shared/flash/VideoPlayer/svtplayer.swf")
        nuevoitem.setProperty("PlayPath", "kluster/20081228/0812292020_GJKLS332")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://fl1.c00928.cdn.qbrick.com/00928/definst/kluster/20081228/0812292020_GJKLS332", nuevoitem)

        #http://es.turbonick.nick.com/turbonick/
        #rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv
        #/global/apps/broadband/swf/bb_flv_player.swf
        logFile.debug('turbonick')
        nuevoitem = xbmcgui.ListItem("turbonick")
        #liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        #liz.setInfo( type="Video", infoLabels={ "Title": name } )
        #nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/dynamo/droplets/detect/multimedia/loader.swf")
        #nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        #nuevoitem.setProperty("app", "ondemand")
        #nuevoitem.setProperty("PlayPath", "mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv")
        #nuevoitem.setProperty("PageURL", pageURL)
        #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv", nuevoitem)
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/AVATAR1A_OD_640.flv", nuevoitem)

        HOGARUTIL
        logFile.debug('bbb')
        nuevoitem = xbmcgui.ListItem("bbb")
        nuevoitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://aialanetfs.fplive.net/aialanet?slist=Jardineria/palmera-roebelen.flv", nuevoitem)

        #20090324 19:56:56 - INFO     - chn_class.py     - 1020 - Going to playback a single item http://s40.wuapi.com:82/dl/ccaf3f63c5bf12a814d849a7066b32f0/49c92cf5/14202.mp4
        #nuevoitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
        logFile.debug('plustv')
        nuevoitem = xbmcgui.ListItem("plustv")
        nuevoitem.setProperty("app", "ondemand")
        nuevoitem.setProperty("PlayPath", "14314/plus/plustv/PO746516.flv")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://od.flash.plus.es/ondemand/14314/plus/plustv/PO746516.flv", nuevoitem)

        logFile.debug('bbb')
        nuevoitem = xbmcgui.ListItem("bbb")
        #nuevoitem.setProperty("SWFPlayer", "http://www.hogarutil.com/staticFiles/static/player/BigBainetPlayer.swf")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://fm-1334fd73c0eadb85dc66f4fb054a8c3cf3c28ee5.id.velocix.com/flash/?slist=mp4:bt-1334fd73c0eadb85dc66f4fb054a8c3cf3c28ee5", nuevoitem)

        logFile.debug('mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv')
        nuevoitem = xbmcgui.ListItem("mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv")
        nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        nuevoitem.setProperty("PlayPath", "mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv", nuevoitem)

        logFile.debug('_!/intlnick/es/AVATAR/Avatar3b_od640.flv')
        nuevoitem = xbmcgui.ListItem("_!/intlnick/es/AVATAR/Avatar3b_od640.flv")
        nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        nuevoitem.setProperty("PlayPath", "_!/intlnick/es/AVATAR/Avatar3b_od640.flv")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv", nuevoitem)

        logFile.debug('intlnick/es/AVATAR/Avatar3b_od640.flv')
        nuevoitem = xbmcgui.ListItem("intlnick/es/AVATAR/Avatar3b_od640.flv")
        nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        nuevoitem.setProperty("PlayPath", "intlnick/es/AVATAR/Avatar3b_od640.flv")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv", nuevoitem)

        logFile.debug('es/AVATAR/Avatar3b_od640.flv')
        nuevoitem = xbmcgui.ListItem("es/AVATAR/Avatar3b_od640.flv")
        nuevoitem.setProperty("SWFPlayer", "http://es.turbonick.nick.com/global/apps/broadband/swf/bb_flv_player.swf")
        nuevoitem.setProperty("PlayPath", "es/AVATAR/Avatar3b_od640.flv")
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("rtmp://cp35019.edgefcs.net/ondemand/mtviestor/_!/intlnick/es/AVATAR/Avatar3b_od640.flv", nuevoitem)
'''