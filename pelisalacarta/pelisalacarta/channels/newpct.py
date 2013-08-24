# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Newpct"
__channel__ = "newpct"
__language__ = "ES"
__creationdate__ = "20130308"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newpct.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Películas", url="http://www.newpct.com/include.inc/load.ajax/load.topbar.php?userName=", extra="Peliculas" ))
    itemlist.append( Item(channel=__channel__, action="submenu" , title="Series"   , url="http://www.newpct.com/include.inc/load.ajax/load.topbar.php?userName=", extra="Series" ))
    #itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar" ))
  
    return itemlist

def search(item,texto):
    logger.info("[newpct.py] search")
    if item.url=="":
        item.url="http://jkanime.net/buscar/%s/"
    texto = texto.replace(" ","+")
    item.url = item.url % texto
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def submenu(item):
    logger.info("[newpct.py] peliculas")
    itemlist=[]
    
    data = scrapertools.cache_page(item.url)

    '''
    <li><a href="#" rel="nofollow" class="dir" title="Descargar Peliculas Gratis">Peliculas<img src="http://www.newpct.com/sections.inc/top.column.inc/topmenu.inc/images/arows.png" alt="Descargas Torrent"></a>
    <ul>
    <li><a href="http://www.newpct.com/peliculas-castellano/peliculas-rip/" title="Descargar Peliculas en Castellano DVDRIP" >Peliculas DVDRIP-BRRIP Castellano</a></li>
    <li><a href="http://www.newpct.com/peliculas-latino/" title="Descargar Peliculas Latino Gratis">Peliculas Latino</a></li>
    <li><a href="http://www.newpct.com/peliculas-castellano/estrenos-de-cine/" title="Descargar Estrenos de Cine Gratis">Estrenos de Cine Castellano</a></li>
    <li><a href="http://www.newpct.com/cine-alta-definicion-hd/" title="Descargar Peliculas en HD, Alta Definicion Gratis">Peliculas Alta Definicion HD</a></li>
    <li><a href="http://www.newpct.com/peliculas-en-3d-hd/" title="Descargar Peliculas en 3D HD" >Peliculas en 3D HD</a></li>
    <li><a href="http://www.newpct.com/peliculas-castellano/peliculas-dvd/" title="Descargar Peliculas DVD FULL">Peliculas DVDFULL</a></li>
    <li><a href="http://www.newpct.com/peliculas-vo/" title="Descargar Peliculas en V.O Subtituladas">Peliculas V.O.Subtituladas</a></li>
    <li><a href="http://www.newpct.com/anime/" title="Descargar Series y Peliculas Anime Gratis">Anime</a></li>
    <li><a href="http://www.newpct.com/documentales/" title="Descargar Documentales Gratis">Documentales</a></li>
    </ul>
    </li>
    '''
    data = scrapertools.get_match(data,'<a href="\#" rel="nofollow" class="dir" title="Descargar '+item.extra+' Gratis">'+item.extra+'(.*?)</ul>')

    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="listado" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    
    return itemlist

def listado(item):
    logger.info("[newpct.py] listado")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    
    '''
    <li>
    <a href='http://www.newpct.com/descargar-pelicula/la-pequena-venecia/'>
    <div class='boxgrid captionb'>
    <img src='http://images.newpct.com/banco_de_imagenes/destacados/038707/la-pequeña-venecia--dvdrip--ac3-5-1-español-castellano--2012-.jpg'  alt='Descargar Peliculas Castellano &raquo; Películas RIP La Pequeña Venecia [DVDrip][AC3 5.1 Español Castellano][2012]' />
    <div class='cover boxcaption'>
    <h3>La Pequeña Venecia </h3>
    <p>Peliculas Castellano<br/>
    Calidad: DVDRIP AC3 5.1<br>
    Tama&ntilde;o: 1.1 GB<br>
    Idioma : Español Castellano
    </p>
    </div>
    </div>
    </a>
    <div id='bot-desc'>
    <div id='tinfo'>
    <a class='youtube' href='#' rel='gx9EKDC0UFQ' title='Ver Trailer' alt='Ver Trailer'>
    <img style='width:25px;' src='http://www.newpct.com/images.inc/images/playm2.gif'></a>
    </div>
    <div id='tdescargar' ><a class='atdescargar' href='http://www.newpct.com/descargar-pelicula/la-pequena-venecia/'>DESCARGAR</a></div>
    </div>
    </li>
    '''
    patron  = "<li[^<]+"
    patron += "<a href='([^']+)'[^<]+"
    patron += "<div class='boxgrid captionb'[^<]+"
    patron += "<img src='([^']+)'[^<]+"
    patron += "<div class='cover boxcaption'[^<]+"
    patron += '<h3>([^<]+)</h3>(.*?)</div>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip()
        title = unicode( title, "iso-8859-1" , errors="replace" ).encode("utf-8")

        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot).strip()
        plot = unicode( plot, "iso-8859-1" , errors="replace" ).encode("utf-8")

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot"))

    # Página siguiente
    '''
    GET /include.inc/ajax.php/orderCategory.php?type=todo&leter=&sql=SELECT+DISTINCT+++%09%09%09%09%09%09torrentID%2C+++%09%09%09%09%09%09torrentCategoryID%2C+++%09%09%09%09%09%09torrentCategoryIDR%2C+++%09%09%09%09%09%09torrentImageID%2C+++%09%09%09%09%09%09torrentName%2C+++%09%09%09%09%09%09guid%2C+++%09%09%09%09%09%09torrentShortName%2C++%09%09%09%09%09%09torrentLanguage%2C++%09%09%09%09%09%09torrentSize%2C++%09%09%09%09%09%09calidad+as+calidad_%2C++%09%09%09%09%09%09torrentDescription%2C++%09%09%09%09%09%09torrentViews%2C++%09%09%09%09%09%09rating%2C++%09%09%09%09%09%09n_votos%2C++%09%09%09%09%09%09vistas_hoy%2C++%09%09%09%09%09%09vistas_ayer%2C++%09%09%09%09%09%09vistas_semana%2C++%09%09%09%09%09%09vistas_mes++%09%09%09%09++FROM+torrentsFiles+as+t+WHERE++(torrentStatus+%3D+1+OR+torrentStatus+%3D+2)++AND+(torrentCategoryID+IN+(1537%2C+758%2C+1105%2C+760%2C+1225))++++ORDER+BY+torrentDateAdded++DESC++LIMIT+0%2C+50&pag=3&tot=&ban=3&cate=1225 HTTP/1.1
    Host: www.newpct.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0
    Accept: */*
    Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    X-Requested-With: XMLHttpRequest
    Referer: http://www.newpct.com/peliculas-castellano/peliculas-rip/
    Cookie: adbooth_popunder=5%7CSat%2C%2009%20Mar%202013%2018%3A23%3A22%20GMT
    Connection: keep-alive
    '''
    
    '''
    function orderCategory(type,leter,pag,other)
    {
        
        
        if(leter=='buscar')
        {
            leter = document.getElementById('word').value;
        }
        if(type=='todo')
        {
            document.getElementById('todo').className = "active_todo";
        }	
        if(type=='letter')
        {
            switch(leter)
            {
                case '09':
                document.getElementById('09').className = "active_num";
                break;
                default:
                document.getElementById(leter).className = "active_a";
                break;
            }
        }
        
        var parametros = {
                    "type" : type,
                    "leter" : leter,
                    "sql" : "SELECT DISTINCT   						torrentID,   						torrentCategoryID,   						torrentCategoryIDR,   						torrentImageID,   						torrentName,   						guid,   						torrentShortName,  						torrentLanguage,  						torrentSize,  						calidad as calidad_,  						torrentDescription,  						torrentViews,  						rating,  						n_votos,  						vistas_hoy,  						vistas_ayer,  						vistas_semana,  						vistas_mes  				  FROM torrentsFiles as t WHERE  (torrentStatus = 1 OR torrentStatus = 2)  AND (torrentCategoryID IN (1537, 758, 1105, 760, 1225))    ORDER BY torrentDateAdded  DESC  LIMIT 0, 50",
                    "pag" : pag,   
                    "tot" : '',
                    "ban" : '3',
                    "other": other,
                    "cate" : '1225'
                    
            };
        //alert(type+leter);
        
        $('#content-category').html('<div style="margin:100px auto;width:100px;height:100px;"><img src="http://www.newpct.com/images.inc/images/ajax-loader.gif"/></div>');
            var page = $(this).attr('data');        
            var dataString = 'page='+page;
            
         $.ajax({
              type: "GET",
              url:   'http://www.newpct.com/include.inc/ajax.php/orderCategory.php',
              data:  parametros,
              success: function(data) {
             
                    //Cargamos finalmente el contenido deseado
                    $('#content-category').fadeIn(1000).html(data);
              }
         });
         
    }
    '''
    if item.extra!="":
        bloque=item.extra
    else:
        bloque = scrapertools.get_match(data,"function orderCategory(.*?)\}\)\;")
    logger.info("bloque="+bloque)
    param_type=scrapertools.get_match(data,"<a href='javascript:;' onclick=\"orderCategory\('([^']+)'[^>]+> >> </a>")
    logger.info("param_type="+param_type)
    param_leter=scrapertools.get_match(data,"<a href='javascript:;' onclick=\"orderCategory\('[^']+','([^']*)'[^>]+> >> </a>")
    logger.info("param_leter="+param_leter)
    param_pag=scrapertools.get_match(data,"<a href='javascript:;' onclick=\"orderCategory\('[^']+','[^']*','([^']+)'[^>]+> >> </a>")
    logger.info("param_pag="+param_pag)
    param_sql=scrapertools.get_match(bloque,'"sql"\s*\:\s*"([^"]+)')
    logger.info("param_sql="+param_sql)
    param_tot=scrapertools.get_match(bloque,"\"tot\"\s*\:\s*'([^']*)'")
    logger.info("param_tot="+param_tot)
    param_ban=scrapertools.get_match(bloque,"\"ban\"\s*\:\s*'([^']+)'")
    logger.info("param_ban="+param_ban)
    param_cate=scrapertools.get_match(bloque,"\"cate\"\s*\:\s*'([^']+)'")
    logger.info("param_cate="+param_cate)
    base_url = scrapertools.get_match(bloque,"url\s*\:\s*'([^']+)'")
    logger.info("base_url="+base_url)
    #http://www.newpct.com/include.inc/ajax.php/orderCategory.php?type=todo&leter=&sql=SELECT+DISTINCT+++%09%09%09%09%09%09torrentID%2C+++%09%09%09%09%09%09torrentCategoryID%2C+++%09%09%09%09%09%09torrentCategoryIDR%2C+++%09%09%09%09%09%09torrentImageID%2C+++%09%09%09%09%09%09torrentName%2C+++%09%09%09%09%09%09guid%2C+++%09%09%09%09%09%09torrentShortName%2C++%09%09%09%09%09%09torrentLanguage%2C++%09%09%09%09%09%09torrentSize%2C++%09%09%09%09%09%09calidad+as+calidad_%2C++%09%09%09%09%09%09torrentDescription%2C++%09%09%09%09%09%09torrentViews%2C++%09%09%09%09%09%09rating%2C++%09%09%09%09%09%09n_votos%2C++%09%09%09%09%09%09vistas_hoy%2C++%09%09%09%09%09%09vistas_ayer%2C++%09%09%09%09%09%09vistas_semana%2C++%09%09%09%09%09%09vistas_mes++%09%09%09%09++FROM+torrentsFiles+as+t+WHERE++(torrentStatus+%3D+1+OR+torrentStatus+%3D+2)++AND+(torrentCategoryID+IN+(1537%2C+758%2C+1105%2C+760%2C+1225))++++ORDER+BY+torrentDateAdded++DESC++LIMIT+0%2C+50&pag=3&tot=&ban=3&cate=1225
    url_next_page = base_url + "?" + urllib.urlencode( { "type":param_type, "leter":param_leter, "sql":param_sql, "pag":param_pag, "tot":param_tot, "ban":param_ban, "cate":param_cate } )
    logger.info("url_next_page="+url_next_page)
    itemlist.append( Item(channel=__channel__, action="listado" , title=">> Página siguiente" , url=url_next_page, extra=bloque))

    return itemlist

def findvideos(item):
    logger.info("[newpct.py] findvideos")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    torrent_id = scrapertools.get_match(data,"'torrentID'\s*\:\s*'(\d+)'")
    
    data = data + scrapertools.cache_page("http://www.newpct.com/include.inc/ajax.php/update.links.php?userID=&torrentID="+torrent_id)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    submenu_items = submenu(mainlist_items[0])
    listado_items = listado(submenu_items[0])
    for listado_item in listado_items:
        play_items = findvideos(listado_item)
        
        if len(play_items)>0:
            return True

    return False