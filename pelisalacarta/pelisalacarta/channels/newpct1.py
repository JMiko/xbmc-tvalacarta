# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct1
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
__title__ = "newpct1"
__channel__ = "newpct1"
__language__ = "ES"
__creationdate__ = "20141102"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newpct1.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="submenu", title="Películas", url="http://www.newpct1.com/peliculas/") )
    itemlist.append( Item(channel=__channel__, action="submenu", title="Series", url="http://www.newpct1.com/series/") )
    itemlist.append( Item(channel=__channel__, action="search", title="Buscar") )

    return itemlist

def search(item,texto):
    logger.info("[newpct1.py] search")
    #categoryIDR=767&categoryID=1343&idioma=&calidad=HDTV+720p+AC3+5.1&ordenar=Fecha&inon=Descendente&q=Boardwalk+Empire
    item.url = "http://www.newpct1.com/index.php?page=buscar&q=%s&ordenar=Nombre&inon=Ascendente" % texto

    return busqueda(item)

def busqueda(item):
    logger.info("[newpct1.py] busqueda")
    itemlist=[]

    data = re.sub(r'\n|\r|\t|\s{2}|<!--.*?-->|<i class="icon[^>]+"></i>',"",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="buscar-list">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "><img src="http://www.newpct1.com/pictures/f/minis/40669_x-men-primera-generacion--.jpg" alt="Descargar DVDScreener X-Men Primera Generacion "></a> <div class="info"><a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "><h2 style="padding:0;">X-Men Primera Generacion [DVD Screener][Spanish][2011]</h2> </a><span class="votadas">6.50</span><span>08-07-2011</span><span>1.9 GB</span><span class="color"> <a href="http://www.newpct1.com/descargar/x-men-primera-generacion/40669/" title="Descargar DVDScreener X-Men Primera Generacion "> Descargar</a> </div> </li>

    #<li><a href="http://www.newpct1.com/serie/the-big-bang-theory-/capitulo-811/" title="Descargar Serie HD The Big Bang Theory - Temporada 88x11"><img src="http://www.newpct1.com/pictures/c/minis/1869_the-big-bang-theory-.jpg" alt="Descargar Serie HD The Big Bang Theory - Temporada 8 "></a> <div class="info"><a href="http://www.newpct1.com/serie/the-big-bang-theory-/capitulo-811/" title="Descargar Serie HD The Big Bang Theory - Temporada 88x11"><h2 style="padding:0;"><strong style="color:red;background:none;"><font color='blue'><b><font color='blue'><b>The Big</b></font></b></font> Bang Theory - Temporada 8 </strong>- Temporada <span style="color:red;background:none;">[ 8 ]</span> Capitulo <span style="color:red;background:none;">[ 11 ] &nbsp;&nbsp;Español Castellano </span> Calidad  <span style="color:red;background:none;">[ HDTV 720p AC3 5.1 ]</span></h2> </a><span class="votadas"> <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star-empty"></i><i class="icon-star-empty"></i>6.50</span><span>20-12-2014</span><span>750 MB</span><span class="color"> <a href="http://www.newpct1.com/serie/the-big-bang-theory-/capitulo-811/" title="Descargar Serie HD The Big Bang Theory - Temporada 88x11"><i class="icon-cloud-download"></i> Descargar</a> </div> </li>

    patron  = '<img src="([^"]+)".*?'
    patron += '<a href="([^"]+)".*?'
    patron += '<h2[^>]*>(.*?)</h2> </a>'
    patron += '<span class="votadas">([^<]+)</span>'
    patron += '<span>([^<]+)</span>'
    patron += '<span>([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedthumbnail,scrapedurl,scrapedtitle,votos,fecha,peso in matches:
        url = scrapedurl
        scrapedtitle = re.sub(r'(<.*?>)','',scrapedtitle)
        title = scrapedtitle+"["+votos+"]["+fecha+"]["+peso+"]"
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="busqueda" , title=">> Página siguiente" , url=url_next_page))

    return itemlist

def submenu(item):
    logger.info("[newpct1.py] submenu")
    itemlist=[]

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    #<li><a href="http://www.newpct1.com/peliculas/"><i class="icon-facetime-video"></i> Peliculas</a><ul><li><a href="http://www.newpct1.com/peliculas/" title="Peliculas en Castellano" >Peliculas Castellano</a></li><li><a href="http://www.newpct1.com/peliculas-latino/" title="Peliculas Latino">Peliculas Latino</a></li><li><a href="http://www.newpct1.com/estrenos-de-cine/" title="Estrenos de Cine">Estrenos de Cine</a></li><li><a href="http://www.newpct1.com/peliculas-hd/" title="Peliculas HD">Peliculas HD</a></li><li><a href="http://www.newpct1.com/peliculas-3d/" title="Peliculas en 3D" >Peliculas en 3D</a></li><li><a href="http://www.newpct1.com/otras-peliculas/" title="Otras Peliculas">Otras Peliculas</a></li><li><a href="http://www.newpct1.com/peliculas-vo/" title="Peliculas Subtituladas">Peliculas Subtituladas</a></li><li><a href="http://www.newpct1.com/anime/" title="Anime">Anime</a></li></ul></li>

    patron = '<li><a href="'+item.url+'">.*?<ul>(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    print "#### Newpct1 submenu #########################################"
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = scrapedurl
        print "title = %s" % title
        print "url = %s" % url
        itemlist.append( Item(channel=__channel__, action="listado" ,title=title, url=url, extra="pelilist") )
        itemlist.append( Item(channel=__channel__, action="alfabeto" ,title=title+" [A-Z]", url=url, extra="pelilist") )
    print "##############################################################"
    
    return itemlist

def alfabeto(item):
    logger.info("[newpct1.py] alfabeto")
    itemlist = []

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="alfabeto">(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)"[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.upper()
        url = scrapedurl

        itemlist.append( Item(channel=__channel__, action="completo" ,title=title, url=url, extra=item.extra) )

    return itemlist

def listado(item):
    logger.info("[newpct1.py] listado")
    itemlist = []

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="'+item.extra+'">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/pelicula/x-men-dias-del-futuro-pasado/ts-screener/" title="Descargar XMen Dias Del Futuro gratis"><img src="http://www.newpct1.com/pictures/f/58066_x-men-dias-del-futuro--blurayrip-ac3-5.1.jpg" width="130" height="180" alt="Descargar XMen Dias Del Futuro gratis"><h2>XMen Dias Del Futuro </h2><span>BluRayRip AC3 5.1</span></a></li>

    patron  = '<a href="([^"]+)"[^>]+>'
    patron += '<img src="([^"]+)"[^>]+>'
    patron += '<h2[^>]*>([^<]+)</h2>'
    patron += '<span>([^<]*)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedurl,scrapedthumbnail,scrapedtitle,calidad in matches:
        url = scrapedurl
        title = scrapedtitle+calidad
        thumbnail = scrapedthumbnail
        action = "findvideos"
        if "1.com/series" in url: action = "episodios"
        itemlist.append( Item(channel=__channel__, action=action, title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="listado" , title=">> Página siguiente" , url=url_next_page, extra=item.extra))

    return itemlist

def episodios(item):
    logger.info("[newpct1.py] episodios")
    itemlist=[]

    data = re.sub(r'\n|\r|\t|\s{2}|<!--.*?-->|<i class="icon[^>]+"></i>',"",scrapertools.cache_page(item.url))
    data = re.sub(r'\[Cap[^\]]+\]',"",data)
    #data = re.sub(r'</span> Calidad|</span></h2></a>',"",data)
    #data = re.sub(r'Serie <strong style="color:red;background:none;">[^<]+</strong>[^<]+<span style="color:red;background:none;">[^<]+</span>[^<]+<span style="color:red;background:none;">[^<]+</span>',"[",data)

    #data = data.replace('</span> Calidad <span style="color:red;background:none;">',']')

    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="buscar-list">(.*?)</ul>'
    fichas = scrapertools.get_match(data,patron)

    #fichas1 = fichas.replace('</li>','</li>\n')

    #print "## fichas: %s\n" % (fichas1)

    #<li><a href="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-603/" title="Serie The Big Bang Theory 6x03"><img src="http://www.newpct1.com/pictures/c/minis/1092_the-big-bang-theory.jpg" alt="Serie The Big Bang Theory 6x03"></a> <div class="info"> <a href="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-603/" title="Serie The Big Bang Theory 6x03"><h2 style="padding:0;">Serie <strong style="color:red;background:none;">The Big Bang Theory - Temporada 6 </strong> - Temporada<span style="color:red;background:none;">[ 6 ]</span>Capitulo<span style="color:red;background:none;">[ 03 ]</span><span style="color:red;background:none;padding:0px;">Español Castellano</span> Calidad <span style="color:red;background:none;">[ HDTV ]</span></h2></a> <span>02-11-2012</span> <span>225 MB</span> <span class="color"><ahref="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-603/" title="Serie The Big Bang Theory 6x03"> Descargar</a> </div></li>

    #<li><a href="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-602/" title="Serie The Big Bang Theory 6x00"><img src="http://www.newpct1.com/pictures/c/minis/1092_the-big-bang-theory.jpg" alt="Serie The Big Bang Theory 6x00"></a> <div class="info"> <a href="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-602/" title="Serie The Big Bang Theory 6x00"><h2 style="padding:0;">The Big Bang Theory - Temporada 6 [HDTV][Español Castellano]</h2></a> <span>26-10-2012</span> <span>230 MB</span> <span class="color"><ahref="http://www.newpct1.com/serie/the-big-bang-theory/capitulo-602/" title="Serie The Big Bang Theory 6x00"> Descargar</a> </div></li>

    patron  = '<a href="([^"]+)" title="([^"]+)">'
    patron += '<img src="([^"]+)".*?'
    patron += '(<h2 style="padding:0;">.*?)</a> '
    patron += '<span>([^<]+)</span> '
    patron += '<span>([^<]+)</span>'

    matches = re.compile(patron,re.DOTALL).findall(fichas)

    for scrapedurl,scrapedtitle,scrapedthumbnail,idioma_calidad,fecha,peso in matches:

        try:
            print "### [newpct1] episodios.for.try ### idioma_calidad: %s" % (idioma_calidad)
            patron = '<span style=".*?0px;">([^<]+)</span>'
            idioma = scrapertools.get_match(idioma_calidad, patron)
            patron = '<span style=".*?none;">([^<]+)</span>'
            calidad = scrapertools.get_match(idioma_calidad, patron)
        except:
            print "### [newpct1] episodios.for.except ### idioma_calidad: %s" % (idioma_calidad)
            patron = '\[[^\]]+\](\[[^\]]+\])'
            idioma = scrapertools.get_match(idioma_calidad, patron)
            patron = '(\[[^\]]+\])\[[^\]]+\]'
            calidad = scrapertools.get_match(idioma_calidad, patron)

        #capt = scrapedurl[:-2]
        #print "## capt: %s" % (capt)
        #title = scrapedtitle[:-1]+capt
        #print "## title: %s" % (title)

        url = scrapedurl
        title = scrapedtitle+" "+idioma+" "+calidad+"[ "+fecha+" ][ "+peso+" ]"
        thumbnail = scrapedthumbnail
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title, url=url, thumbnail=thumbnail) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)

        #print "### paginacion: %s\n" % (paginacion)

        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^"]+)">Next</a>')
            itemlist.append( Item(channel=__channel__, action="episodios" , title=">> Página siguiente" , url=url_next_page))

    return itemlist

def findvideos(item):
    logger.info("[newpct1.py] findvideos")
    itemlist=[]

    ## Cualquiera de las tres opciones son válidas
    #item.url = item.url.replace("1.com/","1.com/ver-online/")
    #item.url = item.url.replace("1.com/","1.com/descarga-directa/")
    item.url = item.url.replace("1.com/","1.com/descarga-torrent/")

    # Descarga la página
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    title = scrapertools.find_single_match(data,"<h1><strong>([^<]+)</strong>[^<]+</h1>")
    title+= scrapertools.find_single_match(data,"<h1><strong>[^<]+</strong>([^<]+)</h1>")
    caratula = scrapertools.find_single_match(data,'<div class="entry-left">.*?src="([^"]+)"')

    #<a href="http://tumejorjuego.com/download/index.php?link=descargar-torrent/058310_yo-frankenstein-blurayrip-ac3-51.html" title="Descargar torrent de Yo Frankenstein " class="btn-torrent" target="_blank">Descarga tu Archivo torrent!</a>

    patron = '<a href="([^"]+)" title="[^"]+" class="btn-torrent" target="_blank">'

    # escraped torrent
    url = scrapertools.find_single_match(data,patron)
    if url!="":
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title+" [torrent]", fulltitle=title, url=url , thumbnail=caratula, plot=item.plot, folder=False) )

    # escraped ver vídeos, descargar vídeos un link, múltiples liks
    data = data.replace("'",'"')
    data = data.replace('javascript:;" onClick="popup("http://www.newpct1.com/pct1/library/include/ajax/get_modallinks.php?links=',"")
    data = data.replace("http://tumejorserie.com/descargar/url_encript.php?link=","")
    data = data.replace("$!","#!")

    patron_descargar = '<div id="tab2"[^>]+>.*?</ul>'
    patron_ver = '<div id="tab3"[^>]+>.*?</ul>'

    match_ver = scrapertools.find_single_match(data,patron_ver)
    match_descargar = scrapertools.find_single_match(data,patron_descargar)

    patron = '<div class="box1"><img src="([^"]+)".*?' # logo
    patron+= '<div class="box2">([^<]+)</div>'         # servidor
    patron+= '<div class="box3">([^<]+)</div>'         # idioma
    patron+= '<div class="box4">([^<]+)</div>'         # calidad
    patron+= '<div class="box5"><a href="([^"]+)".*?'  # enlace
    patron+= '<div class="box6">([^<]+)</div>'         # titulo

    enlaces_ver = re.compile(patron,re.DOTALL).findall(match_ver)
    enlaces_descargar = re.compile(patron,re.DOTALL).findall(match_descargar)

    for logo, servidor, idioma, calidad, enlace, titulo in enlaces_ver:
        servidor = servidor.replace("played","playedto")
        titulo = titulo+" ["+servidor+"]"
        itemlist.append( Item(channel=__channel__, action="play", server=servidor, title=titulo , fulltitle = item.title, url=enlace , thumbnail=logo , plot=item.plot , folder=False) )

    for logo, servidor, idioma, calidad, enlace, titulo in enlaces_descargar:
        servidor = servidor.replace("uploaded","uploadedto")
        partes = enlace.split(" ")
        p = 1
        for enlace in partes:
            parte_titulo = titulo+" (%s/%s)" % (p,len(partes)) + " ["+servidor+"]"
            p+= 1
            itemlist.append( Item(channel=__channel__, action="play", server=servidor, title=parte_titulo , fulltitle = item.title, url=enlace , thumbnail=logo , plot=item.plot , folder=False) )

    return itemlist

def completo(item):
    logger.info("[newpct1.py] completo")
    itemlist = []

    # Guarda el valor por si son etquitas para que lo vea 'listadofichas'
    item_extra = item.extra

    # Lee las entradas
    items_programas = listado(item)

    salir = False
    while not salir:

        # Saca la URL de la siguiente página
        ultimo_item = items_programas[ len(items_programas)-1 ]

        # Páginas intermedias
        if ultimo_item.action=="listado":
            # Quita el elemento de "Página siguiente" 
            ultimo_item = items_programas.pop()

            # Añade las entradas de la página a la lista completa
            itemlist.extend( items_programas )
    
            # Carga la sigiuente página
            ultimo_item.extra = item_extra
            items_programas = listado(ultimo_item)

        # Última página
        else:
            # Añade a la lista completa y sale
            itemlist.extend( items_programas )
            salir = True

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    submenu_items = submenu(mainlist_items[0])
    listado_items = listado(submenu_items[0])
    for listado_item in listado_items:
        play_items = findvideos(listado_item)
        
        if len(play_items)>0:
            return True

    return False