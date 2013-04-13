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
            #item.url = "http://www.mega-spain.com/index.php"
            #return foro(item)
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
    patron = '<div class="inner" id="msg_.*?<img src="([^"]+)" alt="" class="bbc_img" /><br />(.*?)href="https://mega.co.nz(.*?)" class="bbc_link" '
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedthumbnail, scrapedplot, scrapedurl in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        scrapedurl = "https://mega.co.nz"+scrapedurl
        scrapedurl =            scrapedurl.replace("https://mega.co.nz/#!","http://megastreamer.net/mega_stream.php?url=https%3A%2F%2Fmega.co.nz%2F%23%21")
        scrapedurl = scrapedurl.replace("!","%21")
        scrapedurl=scrapedurl+"&mime=vnd.divx"
        thumbnail = scrapedthumbnail
        title = "Si el archivo es compatible con el reproductor de XBMC comenzará la reproducción de " + "'" + item.title + "'"
        scrapedplot = scrapedplot.replace("<br />","\n")
        scrapedplot = scrapedplot.replace("&nbsp; &nbsp;","")
        scrapedplot = scrapedplot.replace("&nbsp;"," ")
        scrapedplot = scrapedplot.replace("Ver trailer externo","")
        scrapedplot = scrapedplot.replace("Trailers/Vídeos","")
        scrapedplot = scrapertools.htmlclean(scrapedplot)
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        plot = scrapedplot
        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=scrapedurl , thumbnail=thumbnail , plot=plot , folder=True) )
        
    return itemlist
    
    