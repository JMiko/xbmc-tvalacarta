# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "cinegratis"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinegratis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title="Películas - Novedades"            , url="http://www.cinegratis.net/index.php?module=peliculas"))
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title="Películas - Estrenos"             , url="http://www.cinegratis.net/index.php?module=estrenos"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliscat"   , title="Películas - Lista por categorías" , url="http://www.cinegratis.net/index.php?module=generos"))
    itemlist.append( Item(channel=CHANNELNAME, action="pelisalfa"  , title="Películas - Lista alfabética"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseries" , title="Series - Novedades"               , url="http://www.cinegratis.net/index.php?module=series"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple" , title="Series - Todas"                   , url="http://www.cinegratis.net/index.php?module=serieslist"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseries" , title="Dibujos - Novedades"              , url="http://www.cinegratis.net/index.php?module=anime"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple" , title="Dibujos - Todos"                  , url="http://www.cinegratis.net/index.php?module=animelist"))
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title="Documentales - Novedades"         , url="http://www.cinegratis.net/index.php?module=documentales"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple" , title="Documentales - Todos"             , url="http://www.cinegratis.net/index.php?module=documentaleslist"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"     , title="Buscar"                           , url="http://www.cinegratis.net/index.php?module=search&title=%s"))

    return itemlist

def pelisalfa(item):
    logger.info("[cinegratis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="0-9", url="http://www.cinegratis.net/index.php?module=peliculaslist&init="))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="A", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=a"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="B", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=b"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="C", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=c"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="D", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=d"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="E", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=e"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="F", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=f"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="G", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=g"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="H", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=h"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="I", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=i"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="J", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=j"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="K", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=k"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="L", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=l"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="M", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=m"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="N", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=n"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="O", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=o"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="P", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=p"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="Q", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=q"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="R", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=r"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="S", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=s"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="T", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=t"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="U", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=u"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="V", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=v"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="W", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=w"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="X", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=x"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="Y", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=y"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple", title="Z", url="http://www.cinegratis.net/index.php?module=peliculaslist&init=z"))

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto, categoria="*"):
    logger.info("[cinegratis.py] search")

    texto = texto.replace(" ", "+")
    itemlist = []
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            if categoria in ("*","F"):
                item.url = "http://www.cinegratis.net/index.php?module=search&title="+texto
                itemlist.extend(listsimple(item)) 
            if categoria in ("*","D"):
                item.url = "http://www.cinegratis.net/index.php?hstitle="+texto+"&hscat=Documentales&hsyear"
                itemlist.extend(listsimple_documentales(item))
        else:
            item.url = item.url % texto
            itemlist.extend(listsimple(item))
              
        return itemlist
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def peliscat(item):
    logger.info("[cinegratis.py] peliscat")

    url = item.url

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple" , title="Versión original" , url="http://www.cinegratis.net/index.php?module=search&title=subtitulado"))
    itemlist.append( Item(channel=CHANNELNAME, action="listsimple" , title="Versión latina"   , url="http://www.cinegratis.net/index.php?module=search&title=latino"))

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<td align='left'><a href='([^']+)'><img src='([^']+)' border='0'></a></td>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        patron2 = "genero/([A-Za-z\-]+)/"
        matches2 = re.compile(patron2,re.DOTALL).findall(match[0])
        scrapertools.printMatches(matches2)
        
        scrapedtitle = matches2[0]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listsimple(item):
    logger.info("[cinegratis.py] listsimple")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<a href='(index.php\?module\=player[^']+)'[^>]*>(.*?)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listvideos(item):
    logger.info("[cinegratis.py] listvideos")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae los items
    patronvideos  = "<table.*?<td.*?>([^<]+)<span class='style1'>\(Visto.*?"
    patronvideos += "<div align='justify'>(.*?)</div>.*?"
    patronvideos += "<a href='(.*?)'.*?"
    patronvideos += "<img src='(.*?)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[0]
        if url.startswith('http://www.cinegratis.net/genero'):
            url="http://www.cinegratis.net/"
        scrapedurl = urlparse.urljoin(url,match[2])
        scrapedthumbnail = urlparse.urljoin(url,match[3])
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la marca de siguiente página
    patronvideos  = "<a href='[^']+'><u>[^<]+</u></a> <a href='([^']+)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listseries(item):
    logger.info("[cinegratis.py] listvideos")

    url = item.url
    
    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae los items
    patronvideos  = "<table width='785'[^>]+><tr><td[^>]+>([^<]+)<.*?"
    patronvideos += "<div align='justify'>(.*?)</div>.*?"
    patronvideos += "<a href='(.*?)'.*?"
    patronvideos += "<img src='(.*?)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = urlparse.urljoin(url,match[2])
        scrapedthumbnail = urlparse.urljoin(url,match[3])
        scrapedplot = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Extrae la marca de siguiente página
    patronvideos  = "<a href='[^']+'><u>[^<]+</u></a> <a href='([^']+)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="listseries" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist
    

def listsimple_documentales(item):
    logger.info("[cinegratis.py] listsimple_documentales")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    '''
<table cellspacing='1' cellpadding='0' class='style3'>
<tr class='style4'><td>T�tulo</td><td width='10'></td><td>G�nero</td></tr>
<tr><td height='5'></td></tr>
<tr><td><a href='/pelicula/Abusos sexuales y el Vaticano/455'>Abusos sexuales y el Vaticano</td><td width='10'></td><td>Documentales</td></tr>
<tr><td><a href='/pelicula/Abusos sexuales y el Vaticano (Documental)/7320'>Abusos sexuales y el Vaticano (Documental)</td><td width='10'></td><td>Documentales</td></tr>
</table></td></tr></table></td></tr></table>
    '''
    # Extrae los items
    patronvideos  = "<tr><td><a href='([^']+)'>([^<]+)</td>"   
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin("http://www.cinegratis.net",match[0]).replace(" ","+")
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def findvideos(item):
    logger.info("[cinegratis.py] findvideos")

    from core import scrapertools
    data = scrapertools.cache_page(item.url)    
    patronvideos = "<td width='100\%' align='justify' valign='top' class='style3'>(.+?)<br>\s*?<center>\s*?<br><br>\s*?\s*?<style>.+?(http://www\.stage54\.net/cgimages/caratulas/.+?jpg)" # plot
    matches = re.compile(patronvideos,re.S).findall(data)
    if len(matches)>0: 
        item.plot = matches[0][0]
        item.thumbnail = matches[0][1]

    from servers import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]
        itemlist.append( Item(channel=channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, fulltitle=item.fulltitle, folder=False))

    return itemlist

    

