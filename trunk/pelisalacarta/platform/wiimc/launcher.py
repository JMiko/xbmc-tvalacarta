# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from core import config

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("wiimc")

def controller(plugin_name,port,host,path,headers):

    respuesta = ""

    respuesta += "version=7\n"
    respuesta += "logo=http://www.mimediacenter.info/xbmc/tvalacarta/icon.jpg\n"
    respuesta += "title="+plugin_name+" 3.0.0 (WiiMC)\n"
    respuesta += "\n"

    if path == "/wiimc/" or path=="/wiimc":
        import channelselector
        channelslist = channelselector.getmainlist()

        for channel in channelslist:

            # Quita el canal de ayuda y el de configuración, no sirven en WiiMC
            if channel.channel!="configuracion" and channel.channel!="ayuda":
                respuesta += "type=playlist\n"
                respuesta += "name="+channel.title+"\n"
                respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
                respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/"+channel.action+"/none/none/playlist.plx\n"
                respuesta += "\n"
    
    elif path.startswith("/wiimc/channelselector/channeltypes"):
        
        import channelselector
        channelslist = channelselector.getchanneltypes()
        
        for channel in channelslist:
            respuesta += "type=playlist\n"
            respuesta += "name="+channel.title+"\n"
            respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
            respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/"+channel.action+"/"+channel.category+"/none/playlist.plx\n"
            respuesta += "\n"
    
    elif path.startswith("/wiimc/channelselector/listchannels"):
        
        category = path.split("/")[4]
        logger.info("##category="+category)

        import channelselector
        channelslist = channelselector.filterchannels(category)
        
        for channel in channelslist:
            if channel.type=="generic" or channel.type=="wiimc":
                respuesta += "type=playlist\n"
                respuesta += "name="+channel.title+"\n"
                respuesta += "thumb=http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.channel+".png\n"
                respuesta += "URL=http://"+host+"/wiimc/"+channel.channel+"/mainlist/none/none/playlist.plx\n"
                respuesta += "\n"

    else:
        from platform.wiimc import wiitools
        itemlist,channel = wiitools.getitems(path)
        
        import urllib
        for item in itemlist:
            if item.action=="search":
                logger.info("  Buscador")
                if item.server=="": item.server="none"
                if item.url=="": item.url="none"
                url = "http://%s/%s/%s/%s/%s/playlist.plx" % ( host+"/wiimc" , channel , item.action , urllib.quote_plus(item.url) , item.server )               
                respuesta += "type=search\n"
                respuesta += "name=%s\n" % item.title
                if item.thumbnail != "":
                    respuesta += "thumb=%s\n" % item.thumbnail
                respuesta += "URL=%s\n" % url
                respuesta += "\n"
 
            elif item.folder or item.action=="play":
                logger.info("  Nivel intermedio")
                if item.server=="": item.server="none"
                if item.url=="": item.url="none"
                if item.title=="": item.title="Ver el video-"

                url = "http://%s/%s/%s/%s/%s/%s/playlist.plx" % ( host+"/wiimc" , channel , item.action , urllib.quote_plus(item.url) , item.server ,urllib.quote_plus(item.title) )
                respuesta += "type=playlist\n"
                respuesta += "name=%s\n" % item.title
                if item.thumbnail != "":
                    respuesta += "thumb=%s\n" % item.thumbnail
                respuesta += "URL=%s\n" % url
                respuesta += "\n"
            else:
                logger.info("  Video")
                respuesta += "type=video\n"
                respuesta += "name=%s\n" % item.title
                respuesta += "URL=%s\n" % item.url
                respuesta += "\n"

    return respuesta