# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculamos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Peliculamos"
__channel__ = "peliculamos"
__language__ = "ES"
__creationdate__ = "20121105"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculamos.py] mainlist")
    item.url="http://peliculamos.net/"
    return generos(item)

def generos(item):
    logger.info("[peliculamos.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h2[^>]+>Categorie</h2>(.*?)</ul>')
    
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="listado" , title=title , url=url, thumbnail=thumbnail, plot=plot))        

    return itemlist

def listado(item):
    logger.info("[peliculamos.py] listado")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    '''
    <div id="post-5150" class="post-5150 post type-post status-publish format-standard hentry category-animazione category-commedia category-family tag-hotel-transylvania tag-ita tag-nowvideo tag-putlocker tag-streaming tag-vk">
    <h2 class="h2 entry-title">
    <a href="http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/" rel="bookmark" title="Permalink to Hotel Transylvania Streaming ITA VK Putlocker">Hotel Transylvania Streaming ITA VK Putlocker</a></h2>
    <div class="posted-on">
    <span class="meta-prep meta-prep-author">Posted on</span> <a href="http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/" title="October 26, 2012 8:01 pm" rel="bookmark"><span class="entry-date">October 26, 2012 8:01 pm</span></a> <span class="meta-sep">by</span> <span class="author vcard"><a class="url fn n" href="http://peliculamos.net/author/cismpg/" title="View all posts by Cismpg" rel="vcard:url">Cismpg</a></span> <a href="http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/#comments" class="raindrops-comment-link"><span class="raindrops-comment-string point"></span><em> Comment</em></a>			</div>
    <div class="entry-content clearfix">
    <div class="rw-left"><div class="rw-ui-container rw-class-blog-post rw-urid-51510"></div><div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating"><meta itemprop="ratingValue" content="5" /><meta itemprop="ratingCount" content="1" /></div></div><div class="fblike" style="height:25px; height:25px; overflow:hidden;"><iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fpeliculamos.net%2Fhotel-transylvania-streaming-ita-vk-putlocker%2F&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font=arial&amp;colorscheme=light" scrolling="no" frameborder="0" allow Transparency="true" style="border:none; overflow:hidden; width:450px;"></iframe></div><p><strong><img class="alignleft" src="http://mr.comingsoon.it/imgdb/locandine/140x200/48989.png" alt="" width="140" height="200" />Hotel Transylvania</strong></p>
    <p><em>Genere: Animazione, Commedia, Family</em></p>
    <p><em>Anno: 2012</em></p>
    <p><em>Regia: Genndy Tartakovsky</em></p>
    <p><em>Attori: Adam Sandler, Selena Gomez, Steve Buscemi, Kevin James, David Spade, Andy Samberg</em></p><!--Ad Injection:random-->
    <div style=''><center> <!-- Begin BidVertiser code -->
    <SCRIPT LANGUAGE="JavaScript1.1" SRC="http://bdv.bidvertiser.com/BidVertiser.dbm?pid=484093&bid=1202522" type="text/javascript"></SCRIPT>
    <noscript><a href="http://www.bidvertiser.com/bdv/BidVertiser/bdv_publisher_toolbar_creator.dbm">toolbar maker</a></noscript>
    <!-- End BidVertiser code --> </center></div>
    <p><em>Paese: USA</em></p>
    <p><em>Durata: 91 Min</em></p>
    <p><strong>Trama: </strong>Benvenuti all&#8217;Hotel Transylvania, il sontuoso resort a cinque stelle di Dracula dove i mostri e le loro rispettive famiglie possono divertirsi, liberi di essere sé stessi, senza alcuna presenza umana a dar loro fastidio. Durante uno speciale fine settimana, Dracula invita alcuni dei mostri più famosi del mondo a celebrare insieme il 118mo compleanno della figlia Mavis. Tra questi, Frankenstein e consorte, la Mummia, l&#8217;Uomo Invisibile, una famiglia di lupi mannari, e tanti altri. Per Drac, intrattenere tutti questi mostri leggendari non è certo un problema, ma il suo mondo sembra sgretolarsi quando all&#8217;albergo arriva un ragazzo che si prende una bella cotta per la giovane Mavis.</p>
    <p><strong>Trailer:</strong><strong></strong></p>
    <p><object id="_fp_0.368953057564795" width="640" height="360" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" name="player"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="wmode" value="transparent" /><param name="quality" value="high" /><param name="flashvars" value="config=http%3A//www.comingsoon.it/Video/Player/embed/32/%3Fsrc%3DMP4/9117.mp4%26lnkUrl%3DaHR0cDovL3d3dy5jb21pbmdzb29uLml0L0ZpbG0vU2NoZWRhL1ZpZGVvLz9rZXk9NDg5ODktOTExNw.." /><param name="src" value="http://mr.comingsoon.it/js/flowplayer/3209/flowplayer-3.2.9.swf" /><embed id="_fp_0.368953057564795" width="640" height="360" type="application/x-shockwave-flash" src="http://mr.comingsoon.it/js/flowplayer/3209/flowplayer-3.2.9.swf" allowfullscreen="true" allowscriptaccess="always" wmode="transparent" quality="high" flashvars="config=http%3A//www.comingsoon.it/Video/Player/embed/32/%3Fsrc%3DMP4/9117.mp4%26lnkUrl%3DaHR0cDovL3d3dy5jb21pbmdzb29uLml0L0ZpbG0vU2NoZWRhL1ZpZGVvLz9rZXk9NDg5ODktOTExNw.." name="player" /></object></p>
    <p><strong>Streaming:</strong> </p>
    <p><span class='st_facebook_large' st_title='Hotel Transylvania Streaming ITA VK Putlocker' st_url='http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/' displayText='share'></span>
    </span><span class='st_twitter_large' st_title='Hotel Transylvania Streaming ITA VK Putlocker' st_url='http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/' displayText='share'></span>
    </span><span class='st_email_large' st_title='Hotel Transylvania Streaming ITA VK Putlocker' st_url='http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/' displayText='share'></span>
    </span><span class='st_sharethis_large' st_title='Hotel Transylvania Streaming ITA VK Putlocker' st_url='http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/' displayText='share'></span>
    </span><span class='st_fblike_large' st_title='Hotel Transylvania Streaming ITA VK Putlocker' st_url='http://peliculamos.net/hotel-transylvania-streaming-ita-vk-putlocker/' displayText='share'></span>
    </span><span class='st_plusone_large' st_title='Ho
    '''
    patron  = '<div id="post-[^<]+'
    patron += '<h2 class="h2 entry-title">[^<]+'
    patron += '<a href="([^"]+)"[^>]+>([^<]+)</a></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot))        

    try:
        siguiente = scrapertools.get_match(data,'<a href="([^<]+)"[^<]+<span class="meta-nav"[^<]+</span> Older posts</a>')
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="listado", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    except:
        pass
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                mirrors = findvideos(item=itemlist[0])
                if len(mirrors)>0:
                    return True

    return False