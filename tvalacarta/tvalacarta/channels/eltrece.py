# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para eltrece
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "eltrece"
MAIN_URL = "http://www.eltrecetv.com.ar/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[eltrece.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Destacadas" , action="novedades", url=MAIN_URL, extra=". Comentados", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Capítulos completos" , action="novedades", url=MAIN_URL, extra="Capitulos completos", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="+ Vistos" , action="novedades", url=MAIN_URL, extra="Notas m", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos" , action="novedades", url=MAIN_URL, extra="Últimos", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="En exclusivo" , action="novedades", url=MAIN_URL, extra="En exclusivo", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas" , action="programas", url=MAIN_URL, folder=True) )

    return itemlist

def novedades(item):
    logger.info("[eltrece.py] novedades")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    try:
        pagina_siguiente = scrapertools.get_match(data,'<div class="grid960-list".*?<div class="item-list"><ul class="pager pager-load-more[^<]+<li class="pager-next first last"><a href="([^"]+)">Mostrar m')
    except:
        pagina_siguiente=""
    logger.info("pagina_siguiente="+pagina_siguiente)

    try:
        data = scrapertools.get_match(data,'<div class="view-content"[^<]+<div class="grid960-list"[^<]+<h3>'+item.extra+'(.*?)</div>\s+</div>[^<]+')
    except:
        pass
    logger.info("data="+data)

    patron  = '<a href="([^"]+)"><img typeof="[^"]+" src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<h5><a href="[^"]+">[^<]+</a></h5>[^<]+'
    patron += '<h4><a href="[^"]+">([^<]+)</a></h4>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="eltrece", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    # Paginación
    if pagina_siguiente!="":
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="novedades", url=urlparse.urljoin(item.url,pagina_siguiente), folder=True) )

    return itemlist

def programas(item):
    logger.info("[eltrece.py] programas")
    
    # Descarga la página
    if item.extra=="":
        data = scrapertools.cache_page( item.url )
        bloque = scrapertools.get_match(data,"<h3>Programas</h3>(.*?)</ul>")
    else:
        data = scrapertools.cache_page( item.url , post=item.extra)
        
        data_json = load_json(data)
        bloque=data_json[1]['data']
        data=bloque
        logger.info("bloque="+bloque)
    
    patron  = '<li class="views-row views-row-[^"]+">[^<]+'
    patron += '<a href="([^"]+)">([^<]+)</a>\s+</li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="secciones", url=scrapedurl, folder=True) )

    # Paginación
    try:
        numero_pagina = scrapertools.get_match(data,'<li class="pager-next first last"><a href=".*?\?page\=(\d+)">')
        pagina_siguiente = "http://www.eltrecetv.com.ar/views/ajax"
        post = "page="+numero_pagina+"&pager_element=0&view_args=&view_base_path=null&view_display_id=block&view_dom_id=e835618f1d8d5e82b6bc6c2995931b97&view_name=menu_programas&view_path=programa/cuestión-de-peso/cuestion-de-peso-2012/674/en-exclusiva"
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="programas", url=pagina_siguiente, extra=post, folder=True) )
    except:
        pass

    return itemlist

def secciones(item):
    logger.info("[eltrece.py] secciones")
    itemlist = []

    data=scrapertools.cache_page(item.url)
    data=scrapertools.get_match(data,'<ul class="menu-interno-programa[^"]+">(.*?)</ul>')
    patron = '<li[^<]+<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for url,titulo in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=CHANNELNAME, title=titulo , action="episodios", url=scrapedurl, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[eltrece.py] episodios")
    
    # Descarga la página
    if item.extra=="":
        data = scrapertools.cache_page( item.url )
    else:
        data = scrapertools.cache_page( item.url , post=item.extra)
        
        data_json = load_json(data)
        logger.info("data_json="+str(data_json))
        data=data_json[1]['data']
        logger.info("data="+data)

    '''
    <div class="views_row views_row_4 views_row_even grid_3 alpha">  
    <a href="/periodismo-para-todos/periodismo-para-todos/00053539/megaminer%C3%AD-pol%C3%ADtica-y-negocios"><img typeof="foaf:Image" src="http://cdn.eltrecetv.com.ar/sites/default/files/styles/180x101/public/famatina-2.jpg" width="180" height="101" alt="" /></a>    
    <h5>        <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2012-07-15T21:30:00-03:00">15/07/2012</span>  </h5>  
    <h4><a href="/periodismo-para-todos/periodismo-para-todos/00053539/megaminer%C3%AD-pol%C3%ADtica-y-negocios">Megaminería, política y negocios</a></h4>    
    <span class="total_views">9,383</span>  </div>
    '''
    patron  = '<div class="views_row views_row_\d+ views_row_[^<]+'
    patron += '<a href="([^"]+)"><img typeof="foaf.Image" src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<h5>\s+<span[^>]+>([^<]+)</span>\s+</h5>[^<]+'
    patron += '<h4><a href="[^"]+">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,fecha,title in matches:
        scrapedtitle = title+" ("+fecha+")"
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="eltrece", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    # Paginación
    try:
        #<ul class="pager pager-load-more"><li class="pager-next first last"><a href="/programa/periodismo-para-todos/periodismo-para-todos?page=2">Mostrar más videos ▼</a></li>
        numero_pagina = scrapertools.get_match(data,'<li class="pager-next[^<]+<a href=".*?\?page\=(\d+)">Mostrar m')
        pagina_siguiente = "http://www.eltrecetv.com.ar/views/ajax"

        if item.extra=="":
            nodo = scrapertools.get_match(data,'<link rel="shortlink" href="/node/\d+" />')
            view_args = scrapertools.get_match(data,'view_args"\:"([^"]+)"')
            view_args = view_args.replace("\\","")
            post = "page="+numero_pagina+"&pager_element=0&view_args="+view_args+"&view_base_path=null&view_display_id=block&view_dom_id=ca1b6cbfe6bdde9993cab251a0cabf43&view_name=notas_temporada&view_path="+nodo
        else:
            post = re.compile("page=\d+",re.DOTALL).sub("page="+numero_pagina,item.extra)

        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="episodios", url=pagina_siguiente, extra=post, folder=True) )
    except:
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)


    return itemlist


# TODO: Pasar al core
def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct

    try:
        from lib import simplejson
        json_data = simplejson.loads(data, object_hook=to_utf8)
        return json_data
    except:
        try :        
            import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
        except:
            import traceback
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)
            
            try:
                import json
                json_data = json.loads(data, object_hook=to_utf8)
                return json_data
            except:
                import traceback
                from pprint import pprint
                exc_type, exc_value, exc_tb = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_tb)
                for line in lines:
                    line_splits = line.split("\n")
                    for line_split in line_splits:
                        logger.error(line_split)

                try:
                    json_data = JSON.ObjectFromString(data, encoding="utf-8")
                    return json_data
                except:
                    import traceback
                    from pprint import pprint
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_tb)
                    for line in lines:
                        line_splits = line.split("\n")
                        for line_split in line_splits:
                            logger.error(line_split)
