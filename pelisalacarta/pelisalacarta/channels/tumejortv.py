# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tumejortv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tumejortv"
__category__ = "F,S"
__type__ = "generic"
__title__ = "tumejortv.com"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tumejortv.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="submenu" , title="Películas"    , url="http://www.tumejortv.com/directorio/peliculas", extra="peliculas"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Películas VO" , url="http://www.tumejortv.com/directorio/peliculas_vo", extra="peliculas"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Series"       , url="http://www.tumejortv.com/directorio/series", extra="series"))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Series VO"    , url="http://www.tumejortv.com/directorio/series_vo", extra="series"))

    return itemlist

def search(item,texto):
    return []

def submenu(item):
    logger.info("[tumejortv.py] submenu")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action=item.extra        , title="Novedades"                  , url=item.url))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Todas por orden alfabético" , url=item.url, extra=item.extra))

    return itemlist

def alfabetico(item):
    logger.info("[tumejortv.py] alfabetico")
    
    itemlist=[]
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action=item.extra, title=str(letra), url = item.url + "/filtro_letras/"+letra))

    itemlist.append( Item(channel=item.channel, action=item.extra, title="0-9", url = item.url + "/filtro_letras/0"))

    return itemlist

# Listado de novedades de la pagina principal
def peliculas(item):
    logger.info("[tumejortv.py] peliculas")

    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las películas
    '''
    <div class="antlo_dir_all_container">
    <a rel="tag" href="http://www.tumejortv.com/peliculas/kika-Superbruja-El-Viaje-A-Mandolan--2012-/" class="antlo_dir_pic_container color1" alt="kika Superbruja El Viaje A Mandolan [2012]" title="kika Superbruja El Viaje A Mandolan [2012]">
    <div class="antlo_dir_bandera"><img src="http://www.tumejortv.com/images/flags/f_estrenos_dvd.png" alt="kika Superbruja El Viaje A Mandolan [2012]" title="kika Superbruja El Viaje A Mandolan [2012]"/></div>
    <div class="antlo_dir_img_container"><img src="http://www.tumejortv.com/images/posters/jrUsuGVCAMxrPdan.jpeg" alt="kika Superbruja El Viaje A Mandolan [2012]"/>
    <div class="antlo_pic_more_info"><span class="color1">Película  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="Español" title="Español"/><img src="http://www.tumejortv.com/images/general/posee_trailer.png" alt="Trailer" title="Trailer" style="margin: 0 3px;"/></span></div></div><p>
    <div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span style="font-size:1px;color:#3E3E3E;">Película </span><br/> kika Superbruja El Viaje A Man...</h3>
    <span class="antlo_dir_video_cat">Aventuras</span><h5 class="antlo_dir_video_calidad">DVD-RIP AC3</h5>
    </div></p></a></div><div class="antlo_dir_all_container"><a rel="tag" href="http://www.tumejortv.com/peliculas/Chocolate--2012-/" class="antlo_dir_pic_container color1" alt="Chocolate [2012]" title="Chocolate [2012]"><div class="antlo_dir_bandera"><img src="http://www.tumejortv.com/images/flags/f_estrenos_dvd.png" alt="Chocolate [2012]" title="Chocolate [2012]"/></div><div class="antlo_dir_img_container"><img src="http://www.tumejortv.com/images/posters/7BFXjdiCqYE53yVW.jpeg" alt="Chocolate [2012]"/><div class="antlo_pic_more_info"><span class="color1">Película  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="Español" title="Español"/><img src="http://www.tumejortv.com/images/general/posee_trailer.png" alt="Trailer" title="Trailer" style="margin: 0 3px;"/></span></div></div>
    '''
    '''
    <div class="antlo_dir_all_container">
    <a rel="tag" href="http://www.tumejortv.com/peliculas/Hincame-el-diente/" class="antlo_dir_pic_container color1" alt="Híncame el diente [2010]" title="Híncame el diente [2010]">
    <div class="antlo_dir_bandera"><img src="http://www.tumejortv.com/images/flags/f_actualizado.png" alt="Híncame el diente [2010]" title="Híncame el diente [2010]"/></div>
    <div class="antlo_dir_img_container"><img src="http://www.tumejortv.com/images/posters/JzYbXhxAdj7Y2tYM.jpeg" alt="Híncame el diente [2010]"/>
    <div class="antlo_pic_more_info"><span class="color1">Película  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="Español" title="Español"/></span></div></div><p><div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span style="font-size:1px;color:#3E3E3E;">Película </span><br/> Híncame el diente [2010]</h3><span class="antlo_dir_video_cat">Comedia</span><h5 class="antlo_dir_video_calidad">DVD-RIP</h5></div></p></a></div>
    '''
    patron  = '<div class="antlo_dir_all_container">'
    patron += '<a rel="tag" href="([^"]+)" class="antlo_dir_pic_container color1"[^>]+>'
    patron += '<div class="antlo_dir_bandera"[^<]+<img[^<]+</div>'
    patron += '<div class="antlo_dir_img_container"><img src="([^"]+)"[^>]+>'
    patron += '<div class="antlo_pic_more_info"><span class="color1">([^>]+)<img src="[^"]+" alt="([^"]+)".*?</span></div></div><p>'
    patron += '<div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span[^>]+[^<]+</span><br/>([^<]+)</h3>'
    patron += '<span class="antlo_dir_video_cat">([^<]+)</span><h5 class="antlo_dir_video_calidad">([^<]+)</h5>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,tipo,idioma,titulo,categoria,calidad in matches:
        scrapedtitle = titulo+" ("+idioma.strip()+") ("+calidad+")"
        scrapedurl = url+"enlaces/"
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Ordena los listados alfabéticos
    if "filtro_letras" in item.url:
        itemlist = sorted(itemlist, key=lambda Item: Item.title)    

    # Extrae la página siguiente
    patron = '<a href="([^"]+)">SIGUIENTE</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedtitle = ">> Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def series(item,extended=True):
    logger.info("[tumejortv.py] series")

    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    '''
    <div class="antlo_dir_all_container">
    <a rel="tag" href="http://www.tumejortv.com/series/Chuck/" class="antlo_dir_pic_container color2" alt="Chuck" title="Chuck">
    <div class="antlo_dir_bandera"><img src="http://www.tumejortv.com/images/flags/f_estrenos_nuevo.png" alt="Chuck" title="Chuck"/></div>
    <div class="antlo_dir_img_container"><img src="http://www.tumejortv.com/images/posters/mqvyK6s4kzBvTYJq.jpeg" alt="Chuck"/>
    <div class="antlo_pic_more_info"><span class="color2">Serie  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="Español" title="Español"/><img src="http://www.tumejortv.com/images/general/posee_trailer.png" alt="Trailer" title="Trailer" style="margin: 0 3px;"/></span></div></div><p>
    <div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span style="font-size:1px;color:#3E3E3E;">Serie </span><br/> Chuck</h3>
    <h4 class="antlo_dir_video_cat">Temporada <span class="white">5</span> Capítulo <span class="white">2</span></h4>
    <h5 class="antlo_dir_video_calidad">HDTV</h5></div></p></a></div>
    '''
    '''
    <div class="antlo_dir_all_container">
    <a rel="tag" href="http://www.tumejortv.com/series/Ringer/" class="antlo_dir_pic_container color2" alt="Ringer" title="Ringer">
    <div class="antlo_dir_bandera"></div>
    <div class="antlo_dir_img_container"><img src="http://www.tumejortv.com/images/posters/2x5EyHacUHzJGmZ4.jpeg" alt="Ringer"/>
    <div class="antlo_pic_more_info"><span class="color2">Serie  <img src="http://www.tumejortv.com/images/idioma/antlo-es.png" alt="Español" title="Español"/>
    </span></div></div><p><div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span style="font-size:1px;color:#3E3E3E;">Serie </span><br/> Ringer</h3><h4 class="antlo_dir_video_cat">Temporada <span class="white">1</span> Capítulo <span class="white">10</span></h4><h5 class="antlo_dir_video_calidad">HDTV</h5></div></p></a></div>
    '''

    # Extrae las series
    patron  = '<div class="antlo_dir_all_container">'
    patron += '<a rel="tag" href="([^"]+)" class="antlo_dir_pic_container color[^"]+"[^>]+>'
    patron += '<div class="antlo_dir_bandera.*?</div>'
    patron += '<div class="antlo_dir_img_container"><img src="([^"]+)"[^>]+>'
    patron += '<div class="antlo_pic_more_info"><span class="[^"]+">([^>]+)<img src="[^"]+" alt="([^"]+)".*?</span></div></div><p>'
    patron += '<div class="antlo_dir_box_text_container"><h3 class="antlo_dir_video_title"><span[^<]+</span><br/>([^<]+)</h3>'
    patron += '<h4 class="antlo_dir_video_cat">(.*?)<h5 class="antlo_dir_video_calidad">([^<]+)</h5'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,tipo,idioma,titulo,categoria,calidad in matches:
        scrapedtitle = titulo.strip()
        if extended:
            scrapedtitle = scrapedtitle +" ("+idioma.strip()+") ("+scrapertools.htmlclean(calidad)+")"
        scrapedurl = url+"capitulos/"
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findepisodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=titulo))

    # Ordena los listados alfabéticos
    if "filtro_letras" in item.url:
        itemlist = sorted(itemlist, key=lambda Item: Item.title)    

    # Extrae la página siguiente
    patron = '<a href="([^"]+)">SIGUIENTE</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedtitle = ">> Pagina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def findvideos(item):
    logger.info("[tumejortv.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    
    from servers import servertools
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"
    
    patron = '<a title="[^>]+" href="(http://www.tumejortv.com/.*?/url/\d+)"[^>]+>([^<]+)</a></td><td>([^<]+)</td><td><img src="[^"]+" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,server,calidad,idioma in matches:
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=server.strip()+" ("+idioma+") ("+calidad+") -> En partes" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=True, fulltitle=item.title))

    return itemlist

def findepisodios(item):
    logger.info("[tumejortv.py] findvideos")
    
    itemlist=[]
    
    data = scrapertools.cache_page(item.url)
    #<a href="#" class="antlo_temporadas_li" title="Haga clic para ver listado de capítulos"><img src="http://www.tumejortv.com/images/general/more.png" /> TEMPORADA 1<span style="float:right;"><img src="http://www.tumejortv.com/images/general/estreno.png" alt="EstrenoT"/></span></a><div><table class="antlo_links_table">
    patron = '<a href="\#" class="antlo_temporadas_li" title="Haga clic[^"]+"><img[^>]+>( TEMPORADA [^<]+)<(.*?)</table>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for temporada,episodios in matches:
        
        patronepisodio = '<tr><td></td><td[^>]+><a title="[^"]+" alt="[^"]+" href="([^"]+)"> <img[^>]+><br />[^<]+</a></td><td>([^<]+)</td><td>([^<]+)</td><td><a[^>]+>([^<]+)</a></td></tr>'
        matches2 = re.compile(patronepisodio,re.DOTALL).findall(episodios)
        for url,episodio,num_enlaces,titulo in matches2:
            temporada = temporada.replace("TEMPORADA","").strip()
            if len(episodio)<2:
                episodio = "0"+episodio
            itemlist.append( Item(channel=__channel__, action="findvideos" , title=temporada+"x"+episodio+" "+titulo+" ("+num_enlaces+" enlaces)" , url=url, thumbnail=item.thumbnail, show=item.show, plot=item.plot, folder=True, fulltitle=item.title))

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="findepisodios", show=item.show) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    submenu_items = submenu(mainlist_items[0])
    peliculas_items = peliculas(submenu_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien