# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para filmixt
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmixt"
__category__ = "F"
__type__ = "generic"
__title__ = "Filmixt"
__language__ = "ES"

DEBUG = config.get_setting("debug")

SESION = config.get_setting("session","filmixt")
LOGIN = config.get_setting("login","filmixt")
PASSWORD = config.get_setting("password","filmixt")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descarregadirecta.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="Generico"        , title="Estrenos"                      , url="http://filmixt.com/descarga-6-0-0-0-fx-1-1.fx"))
    itemlist.append( Item(channel=__channel__ , action="Generico"         , title="Dibuixos"            , url="http://www.descarregadirecta.com/browse-dibuixos-videos-1-date.html"))
    itemlist.append( Item(channel=__channel__ , action="Generico"        , title="Documentales"          , url="http://www.descarregadirecta.com/browse-documentals-videos-1-date.html" ))
    itemlist.append( Item(channel=__channel__ , action="Generico"         , title="Esports"               , url="http://www.descarregadirecta.com/browse-esports-videos-1-date.html" ))
    itemlist.append( Item(channel=__channel__ , action="Generico"         , title="Series"               , url="http://www.descarregadirecta.com/browse-series-videos-1-date.html" ))
    itemlist.append( Item(channel=__channel__ , action="Generico"         , title="Pel·licules per Génere (Registre Necessàri)"               , url="http://www.descarregadirecta.com/browse-pelicules-videos-1-artist.html" ))
    itemlist.append( Item(channel=__channel__ , action="buscavideos"         , title="Totes Les Pel·licules (Registre Necessàri)"               , url="http://www.descarregadirecta.com/browse-pelicules-videos-1-artist.html" ))
    
    if SESION=="true":

        perform_login(LOGIN,PASSWORD)

        itemlist.append( Item(channel=__channel__, title="Tancar sessió("+LOGIN+")", action="logout"))

    else:

        itemlist.append( Item(channel=__channel__, title="Iniciar sessió", action="login"))
    
    return itemlist


def Generico(item):
    logger.info("[filmixt.py] Generico")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<div class="fichaMiniPortada">(.*?)<div class="masdatos">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        patron  = '<a href="([^"]+)" class="imagenFicha" title="[^"]+" style="background\-image\:url\((.*?)\);"></a[^<]+'
        patron += '<a href="[^"]+" class="titleFicha" title="[^"]+">([^<]+)</a>[^<]+'
        patron += '<a href="[^"]+" class="calidadFicha" title="[^"]+">([^<]+)<'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = match2[0]
            scrapedtitle =match2[2]+" ("+match2[3]+")"
            scrapedthumbnail = "http://filmixt.com/"+match2[1]
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            
            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="buscavideos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist

def buscavideos(item):
    logger.info("[filmixt.py] BuscaVideos")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    

    patron = '<div class="descAdicionales">.*?<div class="links">.*?<a href="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    logger.info(matches[0])
    
    url = matches[0]
    data = scrapertools.cachePage(url)
    
    logger.info(data)
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist

def detail(item):
    logger.info("[Descarregadirecta.py] detail")

    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    scrapedurl = ""
    url = item.url

    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Usa findvideos    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))



    return itemlist

def login(item):
    if config.get_platform() in ("wiimc", "rss"):
        login = config.get_setting("filmixtuser")
        password = config.get_setting("filmixtpassword")
        if login<>"" and password<>"":
            url="http://in.perfilunico.com/?web=5835&alerts=1&web_data=http://filmixt.com/"
            data = scrapertools.cache_page("http://in.perfilunico.com/?web=5835&alerts=1&web_data=http://filmixt.com/",post="username=%s&password=%s" % (login,password))
            itemlist = []
            itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    else:
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
    
def perform_login(login,password):
    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias
    login = login.replace("@","%40")
    data = scrapertools.cache_page("http://in.perfilunico.com/?web=5835&alerts=1&web_data=http://filmixt.com/",post="username=%s&password=%s" % (login,password))
    
    data = scrapertools.cache_page("http://filmixt.com/login.php",post="username=%s&password=%s" % (login,password))
   
    
    
    
def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
    return itemlist