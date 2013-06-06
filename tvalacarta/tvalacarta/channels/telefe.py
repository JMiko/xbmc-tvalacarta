# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Telefe
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "telefe"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[telefe.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , action="programas"  , thumbnail = "" , url="http://www.telefe.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Exclusivo web"       , action="videos"     , thumbnail = "" , url="http://www.telefe.com/tipo/exclusivo-web/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Vídeos"              , action="videos"     , thumbnail = "" , url="http://www.telefe.com/tipo/videos/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Episodios completos" , action="videos"     , thumbnail = "" , url="http://www.telefe.com/tipo/capitulos-completos"))

    return itemlist

def programas(item):
    logger.info("[telefe.py] programas")
    
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h3>Todos los Programas</h3>(.*?)</ul>')
    
    patron  = '<li[^<]+<a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="videos" , url=url, thumbnail=thumbnail, plot=plot , show=scrapedtitle, folder=True) )

    return itemlist

def videos(item):
    logger.info("[telefe.py] videos")
    
    itemlist=[]

    # Extrae los programas
    '''
    <div id="post-66135" class="post-66135 post type-post status-publish format-standard hentry category-amorencustodia row with-thumbnail">
    <div class="entry-category" >
    <a href="http://www.telefe.com/amorencustodia/" title="Amor en custodia">Amor en custodia</a>&nbsp;
    </div>
    <div class="entry-data">
    <div class="entry-media">
    <a href="http://www.telefe.com/2013/05/30/capitulo8/"
    title="Enlace permanente a Capítulo 8: Peligro y amenaza"
    rel="bookmark"><img width="200" height="112" src="http://www.telefe.com/wp-content/blogs.dir/10/files/2013/05/UAAI9069-37019-200x112.jpg" class="attachment-thumb-16:9-33% wp-post-image" alt="UAAI9069-37019" title="Capítulo 8: Peligro y amenaza" /> </a>
    </div>
    <h2 class="entry-title">
    <a href="http://www.telefe.com/2013/05/30/capitulo8/"
    title="Enlace permanente a Capítulo 8: Peligro y amenaza"
    rel="bookmark">Capítulo 8: Peligro y amenaza </a>
    </h2>
    <div class="entry-meta">
    <a href="http://www.telefe.com/2013/05/30/capitulo8/" title="9:41" rel="bookmark"><span class="entry-date">30 mayo, 2013</span></a>     </div>
    <div class="entry-summary">
    <p>Reviví todos los capítulos de Amor en custodia</p>
    </div>
    '''
    data = scrapertools.cache_page(item.url)
    logger.info("url="+item.url)
    logger.info("data="+data)
    
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<div class="entry-category"[^<]+'
    patron += '<a[^>]+>([^"]+)</a[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="entry-data[^<]+'
    patron += '<div class="entry-media[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img width="[^"]+" height="[^"]+" src="([^"]+)"[^<]+</a[^<]+'
    patron += '</div>[^<]+'
    patron += '<h2 class="entry-title"[^<]+'
    patron += '<a[^>]+>(.*?)</a[^<]+'
    patron += '</h2>[^<]+'
    patron += '<div class="entry-meta"[^<]+'
    patron += '<a[^<]+<span[^<]+</span></a[^<]+</div[^<]+'
    patron += '<div class="entry-summary"[^<]+'
    patron += '<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedshow,scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedshow.strip()+" - "+scrapertools.htmlclean(scrapedtitle)
        title = title.strip()
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = scrapedplot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="telefe", url=url, thumbnail=thumbnail, fanart=thumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )


    '''
    <div id="post-9215" class="post-9215 post type-post status-publish format-standard hentry category-capitulos-completos">
    <h2 class="entry-title"><a href="http://dulceamor.telefe.com/2013/04/18/capitulo-295-hd/" title="Enlace permanente a Capítulo 295: (HD)" rel="bookmark">Capítulo 295: (HD)</a></h2>

    <img width="150" height="111" src="http://dulceamor.telefe.com/wp-content/blogs.dir/23/files/2013/04/Marcos-y-Victoria-150x111.jpg" class="attachment-loop-thumb wp-post-image" alt="Marcos y Victoria" title="Marcos y Victoria" />
    <div class="entry-summary">
    <p>VIDEO SÓLO VISIBLE EN ARGENTINA. Para visualizarlo recomendamos tener la última versión de Flash Player. Para bajarlo hacé click aquí Aire 17-04-13 &nbsp; &nbsp;</p>
    </div><!-- .entry-summary -->

    <div class="entry-utility">
    Publicado el <a href="http://dulceamor.telefe.com/2013/04/18/capitulo-295-hd/" title="9:52" rel="bookmark"><span class="entry-date">18 abril, 2013</span></a>                                   <span class="cat-links">
    en <a href="http://dulceamor.telefe.com/capitulos-completos/" title="Ver todas las entradas en Capítulos Completos HD" rel="category tag">Capítulos Completos HD</a>                    </span>
    <span class="meta-sep">|</span>
    <span class="comments-link"><a href="http://dulceamor.telefe.com/2013/04/18/capitulo-295-hd/#comments" title="Comentarios en Capítulo 295: (HD)">119 comentarios</a></span>
    </div><!-- .entry-utility -->
    </div>

    '''
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<h2 class="entry-title"><a href="([^"]+)" title="[^"]+" rel="bookmark">([^<]+)</a></h2>[^<]+'
    patron += '<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail in matches:
        scrapedtitle = title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="telefe", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    # Si no hay vídeos cambia http://dulceamor.telefe.com/ por http://dulceamor.telefe.com/capitulos-completos/
    if len(itemlist)==0:
        try:
            capitulos_completos_url = scrapertools.get_match(data,'<a href="(http\://[a-z0-9\.]+/capitulos-completos/)"')
            item.url = capitulos_completos_url
            itemlist = videos(item)
        except:
            pass

    # Patron alternativo
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<a href="([^"]+)" title="[^"]+" rel="bookmark"><img width="\d+" height="\d+" src="([^"]+)"[^<]+</a></h2>[^<]+'
    patron += '<h2 class="entry-title"><a[^<]+>([^<]+)</a></h2>[^<]+'
    patron += '<div class="entry-meta">[^<]+'
    patron += '<a[^<]+<span[^<]+</span></a>[^<]+</div>[^<]+'
    patron += '<div class="entry-summary">(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,thumbnail,title,plot in matches:
        scrapedtitle = title
        scrapedplot = scrapertools.htmlclean(plot)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="telefe", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    # Si aún así no hay vídeos...
    # Cambia: http://www.telefe.com/programas/am/
    # Por: http://www.telefe.com/am/
    if len(itemlist)==0 and "programas" in item.url:
        item.url = item.url.replace("/programas/","/")
        itemlist = videos(item)

    patron = '<a href="([^"]+)" >\&laquo\; Anterior</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl = matches[0]
        scrapedtitle = "!Página siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot) )

    return itemlist
