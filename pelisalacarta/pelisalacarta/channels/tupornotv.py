# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tupornotv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from servers import servertools
#from platformcode.xbmc import xbmctools
from core import config
from core.item import Item
from core import logger
#from pelisalacarta import buscador

from core import scrapertools

__channel__ = "tupornotv"
__category__ = "F"
__type__ = "generic"
__title__ = "tuporno.tv"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tupornotv.py] mainlist")
    
    itemlist = []
    itemlist.append( Item( channel=__channel__ , title="Pendientes de Votación" , action="novedades" , url="http://tuporno.tv/pendientes") )
    itemlist.append( Item( channel=__channel__ , title="Populares" , action="masVistos" , url="http://tuporno.tv/" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Categorias" , action="categorias" , url="http://tuporno.tv/categorias/" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Videos Recientes" , action="novedades" , url="http://tuporno.tv/videosRecientes/" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Top Videos (mas votados)" , action="masVotados" , url="http://tuporno.tv/topVideos/" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Nube de Tags" , action="categorias" , url="http://tuporno.tv/tags/" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Buscar" , action="search") )
    
    return itemlist

def novedades(item):
    logger.info("[tupornotv.py] novedades")
    url = item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    # seccion novedades
    '''
    <table border="0" cellpadding="0" cellspacing="0" ><tr><td align="center" width="100%" valign="top" height="160px">
    <a href="/videos/cogiendo-en-el-bosque"><img src="imagenes/videos//c/o/cogiendo-en-el-bosque_imagen2.jpg" alt="Cogiendo en el bosque" border="0" align="top" /></a>
    <h2><a href="/videos/cogiendo-en-el-bosque">Cogiendo en el bosque</a></h2>
    '''
    patronvideos  = '(?:<table border="0" cellpadding="0" cellspacing="0" ><tr><td align="center" width="100." valign="top" height="160px">|<td align="center" valign="top" width="25%">)[^<]+'
    patronvideos += '<a href="(.videos[^"]+)"><img src="([^"]+)" alt="([^"]+)"(.*?)</td>'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        # Titulo
        scrapedtitle = match[2]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        try:
            duracion = re.compile('n: (.+?)</span>').findall(match[3])[0]
        except:
            try:
                duracion = re.compile('\((.+?)\)<br').findall(match[3])[0]
            except:
                duracion = ""
             
        #logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], duracion=["+duracion+"]")
        # Añade al listado de XBMC
        trozos = scrapedurl.split("/")
        id = trozos[len(trozos)-1]
        videos = "http://149.12.64.129/videoscodiH264/"+id[0:1]+"/"+id[1:2]+"/"+id+".flv"
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle+" ["+duracion+"]" , url=videos , thumbnail=scrapedthumbnail , plot=scrapedplot, server="Directo", folder=False) )

    # ------------------------------------------------------
    # Extrae el paginador
    # ------------------------------------------------------
    #<a href="/topVideos/todas/mes/2/" class="enlace_si">Siguiente </a>
    patronsiguiente = '<a href="([^"]+)" class="enlace_si">Siguiente </a>'
    siguiente = re.compile(patronsiguiente,re.DOTALL).findall(data)
    if len(siguiente)>0:
        patronultima = '<!--HV_SIGUIENTE_ENLACE'
        ultpagina = re.compile(patronultima,re.DOTALL).findall(data)
        scrapertools.printMatches(siguiente)
    
        if len(ultpagina)>0:
            scrapedurl = urlparse.urljoin(url,siguiente[0])
            itemlist.append( Item(channel=__channel__, action="novedades", title="!Next page" , url=scrapedurl , folder=True) )

    return itemlist

def masVistos(item):
    logger.info("[tupornotv.py] masVistos")
    
    itemlist = []
    itemlist.append( Item( channel=__channel__ , title="Hoy" , action="novedades" , url="http://tuporno.tv/hoy" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Recientes" , action="novedades" , url="http://tuporno.tv/recientes" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Semana" , action="novedades" , url="http://tuporno.tv/semana" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Mes" , action="novedades" , url="http://tuporno.tv/mes" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Año" , action="novedades" , url="http://tuporno.tv/ano" , folder=True ) )
    return itemlist

def categorias(item):
    logger.info("[tupornotv.py] categorias")
    
    
    url=item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    # seccion categorias
    # Patron de las entradas
    if url == "http://tuporno.tv/categorias/":
        patronvideos  = '<li><a href="([^"]+)"'      # URL
        patronvideos += '>([^<]+)</a></li>'          # TITULO
    else:
        patronvideos  = '<a href="(.tags[^"]+)"'     # URL
        patronvideos += ' class="[^"]+">([^<]+)</a>'    # TITULO
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        if match[1] in ["SexShop","Videochat","Videoclub"]:
            continue
        # Titulo
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle.capitalize() , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist

def masVotados(item):
    logger.info("[tupornotv.py] masVotados")
    
    itemlist = []
    itemlist.append( Item( channel=__channel__ , title="Hoy" , action="novedades" , url="http://tuporno.tv/topVideos/todas/hoy" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Recientes" , action="novedades" , url="http://tuporno.tv/topVideos/todas/recientes" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Semana" , action="novedades" , url="http://tuporno.tv/topVideos/todas/semana" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Mes" , action="novedades" , url="http://tuporno.tv/topVideos/todas/mes" , folder=True ) )
    itemlist.append( Item( channel=__channel__ , title="Año" , action="novedades" , url="http://tuporno.tv/topVideos/todas/ano" , folder=True ) )
    return itemlist

def search(item):
    logger.info("[tupornotv.py] search")
    tecleado = item.extra.replace(" ", "+")
    item.url = "http://tuporno.tv/buscador/?str=" + tecleado
    itemlist = getsearch(item)
    return itemlist
   
def getsearch(item):
    logger.info("[tupornotv.py] getsearch")
    data = scrapertools.cachePage(item.url)
    patronvideos  = '<td align="left"><a href="(.videos[^"]+)"><img src="([^"]+)" alt="(.+?)" (.*?)<span class="tmp">(.+?)</span></h2>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        itemlist = []
        for match in matches:
            # Titulo
            scrapedtitle = match[2].replace("<b>","")
            scrapedtitle = scrapedtitle.replace("</b>","")
            scrapedurl = urlparse.urljoin("http://tuporno.tv/",match[0])
            scrapedthumbnail = urlparse.urljoin("http://tuporno.tv/",match[1])
            scrapedplot = ""
            duracion = match[4]
            trozos = scrapedurl.split("/")
            id = trozos[len(trozos)-1]
            videos = "http://149.12.64.129/videoscodiH264/"+id[0:1]+"/"+id[1:2]+"/"+id+".flv"
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle+" ["+duracion+"]" , url=videos , thumbnail=scrapedthumbnail , plot=scrapedplot, server="Directo", folder=False) )
    
        '''<a href="/buscador/?str=busqueda&desde=HV_PAGINA_SIGUIENTE" class="enlace_si">Siguiente </a>'''
        patronsiguiente = '<a href="([^"]+)" class="enlace_si">Siguiente </a>'
        siguiente = re.compile(patronsiguiente,re.DOTALL).findall(data)
        if len(siguiente)>0:
            patronultima = '<!--HV_SIGUIENTE_ENLACE'
            ultpagina = re.compile(patronultima,re.DOTALL).findall(data)
            scrapertools.printMatches(siguiente)
    
            if len(ultpagina)==0:
                scrapedurl = urlparse.urljoin(item.url,siguiente[0])
                itemlist.append( Item(channel=__channel__, action="getsearch", title="!Next page" , url=scrapedurl , folder=True) )
        
    return itemlist
