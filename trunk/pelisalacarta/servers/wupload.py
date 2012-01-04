# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Wupload (sÃ³lo filenium)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[wupload.py] get_video_url(page_url='%s')" % page_url)

    location = scrapertools.get_header_from_response(page_url,header_to_get="location")
    if location!="":
        page_url = location

    logger.info("[wupload.py] location=%s" % page_url)

    video_id = extract_id(page_url)
    logger.info("[wupload.py] video_id=%s" % video_id)

    data = scrapertools.cache_page(url=page_url)
    patron = 'href="(.*?start=1.*?)"'
    matches = re.compile(patron).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        logger.error("[wupload.py] No encuentra el enlace Free")
        return []
    
    # Obtiene link de descarga free
    download_link = matches[0]
    if not download_link.startswith("http://"):
        download_link = urlparse.urljoin(page_url,download_link)

    logger.info("[wupload.py] Link descarga: "+download_link)

    # Descarga el enlace
    headers = []
    headers.append( ["X-Requested-With", "XMLHttpRequest"] )
    headers.append( ["Referer"         , page_url ])
    headers.append( ["User-Agent"      , "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12" ])
    headers.append( ["Content-Type"    , "application/x-www-form-urlencoded; charset=UTF-8"])
    headers.append( ["Accept-Encoding" , "gzip, deflate"])
    headers.append( ["Accept","*/*"])
    headers.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"])
    headers.append( ["Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"])
    headers.append( ["Connection","keep-alive"])
    headers.append( ["Pragma","no-cache"])
    headers.append( ["Cache-Control","no-cache"])

    data = scrapertools.cache_page( download_link , headers=headers, post="" )
    logger.info(data)
    
    while True:
        # Detecta el tiempo de espera
        patron = "countDownDelay = (\d+)"
        matches = re.compile(patron).findall(data)
        if len(matches)>0:
            tiempo_espera = int(matches[0])
            logger.info("[wupload.py] tiempo de espera %d segundos" % tiempo_espera)
            
            #import time
            #time.sleep(tiempo_espera)
            from platformcode.xbmc import xbmctools
            resultado = xbmctools.handle_wait(tiempo_espera+5,"Progreso","Conectando con servidor Wupload (Free)")
            if resultado == False:
                break

            tm = scrapertools.get_match(data,"name='tm' value='([^']+)'")
            tm_hash = scrapertools.get_match(data,"name='tm_hash' value='([^']+)'")
            post = "tm=" + tm + "&tm_hash=" + tm_hash
            data = scrapertools.cache_page( download_link , headers=headers, post=post )
            logger.info(data)
        else:
            logger.info("[wupload.py] no encontrado tiempo de espera")
    
        # Detecta captcha
        patron = "Recaptcha\.create"
        matches = re.compile(patron).findall(data)
        if len(matches)>0:
            logger.info("[wupload.py] está pidiendo el captcha")
            recaptcha_key = scrapertools.get_match( data , 'Recaptcha\.create\("([^"]+)"')
            logger.info("[wupload.py] recaptcha_key="+recaptcha_key)

            data_recaptcha = scrapertools.cache_page("http://www.google.com/recaptcha/api/challenge?k="+recaptcha_key)
            patron="challenge.*?'([^']+)'"
            challenges = re.compile(patron, re.S).findall(data_recaptcha)
            if(len(challenges)>0):
                challenge = challenges[0]
                image = "http://www.google.com/recaptcha/api/image?c="+challenge
                
                #CAPTCHA
                exec "import pelisalacarta.captcha as plugin"
                tbd = plugin.Keyboard("","",image)
                tbd.doModal()
                confirmed = tbd.isConfirmed()
                if (confirmed):
                    tecleado = tbd.getText()

            post = "recaptcha_challenge_field=%s&recaptcha_response_field=%s" % (challenge,tecleado.replace(" ","+"))
            data = scrapertools.cache_page( download_link , headers=headers, post=post )
            logger.info(data)

        else:
            logger.info("[wupload.py] no encontrado captcha")
    
        # Detecta captcha
        patron = '<p><a href="(http\:\/\/.*?wupload[^"]+)">'
        matches = re.compile(patron).findall(data)
        if len(matches)>0:
            final_url = matches[0]
            '''
            'GET /download/2616019677/4f0391ba/9bed4add/0/1/580dec58/3317afa30905a31794733c6a32da1987719292ff
            HTTP/1.1
            Accept-Language: es-es,es;q=0.8,en-us;q=0.5,en;q=0.3
            Accept-Encoding: gzip, deflate
            Connection: close\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12
            Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
            Host: s107.wupload.es
            Referer: http://www.wupload.es/file/2616019677
            Pragma: no-cache
            Cache-Control: no-cache
            X-Requested-With: XMLHttpRequest
            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
            Cookie: lastUrlLinkId=2616019677\r\n\r\n'
            00:39:39 T:2956623872  NOTICE: reply:
            00:39:39 T:2956623872  NOTICE: 'HTTP/1.1 200 OK\r\n'
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Server: nginx
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Date: Tue, 03 Jan 2012 23:39:39 GMT
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Content-Type: "application/octet-stream"
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Content-Length: 230336429
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Last-Modified: Tue, 06 Sep 2011 01:07:26 GMT
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Connection: close
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: Set-Cookie: dlc=1; expires=Thu, 02-Feb-2012 23:39:39 GMT; path=/; domain=.wupload.es
            00:39:39 T:2956623872  NOTICE: header:
            00:39:39 T:2956623872  NOTICE: : attachment; filename="BNS609.mp4"
            '''
            logger.info("[wupload.py] link descarga "+final_url)
            final_url = final_url + "|" + urllib.quote("Referer=http://www.wupload.es/file/"+video_id+"&Cookie=lastUrlLinkId="+video_id)
            return [["(Free)",final_url]]
        else:
            logger.info("[wupload.py] no detectado link descarga")

    return []

def extract_id(url):
    return scrapertools.get_match(url,'wupload.*?/file/(\d+)')

def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = '(http://www.wupload.*?/file/\d+)'
    logger.info("[wupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[wupload]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'wupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve