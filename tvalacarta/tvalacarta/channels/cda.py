# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Contenidos Digitales Abiertos
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#
# Autor: Juan Pablo Candioti (@JPCandioti)
# Desarrollo basado sobre otros canales de tvalacarta
#------------------------------------------------------------

import re, json

from core import logger
from core import scrapertools
from core.item import Item


DEBUG = True
PLOT = True
CHANNELNAME = "cda"
MAIN_URL = "http://cda.gob.ar"


def isGeneric():
    return True


def mainlist(item):
    logger.info("[" + CHANNELNAME + ".py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Series-Unitarios" , action="programas", url=MAIN_URL+"/series-unitarios/" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales"     , action="programas", url=MAIN_URL+"/documentales/"     , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Cortos"           , action="programas", url=MAIN_URL+"/cortos/"           , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Micros"           , action="programas", url=MAIN_URL+"/micros/"           , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Igualdad Cultural", action="programas", url=MAIN_URL+"/igualdad-cultural/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Clip CDA"         , action="calidades", url=MAIN_URL+"/clip/512/cda"      , folder=True) )

    return itemlist


def programas(item):
    logger.info("[" + CHANNELNAME + ".py] programas")
    
    # Descargo la página de la sección.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    try:
        pagina_siguiente = scrapertools.get_match(data, '&gt;&gt;</a>\s*</li>\s*<li>\s*<a class="btn arrow" href="(.*?)">&gt;</a>\s*</li>')
    except:
        pagina_siguiente = ""
    if (DEBUG): logger.info("pagina_siguiente=" + pagina_siguiente)

    # Extraigo URL, imagen y título.
    patron  = '<article.*?>\s*<a href="(.*?)">\s*<img src="(.*?)".*?/>\s*<h3>(.*?)</h3>.*?</article>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for iurl, ithumbnail, ititle in matches:
        if PLOT:
            try:
                plot_data = scrapertools.cachePage(iurl)
                if (DEBUG): logger.info(data)

                # Extraigo la sinópsis del programa y luego borro todas las etiquetas HTML.
                iplot = scrapertools.htmlclean(scrapertools.get_match(plot_data, '<h3>Sinopsis</h3><p.*?>(.*?)</p>'))
                if (DEBUG): logger.info('plot:' + iplot)
            except:
                iplot = "";
        else:
            iplot = "";

        # Añado el item del programa al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle) , action="capitulos", url=iurl, thumbnail=ithumbnail, plot=iplot, folder=True) )

    # Si existe una página siguiente entonces agrego un item de paginación.
    if pagina_siguiente != "":
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente", action="programas", url=MAIN_URL+pagina_siguiente, folder=True) )

    return itemlist


def capitulos(item):
    logger.info("[" + CHANNELNAME + ".py] capitulos")

    try:
        # Extraigo el id del programa.    
        programa_id = scrapertools.get_match(item.url, '/(\d+)/')
        if (DEBUG): logger.info('ID:' + programa_id)

        # Solicito los capítulos del programa.
        data = scrapertools.cachePage(MAIN_URL + '/chapters/ajax/' + programa_id)
        if (DEBUG): logger.info('Json:' + data)
    
        objects = json.loads(data, object_hook=to_utf8)
    
        itemlist = []
        for object in objects['chapters']:
            try:
                # Si el nombre del capítulo incluye el nombre del programa, extraigo sólo el nombre del capítulo.
                ititle = scrapertools.get_match(object['title'], '.*?: (.*)')
            except:
                ititle = object['title']
    
            # Añado el item del capítulo al listado.
            itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle), action="calidades", url=MAIN_URL+'/clip/'+object['id']+'/', thumbnail=item.thumbnail, folder=True ) )
    
        return itemlist
    except:
        # Si no existen capítulos para este programa entonces es un clip.
        return calidades(item)


def calidades(item):
    logger.info("[" + CHANNELNAME + ".py] calidades")

    # Descargo la página del clip.
    data = scrapertools.cache_page(item.url)
    if (DEBUG): logger.info("data=" + data)

    ititle = scrapertools.get_match(data, '<h1 id="title">(.*?)</h1>')
    sRtmp = scrapertools.get_match(data, 'streamer: "(rtmp://.*?)/.*?",')
    sApp  = scrapertools.get_match(data, 'streamer: "rtmp://.*?/(.*?)",')
    sSwfUrl = MAIN_URL + scrapertools.get_match(data, 'flashplayer: "(.*?)",')
    
    # Solicito las calidades del clip.
    clip_id = scrapertools.get_match(item.url, '/(\d+)/')
    if (DEBUG): logger.info('ID:' + clip_id)
    data = scrapertools.cachePage(MAIN_URL + '/clip/ajax/' + clip_id)
    if (DEBUG): logger.info('Json:' + data)

    objects = json.loads(data)

    itemlist = []
    for object in objects['versions']:
        sPlaypath = 'mp4:' + object['src']
        sStreamUrl = sRtmp + ' app=' + sApp + ' swfurl=' + sSwfUrl + ' playpath=' + sPlaypath
        if (DEBUG): logger.info("stream=" + sStreamUrl)

        # Añado el item de la calidad al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=object['name'].title()+' ('+object['bitrate']+'kbps)', action="play", url=sStreamUrl, thumbnail=item.thumbnail, extra=ititle, folder=False ) )

    return itemlist

def to_utf8(dct):
    rdct = {}
    for k, v in dct.items() :
        if isinstance(v, (str, unicode)) :
            rdct[k] = v.encode('utf8', 'ignore')
        else :
            rdct[k] = v
    return rdct
