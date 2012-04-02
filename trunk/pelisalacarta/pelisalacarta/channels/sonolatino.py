# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para sonolatino.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from core import downloadtools

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

__channel__ = "sonolatino"
__category__ = "M"
__type__ = "xbmc"
__title__ = "Sonolatino"
__language__ = ""

DEBUG = config.get_setting("debug")

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

logger.info("[sonolatino.py] init")

IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_data_path(), 'resources' , 'images' , 'posters' ) )


def mainlist(params,url,category):
    logger.info("[sonolatino.py] mainlist")
    
    xbmctools.addnewfolder( __channel__ , "Videosnuevos"  , category , "Videos Musicales - Nuevos"           ,"http://www.sonolatino.com/newvideos.html","","")
    xbmctools.addnewfolder( __channel__ , "TipoVideo"     , category , "Videos Musicales - Categorias"       ,"","","")
    #xbmctools.addnewfolder( __channel__ , "tagvideos"  , category , "Tag de Videos","http://www.sonolatino.com/index.html",os.path.join(IMAGES_PATH, 'tag.png'),"")
    xbmctools.addnewfolder( __channel__ , "topVideos"     , category , "Top Videos Musicales Online"         ,"http://www.sonolatino.com/topvideos.html","","")
    xbmctools.addnewfolder( __channel__ , "listatipoVideo", category , "Videos Musicales Siendo Vistas Ahora","http://www.sonolatino.com/index.html","","")
    xbmctools.addnewfolder( __channel__ , "Videodeldia"   , category , "Video Musical del dia"               ,"http://www.sonolatino.com/index.html","","")
    xbmctools.addnewfolder( __channel__ , "search"          , category , "Buscar"                              ,"","","")
    #xbmctools.addnewfolder( __channel__ , "creartag"           , category , "Crear la lista de categorias","http://www.sonolatino.com/",tecleadoultimo,os.path.join(IMAGES_PATH, 'search_icon.png'),"")
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

      
##############------------------------------------------------------#################    

def search(params,url,category):
    logger.info("[sonolatino.py] search")
    buscador.listar_busquedas(params,url,category)
    
def searchresults(params,url,category):
    logger.info("[sonolatino.py] search")
        
    buscador.salvar_busquedas(params,url,category)
    
    #convert to HTML
    tecleado = url.replace(" ", "+")
    searchUrl = "http://www.sonolatino.com/search.php?keywords="+tecleado+"&btn=Buscar"
    searchresults2(params,searchUrl,category)



###############---------------------------------------------------#####################

def performsearch(texto):
    logger.info("[sonolatino.py] performsearch")
    url = "http://www.sonolatino.com/search.php?keywords="+texto+"&btn=Buscar"

    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    patronvideos = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)">'
    patronvideos += '[^<]+<img src="([^"]+)"  '
    patronvideos += 'alt="([^"]+)"[^>]+><div class="tag".*?</div>.*?'
    patronvideos += '<span class="artist_name">([^<]+)</span>'    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    resultados = []

    for match in matches:
        scrapedtitle = acentos(match[2])
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        resultados.append( [__channel__ , "detail" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
        
    return resultados

def searchresults2(params,url,category):
    logger.info("[sonolatino.py] searchresults")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)">'
    patronvideos += '[^<]+<img src="([^"]+)"  '
    patronvideos += 'alt="([^"]+)"[^>]+><div class="tag".*?</div>.*?'
    patronvideos += '<span class="artist_name">([^<]+)</span>'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = acentos(match[2])

        # URL
        scrapedurl = match[0]
        
        # Thumbnail
        scrapedthumbnail = match[1]
        
        # procesa el resto
        scrapedplot = match[3]

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle+" - "+scrapedplot)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )


        #llama a la rutina paginasiguiente
    cat = 'busca'
    paginasiguientes(patronvideos,data,category,cat)
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############        


def TipoVideo(params, url, category):
    logger.info("[sonolatino.py] TipoVideo")
    
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Bachata","http://www.sonolatino.com/bachata","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Best Rock Songs","http://www.sonolatino.com/toprock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Blues","http://www.sonolatino.com/blues","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Champeta","http://www.sonolatino.com/champeta","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Country Pop","http://www.sonolatino.com/countrypop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Cumbia","http://www.sonolatino.com/cumbia","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Dance","http://www.sonolatino.com/dance","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Dance Punk","http://www.sonolatino.com/dancepunk","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Duranguense","http://www.sonolatino.com/duranguense","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Electro hop","http://www.sonolatino.com/electro-hop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Electro pop","http://www.sonolatino.com/electropop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Electronica","http://www.sonolatino.com/electronica","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Emo","http://www.sonolatino.com/emo","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Especiales","http://www.sonolatino.com/especiales","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Flamenco","http://www.sonolatino.com/flamenco","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Folklorica","http://www.sonolatino.com/folklorica","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Funk Rock","http://www.sonolatino.com/funkrock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Grupera","http://www.sonolatino.com/grupera","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Grupos Nuevos","http://www.sonolatino.com/grupos-nuevos","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Hard rock","http://www.sonolatino.com/Hard-rock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Hip Hop","http://www.sonolatino.com/hiphop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "House","http://www.sonolatino.com/house","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Humor","http://www.sonolatino.com/humor","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Indie pop","http://www.sonolatino.com/indie-pop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Indie Rock","http://www.sonolatino.com/indierock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Jazz","http://www.sonolatino.com/jazz","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Merengue","http://www.sonolatino.com/merengue","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Merengue Urbano","http://www.sonolatino.com/merengue-urbano","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Metal","http://www.sonolatino.com/metal","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Modelos","http://www.sonolatino.com/modelos","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Neo Soul","http://www.sonolatino.com/neosoul","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "New Wave","http://www.sonolatino.com/newwave","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Norte�a","http://www.sonolatino.com/nortena","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Pop","http://www.sonolatino.com/pop","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Pop Punk","http://www.sonolatino.com/poppunk","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Pop Rap","http://www.sonolatino.com/poprap","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Pop Rock","http://www.sonolatino.com/poprock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Post grunge","http://www.sonolatino.com/Post-grunge","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Post Hardcore","http://www.sonolatino.com/posthardcore","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Punk","http://www.sonolatino.com/punk","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "R'n'B","http://www.sonolatino.com/rnb","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Ranchera","http://www.sonolatino.com/ranchera","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Rap","http://www.sonolatino.com/rap","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Reggae Fusion","http://www.sonolatino.com/reggaefusion","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Reggaeton","http://www.sonolatino.com/reggaeton","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Rock & Alternative","http://www.sonolatino.com/rock","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Salsa","http://www.sonolatino.com/salsa","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Chicas","http://www.sonolatino.com/chicas","","")
    xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "Chicos","http://www.sonolatino.com/chicos","","")


    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

 


#############--------------------------------------------------------###########

def listarpor(params,url,category):
    url1=url
    title = urllib.unquote_plus(params.get("title"))[:11]
       
    #verifica si es la primera vez o viene de una paginacion
    if  url.endswith(".html"):           
        return(url)
    else:
        fecha = "-1-date.html"
        vistas = "-1-views.html"
        rating = "-1-rating.html"
        artista = "-1-artist.html" 
     # Abre el di�logo de selecci�n
        opciones = []
        opciones.append("Fecha")
        opciones.append("Vistas")
        opciones.append("Votos")
        opciones.append("Artista")
        dia = xbmcgui.Dialog()
        seleccion = dia.select("Ordenar '"+title+"' por: ", opciones)
        logger.info("seleccion=%d" % seleccion)    
        if seleccion==-1:
           return("")
        if seleccion==0:
           url1 = url + fecha
        elif seleccion==1:
           url1 = url + vistas
        elif seleccion==2:
           url1 = url + rating
        elif seleccion==3:
                url1 = url + artista
         
        return(url1)

   
############---------------------------------------------------------###########

def listaseries(params,url,category):
    logger.info("[sonolatino.py] listaseries")
    #url2 = "http://www.sonolatino.com/index.html"
    data = scrapertools.cachePage(url)
    
    patron = "Relacionadas</h4>(.*?)</ul>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        patron = '<a href="([^"]+)">([^<]+)</a>'
        matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
        scrapedplot = ""
        scrapedthumbnail= ""
        if len(matches)>0:
            for match in matches2:
                scrapedtitle = acentos(match[1])
                print match[0]
                scrapedurl = match[0][:-18]
                print scrapedurl
                if (DEBUG):
                    logger.info("scrapedtitle="+scrapedtitle)
                    logger.info("scrapedurl="+scrapedurl)
                    logger.info("scrapedthumbnail="+scrapedthumbnail)
                        # A�ade al listado de XBMC
                xbmctools.addnewfolder( __channel__ , "listatipodocumental" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )                    

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def listatipoVideo(params,url,category):
    logger.info("[sonolatino.py] listatipodocumental")

    # busca tipo de listado por : FECHA | VISTAS | RATING #
    url = listarpor(params,url,category) 
    if len(url)==0 :
       return  
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Extrae las entradas (carpetas)
            

    if url == "http://www.sonolatino.com/index.html":
        patronvideos = '<li class="item">[^<]+<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)" class="imag".*?/></a>'
        cat = "viendose"
    else:  
        patronvideos  = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)"'
        patronvideos += '>[^<]+<img src="([^"]+)"  alt="([^"]+)".*?<span class="artist_name">([^<]+)</span>'
        cat = "tipo"
            
            
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    #logger.info("matches = "+matches[0])
    scrapedplot = ""
    for match in matches:
        # Titulo
        scrapedtitle = scrapertools.unescape(match[2])

        # URL
        scrapedurl = match[0]
        
        # Thumbnail
        scrapedthumbnail = match[1]
        
        # procesa el resto
        if cat == "tipo":
           scrapedplot = scrapertools.unescape(match[3])
        else:
           for campo in re.findall("/(.*?)/",match[0]):
            scrapedplot = campo
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )
 #  -------------------------------------------
 #     Busqueda de la siguiente pagina
    
    if cat == "tipo":
           patron_pagina_sgte = '</span><a href="([^"]+)"'
           paginasiguientes(patron_pagina_sgte,data,category,cat)

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

##############---------------------------------------------------------##############

def Videosnuevos(params,url,category):
    url1=url
    # Abre el di�logo de selecci�n
    opciones = []
    opciones.append("Todo el tiempo")
    opciones.append("Hoy")
    opciones.append("Ayer")
    opciones.append("Este Mes")
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Elige uno", opciones)
    logger.info("seleccion=%d" % seleccion)    
    if seleccion==-1:
           return
    if seleccion==0:
           url1 = "http://www.sonolatino.com/newvideos.html"
    elif seleccion==1:
           url1 = "http://www.sonolatino.com/newvideos.html?d=today"
    elif seleccion==2:
           url1 = "http://www.sonolatino.com/newvideos.html?d=yesterday"
    elif seleccion==3:
           url1 = "http://www.sonolatino.com/newvideos.html?d=month"
    Videosnuevoslist(params,url1,category)



#############----------------------------------------########################



def Videosnuevoslist(params,url,category):
    logger.info("[sonolatino.py] VideoesNuevos")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)

    
    patronvideos  = '<tr><td.*?<a href="([^"]+)">'
    patronvideos += '<img src="([^"]+)" '
    patronvideos += 'alt="[^"]+".*?'
    patronvideos += 'width="250">([^<]+)<'
    patronvideos += 'td class.*?<a href="[^>]+>([^<]+)</a></td><td class.*?>([^<]+)</td></tr>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info("matches = "+str(matches))
    if DEBUG:
        scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        # Titulo
        scrapedtitle = match[2] + " - " + match[3]+" - " + match[4].replace('&iacute;','i')
        print scrapedtitle
        scrapedtitle = scrapertools.unescape(scrapedtitle)

        # URL
        scrapedurl = match[0]
        
        # Thumbnail
        scrapedthumbnail = match[1]
        imagen = ""
        # procesa el resto
        scrapedplot = match[3]
        tipo = match[3]

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
            #xbmctools.addthumbnailfolder( __channel__ , scrapedtitle, scrapedurl , scrapedthumbnail, "detail" )
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle ,scrapedurl , scrapedthumbnail , scrapedplot )
    

    # Busca enlaces de paginas siguientes...
    cat = "nuevo"
    patronvideo = patronvideos
    paginasiguientes(patronvideo,data,category,cat)     

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

##########---------------------------------------------------------------#############

def Videodeldia(params,url,category):
#    list(params,url,category,patronvideos)
    logger.info("[sonolatino.py] Videodeldia")
           
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    patronvideos = 'Video Musical: <a href="([^"]+)">([^<]+)</a>'
    matches =  re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        # Titulo
        scrapedtitle = acentos(match[1])

        # URL
        scrapedurl = match[0]
          
        # Thumbnail
        scrapedthumbnail = ""

        # scrapedplot
        scrapedplot = ""
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)
 
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot ) 
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True ) 

################---------------------------------------------------------###########


############---------------------------------------------------#######################
def topVideos(params,url,category):
    url2=url
    data = scrapertools.cachePage(url)
    patron = '<option value="([^"]+)" >([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        opciones = []
        urls = []
        opciones.append("Todo el Tiempo")
        urls.append("http://www.sonolatino.com/topvideos.html")
        opciones.append("Ultimos 2 dias")
        urls.append("http://www.sonolatino.com/topvideos.html?do=recent")
        
        for match in matches:
            opciones.append(scrapertools.unescape(match[1]))
            urls.append(match[0])
            # Abre el di�logo de selecci�n
        
        dia = xbmcgui.Dialog()
        seleccion = dia.select("Elige Listar Top por :", opciones)
        logger.info("seleccion=%d" % seleccion) 
        if seleccion==-1:
            return
        
        url2 = urls[seleccion]
        toplist(params,url2,category)



############----------------------------------------------####################

def toplist(params,url,category):
    logger.info("[sonolatino.py] toplist")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    logger.info("[sonolatino.py] toplist "+url) 
    if url== "http://www.sonolatino.com/topvideos.html?do=recent":
        
        patronvideos = '<tr>[^<]+<td[^>]+>([^<]+)</td>[^<]+<td'
        patronvideos += '[^>]+><a href="([^"]+)">'
        patronvideos += '<img src="([^"]+)" alt=[^>]+>'
        patronvideos += '</a></td>[^<]+<td[^>]+>([^<]+)</td>[^<]+<td[^>]+>'
        patronvideos += '<a href="[^"]+">([^<]+)</a>'
        patronvideos += '</td>[^<]+<td[^>]+>([^<]+)</td>'

    else:
        
        patronvideos = '<tr>[^>]+>([^<]+)</td>'
        patronvideos += '[^>]+><a href="([^"]+)">'
        patronvideos += '<img src="([^"]+)"'
        patronvideos += ' alt="([^"]+)"[^>]+>'
        patronvideos += '</a></td>[^>]+>([^<]+)</td>[^>]+>'
        patronvideos += '<a href="[^"]+">[^>]+></td>[^>]+>([^<]+)</td>'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[3]

        # URL
        scrapedurl = match[1]
        
        # Thumbnail
        scrapedthumbnail = match[2]
        
        # procesa el resto
        scrapedplot = match[4]+" - " + "Vistas : "+match[5]+" veces"

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        #    xbmctools.addnewvideo( __channel__ , "detail" , category , "directo" , match[0]+") "+scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )

        xbmctools.addthumbnailfolder( __channel__ , match[0]+") "+scrapedtitle+" - "+scrapedplot, scrapedurl , scrapedthumbnail, "detail" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############

def detail(params,url,category):
    logger.info("[sonolatino.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    if len(thumbnail)<=0:
        patron = '<td valign="top">[^<]+<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            thumbnail = matches[0]
    print thumbnail
    thumnbail = thumbnail
    ok = "false"
    
    patrondescrip = '<td.+?class="letra">[^<]+<h3>(.*?)</td>'
    descripcion = ""
    plot = ""
    uri = url
    matches = re.compile(patrondescrip,re.DOTALL).findall(data)
    
    if len(matches)>0:
        descripcion = matches[0]
        descripcion = descripcion.replace("&nbsp;","")
        descripcion = descripcion.replace("<BR>","\n")
        #descripcion = descripcion.replace("\r","")
        #descripcion = descripcion.replace("\n"," ")
        descripcion = descripcion.replace("\t","")
        descripcion = re.sub("<[^>]+>"," ",descripcion)
#        logger.info("descripcion="+descripcion)
        descripcion = acentos(descripcion)
#        logger.info("descripcion="+descripcion)
        try :
            plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
        except:
            plot = descripcion
    # ----------------------------------------------------------------------------
    # Busca los enlaces a los videos de : "Megavideo"
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        videotitle = video[0]
        url1 = video[1].replace("&amp;","&")
        logger.info("url   ="+url)
        if  url.endswith(".jpg"):break
        server = video[2]
        if server=="Megavideo" or "Veoh":
            xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip().replace("(Megavideo)","").replace("  "," ") + " - " + videotitle , url1 , thumbnail , plot )
            
        else:
            xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip().replace(server,"").replace("  "," ") + " - " + videotitle , url1 , thumbnail , plot )


        
      
    # ------------------------------------------------------------------------------------
       #  ---- Extrae los videos directos ----- 

    # Extrae los enlaces a los v�deos (Directo)
    patronvideos = "file: '([^']+)'"
    servidor = "Directo"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)
       # ---------------------------------------
       
    # Extrae los enlaces a los v�deos (izlesene)
    patronvideos = 'http://www.izlesene.com/.+?video=([0-9]{7})'
    servidor = "izlesene"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)

       #  --- Extrae los videos de veoh  ----
    patronvideos = 'var embed_code[^>]+>   <param name="movie" value="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf.*?permalinkId=(.*?)&player=videodetailsembedded&videoAutoPlay=0&id=anonymous"></param>'
    servidor = "Veoh"
    extraevideos(patronvideos,data,category,title+" - Video en  Veoh",thumbnail,plot,servidor)
       # ---------------------------------------


     
#var embed_code =  '<embed id="VideoPlayback" src="http://video.google.com/googleplayer.swf?docid=1447612366747092264&hl=en&fs=true" style="width:496px;height:401px" allowFullScreen="true" allowScriptAccess="always" type="application/x-shockwave-flash" wmode="window">  </embed>' ;

       #  --- Extrae los videos de google  ----
    patronvideos = '<embed id="VideoPlayback" src="http://video.google.com/googleplayer.swf.*?docid=(.*?)&hl=en&'
    servidor = "Google"
    extraevideos(patronvideos,data,category,title+" - [Video en google]",thumbnail,plot,servidor)
       # --------------------------------------- 

       #  --- Extrae los videos de http://n59.stagevu.com  ----
    patronvideos = '"http://.*?.stagevu.com/v/.*?/(.*?).avi"'
    servidor = "Stagevu"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)
    
    #  --- Extrae los videos de dailymotion.com  ----
    patronvideos = 'value="http://www.dailymotion.com/([^"]+)"'
    
    servidor = "Dailymotion"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)
    
    #  --- Extrae los videos de vimeo.com  ----
    patronvideos = "http://vimeo.com.*?clip_id=([0-9]{8})"
    servidor = "Vimeo"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)
    
    #  --- Extrae los videos de yahoo.com  ----
    patronvideos = "http://.*?video.yahoo.com.*?id=([v0-9]{10})"
    servidor = "Yahoo"
    extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor)
    
       # --Muestra Una opcion mas para videos documentales relacionados con el tema--
    print "esta es la url :%s" %url
    try:
            patron = "http://www.sonolatino.com.*?\_(.*?)\.html"
            matches = re.compile(patron,re.DOTALL).findall(url)
            url = uri
            titulo = "Ver Videos Relacionados"
            xbmctools.addnewfolder( __channel__ , "Relacionados" , category , titulo , url , "" , "L�sta algunos videos relacionados con el mismo video musical" )
                    
            url = "http://www.sonolatino.com/ajax.php?p=detail&do=show_more_best&vid="+matches[0]
            titulo = "Ver Videos mas vistos"
            xbmctools.addnewfolder( __channel__ , "Relacionados" , category , titulo , url , "" , "L�sta algunos mas vistos relacionados con el video musical" )
        
            titulo = "Ver Videos del mismo Artista"
            url = "http://www.sonolatino.com/ajax.php?p=detail&do=show_more_artist&vid="+matches[0]
            xbmctools.addnewfolder( __channel__ , "Relacionados" , category , titulo , url , "" , "L�sta algunos videos relacionados con el mismo Artista" )
    except:
            pass
    patron  = '<h1 class="h2_artistnuevo">([^<]+)</h1>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        xbmctools.addnewfolder( "trailertools" , "buscartrailer" , category , "[Buscar la cancion en Youtube:] "+matches[0] , title , os.path.join(IMAGES_PATH, 'youtube_logo.png') , "Busca el video en Youtube" )
        try:
            artista = matches[0].split("-")[0].strip()
            xbmctools.addnewfolder( "trailertools" , "buscartrailer" , category , "[Buscar artista en Youtube:] "+artista , title , os.path.join(IMAGES_PATH, 'youtube_logo.png') , "Busca el video en Youtube" )
        except:
                pass
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

#############----------------------------------------------------------#############

def extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor):
    logger.info("patron="+patronvideos)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)        

    if len(matches)>0 :
        # A�ade al listado de XBMC
        if servidor == "Directo":
            if "youtube.com" in  matches[0]:
                from youtube import Extract_id
                url = Extract_id(matches[0])
                xbmctools.addnewvideo( __channel__ , "play" , category , "Youtube" , "%s [YOUTUBE]" %title , url , thumbnail , plot )
            else:
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , "%s [Directo]" %title, matches[0] , thumbnail , plot )

        elif servidor == "Veoh":
            from servers import veoh
            veohurl = veoh.get_video_url(matches[0])
            logger.info(" veohurl = " +veohurl)

            if len(veohurl)>0:
                if  veohurl=="http://./default.asp":
                    advertencia = xbmcgui.Dialog()
                    resultado = advertencia.ok('El Video Video' , title , 'no existe en Veoh','visite la pagina www.sonolatino.com para reportarlo' )
                    return
                logger.info(" newmatches = "+veohurl)
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title, veohurl , thumbnail , plot )
            else:
                advertencia = xbmcgui.Dialog()
                resultado = advertencia.ok('El Video Video' , title , 'no existe en Veoh')
                return 

        elif servidor == "Google":
            url = "http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+matches[0]
            logger.info(" Url = "+url)
            data1 = scrapertools.cachePage(url)
            newpatron = '</script>.*?<a href="(.*?)" title="Click to Download">'
            newmatches = re.compile(newpatron,re.DOTALL).findall(data1)
            if len(newmatches)>0:
                logger.info(" newmatches = "+newmatches[0])
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title, newmatches[0] , thumbnail , plot )

        elif servidor == "Stagevu":
            url= "http://stagevu.com/video/"+matches[0]
            from servers import stagevu
            url = stagevu.get_video_url(url)
            
            logger.info(" url = "+url)
            
            
            videotitle = "Video en Stagevu"
            server = servidor
            xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title.strip().replace(server,"").replace("  "," ") + " - " + videotitle , url , thumbnail , plot )
        
        elif servidor == "izlesene":
            url = "http://www.izlesene.com/actions/video/embed.php?video="+matches[0]
            data1 = scrapertools.cachePage(url)
            newpatron = "fURL=([^\&]+)\&vduration=([^\&]+)\&"
            newmatches = re.compile(newpatron,re.DOTALL).findall(data1)
            if len(newmatches)>0:
                logger.info(" izlesene furl = "+newmatches[0][0])
                url = "http://dcdn.nokta.com/%s%s" %(newmatches[0][0], "_1_5_1.xml")
                xbmctools.addnewvideo( __channel__ , "play" , category , "izlesene" , "%s (%s) [IZLESENE]" %(title,newmatches[0][1]) , url , thumbnail , plot )
        
        elif servidor == "Dailymotion":
            if "/" in matches[0]:
                idd = matches[0].split("/")
                id  = idd[len(idd)-1]
            else:
                id = matches[0]
            daily = 'http://www.dailymotion.com/video/%s'%id
            data2 = scrapertools.cachePage(daily)
            Lowres=re.compile('%22sdURL%22%3A%22(.+?)%22').findall(data2)
            if len(Lowres)>0:
                videourl = urllib.unquote(Lowres[0])
                videourl = videourl.replace("\/","/")
                
                    
                subtitle = "[FLV-Directo-Dailymotion]"
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
            
            # Busca el enlace al video con formato HQ (H264)        
            Highres=re.compile('%22hqURL%22%3A%22(.+?)%22').findall(data2)
            if len(Highres)>0:
                videourl = urllib.unquote(Highres[0])
                videourl = videourl.replace("\/","/")
                
                        
                subtitle = "[h264-Directo-Dailymotion-este video no es soportado en versiones antiguas o xbox plataforma]"
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
        
        elif servidor == "Vimeo":
            subtitle = "[Vimeo]"
            xbmctools.addnewvideo( __channel__ , "play" , category , "Vimeo" , title + " - "+subtitle, matches[0] , thumbnail , plot )
        ## -------------------------
        
        elif servidor == "Yahoo":
            import yahoo
            subtitle  = "[Yahoo]"
            video_url = yahoo.geturl(matches[0])
            if len(video_url)>0:
                if "rtmp" in video_url:
                    addnewvideo( __channel__ , "playRtmp" , category , "Directo" , title + " - "+subtitle, video_url , thumbnail , plot )
                else:
                    xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, video_url , thumbnail , plot )
#############----------------------------------------------------------#############

def play(params,url,category):
    logger.info("[sonolatino.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    
    try:
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    except:
        thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = urllib.unquote_plus( params.get("plot") )
    plot = urllib.unquote_plus( params.get("plot") )

    try:
        plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    except:
        plot = xbmc.getInfoLabel( "ListItem.Plot" )

    server = params["server"]
    logger.info("[sonolatino.py] thumbnail="+thumbnail)
    logger.info("[sonolatino.py] server="+server)
    
    if server == "izlesene":
        print server
        data = scrapertools.cachePage(url)
        print data
        patron = 'durl="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            url = matches[0]
            server = "Directo"
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)


def playRtmp(params,url,category):
    logger.info("[sonolatino.py] playRtmp")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    
    try:
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    except:
        thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = urllib.unquote_plus( params.get("plot") )
    plot = urllib.unquote_plus( params.get("plot") )

    try:
        plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    except:
        plot = xbmc.getInfoLabel( "ListItem.Plot" )

    server = params["server"]
    logger.info("[sonolatino.py] thumbnail="+thumbnail)
    logger.info("[sonolatino.py] server="+server    )
    
    
    

    item=xbmcgui.ListItem(title, iconImage='', thumbnailImage=thumbnail, path=url)
    item.setInfo( type="Video",infoLabels={ "Title": title})
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    




#############----------------------------------------------------------#############

def paginasiguientes(patronvideos,data,category,cat):

# ------------------------------------------------------
    # Extrae la p�gina siguiente
    # ------------------------------------------------------
    patron    = '</span><a href="([^"]+)"' 
    matches   = re.compile(patron,re.DOTALL).findall(data)
    #menutitle = "Volver Al Menu Principal"
    #menurl    = "http://www.sonolatino.com/"
    if DEBUG:
        scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Pagina siguiente"
        scrapedurl = "http://www.sonolatino.com/" + match
        scrapedthumbnail = os.path.join(IMAGES_PATH, 'next.png')
        scrapeddescription = ""

        # Depuracion
        if DEBUG:
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        if cat == 'tipo':   
        # A�ade al listado de XBMC
            xbmctools.addthumbnailfolder( __channel__ , scrapedtitle , scrapedurl , scrapedthumbnail, "listatipoVideo" )
        elif cat == 'nuevo':
            xbmctools.addthumbnailfolder( __channel__ , scrapedtitle , scrapedurl , scrapedthumbnail, "Videosnuevoslist" )
        elif cat == 'tag':
            xbmctools.addthumbnailfolder( __channel__ , scrapedtitle , "http://www.sonolatino.com.es/series"+match , scrapedthumbnail, "tagdocumentaleslist" )
        elif cat == 'busca':
            xbmctools.addthumbnailfolder( __channel__ , scrapedtitle , scrapedurl , scrapedthumbnail, "searchresults" )
               

    #xbmctools.addthumbnailfolder( __channel__ , menutitle , menurl , "", "volvermenu" )
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
########-------------------------------------------------------############
  
def acentos(title):

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
######-----------------------------------------------##############

def verRelacionados(params,data,category):
    
    patronvideos  = '<div class="item">.*?<a href="([^"]+)"'
    patronvideos += '><img src="([^"]+)".*?'
    patronvideos += 'alt="([^"]+)".*?/></a>.*?'
    patronvideos += '<span class="artist_name">([^<]+)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        scrapedtitle = acentos(match[2])

        # URL
        scrapedurl = match[0]
        
        # Thumbnail
        scrapedthumbnail = match[1]
        
        # procesa el resto
        scrapeddescription = match[3]

        # procesa el resto
        scrapedplot = ""

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle+" - "+scrapeddescription , scrapedurl , scrapedthumbnail , scrapedplot )

        # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
 
def Relacionados(params,url,category): 
    
    data = scrapertools.cachePage(url)
    print data
    verRelacionados(params,data,category)


def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ,Serie=""):
    if DEBUG:
        try:
            logger.info('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
        except:
            logger.info('[xbmctools.py] addnewvideo(<unicode>)')
    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
    listitem.setProperty('IsPlayable', 'true')
    #listitem.setProperty('fanart_image',os.path.join(IMAGES_PATH, "cinetube.png"))
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server , Serie)
    #logger.info("[xbmctools.py] itemurl=%s" % itemurl)
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem)

def playrtmp(params,url,category):
    
    icon = "DefaultVideo.png"
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
        
    item=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumbnail, path=url)
    item.setInfo( type="Video",infoLabels={ "Title": title, "Plot": plot})
    item.setProperty( "IsPlayable", "true" )
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    

def creartag(params,url,category):
    nombrefichero = os.path.join( config.get_setting("downloadpath"), "sonolatino_category.txt")
    data = scrapertools.cachePage(url)
    patron = '<ul id="ul_categories">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
        matches2 = re.compile(patron,re.DOTALL).findall(matches[0])
        if len(matches2)>0:
            filetag = open(nombrefichero,"w")
            
            for match in matches2:
                filetag.write('xbmctools.addnewfolder(__channel__ , "listatipoVideo" , category , "%s","%s","","")\n' %(match[1],match[0]))
                
            filetag.flush();
            filetag.close()            
            print "Lista tag creada correctamente"
        else:
            print "no encontro ningun tag"
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
    
