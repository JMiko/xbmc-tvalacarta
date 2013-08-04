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

    '''
    <div class="shows-menu"><ul id="menu-shows" class="menu"><li id="menu-item-72715" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-72715"><a href="#">Programas</a>
    <ul class="sub-menu">
        <li id="menu-item-62998" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-62998"><a href="http://www.telefe.com/aliados/">Aliados</a></li>
        <li id="menu-item-51867" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-51867"><a href="http://www.telefe.com/am/">AM</a></li>
        <li id="menu-item-51884" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-51884"><a href="http://telefenoticias.com.ar/es/tusnoticieros/bairesdirecto/index.shtml">Baires Directo</a></li>
        <li id="menu-item-51868" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-51868"><a href="http://www.telefe.com/casadosconhijos/">Casados con hijos</a></li>
        <li id="menu-item-65786" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-65786"><a href="http://www.telefe.com/celebritysplash/">Celebrity Splash</a></li>
        <li id="menu-item-51888" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-51888"><a href="http://telefenoticias.com.ar/tusnoticieros/diariodemedianoche/">Diario de Medianoche</a></li>
    </ul>
    </ul></div></div></div>
    '''
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="shows-menu">(.*?)</div></div></div>')
    
    patron  = '<li[^<]+<a href="(http\://www.telefe.com/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="secciones" , url=url, thumbnail=thumbnail, plot=plot , show=scrapedtitle, folder=True) )

    # Añade aparte los de las series antiguas, que tienen otro formato
    itemlist.append( Item(channel=CHANNELNAME, action="videos_site_especial", title="La dueña", url="http://laduena.telefe.com/capitulos-completos/", thumbnail="", folder=True))
    itemlist.append( Item(channel=CHANNELNAME, action="videos_site_especial", title="Dulce amor", url="http://dulceamor.telefe.com/capitulos-completos/", thumbnail="", folder=True))
    itemlist.append( Item(channel=CHANNELNAME, action="videos_site_especial", title="El elegido", url="http://elelegido.telefe.com/resumenes/", thumbnail="", folder=True))
    itemlist.append( Item(channel=CHANNELNAME, action="videos_site_especial", title="Los graduados", url="http://losgraduados.telefe.com/category/capitulos/", thumbnail="", folder=True))

    return itemlist

def secciones(item):
    logger.info("[telefe.py] secciones")
    
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    id_programa = scrapertools.get_match(item.url,"http\://www.telefe.com/(.*?)/")

    #href="/am/?taxonomy=tipo&term=exclusivo-web"
    patron  = 'href="/'+id_programa+'/\?taxonomy\=tipo\&term\=([a-z0-9\-]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        title = match.replace("-"," ").capitalize()
        url = 'http://www.telefe.com/'+id_programa+'/?taxonomy=tipo&term='+match
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="videos" , url=url, thumbnail=thumbnail, plot=plot , show=item.title, folder=True) )

    url = 'http://www.telefe.com/'+id_programa+'/?type=chrono'
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los videos" , action="videos" , url=url, show=item.title, folder=True) )

    return itemlist

def videos(item):
    logger.info("[telefe.py] videos")
    
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    
    patron = '<div id="post-\d+"[^<]+(.*?)</div[^<]+</div[^<]+</div[^<]+</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:

        '''
        <div class="entry-data">
        <div class="entry-media">
        <a href="http://www.telefe.com/2012/11/20/am-i-como-las-prefieren-los-hombres/"
        title="Enlace permanente a AM I ¿Cómo las prefieren los hombres?"
        rel="bookmark"><img width="200" height="112" src="http://www.telefe.com/wp-content/blogs.dir/10/files/2012/11/UAAE7432-874-200x112.jpg" class="attachment-thumb-16:9-33% wp-post-image" alt="UAAE7432-874" title="&lt;i&gt;AM&lt;/i&gt; I ¿Cómo las prefieren los hombres?" /> </a>
        </div>

        <h2 class="entry-title">
        <a href="http://www.telefe.com/2012/11/20/am-i-como-las-prefieren-los-hombres/"
        title="Enlace permanente a AM I ¿Cómo las prefieren los hombres?"
        rel="bookmark"><i>AM</i> I ¿Cómo las prefieren los hombres? </a>
        </h2>
        '''

        try:
            scrapedshow = scrapertools.get_match(match,'<div class="entry-category"[^<]+<a[^>]+>([^"]+)</a[^<]+')
        except:
            scrapedshow = ""

        try:
            scrapedurl = scrapertools.get_match(match,'<div class="entry-media[^<]+<a href="([^"]+)"')
        except:
            scrapedurl = ""

        try:
            scrapedthumbnail = scrapertools.get_match(match,'<div class="entry-media[^<]+<a href="[^"]+"[^<]+<img width="[^"]+" height="[^"]+" src="([^"]+)"')
        except:
            scrapedthumbnail = ""

        try:
            scrapedtitle = scrapertools.get_match(match,'<h2 class="entry-title"[^<]+<a[^>]+>(.*?)</h2')
        except:
            scrapedtitle = ""

        try:
            scrapedplot = scrapertools.get_match(match,'<div class="entry-summary"[^<]+<p>([^<]+)</p>')
        except:
            scrapedplot = ""

        if scrapedurl!="":
            title = scrapedshow.strip()+" - "+scrapertools.htmlclean(scrapedtitle)
            title = title.strip()
            url = scrapedurl
            thumbnail = scrapedthumbnail
            plot = scrapedplot
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
            itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="telefe", url=url, thumbnail=thumbnail, fanart=thumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    try:
        next_page = scrapertools.get_match(data,"<span class='current'>[^<]+</span><a href='([^']+)'")
        next_page = next_page.replace("#038;","&")
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="videos" , url=urlparse.urljoin(item.url,next_page) , folder=True ) )
    except:
        pass

    return itemlist

def videos_site_especial(item):
    logger.info("[telefe.py] videos")
    
    itemlist=[]

    # Patron alternativo
    data = scrapertools.cache_page(item.url)
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

    try:
        next_page = scrapertools.get_match(data,'<div class="nav-previous"><a href="([^"]+)"')
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="videos_site_especial" , url=next_page, folder=True) )
    except:
        pass

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # El canal tiene estructura programas -> episodios -> play
    items_mainlist = mainlist(Item())
    items_programas = []

    # Todas las opciones del menu tienen que tener algo
    for item_mainlist in items_mainlist:
        exec "itemlist="+item_mainlist.action+"(item_mainlist)"
    
        if len(itemlist)==0:
            print "La sección '"+item_mainlist.title+"' no devuelve nada"
            return False

        if item_mainlist.action=="programas":
            items_programas = itemlist

    # Ahora recorre los programas hasta encontrar vídeos en alguno
    for item_programa in items_programas:
        print "Verificando "+item_programa.title
        items_secciones = secciones(item_programa)

        for item_seccion in items_secciones:
            items_videos = videos(item_seccion)
            if len(items_videos)>0:
                return True

    print "No hay videos en ningún programa"
    return False
