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


__channel__ = "gnula"
__category__ = "F"
__type__ = "generic"
__title__ = "Gnula"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"            , action="scrapping"   , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="A-Z"                  , action="menupelisaz"))
    itemlist.append( Item(channel=__channel__, title="Años"                  , action="menupelisanos"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

def menupelisaz(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="A"        , action="scrapping"   , url="http://gnula.biz/letra/a/"))
    itemlist.append( Item(channel=__channel__, title="B"        , action="scrapping"   , url="http://gnula.biz/letra/b/"))
    itemlist.append( Item(channel=__channel__, title="C"        , action="scrapping"   , url="http://gnula.biz/letra/c/"))
    itemlist.append( Item(channel=__channel__, title="D"        , action="scrapping"   , url="http://gnula.biz/letra/d/"))
    itemlist.append( Item(channel=__channel__, title="E"        , action="scrapping"   , url="http://gnula.biz/letra/e/"))
    itemlist.append( Item(channel=__channel__, title="F"        , action="scrapping"   , url="http://gnula.biz/letra/f/"))
    itemlist.append( Item(channel=__channel__, title="G"        , action="scrapping"   , url="http://gnula.biz/letra/g/"))
    itemlist.append( Item(channel=__channel__, title="H"        , action="scrapping"   , url="http://gnula.biz/letra/h/"))
    itemlist.append( Item(channel=__channel__, title="I"        , action="scrapping"   , url="http://gnula.biz/letra/i/"))
    itemlist.append( Item(channel=__channel__, title="J"        , action="scrapping"   , url="http://gnula.biz/letra/j/"))
    itemlist.append( Item(channel=__channel__, title="K"        , action="scrapping"   , url="http://gnula.biz/letra/k/"))
    itemlist.append( Item(channel=__channel__, title="L"        , action="scrapping"   , url="http://gnula.biz/letra/l/"))
    itemlist.append( Item(channel=__channel__, title="M"        , action="scrapping"   , url="http://gnula.biz/letra/m/"))
    itemlist.append( Item(channel=__channel__, title="N"        , action="scrapping"   , url="http://gnula.biz/letra/n/"))
    itemlist.append( Item(channel=__channel__, title="O"        , action="scrapping"   , url="http://gnula.biz/letra/o/"))
    itemlist.append( Item(channel=__channel__, title="P"        , action="scrapping"   , url="http://gnula.biz/letra/p/"))
    itemlist.append( Item(channel=__channel__, title="Q"        , action="scrapping"   , url="http://gnula.biz/letra/q/"))
    itemlist.append( Item(channel=__channel__, title="R"        , action="scrapping"   , url="http://gnula.biz/letra/r/"))
    itemlist.append( Item(channel=__channel__, title="S"        , action="scrapping"   , url="http://gnula.biz/letra/s/"))
    itemlist.append( Item(channel=__channel__, title="T"        , action="scrapping"   , url="http://gnula.biz/letra/t/"))
    itemlist.append( Item(channel=__channel__, title="U"        , action="scrapping"   , url="http://gnula.biz/letra/u/"))
    itemlist.append( Item(channel=__channel__, title="V"        , action="scrapping"   , url="http://gnula.biz/letra/v/"))
    itemlist.append( Item(channel=__channel__, title="W"        , action="scrapping"   , url="http://gnula.biz/letra/w/"))
    itemlist.append( Item(channel=__channel__, title="X"        , action="scrapping"   , url="http://gnula.biz/letra/x/"))
    itemlist.append( Item(channel=__channel__, title="Y"        , action="scrapping"   , url="http://gnula.biz/letra/y/"))
    itemlist.append( Item(channel=__channel__, title="Z"        , action="scrapping"   , url="http://gnula.biz/letra/z/"))
    return itemlist

def menupelisanos(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="1921"        , action="scrapping"   , url="http://gnula.biz/ano/1921/"))
    itemlist.append( Item(channel=__channel__, title="1922"        , action="scrapping"   , url="http://gnula.biz/ano/1922/"))
    itemlist.append( Item(channel=__channel__, title="1923"        , action="scrapping"   , url="http://gnula.biz/ano/1923/"))
    itemlist.append( Item(channel=__channel__, title="1924"        , action="scrapping"   , url="http://gnula.biz/ano/1924/"))
    itemlist.append( Item(channel=__channel__, title="1925"        , action="scrapping"   , url="http://gnula.biz/ano/1925/"))
    itemlist.append( Item(channel=__channel__, title="1926"        , action="scrapping"   , url="http://gnula.biz/ano/1926/"))
    itemlist.append( Item(channel=__channel__, title="1927"        , action="scrapping"   , url="http://gnula.biz/ano/1927/"))
    itemlist.append( Item(channel=__channel__, title="1928"        , action="scrapping"   , url="http://gnula.biz/ano/1928/"))
    itemlist.append( Item(channel=__channel__, title="1929"        , action="scrapping"   , url="http://gnula.biz/ano/1929/"))
    itemlist.append( Item(channel=__channel__, title="1930"        , action="scrapping"   , url="http://gnula.biz/ano/1930/"))
    itemlist.append( Item(channel=__channel__, title="1931"        , action="scrapping"   , url="http://gnula.biz/ano/1931/"))
    itemlist.append( Item(channel=__channel__, title="1932"        , action="scrapping"   , url="http://gnula.biz/ano/1932/"))
    itemlist.append( Item(channel=__channel__, title="1933"        , action="scrapping"   , url="http://gnula.biz/ano/1933/"))
    itemlist.append( Item(channel=__channel__, title="1934"        , action="scrapping"   , url="http://gnula.biz/ano/1934/"))
    itemlist.append( Item(channel=__channel__, title="1935"        , action="scrapping"   , url="http://gnula.biz/ano/1935/"))
    itemlist.append( Item(channel=__channel__, title="1936"        , action="scrapping"   , url="http://gnula.biz/ano/1936/"))
    itemlist.append( Item(channel=__channel__, title="1937"        , action="scrapping"   , url="http://gnula.biz/ano/1937/"))
    itemlist.append( Item(channel=__channel__, title="1938"        , action="scrapping"   , url="http://gnula.biz/ano/1938/"))
    itemlist.append( Item(channel=__channel__, title="1939"        , action="scrapping"   , url="http://gnula.biz/ano/1939/"))
    itemlist.append( Item(channel=__channel__, title="1940"        , action="scrapping"   , url="http://gnula.biz/ano/1940/"))
    itemlist.append( Item(channel=__channel__, title="1941"        , action="scrapping"   , url="http://gnula.biz/ano/1941/"))
    itemlist.append( Item(channel=__channel__, title="1942"        , action="scrapping"   , url="http://gnula.biz/ano/1942/"))
    itemlist.append( Item(channel=__channel__, title="1943"        , action="scrapping"   , url="http://gnula.biz/ano/1943/"))
    itemlist.append( Item(channel=__channel__, title="1944"        , action="scrapping"   , url="http://gnula.biz/ano/1944/"))
    itemlist.append( Item(channel=__channel__, title="1945"        , action="scrapping"   , url="http://gnula.biz/ano/1945/"))
    itemlist.append( Item(channel=__channel__, title="1946"        , action="scrapping"   , url="http://gnula.biz/ano/1946/"))
    itemlist.append( Item(channel=__channel__, title="1947"        , action="scrapping"   , url="http://gnula.biz/ano/1947/"))
    itemlist.append( Item(channel=__channel__, title="1948"        , action="scrapping"   , url="http://gnula.biz/ano/1948/"))
    itemlist.append( Item(channel=__channel__, title="1949"        , action="scrapping"   , url="http://gnula.biz/ano/1949/"))
    itemlist.append( Item(channel=__channel__, title="1950"        , action="scrapping"   , url="http://gnula.biz/ano/1950/"))
    itemlist.append( Item(channel=__channel__, title="1951"        , action="scrapping"   , url="http://gnula.biz/ano/1951/"))
    itemlist.append( Item(channel=__channel__, title="1952"        , action="scrapping"   , url="http://gnula.biz/ano/1952/"))
    itemlist.append( Item(channel=__channel__, title="1953"        , action="scrapping"   , url="http://gnula.biz/ano/1953/"))
    itemlist.append( Item(channel=__channel__, title="1954"        , action="scrapping"   , url="http://gnula.biz/ano/1954/"))
    itemlist.append( Item(channel=__channel__, title="1955"        , action="scrapping"   , url="http://gnula.biz/ano/1955/"))
    itemlist.append( Item(channel=__channel__, title="1956"        , action="scrapping"   , url="http://gnula.biz/ano/1956/"))
    itemlist.append( Item(channel=__channel__, title="1957"        , action="scrapping"   , url="http://gnula.biz/ano/1957/"))
    itemlist.append( Item(channel=__channel__, title="1958"        , action="scrapping"   , url="http://gnula.biz/ano/1958/"))
    itemlist.append( Item(channel=__channel__, title="1959"        , action="scrapping"   , url="http://gnula.biz/ano/1959/"))
    itemlist.append( Item(channel=__channel__, title="1960"        , action="scrapping"   , url="http://gnula.biz/ano/1960/"))
    itemlist.append( Item(channel=__channel__, title="1961"        , action="scrapping"   , url="http://gnula.biz/ano/1961/"))
    itemlist.append( Item(channel=__channel__, title="1962"        , action="scrapping"   , url="http://gnula.biz/ano/1962/"))
    itemlist.append( Item(channel=__channel__, title="1963"        , action="scrapping"   , url="http://gnula.biz/ano/1963/"))
    itemlist.append( Item(channel=__channel__, title="1964"        , action="scrapping"   , url="http://gnula.biz/ano/1964/"))
    itemlist.append( Item(channel=__channel__, title="1965"        , action="scrapping"   , url="http://gnula.biz/ano/1965/"))
    itemlist.append( Item(channel=__channel__, title="1966"        , action="scrapping"   , url="http://gnula.biz/ano/1966/"))
    itemlist.append( Item(channel=__channel__, title="1967"        , action="scrapping"   , url="http://gnula.biz/ano/1967/"))
    itemlist.append( Item(channel=__channel__, title="1968"        , action="scrapping"   , url="http://gnula.biz/ano/1968/"))
    itemlist.append( Item(channel=__channel__, title="1969"        , action="scrapping"   , url="http://gnula.biz/ano/1969/"))
    itemlist.append( Item(channel=__channel__, title="1970"        , action="scrapping"   , url="http://gnula.biz/ano/1970/"))
    itemlist.append( Item(channel=__channel__, title="1971"        , action="scrapping"   , url="http://gnula.biz/ano/1971/"))
    itemlist.append( Item(channel=__channel__, title="1972"        , action="scrapping"   , url="http://gnula.biz/ano/1972/"))
    itemlist.append( Item(channel=__channel__, title="1973"        , action="scrapping"   , url="http://gnula.biz/ano/1973/"))
    itemlist.append( Item(channel=__channel__, title="1974"        , action="scrapping"   , url="http://gnula.biz/ano/1974/"))
    itemlist.append( Item(channel=__channel__, title="1975"        , action="scrapping"   , url="http://gnula.biz/ano/1975/"))
    itemlist.append( Item(channel=__channel__, title="1976"        , action="scrapping"   , url="http://gnula.biz/ano/1976/"))
    itemlist.append( Item(channel=__channel__, title="1977"        , action="scrapping"   , url="http://gnula.biz/ano/1977/"))
    itemlist.append( Item(channel=__channel__, title="1978"        , action="scrapping"   , url="http://gnula.biz/ano/1978/"))
    itemlist.append( Item(channel=__channel__, title="1979"        , action="scrapping"   , url="http://gnula.biz/ano/1979/"))
    itemlist.append( Item(channel=__channel__, title="1980"        , action="scrapping"   , url="http://gnula.biz/ano/1980/"))
    itemlist.append( Item(channel=__channel__, title="1981"        , action="scrapping"   , url="http://gnula.biz/ano/1981/"))
    itemlist.append( Item(channel=__channel__, title="1982"        , action="scrapping"   , url="http://gnula.biz/ano/1982/"))
    itemlist.append( Item(channel=__channel__, title="1983"        , action="scrapping"   , url="http://gnula.biz/ano/1983/"))
    itemlist.append( Item(channel=__channel__, title="1984"        , action="scrapping"   , url="http://gnula.biz/ano/1984/"))
    itemlist.append( Item(channel=__channel__, title="1985"        , action="scrapping"   , url="http://gnula.biz/ano/1985/"))
    itemlist.append( Item(channel=__channel__, title="1986"        , action="scrapping"   , url="http://gnula.biz/ano/1986/"))
    itemlist.append( Item(channel=__channel__, title="1987"        , action="scrapping"   , url="http://gnula.biz/ano/1987/"))
    itemlist.append( Item(channel=__channel__, title="1988"        , action="scrapping"   , url="http://gnula.biz/ano/1988/"))
    itemlist.append( Item(channel=__channel__, title="1989"        , action="scrapping"   , url="http://gnula.biz/ano/1989/"))
    itemlist.append( Item(channel=__channel__, title="1990"        , action="scrapping"   , url="http://gnula.biz/ano/1990/"))
    itemlist.append( Item(channel=__channel__, title="1991"        , action="scrapping"   , url="http://gnula.biz/ano/1991/"))
    itemlist.append( Item(channel=__channel__, title="1992"        , action="scrapping"   , url="http://gnula.biz/ano/1992/"))
    itemlist.append( Item(channel=__channel__, title="1993"        , action="scrapping"   , url="http://gnula.biz/ano/1993/"))
    itemlist.append( Item(channel=__channel__, title="1994"        , action="scrapping"   , url="http://gnula.biz/ano/1994/"))
    itemlist.append( Item(channel=__channel__, title="1995"        , action="scrapping"   , url="http://gnula.biz/ano/1995/"))
    itemlist.append( Item(channel=__channel__, title="1996"        , action="scrapping"   , url="http://gnula.biz/ano/1996/"))
    itemlist.append( Item(channel=__channel__, title="1997"        , action="scrapping"   , url="http://gnula.biz/ano/1997/"))
    itemlist.append( Item(channel=__channel__, title="1998"        , action="scrapping"   , url="http://gnula.biz/ano/1998/"))
    itemlist.append( Item(channel=__channel__, title="1999"        , action="scrapping"   , url="http://gnula.biz/ano/1999/"))
    itemlist.append( Item(channel=__channel__, title="2000"        , action="scrapping"   , url="http://gnula.biz/ano/2000/"))
    itemlist.append( Item(channel=__channel__, title="2001"        , action="scrapping"   , url="http://gnula.biz/ano/2001/"))
    itemlist.append( Item(channel=__channel__, title="2002"        , action="scrapping"   , url="http://gnula.biz/ano/2002/"))
    itemlist.append( Item(channel=__channel__, title="2003"        , action="scrapping"   , url="http://gnula.biz/ano/2003/"))
    itemlist.append( Item(channel=__channel__, title="2004"        , action="scrapping"   , url="http://gnula.biz/ano/2004/"))
    itemlist.append( Item(channel=__channel__, title="2005"        , action="scrapping"   , url="http://gnula.biz/ano/2005/"))
    itemlist.append( Item(channel=__channel__, title="2006"        , action="scrapping"   , url="http://gnula.biz/ano/2006/"))
    itemlist.append( Item(channel=__channel__, title="2007"        , action="scrapping"   , url="http://gnula.biz/ano/2007/"))
    itemlist.append( Item(channel=__channel__, title="2008"        , action="scrapping"   , url="http://gnula.biz/ano/2008/"))
    itemlist.append( Item(channel=__channel__, title="2009"        , action="scrapping"   , url="http://gnula.biz/ano/2009/"))
    itemlist.append( Item(channel=__channel__, title="2010"        , action="scrapping"   , url="http://gnula.biz/ano/2010/"))
    itemlist.append( Item(channel=__channel__, title="2011"        , action="scrapping"   , url="http://gnula.biz/ano/2011/"))
    itemlist.append( Item(channel=__channel__, title="2012"        , action="scrapping"   , url="http://gnula.biz/ano/2012/"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[gnula.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://gnula.biz/buscar.php?q=%s"
        item.url = item.url % texto
        itemlist.extend(scrapping(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def scrapping(item,paginacion=True):
    logger.info("[gnula.py] scrapping")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a id="darze" href="([^"]+)">[^<]+<span[^>]+>[^<]+<div[^>]+>[^<]+<img class="[^"]+" name="[^"]+" src="([^"]+)"[^>]+>[^<]+<canvas[^>]+></canvas>[^<]+</div>[^<]+</span>[^<]+<span class="tit">([^<]+)</span>[^<]+</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[2]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",match[0])
        scrapedthumbnail = match[1]
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = scrapping(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien