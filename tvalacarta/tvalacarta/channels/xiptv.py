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
    logger.info("[xiptv.py] mainlist")
    itemlist=[]
    itemlist.append( Item( channel=CHANNELNAME , title="Todos los programas"      , action="programas" , url="http://www.xiptv.cat/programes" ))
    itemlist.append( Item( channel=CHANNELNAME , title="Programas por categorías" , action="categorias" , url="http://www.xiptv.cat/programes" ))
    return itemlist

def categorias(item):
    logger.info("[xiptv.py] categorias")
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
    logger.info("[xiptv.py] programas")
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
        title = scrapedtitle+" ("+scrapedcategory+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot).strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=url, page=url , thumbnail=thumbnail, fanart=thumbnail, plot=plot , show=title , category = "programas" , folder=True) )

    # Página siguiente
    patron = '<a href="([^"]+)">next</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="programas" , url=urlparse.urljoin(item.url,match), folder=True) )

    return itemlist

def episodios(item):
    import urllib
    logger.info("[xiptv.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
    <li>
    <div class="item">
    <div class="image drop-shadow curved curved-hz-1 ">
    <a href="/ba-ba/capitol/passeig-amb-barca"><img alt="Hidden_7_27611_imagen_23_infantils" src="/media/asset_publics/resources/000/042/488/video/HIDDEN_7_27611_IMAGEN_23_infantils.jpg?1321639096" /></a>
    </div>
    <div class="archived"><em>històric</em></div>
    <div class="content">
    <span class="date">
    19/08/2010    
    </span>
    <h4>
    <a href="/ba-ba/capitol/passeig-amb-barca">Passeig amb barca</a>
    </h4>
    <h5><a href="/ba-ba">Ba-ba</a></h5>
    <span class="duration">05:12</span>
    <span class="views">119 reproduccions</span>
    <p>Un passeig amb barca pel mar pot ser tota una aventura!</p>
    '''
    patron  = '<li>[^<]+'
    patron += '<div class="item">[^<]+'
    patron += '<div class="[^<]+'
    patron += '<a href="([^"]+)"><img alt="[^"]+" src="([^"]+)".*?'
    patron += '<div class="content">[^<]+'
    patron += '<span class="date">([^<]+)</span>[^<]+'
    patron += '<h4>[^<]+'
    patron += '<a href="[^"]+">([^>]+)</a>[^<]+'
    patron += '</h4>.*?'
    patron += '<span class="duration">([^<]+)</span>[^<]+'
    patron += '<span class="views">[^<]+</span>[^<]+'
    patron += '<p>([^>]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,fecha,scrapedtitle,duracion,scrapedplot in matches:
        title = scrapedtitle + " ("+fecha.strip()+") ("+duracion.strip()+")"
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapedplot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="xiptv", url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot , show=item.show , category = item.category , folder=False) )

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
