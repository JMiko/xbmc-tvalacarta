# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para beeg.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por aampudia
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "beeg"
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[beeg.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="videos"      , title="Útimos videos" , url="http://www.beeg.com/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcategorias"    , title="Listado Categorias"))
    return itemlist

def videos(item):
    logger.info("[beeg.py] videos")
    data = scrapertools.downloadpageWithoutCookies(item.url)
    itemlist = []

    matches = re.compile('<div id="thumbs">.*?<div style="clear: both;"></div></div>', re.S).findall(data)
    for match in matches:
        datos = re.compile('<a href="([^"]+)".*?<img src="([^"]+).*?title="([^"]+)" />.*?</a>', re.S).findall(match)		
        for video in datos:
            try:
                scrapedtitle = unicode( video[2], "utf-8" ).encode("iso-8859-1")
            except:
                scrapedtitle = video[2]
            scrapedurl =  video[0]
            scrapedthumbnail = video[1]
            scrapedplot = ""
            # Depuracion
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
            itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, folder=False))
        
    # EXTRAE EL PAGINADOR
    #<a href='search.php?q=sexo&qcat=video&page=3' class='last'>Next</a></td></tr></table></div></td>
    patronvideos  = '<a href="" onclick="return false" target="_self" class="current">.*?<a href="([^"]+)" target="_self">.*?</div>'
    #patronvideos  = '<a href=\'([^\']+)\' class=\'last\'>Next</a></td></tr></table></div></td>'
    siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(siguiente)
    if len(siguiente)>0:
        itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="!Pagina siguiente" , url=siguiente[0], thumbnail="", plot="", show="!Página siguiente") )
    else:
        paginador = None

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
    
def listcategorias(item):
    logger.info("[beeg.py] listcategorias")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Long Videos", url="http://www.beeg.com/section/long-videos/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Teen Sex"  , url="http://www.beeg.com/section/teen-sex/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Sweet"  , url="http://www.beeg.com/section/sweet/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Beautiful tits"  , url="http://www.beeg.com/section/beautiful-tits/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="In Clothes"  , url="http://www.beeg.com/section/in-clothes/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Harder"  , url="http://www.beeg.com/section/harder/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Anal"  , url="http://www.beeg.com/section/anal/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Moan"  , url="http://www.beeg.com/section/moan/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="European"  , url="http://www.beeg.com/section/european/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Stylish"  , url="http://www.beeg.com/section/stylish/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Group"  , url="http://www.beeg.com/section/group/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Lesbians"  , url="http://www.beeg.com/section/lesbians/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Cumshot"  , url="http://www.beeg.com/section/cumshot/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Masturbation"  , url="http://www.beeg.com/section/masturbation/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Big Cock"  , url="http://www.beeg.com/section/big-cock/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Bit Tits"  , url="http://www.beeg.com/section/big-tits/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Big Ass"  , url="http://www.beeg.com/section/big-ass/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Uniform"  , url="http://www.beeg.com/section/uniform/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="At Work"  , url="http://www.beeg.com/section/at-work/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Blonde"  , url="http://www.beeg.com/section/blonde/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Brunette"  , url="http://www.beeg.com/section/brunette/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Redhead"  , url="http://www.beeg.com/section/redhead/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Fun"  , url="http://www.beeg.com/section/fun/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Lingerie"  , url="http://www.beeg.com/section/lingerie/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Stockings"  , url="http://www.beeg.com/section/stockings/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Panties"  , url="http://www.beeg.com/section/panties/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Skirt"  , url="http://www.beeg.com/section/skirt/"))
    itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Outside"  , url="http://www.beeg.com/section/outside/"))
    return itemlist
    
def play(item):
    logger.info("[beeg.py] play")
    itemlist = []

    '''
    headers=[]
    headers.append( [ "User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:12.0) Gecko/20100101 Firefox/12.0" ] )
    headers.append( [ "Referer","http://beeg.com/" ] )
    headers.append( [ "Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ] )
    headers.append( [ "Accept-Encoding" , "gzip, deflate" ] )
    headers.append( [ "Accept-Language" , "es-es,es;q=0.8,en-us;q=0.5,en;q=0.3" ] )
    headers.append( [ "Connection" , "keep-alive" ] )
    headers.append( [ "Cookie" , "uniqid=xxxxxxxx; firsttime=1336260347; firsttimeref=direct; lasttime=1338080395; pageview=37;" ] )
    '''
    
    data = scrapertools.downloadpageGzip(item.url)
    logger.info("data="+data)

    #'file': 'http://45.video.mystreamservice.com/480p/4014660.mp4',
    #'file': 'http://02.007i.net/480p/4815411.mp4',
    patron = "'file'\: '([^']+)'"
    url = scrapertools.get_match(data,patron)+"?start=0"
    itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="directo", folder=False))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    videos_items = videos(mainlist_items[0])
    play_items = play(videos_items[0])

    if len(play_items)==0:
        return False

    return True
