# -*- coding: utf-8 -*-
#------------------------------------------------------------
# sipeliculas.com - XBMC Plugin
# Canal para sipeliculas.com by juso
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "sipeliculas"
__category__ = "F"
__type__ = "generic"
__title__ = "Si peliculas"
__language__ = "ES"
__creationdate__ = "20120301"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[sipeliculas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Peliculas recientes" , action="lista2", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado por Generos" , action="generos", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Listado Alfabetico" , action="alfa", url="http://www.sipeliculas.com/"))
    itemlist.append( Item(channel=__channel__, title="Buscar pelicula" , action="search", url=""))
 
    return itemlist

def search(item,texto):
    logger.info("[sipeliculas.py] search")
    itemlist = []

    texto = texto.replace(" ","+")
    item.url="http://www.sipeliculas.com/Buscar.php?q="+texto    
    item.extra = ""
    itemlist.extend(lista1(item))
    
    return itemlist

def alfa(item):
    logger.info("[sipeliculas.py] alfabetico")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patron='<div id="abc">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data=matches[0]
    patron='<a .*? href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="lista2", url=scrapedurl)) 
    return itemlist

def generos(item):
    logger.info("[sipeliculas.com] generos")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,"<li><span>CATEGORIAS</span></li>(.*?)</ul>")

    patron='<a  href="([^"]+)".*?>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=unicode( match[1], "iso-8859-1" , errors="replace" ).encode("utf-8")
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="lista2", url=scrapedurl)) 
    return itemlist

def lista1(item):
    logger.info("[sipeliculas.py] lista1")
    itemlist=[]
    data = scrapertools.cachePage(item.url)   
    patron = '<div id="CEN">\n<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        scrapedurl=match[0]
        scrapedtitle=match[1]
        scrapedthumbnail=match[2]
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="mirrors", url=scrapedurl, thumbnail=scrapedthumbnail))

    patron='class="PaginaActual".*?href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapedurl='http://www.sipeliculas.com'+matches[0];
    scrapedurl=scrapedurl.replace('./','/')
    itemlist.append( Item(channel=__channel__, title="! Pagina Siguiente" , action="lista1", url=scrapedurl))
    #itemlist.append( Item(channel=__channel__, title=matchx , action="lista2", url=matchx)) 
    return itemlist

def lista2(item):
    logger.info("[sipeliculas.py] lista2")
    itemlist=[]
    data = scrapertools.cachePage(item.url)   
    bloque = scrapertools.get_match(data,'<ul id="pelis">(.*?)</ul>')
    '''
    <ul id="pelis"><li><a class="lk" title="hada por accidente" href="http://www.sipeliculas.com/ver_4180_hada-por-accidente.html"></a><em></em><i><a class="Ytrailer" href="XhyWDy5TQhI" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359491390.jpg" alt=""/></div><h3>Hada por accidente</h3> <span><a href="http://www.sipeliculas.com/categoria_comedia.html">Comedia</a> <a href="http://www.sipeliculas.com/categoria_aventura.html">Aventura</a>  / 2010</span> </li><li><a class="lk" title="la sirenita 2" href="http://www.sipeliculas.com/ver_4179_la-sirenita-2.html"></a><em></em><i><a class="Ytrailer" href="q9T5PqCaje8" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359490351.jpg" alt=""/></div><h3>La sirenita 2</h3> <span><a href="http://www.sipeliculas.com/categoria_animacion.html">Animación</a> <a href="http://www.sipeliculas.com/categoria_aventura.html">Aventura</a> <a href="http://www.sipeliculas.com/categoria_musical.html">Musical</a>  / 2000</span> </li><li><a class="lk" title="la sirenita" href="http://www.sipeliculas.com/ver_4178_la-sirenita.html"></a><em></em><i><a class="Ytrailer" href="e7SSyCMitfc" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359489703.jpg" alt=""/></div><h3>La sirenita</h3> <span><a href="http://www.sipeliculas.com/categoria_animacion.html">Animación</a> <a href="http://www.sipeliculas.com/categoria_aventura.html">Aventura</a> <a href="http://www.sipeliculas.com/categoria_comedia.html">Comedia</a>  / 1989</span> </li><li><a class="lk" title="vertigo" href="http://www.sipeliculas.com/ver_4177_vertigo.html"></a><em></em><i><a class="Ytrailer" href="pV9yYSu6qA4" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359489195.jpg" alt=""/></div><h3>Vertigo</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a> <a href="http://www.sipeliculas.com/categoria_suspense.html">Suspense</a> <a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a>  / 2009</span> </li><li><a class="lk" title="survival of the dead" href="http://www.sipeliculas.com/ver_4176_survival-of-the-dead.html"></a><em></em><i><a class="Ytrailer" href="AxnNhe27liE" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359487635.jpg" alt=""/></div><h3>Survival of the dead</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a> <a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a>  / 2009</span> </li><li><a class="lk" title="the abandoned" href="http://www.sipeliculas.com/ver_4175_the-abandoned.html"></a><em></em><i><a class="Ytrailer" href="OCmzqrD-G48" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359486713.jpg" alt=""/></div><h3>The abandoned</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a> <a href="http://www.sipeliculas.com/categoria_intriga.html">Intriga</a>  / 2006</span> </li><li><a class="lk" title="el diablo viste a la moda" href="http://www.sipeliculas.com/ver_4174_el-diablo-viste-a-la-moda.html"></a><em></em><i><a class="Ytrailer" href="VVFcOtIbkCo" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359485919.jpg" alt=""/></div><h3>El diablo viste a la moda</h3> <span><a href="http://www.sipeliculas.com/categoria_comedia.html">Comedia</a> <a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a>  / 2006</span> </li><li><a class="lk" title="los miserables" href="http://www.sipeliculas.com/ver_4173_los-miserables.html"></a><em></em><i><a class="Ytrailer" href="RrRGLwAUZ0Y" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359485417.jpg" alt=""/></div><h3>Los miserables</h3> <span><a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a> <a href="http://www.sipeliculas.com/categoria_musical.html">Musical</a>   / 2012</span> </li><li><a class="lk" title="the grudge" href="http://www.sipeliculas.com/ver_4172_the-grudge.html"></a><em></em><i><a class="Ytrailer" href="Kn7odLVy1yo" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359484670.jpg" alt=""/></div><h3>The grudge</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a> <a href="http://www.sipeliculas.com/categoria_intriga.html">Intriga</a>  / 2004</span> </li><li><a class="lk" title="espejos siniestros" href="http://www.sipeliculas.com/ver_4171_espejos-siniestros.html"></a><em></em><i><a class="Ytrailer" href="M4v-K7eVxr4" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359414796.jpg" alt=""/></div><h3>Espejos siniestros</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a>  / 2008</span> </li><li><a class="lk" title="django: sin cadenas" href="http://www.sipeliculas.com/ver_4170_django-sin-cadenas.html"></a><em></em><i><a class="Ytrailer" href="6pKZbJHa17c" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/1359136452.jpg" alt=""/></div><h3>Django: sin cadenas</h3> <span><a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a> <a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a>  / 2012</span> </li><li><a class="lk" title="el doble del diablo" href="http://www.sipeliculas.com/ver_4169_el-doble-del-diablo.html"></a><em></em><i><a class="Ytrailer" href="vFzsXlPnt_s" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/el-doble-del-diablo.jpg" alt=""/></div><h3>El doble del diablo</h3> <span><a href="http://www.sipeliculas.com/categoria_intriga.html">Intriga</a> <a href="http://www.sipeliculas.com/categoria_aventura.html">Aventura</a>  / 2012</span> </li><li><a class="lk" title="no" href="http://www.sipeliculas.com/ver_4168_no.html"></a><em></em><i><a class="Ytrailer" href="osEE7ldHx4I" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/no.jpg" alt=""/></div><h3>No</h3> <span><a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a>  / 2012</span> </li><li><a class="lk" title="la venganza de wyatt earp" href="http://www.sipeliculas.com/ver_4167_la-venganza-de-wyatt-earp.html"></a><em></em><i><a class="Ytrailer" href="FCXpJbke-Y0" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/la-venganza-de-wyatt-earp.png" alt=""/></div><h3>La venganza de wyatt earp</h3> <span><a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a>  / 2012</span> </li><li><a class="lk" title="el atlas de las nubes" href="http://www.sipeliculas.com/ver_4166_el-atlas-de-las-nubes.html"></a><em></em><i><a class="Ytrailer" href="qcqufhbcjL0" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/el-atlas-de-las-nubes.jpg" alt=""/></div><h3>El atlas de las nubes</h3> <span><a href="http://www.sipeliculas.com/categoria_ciencia-ficcion.html">Ciencia Ficción</a> <a href="http://www.sipeliculas.com/categoria_drama.html">Drama</a>  / 2012</span> </li><li><a class="lk" title="the collection" href="http://www.sipeliculas.com/ver_4165_the-collection.html"></a><em></em><i><a class="Ytrailer" href="n08aIH-Bhcc" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/the-collection.jpg" alt=""/></div><h3>The collection</h3> <span><a href="http://www.sipeliculas.com/categoria_terror.html">Terror</a> <a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a>  / 2012</span> </li><li><a class="lk" title="hombre lobo: la bestia entre nosotros" href="http://www.sipeliculas.com/ver_4164_hombre-lobo-la-bestia-entre-nosotros.html"></a><em></em><i><a class="Ytrailer" href="oCXIDeIY59U" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/hombre-lobo-la-bestia-entre-nosotros.jpg" alt=""/></div><h3>Hombre lobo: la bestia entre nosotros</h3> <span><a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a>  / 2012</span> </li><li><a class="lk" title="el hobbit: un viaje inesperado" href="http://www.sipeliculas.com/ver_4163_el-hobbit-un-viaje-inesperado.html"></a><em></em><i><a class="Ytrailer" href="tVyESy1SftQ" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/el-hobbit-un-viaje-inesperado.jpg" alt=""/></div><h3>El hobbit: un viaje inesperado</h3> <span><a href="http://www.sipeliculas.com/categoria_aventura.html">Aventura</a> <a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a>  / 2012</span> </li><li><a class="lk" title="peso pesado" href="http://www.sipeliculas.com/ver_4162_peso-pesado.html"></a><em></em><i><a class="Ytrailer" href="ay9s6_kIqNo" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/peso-pesado.jpg" alt=""/></div><h3>Peso pesado</h3> <span><a href="http://www.sipeliculas.com/categoria_accion.html">Acción</a> <a href="http://www.sipeliculas.com/categoria_comedia.html">Comedia</a>  / 2012</span> </li><li><a class="lk" title="las aventuras de tadeo jones" href="http://www.sipeliculas.com/ver_4161_las-aventuras-de-tadeo-jones.html"></a><em></em><i><a class="Ytrailer" href="91a-09WpQZ0" rel="fancyvideo"></a><div class="vtp">ver trailer de la película</div></i><div class="ig"><img src="http://img.sipeliculas.com/IMG.Mediano/las-aventuras-de-tadeo-jones.jpg" alt=""/></div><h3>Las aventuras de tadeo jones</h3> <span><a href="http://www.sipeliculas.com/categoria_animacion.html">Animación</a>  / 2012</span> </li><div class="br"></div></ul><div id="pages"> <span>Total de páginas: 209</span> <ul><li><a class="select" href="http://www.sipeliculas.com/index_pag_1.htm">1</a></li><li><a href="http://www.sipeliculas.com/index_pag_2.htm">2</a></li><li><a href="http://www.sipeliculas.com/index_pag_3.htm">3</a></li><li><a href="http://www.sipeliculas.com/index_pag_4.htm">4</a></li><li><a href="http://www.sipeliculas.com/index_pag_5.htm">5</a></li><li><a href="http://www.sipeliculas.com/index_pag_6.htm">6</a></li><li><a href="http://www.sipeliculas.com/index_pag_7.htm">7</a></li><li><a href="http://www.sipeliculas.com/index_pag_8.htm">8</a></li><li><a href="http://www.sipeliculas.com/index_pag_9.htm">9</a></li><li><a href="http://www.sipeliculas.com/index_pag_2.htm" alt="Siguiente pagina" title="Siguiente pagina">&raquo;</a></li><li><a href="http://www.sipeliculas.com/index_pag_209.htm" alt="Ultima pagina" title="Ultima pagina">&raquo;&raquo;</a></li></ul> </div>
    ''' 
    patron = '<li><a class="lk" title="([^"]+)" href="([^"]+)"></a><em></em><i><a[^<]+</a><div[^<]+</div></i><div class="ig"><img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="mirrors", url=scrapedurl, thumbnail=scrapedthumbnail))

    patron='<a href="([^"]+)" alt="Siguiente pagina" title="Siguiente pagina"'
    matches = re.compile(patron,re.DOTALL).findall(data)    
    scrapedurl=matches[0];
    itemlist.append( Item(channel=__channel__, title="! Pagina Siguiente" , action="lista2", url=scrapedurl))
    #itemlist.append( Item(channel=__channel__, title=matchx , action="lista2", url=matchx)) 
    return itemlist

def mirrors(item):
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    bloque = scrapertools.get_match(data,'<ul id="listado">(.*?)</ul>')

    '''
    <li><a href="http://www.sipeliculas.com/ver_4174_el-diablo-viste-a-la-moda_10506-1.html">
    <span class="wa">Ver Opción 1</span>
    <span class="wb">videobam</span>
    <span class="wc">Latino</span>
    <span class="wd"> - </span>
    <span class="wf">dvd rip</span>
    </a></li
    '''

    patron  = '<li><a href="([^"]+)"[^<]+'
    patron += '<span class="wa">([^<]+)</span>[^<]+'
    patron += '<span class="wb">([^<]+)</span>[^<]+'
    patron += '<span class="wc">([^<]+)</span>[^<]+'
    patron += '<span class="wd">([^<]+)</span>[^<]+'
    patron += '<span class="wf">([^<]+)</span>[^<]+'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    
    for url,scrapedtitle,servidor,idioma,subtitulos,calidad in matches:
        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        title = title+" ["+servidor+"]["+idioma+"]["+subtitulos+"]["+calidad+"]"
        itemlist.append( Item(channel=__channel__, title=title , action="findvideos", url=url, folder=True))

    if len(itemlist)==0:
        itemlist = findvideos(item)
    
    return itemlist

def findvideosx(item):
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)
    patron='decode64.*?"(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("matches[0]="+matches[0])
    decripted=base64.decodestring(matches[0])
    logger.info("decripted="+decripted)
    listavideos = servertools.findvideos(decripted)
    itemlist = []
    plot=""
    for video in listavideos:
        videotitle = scrapertools.unescape(video[0])
        #print videotitle
        url = video[1]
        server = video[2]
        videotitle = item.title+ " - " +videotitle
        itemlist.append( Item(channel=__channel__, action="play", server=server, title=videotitle , url=url , thumbnail=item.thumbnail , plot=plot ,subtitle="", folder=False) )
    #itemlist.append( Item(channel=__channel__, title=titu , action="generos", url="http://yahoo.com"))
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = lista2(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors_items = mirrors(pelicula_item)
        for mirror_item in mirrors_items:
            if mirror_item.action=="findvideos":
                video_items = findvideos(item=mirror_item)
                if len(video_items)>0:
                    return True
            else:
                return True

    return bien