# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidbull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs
import time

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidbull.py] url="+page_url)
        
    # Lo pide una vez
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    time.sleep(5)
    '''
    <input type="hidden" name="op" value="download2">
    <input type="hidden" name="id" value="8sueg0neje36">
    <input type="hidden" name="rand" value="qzeeevxsks6b57ax2et273j2d7bmdmypzhus3fi">
    <input type="hidden" name="referer" value="">
    
    <input type="hidden" name="method_free" value="">
    <input type="hidden" name="method_premium" value="">
    '''
    op = scrapertools.get_match( data , '<input type="hidden" name="op" value="([^"]+)">')
    id = scrapertools.get_match( data , '<input type="hidden" name="id" value="([^"]+)">')
    randval = scrapertools.get_match( data , '<input type="hidden" name="rand" value="([^"]+)">')

    #op=download2&id=8sueg0neje36&rand=f5ine3x7qo2pa2upku5wbnjktdwvn325mulc4hy&referer=&method_free=&method_premium=&down_direct=1
    post = "op="+op+"&id="+id+"&rand="+randval+"&referer=&method_free=&method_premium=&down_direct=1"
    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    logger.info("data="+data)

    # Extrae el trozo cifrado
    '''
    script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('2l 2=2k 2j(\'a://8.6/e/e.2i\',\'e\',\'2h\',\'2g\',\'9\');2.c(\'2f\',\'f\');2.c(\'2e\',\'2d\');2.c(\'2c\',\'f\');2.c(\'2b\',\'5\');2.c(\'2a\',\'29\');2.4(\'28\',\'../e/27.26\');2.4(\'25\',\'24\');2.4(\'m\',\'a://p.8.6:23/d/21/o.20\');2.4(\'1z\',\'a://p.8.6/i/1y/h.1x\');2.4(\'1w\',\'o\');2.4(\'1v.l\',\'1u\');2.4(\'1t\',\'1s\');2.4(\'1r\',\'j-3\');2.4(\'j.k\',\'a://8.6/h\');2.4(\'j.1q\',\'%1p+1o%1n%1m%1l%1k%1j.6%1i-h-1h.1g%22+1f%g+1e%g+1d%g+1c%1b+1a%19+18%17%n%16%14%n\');2.4(\'b.m\',\'a://8.6/13/12.11\');2.4(\'b.10\',\'f\');2.4(\'b.z\',\'15\');2.4(\'b.y\',\'1\');2.4(\'b.x\',\'0.7\');2.4(\'b.l\',\'w-v\');2.4(\'b.k\',\'a://8.6\');2.4(\'u\',\'t\');2.4(\'s\',\'a://8.6\');2.r(\'q\');',36,94,'||s1||addVariable||com||vidbull||http|logo|addParam||player|true|3D0|ytq373bhddsq||sharing|link|position|file|3E|video|fs4|flvplayer|write|aboutlink|VidBull|abouttext|right|top|out|over|timeout|hide|png|vidbull_playerlogo|images|2FIFRAME||3C|3D338|HEIGHT|3D640|WIDTH|3DNO|SCROLLING|MARGINHEIGHT|MARGINWIDTH|FRAMEBORDER|html|640x318|2Fembed|2Fvidbull|2F|3A|22http|3D|SRC|3CIFRAME|code|plugins|uniform|stretching|left|dock|provider|jpg|00005|image|flv|5fslq63iljrwuxim4m6wx32uxk7nv6rb3orixchf7fgrowdfiwuy5gqp||182|5271|duration|zip|modieus1|skin|opaque|wmode|bufferlength|autostart|always|allowscriptaccess|allowfullscreen|318|640|swf|SWFObject|new|var'.split('|')))
    '''
    patron = "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d\).*?)</script>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado=""
    for match in matches:
        logger.info("match="+match)
        if "mp4" in match or "flv" in match or "video" in match:
            cifrado = match
            break
    
    # Extrae la URL del vídeo
    logger.info("cifrado="+cifrado)
    descifrado = unpackerjs.unpackjs(cifrado)
    descifrado = descifrado.replace("\\","")
    logger.info("descifrado="+descifrado)
    
    # Extrae la URL
    #media_url = scrapertools.get_match(descifrado,"s1.addVariable\('file','([^']+)'\)")
    #<param name="src"value="http://fs10.vidbull.com:182/d/4zsdjpllljrwuximze6sd2yu4a4udufkfckbb5nyt2yku5c7qcqmh5y4/video.avi"/>
    media_url = scrapertools.get_match(descifrado,'<param name="src"value="([^"]+)"')
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vidbull]",media_url])

    for video_url in video_urls:
        logger.info("[vidbull.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidbull.com/3360qika02mo
    # http://vidbull.com/6efa0ns1dpxc.html
    patronvideos  = 'vidbull.com/([A-Z0-9a-z\.]+)'
    logger.info("[vidbull.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidbull]"
        url = "http://vidbull.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidbull' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
