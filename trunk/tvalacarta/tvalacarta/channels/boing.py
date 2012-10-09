# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para boing.es
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[boing.py] init")

DEBUG = True
CHANNELNAME = "boing"
MAIN_URL = "http://www.boing.es/series?order=title&sort=asc"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[boing.py] mainlist")
    item.url = MAIN_URL
    return series(item)

def series(item):
    logger.info("[boing.py] series")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las series
    '''
    <div class="pic"><div class="pic2"><div class="pic3"><a href="/serie/chowder" class="imagecache imagecache-130x73 imagecache-linked imagecache-130x73_linked"><img src="http://www.boing.es/sites/default/files/imagecache/130x73/chowder.jpg" alt="" title=""  class="imagecache imagecache-130x73" width="130" height="73" /></a></div></div></div>
    
    <div class="clear"></div>
    <div class="stars"><form action="/series?order=title&amp;sort=asc"  accept-charset="UTF-8" method="post" id="fivestar-custom-widget-26" class="fivestar-widget">
    <div><div class="fivestar-form-vote-813 clear-block"><input type="hidden" name="content_type" id="edit-content-type-26" value="node"  />
    <input type="hidden" name="content_id" id="edit-content-id-26" value="813"  />
    <div class="fivestar-form-item  fivestar-average-stars"><div class="form-item" id="edit-vote-52-wrapper">
    <span class='edit-vote-52-design'><span class='form-item-value-design1'><span class='form-item-value-design2'><span class='form-item-value-design3'> <input type="hidden" name="vote_count" id="edit-vote-count-26" value="0"  />
    <input type="hidden" name="vote_average" id="edit-vote-average-26" value="67.2237"  />
    <input type="hidden" name="auto_submit_path" id="edit-auto-submit-path-26" value="/fivestar/vote/node/813/vote"  class="fivestar-path" />
    <select name="vote" class="form-select" id="edit-vote-53" ><option value="-">Select rating</option><option value="20">Give it 1/5</option><option value="40">Give it 2/5</option><option value="60">Give it 3/5</option><option value="80" selected="selected">Give it 4/5</option><option value="100">Give it 5/5</option></select><input type="hidden" name="auto_submit_token" id="edit-auto-submit-token-26" value="56e73589059273a3c5fe1a8abc137a87"  class="fivestar-token" />
    
    </span></span></span></span></div>
    </div><input type="hidden" name="destination" id="edit-destination-26" value="series"  />
    <input type="submit" name="op" id="edit-fivestar-submit-26" value="Rate"  class="form-submit fivestar-submit" />
    <input type="hidden" name="form_build_id" id="form-7afce4746464c15152c61b751ad73da5" value="form-7afce4746464c15152c61b751ad73da5"  />
    <input type="hidden" name="form_id" id="edit-fivestar-custom-widget-26" value="fivestar_custom_widget"  />
    </div>
    </div></form></div>
    <div class="title"><a href="/serie/chowder">Chowder</a></div>
    
    <div class="sin">�Qui�n dijo que cocinar es aburrido? La cocina de Chowder...</div>
    '''
    patron  = '<div class="pic"><div class="pic2"><div class="pic3"><a href="([^"]+)"[^<]+<img src="([^"]+)".*?'
    patron += '<div class="title"><a href="[^"]+">([^<]+)</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    destacadas = 4
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        destacadas = destacadas - 1
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if destacadas>=0:
            logger.info("ignorando, es de la caja de destacadas")
        else:
            itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="episodios" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )
    
    #<li class="pager-next"><a href="/series?page=1&amp;order=title&amp;sort=asc" title="Ir a la p�gina siguiente" class="active">siguiente
    patron = '<li class="pager-next"><a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        itemlist.extend( series(Item(channel=item.channel, title="P�gina siguiente >>" , action="series" , url=urlparse.urljoin(item.url,matches[0].replace("&amp;","&")), folder=True) ) )

    return itemlist

def episodios(item):
    logger.info("[boing.py] episodios")

    # Descarga la p�gina
    #http://www.boing.es/serie/hora-de-aventuras
    #http://www.boing.es/videos/hora-de-aventuras
    data = scrapertools.cachePage(item.url.replace("/serie/","/videos/"))
    #logger.info(data)
    bloque = scrapertools.get_match(data,'<div class="Contenedor100">(.*?)<\!-- \/Contenedor100 -->',1)
    logger.info(str(bloque))

    # Extrae los videos
    '''
    <div class="pic"><div class="pic2"><div class="pic3">    
    <a href="/serie/geronimo-stilton/video/top-model">
    <img class="bcvid" height="73" width="130" src="http://i.cdn.turner.com/tbseurope/big/Boing_ES/thumbs/SP_SA_GERSTI0017_01.jpg" />
    </a>
    </div></div></div>
    <div class="series"><a href="/serie/geronimo-stilton">Ger�nimo Stilton</a></div>
    <div class="title"><a href="/serie/geronimo-stilton/video/top-model">Top Model</a></div>
    '''
    '''
    <div class="pic"><div class="pic2"><div class="pic3">
    
    <a href="/serie/generator-rex/video/hombre-contra-hombre">
    <img style="margin-top:10px" height="73" width="130" src="http://i.cdn.turner.com/tbseurope/big/Boing_ES_16_9/thumbs/SP_SA_GENREX0047_01.jpg" />
    </a>
    
    
    </div></div></div>
    <div class="stars"><form action="/videos/generator-rex"  accept-charset="UTF-8" method="post" id="fivestar-custom-widget" class="fivestar-widget">
    <div><div class="fivestar-form-vote-18249 clear-block"><input type="hidden" name="content_type" id="edit-content-type" value="node"  />
    <input type="hidden" name="content_id" id="edit-content-id" value="18249"  />
    <div class="fivestar-form-item  fivestar-average-stars"><div class="form-item" id="edit-vote-wrapper">
    <span class='edit-vote-design'><span class='form-item-value-design1'><span class='form-item-value-design2'><span class='form-item-value-design3'> <input type="hidden" name="vote_count" id="edit-vote-count" value="0"  />
    <input type="hidden" name="vote_average" id="edit-vote-average" value="76.25"  />
    <input type="hidden" name="auto_submit_path" id="edit-auto-submit-path" value="/fivestar/vote/node/18249/vote"  class="fivestar-path" />
    <select name="vote" class="form-select" id="edit-vote-1" ><option value="-">Select rating</option><option value="20">Give it 1/5</option><option value="40">Give it 2/5</option><option value="60">Give it 3/5</option><option value="80" selected="selected">Give it 4/5</option><option value="100">Give it 5/5</option></select><input type="hidden" name="auto_submit_token" id="edit-auto-submit-token" value="36639bc15e086e0bfc3d93bfec3d5287"  class="fivestar-token" />
    
    </span></span></span></span></div>
    </div><input type="hidden" name="destination" id="edit-destination" value="videos/generator-rex"  />
    <input type="submit" name="op" id="edit-fivestar-submit" value="Rate"  class="form-submit fivestar-submit" />
    <input type="hidden" name="form_build_id" id="form-d62c4ce5673f9173ca3edb7e81986457" value="form-d62c4ce5673f9173ca3edb7e81986457"  />
    <input type="hidden" name="form_id" id="edit-fivestar-custom-widget" value="fivestar_custom_widget"  />
    </div>
    </div></form></div>
    <div class="series"><a href="/serie/generator-rex">Generator Rex</a></div>
    <div class="title"><a href="/serie/generator-rex/video/hombre-contra-hombre">Hombre contra hombre</a></div>
    '''
    '''
    <div class="pic3">
    
    <a href="/serie/monster-high/video/monster-high-superpillada" class="imagecache imagecache-130x73 imagecache-linked imagecache-130x73_linked"><img src="http://www.boing.es/sites/default/files/imagecache/130x73/pantallazo2mh.jpg" alt="" title=""  class="imagecache imagecache-130x73" width="130" height="73" /></a>      		      		
    
    </div></div></div>
    <div class="stars"><form action="/videos/monster-high"  accept-charset="UTF-8" method="post" id="fivestar-custom-widget" class="fivestar-widget">
    <div><div class="fivestar-form-vote-24388 clear-block"><input type="hidden" name="content_type" id="edit-content-type" value="node"  />
    <input type="hidden" name="content_id" id="edit-content-id" value="24388"  />
    <div class="fivestar-form-item  fivestar-average-stars"><div class="form-item" id="edit-vote-wrapper">
    <span class='edit-vote-design'><span class='form-item-value-design1'><span class='form-item-value-design2'><span class='form-item-value-design3'> <input type="hidden" name="vote_count" id="edit-vote-count" value="0"  />
    <input type="hidden" name="vote_average" id="edit-vote-average" value="67.9646"  />
    <input type="hidden" name="auto_submit_path" id="edit-auto-submit-path" value="/fivestar/vote/node/24388/vote"  class="fivestar-path" />
    <select name="vote" class="form-select" id="edit-vote-1" ><option value="-">Select rating</option><option value="20">Give it 1/5</option><option value="40">Give it 2/5</option><option value="60">Give it 3/5</option><option value="80" selected="selected">Give it 4/5</option><option value="100">Give it 5/5</option></select><input type="hidden" name="auto_submit_token" id="edit-auto-submit-token" value="219ac03ae7ca6956d5484acb00454195"  class="fivestar-token" />
    
    </span></span></span></span></div>
    </div><input type="hidden" name="destination" id="edit-destination" value="videos/monster-high"  />
    <input type="submit" name="op" id="edit-fivestar-submit" value="Rate"  class="form-submit fivestar-submit" />
    <input type="hidden" name="form_build_id" id="form-9e308b4823178e9cbca63316130d805e" value="form-9e308b4823178e9cbca63316130d805e"  />
    <input type="hidden" name="form_id" id="edit-fivestar-custom-widget" value="fivestar_custom_widget"  />
    </div>
    </div></form></div>
    <div class="series"><a href="/serie/monster-high">Monster High</a></div>
    <div class="title"><a href="/serie/monster-high/video/monster-high-superpillada">Monster High: Superpillada</a></div>
    
    '''
    patron  = '<div class="pic3"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img style="[^"]+" height="\d+" width="\d+" src="([^"]+)".*?'
    patron += '<div class="title"><a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)
    #if DEBUG: scrapertools.printMatches(matches)

    if len(matches)==0:
        patron  = '<div class="pic3"[^<]+'
        patron += '<a href="([^"]+)"[^<]+<img src="([^"]+)".*?'
        patron += '<div class="title"><a[^>]+>([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(bloque)
        scrapertools.printMatches(matches)
        #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        url = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="boing" , url=url, thumbnail=scrapedthumbnail, page=url, show = item.show, folder=False) )

    return itemlist

def test():
    itemsmainlist = mainlist(None)
    for item in itemsmainlist: print item.tostring()

    itemsseries = series(itemsmainlist[1])
    itemsepisodios = episodios(itemsseries[4])

if __name__ == "__main__":
    test()
