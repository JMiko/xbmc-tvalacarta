# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelis24"
__category__ = "F,S"
__type__ = "xbmc"
__title__ = "Pelis24"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelis24.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades"     , action="peliculas", url="http://pelis24.com/index.php"))
    itemlist.append( Item(channel=__channel__, title="Estrenos" , action="peliculas", url="http://pelis24.com/estrenos/"))
    itemlist.append( Item(channel=__channel__, title="Recientes" , action="peliculas", url="http://pelis24.com/index.php?do=lastnews"))
    itemlist.append( Item(channel=__channel__, title="HD 720p" , action="peliculas", url="http://pelis24.com/hd/"))
    itemlist.append( Item(channel=__channel__, title="HD 480p" , action="peliculas", url="http://pelis24.com/peliculas480p/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas en Castellano" , action="peliculas", url="http://pelis24.com/pelicula-ca/"))
    itemlist.append( Item(channel=__channel__, title="Peliculas 3D" , action="peliculas", url="http://pelis24.com/pelicula-3d"))
    return itemlist

def peliculas(item):
    logger.info("[pelis24.py] peliculas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    bloque = scrapertools.get_match(data,"<div id='dle-content'>(.*?)<div id=\"sidebar\" class=\"lcol\"")

    '''
    <div id='dle-content'>
    <a href="http://www.pelis24.com/peliculas/688-siempre-a-tu-lado-hachiko-espanol-online.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/pel029020.jpg" width="145" height="211" alt="Siempre a tu lado, Hachiko (2009)" title="Siempre a tu lado, Hachiko (2009)"/><noscript><img src="http://imgs24.com/images/pel029020.jpg" width="145" height="211" alt="Siempre a tu lado, Hachiko (2009)" title="Siempre a tu lado, Hachiko (2009)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-latino/14538-madly-madagascar-2013.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/madlymadag.jpg" width="145" height="211" alt="Madly Madagascar (2013)" title="Madly Madagascar (2013)"/><noscript><img src="http://imgs24.com/images/madlymadag.jpg" width="145" height="211" alt="Madly Madagascar (2013)" title="Madly Madagascar (2013)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/estrenos/14537-movie-43-2013.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/movie43car.jpg" width="145" height="211" alt="Movie 43 (2013)" title="Movie 43 (2013)"/><noscript><img src="http://imgs24.com/images/movie43car.jpg" width="145" height="211" alt="Movie 43 (2013)" title="Movie 43 (2013)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/hd/14536-soldado-anunimo-jarhead-el-infierno-espera-2006.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/f3867.jpg" width="145" height="211" alt="Soldado Anónimo / Jarhead, el infierno espera (2006)" title="Soldado Anónimo / Jarhead, el infierno espera (2006)"/><noscript><img src="http://imgs24.com/images/f3867.jpg" width="145" height="211" alt="Soldado Anónimo / Jarhead, el infierno espera (2006)" title="Soldado Anónimo / Jarhead, el infierno espera (2006)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-latino/14535-rno-mnstico-2003.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/mysticrive.jpg" width="145" height="211" alt="Río Místico (2003)" title="Río Místico (2003)"/><noscript><img src="http://imgs24.com/images/mysticrive.jpg" width="145" height="211" alt="Río Místico (2003)" title="Río Místico (2003)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-ca/13502-el-joven-bruce-lee-2010-castellano.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://www.pelis24.com/uploads/posts/2012-05/1337890744_eljovenbruceleeportada.jpg" width="145" height="211" alt="El joven Bruce Lee (2010)" title="El joven Bruce Lee (2010)"/><noscript><img src="http://www.pelis24.com/uploads/posts/2012-05/1337890744_eljovenbruceleeportada.jpg" width="145" height="211" alt="El joven Bruce Lee (2010)" title="El joven Bruce Lee (2010)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/hd/14534-el-rey-leun-3-hakuna-matata-2004.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/001elrbtb.jpg" width="145" height="211" alt="El rey león 3 - Hakuna Matata (2004)" title="El rey león 3 - Hakuna Matata (2004)"/><noscript><img src="http://imgs24.com/images/001elrbtb.jpg" width="145" height="211" alt="El rey león 3 - Hakuna Matata (2004)" title="El rey león 3 - Hakuna Matata (2004)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/hd/14533-el-rey-leun-2-el-tesoro-de-simba-1998.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/001elreyle.jpg" width="145" height="211" alt="El Rey León 2 - El tesoro de Simba (1998)" title="El Rey León 2 - El tesoro de Simba (1998)"/><noscript><img src="http://imgs24.com/images/001elreyle.jpg" width="145" height="211" alt="El Rey León 2 - El tesoro de Simba (1998)" title="El Rey León 2 - El tesoro de Simba (1998)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/hd/14532-el-rey-leun-1994.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/elreyleon1.jpg" width="145" height="211" alt="El rey león (1994)" title="El rey león (1994)"/><noscript><img src="http://imgs24.com/images/elreyleon1.jpg" width="145" height="211" alt="El rey león (1994)" title="El rey león (1994)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculas/13076-blancanieves-y-la-leyenda-del-cazador-2012-trailer-subtitulado.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/blancapwg.jpg" width="145" height="211" alt="Blancanieves y la leyenda del cazador (2012)" title="Blancanieves y la leyenda del cazador (2012)"/><noscript><img src="http://imgs24.com/images/blancapwg.jpg" width="145" height="211" alt="Blancanieves y la leyenda del cazador (2012)" title="Blancanieves y la leyenda del cazador (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculasvose/1080-un-ciudadano-ejemplar-espanol-online.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/unciuduyu.jpg" width="145" height="211" alt="Un ciudadano ejemplar / El Vengador (2009)" title="Un ciudadano ejemplar / El Vengador (2009)"/><noscript><img src="http://imgs24.com/images/unciuduyu.jpg" width="145" height="211" alt="Un ciudadano ejemplar / El Vengador (2009)" title="Un ciudadano ejemplar / El Vengador (2009)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/estrenos/14531-hansel-gretel-cazadores-de-brujas-2013.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/nt12hansel.jpg" width="145" height="211" alt="Hansel & Gretel: Cazadores de brujas (2013)" title="Hansel & Gretel: Cazadores de brujas (2013)"/><noscript><img src="http://imgs24.com/images/nt12hansel.jpg" width="145" height="211" alt="Hansel & Gretel: Cazadores de brujas (2013)" title="Hansel & Gretel: Cazadores de brujas (2013)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-ca/14530-blancanieves-2012.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/blancanvn.jpg" width="145" height="211" alt="Blancanieves (2012)" title="Blancanieves (2012)"/><noscript><img src="http://imgs24.com/images/blancanvn.jpg" width="145" height="211" alt="Blancanieves (2012)" title="Blancanieves (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-ca/14360-en-la-mente-del-asesino-alex-cross-2012.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/32814769e7.jpg" width="145" height="211" alt="En la mente del asesino (Alex Cross) (2012)" title="En la mente del asesino (Alex Cross) (2012)"/><noscript><img src="http://imgs24.com/images/32814769e7.jpg" width="145" height="211" alt="En la mente del asesino (Alex Cross) (2012)" title="En la mente del asesino (Alex Cross) (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculasvose/12776-immortals-2011-subtitulado.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/11335xgog.jpg" width="145" height="211" alt="Immortals (2011)" title="Immortals (2011)"/><noscript><img src="http://imgs24.com/images/11335xgog.jpg" width="145" height="211" alt="Immortals (2011)" title="Immortals (2011)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculas/14202-el-atlas-de-las-nubes-2012-trauler-subtitulado.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/cloudatlas.jpg" width="145" height="211" alt="El atlas de las nubes (2012)" title="El atlas de las nubes (2012)"/><noscript><img src="http://imgs24.com/images/cloudatlas.jpg" width="145" height="211" alt="El atlas de las nubes (2012)" title="El atlas de las nubes (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculas/14171-skyfall-james-bond-23-2012-trailer-subtitulado.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/skyfallfin.jpg" width="145" height="211" alt="Skyfall (James Bond 23) (2012)" title="Skyfall (James Bond 23) (2012)"/><noscript><img src="http://imgs24.com/images/skyfallfin.jpg" width="145" height="211" alt="Skyfall (James Bond 23) (2012)" title="Skyfall (James Bond 23) (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/peliculasvose/14138-cosmopolis-2012.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/cosmopopx.jpg" width="145" height="211" alt="Cosmopolis (2012)" title="Cosmopolis (2012)"/><noscript><img src="http://imgs24.com/images/cosmopopx.jpg" width="145" height="211" alt="Cosmopolis (2012)" title="Cosmopolis (2012)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/pelicula-ca/14529-promesas-del-este-2007.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/promesasde.jpg" width="145" height="211" alt="Promesas del Este (2007)" title="Promesas del Este (2007)"/><noscript><img src="http://imgs24.com/images/promesasde.jpg" width="145" height="211" alt="Promesas del Este (2007)" title="Promesas del Este (2007)"/></noscript></a>&nbsp;&nbsp;
    <a href="http://www.pelis24.com/hd/14528-prometheus-2012.html"><img style="display:none;visibility:hidden;" data-cfsrc="http://imgs24.com/images/prometwrw.jpg" width="145" height="211" alt="Prometheus (2012)" title="Prometheus (2012)"/><noscript><img src="http://imgs24.com/images/prometwrw.jpg" width="145" height="211" alt="Prometheus (2012)" title="Prometheus (2012)"/></noscript></a>&nbsp;&nbsp;
	<div class="dpad">
	<div class="basenavi">
		<div class="navigation"><span>1</span> <a href="http://www.pelis24.com/estrenos/page/2/">2</a> <a href="http://www.pelis24.com/estrenos/page/3/">3</a> <a href="http://www.pelis24.com/estrenos/page/4/">4</a> <a href="http://www.pelis24.com/estrenos/page/5/">5</a> <a href="http://www.pelis24.com/estrenos/page/6/">6</a> <a href="http://www.pelis24.com/estrenos/page/7/">7</a> <a href="http://www.pelis24.com/estrenos/page/8/">8</a> <a href="http://www.pelis24.com/estrenos/page/9/">9</a> <a href="http://www.pelis24.com/estrenos/page/10/">10</a> </div>
		<div class="nextprev">
			<span><span class="thide pprev">Anterior</span></span>
			<a href="http://www.pelis24.com/estrenos/page/2/"><span class="thide pnext">Siguiente</span></a>
		</div>
'''
    patron = '<a href="([^"]+)" ><img src="([^"]+)" width="[^"]+" height="[^"]+" alt="[^"]+" title="([^"]+)"/></a>&nbsp;&nbsp;'



    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    # Extrae el paginador
    patronvideos  = '<span>[^<]+</span>[^<]+<a href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
