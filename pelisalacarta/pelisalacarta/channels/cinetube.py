# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "cinetube"
DEBUG = True

SESION = config.get_setting("session","cinetube")
LOGIN = config.get_setting("login","cinetube")
PASSWORD = config.get_setting("password","cinetube")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinetube.py] getmainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Películas"                , action="menupeliculas"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series"                   , action="menuseries"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales"             , action="menudocumentales"))
    itemlist.append( Item(channel=CHANNELNAME, title="Anime"                    , action="menuanime"))
    
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"                   , action="search") )   
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar por Actor/Director", action="search" , url="actor-director") )

    if SESION=="true":
        perform_login(LOGIN,PASSWORD)
        itemlist.append( Item(channel=CHANNELNAME, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=CHANNELNAME, title="Iniciar sesion", action="login"))

    return itemlist

def menupeliculas(item):
    logger.info("[cinetube.py] menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - Novedades"        , action="peliculas"        , url="http://www.cinetube.es/peliculas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - Estrenos de Cine" , action="documentales"     , url="http://www.cinetube.es/peliculas/estrenos-de-cine/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - Estrenos en DVD"  , action="documentales"     , url="http://www.cinetube.es/peliculas/estrenos-dvd/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - Nueva Calidad"    , action="documentales"     , url="http://www.cinetube.es/peliculas/nueva-calidad/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - A-Z"              , action="listalfabetico"   , url="peliculas"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas - Categorías"       , action="listcategorias"   , url="peliculas"))
    
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar Películas"             , action="search"           , url="peliculas") )

    return itemlist

def menuseries(item):
    logger.info("[cinetube.py] menuseries")

    itemlist = []

    itemlist.append( Item(channel=CHANNELNAME, title="Series - Novedades"           , action="series"           , url="http://www.cinetube.es/series/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series - A-Z"                 , action="listalfabetico"   , url="series"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series - Listado completo"    , action="completo"         , url="http://www.cinetube.es/series-todas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series - Categorías"          , action="listcategorias"   , url="series"))

    itemlist.append( Item(channel=CHANNELNAME, title="Buscar Series"                , action="search"           , url="series") )

    return itemlist

def menudocumentales(item):
    logger.info("[cinetube.py] menudocumentales")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Novedades"         , action="documentales"     , url="http://www.cinetube.es/documentales/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - A-Z"               , action="listalfabetico"   , url="documentales"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Listado completo"  , action="completo"         , url="http://www.cinetube.es/documentales-todos/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documentales - Categorías"        , action="listcategorias"   , url="documentales"))

    itemlist.append( Item(channel=CHANNELNAME, title="Buscar Documentales"              , action="search"           , url="documentales") )

    return itemlist

def menuanime(item):
    logger.info("[cinetube.py] menuanime")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Series Anime - Novedades"             , action="series"           , url="http://www.cinetube.es/series-anime/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series Anime - A-Z"                   , action="listalfabetico"   , url="series-anime" ))
    itemlist.append( Item(channel=CHANNELNAME, title="Series Anime - Listado completo"      , action="completo"         , url="http://www.cinetube.es/series-anime-todas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series Anime - Categorías"            , action="listcategorias"   , url="series-anime"))
                     
    itemlist.append( Item(channel=CHANNELNAME, title="Películas Anime - Novedades"          , action="documentales"     , url="http://www.cinetube.es/peliculas-anime/") )
    itemlist.append( Item(channel=CHANNELNAME, title="Películas Anime - A-Z"                , action="listalfabetico"   , url="peliculas-anime" ))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas Anime - Listado completo"   , action="completo"         , url="http://www.cinetube.es/peliculas-anime-todas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Películas Anime - Categorías"         , action="listcategorias"   , url="peliculas-anime"))

    itemlist.append( Item(channel=CHANNELNAME, title="Buscar Anime"                         , action="search"           , url="anime") )

    return itemlist

def perform_login(login,password):
    # Invoca al login, y con eso se quedarán las cookies de sesión necesarias
    login = login.replace("@","%40")
    data = scrapertools.cache_page("http://www.cinetube.es/login.php",post="usuario=%s&clave=%s" % (login,password))

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , CHANNELNAME+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    import xbmc
    keyboard = xbmc.Keyboard("","Login")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        login = keyboard.getText()

    keyboard = xbmc.Keyboard("","Password")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        password = keyboard.getText()

    nombre_fichero_config_canal = os.path.join( config.get_data_path() , CHANNELNAME+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Sesión iniciada", action="mainlist"))
    return itemlist
def prueba (item):
    itemlist = []
    itemlist = (search(item,"dragon ball","S"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[cinetube.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    if "*" in categoria:
        url = "none"
    elif "F" in categoria:
        url = "peliculas"
    elif "S" in categoria:
        url = "series"
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        # Series
        if url=="series" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/series/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(series(item))
        
        # Películas
        if url=="peliculas" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/peliculas/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(peliculas(item))
        
        # Documentales
        if item.url=="documentales" or url=="" or url=="none":
            item.url="http://www.cinetube.es/buscar/peliculas/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(documentales(item))
            
        # Anime
        if url=="anime" or url=="" or url=="none" or "F" in categoria:
            # Peliculas-anime
            item.url="http://www.cinetube.es/buscar/peliculas-anime/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(documentales(item))
        if url=="anime" or url=="" or url=="none" or "S" in categoria:
            # Series-anime
            item.url="http://www.cinetube.es/buscar/series-anime/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(series(item))

        # Actor/Director
        if url=="actor-director":
            item.url="http://www.cinetube.es/buscar/actor-director/?palabra=%s&categoria=&valoracion="
            item.url = item.url % texto
            itemlist.extend(peliculas(item))          
    
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item,paginacion=True):
    logger.info("[cinetube.py] peliculas")

    url = item.url

    # Descarga la página
    data = scrapertools.cachePage(url)

    # Extrae las entradas
    patronvideos  = '<!--PELICULA-->[^<]+'
    patronvideos += '<div class="peli_item textcenter">[^<]+'
    patronvideos += '<div class=[\W]pelicula_img[\W]><a href=.*?.html[^>]+>[^<]+'
    patronvideos += '<img src=["|\']([^"]+?)["|\'][^<]+</a>[^<]+'
    patronvideos += '</div[^<]+<a href=["|\']([^"]+?)["|\'].*?<p class="white">([^<]+)</p>.*?<p><span class="rosa">([^>]+)</span></p><div class="icos_lg">(.*?)</div>'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2] + " [" + match[3] + "]"
        '''
        matchesconectores = re.compile('<img.*?alt="([^"]*)"',re.DOTALL).findall(match[4])
        conectores = ""
        for matchconector in matchesconectores:
            logger.info("matchconector="+matchconector)
            if matchconector=="":
                matchconector = "megavideo"
            conectores = conectores + matchconector + "/"
        if len(matchesconectores)>0:
            scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("descarga directa","DD")
        '''

        # Convierte desde UTF-8 y quita entidades HTML
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        # procesa el resto
        scrapedplot = ""

        scrapedurl = urlparse.urljoin("http://www.cinetube.es/",match[1])
        scrapedthumbnail = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    # Extrae el paginador
    #<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
    patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(url,matches[0])
        pagitem = Item(channel=CHANNELNAME, action="peliculas", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )
        
    return itemlist

def documentales(item):
    logger.info("[cinetube.py] documentales")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    '''
    <!--PELICULA-->
    <div class="peli_item textcenter peli_item_puntos"><a href="/peliculas/drama/ver-pelicula-somewhere.html">
    <div class="pelicula_img">
    <img src="http://caratulas.cinetube.es/pelis/10070.jpg" alt="Somewhere" />
    </div></a>
    <a href="/peliculas/drama/ver-pelicula-somewhere.html" ><div class="estreno"></div></a>                                        <a href="/peliculas/drama/ver-pelicula-somewhere.html" title="Ver estreno Somewhere"><p class="white">Somewhere</p></a>
    <p><span class="rosa">BLURAY-SCREENER</span></p><div class="icos_lg"><img src="http://caratulas.cinetube.es/img/cont/espanol.png" alt="" /><img src="http://caratulas.cinetube.es/img/cont/downupload.png" alt="" /><img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="" /><img src="http://caratulas.cinetube.es/img/cont/ddirecta.png" alt="descarga directa" /> </div><div class="puntos_box">
    <div id="votos_media">6,2</div>
    <div id="votos_votaciones">48 votos</div>
    </div>
    </div>
    <!--FIN PELICULA-->
    '''
    patronvideos  = '<!--PELICULA-->[^<]+'
    patronvideos += '<div class="peli_item textcenter[^<]+<a href="([^"]+)">[^<]+'
    patronvideos += '<div class="pelicula_img">[^<]+'
    patronvideos += '<img src="([^"]+)" alt="([^"]+)"'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        
        # Convierte desde UTF-8 y quita entidades HTML
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        if match[0].startswith("/documentales/serie-documental"):
            itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle+" (serie)" , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
        else:
            itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    # Extrae el paginador
    #<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
    patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="documentales", title="!Página siguiente" , url=scrapedurl) )

    return itemlist

# Pone todas las series del listado alfabético juntas, para no tener que ir entrando una por una
def completo(item):
    logger.info("[cinetube.py] completo()")
    
    url = item.url
    siguiente = True
    itemlist = []
    
    data = scrapertools.cachePage(url)
    patronpag  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
    while siguiente==True:
    
        patron = '<!--SERIE-->.*?<a href="([^"]+)" .*?>([^<]+)</a></span></li>.*?<!--FIN SERIE-->'
        matches = re.compile(patron,re.DOTALL).findall(data)
        for match in matches:
            scrapedtitle = match[1]
            # Convierte desde UTF-8 y quita entidades HTML
            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            
            scrapedplot = ""
            scrapedurl = urlparse.urljoin(url,match[0])
            scrapedthumbnail = ""    

            itemlist.append( Item(channel=CHANNELNAME, action="temporadas", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle, show=scrapedtitle) )

        # Extrae el paginador
        matches = re.compile(patronpag,re.DOTALL).findall(data)
        if len(matches)==0:
            siguiente = False
        else:
            data = scrapertools.cachePage(urlparse.urljoin(url,matches[0]))

    return itemlist

def listalfabetico(item):
    logger.info("[cinetube.py] listalfabetico("+item.url+")")
    
    action = item.url
    if item.url=="series-anime":
        action="series"
    if item.url=="peliculas-anime":
        action="documentales"
    
    baseurl = "http://www.cinetube.es/"+item.url+"/"
    
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="0-9", url=baseurl+"0-9/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="A"  , url=baseurl+"A/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="B"  , url=baseurl+"B/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="C"  , url=baseurl+"C/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="D"  , url=baseurl+"D/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="E"  , url=baseurl+"E/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="F"  , url=baseurl+"F/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="G"  , url=baseurl+"G/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="H"  , url=baseurl+"H/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="I"  , url=baseurl+"I/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="J"  , url=baseurl+"J/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="K"  , url=baseurl+"K/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="L"  , url=baseurl+"L/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="M"  , url=baseurl+"M/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="N"  , url=baseurl+"N/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="O"  , url=baseurl+"O/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="P"  , url=baseurl+"P/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="Q"  , url=baseurl+"Q/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="R"  , url=baseurl+"R/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="S"  , url=baseurl+"S/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="T"  , url=baseurl+"T/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="U"  , url=baseurl+"U/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="V"  , url=baseurl+"V/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="W"  , url=baseurl+"W/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="X"  , url=baseurl+"X/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="Y"  , url=baseurl+"Y/"))
    itemlist.append( Item(channel=CHANNELNAME, action=action , title="Z"  , url=baseurl+"Z/"))

    return itemlist

def listcategorias(item):
    logger.info("[cinetube.py] listcategorias")
    
    action = item.url
    if item.url=="series-anime":
        action="series"
    if item.url=="peliculas-anime":
        action="documentales"
        
    # Descarga la página
    url = urlparse.urljoin("http://www.cinetube.es/",item.url)
    data = scrapertools.cachePage(url)

    # Extrae las entradas
    patronvideos  = '<ul class="categorias">(.*?)</ul>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    if len(matches)==0:
        return []

    data = matches[0]
    patronvideos  = '<li><a href="([^"]+)"><span>([^<]+)</span></a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    itemlist = []
    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[1])
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://www.cinetube.es/",match[0])
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )

    return itemlist

def series(item):
    logger.info("[cinetube.py] series")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("Pagina de %d caracteres" % len(data))

    # Extrae las entradas
    '''
    <li>
    <a href="/series/en-tierra-de-lobos/temporada-1/capitulo-12/"><img src="http://caratulas.cinetube.es/series/8912.jpg" alt="peli" /></a>
    <div class="icos_lg"><img src="http://caratulas.cinetube.es/img/cont/espanol.png" alt="espanol" /> <img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="megavideo.png" /> <img src="http://caratulas.cinetube.es/img/cont/ddirecta.png" alt="descarga directa" /> <p><span class="rosa"></span></p></div>
    <p class="tit_ficha"><a class="tit_ficha" title="Ver serie Tierra de lobos" href="/series/en-tierra-de-lobos/temporada-1/capitulo-12/">Tierra de lobos </a></p>
    <p class="tem_fich">1a Temporada - Cap 12</p>
    </li>
    '''
    '''
    <li>
    <a href="/series/gabriel-un-amor-inmortal/"><img src="http://caratulas.cinetube.es/series/7952.jpg" alt="peli" /></a>
    <div class="icos_lg"><img src="http://caratulas.cinetube.es/img/cont/latino.png" alt="" /><img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="" /><img src="http://caratulas.cinetube.es/img/cont/ddirecta.png" alt="descarga directa" /> </div>                                        
    <p class="tit_ficha">Gabriel, un amor inmortal </p>
    </li>
    '''
    '''
    <li>
    <a href="/series-anime/star-driver-kagayaki-no-takuto/temporada-1/capitulo-13/"><img src="http://caratulas.cinetube.es/seriesa/9009.jpg" alt="peli" /></a>
    <div class="icos_lg"><img src="http://caratulas.cinetube.es/img/cont/sub.png" alt="sub" /> <img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="megavideo.png" /> <img src="http://caratulas.cinetube.es/img/cont/ddirecta.png" alt="descarga directa" /> <p><span class="rosa"></span></p></div>
    <p class="tit_ficha"><a class="tit_ficha" title="Ver serie Star Driver Kagayaki no Takuto" href="/series-anime/star-driver-kagayaki-no-takuto/temporada-1/capitulo-13/">Star Driver Kagayaki no Takuto </a></p>
    <p class="tem_fich">1a Temporada - Cap 13</p>
    </li>
    '''
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a href="([^"]+)"><img src="([^"]+)"[^>]*></a>[^<]+'
    patronvideos += '<div class="icos_lg">(.*?)</div>[^<]+'
    patronvideos += '<p class="tit_ficha">(.*?)</p>[^<]+'
    patronvideos += '(?:<p class="tem_fich">([^<]+)</p>)?'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[3].strip()
        if len(match)>=5:
            scrapedtitle = scrapedtitle+" "+match[4]
        '''
        matchesconectores = re.compile('<img.*?alt="([^"]*)"',re.DOTALL).findall(match[2])
        conectores = ""
        for matchconector in matchesconectores:
            logger.info("matchconector="+matchconector)
            if matchconector=="":
                matchconector = "megavideo"
            conectores = conectores + matchconector + "/"
        if len(matchesconectores)>0:
            scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("megavideo/megavideo","megavideo")
        scrapedtitle = scrapedtitle.replace("descarga directa","DD")
        '''
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle

        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="temporadas", title=scrapedtitle , fulltitle= fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle, show=scrapedtitle) )

    # Paginador
    #<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
    patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="series", title="!Página siguiente" , url=scrapedurl) )

    return itemlist

def temporadas(item):
    logger.info("[cinetube.py] temporadas")
    itemlist = []
    fulltitle = item.fulltitle
    # extra = item.extra
    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Busca el argumento
    patronvideos  = '<div class="content">.*?<p>(.*?)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedplot = scrapertools.htmlclean(matches[0])
        logger.info("plot actualizado en detalle");
    else:
        logger.info("plot no actualizado en detalle");

    # Busca las temporadas
    patron = '<div class="temporadas">.*?<tbody>(.*?)</tbody>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        data = matches[0]
    
    patron  = '<tr><td[^>]+></td>[^<]+'
    patron += '<td><a href="([^"]+)">([^<]+)</a></td>[^<]+'
    patron += '<td>([^<]+)</td>[^<]+'
    patron += '<td><img src="[^"]+" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()+" ("+match[2]+", "+match[3]+")"
        # directory = match[1].strip()
        extra = match[1].strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, extra=extra, show=item.show) )

    # Una trampa, si la serie enlaza no con la temporada sino con la lista de episodios, se resuelve aquí
    if len(itemlist)==0:
        itemlist = episodios(item)
        
    # Si la serie lleva directamente a la página de detalle de un episodio (suele pasar en novedades) se detecta aquí
    if len(itemlist)==0:
        itemlist.extend(findvideos(item))

    return itemlist

def episodios(item):
    '''
    <li>
    <span class="link"><a href="/series/star-wars-las-guerras-clon/temporada-1/capitulo-13/">Star Wars: Las Guerras Clon 1x13 </a></span>
    <dl>
    <dt>Información</dt>
    <dd class="n"><img src="http://caratulas.cinetube.es/img/cont/espanol.png" alt="Español" /></dd><dd class="n"><img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="megavideo.png" /></dd><dd class="n"><img src="http://caratulas.cinetube.es/img/cont/ddirecta.png" alt="Descarga" /></dd>											</dl>
    <p><span><a id="novisto_27325" class="novisto" onclick="cap_yavisto('27325',1,1)">No Visto</a></span> <span><a href="/series/star-wars-las-guerras-clon/temporada-1/capitulo-13/">Ver Ficha</a></span></p>
        </li>
    '''
    logger.info("[cinetube.py] episodios")
    extra = item.extra
    # directory = item.directory
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Busca los episodios
    patron  = '<li>[^<]+'
    patron += '<span class="link"><a href="([^"]+)">([^<]+)</a></span>[^<]+'
    patron += '<dl>[^<]+'
    patron += '<dt>Info[^<]+</dt>[^<]+'
    patron += '<dd class="n"><img src="[^"]+" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()

        # Convierte desde UTF-8 y quita entidades HTML
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail, extra=extra+" "+scrapedtitle, plot=scrapedplot, show=item.show) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[cinetube.py] findvideos")

    try:
        url = item.url
        title = item.title
        fulltitle = item.fulltitle
        extra = item.extra
        thumbnail = item.thumbnail
        plot = item.plot
    
        # Descarga la pagina
        data = scrapertools.cachePage(url)
        #logger.info(data)
        
        # Busca el argumento
        patronvideos  = '<meta name="description" content="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        if len(matches)>0:
            plot = scrapertools.htmlclean(matches[0])
            logger.info("plot actualizado en detalle");
        else:
            logger.info("plot no actualizado en detalle");
    
        # Busca los enlaces a los mirrors, o a los capitulos de las series...
        '''
        FORMATO EN SERIES
        <div class="tit_opts"><a href="/series/hawai-five/temporada-1/capitulo-13/212498.html">
        <p>Opción 1: Ver online en Megavideo <span class="bold"></span></p>
        <p><span>IDIOMA: SUB</span></p>
        <p class="v_ico"><img src="http://caratulas.cinetube.es/img/cont/megavideo.png" alt="Megavideo" /></p>
        '''
        patronvideos = '<div class="tit_opts"><a href="([^"]+)"[^>]*>[^<]+'
        patronvideos += '<p>(.*?)</p>[^<]+'
        patronvideos += '<p><span>(.*?)</span>'
        '''
        patronvideos = '<div class="tit_opts"><a href="([^"]+)".*?>[^<]+'
        patronvideos += '<p>([^<]+)</p>[^<]+'
        patronvideos += '<p><span>(.*?)</span>'
        '''
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
        itemlist = []
        for match in matches:
            logger.info("Encontrado iframe mirrors "+match[0])
            # Lee el iframe
            mirror = urlparse.urljoin(url,match[0].replace(" ","%20"))
            data = scrapertools.cache_page(mirror)
            #logger.info("-------------------------------------------------------------------------------------")
            #logger.info(data)
            #logger.info("-------------------------------------------------------------------------------------")
            '''
            req = urllib2.Request(mirror)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            '''
            patron='ct_url_decode\("([^"]+)"\)'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if len(matches)>0:
                data = matches[0]
                logger.info("-------------------------------------------------------------------------------------")
                logger.info(data)
                logger.info("-------------------------------------------------------------------------------------")
                data = ct_url_decode(data)
                logger.info("-------------------------------------------------------------------------------------")
                logger.info(data)
                logger.info("-------------------------------------------------------------------------------------")
    
            listavideos = servertools.findvideos(data)
            
            for video in listavideos:
                #scrapedtitle = title.strip() + " " + match[1] + " " + match[2] + " " + video[0]
                scrapedtitle = match[1] + " " + match[2] + " " + video[0]
                scrapedtitle = scrapertools.htmlclean(scrapedtitle)
                scrapedurl = video[1]
                server = video[2]
                
                itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl, thumbnail=item.thumbnail, plot=plot, server=server, extra=extra, fanart=item.thumbnail, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        
    return itemlist

def ct_url_decode(C):
    if not(C):
        return C
    
    C = C[::-1]
    X = 4-len(C)%4;
    if X in range(1,4):
        for z in range(X):
            C = C+"="
    
    import base64
    return base64.decodestring(C)
