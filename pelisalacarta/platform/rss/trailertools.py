# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Buscador de Trailers en youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import sys
import string
import os

sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , "../../lib" ) ) )

import gdata.youtube.service
from core.item import Item

try:
    from core import scrapertools
    from core import logger
    from core import config
except:
    from Code.core import scrapertools
    from Code.core import logger
    from Code.core import config
from rsstools import DepuraTitulo as DepuraTitulo
from rsstools import LimpiarTitulo as LimpiarTitulo

CHANNELNAME = "trailertools"
# Esto permite su ejecución en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

DEBUG = True

### Nueva función para modificación en RTD1283
def search(item,titulo):
    itemlist = []
    listavideos = gettrailer(titulo,"","false")
    if len(listavideos)>0:
        for video in listavideos:
            try:
                plot = video[4]
            except: plot = ""
            if video[5]=="YOUTUBE": fulltitle = "Duración "+video[3]+" (youtube.com)"
            else: fulltitle = "(trailerdepeliculas.org)"
            
            itemlist.append( Item(channel=CHANNELNAME, title=video[1] , url=video[0], server="youtube" ,action="play",  folder=False, thumbnail=video[2], fulltitle=video[1], plot=plot) )
    else: 
       itemlist.append( Item(channel=CHANNELNAME, title="Ninguno hallado. Redifinir busqueda" , url="none" ,action="search") )
       itemlist.append( Item(channel=CHANNELNAME, title="Menú principal" , url="none" ,action="EXIT") )
    return itemlist

###
def gettrailer(titulovideo,category="",solo="false"):
    print "[trailertools.py] Modulo: gettrailer(titulo = %s , category = %s)"  % (titulovideo,category)
    titulovideo = LimpiarTitulo(urllib.unquote_plus(titulovideo))
    if not solo=="true":
        titulo = DepuraTitulo(titulovideo)
        encontrados = []
        if len(titulo)==0:
            titulo = "El_video_no_tiene_titulo"

        encontrados = GetFrom_Trailersdepeliculas(titulo)      # Primero busca en www.trailerdepeliculas.org
        encontrados  = encontrados + GetVideoFeed(titulo)      # luego busca con el API de youtube 
    else:
        titulo = titulovideo
        encontrados = []
        if len(titulo)==0:
            titulo = "El_video_no_tiene_titulo"
        encontrados = GetFrom_Trailersdepeliculas(titulo)      # Primero busca en www.trailerdepeliculas.org
        encontrados  = encontrados + GetVideoFeed(titulo,"false")
    if len(encontrados)==0: 
        encontrados = GetFromYoutubePlaylist(titulo)           # si no encuentra, busca en las listas de la web de youtube
    
    return encontrados
    
def GetFrom_Trailersdepeliculas(titulovideo):
    print "[trailertools.py] Modulo: GetFrom_Trailersdepeliculas(titulo = %s)"  % titulovideo
    devuelve = []
    
    
    titulo = LimpiarTitulo(titulovideo)
    # ---------------------------------------
    #  Busca el video en la pagina de www.trailerdepeliculas.org,
    #  la busqueda en esta pagina es porque a veces tiene los
    #  trailers en ingles y que no existen en español
    # ----------------------------------------
    c = 0
    url1 ="http://www.trailersdepeliculas.org/"
    url  ="http://www.trailersdepeliculas.org/buscar.html"
    urldata=getpost(url,{'busqueda': titulo})
    #logger.info("post url  :  "+urldata)

    patronvideos = '<div class="cnt">\s+?<h4><a href="([^"]+?)">([^<]+?)</a></h4>' # url, title
    matches  = re.compile(patronvideos,re.DOTALL).findall(urldata)
    if len(matches)>0:
        patronvideos1 = 'movie" value="http://www.youtube.com/v/([^&]+)&' # url
        patronvideos2 = '<img src="([^"]+?)"[^>]+?>\s+<h4>[^<]+?</h4>.+?votos\)</p>\s*?<p[^>]+?>([^<]+?)</p>' # thumbnail, plot
        for match in matches:
            logger.info("Trailers encontrados en www.trailerdepeliculas.org :  "+match[1])
            #url2  ="http://www.trailersdepeliculas.org/"+match[0]
            if titulo in (string.lower(LimpiarTitulo(match[1]))):
                urlpage = urlparse.urljoin(url1,match[0])
                #thumbnail = urlparse.urljoin(url1,match[2])
                data     = scrapertools.cachePage(urlpage)
                logger.info("Trailer elegido :  "+match[1])
                matches2 = re.compile(patronvideos1,re.DOTALL).findall(data)
                matches3 = re.compile(patronvideos2,re.DOTALL).findall(data)
                for match2 in matches2:
                    logger.info("link yt del Trailer encontrado :  "+match2)
                    c=c+1
                    thumbnail = urlparse.urljoin(url1,matches3[0][0])
                    plot = matches3[0][1]
                    devuelve.append( ["http://www.youtube.com/watch?v="+match2+"&feature=youtube_gdata_player", match[1] , thumbnail,"", plot, "TRAILERDEPELICULAS"] )
            
        logger.info(" lista de links encontrados U "+str(len(match)))
    print '%s Trailers encontrados en Modulo: GetFrom_Trailersdepeliculas()' % str(c)
    return devuelve

####################################################################################################
# Buscador de Trailer : mediante el servicio de Apis de Google y Youtube                           #
####################################################################################################
        
def GetVideoFeed(titulo,solo="false"):
    print "[trailertools.py] Modulo: GetVideoFeed(titulo = %s)"  % titulo
    if solo=="true":
        esp   = ""
        noesp = ""
    else:
        esp   = " trailer espanol"
        noesp = " trailer"
    devuelve = []
    encontrados = set()
    c = 0
    yt = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = titulo+esp
    print query.vq
    query.orderby = 'relevance' #'viewCount'
    query.racy = 'include'
    #query.client = 'ytapi-youtube-search'
    #query.alt = 'rss'
    #query.v = '2'
    feed = yt.YouTubeQuery(query)
    plot = ""
    
    if solo=="true" :
        for entry in feed.entry:
            print 'Video title: %s' % entry.media.title.text
            titulo2 = str(entry.media.title.text)
            url = entry.media.player.url
            duracion = int(entry.media.duration.seconds)
            duracion = "%02d:%02d" % ( int( duracion / 60 ), duracion % 60)
            
            for thumbnail in entry.media.thumbnail:
                url_thumb = thumbnail.url
            
            devuelve.append([url,titulo2,url_thumb,duracion, plot, "YOUTUBE"])
            
            
        return (devuelve)        
    else:    
        for entry in feed.entry:
            print 'Video title: %s' % entry.media.title.text
            titulo2 = str(entry.media.title.text)
            url = entry.media.player.url
            duracion = int(entry.media.duration.seconds)
            duracion = "%02d:%02d" % ( int( duracion / 60 ), duracion % 60, )
            if titulo in (LimpiarTitulo(titulo2)): 
                for thumbnail in entry.media.thumbnail:
                    url_thumb = thumbnail.url
                if url not in encontrados:
                    devuelve.append([url,titulo2,url_thumb,duracion, plot, "YOUTUBE"])
                    encontrados.add(url)
                    c = c + 1
                if c > 10:
                    return (devuelve)
        if c < 6:
            query.vq =titulo+noesp
            feed = yt.YouTubeQuery(query)
            for entry in feed.entry:
                print 'Video title: %s' % entry.media.title.text
                titulo2 = str(entry.media.title.text)
                url = entry.media.player.url
                duracion = int(entry.media.duration.seconds)
                duracion = "%02d:%02d" % ( int( duracion / 60 ), duracion % 60, )
                if titulo in (LimpiarTitulo(titulo2)):
                    for thumbnail in entry.media.thumbnail:
                        url_thumb = thumbnail.url
                    
                    if url not in encontrados:
                        devuelve.append([url,titulo2,url_thumb,duracion, plot, "YOUTUBE"])
                        encontrados.add(url)
                        c = c + 1
                    if c > 10:
                        return (devuelve)
        if c < 6:
            query.vq =titulo
            feed = yt.YouTubeQuery(query)
            for entry in feed.entry:
                print 'Video title: %s' % entry.media.title.text
                titulo2 = str(entry.media.title.text)
                url = entry.media.player.url
                duracion = int(entry.media.duration.seconds)
                duracion = " (%02d:%02d)" % ( int( duracion / 60 ), duracion % 60, )
                if titulo in (LimpiarTitulo(titulo2)):
                    for thumbnail in entry.media.thumbnail:
                        url_thumb = thumbnail.url
                    
                    if url not in encontrados:
                        devuelve.append([url,titulo2,url_thumb,duracion, plot, "YOUTUBE"])
                        encontrados.add(url)
                        c = c + 1
                    if c > 10:
                        return (devuelve)

    print '%s Trailers encontrados en Modulo: GetVideoFeed()' % str(c)
    return (devuelve)
    
def GetFromYoutubePlaylist(titulovideo):
    print "[trailertools.py] Modulo: GetFromYoutubePlaylist(titulo = %s)"  % titulovideo
    devuelve = []    
    #
    # ---------------------------------------
    #  Busca el video en las listas de youtube
    # ---------------------------------------
    c = 0
    #http://www.youtube.com/results?search_type=search_playlists&search_query=luna+nueva+trailer&uni=1
    for i in ["+trailer+espa%C3%B1ol","+trailer"]:
        listyoutubeurl  = "http://www.youtube.com/results?search_type=search_playlists&search_query="
        listyoutubeurl += titulovideo.replace(" ","+")+i+"&uni=1"
        listyoutubeurl = listyoutubeurl.replace(" ","")
        logger.info("Youtube url parametros de busqueda  :"+listyoutubeurl)
        data = scrapertools.cachePage(listyoutubeurl)

        thumbnail=""
        patronyoutube  = '<span><a class="hLink" title="(.*?)" href="(.*?)">.*?'
        #patronyoutube += '<span class="playlist-video-duration">(.*?)</span>'
        matches  = re.compile(patronyoutube,re.DOTALL).findall(data)
        if len(matches)>0:
            for match in matches:
                logger.info("Trailer Titulo encontrado :"+match[0])
                logger.info("Trailer Url    encontrado :"+match[1])
                logger.info("Trailer Titulo Recortado  :"+string.lower(LimpiarTitulo(match[0])))
                if (titulovideo) in (string.lower(LimpiarTitulo(match[0]))):
                    campo = match[1]
                    longitud = len(campo)
                    campo = campo[-11:]
                    logger.info("codigo del video :  "+campo)
                    scrapedurl = "http://www.youtube.com/watch?v="+campo
                    patron    = "(http\:\/\/i[^/]+/vi/"+campo+"/default.jpg)"
                    matches2  = re.compile(patron,re.DOTALL).findall(data)
                    if len(matches2)>0:
                        thumbnail = matches2[0]
                    c = c + 1
                    logger.info("Trailer elegido :  "+match[1])
                    devuelve.append( [scrapedurl, match[0] , thumbnail,""] )
                    #scrapedthumbnail = thumbnail
                    #scrapedtitle     = match[0]
                    #scrapedurl       = match[1]
                    if c == 6 :
                        break
            #logger.info(" Total de links encontrados U "+str(len(match)))
        if c == 6:break
    print '%s Trailers encontrados en Modulo: GetFromYoutubePlaylist()' % str(c)
    return devuelve

    

def getpost(url,values): # Descarga la pagina con envio de un Form
    try:
        data = urllib.urlencode(values)          
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read() 
        return the_page 
    except Exception: 
        return "Err " 



