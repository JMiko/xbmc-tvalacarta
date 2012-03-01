# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurweb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "shurhd"
__category__ = "F"
__type__ = "generic"
__title__ = "Shurhd"
__language__ = "ES"

DEBUG = config.get_setting("debug")
SESION = config.get_setting("session","shurhd")
LOGIN = config.get_setting("login","shurhd")
PASSWORD = config.get_setting("password","shurhd")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[shurweb.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"                , action="scrapping"   , url="http://www.shurhd.com/"))
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas"))
#    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    if SESION=="true":
        perform_login(LOGIN,PASSWORD)
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login"))

    return itemlist

def perform_login(login,password):
    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias
    url="http://www.shurhd.com/wp-login.php"
    data = scrapertools.cache_page(url,post="log="+LOGIN+"&pwd="+PASSWORD+"&rememberme=forever&wp-submit=Acceder&redirect_to=http%3A%2F%2Fwww.shurhd.com%2Fwp-admin%2F&testcookie=1")

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    if config.get_platform() in ("wiimc", "rss"):
        if LOGIN<>"" and PASSWORD<>"":
            perform_login(LOGIN,PASSWORD)
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

        if LOGIN<>"" and PASSWORD<>"":
            perform_login(LOGIN,PASSWORD)
            itemlist = []
            itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))

    return itemlist


def menupeliculas(item):
    logger.info("[shurweb.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - HD"        , action="scrapping"   , url="http://www.shurhd.com/category/hd/") )
    itemlist.append( Item(channel=__channel__, title="Películas - DVD"        , action="scrapping"   , url="http://www.shurhd.com/category/otras-calidades/") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[shurweb.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.shurweb.es/?s=%s"
        item.url = item.url % texto
        itemlist.extend(scrappingSearch(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def scrappingSearch(item,paginacion=True):
    logger.info("[shurweb.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">([^#]+)#888"><b>([^<]+)</b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        if match[5] == 'Peliculas' or match[5] == 'Series':
            scrapedtitle =  match[2]
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            scrapedplot = ""
            scrapedurl = match[3]
            scrapedthumbnail = match[1]
            if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    return itemlist

def scrapping(item,paginacion=True):
    logger.info("[shurweb.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+><div src="" class="kucukIcon"></div></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[1]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    patronvideos  = '<li><a class="next page-numbers" href="([^"]+)">[^<]+</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = matches[0]
        pagitem = Item(channel=__channel__, action="scrapping", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( scrapping(pagitem) )
        else:
            itemlist.append( pagitem )
    return itemlist

def findvideos(item):
    logger.info("[shurweb.py] findvideos")
    try:
        url = item.url
        fulltitle = item.fulltitle
        extra = item.extra
        plot = item.plot
        data = scrapertools.cachePage(url)
        patronvideos = '<iframe src="(http://([^/]+)([^"]+))"[^w]+width=[^>]+></iframe>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        itemlist = []
        for match in matches:
            scrapedtitle = match[1]
            scrapedtitle = scrapertools.htmlclean(scrapedtitle)
            scrapedurl = match[0]
            server = match[1]
            if "vk" in server:
            	server = "vk"
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl, thumbnail=item.thumbnail, plot=plot, server=server, extra=extra, category=item.category, fanart=item.thumbnail, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    menupeliculas_items = menupeliculas(mainlist_items[0])
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(menupeliculas_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien