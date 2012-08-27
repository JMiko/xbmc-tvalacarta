# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para bajui
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "bajui"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Bajui"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[bajui.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas", url="http://www.bajui.com/descargas/categoria/2/peliculas",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="menuseries",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="menudocumentales",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menupeliculas(item):
    logger.info("[bajui.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - Novedades"        , action="peliculas"   , url=item.url,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"              , action="peliculas"   , url=item.url+"/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    
    #<ul class="submenu2 subcategorias"><li ><a href="/descargas/subcategoria/4/br-scr-dvdscr">BR-Scr / DVDScr</a></li><li ><a href="/descargas/subcategoria/6/dvdr-full">DVDR - Full</a></li><li ><a href="/descargas/subcategoria/1/dvdrip-vhsrip">DVDRip / VHSRip</a></li><li ><a href="/descargas/subcategoria/3/hd">HD</a></li><li ><a href="/descargas/subcategoria/2/hdrip-bdrip">HDRip / BDRip</a></li><li ><a href="/descargas/subcategoria/35/latino">Latino</a></li><li ><a href="/descargas/subcategoria/5/ts-scr-cam">TS-Scr / CAM</a></li><li ><a href="/descargas/subcategoria/7/vos">VOS</a></li></ul>
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<ul class="submenu2 subcategorias">(.*?)</ul>')
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, title="Películas en "+title , action="peliculas", url=scrapedurl,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))

    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"      , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menuseries(item):
    logger.info("[bajui.py] menuseries")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series - Novedades"           , action="peliculas"        , url="http://www.bajui.com/descargas/categoria/3/series",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series - A-Z"                 , action="peliculas"        , url="http://www.bajui.com/descargas/categoria/3/series/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Series - HD"                  , action="peliculas"        , url="http://www.bajui.com/descargas/subcategoria/11/hd/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"            , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

def menudocumentales(item):
    logger.info("[bajui.py] menudocumentales")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Documentales - Novedades"         , action="peliculas"     , url="http://www.bajui.com/descargas/categoria/7/docus-y-tv",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Documentales - A-Z"               , action="peliculas"     , url="http://www.bajui.com/descargas/categoria/7/docus-y-tv/orden:nombre",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                           , action="search"        , url="",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[bajui.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.bajui.com/descargas/busqueda/%s"
        item.url = item.url % texto
        itemlist.extend(peliculas(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscar(item,paginacion=True):
    logger.info("[bajui.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">([^#]+)#888"><b>([^<]+)</b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        if match[5] == 'Peliculas' or match[5] == 'Series':
            scrapedtitle =  match[2]
            # Convierte desde UTF-8 y quita entidades HTML
            #        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            # procesa el resto
            scrapedplot = ""

            scrapedurl = urlparse.urljoin("http://www.bajui.com/",match[3])
            scrapedthumbnail = urlparse.urljoin("http://www.bajui.com/",match[1])
            if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    # Extrae el paginador
    #<a href="categoria/2/peliculas/pag:2/orden:nombre" class="pagina pag_sig">Siguiente »</a>
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin("http://www.bajui.com/",matches[0])
        pagitem = Item(channel=__channel__, action="peliculas", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )

    return itemlist

def peliculas(item,paginacion=True):
    logger.info("[bajui.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cache_page(url)
    '''
    <li id="ficha-42601" class="ficha2 " >
    <div class="detalles-ficha" >
    <span class="nombre-det">Ficha: Solty Rei - Temporada única</span>
    <span class="categoria-det">Categoría: Series - Series</span>
    <span class="descrip-det">TÍTULO ORIGINAL	Solty Rei (SoltyRei) (TV Series)<br />
    AÑO	2005<br />
    DURACIÓN	Trailers/Vídeos 30 min.<br />
    PAÍS	<br />
    DIRECTOR	Yoshimasa Hiraike, Masashi Abe, Ryuichi Kimura, Yoshihiko Iwada<br />
    GUIÓN	Noboru Kimura<br />
    MÚSICA	Toshiyuki Omori<br />
    FOTOGRAFÍA	Animation<br />
    REPARTO	Animation<br />
    PRODUCTORA	Gonzo   <br />
    WEB OFICIAL	http://www.soltyrei.tv/<br />
    GÉNERO	Serie de TV. Animación. Ciencia ficción. Acción. Drama | Robots<br />
    SINOPSIS	Serie de TV (2005-2006). 24 episodios. En un mundo brutal y con una sociedad defenest...</span>
    </div><a href="/descarga/42601/solty-rei-temporada-unica" >
    <img src="thumb_fichas/42601_m.jpg" alt="Imagen Solty Rei - Temporada única" onmouseover="javascript:mostrar_descrip2(42601);" onmouseout="javascript:ocultar_descrip2(42601);"/></a>
    <a class="nombre-ficha" href="/descarga/42601/solty-rei-temporada-unica">Solty Rei - Temp...</a>
    <span class="categoria">Series - Series</span></li>
    '''
    '''
    <li id="ficha-43651" class="ficha2 " >
    <div class="detalles-ficha" >
    <span class="nombre-det">Ficha: Al Borde del Abismo (Man on a Ledge) [DVDRip]</span>
    <span class="categoria-det">Categoría: Peliculas - DVDRip / VHSRip</span>
    <span class="descrip-det">TÍTULO ORIGINAL: Man on a ledge. <br />
    AÑO: 2012<br />
    GENERO: Thriller. <br />
    REPARTO: Sam Worthington (Nick Cassidy), Elizabeth Banks (Lydia), Jamie Bell (Joey Cassidy), Anthony Mackie (Mike), Genesis Rodriguez (Angie), Ed Harris (David Englander), Kyra Sedgwick (Suzie), Edward Burns, William Sadler. <br />
    SINOPSIS: “Al borde del abismo” (Man on a ledge) nos relatará la historia de un ex policía que ingresa en la cárcel tras ser acusado de cometer un crimen en el que asegura no haber participado. E...</span>
    </div><img src="images/ficha-nuevo.png" class="ficha-nuevo" /><a href="/descarga/43651/al-borde-del-abismo-man-on-a-ledge-dvdrip" >
    <img src="thumb_fichas/43651_m.jpg" alt="Imagen Al Borde del Abismo (Man on a Ledge) [DVDRip]" onmouseover="javascript:mostrar_descrip2(43651);" onmouseout="javascript:ocultar_descrip2(43651);"/></a>
    <a class="nombre-ficha" href="/descarga/43651/al-borde-del-abismo-man-on-a-ledge-dvdrip">Al Borde del Abi...</a>
    <span class="categoria">Peliculas - DVDRip...</span></li>
    '''
    
    patron  = '<li id="ficha-\d+" class="ficha2[^<]+'
    patron += '<div class="detalles-ficha"[^<]+'
    patron += '<span class="nombre-det">Ficha\: ([^<]+)</span>[^<]+'
    patron += '<span class="categoria-det">[^<]+</span>[^<]+'
    patron += '<span class="descrip-det">(.*?)</span>[^<]+'
    patron += '</div>.*?<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for title,plot,url,thumbnail in matches:
        scrapedtitle = title
        scrapedplot = plot
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin("http://www.bajui.com/",thumbnail.replace("_m.jpg","_g.jpg"))
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="enlaces", title=scrapedtitle , fulltitle=title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )

    # Extrae el paginador
    patron = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin("http://www.bajui.com/",matches[0])
        pagitem = Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl,fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg")
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )

    return itemlist

def enlaces(item):
    logger.info("[bajui.py] enlaces")
    itemlist = []
    '''
    <div class="box-enlace-cabecera">
    <div class="datos-usuario"><img class="avatar" src="images/avatars/118329_p.jpg" />Enlaces de: 
    <a class="nombre-usuario" href="/usuario/charlyjerico">charlyjerico</a> </div>
    <div class="datos-act">Actualizado: 02:01, 20-07-2012</div><div class="datos-gracias">7 gracias</div><div class="datos-boton-mostrar"><a id="boton-mostrar-183463" class="boton" href="javascript:mostrar_enlaces(183463);">Mostrar enlaces</a></div>
    <div class="datos-servidores"><div class="datos-servidores-cell"><img src="/images/servidores/bitshare.png" title="bitshare.com" border="0" alt="bitshare.com" /><img src="/images/servidores/freakshare.net.jpg" title="freakshare.com" border="0" alt="freakshare.com" /><img src="/images/servidores/rapidgator.png" title="rapidgator.net" border="0" alt="rapidgator.net" /><img src="/images/servidores/turbobit.png" title="turbobit.net" border="0" alt="turbobit.net" /><img src="/images/servidores/muchshare.png" title="muchshare.net" border="0" alt="muchshare.net" /><img src="/images/servidores/letitbit.png" title="letitbit.net" border="0" alt="letitbit.net" /><img src="/images/servidores/shareflare.png" title="shareflare.net" border="0" alt="shareflare.net" /><img src="/images/servidores/otros.gif" title="Otros servidores" border="0" alt="Otros" /></div></div>	
    </div>
    '''
    '''
    <div class="box-enlace-cabecera">
    <div class="datos-usuario"><img class="avatar" src="images/avatars/121466_p.jpg" />Enlaces de: 
    <a class="nombre-usuario" href="/usuario/yamil4466">yamil4466</a> </div>
    <div class="datos-act">Actualizado: Hace 2 horas</div><div class="datos-boton-mostrar"><a id="boton-mostrar-184320" class="boton" href="javascript:mostrar_enlaces(184320);">Mostrar enlaces</a></div>
    <div class="datos-servidores"><div class="datos-servidores-cell"><img src="/images/servidores/turbobit.png" title="turbobit.net" border="0" alt="turbobit.net" /><img src="/images/servidores/shareflare.png" title="shareflare.net" border="0" alt="shareflare.net" /><img src="/images/servidores/letitbit.png" title="letitbit.net" border="0" alt="letitbit.net" /><img src="/images/servidores/rapidshare.com.jpg" title="rapidshare.com" border="0" alt="rapidshare.com" /><img src="/images/servidores/2shared.gif" title="2shared.com" border="0" alt="2shared.com" /><img src="/images/servidores/jumbofiles.png" title="jumbofiles.com" border="0" alt="jumbofiles.com" /><img src="/images/servidores/putlocker.png" title="putlocker.com" border="0" alt="putlocker.com" /><img src="/images/servidores/zippyshare.png" title="zippyshare.com" border="0" alt="zippyshare.com" /><img src="/images/servidores/mediafire.com.png" title="mediafire.com" border="0" alt="mediafire.com" /></div></div>	
    
    </div>
    <div id="enlaces-184320"><img id="enlaces-cargando-184320" src="/images/cargando.gif" style="display:none;"/></div>
    </li>
    '''
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron  = '<div class="box-enlace-cabecera">[^<]+'
    patron += '<div class="datos-usuario"><img class="avatar" src="([^"]+)" />Enlaces[^<]+'
    patron += '<a class="nombre-usuario" href="[^"]+">([^<]+)</a> </div>[^<]+'
    patron += '<div class="datos-act">Actualizado. ([^<]+)</div>.*?<div class="datos-boton-mostrar"><a id="boton-mostrar-\d+" class="boton" href="javascript.mostrar_enlaces\((\d+)\)\;">Mostrar enlaces</a></div>[^<]+'
    patron += '<div class="datos-servidores"><div class="datos-servidores-cell">(.*?)</div></div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for thumbnail,usuario,fecha,id,servidores in matches:
        #<img src="/images/servidores/bitshare.png" title="bitshare.com" border="0" alt="bitshare.com" /><img src="/images/servidores/freakshare.net.jpg" title="freakshare.com" border="0" alt="freakshare.com" /><img src="/images/servidores/rapidgator.png" title="rapidgator.net" border="0" alt="rapidgator.net" /><img src="/images/servidores/turbobit.png" title="turbobit.net" border="0" alt="turbobit.net" /><img src="/images/servidores/muchshare.png" title="muchshare.net" border="0" alt="muchshare.net" /><img src="/images/servidores/letitbit.png" title="letitbit.net" border="0" alt="letitbit.net" /><img src="/images/servidores/shareflare.png" title="shareflare.net" border="0" alt="shareflare.net" /><img src="/images/servidores/otros.gif" title="Otros servidores" border="0" alt="Otros" />
        patronservidores = '<img src="[^"]+" title="([^"]+)"'
        matches2 = re.compile(patronservidores,re.DOTALL).findall(servidores)
        lista_servidores = ""
        for servidor in matches2:
            lista_servidores = lista_servidores + servidor + ", "
        lista_servidores = lista_servidores[:-2]

        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedurl = "http://www.bajui.com/ajax/mostrar-enlaces.php?id="+id
        scrapedplot=item.plot
        scrapedtitle="Enlaces de "+usuario+" ("+fecha+") ("+lista_servidores+")"

        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , context="4|5",fanart="http://pelisalacarta.mimediacenter.info/fanart/bajui.jpg") )

    return itemlist
        
def findvideos(item):
    logger.info("[bajui.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = item.plot
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.fulltitle
        
        parsed_url = urlparse.urlparse(videoitem.url)
        fichero = parsed_url.path
        partes = fichero.split("/")
        titulo = partes[ len(partes)-1 ]
        videoitem.title = titulo + " - [" + videoitem.server+"]"
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    import time
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto los buscadores)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            
            for item in itemlist:
                if item.action!="search":
                    exec "itemlist2 ="+item.action+"(item)"
                    
                    # Este canal tiene captcha...
                    time.sleep(5)
        
                    if len(itemlist2)==0:
                        return False

    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        lista_enlaces = enlaces(item=pelicula_item)
        for un_enlace in lista_enlaces:
            mirrors = findvideos(item=un_enlace)
            if len(mirrors)>0:
                bien = True
                break
        if bien:
            break

    return bien
