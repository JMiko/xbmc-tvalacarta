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
    #itemlist.append( Item(channel=CHANNELNAME, title="Clip CDA"         , action="calidades", url=MAIN_URL+"/clip/512/cda"      , folder=True) )

    return itemlist


def programas(item):
    logger.info("[" + CHANNELNAME + ".py] programas")
    
    # Descargo la página de la sección.
    data = scrapertools.cachePage(item.url)
    if (DEBUG): logger.info(data)

    try:
        pagina_siguiente = scrapertools.get_match(data, '<li>\s*<a class="btn arrow" href="(.*?)">»</a>\s*</li>')
    except:
        pagina_siguiente = ""
    if (DEBUG): logger.info("pagina_siguiente=" + pagina_siguiente)

    # Extraigo URL, imagen y título y descripción.
    #patron  = '<article.*?>\s*<a.*?href="(.*?)".*?>\s*<img.*?src="(.*?)".*?/>.*?<h3.*?>(.*?)</h3>.*?<h3>Sinopsis</h3><.*?>(.*?)</.*?>'
    patron  = '<article.*?>\s*<a.*?href=".*?/(\w+)/(\d+)/.*?".*?>\s*<img.*?src="(.*?)".*?/>.*?<h3.*?>(.*?)</h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for itype, iid, ithumbnail, ititle in matches:
        if itype == 'clip':
            iaction = 'calidades'
        else:
            iaction = 'capitulos'

        # Añado el item del programa al listado.
        #itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle) , action="capitulos", url=iurl, thumbnail=ithumbnail, plot=scrapertools.htmlclean(iplot), folder=True) )
        itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle) , action=iaction, url=iid, thumbnail=ithumbnail, folder=True) )

    # Si existe una página siguiente entonces agrego un item de paginación.
    if pagina_siguiente != "":
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente", action="programas", url=MAIN_URL+pagina_siguiente, folder=True) )

    return itemlist


def capitulos(item):
    logger.info("[" + CHANNELNAME + ".py] capitulos")

    #try:
    #    # Extraigo el id del programa.    
    #    programa_id = scrapertools.get_match(item.url, '/(\d+)/')
    #    if (DEBUG): logger.info('ID:' + programa_id)
    #
    #    # Solicito los capítulos del programa.
    #    data = scrapertools.cachePage(MAIN_URL + '/chapters/ajax/' + programa_id)
    #    if (DEBUG): logger.info('Json:' + data)
    #
    #    objects = json.loads(data, object_hook=to_utf8)
    #
    #    itemlist = []
    #    for object in objects['chapters']:
    #        try:
    #            # Si el nombre del capítulo incluye el nombre del programa, extraigo sólo el nombre del capítulo.
    #            ititle = scrapertools.get_match(object['title'], '.*?: (.*)')
    #        except:
    #            ititle = object['title']
    #
    #        # Añado el item del capítulo al listado.
    #        itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle), action="calidades", url=MAIN_URL+'/clip/ajax/'+object['id']+'/', thumbnail=item.thumbnail, folder=True ) )
    #
    #    return itemlist
    #except:
    #    # Si no existen capítulos para este programa entonces es un clip.
    #    return calidades(item)

    # Descargo la página de la sección.
    data = scrapertools.cachePage(MAIN_URL+'/serie/'+item.url+'/')
    if (DEBUG): logger.info(data)

    # Extraigo URL, imagen y título y descripción.
    patron  = '<article.*?item_id="(\d*)".*?>\s*<a.*?href=".*?".*?>\s*<img.*?src="(.*?)".*?/>.*?<h3 itemprop="name">(.*?)</h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for ivideo, ithumbnail, ititle in matches:
        # Añado el item del programa al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=scrapertools.htmlclean(ititle), action="calidades", url=ivideo, thumbnail=ithumbnail, folder=True ) )

    return itemlist


def calidades(item):
    logger.info("[" + CHANNELNAME + ".py] calidades")

    data = scrapertools.cachePage(MAIN_URL+'/clip/ajax/'+item.url+'/')
    if (DEBUG): logger.info('Json:' + data)

    video = json.loads(data)
    # Descargo la página del clip.
    data = scrapertools.cache_page('http://186.33.226.132/vod/smil:content/videos/clips/' + video['video_id'] + '.smil/playlist.m3u8')
    if (DEBUG): logger.info("data=" + data)

    # Extraigo calidades.
    patron  = '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=(\d*)\n(chunklist_.*?\.m3u8)'
    matches = re.compile(patron, re.DOTALL).findall(data)

    itemlist = []
    for iquality, ifile in matches:
        if iquality == '200000':
            quality = 'Móvil 180p (' + iquality + 'bps)'
        elif iquality == '700000':
            quality = 'LD (' + iquality + 'bps)'
        elif iquality == '1200000':
            quality = 'SD (' + iquality + 'bps)'
        elif iquality == '2000000':
            quality = 'HD 720 (' + iquality + 'bps)'
        else:
            quality = 'Desconocida (' + iquality + 'bps)'
        
        sPlaypath = 'http://186.33.226.132/vod/smil:content/videos/clips/' + video['video_id'] + '.smil/' + ifile
        if (DEBUG): logger.info("sPlaypath=" + sPlaypath)

        # Añado el item de la calidad al listado.
        itemlist.append( Item(channel=CHANNELNAME, title=quality, action='play', url=sPlaypath, thumbnail=item.thumbnail, extra=item.title, folder=False ) )

    return itemlist

def to_utf8(dct):
    rdct = {}
    for k, v in dct.items() :
        if isinstance(v, (str, unicode)) :
            rdct[k] = v.encode('utf8', 'ignore')
        else :
            rdct[k] = v
    return rdct
