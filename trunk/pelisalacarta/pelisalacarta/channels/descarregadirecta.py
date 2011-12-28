# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal Descarregadirecta Carles Carmona
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

__channel__ = "descarregadirecta"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Descarrega Directa (CAT)"
__language__ = "CAT"
__creationdate__ = "20111019"

DEBUG = config.get_setting("debug")

SESION = config.get_setting("session","descarregadirecta")

LOGIN = config.get_setting("login","descarregadirecta")

PASSWORD = config.get_setting("password","descarregadirecta")

def isGeneric():
    return True


def mainlist(item):
    logger.info("[descarregadirecta.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=__channel__ , action="Generico"        , title="Anime"                      , url="http://www.descarregadirecta.com/browse-anime-videos-1-date.html"))
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
    logger.info("[descarregadirecta.py] Anime")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '<h4>Categoria relacionada</h4>(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = match2[0]
            scrapedtitle =match2[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="buscavideos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist

def buscavideos(item):
    logger.info("[descarregadirecta.py] BuscaVideos")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    

    patron = '<div class="video_i">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '<a href="(.*?)".*?title="(.*?)".*?'
        patron  += '<img src="(.*?)".*?>'
        #patron  += '<span class="titulotool"><strong>(.*?)</strong></span> <strong>(.*?)</strong>.*?'
        #patron  += '<span class="pop_desc">.*?<p>(.*?)</p>'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
            scrapedtitle = match2[1]
            scrapedurl = match2[0]
            scrapedthumbnail = match2[2].replace(" ","%20")
            scrapedplot = match2[0]
            
            itemlist.append( Item(channel=item.channel , action="detail"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))
    
    #Extrae la marca de siguiente p�gina
    #<span class='current'>1</span><a href='http://delatv.com/page/2' class='page'>2</a>
    patronvideos  = '<span class="current">[^<]+</span>[^<]*<a.*?href="([^"]+)"' #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)==0:
        patronvideos  = "<span class='current'>[^<]+</span>[^<]*<a.*?href='([^']+)'" #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'""
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Pàgina Següent"
        scrapedurl = urlparse.urljoin(url,matches[0])#matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel , action="buscavideos"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

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

    itemlist.append( Item(channel=__channel__, title="Sessió iniciada", action="mainlist"))

    return itemlist

def perform_login(login,password):
    
    logger.info("[Descarregadirecta.py] performlogin")

    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias

    login = login.replace("@","%40")

    data = scrapertools.cache_page("http://www.descarregadirecta.com/login.php",post="username=%s&pass=%s&remember=%s&ref=&Login=%s" % (login,password,"1","Iniciar+Sessi%C3%B3"))
    
    