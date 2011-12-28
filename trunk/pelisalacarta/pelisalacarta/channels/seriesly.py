# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriesly"
__category__ = "S,A"
__type__ = "generic"
__title__ = "Series.ly"
__language__ = "ES"
__creationdate__ = "20111119"

DEBUG = config.get_setting("debug")
SESION = config.get_setting("session","seriesly")
LOGIN = config.get_setting("login","seriesly")
PASSWORD = config.get_setting("password","seriesly")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesly.py] mainlist")

    itemlist = []
    
    itemlist.append( Item(channel=__channel__, title="Buscar series", action="search"))
    itemlist.append( Item(channel=__channel__, title="Mis series", action="series"))
    itemlist.append( Item(channel=__channel__, title="Mis pelis", action="mispelis"))

    if SESION=="true":
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login"))

    return itemlist

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    import xbmc
    keyboard = xbmc.Keyboard("","Login")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        login = keyboard.getText()

    keyboard = xbmc.Keyboard("","Password")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        password = keyboard.getText()

    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    return itemlist

def series(item):

    logger.info("[seriesly.py] Mis Series")

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/api/api_login.php?lg_login="+LOGIN+"&lg_pass="+PASSWORD+"&auth_token="+auth_token
    post = "lg_login=%s&lg_pass=%s" % (LOGIN, PASSWORD)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    #Series Usuario
    
    url="http://series.ly/api/userSeries.php?auth_token="+auth_token+"&user_token="+user_token+"&type=&format=xml"
    data = scrapertools.cache_page(url)
    
    # Extrae las entradas (carpetas)
   
    patron = '<item>(.*?)</item>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<idSerie>(.*?)</idSerie>'
        patron  += '<title>(.*?)</title>'
        patron  += '<seasons>(.*?)</seasons>'
        patron  += '<episodes>(.*?)</episodes>'
        patron  += '<poster>(.*?)</poster>'
        patron  += '<thumb>(.*?)</thumb>'
        patron  += '<small_thumb>(.*?)</small_thumb>'
        patron  += '<status>(.*?)</status>'
        
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://series.ly/api/detailSerie.php?caps=1&auth_token="+auth_token+"&idSerie="+match2[0]+"&user_token="+user_token+"&format=xml"
            scrapedtitle =match2[1]+" ("+match2[2]+" Temporadas) ("+match2[3]+" Episodios)"
            scrapedthumbnail = match2[4]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="capitulos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot,extra=auth_token+"|"+user_token ))
    
    return itemlist

def mispelis(item):

    logger.info("[seriesly.py] Mis Pelis")

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/api/api_login.php?lg_login="+LOGIN+"&lg_pass="+PASSWORD+"&auth_token="+auth_token
    post = "lg_login=%s&lg_pass=%s" % (LOGIN, PASSWORD)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    #Peliculas Usuario
    
    url="http://series.ly/api/userMovies.php?auth_token="+auth_token+"&user_token="+user_token+"&type=&format=xml"
    data = scrapertools.cache_page(url)
    
    # Extrae las entradas (carpetas)
   
    patron = '<item>(.*?)</item>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<idFilm>(.*?)</idFilm>'
        patron  += '<title>(.*?)</title>'       
        patron  += '<year>(.*?)</year>'
        patron  += '<genre>(.*?)</genre>'
        patron  += '<poster>(.*?)</poster>'
        patron  += '<thumb>(.*?)</thumb>'
        patron  += '<small_thumb>(.*?)</small_thumb>'
        patron  += '<status>(.*?)</status>'
        
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://series.ly/api/detailMovie.php?auth_token="+auth_token+"&idFilm="+match2[0]+"&user_token="+user_token+"&format=xml"
            scrapedtitle =match2[1]+" ("+match2[2]+")"
            scrapedthumbnail = match2[4]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="pelis"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot,extra=auth_token+"|"+user_token ))
    
    return itemlist

def capitulos(item):

    logger.info("[seriesly.py] Capitulos")
    
    # TOKENS
    
    auth_token = item.extra.split("|")[0]
    user_token = item.extra.split("|")[1]
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas (carpetas)
   
    patron = '<episode>(.*?)</episode>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<idc>(.*?)</idc>'
        patron  += '<title>(.*?)</title>'
        patron  += '<season>(.*?)</season>'
        patron  += '<viewed>(.*?)</viewed>'
                
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://series.ly/api/linksCap.php?auth_token="+auth_token+"&idCap="+match2[0]+"&user_token="+user_token+"&format=xml"
            scrapedtitle = match2[2]+" - "+match2[1]
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="buscavideos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, extra=auth_token+"|"+user_token+"|"+str(match2[0]) ))
    
    
    return itemlist

def buscavideos(item):

    logger.info("[seriesly.py] Buscavideos")
    
    # TOKENS
    
    auth_token = item.extra.split("|")[0]
    user_token = item.extra.split("|")[1]
    
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas (carpetas)
   
    patron = '<item>(.*?)</item>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<language>(.*?)</language>'
        patron  += '<subtitles>(.*?)</subtitles>'
        patron  += '<hd>(.*?)</hd>.*?'
        patron  += '<url_megavideo>(.*?)</url_megavideo>'
        
               
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl= match2[3].replace("&amp;","&")
            scrapedtitle = item.title+" ("+match2[0]+")(Subtítulos "+match2[1]+")"
            if match2[2]=="1": scrapedtitle += " (HD)"
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="links"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, extra=auth_token+"|"+user_token+"|"+str(match[3]) ))
    
    return itemlist

def links(item):
    
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    listavideos = servertools.findvideos(data)
            
    itemlist = []
    
    for video in listavideos:
        #scrapedtitle = title.strip() + " " + match[1] + " " + match[2] + " " + video[0]
        scrapedtitle = video[0]
        srapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedurl = video[1]
        server = video[2]
            
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot="", server=server, extra="", category=item.category, fanart=item.thumbnail, folder=False))
    
    
    return itemlist

def pelis(item):

    logger.info("[seriesly.py] Pelis")
    
    # TOKENS
    
    auth_token = item.extra.split("|")[0]
    user_token = item.extra.split("|")[1]
    # Extrae las entradas (carpetas)
    
    data = scrapertools.cache_page(item.url)
    patron = '<links>(.*?)</links>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    
    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<language>(.*?)</language>'
        patron  += '<subtitles>(.*?)</subtitles>'        
        patron  += '<quality>(.*?)</quality>'
        patron  += '<part>(.*?)</part>'
        patron  += '<uploader>(.*?)</uploader>'
        patron  += '<highDef>(.*?)</highDef>'
        patron  += '<server>(.*?)</server>.*?'
        patron  += '<url_megavideo>(.*?)</url_megavideo>'
               
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl= "http://series.ly/api/goLink.php?auth_token="+auth_token+"&user_token="+user_token+"&enc="+match2[7].strip()
            scrapedtitle = item.title+" ("+match2[2]+") ("+match2[0]+")(Subtítulos "+match2[1]+") (Parte "+match2[3]+")"
            if match2[5]=="1": scrapedtitle += " (HD)"
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="links"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, extra=auth_token+"|"+user_token+"|"+str(match[3]) ))
    
    return itemlist

def search(item,texto, categoria="*"):
    logger.info("[cuevana.py] search")
    
     # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/api/api_login.php?lg_login="+LOGIN+"&lg_pass="+PASSWORD+"&auth_token="+auth_token
    post = "lg_login=%s&lg_pass=%s" % (LOGIN, PASSWORD)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    url="http://series.ly/api/search.php?auth_token="+auth_token+"&search="+texto+"&type=serie&format=xml"
    
    # Extrae las entradas (carpetas)
    
    data = scrapertools.cache_page(url)
    patron = '<item>(.*?)</item>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<idSerie>(.*?)</idSerie>'
        patron  += '<title>(.*?)</title>'
        patron  += '<seasons>(.*?)</seasons>'
        patron  += '<episodes>(.*?)</episodes>'
        patron  += '<poster>(.*?)</poster>'
        patron  += '<thumb>(.*?)</thumb>'
        patron  += '<small_thumb>(.*?)</small_thumb>'
        
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://series.ly/api/detailSerie.php?caps=1&auth_token="+auth_token+"&idSerie="+match2[0]+"&user_token="+user_token+"&format=xml"
            scrapedtitle =match2[1]+" ("+match2[2]+" Temporadas) ("+match2[3]+" Episodios)"
            scrapedthumbnail = match2[4]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="capitulos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot,extra=auth_token+"|"+user_token ))
    
    return itemlist