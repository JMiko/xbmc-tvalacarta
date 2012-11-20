# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriespepito
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriespepito"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriespepito"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"        , title="Novedades", url="http://www.seriespepito.com/nuevos-capitulos/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="lomasvisto"        , title="Lo más visto", url="http://www.seriespepito.com/nuevos-capitulos/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"   , title="Listado alfabético",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))
    itemlist.append( Item(channel=__channel__, action="allserieslist"    , title="Listado completo",    url="http://www.seriespepito.com/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def novedades(item):
    logger.info("[seriespepito.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="lista_series">(.*?)</ul>')
    
    patron  = '<li>[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += "<img src='([^']+)'[^>]+>(.*?)</li>"

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodelist" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=scrapedtitle, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def lomasvisto(item):
    logger.info("[seriespepito.py] lomasvisto")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'Lo mas visto de Pepito[^<]+</div>[^<]+<ul class=\'nav\'>(.*?)</ul>')
    patron  = '<li>[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += "<img src='([^']+)'[^>]+>(.*?)</li>"

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        logger.info("title="+scrapedtitle)
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = title.replace("\r","").replace("\n","")
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        logger.info("title="+title)

        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodelist" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=scrapedtitle, viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def allserieslist(item):
    logger.info("[seriespepito.py] allserieslist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,"<ul class='nav' id='lista_completa_series_ul'>(.*?)</ul>")
    patron = "<li><a href='([^']+)'>([^<]+)</a></li>"

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = unicode( match[1].strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Ajusta el encoding a UTF-8
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")

        itemlist.append( Item(channel=__channel__, action="episodelist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def listalfabetico(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="0-9",url="http://www.seriespepito.com/lista-series-num/"))
    for letra in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title=letra,url="http://www.seriespepito.com/lista-series-"+letra.lower()+"/",fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def alphaserieslist(item):
    logger.info("[seriespepito.py] alphaserieslist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul class="lista_series">(.*?)</ul>')

    patron = '<li><a href="([^"]+)" title="([^"]+)"><img src=\'([^\']+)\''
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodelist" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=scrapedtitle,viewmode="movie", fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist


def detalle_programa(item,data=""):
    if data=="":
        data = scrapertools.cachePage(item.url)
    
    data2 = scrapertools.get_match(data,'<div class="noticia_cuerpo clearfix">(.*?)</div>')

    # Thumbnail
    patron  = '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data2)
    if len(matches)>0 and item.thumbnail=="":
        item.thumbnail = matches[0].replace("%20"," ")

    # Argumento
    item.plot = scrapertools.htmlclean(data2)

    return item

def episodelist(item):
    logger.info("[seriespepito.py] list")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Completa plot y thumbnail
    item = detalle_programa(item,data)
    
    data = scrapertools.get_match(data,"<ul class='nav_lista_capitulos'>(.*?)<br")
    logger.info(data)

    # Extrae los capítulos
    '''
    <li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-15/' title='Capitulo 15'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x15 - Capitulo 15</a>
    <span class='flag flag_vo'></span><span class='flag flag_vos'></span></li><li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-16/' title='Capitulo 16'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x16 - Capitulo 16</a>
    <span class='flag flag_vo'></span><span class='flag flag_vos'></span></li><li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-17/' title='Capitulo 17'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x17 - Capitulo 17</a>
    <span class='flag flag_vo'></span><span class='flag flag_vos'></span></li><li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-18/' title='Capitulo 18'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x18 - Capitulo 18</a>
    <span class='flag flag_vo'></span><span class='flag flag_vos'></span></li><li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-19/' title='Capitulo 19'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x19 - Capitulo 19</a>
    <span class='flag flag_vo'></span><span class='flag flag_vos'></span></li><li><a  href='http://hart-of-dixie.seriespepito.com/capitulos-primera-temporada-1/capitulo-20/' title='Capitulo 20'><i class='icon-film'></i> Hart of dixie (Doctora en Alabama) 1x20 - Capitulo 20</a>
    '''
    patron  = "<li><a\s+href='([^']+)'[^>]+>"
    patron += "<i[^<]+</i>"
    patron += "([^<]+)</a>(.*?)</li>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for scrapedurl,scrapedtitle,idiomas in matches:
        title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        if "flag_es" in idiomas:
            title = title + " (Español)"
        if "flag_vo'" in idiomas:
            title = title + " (VO)"
        if "flag_vos" in idiomas:
            title = title + " (VOS)"
        url = scrapedurl
        thumbnail = item.thumbnail
        plot = item.plot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, show=item.show))

    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodelist", show=item.show,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg", viewmode="movie_with_plot"))

    return itemlist

def findvideos(item):
    logger.info("[seriespepito.py] findvideos")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    '''
    <tr><td><div class='flag flag_es'></div></td><td>16/09/2012</td><td><img src='http://nowvideo.eu/favicon.ico' width='16px' height='16px' style='border:0;background:none; margin:0 3px 0 0; padding:0' >
    <b>nowvideo.eu</b></td><td><a class='btn btn-mini enlace_link' href='http://www.nowvideo.eu/video/50565ad5b8843' target='_blank' rel='nofollow' alt=''><i class='icon-play'></i> Ver</a></td><td>kubik</td><td></td></tr><tr><td>
    '''
    # Listas de enlaces
    patron  = "<tr><td><div class='([^']+')></div></td>"
    patron += "<td>[^<]+</td>"
    patron += "<td><img src='([^']+)'[^>]+>"
    patron += "<b>([^<]+)</b></td><td><a class='[^']+' href='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for idiomas,scrapedthumbnail,servidor,scrapedurl in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = "Ver en "+servidor
        plot = ""

        if "flag_es" in idiomas:
            title = title + " (Español)"
        if "flag_vo'" in idiomas:
            title = title + " (VO)"
        if "flag_vos" in idiomas:
            title = title + " (VOS)"

        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False,fanart="http://pelisalacarta.mimediacenter.info/fanart/seriespepito.jpg"))

    return itemlist

def play(item):
    logger.info("[seriespepito.py] play")
    itemlist=[]
    
    data = scrapertools.cache_page(item.url)
    
    videoitemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in videoitemlist:
        if not "favicon" in videoitem.url:
            videoitem.title = "Mirror %d%s" % (i,videoitem.title)
            videoitem.fulltitle = item.fulltitle
            videoitem.channel=channel=__channel__
            itemlist.append(videoitem)
            i=i+1

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    series_items = novedades(mainlist_items[0])
    bien = False
    for serie_item in series_items:
        episode_items = episodelist( item=serie_item )

        for episode_item in episode_items:
            mediaurls = findvideos( episode_item )
            if len(mediaurls)>=0 and len( play(mediaurls[0]) )>0:
                return True

    return False