# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para megahd
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

__channel__ = "megahd"
__category__ = "F"
__type__ = "generic"
__title__ = "Megahd"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

MAIN_HEADERS = []
MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Encoding","gzip, deflate"] )
MAIN_HEADERS.append( ["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )
MAIN_HEADERS.append( ["DNT","1"] )
MAIN_HEADERS.append( ["Host","megahd.se"] )
MAIN_HEADERS.append( ["Referer","http://megahd.se/foro/login/"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Windows NT 5.1; rv:19.0) Gecko/20100101 Firefox/19.0"] )
MAIN_HEADERS.append( ["Accept-Charset","ISO-8859-1"] )

def isGeneric():
    return True

def login():
    logger.info("[megahd.py] login")
    # Calcula el hash del password
    
    LOGIN = config.get_setting("megahduser") 
    PASSWORD = config.get_setting("megahdpassword")
    
    logger.info("LOGIN="+LOGIN)
    logger.info("PASSWORD="+PASSWORD)
    # Hace el submit del login
    post = "user="+LOGIN+"&passwrd="+PASSWORD
    logger.info("post="+post)
    data = scrapertools.cache_page("http://megahd.se/foro/login2/" , post=post, headers=MAIN_HEADERS)
    return True

def mainlist(item):
    logger.info("[megahd.py] mainlist")
    itemlist = []
    
    
    
    if config.get_setting("megahdaccount")!="true":
    
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="" , url="" , folder=False ) )
    else:
        if login():
            itemlist.append( Item( channel=__channel__ , title="Películas" , action="foro" , url="http://megahd.se/foro/peliculas/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Anime" , action="foro" , url="http://megahd.se/foro/anime/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Series" , action="foro" , url="http://megahd.se/foro/series/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Documentales y Deportes" , action="foro" , url="http://megahd.se/foro/documentales/" , folder=True ) )
            itemlist.append( Item( channel=__channel__ , title="Zona Infantil" , action="foro" , url="http://megahd.se/foro/zona-infantil/" , folder=True ) )
        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )
    return itemlist

def foro(item):
    logger.info("[megahd.py] foro")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    if '<h3 class="catbg">Subforos</h3>' in data: # HAY SUBFOROS
        patron = '<a class="subje(.*?)t" href="([^"]+)" name="[^"]+">([^<]+)</a>&nbsp' 
        action = "foro"
    else: # MANDA A SACAR EL LINK DEL VIDEO
        patron = '<td class="subject windowbg2">.*?<div >.*?<span id="([^"]+)"> <a href="([^"]+)".*?>([^<]+)</a> </span>' 
        action = "find_link_mega"
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedmsg, scrapedurl,scrapedtitle in matches:
            scrapedmsg = scrapedmsg.replace("msg_","?action=thankyou;msg=")
            url = urlparse.urljoin(item.url,scrapedurl)
            title = scrapertools.htmlclean(scrapedtitle)
            title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            title = scrapedtitle 
            thumbnail = ""
            plot = url+scrapedmsg
            # Añade al listado
            itemlist.append( Item(channel=__channel__, action=action, title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
            
    
    # EXTRAE EL LINK DE LA SIGUIENTE PAGINA
    patron = '<div class="pagelinks">Páginas:.*?\[<strong>[^<]+</strong>\].*?<a class="navPages" href="(?!\#bot)([^"]+)">[^<]+</a>.*?</div>'
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
    logger.info("[megahd.py] find_link_mega")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    
    if 'http://megahd.se/foro/Themes/inverted/images/hidden.png' in data:
        data = scrapertools.cache_page(item.plot)
        
    else:
        no_thanks = "SI"
    
    
    patronimage = '<div class="inner" id="msg_\d{1,9}".*?<img src="([^"]+)"'
    
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    if len(matches)>0:
        thumbnail = matches[0]
        thumbnail = scrapertools.htmlclean(thumbnail)
        thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = ""
 
    patronplot = '<div class="inner" id="msg_\d{1,9}".*?<img src="[^"]+".*?Reportar Links Rotos'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    if len(matches)>0:
        plot = matches[0]
        
        if '.rar' in data:
            item.title = '¡ ATENCION! Es posible que no se reproduzca "' + item.title + '" ya que el archivo es un rar'
        elif '.zip' in data:
            item.title = '¡ ATENCION! Es posible que no se reproduzca "' + item.title + '" ya que el archivo es un zip'
        else:
            item.title = '"' + item.title + '" se reproducirá si el archivo es compatible con el reproductor de XBMC'
            
        title = item.title 
        #title = "msgt es " + msgt + "---item.plot es: " + item.plot
        
        plot = scrapertools.htmlclean(plot)
        url = ""
  
    patronurl = '>https://mega.co.nz/(.*?)<'
    matches = re.compile(patronurl,re.DOTALL).findall(data)
    for scrapedurl in matches:
        url = scrapedurl
        url = "https://mega.co.nz/" + url
        url = url.replace("https://mega.co.nz/#!","http://megastreamer.net/mega_stream.php?url=https%3A%2F%2Fmega.co.nz%2F%23%21")
        url = url.replace("!","%21")
        url = url + "&mime=vnd.divx"
        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="play", title= title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
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

    