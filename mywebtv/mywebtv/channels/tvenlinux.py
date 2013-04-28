# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal TVenLinux
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tvenlinux"
__type__ = "generic"
__title__ = "TVenLinux"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("mywebtv.channels.tvenlinux.mainlist")
    itemlist = []

    # Lee el script
    filename = os.path.join( config.get_runtime_path() , "streams" , "TVenLinux.sh" )
    f = open(filename)
    data = f.read()
    f.close()

    # Busca el bloque con los canales
    canales = scrapertools.get_match(data,"case \$CANAL in(.*?)esac")
    #logger.info("[tvenlinux.py] canales="+canales)
    lineas = canales.split(";;")
    for linea in lineas:
        logger.info("linea="+linea.strip())

        try:
            title = scrapertools.get_match(linea+";;",'(.*?)\).*?\;\;').strip()
            url = scrapertools.get_match(linea+";;",'.*?\)(.*?)\;\;')
            
            #rtmpdump -m 200 -r "rtmp://cp68975.live.edgefcs.net:1935/live" -y "LA1_AKA_WEB_NOG@58877" -W "http://www.rtve.es/swf/4.1.11/RTVEPlayerVideo.swf" -p "http://www.rtve.es/noticias/directo-la-1"
            #  -t "rtmp://cp68975.live.edgefcs.net:1935/live" -v -q -o /tmp/$CANAL."$ID" & ;;
            #    url=full_url + " app=" + app + " swfUrl=" + swfurl + " playpath=" + playpath + " pageUrl="+pageurl

            '''
            02:21:05 T:2957651968   ERROR: Valid RTMP options are:
            02:21:05 T:2957651968   ERROR:      socks string   Use the specified SOCKS proxy
            02:21:05 T:2957651968   ERROR:        app string   Name of target app on server
            02:21:05 T:2957651968   ERROR:      tcUrl string   URL to played stream
            02:21:05 T:2957651968   ERROR:    pageUrl string   URL of played media's web page
            02:21:05 T:2957651968   ERROR:     swfUrl string   URL to player SWF file
            02:21:05 T:2957651968   ERROR:   flashver string   Flash version string (default MAC 10,0,32,18)
            02:21:05 T:2957651968   ERROR:       conn AMF      Append arbitrary AMF data to Connect message
            02:21:05 T:2957651968   ERROR:   playpath string   Path to target media on server
            02:21:05 T:2957651968   ERROR:   playlist boolean  Set playlist before play command
            02:21:05 T:2957651968   ERROR:       live boolean  Stream is live, no seeking possible
            02:21:05 T:2957651968   ERROR:  subscribe string   Stream to subscribe to
            02:21:05 T:2957651968   ERROR:        jtv string   Justin.tv authentication token
            02:21:05 T:2957651968   ERROR:       weeb string   Weeb.tv authentication token
            02:21:05 T:2957651968   ERROR:      token string   Key for SecureToken response
            02:21:05 T:2957651968   ERROR:     swfVfy boolean  Perform SWF Verification
            02:21:05 T:2957651968   ERROR:     swfAge integer  Number of days to use cached SWF hash
            02:21:05 T:2957651968   ERROR:    swfsize integer  Size of the decompressed SWF file
            02:21:05 T:2957651968   ERROR:    swfhash string   SHA256 hash of the decompressed SWF file
            02:21:05 T:2957651968   ERROR:      start integer  Stream start position in milliseconds
            02:21:05 T:2957651968   ERROR:       stop integer  Stream stop position in milliseconds
            02:21:05 T:2957651968   ERROR:     buffer integer  Buffer time in milliseconds
            02:21:05 T:2957651968   ERROR:    timeout integer  Session timeout in seconds
            '''
            url = url.replace("rtmpdump ","")
            url = url.replace("\"","")
            url = re.compile("-m \d+",re.DOTALL).sub("",url)
            url = url.replace("-y ","playpath=")
            url = url.replace("-a ","app=")
            url = url.replace("-W ","swfVfy=")
            url = url.replace("-p ","pageUrl=")
            url = url.replace("-t ","tcUrl=")
            url = url.replace("-v ","live=true")
            url = url.replace("-q ","")
            url = re.compile("-o\s+[^\s]+\s+&",re.DOTALL).sub("",url)
            url = url.replace("> /tmp/$CANAL.$ID &","")
            url = url + " timeout=300"
            
            rtmpurl = scrapertools.get_match(url,"-r\s+([^\s]+)")
            url = re.compile("-r\s+[^\s]+",re.DOTALL).sub("",url)
            url = rtmpurl + url
            url = re.compile("\s+",re.DOTALL).sub(" ",url)

            itemlist.append( Item( channel=__channel__ , action="play" , title=title , url=url, folder=False))

        except:
            pass

    return itemlist