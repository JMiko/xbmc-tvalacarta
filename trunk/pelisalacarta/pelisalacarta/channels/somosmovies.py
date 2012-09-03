# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para somosmovies
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "somosmovies"
__category__ = "F,S,D,A"
__type__ = "generic"
__title__ = "Somosmovies"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[somosmovies.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"    , action="listado", url="http://www.somosmovies.com"))
    itemlist.append( Item(channel=__channel__, title="Series"       , action="listado", url="http://www.somosmovies.com/search/label/Series?max-results=12"))
    itemlist.append( Item(channel=__channel__, title="Anime"        , action="listado", url="http://www.somosmovies.com/search/label/Anime?max-results=12"))
    
    return itemlist

def listado(item):
    logger.info("[somosmovies.py] listado")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    # Extrae las entradas
    '''
    <article CLASS='post crp'>
    <header><h3 CLASS='post-title entry-title item_name'>
    <a href='http://www.somosmovies.com/2012/09/blancanieves-y-el-cazador-2012.html' title='Blancanieves y el Cazador (2012)'>Blancanieves y el Cazador (2012)</a>
    </h3>
    </header>
    <section CLASS='post-body entry-content clearfix'>
    <a href='http://www.somosmovies.com/2012/09/blancanieves-y-el-cazador-2012.html' title='Blancanieves y el Cazador (2012)'><center><img border="0" src="http://4.bp.blogspot.com/-IGXqSKwmBnA/UEJzNarqbsI/AAAAAAAABfM/JZHRa09aJDo/s1600/poster.jpg" style="display: block; height: 400px; width: 316;"></center></a>
    <div CLASS='latino'></div>
    <div CLASS='pie-post'>
    <div style='float:left'>
    <div class='fb-like' data-href='http://www.somosmovies.com/2012/09/blancanieves-y-el-cazador-2012.html' data-layout='button_count' data-send='false' data-show-faces='false' data-width='120'></div>
    </div>
    </div>
    <div STYLE='clear: both;'></div>
    </section>
    </article>
    '''
    '''
    <article CLASS='post crp'>
    <header><h3 CLASS='post-title entry-title item_name'>
    <a href='http://www.somosmovies.com/2012/08/the-avengers-los-vengadores-2012.html' title='Los Vengadores (2012)'>Los Vengadores (2012)</a>
    </h3>
    </header>
    <section CLASS='post-body entry-content clearfix'>
    <a href='http://www.somosmovies.com/2012/08/the-avengers-los-vengadores-2012.html' title='Los Vengadores (2012)'><center><img border="0" src="http://4.bp.blogspot.com/-cF8QdycAgno/UDkWNys9iKI/AAAAAAAABd4/QPNK1tN9Qog/s1600/poster.jpg" style="display: block; height: 400px; width: 316;"></center></a>
    <div CLASS='latino'></div>
    <div CLASS='pie-post'>
    <div style='float:left'>
    <div class='fb-like' data-href='http://www.somosmovies.com/2012/08/the-avengers-los-vengadores-2012.html' data-layout='button_count' data-send='false' data-show-faces='false' data-width='120'></div>
    </div>
    </div>
    <div STYLE='clear: both;'></div>
    </section>
    </article>
    '''

    patron = "<article(.*?)</article>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        logger.info("match="+match)
        scrapedtitle = scrapertools.get_match(match,"<a href='[^']+' title='([^']+)'")
        scrapedurl = urlparse.urljoin(item.url, scrapertools.get_match(match,"<a href='([^']+)' title='[^']+'") )
        scrapedplot = ""
        scrapedthumbnail = urlparse.urljoin(item.url, scrapertools.get_match(match,'<img border="0" src="([^"]+)"') )
        try:
            idioma = scrapertools.get_match(match,"</center></a[^<]+<div CLASS='([^']+)'></div>")
            scrapedtitle = scrapedtitle + " ("+idioma.upper()+")"
        except:
            pass
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<a CLASS='blog-pager-older-link' href='http://www.somosmovies.com/search?updated-max=2012-08-22T23:10:00-05:00&amp;max-results=16' id='Blog1_blog-pager-older-link' title='Siguiente Película'>Siguiente &#187;</a>
    patronvideos  = "<a CLASS='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link' title='Siguiente"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        #http://www.somosmovies.com/search/label/Peliculas?updated-max=2010-12-20T08%3A27%3A00-06%3A00&max-results=12
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedurl = scrapedurl.replace("%3A",":")
        itemlist.append( Item(channel=__channel__, action="listado", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[somosmovies.py] findvideos")
    itemlist = []
    
    data = scrapertools.cachePage(item.url)
    
    '''
    <fieldset id="enlaces"><legend>Enlaces</legend><br />
    <div class="clearfix uno"><div class="dos"><b>1 LINK</b></div><div class="tres"><a href="http://goo.gl/U5Vdj" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://goo.gl/cCndD" target="_blank">EDOC</a> <b class="sep">|</b> <a href="http://goo.gl/j1SXg" target="_blank">PutLocker</a> <b class="sep">|</b> <a href="http://goo.gl/dT6ki" target="_blank">GlumboUploads</a> <b class="sep">|</b> <a href="http://goo.gl/UzNPb" target="_blank">RapidGator</a> <b class="sep">|</b> <a href="http://goo.gl/zawVY" target="_blank">TurboBit</a> <b class="sep">|</b> <a href="http://goo.gl/NLGjA" target="_blank">DepositFiles</a> <b class="sep">|</b> <a href="http://goo.gl/DQyv1" target="_blank">FreakShare</a> <br />
    </div></div><div class="clearfix uno"><div class="dos"><b>EN PARTES</b></div><div class="tres"><a href="http://goo.gl/bvAUf" target="_blank">Zippyshare</a> <b class="sep">|</b> <a href="http://goo.gl/2cA1o" target="_blank">1Fichier</a> <b class="sep">|</b> <a href="http://goo.gl/fCIyM" target="_blank">EDOC</a></div></div></fieldset>
    '''
    # Se queda con la caja de enlaces
    data = scrapertools.get_match(data,'<fieldset id="enlaces"><legend>Enlaces</legend>(.*?)</fieldset>')
    
    # Se queda con los enlaces 1 LINK
    data = scrapertools.get_match(data,'<div class="clearfix uno"><div class="dos"><b>1 LINK</b></div><div class="tres">(.*?)</div></div>')
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, server="", folder=False))

    return itemlist

def play(item):
    logger.info("[somosmovies.py] play(item.url="+item.url+")")
    itemlist=[]

    if "goo.gl" in item.url:
        logger.info("Acortador goo.gl")
        location = scrapertools.get_header_from_response(item.url,header_to_get="location")
        item.url = location
        return play(item)
    
    #adf.ly
    elif "j.gs" in item.url:
        logger.info("Acortador j.gs (adfly)")
        from servers import adfly
        location = adfly.get_long_url(item.url)
        item.url = location
        return play(item)

    else:
        from servers import servertools
        itemlist=servertools.find_video_items(data=item.url)
        for videoitem in itemlist:
            videoitem.channel=__channel__
            videoitem.folder=False

    return itemlist
