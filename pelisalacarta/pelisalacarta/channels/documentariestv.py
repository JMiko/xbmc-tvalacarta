# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documentariestv.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

#from pelisalacarta import buscador

__channel__ = "documentariestv"
__category__ = "D"
__type__ = "generic"
__title__ = "DocumentariesTV"
__language__ = "EN"

DEBUG = config.get_setting("debug")

tecleadoultimo = ""
IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'documaniatv' )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[documentariestv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="documentalesnuevos"  , title="New documentaries" , url="http://www.documentariestv.net/newvideos.html",thumbnail=os.path.join(IMAGES_PATH, 'nuevos.png')))
    itemlist.append( Item(channel=__channel__, action="TipoDocumental"      , title="By type"           , url="http://www.documentariestv.net/index.html",thumbnail=os.path.join(IMAGES_PATH, 'tipo.png')))
    itemlist.append( Item(channel=__channel__, action="tagdocumentales"     , title="By tag"            , url="http://www.documentariestv.net/index.html",thumbnail=os.path.join(IMAGES_PATH, 'tag.png')))
    #itemlist.append( Item(channel=__channel__, action="topdocumentales"     , title="Top documentales online"          , url="http://www.documaniatv.com/topvideos.html",thumbnail=os.path.join(IMAGES_PATH, 'top.png')))
    #itemlist.append( Item(channel=__channel__, action="listatipodocumental" , title="Documentales siendo vistos ahora" , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'viendose.png')))
    #itemlist.append( Item(channel=__channel__, action="documentaldeldia"    , title="Documental del dia"               , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'deldia.png')))
    #itemlist.append( Item(channel=__channel__, action="search"              , title="Buscar"                           , url="http://www.cinetube.es/peliculas/",thumbnail=os.path.join(IMAGES_PATH, 'search_icon.png')))
    return itemlist

def documentalesnuevos(item):
    logger.info("[documentariestv.py] documentalesnuevos")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<tr><td.*?<a href="([^"]+)">'
    patronvideos += '<img src="([^"]+)".*?'
    patronvideos += 'alt="([^"]+)".*?'
    patronvideos += 'width="250">([^<]+)<'
    patronvideos += 'td class.*?<a href="[^"]+">[^<]+</a></td><td class.*?>([^<]+)</td></tr>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info("matches = "+str(matches))

    for match in matches:
        scrapedtitle = acentos(match[2])+" - " + match[3]+" - " + match[4] 
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        imagen = ""
        scrapedplot = match[3]
        tipo = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Busca enlaces de paginas siguientes...
    cat = "nuevo"
    patronvideo = patronvideos
    itemlist.extend(paginasiguientes(patronvideo,data,"",cat))
    
    return itemlist


def TipoDocumental(item):
    logger.info("[documentariestv.py] TipoDocumental")
    itemlist = []

    # Saca el bloque con las categorias
    data = scrapertools.cache_page(item.url)
    patron = '<ul id="ul_categories">(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return []
    
    # Saca la lista de categorias
    data = matches[0]
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__ , action="listatipodocumental" , title=match[1],url=match[0]))
    
    return itemlist

def listatipodocumental(item):
    logger.info("[documentariestv.py] listatipodocumental")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    if item.url == "http://www.documentariestv.net/index.html":
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
        scrapedtitle = acentos(match[2])
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        
        # procesa el resto
        if cat == "tipo":
           scrapedplot = match[3]
        else:
           for campo in re.findall("/(.*?)/",match[0]):
                scrapedplot = campo

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle + " - " + scrapedplot , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if cat == "tipo":
        patron_pagina_sgte = '</span><a href="([^"]+)"'
        itemlist.extend( paginasiguientes(patron_pagina_sgte,data,"",cat))

    return itemlist

def tagdocumentales(item):
    logger.info("[documentariestv.py] tagdocumentales")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<a href="([^"]+)" class="tag_cloud_link" style="[^>]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__ , action="tagdocumentaleslist" , title=match[1],url=match[0]))
    
    return itemlist

def tagdocumentaleslist(item):
    logger.info("[documentariestv.py] tagdocumentaleslist")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae el listado de documentales del tag
    patronvideos  = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)"'
    patronvideos += '>[^<]+<img src="([^"]+)"  alt="([^"]+)".*?<span class="artist_name">([^<]+)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)         

    for match in matches:
        scrapedtitle = acentos(match[2])
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapeddescription = match[3]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle + " - " + scrapeddescription , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    # P�gina siguiente
    patron = '<a href="([^"]+)">next &raquo;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)         
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="tagdocumentaleslist", title="P�gina siguiente" , url=urlparse.urljoin(item.url,match) , folder=True) )
    
    return itemlist

def detail(item):
    logger.info("[documentariestv.py] detail")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    descripcion = ""
    plot = ""
    patrondescrip = '<h3>Description</h3>(.*?)<br><br>'
    matches = re.compile(patrondescrip,re.DOTALL).findall(data)
    if len(matches)>0:
        descripcion = matches[0]
        descripcion = descripcion.replace("&nbsp;","")
        descripcion = descripcion.replace("<br/>","")
        descripcion = descripcion.replace("\r","")
        descripcion = descripcion.replace("\n"," ")
        descripcion = descripcion.replace("\t"," ")
        descripcion = re.sub("<[^>]+>"," ",descripcion)
        descripcion = acentos(descripcion)
        try :
            plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
        except:
            plot = descripcion

    # Busca los enlaces a los videos de : "Megavideo"
    video_itemlist = servertools.find_video_items(data=data)
    for video_item in video_itemlist:
        itemlist.append( Item(channel=__channel__ , action="play" , server=video_item.server, title=item.title+video_item.title,url=video_item.url, thumbnail=video_item.thumbnail, plot=video_item.plot, folder=False))

    # Extrae los enlaces a los v�deos (Directo)
    patronvideos = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        if not "www.youtube" in matches[0]:
            itemlist.append( Item(channel=__channel__ , action="play" , server="Directo", title=item.title+" [directo]",url=matches[0], thumbnail=item.thumbnail, plot=item.plot))

    return itemlist

def documentalesnuevoslist(params,url,category):
    logger.info("[documentariestv.py] DocumentalesNuevos")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<tr><td.*?<a href="([^"]+)">'
    patronvideos += '<img src="([^"]+)".*?'
    patronvideos += 'alt="([^"]+)".*?'
    patronvideos += 'width="250">([^<]+)<'
    patronvideos += 'td class.*?<a href="[^"]+">[^<]+</a></td><td class.*?>([^<]+)</td></tr>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #logger.info("matches = "+str(matches))
    if DEBUG:
            scrapertools.printMatches(matches)
    for match in matches:
        # Titulo
        # Titulo
        scrapedtitle = acentos(match[2])+" - " + match[3]+" - " + match[4] 

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

def documentaldeldia(params,url,category):
#    list(params,url,category,patronvideos)
    logger.info("[documentariestv.py] Documentaldeldia")
               
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
        
    patronvideos = 'Now Playing: <a href="([^"]+)">([^<]+)</a>'
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
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True ) 

def topdocumentales(params,url,category):
    url2=url
    # Abre el di�logo de selecci�n
    opciones = []
    opciones.append("All time")
    opciones.append("Last 7 days")
    opciones.append("Biography")
    opciones.append("Technology")
    opciones.append("Science")
    opciones.append("Nature")
    opciones.append("Politics")
    opciones.append("History")
    opciones.append("Sport")
    opciones.append("Mysteries")
    opciones.append("Social")
    opciones.append("Travel/adventure")
    opciones.append("Art/Cinema")
    opciones.append("Religion/Spirituality")
    opciones.append("Terrorism/911")
    opciones.append("Drugs")
    opciones.append("Crime/Prison")
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Select one", opciones)
    logger.info("seleccion=%d" % seleccion) 
    if seleccion==-1:
        return
    if seleccion==0:
        url2 = "http://www.documentariestv.net/topvideos.html"
    elif seleccion==1:
        url2 = "http://www.documentariestv.net/topvideos.html?do=recent"
    elif seleccion==2:
        url2 = "http://www.documentariestv.net/topvideos.html?c=Biography"
    elif seleccion==3:
        url2 = "http://www.documentariestv.net/topvideos.html?c=Technology" 
    elif seleccion==4: 
        url2 = "http://www.documentariestv.net/topvideos.html?c=Science"
    elif seleccion==5: 
        url2 = "http://www.documentariestv.net/topvideos.html?c=nature"
    elif seleccion==6:
        url2 = "http://www.documentariestv.net/topvideos.html?c=politics"
    elif seleccion==7:
        url2 = "http://www.documentariestv.net/topvideos.html?c=history"
    elif seleccion==8:
        url2 = "http://www.documentariestv.net/topvideos.html?c=Sports"
    elif seleccion==9:
        url2 = "http://www.documentariestv.net/topvideos.html?c=Mysteries"
    elif seleccion==10:
        url2 = "http://www.documentariestv.net/topvideos.html?c=social" 
    elif seleccion==11:
        url2 = "http://www.documentariestv.net/topvideos.html?c=travel"
    elif seleccion==12:
        url2 = "http://www.documentariestv.net/topvideos.html?c=art"               
    elif seleccion==13:
        url2 = "http://www.documentariestv.net/topvideos.html?c=religion"
    elif seleccion==14:
        url2 = "http://www.documentariestv.net/topvideos.html?c=terrorism"               
    elif seleccion==15:
        url2 = "http://www.documentariestv.net/topvideos.html?c=drugs"               
    elif seleccion==16:
        url2 = "http://www.documentariestv.net/topvideos.html?c=crime"                  
                        
    toplist(params,url2,category)
############----------------------------------------------####################

def toplist(params,url,category):
    logger.info("[documentariestv.py] toplist")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    logger.info("[documentariestv.py] toplist "+url) 
    if url== "http://www.documentariestv.net/topvideos.html?do=recent":
            
        patronvideos = '<tr>[^>]+>([^<]+)</td>'
        patronvideos += '[^>]+><a href="([^"]+)">'
        patronvideos += '<img src="([^"]+)" alt="" class[^>]+>'
        patronvideos += '</a></td>[^>]+>([^<]+)</td>[^>]+>'
        patronvideos += '<a href="[^"]+">([^<]+)</a>'
        patronvideos += '</td>[^>]+>([^<]+)</td>'

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
        scrapedtitle = acentos(match[3])

        # URL
        scrapedurl = match[1]
        
        # Thumbnail
        scrapedthumbnail = match[2]
        
        # procesa el resto
        scrapedplot = match[4]+" - " + "Views : "+match[5]+" times"

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        # A�ade al listado de XBMC
        #        xbmctools.addnewvideo( __channel__ , "detail" , category , "directo" , match[0]+") "+scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )

        xbmctools.addthumbnailfolder( __channel__ , match[0]+") "+scrapedtitle+" - "+scrapedplot, scrapedurl , scrapedthumbnail, "detail" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############


def paginasiguientes(patronvideos,data,category,cat):

    itemlist = []

    patron    = '</span><a href="([^"]+)"' 
    matches   = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = "Next page"
        scrapedurl = "http://www.documentariestv.net/" + match
        scrapedthumbnail = os.path.join(IMAGES_PATH, 'next.png')

        if cat == 'tipo':
            itemlist.append( Item(channel=__channel__, action="listatipodocumental", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'nuevo':
            itemlist.append( Item(channel=__channel__, action="documentalesnuevos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'tag':
            itemlist.append( Item(channel=__channel__, action="tagdocumentaleslist", title=scrapedtitle , url="http://www.documentariestv.net"+match , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'busca':
            itemlist.append( Item(channel=__channel__, action="searchresults", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )

    return itemlist



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
  

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    items = documentalesnuevos(mainlist_items[0])
    bien = False
    for singleitem in items:
        mirrors = servertools.find_video_items( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien