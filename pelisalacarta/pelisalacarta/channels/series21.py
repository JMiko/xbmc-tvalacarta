# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series21 by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import string
from core import decrypt21

import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import config
from core import logger
from platformcode.xbmc import xbmctools
from core.item import Item
from servers import servertools
from servers import youtube

from pelisalacarta import buscador

__channel__ = "series21"
__category__ = "S"
__type__ = "xbmc"
__title__ = "Series21"
__language__ = "ES"

DEBUG = config.get_setting("debug")

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[series21.py] init")

def mainlist(params,url,category):
    logger.info("[series21.py] mainlist")

    # A�ade al listado de XBMC
    xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , "Series - Novedades"            ,"http://www.series21.com","","","novedades")
    xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , "Series - Estrenos"             ,"http://www.series21.com","","","estrenos")
    #xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , "Spoilers ","http://www.series21.com/","","","spoilers")
    xbmctools.addnewfolder( __channel__ , "seriesalfa"  , category , "Series - Lista alfab�tica (Con Sinopsis y Poster)"     ,"","","")
    xbmctools.addnewfolder( __channel__ , "SeriesBuscaAlfa"   , category , "Series - Busqueda Alfab�tica (toda la base de datos)" ,"http://www.series21.com/listado-series/","","")
    #xbmctools.addnewfolder( __channel__ , "listaActoresMasBuscados" , category , "Actores - Lista Los M�s Buscados"     ,"http://www.series21.com/","","")
    #xbmctools.addnewfolder( __channel__ , "buscaporletraActor"      , category , "Actores - Busqueda Alfab�tica"  ,"http://www.series21.com/actores/","","")    
    xbmctools.addnewfolder( __channel__ , "search"                  , category , "Series - Buscar"                           ,"","","")

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def seriesalfa(params, url, category):

    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "0-9","http://www.series21.com/0-9/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "A","http://www.series21.com/a/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "B","http://www.series21.com/b/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "C","http://www.series21.com/c/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "D","http://www.series21.com/d/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "E","http://www.series21.com/e/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "F","http://www.series21.com/f/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "G","http://www.series21.com/g/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "H","http://www.series21.com/h/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "I","http://www.series21.com/i/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "J","http://www.series21.com/j/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "K","http://www.series21.com/k/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "L","http://www.series21.com/l/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "M","http://www.series21.com/m/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "N","http://www.series21.com/n/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "O","http://www.series21.com/o/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "P","http://www.series21.com/p/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "Q","http://www.series21.com/q/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "R","http://www.series21.com/r/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "S","http://www.series21.com/s/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "T","http://www.series21.com/t/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "U","http://www.series21.com/u/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "V","http://www.series21.com/v/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "W","http://www.series21.com/w/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "X","http://www.series21.com/x/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "Y","http://www.series21.com/y/","","","")
    xbmctools.addnewfolderextra( __channel__ ,"listsimple", category , "Z","http://www.series21.com/z/","","","")

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )



def search(params,url,category):
    logger.info("[series21.py] search")

    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            searchUrl = "http://www.series21.com/?palabra="+tecleado
            params["title"]="Z"
            listsimple(params,searchUrl,category)

def SeriesBuscaAlfa(params,url,category):
    logger.info("[series21.py] peliscat")
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Extrae los G�neros de las Peliculas
    patronvideos = '<div class="serieslist">(.*?)</div><!--list-->'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<a href="([^"]+)">([^<]+)</a>'
    matches1 = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    opciones = []
    opciones.append("Buscar por palabras (Teclado)")
    opciones.append("Listado completo")
    opciones.append("0-9")
    for letra in letras:
        opciones.append(letra)
    dia = xbmcgui.Dialog()
    seleccion = dia.select("busqueda rapida, elige uno : ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 :return
    if seleccion == 0:
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)>0:
                logger.info("Nuevo string tecleado   "+tecleado)
                for match in matches1:
                    if (string.lower(tecleado)) in (string.lower(match[1])):
                        scrapedurl   = "http://www.series21.com"+match[0]
                        scrapedtitle = match[1]
                        scrapedthumbnail = ""
                        scrapedplot = " "
                        if (DEBUG):
                            logger.info("scrapedtitle="+scrapedtitle)
                            logger.info("scrapedurl="+scrapedurl)
                            logger.info("scrapedthumbnail="+scrapedthumbnail)
                            #  A�ade al listado de XBMC
                            xbmctools.addnewfolder( __channel__ , "listarTemporada" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
    elif seleccion == 1:
        for match in matches1:
            url    = urlparse.urljoin(url,match[0])
            genero = match[1]
    
            xbmctools.addnewfolder( __channel__ , "listarTemporada" , category , genero ,url,"","")
    elif seleccion == 2:
        for match in matches1:


            if match[1][0:1] in ("0123456789"):
                scrapedurl   = match[0]
                scrapedtitle = match[1]
                scrapedthumbnail = ""
                scrapedplot = " "
                if (DEBUG):
                    logger.info("scrapedtitle="+scrapedtitle)
                    logger.info("scrapedurl="+scrapedurl)
                    logger.info("scrapedthumbnail="+scrapedthumbnail)
                    
                    # A�ade al listado de XBMC
                    xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

                                
    else:
        for match in matches1:
            if match[1][0:1] == letras[seleccion-3]:
                scrapedurl   = "http://www.series21.com"+match[0]
                scrapedtitle = match[1]
                scrapedthumbnail = ""
                scrapedplot = " "
                if (DEBUG):
                    logger.info("scrapedtitle="+scrapedtitle)
                    logger.info("scrapedurl="+scrapedurl)
                    logger.info("scrapedthumbnail="+scrapedthumbnail)
                    #  A�ade al listado de XBMC
                    xbmctools.addnewfolder( __channel__ , "listarTemporada" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )    
    


    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listsimple(params,url,category):
    logger.info("[series21.py] listsimple")
    url1 = "http://www.series21.com"
    extra= urllib.unquote_plus(params.get("extradata"))
    title = urllib.unquote_plus(params.get("title"))
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    logger.info("esta es la url: "+url)
    # Extrae las entradas (carpetas)
    scrapedplot = ""
    patronvideos = ""
    if (title == "Series - Estrenos") or  url1+"/nuevo" in url:
        patronvideos  = '<div class="film2"[^>]+>.*?' 
        patronvideos += '<img src="([^"]+)".*?'                             # Imagen
        patronvideos += '<a href="([^"]+)".*?'                                  # Url
        patronvideos += '<b>([^<]+)</b>.*?'                            # Nombre de la serie 
        patronvideos += '<div style[^>]+>([^<]+)</div>'                     # Titulo del capitulo 
        #patronvideos += '.*?<b>(Temporada:</b>.*?)<.*?</a>--><br/>'                        
        #patronvideos += '.*?<div style=[^>]+>'                                            # Genero
        #patronvideos += '.*?<b>(Doblaje:</b>.*?)<.*?-->'                                   # Idioma
        
    elif title in "0-9ABCDEFGHIJKLMNOPQRSTUVWXYZ" or extra=="actor":
        patronvideos  = '<a href="([^"]+)"'                                # url
        patronvideos += '.*?<img src="([^"]+)".*?'                              # Imagen
        patronvideos += 'class="titulo">([^<]+)</a>.*?'                               # Titulo
        patronvideos += '<b>(Sinopsis: </b>.*?)</div>'                          # Sinopsis
    #<li style="margin:0px; padding:0px;  height:18px; margin-left:5px;">
    #                        <b>Dexter</b>: <a href="/dexter/5x10-in-the-beginning/">5x10 -  In the Beginning</a>  | Subtitulado    
    elif title == "Series - Novedades":
        patronvideos  = '<li style=.*?margin-left[^>]+>[^<]+'
        patronvideos += '<b>([^<]+)</b>\: <a href="([^"]+)"'
        patronvideos += '>([^<]+)</a>(.+?)</li>'
        #patronvideos += '<br /><b>(.*?)</b><br />(.*?)</a></div>'
    logger.info("[ listsimple  patronvideos: "+patronvideos)
    #<li style="margin:0px; padding:0px;  height:18px; margin-left:5px;"><a style="text-decoration:none;" href="/bella-calamidades/1x124-capitulo-124/">Bella calamidades 1x124 - Capitulo - 124</a></li>
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    solo_capitulo = False
    #logger.info("[ listsimple  matches")
    for match in matches:
        # Atributos
        #scrapedtitle = match[2]
        #scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        #scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url1,match[1])
        scrapedthumbnail = urlparse.urljoin(url1,match[0])
        scrapedthumbnail = scrapedthumbnail.replace(" ","")
        if title in "0-9ABCDEFGHIJKLMNOPQRSTUVWXYZ" or extra=="actor":
            scrapedtitle = match[2].replace("\n\t","")
            scrapedplot  = match[3].replace("\n"," ")+"\n"
            scrapedurl = urlparse.urljoin(url1,match[0])
            scrapedthumbnail = urlparse.urljoin(url1,match[1])
            scrapedthumbnail = scrapedthumbnail.replace(" ","")            
        if title == "Series - Novedades":
            scrapedurl = urlparse.urljoin(url1,match[1])
            scrapedthumbnail = ""
            #scrapedthumbnail = scrapedthumbnail.replace(" ","")
            solo_capitulo = True
            #scrapedplot  = "Serie:    "+match[2]+"\n"
            #scrapedplot += "Capitulo: "+match[3]
            if "esp.gif" in match[3]:
                idioma = "Espa�ol"
            else:
                idioma = match[3].replace("  | ","").replace("\t\t\t\t\t\t","")
                
            scrapedtitle = "%s - %s (%s)" %(match[0],match[2],idioma)
        if (title == "Series - Estrenos")   or  url1+"/nuevo" in url:
            scrapedtitle = match[2]
            scrapedurl = urlparse.urljoin(url1,match[1])
            scrapedthumbnail = urlparse.urljoin(url1,match[0])
            scrapedthumbnail = scrapedthumbnail.replace(" ","")
            solo_capitulo = True
            scrapedtitle = scrapedtitle + " - " + match[3].replace("\t\t","")
            #scrapedplot = match[3].replace("\n","")+"\n"    
            #scrapedplot  = scrapedplot.replace(":",":          ")
            #scrapedplot += match[5].replace("\n"," ")+"\n"
            #scrapedplot += match[6].replace(":",":      ")
        #scrapedtitle = scrapedtitle.replace("\n\t"," ")    
        scrapedplot  = re.sub("<[^>]+>"," ",scrapedplot)
        scrapedplot  = scrapedplot.replace("&eacute;","�")
        scrapedplot  = scrapedplot.replace("&oacute;","�")
        scrapedplot  = scrapedplot.replace("&ntilde;","�")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")


        # A�ade al listado de XBMC
        if solo_capitulo:
            xbmctools.addnewfolder( __channel__ , "ListarVideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , fanart=scrapedthumbnail )
        else:
            xbmctools.addnewfolder( __channel__ , "listarTemporada" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , fanart=scrapedthumbnail )
        #<div class="pagination" align="center" ><p><span  class='current'>1</span><a  href='/estrenos/2/'>2</a><a  href='/estrenos/2/'>Siguiente &raquo;</a><a  href='/estrenos/2/'></a>
    # Extrae la marca de siguiente p�gina
    if title == "Series - Novedades" or "http://www.series21.com/nuevo" in url:
        patronvideos = '<div class="pagination" align="center" ><div.*?<a href="([^"]+)">M�s series'
    
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

        if len(matches)>0:
            extra = "siguiente"
            scrapedtitle = "P�gina siguiente"
            scrapedurl = urlparse.urljoin(url1,matches[0])
            scrapedthumbnail = ""
            scrapedplot = ""
            xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot,extra )

    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listarTemporada(params,url,category):
    logger.info("[series21.py] listvideos")
    url1 = "http://www.series21.com"
    if url=="":
        url = "http://www.series21.com"
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    titulo_serie  = urllib.unquote_plus(params.get("title"))
    if titulo_serie == "Cambiar a otras temporadas":
        titulo_serie = urllib.unquote_plus(params.get("extradata"))
    #thumbnail = urllib.unquote_plus(params.get("thumbnail"))
    #plot = urllib.unquote_plus(params.get("plot"))
    actor=""
    # Busca el area donde estan los videos y la descripcion
    patronvideos   = '<h3>(.*?)</h3>'                                            # Temporada de la Serie
    patronvideos  += '.*?<img.+?src="([^"]+)"  width=.*?/>'                        # Thumbnail de la Serie
    patronvideos  += '.*?<ul(.*?)</ul>'                                          # Capitulos de la Serie  
    matches        = re.compile(patronvideos,re.DOTALL).findall(data)
    patroncapit    = '<li><a href="([^"]+)".+?>(.+?)</a>(.+?)</li>'
    
        
    patronplot     = '<div style="margin:0px; padding:0px; text-align:justify;">(.*?)</div>'
    sinopsis       = re.compile(patronplot,re.DOTALL).findall(data)
    plot           = "Serie : "+titulo_serie+"\n"
    
    # Busca los actores
    patronactor    = '<div id="actores">(.*?)cursor:pointer'
    matchesactor   = re.compile(patronactor,re.DOTALL).findall(data)
    matchesactores = ""
    if len(matchesactor)>0:
        matchesactores = buscactores(matchesactor[0]) 
        print ' actores: %s' %str(len(matchesactores))
    if len(matchesactores)>0:
        actor =  "Actores:   "
        c = 0
        actores = "ACTORES DE ESTA SERIE :\n\n"
        for match in matchesactores:
            c       =  c + 1
            actores = actores + "-"+match[1] + "\n"
            if   c == 3 or c == 6 :
                actor = actor + match[1] + "\n"
            elif c == 4 or c == 7:
                actor = actor + "*              "  + match[1]+" , "
            else:
                actor = actor + match[1]+ " , "
                

    # Abre ventana de eleccion de temporadas            
                
    if len(matches)>1:
        opciones = []
        opciones.append(" Todas las Temporadas")
        for match in matches:
            temporada = re.sub("<[^>]+>"," ",match[0]).replace("-","").replace(">","")
            opciones.append(temporada)
        dia = xbmcgui.Dialog()
        seleccion = dia.select("Elige un tipo de Listado", opciones)
        logger.info("seleccion=%d" % seleccion)
    else:
        seleccion = 0
    if seleccion == -1:
        return
    if seleccion == 0:
        for match in matches:
            print 'esta es la %s' %match[0]
            print 'este es el thumbnail %s ' %match[1]
            thumbnail =  urlparse.urljoin(url1,match[1])
            temporada = re.sub("<[^>]+>"," ",match[0]).replace("-","").replace(">","")
            
            temporada += "\n" +actor+"\n"+ "Sinopsis : " + str(sinopsis[0].replace("\n\t\t\t\t\t",""))
            matchescapit = re.compile(patroncapit,re.DOTALL).findall(match[2])
            for match1 in matchescapit:
                esp  = ""
                subt = ""
                url  = match1[0]
                if "esp.gif" in match1[2]:
                    esp = " (Espa�ol)"
                if "Subtitulado" in match1[2]:
                    subt = " (VOS)"
                    
                titulo = titulo_serie+" - "+match1[1]+ esp + subt
                xbmctools.addnewfolder( __channel__ , "ListarVideos" , category , titulo , url , thumbnail, plot+temporada , fanart=thumbnail )
                
    else:
        thumbnail = urlparse.urljoin(url1,matches[seleccion-1][1])
        temporada = re.sub("<[^>]+>"," ",matches[seleccion-1][0]).replace("-","").replace(">","")
        #logger.info("matches "+matches[seleccion-1][2])
        matchescapit = re.compile(patroncapit,re.DOTALL).findall(matches[seleccion-1][2])
        plot   += temporada + "\n"
        plot   += actor+"\n"+"Sinopsis : " + str(sinopsis[0].replace("\n\t\t\t\t\t",""))
        if len(matchescapit)>0:
            for match1 in matchescapit:
                url    = match1[0]
                titulo = titulo_serie + " - " + match1[1]
                
                xbmctools.addnewfolder( __channel__ , "ListarVideos" , category , titulo , url , thumbnail, plot )
                
    # Busca Series relacionadas con los actores
    if len(matchesactores)>0:
        titulo = "Lista Series relacionadas con los actores"
        xbmctools.addnewfolderextra( __channel__ , "listaractores" , category , titulo , url , thumbnail, actores,matchesactor[0] , fanart=thumbnail )    
                
    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
    
def ListarVideos(params,url,category):
    url1 = "http://www.series21.com"
    url1 = urlparse.urljoin(url1,url)
    title = urllib.unquote_plus(params.get("title"))
    thumbnail = urllib.unquote_plus(params.get("thumbnail"))
    plot = urllib.unquote_plus(params.get("plot"))            
    data = scrapertools.cachePage(url1)
    # Busca el area donde estan los videos y la descripcion
    patronvideos = '<div id="content">(.*?)<!-- FIN #content-->'
    matches      = re.compile(patronvideos,re.DOTALL).findall(data)
    matchesBK = matches[0]


    # Extrae las entradas (videos) para megavideo
    patronvideos  = '<span  style="font-size:12px;"><strong>(.*?)</strong></span><br/>.*?'
    patronvideos += '<span.*?>.*?<a href="http\:\/\/www.megavideo.com\/([\?v=|v/|\?d=]+)([A-Z0-9]{8}).*?" target'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    encontrados = set()
    for match in matches:
        if match[2] not in encontrados:
            encontrados.add(match[2])
            if 'v' in match[1]:
                server = "Megavideo"
            else:
                server = "Megaupload"
            doblaje = scrapertools.entityunescape(match[0])
            # Titulo
            scrapedtitle = title + " -   [" +doblaje+ "]" + " ("+server+")"
            # URL
            scrapedurl = match[2]
            # Thumbnail
            scrapedthumbnail = thumbnail
            # Argumento
            #print 'este es el plot %s ' %plot
            #print ' doblaje %s ' %doblaje
            scrapedplot = plot
            if ("Espa�ol" in plot) and not (doblaje in plot):
                scrapedplot = scrapedplot.replace("Espa�ol",doblaje)
            elif "subtitulado" in plot and not (doblaje in plot):
                scrapedplot = scrapedplot.replace("Versi�n original (subtitulado)",doblaje)
            elif not doblaje in plot:
                scrapedplot += "\n" + "Doblaje : " + doblaje
            
            # Depuracion
            if (DEBUG):
                logger.info("scrapedtitle="+scrapedtitle)
                logger.info("scrapedurl="+scrapedurl)
                logger.info("scrapedthumbnail="+scrapedthumbnail)

            # A�ade al listado de XBMC
            xbmctools.addnewvideo( __channel__ , "play" , category ,server, scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
    if len(matches)==0:
        listavideos = servertools.findvideos(data)
        encontrados = set()
        for titulo,scrapedurl,servidor in listavideos:
            if scrapedurl.strip() not in encontrados:
                encontrados.add(scrapedurl.strip())
                xbmctools.addnewvideo( __channel__ , "play" , category ,servidor, title+ " - %s" %titulo , scrapedurl , thumbnail, plot )
    patronvideos = '<span class="bloque-doblaje">(.+?)</span>[^<]+'
    patronvideos +='<span class="bloque-link">[^<]+<a href="javascript\:goTo\(\'([^\']+)\'\, \'([^\']+)\'\)"(.+?)</span>'
    #patronvideos +='(?:\| <a href="javascript\:goTo\(\'([^\']+)\'\, \'([^\']+)\'\)".*?)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
    
        # URL
        if "megavideo" in match[2]:
            server = "Megavideo"
        elif "megaupload" in match[2]:
            server = "Megaupload"
        if "esp.gif" in match[0]:
            doblaje = "Espa�ol"
            
        else:
            doblaje = match[0].strip()            
        base64 = decrypt21.Base64()
        try:
            url2 = re.compile("javascript\:goTo\(\'([^\']+)\'\, \'([^\']+)\'\)").findall(match[3])[0]
            scrapedurl2 = base64._extract_code(base64.decode(url2[0]))
            scrapedurl = base64._extract_code(base64.decode(match[1]))
            part1 = " Parte 1 "
            part2 = " Parte 2 "
            scrapedtitle2 = title + part2+ " -   [" +doblaje+ "]" + " ("+server+")"
            #print match[3]
        except:
            scrapedurl = base64._extract_code(base64.decode(match[1]))
            part1 = ""
            part2 = ""            
            
        

        scrapedtitle = title + part1+ " -   [" +doblaje+ "]" + " ("+server+")"


        # Thumbnail
        scrapedthumbnail = thumbnail
        # Argumento
        scrapedplot = plot

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewvideo( __channel__ , "play" , category ,server, scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        if part2:
            xbmctools.addnewvideo( __channel__ , "play" , category ,server, scrapedtitle2 , scrapedurl2 , scrapedthumbnail, scrapedplot )
    
    
    # Extrae las entradas (videos) directos
    patronvideos = 'flashvars="file=([^\&]+)\&amp;controlbar=over'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        
        data1 = scrapertools.cachePage(matches[0])
        #logger.info(data)
        patron = 'author">(.*?)</media:credit>.*?<media\:content url="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data1)
        scrapertools.printMatches(matches)
        
        for match in matches:
            # A�ade al listado de XBMC
            xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title +" -  ["+match[0]+"]"+ " (Directo)" , match[1] , thumbnail , plot )
    # Busca el Spoiler 
    patronvideos = '(http://www.youtube.com[^"]+)"'
    matchSpoiler = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matchSpoiler)>0:
        encontrados = set()
        for match in matchSpoiler:
            if match not in encontrados:
                encontrados.add(match)
                # A�ade al listado de XBMC
                xbmctools.addnewvideo( __channel__ , "youtubeplay" , category ,"Directo", "Ver El Spoiler de : "+title , match , thumbnail, "Ver Video Spoiler" )
            

        
    # Lista series relacionadas
    titulo = "Ver otros capitulos de esta temporada" 
    matches = buscarelacionados(matchesBK)
    plot2 = "CAPITULOS DE ESTA TEMPORADA :\n\n"
    for match in matches:
        plot2 = plot2 + "-"+match[2]+"\n"
    xbmctools.addnewfolderextra( __channel__ , "listarelacionados" , category , titulo , url , thumbnail, plot2,matchesBK )
    #<div class="film"><a href="/house/#t_57"><img src="/thumbs/temporadas/95/120/57.jpg"
    # Cambiar de Temporada
    patron = 'div class="film"><a href="([^"]+)"><img src="([^"]+)" style'
    matchSerie= re.compile(patron,re.DOTALL).findall(matchesBK)
    if len(matchSerie)>1:
        for temp in matchSerie:
            url2      = urlparse.urljoin(url1,temp[0])
            thumbnail = urlparse.urljoin(url1,temp[1])
            titulo = "Cambiar a otras temporadas"
            titulo_serie = temp[0].split("/")
            titulo2 = titulo_serie[1].replace("-"," ")
            #print ' titulo%s ' %titulo2
            xbmctools.addnewfolderextra( __channel__ , "listarTemporada" , category , titulo , url2 , thumbnail, plot,titulo2 )
            break    
        
    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    logger.info("[series21.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)

def youtubeplay(params,url,category):
    logger.info("[series21.py] youtubeplay")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = "Ver Video"
    server = "Directo"
    id = youtube.Extract_id(url)
    # Abre el di�logo de selecci�n
    opciones = []
    opciones.append("(FLV) Baja calidad")
    opciones.append("(MP4) Alta calidad")
    dia = xbmcgui.Dialog()
    seleccion = dia.select("tiene 2 formatos elige uno", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion==-1:
        return("")
    if seleccion == 0:
        videourl,videoinfo = youtube.GetYoutubeVideoInfo(id)
    else:
        videourl = youtube.geturl(id)
    logger.info("link directo de youtube : "+videourl)
    xbmctools.play_video("Trailer",server,videourl,category,title,thumbnail,plot)
 

def listaractores(params,url,category):
    logger.info("[series21.py] listaractores")
    extra= urllib.unquote_plus(params.get("extradata"))
    url1 = "http://www.series21.com"
    actores = buscactores(extra)
    opciones = []
    actorURL = []
    for i in actores:
        opciones.append(i[1])
        actorURL.append(urlparse.urljoin(url1,i[0]))           
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Selecciona uno ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1:return
    else:
        params["title"]="Z"
        listsimple(params,actorURL[seleccion],category)
    return
    
def buscactores(data):
    patronvideos = '<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        return matches
    else:
        return ""
    
def listarelacionados(params,url,category):
    logger.info("[series21.py] listaractores")
    
    url1 = "http://www.series21.com"
    #patronvideos = '<div><a href="([^"]+)">([^<]+)</a><br'
    data = urllib.unquote_plus(params.get("extradata"))
    matches = buscarelacionados(data)
    plot = "" 
    patronvideos = '<b>Serie:</b>(.*?)<.*?<b>Temporada:</b>(.*?)<a'
    serie = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in serie:
        plot  = 'Serie : '+ match[0]+'\n'
        plot += 'Temporada : '+match[1]
    opciones = []
    URL = []
    for i in matches:
        if i[0] == "><a href=":
            opciones.append(i[2])
            URL.append(i[1])
        else:
            opciones.append("**"+i[2]+"**")
        
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Selecciona uno ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 :return
    elif "(Viendo ahora)" in opciones[seleccion]:return
    else:
        params["title"] = opciones[seleccion]
        params["plot"] = plot 
        ListarVideos(params,URL[seleccion],category)
    return
    
def buscarelacionados(data):
    patronvideos = '<div class="filmrelacionado"(><a href=| style=)"([^"]+)">(.*?)</'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    return (matches)
    
def buscaporletraActor(params,url,category):
    logger.info("[series21.py] buscaporletra")
    data = scrapertools.cachePage(url)
    patron  = '<div class="title">Listado de Actores</div><br/>(.*?)<ul class="menustyle">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    patron  = '<a href="(.*?)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(matches[0])
        
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    opciones = []
    opciones.append("Buscar por palabras (Teclado)")
    #opciones.append("0-9")
    for letra in letras:
        opciones.append(letra)
    dia = xbmcgui.Dialog()
    seleccion = dia.select("busqueda rapida, elige uno : ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 :return
    if seleccion == 0:
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)>0:
                logger.info("Nuevo string tecleado   "+tecleado)
                for match in matches:
                    if (string.lower(tecleado)) in (string.lower(match[1])):
                        scrapedurl   = "http://www.series21.com"+match[0]
                        scrapedtitle = match[1]
                        scrapedthumbnail = ""
                        scrapedplot = " "
                        if (DEBUG):
                            logger.info("scrapedtitle="+scrapedtitle)
                            logger.info("scrapedurl="+scrapedurl)
                            logger.info("scrapedthumbnail="+scrapedthumbnail)
                            #  A�ade al listado de XBMC
                            xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot,"actor" )
                                
    else:
        for match in matches:
            if match[1][0:1] == letras[seleccion-1]:
                scrapedurl   = "http://www.series21.com"+match[0]
                scrapedtitle = match[1]
                scrapedthumbnail = ""
                scrapedplot = " "
                if (DEBUG):
                    logger.info("scrapedtitle="+scrapedtitle)
                    logger.info("scrapedurl="+scrapedurl)
                    logger.info("scrapedthumbnail="+scrapedthumbnail)
                    #  A�ade al listado de XBMC
                    xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot,"actor" )
                
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listaActoresMasBuscados(params,url,category):
    logger.info("[series21.py] listaActoresMasBuscados")
    extra="actor"
    url1 = "http://www.series21.com"
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    patronvideos = 'Los m&aacute;s buscados:    <br />(.*?)</div>'
    matches1 = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<a href="([^"]+)">([^<]+)</a>'
    matches =  re.compile(patronvideos,re.DOTALL).findall(matches1[0])
    scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        scrapedtitle = match[1]
        # URL
        scrapedurl = urlparse.urljoin(url1,match[0])
        # Thumbnail
        scrapedthumbnail = ""
        
        # Argumento
        scrapedplot = "Busca las Series existentes de este Actor � Actriz"

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewfolderextra( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot,extra )
        
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
