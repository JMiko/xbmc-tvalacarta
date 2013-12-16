# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Fútbol Para Todos
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#
# Autor: Juan Pablo Candioti (@JPCandioti)
# Desarrollo basado sobre otros canales de tvalacarta
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core.item import Item


DEBUG = True
CHANNELNAME = "fpt"
MAIN_URL = "http://www.futbolparatodos.com.ar"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[" + CHANNELNAME + "] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Clip de Apertura Torneo Inicial 2013", action="play", server="youtube", url="http://www.youtube.com/watch?v=q_D6d_6z_Wk", folder=False) )
    itemlist.append( Item(channel=CHANNELNAME, title="Goles"                     , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=goles"                  , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Jugadas"                   , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=jugadas"                , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Entrevistas"               , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=entrevistas"            , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Homenajes"                 , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=homenajes"              , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="El amor para toda la vida" , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=amorparatodalavida"     , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Utilero soy"               , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=utilerosoy"             , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="El rompecabezas del fútbol", action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=elrompecabezasdelfutbol", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Lecciones de fútbol"       , action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo=lecciones-de-futbol"    , folder=True) )

    return itemlist


def videos(item):
    logger.info("[" + CHANNELNAME + "] videos")

    # Descargo la página de la sección.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    tipo = scrapertools.get_match(item.url, '\?tipo=([^&]+)')

    try:
        pagina_siguiente = scrapertools.get_match(data, '<div\s+id="(\d+)" class="ultimo removerultimo".*?>\s*<br clear="all">')
    except:
        pagina_siguiente = ""
    if (DEBUG): logger.info("pagina_siguiente=" + pagina_siguiente)

    # Extraigo id, imagen, título y descripción del video.
    patron  = '<li\s*class=".*?">\s*<div\s*style="position: relative;"><a\s*href="http://www.youtube.com/embed/(.{11})\?autoplay=1" class="lbpModal cboxElement" title=".*?"><img\s*.*?src="(.*?)".*?/><img\s*src=".*?/wp-content/uploads/transparent-play-player.png".*?></a></div><div\s*class="golitemdetalle">.*?</br>\s*<a\s*href=".*?" >(.*?)</a></br>\s*(.*?)</div></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for id_video, ithumbnail, ititle, iplot in matches:
        ititle2 = re.sub(r"&#?\w+;", "", ititle)
        logger.info("[" + CHANNELNAME + "] title=" + ititle2)
        # Añado el item del video al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle2), action="play", server="youtube", url="http://www.youtube.com/watch?v="+id_video, thumbnail=ithumbnail, plot=iplot, folder=False) )

    # Si existe una página siguiente entonces agrego un item de paginación.
    if pagina_siguiente != "":
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente", action="videos", url=MAIN_URL+"/wp-content/themes/fpt2/jquery_cargar_videos.php?tipo="+tipo+"&desde="+str(int(pagina_siguiente)+1), folder=True) )

    return itemlist
