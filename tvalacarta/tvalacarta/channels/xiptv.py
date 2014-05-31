# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para xip/tv
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

DEBUG = False
CHANNELNAME = "xiptv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.xiptv mainlist")
    itemlist=[]
    itemlist.append( Item( channel=CHANNELNAME , title="Últimos vídeos añadidos"  , action="episodios" , url="http://www.xiptv.cat/capitols" , folder=True) )
    itemlist.append( Item( channel=CHANNELNAME , title="Televisiones locales"     , action="cadenas" , url="http://www.xiptv.cat" ))
    itemlist.append( Item( channel=CHANNELNAME , title="Todos los programas"      , action="programas" , url="http://www.xiptv.cat/programes" ))
    itemlist.append( Item( channel=CHANNELNAME , title="Programas por categorías" , action="categorias" , url="http://www.xiptv.cat/programes" ))
    return itemlist

def cadenas(item):
    logger.info("tvalacarta.channels.xiptv cadenas")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<a href="#">Televisions locals</a>(.*?)</div>')

    # Extrae las categorias (carpetas)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="cadena" , url=url, folder=True) )

    return itemlist

def cadena(item):
    logger.info("tvalacarta.channels.xiptv cadena")
    itemlist=[]
    itemlist.append( Item( channel=CHANNELNAME , title="Últimos vídeos añadidos a "+item.title  , action="episodios" , url=urlparse.urljoin(item.url,"/capitols") , folder=True) )
    itemlist.append( Item( channel=CHANNELNAME , title="Todos los programas de "+item.title      , action="programas" , url=urlparse.urljoin(item.url,"/programes") ))
    return itemlist

def categorias(item):
    logger.info("tvalacarta.channels.xiptv categorias")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<select id="program_program_categories" name="program.program_categories.">(.*?)</select>')

    # Extrae las categorias (carpetas)
    patron = '<option value="([^"]+)">([^>]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        #http://www.xiptv.cat/programes?program%5Bfull_text%5D=&program%5Bprogram_categories%5D=Infantils&program%5Bhistoric%5D=1&commit=Cercar
        url = "http://www.xiptv.cat/programes?program%5Bfull_text%5D=&program%5Bprogram_categories%5D="+scrapedurl+"&program%5Bhistoric%5D=1&commit=Cercar"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="programas" , url=url, folder=True) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.xiptv programas")
    itemlist=[]
    
    # Extrae los programas
    data = scrapertools.cache_page(item.url)
    '''
    <li>
    <div class="item">
    <div class="image drop-shadow curved curved-hz-1">
    <a href="/diaridelamusica-com"><img alt="Diari-de-la-musica" src="/media/asset_publics/resources/000/067/941/program/diari-de-la-musica.jpg?1321662172" /></a>
    </div>
    <div class="content">
    <h4><a href="/diaridelamusica-com">Diaridelamúsica.com</a></h4>
    <h5>
    <a href="/programes?model_type=Program&amp;program%5Bprogram_categories%5D=Cultura">Cultura</a>
    </h5>
    <p>Diaridelamusica.com, dóna tota la informació sobre l'estat de l'escena musical al país. És un espai dinàmic i proper que genera a parts iguals un racó informatiu del succeït en clau musical a tot el nostre territori i també del que ha d'arribar.
    L’espai té un format modern i atrevit que se serveix en càpsules i busca la concertació amb els agen...</p>
    <span class="chapters">
    423 capítols
    </span>
    <dl>
    <dt>TV responsable</dt>
    <dd>m1tv</dd>
    <dt>Categoria</dt>
    <dd>
    <a href="/programes?model_type=Program&amp;program%5Bprogram_categories%5D=Cultura">Cultura</a>
    </dd>    
    </dl>
    </div>
    </div>
    </li>
    '''
    patron  = '<li>[^<]+'
    patron += '<div class="item">[^<]+'
    patron += '<div class="[^<]+'
    patron += '<a href="([^"]+)"><img alt="[^"]+" src="([^"]+)".*?'
    patron += '<div class="content">[^<]+'
    patron += '<h4><a href="[^"]+">([^>]+)</a></h4>[^<]+'
    patron += '<h5>[^<]+'
    patron += '<a[^>]+>([^>]+)</a>[^<]+'
    patron += '</h5>[^<]+'
    patron += '<p>([^>]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedcategory,scrapedplot in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedcategory+"\n"+scrapedplot).strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="episodios" , url=url, page=url , thumbnail=thumbnail, fanart=thumbnail, plot=plot , show=title , category = "programas" , viewmode="movie_with_plot", folder=True) )

    # Página siguiente
    patron = '<a href="([^"]+)">next</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="programas" , url=urlparse.urljoin(item.url,match), folder=True) )

    return itemlist

def episodios(item):
    import urllib
    logger.info("tvalacarta.channels.xiptv episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
    <li>
    <div class="item">
    <div class="image drop-shadow curved curved-hz-1 ">
    <a href="/la-setmana-catalunya-central/capitol/capitol-30"><img alt="Imatge_pgm30" src="/media/asset_publics/resources/000/180/341/video/imatge_pgm30.jpg?1396620287" /></a>
    </div>
    <div class="content">
    <span class="date">
    04/04/2014
    </span>
    <h4>
    <a href="/la-setmana-catalunya-central/capitol/capitol-30">Capítol 30</a>
    </h4>
    <p><h5><a href="/la-setmana-catalunya-central" target="_blank">La setmana Catalunya central</a> </h5>
    </p>
    <span class="duration">25:02</span>
    <span class="views">0 reproduccions</span>
    <p>Al llarg dels segle XIX el Seminari de Vic va anar forjant una col·lecció de Ciències Naturals que representa, a dia d’avui, un valuós testimoni històric. Al programa d’avui coneixerem el nou destí de les peces que integren aquesta col·lecció i quin és el seu nou destí: integrar-se al fons del Museu del Ter de Manlleu. En aquesta edició de ‘La S...</p>
    <div class="related">
    '''
    patron = '<li[^<]+<div class="item">(.*?)<div class="related">'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        fecha = scrapertools.find_single_match(match,'<span class="date">([^<]+)</span>').strip()
        duracion = scrapertools.find_single_match(match,'<span class="duration">([^<]+)</span>').strip()
        titulo_programa = scrapertools.find_single_match(match,'<p><h5><a[^>]+>([^<]+)</a>').strip()
        titulo_episodio = scrapertools.find_single_match(match,'<h4[^<]+<a[^>]+>([^<]+)</a>').strip()
        scrapedurl = scrapertools.find_single_match(match,'<h4[^<]+<a href="([^"]+)"')
        scrapedthumbnail = scrapertools.find_single_match(match,'<img alt="[^"]+" src="([^"]+)"')
        scrapedplot = scrapertools.find_single_match(match,'<p>([^<]+)</p>').strip()

        title = scrapertools.htmlclean(titulo_programa + " - " + titulo_episodio + " (" + fecha + ") (" + duracion + ")")
        url = urlparse.urljoin( item.url , scrapedurl )
        thumbnail = urlparse.urljoin( item.url , scrapedthumbnail )
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="xiptv", url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot , show=item.show , category = item.category , viewmode="movie_with_plot", folder=False) )

    # Página siguiente
    patron = '<a href="([^"]+)">next</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="episodios" , url=urlparse.urljoin(item.url,match), folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # Todas las opciones tienen que tener algo
    items = mainlist(Item())
    programas_items = programas(items[0])
    if len(programas_items)==0:
        return False

    episodios_items = episodios(programas_items[0])
    if len(episodios_items)==0:
        return False

    return bien
