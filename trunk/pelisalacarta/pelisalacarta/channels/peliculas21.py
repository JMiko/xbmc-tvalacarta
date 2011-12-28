# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculas21 by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

from servers import youtube
from servers import servertools

from pelisalacarta import buscador

from core import config
from core import logger
from core import decrypt21
from platformcode.xbmc import xbmctools
from core import scrapertools

__channel__ = "peliculas21"
__category__ = "F"
__type__ = "xbmc"
__title__ = "Peliculas21"
__language__ = "ES"

DEBUG = config.get_setting("debug")

# Traza el inicio del canal
logger.info("[peliculas21.py] init")


IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images','posters' ) )

def mainlist(params,url,category):
    logger.info("[peliculas21.py] mainlist")

    novedades = "http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=&periodo=0&idgenero=0&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4"
    MasVistos = "http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=hits&periodo=0&idgenero=0&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4"
    puntuacion = "http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=puntuacion&periodo=0&idgenero=0&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4"
    # A�ade al listado de XBMC

    xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , "Pel�culas - Novedades"            ,novedades,"","")
    xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , "Pel�culas - Mas Vistos"           ,MasVistos,"","")
    xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , "Pel�culas - Mejor Puntuadas"      ,puntuacion,"","")
    xbmctools.addnewfolder( __channel__ , "buscaporanyo"     , category , "Pel�culas - Busqueda por A�o de Estreno"             ,"http://www.peliculas21.com/estrenos/","","")
    xbmctools.addnewfolder( __channel__ , "listsimple"       , category , "Trailers  - Pr�ximos Estrenos"    ,"http://www.peliculas21.com/trailers/","","")
    xbmctools.addnewfolder( __channel__ , "peliscat"         , category , "Pel�culas - Lista por categor�as" ,"http://www.peliculas21.com/","","")
    xbmctools.addnewfolder( __channel__ , "pelisalfa"        , category , "Peliculas - Lista alfab�tica"     ,"","","")
    xbmctools.addnewfolder( __channel__ , "listaActoresMasBuscados" , category , "Actores   - Lista Los M�s Buscados"     ,"http://www.peliculas21.com/","","")
    xbmctools.addnewfolder( __channel__ , "buscaporletraActor" , category , "Actores   - Lista Alfab�tica"     ,"http://www.peliculas21.com/actores/","","")    
    xbmctools.addnewfolder( __channel__ , "search"           , category , "Pel�culas - Buscar"               ,"","","")


    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def pelisalfa(params, url, category):

    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "0-9","http://www.peliculas21.com/0-9/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "A","http://www.peliculas21.com/a/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "B","http://www.peliculas21.com/b/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "C","http://www.peliculas21.com/c/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "D","http://www.peliculas21.com/d/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "E","http://www.peliculas21.com/e/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "F","http://www.peliculas21.com/f/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "G","http://www.peliculas21.com/g/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "H","http://www.peliculas21.com/h/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "I","http://www.peliculas21.com/i/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "J","http://www.peliculas21.com/j/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "K","http://www.peliculas21.com/k/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "L","http://www.peliculas21.com/l/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "M","http://www.peliculas21.com/m/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "N","http://www.peliculas21.com/n/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "O","http://www.peliculas21.com/o/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "P","http://www.peliculas21.com/p/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "Q","http://www.peliculas21.com/q/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "R","http://www.peliculas21.com/r/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "S","http://www.peliculas21.com/s/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "T","http://www.peliculas21.com/t/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "U","http://www.peliculas21.com/u/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "V","http://www.peliculas21.com/v/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "W","http://www.peliculas21.com/w/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "X","http://www.peliculas21.com/x/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "Y","http://www.peliculas21.com/y/","","")
    xbmctools.addnewfolder( __channel__ ,"listsimpleMirror", category , "Z","http://www.peliculas21.com/z/","","")

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )



def search(params,url,category):
    logger.info("[peliculas21.py] search")
    buscador.listar_busquedas(params,url,category)

def searchresults(params,url,category):
    logger.info("[peliculas21.py] searchresults")
    
    buscador.salvar_busquedas(params,url,category)
    #convert to HTML
    tecleado = url.replace(" ", "+")
    searchUrl = "http://www.peliculas21.com/?palabra="+tecleado
    listsimpleMirror(params,searchUrl,category)

def performsearch(texto):
    logger.info("[peliculas.py] performsearch")
    url = "http://www.peliculas21.com/?palabra="+texto
    url1 = "http://www.peliculas21.com"

    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)

    patronvideos  = '<div.+?class="filmgal"[^>]+>.*?'
    patronvideos += '<a href="([^"]+)"[^>]+'                                        # url
    patronvideos += '>.*?<img alt="([^"]+)" '                                       # Titulo

    patronvideos += 'src="([^"]+)"'                                                 # Imagen
    patronvideos += '(.*?)reproducciones'                        # Contenido

    
    resultados = []
    for match in matches:
        # Atributos
        scrapedplot = ""
        scrapedthumbnail = ""
        try:
            scrapedtitle = re.compile('<span class\="titulotool">(.*?)</div>',re.DOTALL).findall(match[3])[0]
            scrapedtitle = re.sub("<[^>]+>","",scrapedtitle).replace("\n\t\t","").strip()
            #print scrapedtitle
        except:
            scrapedtitle = match[1]        
        
        #scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        #scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url1,match[0])
        
        scrapedthumbnail = urlparse.urljoin(url1,match[2])
        scrapedthumbnail = scrapedthumbnail.replace(" ","")
        plot = match[3]
        print plot
        try    :Sinopsis = re.compile("Sinopsis:(.*?)</div>").findall(plot)[0]
        except :Sinopsis="<>"
        print Sinopsis
        Sinopsis = " Sinopsis: " + Sinopsis.strip()
            
        try    :Genero = re.compile("G�nero:(.+?)</div>").findall(plot)[0]
        except :Genero = ""
        Genero = "Genero: " + Genero.strip()
        

        try    :Duracion = re.compile("Duraci&oacute;n:(.+?)</div>").findall(plot)[0]
        except :Duracion = ""
        Duracion = "Duracion: " + Duracion.strip()
        
        try    :Actores = re.compile("Actores:(.+?)</div>").findall(plot)[0]
        except :Actores = ""
        Actores = "Actores: " + Actores.strip()
                                    
        scrapedplot  = Genero + "\n" + Duracion + "\n" + Actores + "\n" + Sinopsis
        

        

        #scrapedplot += match[4].replace("\n","")+"\n"    
        

        #scrapedplot += match[5].replace("\n"," ")+"\n"
        
        #scrapedplot += ""
        scrapedplot  = re.sub("<[^>]+>","",scrapedplot)
        scrapedplot  = scrapedplot.replace("&aacute;","�")
        scrapedplot  = scrapedplot.replace("&iacute;","�")
        scrapedplot  = scrapedplot.replace("&eacute;","�")
        scrapedplot  = scrapedplot.replace("&oacute;","�")
        scrapedplot  = scrapedplot.replace("&uacute;","�")
        scrapedplot  = scrapedplot.replace("&ntilde;","�")

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        resultados.append( [__channel__ , "listvideos" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
        
    return resultados

def peliscat(params,url,category):
    logger.info("[peliculas21.py] peliscat")
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    
    # Extrae los G�neros de las Peliculas

    patronvideos = '<div id="textidgenero">G�nero:</div>(.*?)</select>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    patronvideos = '<option value="([^"]+)"  >([^<]+)</option>'
    matches1 = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    for match in matches1:
    
        #http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=&periodo=0&idgenero=5&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4&num_ale=0.5685049552958528
        url    = "http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=&periodo=0&idgenero=%s&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4" %match[0]
        genero = match[1]
    
    
        xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , genero ,url,"","")

    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listsimple(params,url,category):
    logger.info("[peliculas21.py] listsimple")
    url1 = "http://www.peliculas21.com"
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    '''
    <div class="fichafilm" >
        <a href="/el-hombre-lobo/"  target="_blank" class="titulo">
            <img alt="El hombre lobo" src="/thumbs_95_140_85/t2_4859.jpg"  width="95" height="140" border="0" />El hombre lobo        </a> (2010)<br />
        
                    <b>Duraci&oacute;n:</b> 1h 34min<br />
                <div><b>G&eacute;nero:</b>
    Thriller y Miedo / Terror    </div>
    <div><b>Doblaje:</b>
     Espa&ntilde;ol    </div>
    <div style="text-align:justify;">
        <b>Sinopsis:</b>
        Remake del cl�sico de terror de 1941, que desarrolla la historia de Lawrence, un joven que debe afrontar el abandono de su madre desde muy peque�o, y qui�n huye de su pueblo en busca de un mejor futuro que le permita olvidar momentos tan dolorosos de su ni�ez. Lawrence, se ve obligado a volver despu...    </div>
    <div class="datos">
            <div class="verde">+
    613 puntos</div>
        <div class="reproducciones">
    122638 reproducciones</div>
        <br class="corte"/></div></div>
    '''
    #|<div class="fichafilm" >.*?
    # Extrae las entradas (carpetas)
    
    patronvideos  = '<div.+?class="filmgal-trailer"[^>]+>.*?'
    patronvideos += '<a href="([^"]+)"[^>]+'                                        # url
    patronvideos += '>.*?<img alt="([^"]+)" '                                       # Titulo

    patronvideos += 'src="([^"]+)"'                                                 # Imagen
    patronvideos += '(.*?)reproducciones</div>'                        # Contenido
    print patronvideos
    print data
    #logger.info("[ listsimple  patronvideos")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    #logger.info("[ listsimple  matches")
    for match in matches:
        # Atributos
        scrapedplot = ""
        scrapedthumbnail = ""
        try:
            scrapedtitle = re.compile('<span class\="titulotool">(.*?)</div>',re.DOTALL).findall(match[3])[0]
            scrapedtitle = re.sub("<[^>]+>"," ",scrapedtitle).replace("  "," ").strip()
            #print scrapedtitle
        except:
            scrapedtitle = match[1]        
        
        #scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        #scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url1,match[0])
        
        scrapedthumbnail = urlparse.urljoin(url1,match[2])
        scrapedthumbnail = scrapedthumbnail.replace(" ","")
        plot = match[3]
        print plot
        try    :Sinopsis = re.compile("Sinopsis:(.*?)</div>").findall(plot)[0]
        except :Sinopsis="<>"
        print Sinopsis
        Sinopsis = " Sinopsis: " + Sinopsis.strip()
            
        try    :Genero = re.compile("G�nero:(.+?)</div>").findall(plot)[0]
        except :Genero = ""
        Genero = "Genero: " + Genero.strip()
        

        try    :Duracion = re.compile("Duraci&oacute;n:(.+?)</div>").findall(plot)[0]
        except :Duracion = ""
        Duracion = "Duracion: " + Duracion.strip()
        
        try    :Actores = re.compile("Actores:(.+?)</div>").findall(plot)[0]
        except :Actores = ""
        Actores = "Actores: " + Actores.strip()
                                    
        scrapedplot  = Genero + "\n" + Duracion + "\n" + Actores + "\n" + Sinopsis
        

        

        #scrapedplot += match[4].replace("\n","")+"\n"    
        

        #scrapedplot += match[5].replace("\n"," ")+"\n"
        
        #scrapedplot += ""
        scrapedplot  = re.sub("<[^>]+>","",scrapedplot)
        scrapedplot  = scrapedplot.replace("&aacute;","�")
        scrapedplot  = scrapedplot.replace("&iacute;","�")
        scrapedplot  = scrapedplot.replace("&eacute;","�")
        scrapedplot  = scrapedplot.replace("&oacute;","�")
        scrapedplot  = scrapedplot.replace("&uacute;","�")
        scrapedplot  = scrapedplot.replace("&ntilde;","�")
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot, context =5 )
        #<div class="pagination" align="center" ><p><span  class='current'>1</span><a  href='/estrenos/2/'>2</a><a  href='/estrenos/2/'>Siguiente &raquo;</a><a  href='/estrenos/2/'></a>
    # Extrae la marca de siguiente p�gina

    
    patronvideos  = "<span  class='current'>[^<]+</span><a  href='([^']+)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P�gina siguiente"
        scrapedurl = urlparse.urljoin(url1,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , fanart = scrapedthumbnail )

    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listsimpleMirror(params,url,category):
    logger.info("[peliculas21.py] listsimple")
    url1 = "http://www.peliculas21.com"
    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)

    patronvideos  = '<div.+?class="filmgal"[^>]+>.*?'
    patronvideos += '<a href="([^"]+)"[^>]+'                                        # url
    patronvideos += '>.*?<img alt="([^"]+)" '                                       # Titulo

    patronvideos += 'src="([^"]+)"'                                                 # Imagen
    patronvideos += '(.*?)reproducciones'                        # Contenido
    #print patronvideos
    #print data
    #logger.info("[ listsimple  patronvideos")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    #logger.info("[ listsimple  matches")
    for match in matches:
        # Atributos
        scrapedplot = ""
        scrapedthumbnail = ""
        #print match[3]
        try:
            scrapedtitle = re.compile('<span class\="titulotool">(.*?)</div>',re.DOTALL).findall(match[3])[0]
            scrapedtitle = re.sub("<[^>]+>","",scrapedtitle).replace("\n\t\t","").strip()
            #print scrapedtitle
        except:
            scrapedtitle = match[1]
            
        
        #scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
        #scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedurl = urlparse.urljoin(url1,match[0])
        
        scrapedthumbnail = urlparse.urljoin(url1,match[2])
        scrapedthumbnail = scrapedthumbnail.replace(" ","")
        plot = match[3].replace("\n","")
        try    :Sinopsis = re.compile("Sinopsis:(.*?)</div>").findall(plot)[0]
        except :Sinopsis="<>"
        print Sinopsis
        Sinopsis = "Sinopsis: " + Sinopsis.strip()
            
        try       :Genero = re.compile("G&eacute;nero:(.*?)</div>").findall(plot)[0]
        except :Genero = ""
        Genero = "Genero:  " + Genero.strip()
        print Genero

        try    :Duracion = re.compile("Duraci&oacute;n:(.*?)</div>").findall(plot)[0]
        except :Duracion = ""
        Duracion = "Duracion: " + Duracion.strip()
        
        try    :Actores = re.compile("Actores:(.*?)</div>").findall(plot)[0]
        except :Actores = ""
        Actores = "Actores:  " + Actores.strip()
        print Actores                            
        scrapedplot  = Genero + "\n" + Duracion + "\n" + Actores + "\n" + Sinopsis
        

        

        #scrapedplot += match[4].replace("\n","")+"\n"    
        

        #scrapedplot += match[5].replace("\n"," ")+"\n"
        
        #scrapedplot += ""
        scrapedplot  = re.sub("<[^>]+>","",scrapedplot)
        scrapedplot  = scrapedplot.replace("&aacute;","�")
        scrapedplot  = scrapedplot.replace("&iacute;","�")
        scrapedplot  = scrapedplot.replace("&eacute;","�")
        scrapedplot  = scrapedplot.replace("&oacute;","�")
        scrapedplot  = scrapedplot.replace("&uacute;","�")
        scrapedplot  = scrapedplot.replace("&ntilde;","�")
        
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , context=5)
        #<div class="pagination" align="center" ><p><span  class='current'>1</span><a  href='/estrenos/2/'>2</a><a  href='/estrenos/2/'>Siguiente &raquo;</a><a  href='/estrenos/2/'></a>
    # Extrae la marca de siguiente p�gina
    

    patronvideos  = "<a  href=\"#periodoslist\" onclick=\"paginaperiodo\(([^\)]+)\);\">Siguiente &raquo;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        #http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=&periodo=0&idgenero=5&idactor=0&listado_style=2&pagina=&periodos_ajax=&valorperiodo=4
        scrapedtitle = "P�gina siguiente"
    
        paramsurl = dict(part.split('=') for part in url.split('?')[1].split('&'))
        print paramsurl
        sigtepag = matches[0].replace("'","").split(',')
        scrapedurl = "http://www.peliculas21.com/ajaxs/ajax_periodos.php?valor=%s&periodo=%s&idgenero=%s&idactor=%s&listado_style=%s&pagina=%s&periodos_ajax=%s&valorperiodo=%s" %(paramsurl["valor"],paramsurl["periodo"],paramsurl["idgenero"],paramsurl["idactor"],paramsurl["listado_style"],sigtepag[6],paramsurl["periodos_ajax"],paramsurl["valorperiodo"])
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        
    else:
        
        
        patron = "<span  class='current'>[^<]+</span><a  href='([^']+)'>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            scrapedtitle = "P�gina siguiente"
            scrapedurl   = urlparse.urljoin(url1,matches[0])
            scrapedthumbnail = ""
            scrapedplot  = ""
            xbmctools.addnewfolder( __channel__ , "listsimpleMirror" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , fanart = scrapedthumbnail)
            
    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listvideos(params,url,category):
    logger.info("[peliculas21.py] listvideos")

    if url=="":
        url = "http://www.peliculas21.com"
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    #title = urllib.unquote_plus(params.get("title"))
    #thumbnail = urllib.unquote_plus(params.get("thumbnail"))
    #plot = urllib.unquote_plus(params.get("plot"))
    
    # Busca el area donde estan los videos y la descripcion
    patronvideos = '<div  class="peliculadoblaje">(.*?)<!-- FIN #content-->'
    matches      = re.compile(patronvideos,re.DOTALL).findall(data)
    
    # busca el titulo y el thumbnail
    patronvideos = '<img src="([^"]+)"[^>]+>[^<]+<[^>]+>([^<]+)</div>'
    matches2 =  re.compile(patronvideos,re.DOTALL).findall(matches[0])
    for match in matches2:
        title = match[1]
        thumbnail = urlparse.urljoin(url,match[0])
    plot = ""
    patronvideos = '<b>Duraci&oacute;n:</b>(.*?)<br />'
    duracion     = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    if len(duracion)>0:plot = "Duracion:"+duracion[0] + "\n"
        
    patronvideos = '<b>G&eacute;nero:</b>(.*?)<br />'
    genero       = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    if len(genero)>0:plot = plot + "Genero:  "+genero[0] +"\n"
    
    patronvideos = '<b>Sinopsis:</b>(.*?)</div>'
    sinopsis     = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    
    
      
    # Busca los actores
    matchesactores = buscactores(matches[0]) 
    if len(matchesactores)>0:
        plot = plot + "Actores:   "
        c = 0
        actores = "ACTORES DE ESTA PELICULA :\n\n"
        for match in matchesactores:
            c =  c + 1
            actores = actores + "-"+match[1] + "\n"
            if   c == 3:
                plot = plot + match[1] + "\n"
            elif c == 4:
                plot = plot + "*              "  + match[1]+" "
            else:
                plot = plot + match[1]+ " , "
        
    plot = plot    + "\nSinopsis: " + sinopsis[0]
    plot = re.sub("<[^>]+>"," ",plot)
    # Busca el trailer 
    patronvideos = '<param name="movie" value="([^"]+)"></param>'
    matchtrailer = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    if len(matchtrailer)>0:
        for match in matchtrailer:
        # A�ade al listado de XBMC
            xbmctools.addnewvideo( __channel__ , "youtubeplay" , category ,"Directo", "Ver El Trailer de : "+title , match , thumbnail, plot )
    else:
        #import core.trailertools
        print title
        s = unicode( title, "latin-1" )
        # A�ade al listado de XBMC

        xbmctools.addnewfolder( "trailertools" , "buscartrailer" , category , config.get_localized_string(30110)+" "+title , url , os.path.join(IMAGES_PATH, 'trailertools.png'), plot ) # Buscar trailer para
        
        
    matchesBK = matches[0]
    # Extrae las entradas (videos) para megavideo con tipo de audio
    patronvideos  = '<span  style="font-size:12px;"><strong>(.*?)</strong></span><br/>.*?'
    patronvideos += '<span.*?>.*?<a href="http\:\/\/www.megavideo.com\/[\?v=|v/]+([A-Z0-9]{8}).*?" target="_blank">1</a>.</span><br />'
    
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    encontrados = set()
    for match in matches:
        if match[1] not in encontrados:
            encontrados.add(match[1])
        
            # Titulo
            scrapedtitle = title + " -   [" +scrapertools.entityunescape(match[0])+ "]" + " (Megavideo)"

            # URL
            scrapedurl = match[1]
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
            xbmctools.addnewvideo( __channel__ , "play" , category ,"Megavideo", scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
    if len(matches)==0:
        listavideos = servertools.findvideos(data)
        encontrados = set()
        for titulo,scrapedurl,servidor in listavideos:
            if scrapedurl.strip() not in encontrados:
                encontrados.add(scrapedurl.strip())
                xbmctools.addnewvideo( __channel__ , "play" , category ,servidor, title+ " - %s" % titulo  , scrapedurl , thumbnail, plot )        
    '''
    <span class="bloque-uploader">An�nimo</span>
    <span class="bloque-doblaje"><img src="../images/esp.gif" class="bandera" /></span>
    <span class="bloque-link">Opci�n 8: <a href="javascript:goTo('aHR0cDovL3d3dy5tZWdhdmlkZW8uY29tLz92PTVOM0JYOVMx', 'megavideo.com')" rel="nofollow">Ver pel�cula</a></span>
    '''
    patronvideos = '<span class="bloque-doblaje">(.+?)</span>[^<]+'
    patronvideos +='<span class="bloque-link">[^<]+<a href="#" onclick="goTo\(\'([^\']+)\'\, \'([^\']+)\'\).+?"(.+?)</span>'
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
            url2 = re.compile("onclick=\"goTo\(\'([^\']+)\'\, \'([^\']+)\'\)").findall(match[3])[0]
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
            
    # Busca otras peliculas relacionadas con los actores
    if len(matchesactores)>0:
        titulo = "Busca otros Films de los actores de esta pelicula"
        xbmctools.addnewfolder( __channel__ , "listaractores" , category , titulo , matchesBK , thumbnail, actores )
        
    # Lista peliculas relacionadas
    titulo = "Ver Peliculas Relacionadas" 
    matches = buscarelacionados(matchesBK)
    plot2 = "PELICULAS RELACIONADAS :\n\n"
    for match in matches:
        plot2 = plot2 + "-"+match[1]+"\n"
    xbmctools.addnewfolder( __channel__ , "listarelacionados" , category , titulo , matchesBK , thumbnail, plot2 , fanart = thumbnail )
    
    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
    logger.info("[peliculas21.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)

def youtubeplay(params,url,category):
    logger.info("[peliculas21.py] youtubeplay")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = "Ver Video"
    server = "Directo"
    id = youtube.Extract_id(url)
    videourl = youtube.geturl(id)

    if videourl == ("" or "Esc"):return
    logger.info("link directo de youtube : "+videourl)
    xbmctools.play_video("Trailer",server,videourl,category,title,thumbnail,plot)
 

def listaractores(params,data,category):
    logger.info("[peliculas21.py] listaractores")
    
    url1 = "http://www.peliculas21.com"
    actores = buscactores(data)
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
        listsimple(params,actorURL[seleccion],category)
    return
    
def buscactores(data):
    patronvideos = ' <a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    return(matches)
    
def listarelacionados(params,data,category):
    logger.info("[peliculas21.py] listaractores")
    
    url1 = "http://www.peliculas21.com"
    #patronvideos = '<div><a href="([^"]+)">([^<]+)</a><br'
    matches = buscarelacionados(data) #re.compile(patronvideos,re.DOTALL).findall(data)
    
    opciones = []
    URL = []
    for i in matches:
        opciones.append(i[1])
        URL.append(urlparse.urljoin(url1,i[0]))           
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Selecciona uno ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1:return
    else:
        listvideos(params,URL[seleccion],category)
    return
    
def buscarelacionados(data):
    patronvideos = '<div class="film"><a href="([^"]+)"><[^>]+><br />([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    return (matches)
    
def buscaporletraActor(params,url,category):
    logger.info("[peliculas21.py] buscaporletra")
    '''
    data = scrapertools.cachePage(url)
    patron  = '<div class="title">Listado de Actores</div><br/>(.*?)<div class="subtitulo">Abecedario</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    patron  = '<a href="(.*?)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(matches[0])
    '''    
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    opciones = []

    #opciones.append("Buscar por palabras (Teclado)")
    #opciones.append("0-9")
    for letra in letras:
        opciones.append(letra)
    dia = xbmcgui.Dialog()
    
    seleccion = dia.select("Elige una letra : ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 :return

    
    url   = "http://www.peliculas21.com/actores/%s/" %letras[seleccion]
    listActoresAlfab(params,url,category)
                
    
def listaActoresMasBuscados(params,url,category):
    logger.info("[peliculas21.py] listaActoresMasBuscados")
    
    url1 = "http://www.peliculas21.com"
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    patronvideos = 'Los m�s buscados:(.*?)M�s actores</a></div>'
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
        scrapedplot = "Busca los Films existentes de este Actor � Actriz"

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def listActoresAlfab(params,url,category):
    logger.info("[peliculas21.py] listaActoresAlfab")
    

    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    patronvideos = '<div class="actores_2">(.*?)</div></div>'
    matches1 = re.compile(patronvideos,re.DOTALL).findall(data)
    patronvideos = '<a href="([^"]+)">([^<]+)</a>'
    matches =  re.compile(patronvideos,re.DOTALL).findall(matches1[0])
    scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        scrapedtitle = match[1]
        # URL
    
        scrapedurl = urlparse.urljoin(url,match[0])
        # Thumbnail
        scrapedthumbnail = ""
        
        # Argumento
        scrapedplot = "Busca los Films existentes de este Actor � Actriz"

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
        
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def buscaporanyo(params,url,category):
    logger.info("[peliculas21.py] buscaporanyo")
    #url = "http://www.peliculas21.com/%s/%s/"
    anho=2011
    anyoactual = anho
    anyoinic   = 1950
    opciones = []
    for i in range(anyoactual-anyoinic+1):
        opciones.append(str(anyoactual))
        anyoactual = anyoactual - 1           
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Listar desde el A�o: ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 :return
    if seleccion == 0:
        url = "http://www.peliculas21.com/"+opciones[seleccion]+"/"+opciones[seleccion]+"/"
        listsimple(params,url,category)
        return
    if seleccion>30:
        anyoactual = anho + 30 - seleccion
        rangonuevo = 31
    else:
        anyoactual = anho
        rangonuevo = seleccion + 1
    desde      = opciones[seleccion]
    
    opciones2 = []
    for j in range(rangonuevo):
        opciones2.append(str(anyoactual))
        anyoactual = anyoactual - 1
    dia2 = xbmcgui.Dialog()
    seleccion2 = dia2.select("Listar hasta el a�o:",opciones2)
    if seleccion == -1 :
        url = "http://www.peliculas21.com/"+desde+"/"+desde+"/"
        listsimple(params,url,category)
        return
    url = "http://www.peliculas21.com/"+desde+"/"+opciones2[seleccion2]+"/"
    listsimple(params,url,category)
    return    
