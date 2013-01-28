# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools

from core import config
from core import logger

logger.info("[servertools.py] init")

def findvideos(data):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []

    # Megavideo - Vídeos con título
    logger.info("1) Megavideo con titulo...")
    patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[0].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = match[1]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    logger.info("1b) Megavideo con titulo...")
    patronvideos  = '<a href\="http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})".*?>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("1c) Megavideo sin titulo...")
    #http://www.megavideo.com/?v=OYGXMZBM
    patronvideos  = 'http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        titulo = ""
        if titulo == "":
            titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("1d) Megavideo sin titulo...")
    #http://www.megavideo.com/?v=OYGXMZBM
    patronvideos  = 'http\:\/\/www.megavideo.com/\?v\=([A-Z0-9]{8})'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        titulo = ""
        if titulo == "":
            titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # KOCHIKAME - Megaupload - Vídeos con título
    logger.info("1k) Megaupload con titulo...")
    patronvideos  = '<a href\="http\:\/\/www.megaupload.com/\?d\=([^"]+)".*?>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = match[1].strip()+" - [Megaupload]"
        if titulo[0:3] == "Cap":
            titulo = titulo[9:]
        url = match[0]
        if url == "3P78ET7H":
            titulo = "012 - "+titulo
        if url == "99D5HEEY":
            titulo = "000 - (muestra <1min)"
            titulo = titulo.replace('&#33;' , '!') 

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("1d) Megaupload sin titulo...")
    #http://www.megavideo.com/?v=OYGXMZBM
    patronvideos  = 'http\:\/\/www.megaupload.com/\?d\=([A-Z0-9]{8})'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        titulo = ""
        if titulo == "":
            titulo = "[Megaupload]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("13) Megaupload sin titulo...")
    #http://www.megaupload.com/?s=tumejortv&confirmed=1&d=6FQOWHTI
    patronvideos  = 'http\:\/\/www.megaupload.com/.*?d\=([A-Z0-9]{8})'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        titulo = ""
        if titulo == "":
            titulo = "[Megaupload]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    logger.info("2) Megavideo sin titulo...")
    patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Vreel - Vídeos con título
    logger.info( "3) Vreel con título...")
    patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[0].strip()
        if titulo == "":
            titulo = "[Vreel]"
        url = match[1]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Vreel' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Vreel - Vídeos con título
    logger.info("4) Vreel con titulo...")
    patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[0].strip()
        if titulo == "":
            titulo = "[Vreel]"
        url = match[1]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Vreel' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    '''
    # WUAPI
    logger.info("5) wuapi sin título")
    patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "Sin título ("+match[23:]+")"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Wuapi' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # WUAPI
    logger.info("6) wuapi sin título...")
    patronvideos  = '(http://wuapi.com[^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "Sin título ("+match[23:]+")"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Wuapi' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    '''
    
    # STAGEVU
    logger.info("7) Stagevu sin título...")
    patronvideos  = '"(http://stagevu.com[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Stagevu]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # TU.TV
    logger.info("8) Tu.tv sin título...")
    patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tu.tv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # TU.TV
    logger.info("9) Tu.tv sin título...")
    #<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
    patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tu.tv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("9b) Tu.tv sin título...")
    #<embed src="http://tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aW
    patronvideos  = '<embed src="(http://tu.tv/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tu.tv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    logger.info("10 ) Megavideo sin titulo...")
    patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    logger.info("11) Megavideo sin titulo...")
    patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # STAGEVU
    '''
    logger.info("12) Stagevu...")
    patronvideos  = '(http://stagevu.com[^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "Ver el vídeo en Stagevu"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    '''
        
    # Vreel - Vídeos sin título
    logger.info("13) Vreel sin titulo...")
    patronvideos  = '(http://beta.vreel.net[^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Vreel]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Vreel' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    logger.info("14) Megavideo con titulo...")
    patronvideos  = '<a href="http://www.megavideo.com/\?v\=([^"]+)".*?>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = match[1].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    logger.info("14b) Megavideo con titulo...")
    patronvideos  = '<param name="movie" value=".*?v\=([A-Z0-9]{8})" />'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Stagevu...")
    patronvideos  = '"http://stagevu.com.*?uid\=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Stagevu]"
        url = "http://stagevu.com/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Megavideo... formato d=XXXXXXX")
    patronvideos  = '"http://www.megavideo.com/.*?\&d\=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Megaupload... formato megavideo con d=XXXXXXX")
    patronvideos  = '"http://www.megavideo.com/\?d\=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Movshare...")
    patronvideos  = '"(http://www.movshare.net/video/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Movshare]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Veoh...")
    patronvideos  = '"http://www.veoh.com/veohplayer.swf.*?permalinkId=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Veoh]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veoh' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Directo - myspace")
    patronvideos  = 'flashvars="file=(http://[^\.]+.myspacecdn[^\&]+)&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def findurl(code,server):
    mediaurl = "ERROR"
    if server == "justintv":
        from servers import justintv
        mediaurl = justintv.get_video_url(code)[0][1]
        logger.info("mediaurl="+str(mediaurl))
        
    if server == "ustream":
        from servers import ustream
        mediaurl = ustream.get_video_url(code)[0][1]
        logger.info("mediaurl="+str(mediaurl))
        
    if server == "Megavideo":
        mediaurl = megavideo.Megavideo(code)
        
    if server == "Megaupload":
        mediaurl = megaupload.getvideo(code)
        
    if server == "Wuapi":
        mediaurl = wuapi.Wuapi(code)
        
    if server == "Vreel":
        mediaurl = vreel.Vreel(code)

    if server == "Stagevu":
        mediaurl = stagevu.Stagevu(code)
    
    if server == "tu.tv":
        mediaurl = tutv.Tutv(code)
    
    if server == "movshare":
        mediaurl = movshare.getvideo(code)
    
    if server == "veoh":
        mediaurl = veoh.getvideo(code)
    
    if server == "Directo":
        mediaurl = code
    return mediaurl

def getmegavideolow(code):
    return megavideo.getlowurl(code)

def getmegavideohigh(code):
    return megavideo.gethighurl(code)

def getmegauploadhigh(code):
    return megaupload.gethighurl(code)

def getmegauploadlow(code):
    return megaupload.getlowurl(code)