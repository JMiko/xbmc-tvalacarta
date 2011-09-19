# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documaniatv.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

#from pelisalacarta import buscador

CHANNELNAME = "documaniatv"

logger.info("[documaniatv.py] init")
tecleadoultimo = ""
DEBUG = True
IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'documaniatv' )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[documaniatv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="documentalesnuevos"  , title="Novedades" , url="http://www.documaniatv.com/newvideos.html",thumbnail=os.path.join(IMAGES_PATH, 'nuevos.png')))
    itemlist.append( Item(channel=CHANNELNAME, action="TipoDocumental"      , title="Por tipos" , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'tipo.png')))
    itemlist.append( Item(channel=CHANNELNAME, action="tagdocumentales"     , title="Por tags"  , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'tag.png')))
    #itemlist.append( Item(channel=CHANNELNAME, action="topdocumentales"     , title="Top documentales online"          , url="http://www.documaniatv.com/topvideos.html",thumbnail=os.path.join(IMAGES_PATH, 'top.png')))
    #itemlist.append( Item(channel=CHANNELNAME, action="listatipodocumental" , title="Documentales siendo vistos ahora" , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'viendose.png')))
    #itemlist.append( Item(channel=CHANNELNAME, action="documentaldeldia"    , title="Documental del dia"               , url="http://www.documaniatv.com/index.html",thumbnail=os.path.join(IMAGES_PATH, 'deldia.png')))
    #itemlist.append( Item(channel=CHANNELNAME, action="search"              , title="Buscar"                           , url="http://www.cinetube.es/peliculas/",thumbnail=os.path.join(IMAGES_PATH, 'search_icon.png')))
    return itemlist

def documentalesnuevos(item):
    logger.info("[documaniatv.py] documentalesnuevos")
    itemlist = []

    # Descarga la página
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

        itemlist.append( Item(channel=CHANNELNAME, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Busca enlaces de paginas siguientes...
    cat = "nuevo"
    patronvideo = patronvideos
    itemlist.extend(paginasiguientes(patronvideo,data,"",cat))
    
    return itemlist

def TipoDocumental(item):
    logger.info("[documaniatv.py] TipoDocumental")
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
        itemlist.append( Item(channel=CHANNELNAME , action="listatipodocumental" , title=match[1],url=match[0]))
    
    return itemlist

def listatipodocumental(item):
    logger.info("[documaniatv.py] listatipodocumental")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    if item.url == "http://www.documaniatv.com/index.html":
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

        itemlist.append( Item(channel=CHANNELNAME, action="detail", title=scrapedtitle + " - " + scrapedplot , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if cat == "tipo":
        patron_pagina_sgte = '</span><a href="([^"]+)"'
        itemlist.extend( paginasiguientes(patron_pagina_sgte,data,"",cat))

    return itemlist

def tagdocumentales(item):
    logger.info("[documaniatv.py] tagdocumentales")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron = '<a href="([^"]+)" class="tag_cloud_link" style="[^>]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME , action="tagdocumentaleslist" , title=match[1],url=match[0]))
    
    return itemlist

def tagdocumentaleslist(item):
    logger.info("[documaniatv.py] tagdocumentaleslist")
    itemlist = []

    # Descarga la página
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

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="detail", title=scrapedtitle + " - " + scrapeddescription , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    # Página siguiente
    patron = '<a href="([^"]+)">next &raquo;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)         
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="tagdocumentaleslist", title="Página siguiente" , url=urlparse.urljoin(item.url,match) , folder=True) )
    
    return itemlist

def detail(item):
    logger.info("[documaniatv.py] detail")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    descripcion = ""
    plot = ""
    patrondescrip = '<h3>Descripci[^<]+</h3>(.*?)<br><br>'
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
        itemlist.append( Item(channel=CHANNELNAME , action="play" , server=video_item.server, title=item.title+video_item.title,url=video_item.url, thumbnail=video_item.thumbnail, plot=video_item.plot, folder=False))

    # Extrae los enlaces a los vídeos (Directo)
    patronvideos = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        itemlist.append( Item(channel=CHANNELNAME , action="play" , server="Directo", title=title+" [directo]",url=matches[0], thumbnail=thumbnail, plot=plot))

    return itemlist

def search(item):
    logger.info("[documaniatv.py] search")
    buscador.listar_busquedas(item)
    
def searchresults(item):
    logger.info("[documaniatv.py] search")
            
    buscador.salvar_busquedas(item)
    
    #convert to HTML
    tecleado = url.replace(" ", "+")
    searchUrl = "http://www.documaniatv.com/search.php?keywords="+tecleado+"&btn=Buscar"
    searchresults2(params,searchUrl,category)

def performsearch(texto):
    logger.info("[documaniatv.py] performsearch")
    url = "http://www.documaniatv.com/search.php?keywords="+texto+"&btn=Buscar"

    # Descarga la página
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

        # Añade al listado de XBMC
        resultados.append( [CHANNELNAME , "detail" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
        
    return resultados

def searchresults2(item):
    logger.info("[documaniatv.py] searchresults")

    # Descarga la página
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

        # Añade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )


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

def listarpor(item):
        url1=url
        title = urllib.unquote_plus(params.get("title"))[:11]
           
        #verifica si es la primera vez o viene de una paginacion
        if  url.endswith(".html"):               
            return(url)
        else:
            fecha = "videos-1-date.html"
            vistas = "videos-1-views.html"
            rating = "videos-1-rating.html" 
         # Abre el diálogo de selección
            opciones = []
        opciones.append("Fecha")
        opciones.append("Vistas")
        opciones.append("Votos")
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
        return(url1)
#############-----------------------------------#########################

def documentaldeldia(item):
#    list(item,patronvideos)
    logger.info("[documaniatv.py] Documentaldeldia")
               
    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
        
    patronvideos = 'Documental del dia:<[^>]+>.*?<a href="([^"]+)">([^<]+)</a>'
    matches =  re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        scrapedtitle = acentos(match[1])
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot ) 

    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True ) 

################---------------------------------------------------------###########


#############----------------------------------------------------------#############



############---------------------------------------------------#######################

def topdocumentales(item):
    url2=url
    # Abre el diálogo de selección
    opciones = []
    opciones.append("Todo el tiempo")
    opciones.append("Ultimos 7 dias")
    opciones.append("Politica")
    opciones.append("Naturaleza")
    opciones.append("Historia")
    opciones.append("Deporte")
    opciones.append("Biografias")
    opciones.append("en ingles")
    opciones.append("Ciencia y tecnologia")
    opciones.append("Social")
    opciones.append("Viajes")
    opciones.append("Arte y cine")
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Elige Listar Top por :", opciones)
    logger.info("seleccion=%d" % seleccion) 
    if seleccion==-1:
       return
    if seleccion==0:
       url2 = "http://www.documaniatv.com/topvideos.html"
    elif seleccion==1:
       url2 = "http://www.documaniatv.com/topvideos.html?do=recent"
    elif seleccion==2:
       url2 = "http://www.documaniatv.com/topvideos.html?c=politica"  
    elif seleccion==3:
       url2 = "http://www.documaniatv.com/topvideos.html?c=naturaleza"
    elif seleccion==4:
       url2 = "http://www.documaniatv.com/topvideos.html?c=historia" 
    elif seleccion==5: 
       url2 = "http://www.documaniatv.com/topvideos.html?c=deporte"
    elif seleccion==6: 
       url2 = "http://www.documaniatv.com/topvideos.html?c=biografias"
    elif seleccion==7:
       url2 = "http://www.documaniatv.com/topvideos.html?c=ingles"
    elif seleccion==8:
       url2 = "http://www.documaniatv.com/topvideos.html?c=tecnologia"
    elif seleccion==9:
       url2 = "http://www.documaniatv.com/topvideos.html?c=social"
    elif seleccion==10:
       url2 = "http://www.documaniatv.com/topvideos.html?c=viajes"
    elif seleccion==11:
       url2 = "http://www.documaniatv.com/topvideos.html?c=arte" 
 
    toplist(params,url2,category)
############----------------------------------------------####################

def toplist(item):
    logger.info("[documaniatv.py] toplist")

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    logger.info("[documaniatv.py] toplist "+url) 
    if url== "http://www.documaniatv.com/topvideos.html?do=recent":
            
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
        scrapedtitle = acentos(match[3])

        # URL
        scrapedurl = match[1]
        
        # Thumbnail
        scrapedthumbnail = match[2]
        
        # procesa el resto
        scrapedplot = match[4]+" - " + "Vistas : "+match[5]+" veces"

        xbmctools.addthumbnailfolder( CHANNELNAME , match[0]+") "+scrapedtitle+" - "+scrapedplot, scrapedurl , scrapedthumbnail, "detail" )

    # Label (top-right)...
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def paginasiguientes(patronvideos,data,category,cat):

    itemlist = []

    patron    = '</span><a href="([^"]+)"' 
    matches   = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = "Pagina siguiente"
        scrapedurl = "http://www.documaniatv.com/" + match
        scrapedthumbnail = os.path.join(IMAGES_PATH, 'next.png')

        if cat == 'tipo':
            itemlist.append( Item(channel=CHANNELNAME, action="listatipodocumental", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'nuevo':
            itemlist.append( Item(channel=CHANNELNAME, action="documentalesnuevos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'tag':
            itemlist.append( Item(channel=CHANNELNAME, action="tagdocumentaleslist", title=scrapedtitle , url="http://www.documaniatv.com"+match , thumbnail=scrapedthumbnail , folder=True) )
        elif cat == 'busca':
            itemlist.append( Item(channel=CHANNELNAME, action="searchresults", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , folder=True) )

    return itemlist

def acentos(title):

    title = title.replace("Ã‚Â", "")
    title = title.replace("ÃƒÂ©","é")
    title = title.replace("ÃƒÂ¡","á")
    title = title.replace("ÃƒÂ³","ó")
    title = title.replace("ÃƒÂº","ú")
    title = title.replace("ÃƒÂ­","í")
    title = title.replace("ÃƒÂ±","ñ")
    title = title.replace("Ã¢â‚¬Â", "")
    title = title.replace("Ã¢â‚¬Å“Ã‚Â", "")
    title = title.replace("Ã¢â‚¬Å“","")
    title = title.replace("Ã©","é")
    title = title.replace("Ã¡","á")
    title = title.replace("Ã³","ó")
    title = title.replace("Ãº","ú")
    title = title.replace("Ã­","í")
    title = title.replace("Ã±","ñ")
    title = title.replace("Ãƒâ€œ","Ó")
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
        scrapedtitle = acentos(match[2])
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapeddescription = match[3]
        scrapedplot = ""

        xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle+" - "+scrapeddescription , scrapedurl , scrapedthumbnail , scrapedplot )

    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
 
def Relacionados(item): 
    
    data = scrapertools.cachePage(url)
    print data
    verRelacionados(params,data,category)
