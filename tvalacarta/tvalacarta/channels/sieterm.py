# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para 7rm
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("tvalacarta.channels.sieterm init")

DEBUG = False
CHANNELNAME = "sieterm"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.sieterm mainlist")

    itemlist = []
    #itemlist.append( Item(channel=CHANNELNAME, title="Últimos vídeos añadidos" , url="" , action="novedades" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , url="http://www.7rm.es/servlet/rtrm.servlets.ServletLink2?METHOD=LSTBLOGALACARTA&sit=c,6&serv=BlogPortal2&orden=2" , action="programas" , folder=True) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.sieterm programas")

    itemlist = []
    data = scrapertools.cachePage(item.url)
    
    # Extrae las entradas (carpetas)
    patron  = '<dt class="alacarta-video">[^<]+'
    patron += '<a href="([^"]+)">([^<]+)</a>[^<]+'
    patron += '</dt>[^<]+'
    patron += '<dd style="height:100%;overflow:hidden;">[^<]+'
    patron += '<a[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a>([^<]+)</dd>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    for match in matches:
        # Atributos del vídeo
        scrapedtitle = unicode( match[1].strip() , "iso-8859-1" , errors="ignore").encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,match[0]).replace("&amp;","&")
        scrapedthumbnail = urlparse.urljoin(item.url,match[2]).replace("&amp;","&")
        scrapedplot = unicode( match[3].strip() , "iso-8859-1" , errors="ignore").encode("utf-8")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , viewmode="movie_with_plot", folder=True ) )

    # Busca la página siguiente
    pagina_siguiente = scrapertools.find_single_match(data,'<a class="list-siguientes" href="([^"]+)" title="Ver siguientes a la cartas">Siguiente</a>')
    if pagina_siguiente!="":
        pagina_siguiente = urlparse.urljoin(item.url,pagina_siguiente)
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="programas" , url=pagina_siguiente , folder=True) )

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.sieterm episodios")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae los vídeos
    '''
    <dt class="alacarta-video"><a href="http://..." title="...">Murcianos por el mundo: Cracovia</a> · 12/05/2010 · (5411 veces visto)</dt>
    <dd style="height:100%; overflow:hidden">
    <a href="http://www.7rm.es/servlet/rtrm.servlets.ServletLink2?METHOD=DETALLEALACARTA&amp;sit=c,6,ofs,10&amp;serv=BlogPortal2&amp;orden=1&amp;idCarta=40&amp;mId=4182&amp;autostart=TV" title="Ver v&iacute;deo">
    <img src="http://mediateca.regmurcia.com/MediatecaCRM/ServletLink?METHOD=MEDIATECA&amp;accion=imagen&amp;id=4182" alt="Murcianos por el mundo: Cracovia" title="Murcianos por el mundo: Cracovia" style="width:95px" />
    </a>
    Esta semana nos desplazamos al sur de Polonia, a Cracovia y Wroclaw, para conocer cómo viven seis murcianos en una de las ciudades más importantes de Polonia y Patrimonio de la Humanidad.
    <a href="http://ficheros.7rm.es:3025/Video/4/1/4182_BAJA.mp4">
    <img src="/images/bajarArchivo.gif" alt="Descargar Archivo" title="Descargar Archivo" style="margin:0;padding:0 5px 0 0;vertical-align:middle;border:none" />
    </a>
    </dd>
    '''
  
    '''
    <dt class="alacarta-video"><a href="http://www.7rm.es/servlet/rtrm.servlets.ServletLink2?METHOD=DETALLEALACARTA&amp;sit=c,6,ofs,0&amp;serv=BlogPortal2&amp;orden=2&amp;idCarta=36&amp;mId=3214&amp;autostart=TV" title="Ver v&iacute;deo">De la tierra al mar</a> · 22/12/2009 · (1072 veces visto)</dt>
    <dd style="height:100%; overflow:hidden">
    <a href="http://www.7rm.es/servlet/rtrm.servlets.ServletLink2?METHOD=DETALLEALACARTA&amp;sit=c,6,ofs,0&amp;serv=BlogPortal2&amp;orden=2&amp;idCarta=36&amp;mId=3214&amp;autostart=TV" title="Ver v&iacute;deo">
    <img src="http://mediateca.regmurcia.com/MediatecaCRM/ServletLink?METHOD=MEDIATECA&amp;accion=imagen&amp;id=3214" alt="De la tierra al mar" title="De la tierra al mar" style="width:95px" />
    </a>
    En este programa conocemos a Plácido, joven agricultor que nos mostrará la mala situación en que se encuentra el sector, informamos de la campaña 'Dale vida a tu árbol', asistimos a la presentación del libro 'Gestión ambiental. Guía fácil para empresas y profesionales', y nos hacemos eco del malestar de nuestros agricultores con la nueva normativa europea en materia de fitosanitarios, que entrará en vigor en junio de 2011.
    <a href="http://ficheros.7rm.es:3025/Video/3/2/3214_BAJA.mp4">
    <img src="/images/bajarArchivo.gif" alt="Descargar Archivo" title="Descargar Archivo" style="margin:0;padding:0 5px 0 0;vertical-align:middle;border:none" />
    </a>
    </dd>
    '''
    patron  = '<dt class="alacarta-video"><a href="([^"]+)" title="[^"]+">([^<]+)</a>.*?([0-9\/]+).*?</dt>[^<]+'
    patron += '<dd style="[^<]+">[^<]+'
    patron += '<a href="[^"]+" title="[^"]+">[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a>([^<]+)<a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        # Atributos del vídeo
        scrapedtitle = unicode( match[1].strip()+" ("+match[2]+")" , "iso-8859-1" , errors="ignore").encode("utf-8")
        scrapedurl = urlparse.urljoin(item.url,match[5]).replace("&amp;","&")
        scrapedthumbnail = urlparse.urljoin(item.url,match[3]).replace("&amp;","&")
        scrapedplot = unicode( match[4].strip()  , "iso-8859-1" , errors="ignore").encode("utf-8")
        scrapedpage = urlparse.urljoin(item.url,match[0]).replace("&amp;","&")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="directo" , url=scrapedurl, thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot , show = item.show , page=scrapedpage, viewmode="movie_with_plot", folder=False) )

    patron = '<a class="list-siguientes" href="([^"]+)" title="Ver siguientes archivos">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        # Atributos del vídeo
        scrapedtitle = ">> Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show = item.show , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    menuitem = mainlist(Item())[0]
    # El canal tiene estructura programas -> episodios -> play
    programas_itemlist = programas(menuitem)
    if len(programas_itemlist)==0:
        return False

    print "Episodios de "+programas_itemlist[1].tostring()
    episodios_itemlist = episodios(programas_itemlist[1])
    if len(episodios_itemlist)==0:
        return False

    return bien
