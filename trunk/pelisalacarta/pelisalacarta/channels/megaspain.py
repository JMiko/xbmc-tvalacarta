# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para megaspain
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "megaspain"
__category__ = "F"
__type__ = "generic"
__title__ = "Megaspain"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

MAIN_HEADERS = []

MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Encoding","gzip, deflate"] )
MAIN_HEADERS.append( ["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )
MAIN_HEADERS.append( ["DNT","1"] )
MAIN_HEADERS.append( ["Referer","http://www.mega-spain.com/index.php"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Windows NT 6.2; rv:18.0) Gecko/20100101 Firefox/18.0"] )
MAIN_HEADERS.append( ["Accept-Charset","ISO-8859-1"] )

def isGeneric():
    return True

def login():
    logger.info("[megaspain.py] login")

    # Calcula el hash del password
    LOGIN = config.get_setting("megaspainuser") 
    PASSWORD = config.get_setting("megaspainpassword")
    
    
    logger.info("LOGIN="+LOGIN)
    logger.info("PASSWORD="+PASSWORD)
   
    # Hace el submit del login
    post = "user="+LOGIN+"&passwrd="+PASSWORD
    logger.info("post="+post)
    
    data = scrapertools.cache_page("http://www.mega-spain.com/index.php?action=login2" , post=post, headers=MAIN_HEADERS)

    return True

def mainlist(item):
    logger.info("[megaspain.py] mainlist")
    itemlist = []
    
    if config.get_setting("megaspainaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="" , url="" , folder=False ) )
    else:
        if login():
            itemlist.append( Item( channel=__channel__ , title="Peliculas" , action="foro" , url="http://www.mega-spain.com/index.php/board,1.0.html" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Series" , action="foro" , url="http://www.mega-spain.com/index.php/board,3.0.html" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Documentales" , action="foro" , url="http://www.mega-spain.com/index.php/board,24.0.html" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Series Manga/Anime" , action="foro" , url="http://www.mega-spain.com/index.php/board,63.0.html" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Peliculas Manga/Anime" , action="foro" , url="http://www.mega-spain.com/index.php/board,64.0.html" , folder=True ) )

        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )

    return itemlist


def foro(item):
    logger.info("[megaspain.py] foro")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    if '<h3 class="catbg">Subforos</h3>' in data:
        patron = '<a class="subject" href="([^"]+)" name="[^"]+">([^<]+)</a>' # HAY SUBFOROS
        action = "foro"
    else:
        patron = '<span id="msg_.*?"><a href="([^"]+)">([^<]+)</a> </span>' # MANDA A SACAR EL LINK DEL VIDEO
        action = "find_link_mega"
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle in matches:
            url = urlparse.urljoin(item.url,scrapedurl)
            scrapedtitle = scrapertools.htmlclean(scrapedtitle)
            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            title = scrapedtitle
            thumbnail = ""
            plot = ""
            # Añade al listado
            if action=="foro":
                url = scrapedurl
            itemlist.append( Item(channel=__channel__, action=action, title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    
    
    # EXTREA EL LINK DE LA SIGUIENTE PAGINA
    patron = 'div class="pagelinks floatleft.*?<strong>[^<]+</strong>\] <a class="navPages" href="(?!\#bot)([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            url = match
            title = ">> Página Siguiente"
            thumbnail = ""
            plot = ""
            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="foro", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    return itemlist

    
    
def find_link_mega(item):
    logger.info("[megaspain.py] find_link_mega")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    
    patronimage = '<div class="inner" id="msg_\d{1,9}".*?<img src="([^"]+)"'
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    if len(matches)>0:
        thumbnail = matches[0]
        thumbnail = scrapertools.htmlclean(thumbnail)
        thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = ""
 
    patronplot = '<div class="inner" id="msg_\d{1,9}".*?<img src="[^"]+".*?Reportar al moderador'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    if len(matches)>0:
        plot = matches[0]
        
        if '.rar' in data:
            item.title = "rar Es posible que no se reproduzca " + item.title + " ya que el archivo es un rar"
        
        elif '.zip' in data:
            item.title = "zip Es posible que no se reproduzca " + item.title + " ya que el archivo es un zip"
        else:
            item.title = "'" + item.title + "' se reproducirá si el archivo es compatible con el reproductor de XBMC"
                    
        title = item.title
            
        plot = scrapertools.htmlclean(plot)
        url = ""
  
    patronurl = '>htt[ps]://mega.co.nz/(.*?)[<"]'
    
    matches = re.compile(patronurl,re.DOTALL).findall(data)
    for scrapedurl in matches:
        url = scrapedurl
        url = "https://mega.co.nz/" + url
        url = url.replace("https://mega.co.nz/#!","http://megastreamer.net/mega_stream.php?url=https%3A%2F%2Fmega.co.nz%2F%23%21")
        url = url.replace("!","%21")
        url = url + "&mime=vnd.divx"
        #plot = ""
        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    return itemlist
    
    
    
# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Navega hasta la lista de películas
    mainlist_items = mainlist(Item())
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    
    # Si encuentra algún enlace, lo da por bueno
    for pelicula_item in peliculas_items:
        itemlist = findbitly_link(pelicula_item)
        if not itemlist is None and len(itemlist)>=0:
            return True

    return False

    