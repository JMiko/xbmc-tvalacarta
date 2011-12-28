# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para nolomires.com by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import config
from core import logger
from platformcode.xbmc import xbmctools
from core.item import Item
from servers import servertools
from servers import vk
from pelisalacarta import buscador

__channel__ = "nolomires"
__category__ = "F"
__type__ = "xbmc"
__title__ = "NoloMires"
__language__ = "ES"

DEBUG = config.get_setting("debug")

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[nolomires.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[nolomires.py] mainlist")

    # A�ade al listado de XBMC
    xbmctools.addnewfolder( __channel__ , "search" , category , "Buscar","http://www.nolomires.com/","","")
    xbmctools.addnewfolder( __channel__ , "LastSearch" , category , "Peliculas Buscadas Recientemente","http://www.nolomires.com/","","")
    xbmctools.addnewfolder( __channel__ , "listvideosMirror" , category , "Ultimos Estrenos","http://www.nolomires.com/","","")
    #xbmctools.addnewfolder( __channel__ , "TagList"         , category , "Tag de Estrenos por a�o"    ,"http://www.nolomires.com/","","")
    xbmctools.addnewfolder( __channel__ , "MostWatched" , category , "Peliculas Mas Vistas","http://www.nolomires.com/","","")
    xbmctools.addnewfolder( __channel__ , "ListaCat"         , category , "Listado por Categorias"    ,"http://www.nolomires.com/","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"       , category , "Ultimas Pel�culas A�adidas"    ,"http://www.nolomires.com/category/peliculas-en-nolomires/","","")
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def searchresults(params,Url,category):
    logger.info("[nolomires.py] search")


    buscador.salvar_busquedas(params,Url,category)        
    Url = Url.replace(" ", "+")
    searchUrl = "http://www.nolomires.com/?s="+Url+"&x=15&y=19"
    listvideos(params,searchUrl,category)


def search(params,Url,category):
    
    buscador.listar_busquedas(params,Url,category)

def ListaCat(params,url,category):
    logger.info("[nolomires.py] ListaCat")
    
    
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Acci�n","http://www.nolomires.com/category/peliculas-de-accion/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Animado","http://www.nolomires.com/category/peliculas-de-animacion/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Anime","http://www.nolomires.com/category/anime/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Aventura","http://www.nolomires.com/category/peliculas-de-aventura/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "B�lico Guerra ","http://www.nolomires.com/category/peliculas-de-guerra/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Ciencia-Ficci�n","http://www.nolomires.com/category/peliculas-de-ciencia-ficcion/","","")
    #xbmctools.addnewfolder( __channel__ ,"listvideosMirror", category , "Cl�sicos","http://www.nolomires.com/category/peliculasclasicos/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Comedia","http://www.nolomires.com/category/peliculas-de-comedia/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Documentales","http://www.nolomires.com/category/peliculas-sobre-documentales/","","")
    #xbmctools.addnewfolder( __channel__ ,"listvideosMirror", category , "Destacado","http://www.nolomires.com/category/peliculasdestacado/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Documentales Online","http://www.nolomires.com/category/documentales-online-completos/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Drama","http://www.nolomires.com/category/peliculas-de-drama/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Entretenimiento","http://www.nolomires.com/category/entretenimiento/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Estrenos","http://www.nolomires.com/category/ultimos-extrenos/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "General","http://www.nolomires.com/category/general/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Intriga","http://www.nolomires.com/category/peliculas-de-intriga/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Musicales","http://www.nolomires.com/category/peliculas-musicales/","","")
    #xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Peliculas HD","http://www.nolomires.com/category/peliculaspeliculas-hd-categorias/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Romance","http://www.nolomires.com/category/peliculas-sobre-romance/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Suspenso","http://www.nolomires.com/category/peliculas-de-suspenso/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Terror","http://www.nolomires.com/category/peliculas-de-terror/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Thriller","http://www.nolomires.com/category/peliculas-de-thriller/","","")
    xbmctools.addnewfolder( __channel__ ,"listvideos", category , "Todas las Peliculas","http://www.nolomires.com/category/peliculas-en-nolomires/","","")
    
    
    
    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )



        
def TagList(params,url,category):
    logger.info("[nolomires.py] TagList")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Patron de las entradas
    patronvideos  = "<a href='([^']+)' class='[^']+' title='[^']+' style='[^']+'"          # URL
    patronvideos += ">([^<]+)</a>"                                                         # TITULO
      
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # A�ade las entradas encontradas
    for match in matches:
        # Atributos
        scrapedtitle = acentos(match[1])
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )


    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        
def MostWatched(params,url,category):
    logger.info("[nolomires.py] MostWatched")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Patron de las entradas
    patronvideos  = '<li><a href="([^"]+)"  '      # URL
    patronvideos += 'title="([^"]+)">[^<]+'        # TITULO
    patronvideos += '</a>([^<]+)</li>'             # Cantidad de Vistos
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # A�ade las entradas encontradas
    for match in matches:
        # Atributos
        scrapedtitle = acentos(match[1] + match[2])
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )


    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def LastSearch(params,url,category):
    logger.info("[nolomires.py] LastSearch")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Patron de las entradas
    patronvideos  = '<li><a href="([^"]+)" '      # URL
    patronvideos += 'title="([^"]+)">[^<]+'       # TITULO
    patronvideos += '</a></li>'                    # Basura
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # A�ade las entradas encontradas
    for match in matches:
        # Atributos
        scrapedtitle = acentos(match[1])
        scrapedtitle = scrapedtitle.replace("online","").replace("ver ","")
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )


    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

 
def listvideos(params,url,category):
    logger.info("[nolomires.py] listvideos")

    if url=="":
        url = "http://www.nolomires.com/"
                
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    patronvideos  =  '<div class="videoitem">.*?<a href="([^"]+)" '     # URL 0
    patronvideos +=  'title="([^"]+)">'                                 # TITULO 1
    patronvideos +=  '<img style="background: url\(([^\)]+)\)"'         # IMAGEN  2
    #patronvideos += '</div>[^<]+<div class=[^>]+>.*?href="[^"]+"><img '                    
    #patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  # IMAGEN , DESCRIPCION
    #patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        
        scrapedtitle = acentos(match[1])
        # URL
        scrapedurl = match[0]
        # Thumbnail
        scrapedthumbnail = match[2]
        # Argumento
        scrapedplot = ""
        

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        
            # A�ade al listado de XBMC
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    #Extrae la marca de siguiente p�gina
    patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        pag = re.compile("http.*?/page/([^/]+)/").findall(matches[0])
        scrapedtitle = "P�gina siguiente (Nro.%s)" %pag[0]
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listvideosMirror(params,url,category):
    logger.info("[nolomires.py] listvideosMirror")

    if url=="":
        url = "http://www.nolomires.com/"
                
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    patronvideos  =  '<div class="panel" id="[^"]+" style="background: url\(([^\)]+)\).*?'      # IMAGEN   0
    patronvideos +=  '<h2><a href="([^"]+)" '                                                  # URL      1
    patronvideos +=  'title="([^"]+)">[^<]+</a>'                                               # TITULO   2
    patronvideos += '</h2>(.*?)</div>'                                                         # SINOPSIS 3
    #patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                 
    #patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                     
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        
        scrapedtitle = acentos(match[2])
        # URL
        scrapedurl = match[1]
        # Thumbnail
        scrapedthumbnail = match[0]
        # Argumento
        scrapedplot = match[3]
        

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        
            # A�ade al listado de XBMC
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    #Extrae la marca de siguiente p�gina
    patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P�gina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def detail(params,url,category):
    logger.info("[nolomires.py] detail")

    title = acentos(urllib.unquote_plus( params.get("title") ))
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = ""
    scrapedurl = ""
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    # Extrae el argumento
    patronarg = '<h[2-3]>(<span style.*?)</p>'
    matches   = re.compile(patronarg,re.DOTALL).findall(data)
    if len(matches)>0:
        plot  = re.sub("<[^>]+>"," ",matches[0])
    patronthumb = '<div id="textimg"><img src="([^"]+)"'
    matches   = re.compile(patronthumb,re.DOTALL).findall(data)
    if len(matches)>0:
        thumbnail = matches[0]
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos en los servidores habilitados
    # ------------------------------------------------------------------------------------
    
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        
        videotitle = video[0]
        url = video[1]
        server = video[2]
        xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
    
   
            
    ## --------------------------------------------------------------------------------------##
    #               Busca enlaces a videos .flv o (.mp4 dentro de un xml)                     #
    ## --------------------------------------------------------------------------------------##
    patronvideos = 'file=(http\:\/\/[^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    playWithSubt = "play"
    c = 0
    if len(matches)>0:
        for match in matches:
            print "link xml :%s" %match
            subtitle = "[FLV-Directo]"
            c += 1
            sub = ""
            if ("/xml" in match):
                data2 = scrapertools.cachePage(match)
                logger.info("data2="+data2)
                patronvideos  = '<track>.*?'
                patronvideos += '<title>([^<]+)</title>[^<]+'
                patronvideos += '<location>([^<]+)</location>(?:[^<]+'
                patronvideos += '<meta rel="type">video</meta>[^<]+|[^<]+)'
                patronvideos += '<meta rel="captions">([^<]+)</meta>[^<]+'
                patronvideos += '</track>'
                matches2 = re.compile(patronvideos,re.DOTALL).findall(data2)
                scrapertools.printMatches(matches)
                if len(matches2)==0:
                    newpatron = '<title>([^<]+)</title>[^<]+<location>([^<]+)</location>'
                    matches2 = re.compile(newpatron,re.DOTALL).findall(data2)
                    sub = "None"
                for match2 in matches2:
                    
                    try:
                        if match2[2].endswith(".xml"): # Subtitulos con formato xml son incompatibles con XBMC
                            sub = "[Subtitulo incompatible con xbmc]"
                            playWithSubt = "play"
                    except:
                        pass
                    if ".mp4" in match2[1]:
                        subtitle = "[MP4-Directo]"
                    scrapedtitle = '%s (castellano) - %s  %s' %(title,match2[0],subtitle)
                    
                    scrapedurl = match2[1].strip()
                    scrapedthumbnail = thumbnail
                    scrapedplot = plot
                    if ("cast.xml" or "mirror.xml") not in match and sub == "":
                        scrapedtitle = '%s (V.O.S) - %s  %s %s' %(title,match2[0],subtitle,sub)
                        try:
                            if not match2[2].endswith("cine-adicto2.srt") and (sub == ""): 
                                scrapedurl = scrapedurl + "|" + match2[2]
                                playWithSubt = "play2"
                        except:pass    
                    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                            
                    # A�ade al listado de XBMC
                    xbmctools.addnewvideo( __channel__ , playWithSubt , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )
                
            else:
                if match.endswith(".srt"):
                    scrapedurl = scrapedurl + "|" + match 
                    xbmctools.addnewvideo( __channel__ ,"play2"  , category , "Directo" , title + " (V.O.S) - "+subtitle, scrapedurl , thumbnail , plot )
                if     match.endswith(".xml"):
                    sub = "[Subtitulo incompatible con xbmc]"
                    xbmctools.addnewvideo( __channel__ ,"play"  , category , "Directo" , title + " (V.O) - %s %s" %(subtitle,sub), scrapedurl , thumbnail , plot )
                scrapedurl = match
                print scrapedurl

    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces de videos para el servidor vk.com                             #
    ## --------------------------------------------------------------------------------------##
    #http://vkontakte.ru/video_ext.php?oid=93103247&id=149051583&hash=793cde84b05681fa&hd=1
    '''
    patronvideos = '(http\:\/\/vk.+?\/video_ext\.php[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            print " encontro VK.COM :%s" %match
            videourl =    scrapertools.unescape(match)
            xbmctools.addnewvideo( __channel__ , "play" , category , "vk" , title + " - "+"[VK]", videourl , thumbnail , plot )
    '''
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[nolomires.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]

    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)

def play2(params,url,category):
    logger.info("[nolomires.py] play2")
    url1 = url
    if "|" in url:
        urlsplited = url.split("|")
        url1 = urlsplited[0]
        urlsubtit = urlsplited[1]
        subt_ok = "0"
        while subt_ok == "0":
            subt_ok = downloadstr(urlsubtit)
            print "subtitulo subt_ok = %s" % str(subt_ok)
            if subt_ok is None: # si es None la descarga del subtitulo esta ok
                config.set_setting("subtitulo", "true")
                break
    play(params,url1,category)


def acentos(title):

        title = title.replace("&#8211;","-")
        title = title.replace("&nbsp;"," ")
        title = title.replace("Â�", "")
        title = title.replace("Ã©","�")
        title = title.replace("Ã¡","�")
        title = title.replace("Ã³","�")
        title = title.replace("Ãº","�")
        title = title.replace("Ã­","�")
        title = title.replace("Ã±","�")
        title = title.replace("â€", "")
        title = title.replace("â€œÂ�", "")
        title = title.replace("â€œ","")
        title = title.replace("é","�")
        title = title.replace("á","�")
        title = title.replace("ó","�")
        title = title.replace("ú","�")
        title = title.replace("í","�")
        title = title.replace("ñ","�")
        title = title.replace("Ã“","�")
        return(title)
        
        
def downloadstr(urlsub):
    
    import downloadtools
    
    fullpath = os.path.join( config.DATA_PATH, 'subtitulo.srt' )
    if os.path.exists(fullpath):
        try:
            subtitfile = open(fullpath,"w")
            subtitfile.close()
        except IOError:
            logger.info("Error al limpiar el archivo subtitulo.srt "+fullpath)
            raise
    try:        
        ok = downloadtools.downloadfile(urlsub,fullpath)
    except IOError:
        logger.info("Error al descargar el subtitulo "+urlsub)
        return -1
    return ok

def getpost(url,values): # Descarga la pagina con envio de un Form
    
    #url=url
    try:
        data = urllib.urlencode(values)          
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read() 
        return the_page 
    except Exception: 
        return "Err "     
