# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para letmewatchthis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "letmewatchthis"
__category__ = "F,S"
__type__ = "generic"
__title__ = "LetMeWatchThis"
__language__ = "EN"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[letmewatchthis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="doaction" , title="Movies - Full List"   ,url="http://www.1channel.ch/", extra="showlinks"))
    itemlist.append( Item(channel=__channel__, action="alphabetical"    , title="Movies - Alphabetical Order" ,   url="http://www.1channel.ch/", extra="1|showlinks"  ) )
    itemlist.append( Item(channel=__channel__, action="genre"    , title="Movies - Genre" ,   url="http://www.1channel.ch/", extra="showlinks"  ) )
    itemlist.append( Item(channel=__channel__, action="search"    , title="Movies - Search"   ,extra="1") )
    itemlist.append( Item(channel=__channel__, action="doaction"    , title="TV Shows - Full List" ,url="http://www.1channel.ch/?tv", extra="tvshowepisodes"))
    itemlist.append( Item(channel=__channel__, action="alphabetical"    , title="TV Shows - Alphabetical Order" ,   url="http://www.1channel.ch/?tv", extra="2|tvshowepisodes"  ) )
    itemlist.append( Item(channel=__channel__, action="genre"    , title="TV Shows - Genre" ,   url="http://www.1channel.ch/?tv", extra="tvshowepisodes"  ) )
    itemlist.append( Item(channel=__channel__, action="search"    , title="TV Shows - Search"   ,extra="2"))
    
    return itemlist

def alphabetical(item):
    data = scrapertools.cache_page("http://www.1channel.ch/index.php?search")
    iaction, iextra = item.extra.split('|')
    #List Movies By</td>
    #<td><a href="/?letter=123">#</a> <a href="/?letter=a">A</a> <a href="/?letter=b">B</a> <a href="/?letter=z">Z</a> |
    concat = "&sort=alphabet"
    if iaction == "2":
        concat = concat + '&tv'
        
    patron = 'List Movies By</td>(.*?)\|'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    if len(matches) == 1:
        #<a href="/?letter=123">#</a>
        patron = '<a href="([^"]+)">([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])  
        for match in matches:
            scrapedurl = urlparse.urljoin(item.url,match[0]) + concat
            scrapedtitle = match[1]
            itemlist.append( Item(channel=__channel__, action="doaction", title=scrapedtitle ,url=scrapedurl, extra=iextra))
    return itemlist

def genre(item):
    data = scrapertools.cache_page(item.url)
    
    #<ul class="menu-genre-list"><li><a href="/?tv&genre=Action">Action</a></li><li><a href="/?tv&genre=Adventure">Adventure</a></li></ul>
    patron = '<ul class="menu-genre-list">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    if len(matches) == 1:
        #<li><a href="/?tv&genre=Action">Action</a></li>
        patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])  
        for match in matches:
            scrapedurl = urlparse.urljoin(item.url,match[0])
            scrapedtitle = match[1]
            itemlist.append( Item(channel=__channel__, action="doaction", title=scrapedtitle ,url=scrapedurl, extra=item.extra))
    return itemlist

    
def search(item,texto, categoria="*"):
    
    url = 'http://www.1channel.ch/index.php'   
    
    if item.extra == "1":
        #Movies 
        key = getkey("http://www.1channel.ch/")
        post = "search_keywords=%s&key=%s&search_section=%s" % ( texto, key, "1")
        item.url = url + "?" + post
        item.extra = "showlinks"
        return doaction(item)    
    
    if item.extra == "2":
        #TV Shows 
        key = getkey("http://www.1channel.ch/?tv")
        post = "search_keywords=%s&key=%s&search_section=%s" % ( texto, key, "2")
        item.url = url + "?" + post
        item.extra = "tvshowepisodes"
        return doaction(item)  
      
    return []   

def play(item):
    logger.info("[letmewatchthis.py] play")
    
    itemlist = servertools.find_video_items(item) 
    if len(itemlist) == 0:  
        try:
            count = 0
            exit = False
            while(not exit and count < 5):
                #A veces da error al intentar acceder
                try:
                    page = urllib2.urlopen(item.url)
                    urlvideo = page.geturl() 
                    exit = True
                except:
                    count = count + 1
            if(exit):
                    listavideos = servertools.findvideos(urlvideo)
                    for video in listavideos:
                        scrapedtitle = item.title.strip() + " - " + video[0].strip()
                        scrapedurl = video[1]
                        server = video[2]
                        
                        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

        except:  
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line ) 
                 
    for videoitem in itemlist:
        try:
            videoitem.title = scrapertools.get_match(item.title,"Watch Version \d+ of (.*)\(")
        except:
            videoitem.title = item.title
    
    return itemlist


def doaction(item):
    logger.info("[letmewatchthis.py] search")
    
    
    data = scrapertools.cache_page(item.url)
    
    #<div class="index_item index_item_ie"><a href="/watch-2700449-Accused" title="Watch Accused (2010)"><img src="http://images.1channel.ch/thumbs/2700449_Accused_2010.jpg" border="0" width="150" height="225" alt="Watch Accused"><h2>Accused (2010)</h2></a><div
    patron = '<div class="index_item.*?<div'
    matches = re.compile(patron,re.DOTALL).findall(data)
        
    itemlist = []
    for match in matches:
        patron  = 'href="([^"]+)".*?src="([^"]+)".*?<h2>([^<]+)<'
        matches2 = re.compile(patron,re.DOTALL).findall(match)
        if len(matches2)==1:
            match2 = matches2[0]
            # Titulo
            scrapedtitle = match2[2]
            scrapedplot = ""
            scrapedurl = urlparse.urljoin(item.url,match2[0])
            scrapedthumbnail = match2[1]
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action=item.extra, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    
    #<div class="pagination">
    #<a href="/index.php?search_keywords=game&key=23ef634b78404be9&search_section=1&page=1"> << </a>&nbsp;<a href="/index.php?search_keywords=game&key=23ef634b78404be9&search_section=1&page=1">1</a> <a href="/index.php?search_keywords=game&key=23ef634b78404be9&search_section=1&page=2">2</a> <a href="/index.php?search_keywords=game&key=23ef634b78404be9&search_section=1&page=3">3</a> <a href="/index.php?search_keywords=game&key=23ef634b78404be9&search_section=1&page=4">4</a> <span class=current>5</span> </div>
    #</div>
    patronvideos  = '<div class="pagination">.*?</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        patronvideos = '<span class=current>[^<]+</span>[^h]+href="([^"]+)">'        
        matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
        if len(matches)>0:
            scrapedurl = urlparse.urljoin(item.url,matches[0])
            itemlist.append( Item(channel=__channel__, action="doaction", title="!Next page >>" , url=scrapedurl , folder=True, extra= item.extra) )
    
    return itemlist

def tvshowepisodes(item):
    logger.info("[letmewatchthis.py] listepisodes")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    #<div class="tv_container" style="float:left;"><h2><a href="/tv-2700449-Accused/season-1">Season 1</a></h2>
    patron = '<h2><a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)<=1:
        return season(item, data,"Season 1")
    
    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedtitle = match[1]
        itemlist.append( Item(channel=__channel__, action="fillseason", title=scrapedtitle ,url=scrapedurl, extra=item.extra))
    
            
    return itemlist        
def fillseason(item): 
    data = scrapertools.cachePage(item.url)    
    return season(item, data, item.title)
        
def season(item, data, season):    
    itemlist = []      
    #<div class="tv_episode_item"> <a href="/tv-2700449-Accused/season-1-episode-3">Episode 3
    #<span class="tv_episode_name"> - Helen's Story</span>        </a> </div>  
    #<div class="tv_episode_item"> <a href="/tv-13098-The-Game/season-5-episode-4">Episode 4                              </a> </div>
    patron = '<div class="tv_episode_item">(.*?)</div>'
    matches2 = re.compile(patron,re.DOTALL).findall(data)
    for match2 in matches2: 
        #There are chapters without "TITLE"
        patron = '<a href="([^"]+)">([^<]+)<'
        matches3 = re.compile(patron,re.DOTALL).findall(match2)
        patron = '<span class="tv_episode_name">([^<]+)</span>'
        matches4 = re.compile(patron,re.DOTALL).findall(match2)
        if len(matches3) ==1:
            title = ""
            if len(matches4)==1:
                title = matches4[0]
                
            scrapedtitle = season + " " + matches3[0][1].strip() + title
            scrapedthumbnail = item.thumbnail
            scrapedurl = urlparse.urljoin(item.url,matches3[0][0])
            scrapedplot = ""
            itemlist.append( Item(channel=__channel__, action="showlinks", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
             
        
    return itemlist        
        
def showlinks(item):
    logger.info("[letmewatchthis.py] listmirrors")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <a href="/external0" onClick="return  addHit('1889692257', '1')" rel="nofollow" title="Watch Version 3 of Accused" target="_blank">Version 3</a>
    </span></td>
    <td align="center" width="115" valign="middle"><span class="version_host"><script type="text/javascript">document.writeln('veehd.com');</script></span>
    '''
    
    patronvideos  = 'movie_version_link">.*?<a href="(/external[^"]+)".*?title="[^>]+>([^<]+)</a>.*?'
    patronvideos += '<span class="version_host">[^\']+\'([^\']+)\''

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Servidor
        servidor = match[2].strip()
        # Titulo
        scrapedtitle = scrapertools.htmlclean(match[1])+ " [" + servidor + "]"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra="", category=item.category, fanart=item.thumbnail, folder=False))

          
    return itemlist
# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = listmirrors( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien

def getkey(url):
    
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    '''
      <fieldset class="search_container">
        <input type="text" id="search_term" name="search_keywords"  class="box" value="Search Title" onFocus="clearText(this)" onBlur="clearText(this)">
        <input type="hidden" name="key" value="aa68c1afe6a4d965" />
        <input type="hidden" value="2" name="search_section">
        <button class="btn" title="Submit Search" type="submit"></button>
        <span class="search_advanced_link" ><a href="http://www.1channel.ch/index.php?search">Advanced Search</a></span>
      </fieldset>
    '''

    patronvideos  = '<fieldset class="search_container">.*?</fieldset>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches) == 1:
        patronvideos  = 'name="key".*?"([^"]+)"'    
        matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    
    if len (matches) == 1:
        return matches[0]
    
    return ""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    