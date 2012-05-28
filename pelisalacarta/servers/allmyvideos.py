# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Descarga
    data = scrapertools.cache_page( page_url )
    packed = scrapertools.get_match( data , "(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d.*?)</script>",1)
    
    from core import unpackerjs
    unpacked = unpackerjs.unpackjs(packed)
    #('var starttime=$.cookie(\'vposm7p03lbkysdw\');if(starttime==undefined)starttime=0;jwplayer(\'flvplayer\').setup({\'id\':\'playerID\',\'width\':\'960\',\'height\':\'511\',\'file\':\'http://66.220.4.230:182/d/3omd5q77yq5dh6lnhlgzlnwmpjsz6jak4r4dalwptfh3auyzpfu2og6u/video.mp4\',\'image\':\'http://66.220.4.230/i/00012/m7p03lbkysdw.jpg\',\'duration\':\'5836\',\'streamscript\':\'lighttpd\',\'provider\':\'http\',\'http.startparam\':\'start\',\'dock\':\'true\',\'viral.onpause\':\'false\',\'viral.callout\':\'none\',\'start\':starttime,\'plugins\':\'captions-2,fbit-1,timeslidertooltipplugin-3,/player/ova-jw.swf,sharing-3\',\'timeslidertooltipplugin.preview\':{\'enabled\':true,\'path\':\'http://66.220.4.230:182/p/00012/m7p03lbkysdw/\',\'prefix\':\'m7p03lbkysdw_\'},\'sharing.link\':\'http://allmyvideos.net/m7p03lbkysdw\',\'sharing.code\':\'<IFRAME SRC="http://allmyvideos.net/embed-h08ml8bdrpvw-960x511.html" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=960 HEIGHT=531></IFRAME>\',\'config\':\'/player/ova.xml\',\'logo.hide\':\'false\',\'logo.position\':\'top-left\',\'logo.file\':\'/player/gopremium.png\',\'logo.link\':\'/premium.html\',\'skin\':\'/player/skins/bekle.zip\',\'dock.position\':\'left\',\'controlbar.position\':\'bottom\',\'modes\':[{type:\'flash\',src:\'/player/player.swf\'},{type:\'html5\'}]});var playerVersion=swfobject.getFlashPlayerVersion();var output=\'You have Flash player \'+playerVersion.major+\'.\'+playerVersion.minor+\'.\'+playerVersion.release+\' installed\';if((playerVersion.major<1)&&(navigator.appVersion.indexOf(\'iPhone\')==-1)&&(navigator.appVersion.indexOf(\'Android\')==-1)){document.getElementById(\'flashnotinstalled\').style.display=\'block\'}',511,00012player,
    unpacked = unpacked.replace("\\","")
    location = scrapertools.get_match(unpacked,"'file'\:'([^']+)'")+"?start=0"
    
    video_urls = []
    
    import urlparse
    parsed_url = urlparse.urlparse(location)
    
    video_urls.append( [ parsed_url.path[-4:] + " [allmyvideos]",location ] )

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/fg85ovidfwxx
    patronvideos  = '(allmyvideos.net/[a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
