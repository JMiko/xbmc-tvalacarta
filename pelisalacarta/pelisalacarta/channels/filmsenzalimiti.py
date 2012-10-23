# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para filmsenzalimiti
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmsenzalimiti"
__category__ = "F"
__type__ = "generic"
__title__ = "Film Senza Limiti (IT)"
__language__ = "IT"
__creationdate__ = "20120605"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[filmsenzalimiti.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novità"     , action="novedades", url="http://www.filmsenzalimiti.it/"))
    itemlist.append( Item(channel=__channel__, title="Per genere" , action="categorias", url="http://www.filmsenzalimiti.it/"))
    return itemlist

def categorias(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    #<ul id="ul_categories"><li><a href="http://www.filmsenzalimiti.it/browse-filmalcinemastreaming-videos-1-date.html">Al Cinema</a></li><li><a href="http://www.filmsenzalimiti.it/browse-allfilms-videos-1-date.html">All Films</a></li><li><a href="http://www.filmsenzalimiti.it/browse-animazione-videos-1-date.html">Animazione</a></li><li><a href="http://www.filmsenzalimiti.it/browse-anime-videos-1-date.html">Anime</a></li><li><a href="http://www.filmsenzalimiti.it/browse-avventura-videos-1-date.html">Avventura</a></li><li><a href="http://www.filmsenzalimiti.it/browse-azione-videos-1-date.html">Azione</a></li><li><a href="http://www.filmsenzalimiti.it/browse-cinesuccessi-videos-1-date.html">Cinesuccessi</a></li><li><a href="http://www.filmsenzalimiti.it/browse-cofanetti-videos-1-date.html">Cofanetti</a></li><li><a href="http://www.filmsenzalimiti.it/browse-commedia-videos-1-date.html">Commedia</a></li><li><a href="http://www.filmsenzalimiti.it/browse-concerti-videos-1-date.html">Concerti</a></li><li><a href="http://www.filmsenzalimiti.it/browse-demenziale-videos-1-date.html">Demenziale</a></li><li><a href="http://www.filmsenzalimiti.it/browse-documentario-videos-1-date.html">Documentario</a></li><li><a href="http://www.filmsenzalimiti.it/browse-drammatico-videos-1-date.html">Drammatico</a></li><li><a href="http://www.filmsenzalimiti.it/browse-fantascienza-videos-1-date.html">Fantascienza</a></li><li><a href="http://www.filmsenzalimiti.it/browse-horror-videos-1-date.html">Horror</a></li><li><a href="http://www.filmsenzalimiti.it/browse-musical-videos-1-date.html">Musical</a></li><li><a href="http://www.filmsenzalimiti.it/browse-film_natalizi_in_streaming_megavideo_senza_limiti-videos-1-date.html">Natale</a></li><li><a href="http://www.filmsenzalimiti.it/browse-parodia-videos-1-date.html">Parodia</a></li><li><a href="http://www.filmsenzalimiti.it/browse-poliziesco-videos-1-date.html">Poliziesco</a></li><li><a href="http://www.filmsenzalimiti.it/browse-romantico-videos-1-date.html">Romantico</a></li><li><a href="http://www.filmsenzalimiti.it/browse-serietv-videos-1-date.html">Serie TV</a><ul class="hidden_li"><li><a href="http://www.filmsenzalimiti.it/browse-alcatraz-videos-1-date.html">Alcatraz</a></li><li><a href="http://www.filmsenzalimiti.it/browse-cameracaffe-videos-1-date.html">Camera Caffè</a></li><li><a href="http://www.filmsenzalimiti.it/browse-chuck-videos-1-date.html">Chuck</a></li><li><a href="http://www.filmsenzalimiti.it/browse-gossipgirl-videos-1-date.html">Gossip Girl</a></li><li><a href="http://www.filmsenzalimiti.it/browse-greysanatomy-videos-1-date.html">Grey's Anatomy</a></li><li><a href="http://www.filmsenzalimiti.it/browse-lietome-videos-1-date.html">Lie to Me</a></li><li><a href="http://www.filmsenzalimiti.it/browse-onetreehill-videos-1-date.html">One Tree Hill</a></li><li><a href="http://www.filmsenzalimiti.it/browse-scrubs-videos-1-date.html">Scrubs</a></li><li><a href="http://www.filmsenzalimiti.it/browse-sexcity-videos-1-date.html">Sex And City</a></li><li><a href="http://www.filmsenzalimiti.it/browse-sharlock-videos-1-date.html">Sherlock</a></li><li><a href="http://www.filmsenzalimiti.it/browse-tag-videos-1-date.html">Simpson</a></li><li><a href="http://www.filmsenzalimiti.it/browse-teenwolf-videos-1-date.html">Teen Wolf</a></li><li><a href="http://www.filmsenzalimiti.it/browse-theoc-videos-1-date.html">The O.C</a></li><li><a href="http://www.filmsenzalimiti.it/browse-vampirediares-videos-1-date.html">The Vampire Diares</a></li><li><a href="http://www.filmsenzalimiti.it/browse-trueblood-videos-1-date.html">True Blood</a></li></ul></li><li><a href="http://www.filmsenzalimiti.it/browse-sportivo-videos-1-date.html">Sportivo</a></li><li><a href="http://www.filmsenzalimiti.it/browse-thriller-videos-1-date.html">Thriller</a></li></ul>		</div>
    data = scrapertools.get_match(data,'<ul id="ul_categories">(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def novedades(item):
    logger.info("[filmsenzalimiti.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="item">
    <a href="http://www.filmsenzalimiti.it/film/lorax-il-guardiano-della-foresta-video_2daaf402a.html"><img src="http://images.movieplayer.it/2012/03/08/lorax-il-guardiano-della-foresta-la-nuova-locandina-italiana-del-film-233842_medium.jpg" alt="Lorax - Il Guardiano Della Foresta" class="imag" width="116" height="87" /></a><br />
    <span class="artist_name">Film</span>
    <a href="http://www.filmsenzalimiti.it/film/lorax-il-guardiano-della-foresta-video_2daaf402a.html" class="song_name">Lorax - Il Guardiano Della Foresta</a>
    <span class="item_views">5700 views</span>
    </div>
    '''
    patronvideos  = '<div class="item">[^<]+'
    patronvideos += '<a href="([^"]+)"><img src="([^"]+)"\s+alt="([^"]+)"'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )
    
    '''
    <li class="video">
    <div class="video_i">
    <a href="http://www.filmsenzalimiti.it/film/abrafaxe-e-i-pirati-dei-caraibi-video_5b289158e.html">
    <img src="http://giotto.ibs.it/vjack/z74/5050582194074.jpg"  alt="Abrafaxe E I Pirati Dei Caraibi" class="imag" width="116" height="87" /><div class="tag"></div>
    <span class="artist_name">Film</span> Abrafaxe E I Pira...
    </a>
    </div>
    </li>
    '''
    patronvideos  = '<div class="video_i">[^<]+'
    patronvideos += '<a href="([^"]+)">[^<]+'
    patronvideos += '<img src="([^"]+)"\s+alt="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    patron = '<a href="([^"]+)">prossimo \&raquo\;</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Next page"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    items = novedades(mainlist_items[0])
    bien = False
    for singleitem in items:
        mirrors = servertools.find_video_items( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien