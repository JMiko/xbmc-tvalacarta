# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para descargacineclasico
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribuci�n de ermanitu
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "descargacineclasico"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Descarga Cine Cl�sico"
__language__ = "ES"

DEBUG = config.get_setting("debug")
MAIN_URL = "http://descargacineclasico.com/"

LoadThumbnails = True # indica si cargar los carteles

def isGeneric():
    return True

def mainlist(item):
    logger.info("[animeid.py] mainlist")
    
    url = MAIN_URL
    itemlist = []
 
    # Extrae los enlaces a las categorias
    data = scrapertools.cachePage(url)
    patron = "<img src='http://.*?GENEROS.png'/>(.*?)</div>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
    
    patronvideos  = "<a.*?href\='(http://descargacineclasico.blogspot.com/search/label/[^']+)'.*?>([^<]+)<"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))
    
    return itemlist

def peliculas(item):
    logger.info("[descargacineclasico.py] peliculas")

    itemlist = []

    # Extrae las pel�culas
    data = scrapertools.cachePage(item.url)
    '''
    <div class='post hentry'>
    <a name='1324211669208744702'></a>
    <h3 class='post-title entry-title'>
    <a href='http://descargacineclasico.blogspot.com/2009/06/la-bruja-novata.html'>La bruja novata</a>
    </h3>
    <div class='post-header'>
    <div class='post-header-line-1'></div>
    </div>
    
    <div class='post-body entry-content'>
    <div id='summary1324211669208744702'><div style="text-align: justify;"><div style="text-align: justify;"><div class="separator" style="clear: both; text-align: center;"><a href="http://4.bp.blogspot.com/_qv-B-qobdi0/THZ_Xg59eAI/AAAAAAAAFBA/W2v6LriMzsQ/s1600/La+bruja+novata.+DESCARGA+CINE+CLASICO.jpg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="400" src="http://4.bp.blogspot.com/_qv-B-qobdi0/THZ_Xg59eAI/AAAAAAAAFBA/W2v6LriMzsQ/s400/La+bruja+novata.+DESCARGA+CINE+CLASICO.jpg" width="241" /></a></div><div style="text-align: center;"><br />
    </div><div style="text-align: center;">T�TULO ORIGINAL: Bedknobs &amp; Broomsticks (Bedknobs and Broomsticks)</div><div style="text-align: center;">A�O: 1971  </div><div style="text-align: center;">DURACI�N: 117 min.  </div><div style="text-align: center;">PA�S:[Estados Unidos]  </div><div style="text-align: center;">DIRECTOR: Robert Stevenson</div><div style="text-align: center;">GUI�N: Bill Walsh &amp; Don DaGradi (Historia: Marry Norton)</div><div style="text-align: center;">M�SICA: Richard M. Sherman &amp; Robert B. Sherman</div><div style="text-align: center;">FOTOGRAF�A : Frank Phillips</div><div style="text-align: center;"><br />
    
    </div><div style="font-family: Georgia,&quot;Times New Roman&quot;,serif; text-align: center;"><b>REPARTO:&nbsp;</b></div><div style="text-align: center;">Angela Lansbury, David Tomlinson, Roddy McDowall, Sam Jaffe, John Ericson, Tessie O'Shea</div><div style="text-align: center;">PRODUCTORA: Walt Disney</div><div style="text-align: center;">PREMIOS: 1971: Oscar: Mejores efectos visuales. 5 nominaciones</div><div style="text-align: center;">G�NERO: Fant�stico. Comedia. Infantil. Animaci�n | Magia</div><div style="text-align: center;"><br />
    </div><div style="font-family: Georgia,&quot;Times New Roman&quot;,serif; text-align: center;"><b>SINOPSIS:  </b></div><div style="text-align: center;">La estricta y severa Eglantine Price (Angela Lansbury) es una bruja aficionada que tiene que hacerse cargo, muy a su pesar, de 3 ni�os que han sido evacuados al peque�o pueblo costero donde ella vive. Juntos deber�n luchar contra el invasor alem�n, empleando para ello todos los trucos de Eglantine. (FILMAFFINITY)</div></div><div style="font-family: Georgia,&quot;Times New Roman&quot;,serif; text-align: center;"><b><br />
    </b></div><div style="text-align: center;"><b style="font-family: Georgia,&quot;Times New Roman&quot;,serif;">Idioma: Castellano</b></div><div align="center"><b><span style="font-size: 130%;"><br />
    </span></b></div><b><br />
    </b><br />
    <div align="center"><b><b><span style="font-size: 130%;">&#187; Descarga en <a href="http://www.megaupload.com/?d=31UM0Z87" style="font-weight: bold;" target="_blank">MegaUpload</a></span></b></b></div><br />
    
    <b><br />
    </b><br />
    <div align="center"><b><b><span style="font-size: 130%;">&#187; Ver Online en <a href="http://www.megavideo.com/?d=31UM0Z87" style="font-weight: bold;" target="_blank">Megavideo</a></span></b></b></div></div></div>
    <script type='text/javascript'>createSummaryAndThumb("summary1324211669208744702");</script>
    <span class='rmlink' style='float:right'><a href='http://descargacineclasico.blogspot.com/2009/06/la-bruja-novata.html'>Leer m�s...</a></span>
    <div style='clear: both;'></div>
    </div>
    <div class='post-footer'>
    '''
    patronvideos  = "<div class='post hentry'>[^<]+"
    patronvideos += "<a[^>]+></a>[^<]+"
    patronvideos += "<h3[^>]+>[^<]+"
    patronvideos += "<a href='([^']+)'>([^>]+)</a>.*?"
    patronvideos += '<img.*?src="([^"]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0]) # url de la ficha descargacineclasico
        #scrapedthumbnail = match[2].replace("s200","s1600")
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si todo est� ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())

    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien