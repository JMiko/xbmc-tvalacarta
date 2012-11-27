# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videopremium
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#LvX Edited Patched

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videopremium.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    # Lee la URL
    data = scrapertools.cache_page( page_url )
    logger.info("data="+data)
    bloque = scrapertools.get_match(data,'<Form[^>]*method="POST"(.*)</.orm>')
    logger.info("bloque="+bloque)
    op = scrapertools.get_match(bloque,'<input type="hidden" name="op" value="([^"]+)"')
    usr_login = scrapertools.get_match(bloque,'<input type="hidden" name="usr_login" value="([^"]*)"')
    id = scrapertools.get_match(bloque,'<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(bloque,'<input type="hidden" name="fname" value="([^"]+)"')
    referer = scrapertools.get_match(bloque,'<input type="hidden" name="referer" value="([^"]*)"')
    method_free = scrapertools.get_match(bloque,'<input type="[^"]+" name="method_free" value="([^"]+)"')

    # Simula el botón
    #op=download1&usr_login=&id=buq4b8zunbm6&fname=Snow.Buddies-Avventura.In.Alaska.2008.iTALiAN.AC3.DVDRip.H264-PsYcOcReW.avi&referer=&method_free=Watch+Free%21
    post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free
    data = scrapertools.cache_page( page_url , post=post )
    #logger.info("data="+data)
    
    try:
        packed = scrapertools.get_match(data,"(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d\).*?</script>)")
    except:
        packed = scrapertools.get_match(data,"(function\(p, a, c, k, e, d\).*?</script>)")
        packed = "<script type='text/javascript'>eval("+packed

    logger.info("packed="+packed)

    from core import unpackerjs
    unpacked = unpackerjs.unpackjs(packed)
    logger.info("unpacked="+unpacked)


    data=re.search("flowplayer\(\"vplayer\",\"(http://.*?)\",\{key:\\\\'[#\\$0-9-a-f]+\\\\',clip:\{url:\\\\'(.*?)\\\\',provider:\\\\'rtmp\\\\',.*?,netConnectionUrl:\\\\'([^']+)",unpacked)
    '''
    _TEMPLATE_LIVE_URL       = "%s/videochat playpath=stream_%s swfurl=%s swfvfy=true pageUrl=%s"
            rtmp  = re.compile('rtmp="(.+?)"').findall(response)[0]
            image = re.compile('image="(.+?)"').findall(response)[0]
            id    = re.compile('id="(.+?)"').findall(response)[0]
            livelink = _TEMPLATE_LIVE_URL % (rtmp,id,_SWF_URL,_TEMPLATE_URL % (code))
    '''
    location = data.group(3) + " playpath=" + data.group(2) + " swfurl=" +data.group(1) +" swfvfy=true pageUrl=" + page_url
    logger.info("location="+location)
    extension="videopremium.net"
    '''
    location = scrapertools.get_match(data,"url\: '([^']+)'")

    try:
        import urlparse
        parsed_url = urlparse.urlparse(location)
        logger.info("parsed_url="+str(parsed_url))
        extension = parsed_url.path[-4:]
    except:
        if len(parsed_url)>=4:
            extension = parsed_url[2][-4:]
        else:
            extension = ""
    '''
    video_urls.append( [ extension + " [videopremium]",location ] )

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html" target="_blank">1° Tempo</a>
    patronvideos  = '<a href="(http://videopremium.net[^"]+)"[^>]+>([^<]+)</a>'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]+" [videopremium]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

    #http://videopremium.net/buq4b8zunbm6
    #http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html
    patronvideos  = '(videopremium.net/[a-z0-9]+)'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videopremium]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
