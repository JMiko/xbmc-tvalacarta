# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelisflv.net by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE

from core import scrapertools
from core import config
from core import logger
from platformcode.xbmc import xbmctools
from core.item import Item
from core import downloadtools
from servers import vk
from servers import servertools

__channel__ = "pelisflv"
__category__ = "F"
__type__ = "xbmc"
__title__ = "PelisFlv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

ATOM_NS = 'http://www.w3.org/2005/Atom'
PLAYLIST_FILENAME_TEMP = "video_playlist.temp.pls"
FULL_FILENAME_PATH = os.path.join( config.get_setting("downloadpath"), PLAYLIST_FILENAME_TEMP )


# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[pelisflv.py] init")

def mainlist(params,url,category):
    logger.info("[pelisflv.py] mainlist")

    # A�ade al listado de XBMC

    xbmctools.addnewfolder( __channel__ , "listvideofeeds" , category , "Listar - Novedades"    ,"http://www.blogger.com/feeds/3207505541212690627/posts/default?start-index=1&max-results=25","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Listar - Estrenos","http://www.pelisflv.net/search/label/Estrenos","","")
    xbmctools.addnewfolder( __channel__ , "ListadoSeries"  , category , "Listar - Generos"        ,"http://www.pelisflv.net/","","")
    #xbmctools.addnewfolder( __channel__ , "ListadoSeries"  , category , "Listar - Series"        ,"http://www.pelisflv.net/","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Listar - Animacion"        ,"http://www.pelisflv.net/search/label/Animaci%C3%B3n","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Listar - Videos no Megavideo (FLV)"        ,"http://www.pelisflv.net/search/label/Flv","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Listar - Videos en Megavideo"        ,"http://www.pelisflv.net/search/label/Megavideo","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Videos Audio Espa�ol"        ,"http://www.pelisflv.net/search/label/Espa%C3%B1ol","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Videos Audio Latino"        ,"http://www.pelisflv.net/search/label/Latino","","")
    xbmctools.addnewfolder( __channel__ , "listvideos"     , category , "Videos Audio Original Sub Espa�ol"        ,"http://www.pelisflv.net/search/label/Sub%20Espa%C3%B1ol","","")
    xbmctools.addnewfolder( __channel__ , "search"         , category , "Buscar","http://www.pelisflv.net/","","")
    

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
    logger.info("[pelisflv.py] search")

    keyboard = xbmc.Keyboard()
    #keyboard.setDefault('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            searchUrl = "http://www.pelisflv.net/search?q="+tecleado
            listvideos(params,searchUrl,category)

def searchresults(params,url,category):
    logger.info("[pelisflv.py] SearchResult")
    
    
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #print data
    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="poster">[^<]+<a href="([^"]+)"'                          # URL
    patronvideos += '><img src="([^"]+)" width=[^\/]+\/>'                                 # TUMBNAIL
    patronvideos += '</a>[^<]+<[^>]+>[^<]+<[^>]+>[^<]+<a href="[^"]+">([^<]+)</a>'        # TITULO 
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Atributos
        scrapedurl = match[0]
        
        scrapedtitle =match[2]
        scrapedtitle = scrapedtitle.replace("&#8211;","-")
        scrapedtitle = scrapedtitle.replace("&nbsp;"," ")
        scrapedthumbnail = match[1]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Propiedades
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
            


def ListadoCapitulosSeries(params,url,category):
    logger.info("[pelisflv.py] ListadoCapitulosSeries")
    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    
    # Descarga la p�gina
    data = scrapertools.downloadpageGzip(url)
    #logger.info(data)

    # Patron de las entradas

    patron = "<div class='post-body entry-content'>(.*?)<div class='post-footer'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    

    patron = '<a href="([^"]+)"[^>]+><[^>]+>(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(matches[0])
    scrapertools.printMatches(matches)
    patron2 = '<iframe src="([^"]+)"'
    
    # A�ade las entradas encontradas
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        data2 = scrapertools.downloadpageGzip(match[0])
        matches2 = re.compile(patron2,re.DOTALL).findall(data2)
        scrapertools.printMatches(matches2)    
        scrapedurl = matches2[0]
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        

def ListadoSeries(params,url,category):
    logger.info("[pelisflv.py] ListadoSeries")
    title = urllib.unquote_plus( params.get("title") )
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Patron de las entradas
    if "Series" in title:
        patron = "<center><form>(.*?)</form></center>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    
        patron = '<option value="([^"]+)" />(.*?)\n'
        matches = re.compile(patron,re.DOTALL).findall(matches[0])
        scrapertools.printMatches(matches)
    
    elif "Generos" in title:
        
        patron = "<h2>Generos</h2>[^<]+<[^>]+>[^<]+<ul>(.*?)</ul>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
    
        patron = "<a dir='ltr' href='([^']+)'>(.*?)</a>"
        matches = re.compile(patron,re.DOTALL).findall(matches[0])
        scrapertools.printMatches(matches)

    # A�ade las entradas encontradas
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
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
    logger.info("[pelisflv.py] listvideos")

    if url=="":
        url = "http://www.pelisflv.net/"
                
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)


    # Extrae las entradas (carpetas)
    patronvideos  = "<h3 class='post-title entry-title'>[^<]+<a href='([^']+)'"  # URL
    patronvideos += ">([^<]+)</a>.*?"                                            # Titulo   
    patronvideos += '<img style="[^"]+" src="([^"]+).*?'           # TUMBNAIL               
    patronvideos += 'border=[^>]+>.*?<span[^>]+>(.*?)</span></div>'        # Argumento    
    #patronvideos += '</h1>[^<]+</div>.*?<div class=[^>]+>[^<]+'
    #patronvideos += '</div>[^<]+<div class=[^>]+>.*?href="[^"]+"><img '                    
    #patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  # IMAGEN , DESCRIPCION
    #patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    scrapedtitle = ""
    for match in matches:
        # Titulo
        
        scrapedtitle = match[1]
        # URL
        scrapedurl = match[0]
        # Thumbnail
        scrapedthumbnail = match[2]
         
        # Argumento
        scrapedplot = match[3]
        scrapedplot = re.sub("<[^>]+>"," ",scrapedplot)
        scrapedplot = scrapedplot.replace('&#8220;','"')
        scrapedplot = scrapedplot.replace('&#8221;','"')
        scrapedplot = scrapedplot.replace('&#8230;','...')
        scrapedplot = scrapedplot.replace("&nbsp;","")

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        
            # A�ade al listado de XBMC
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Extrae la marca de siguiente p�gina

    patronvideos  = "<div class='status-msg-hidden'>.+?<a href=\"([^\"]+)\""
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

def listvideofeeds(params,url,category):
    logger.info("[pelisflv.py] listvideosfeeds")
    data = None
    thumbnail = ""
    xmldata = urllib2.urlopen(url,data)
    
    xmldoc = minidom.parse(xmldata)
    xmldoc.normalize()
    #print xmldoc.toxml().encode('utf-8')
    xmldata.close()
    c = 0
    plot = ""
    for entry in xmldoc.getElementsByTagNameNS(ATOM_NS, u'entry'):
    #First title element in doc order within the entry is the title
        entrytitle = entry.getElementsByTagNameNS(ATOM_NS, u'title')[0]
        entrylink = entry.getElementsByTagNameNS(ATOM_NS, u'link')[2]
        entrythumbnail = entry.getElementsByTagNameNS(ATOM_NS, u'content')[0]
        etitletext = get_text_from_construct(entrytitle)
        elinktext = entrylink.getAttributeNS(EMPTY_NAMESPACE, u'href')
        ethumbnailtext = get_text_from_construct(entrythumbnail)
        regexp = re.compile(r'src="([^"]+)"')
        match = regexp.search(ethumbnailtext)
        if match is not None:
            thumbnail = match.group(1)
        regexp = re.compile(r'bold;">([^<]+)<')
        match = regexp.search(ethumbnailtext)
        if match is not None:
            plot = match.group(1)
        print ethumbnailtext
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+etitletext)
            logger.info("scrapedurl="+elinktext)
            logger.info("scrapedthumbnail="+thumbnail)
                
        #print etitletext, '(', elinktext, thumbnail,plot, ')'
        xbmctools.addnewfolder( __channel__ , "detail" , category ,  etitletext,  elinktext, thumbnail, plot )
        c +=1
    
    if c >= 25:
        regexp = re.compile(r'start-index=([^\&]+)&')
        match = regexp.search(url)
        if match is not None:
            start_index = int(match.group(1)) + 25
        scrapedtitle = "P�gina siguiente"
        scrapedurl =  "http://www.blogger.com/feeds/3207505541212690627/posts/default?start-index="+str(start_index)+"&max-results=25"
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listvideofeeds" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Cierra el directorio
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
    
def get_text_from_construct(element):
    '''
    Return the content of an Atom element declared with the
    atomTextConstruct pattern.  Handle both plain text and XHTML
    forms.  Return a UTF-8 encoded string.
    '''
    if element.getAttributeNS(EMPTY_NAMESPACE, u'type') == u'xhtml':
        #Grab the XML serialization of each child
        childtext = [ c.toxml('utf-8') for c in element.childNodes ]
        #And stitch it together
        content = ''.join(childtext).strip()
        return content
    else:
        return element.firstChild.data.encode('utf-8')


    
def detail(params,url,category):
    logger.info("[pelisflv.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )
    accion = params.get("accion")

    # Descarga la p�gina
    datafull = scrapertools.cachePage(url)
    #logger.info(data)
    patron = "google_ad_section_start(.*?)google_ad_section_end -->"
    matches = re.compile(patron,re.DOTALL).findall(datafull)
    data2 = ""
    if len(matches)>0:
        data = matches[0]
    else:
        data = datafull
    patron = '<iframe src="(http://pelisflv.net63.net/player/[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = scrapertools.cachePage(matches[0])
    patron = 'href="(http://gamezinepelisflv.webcindario.com/[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(datafull)
    if len(matches)>0:
        data2 = scrapertools.cachePage(matches[0])
        data = data + data2
    ok = False               
          
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        videotitle = video[0]
        url = video[1]
        server = video[2]
        
        xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
    
    # Busca enlaces en el servidor Stagevu - "el modulo servertools.findvideos() no los encuentra"
    
    patronvideos  = "(http://stagevu.com[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        logger.info(" Servidor Stagevu")
        for match in matches:
            ok = True
            scrapedurl = match.replace("&amp;","&")
            xbmctools.addnewvideo( __channel__ ,"play"  , category , "Stagevu" , title+" - [Stagevu]", scrapedurl , thumbnail , plot )

    # Busca enlaces en el servidor Movshare - "el modulo servertools.findvideos() no los encuentra"
    
    patronvideos  = "(http://www.movshare.net[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        logger.info(" Servidor Movshare")
        for match in matches:
            ok = True
            scrapedurl = match.replace("&amp;","&")
            xbmctools.addnewvideo( __channel__ ,"play"  , category , "Movshare" , title+" - [Movshare]", scrapedurl , thumbnail , plot )


        
    # ------------------------------------------------------------------------------------
        #--- Busca los videos Directos
        
    patronvideos = 'file=(http\:\/\/[^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    print "link directos encontrados :%s" %matches

    #print data
    if len(matches)>0:
        for match in matches:
            subtitle = "[FLV-Directo]"
            if ("xml" in match):
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
                
                for match2 in matches2:
                    sub = ""
                    playWithSubt = "play"
                    if match2[2].endswith(".xml"): # Subtitulos con formato xml son incompatibles con XBMC
                        sub = "[Subtitulo incompatible con xbmc]"
                        
                    if ".mp4" in match2[1]:
                        subtitle = "[MP4-Directo]"
                    scrapedtitle = '%s  - (%s)  %s' %(title,match2[0],subtitle)
                    
                    scrapedurl = match2[1].strip()
                    scrapedthumbnail = thumbnail
                    scrapedplot = plot
                    
                    if match2[2].endswith(".srt"): 
                        scrapedurl = scrapedurl + "|" + match2[2]
                        playWithSubt = "play2"
                            
                    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                            
                    # A�ade al listado de XBMC
                    xbmctools.addnewvideo( __channel__ , playWithSubt , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )
                    ok = True
            else:
                if match.endswith(".srt"):
                    scrapedurl = scrapedurl + "|" + match 
                    xbmctools.addnewvideo( __channel__ ,"play2"  , category , "Directo" , title + " (V.O.S) - "+subtitle, scrapedurl , thumbnail , plot )
                    ok = True
                if     match.endswith(".xml"):
                    sub = "[Subtitulo incompatible con xbmc]"
                    xbmctools.addnewvideo( __channel__ ,"play"  , category , "Directo" , title + " (V.O) - %s %s" %(subtitle,sub), scrapedurl , thumbnail , plot )
                    ok = True
                scrapedurl = match
                print scrapedurl
    #src="http://pelisflv.net63.net/player/videos.php?x=http://pelisflv.net63.net/player/xmls/The-Lord-Of-The-Ring.xml"            
    patronvideos = '(http\:\/\/[^\/]+\/[^\/]+\/[^\/]+\/[^\.]+\.xml)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    #print data
    
    if len(matches)>0:
        playlistFile = open(FULL_FILENAME_PATH,"w")
        playlistFile.write("[playlist]\n")
        playlistFile.write("\n")
        for match in matches:
            subtitle = "[FLV-Directo]"
                    

            data2 = scrapertools.cachePage(match.replace(" ","%20"))
            logger.info("data2="+data2)
            patronvideos  = '<track>.*?'
            patronvideos += '<title>([^<]+)</title>.*?'
            patronvideos += '<location>([^<]+)</location>(?:[^<]+'
            patronvideos += '<meta rel="captions">([^<]+)</meta>[^<]+'
            patronvideos += '|([^<]+))</track>'
            matches2 = re.compile(patronvideos,re.DOTALL).findall(data2)
            scrapertools.printMatches(matches)
            c = 0
            for match2 in matches2:
                c +=1
                sub = ""
                playWithSubt = "play"
                if match2[2].endswith(".xml"): # Subtitulos con formato xml son incompatibles con XBMC
                    sub = "[Subtitulo incompatible con xbmc]"
                    
                if  match2[1].endswith(".mp4"):
                    subtitle = "[MP4-Directo]"
                scrapedtitle = '%s  - (%s)  %s' %(title,match2[0],subtitle)
                
                scrapedurl = match2[1].strip()
                scrapedthumbnail = thumbnail
                scrapedplot = plot
                
                if match2[2].endswith(".srt"): 
                    scrapedurl = scrapedurl + "|" + match2[2]
                    playWithSubt = "play2"
                        
                if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                        
                # A�ade al listado de XBMC
                xbmctools.addnewvideo( __channel__ , playWithSubt , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )                    
                ok =True
                
                playlistFile.write("File%d=%s\n"  %(c,match2[1]))
                playlistFile.write("Title%d=%s\n" %(c,match2[0]))
                playlistFile.write("\n")
                
            
            playlistFile.write("NumberOfEntries=%d\n" %c)
            playlistFile.write("Version=2\n")
            playlistFile.flush();
            playlistFile.close()
            if c>0:
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , "Reproducir Todo a la vez...", FULL_FILENAME_PATH , scrapedthumbnail, scrapedplot )
    
    # Busca enlaces en el servidor Videoweed - "el modulo servertools.findvideos() no los encuentra"
    patronvideos = '(http\:\/\/[^\.]+\.videoweed.com\/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        logger.info(" Servidor Videoweed")
        for match in matches:
            ok = True
            scrapedurl = match.replace("&amp;","&")
            xbmctools.addnewvideo( __channel__ ,"play"  , category , "Videoweed" , title+" - [Videoweed]", scrapedurl , thumbnail , plot )        
    
    # Busca enlaces en el servidor Gigabyteupload # http://cdn-2.gigabyteupload.com/files/207bb7b658d5068650ebabaca8ffc52d/vFuriadeTitanes_newg.es.avi
    patronvideos = '(http\:\/\/[^\.]+\.gigabyteupload.com\/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        logger.info(" Servidor Gigabyteupload")
        for match in matches:
            ok = True
            xbmctools.addnewvideo( __channel__ ,"play"  , category , "Gigabyteupload" , title+" - [Gigabyteupload]",match  , thumbnail , plot )

    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces de videos para el servidor vk.com                             #
    ## --------------------------------------------------------------------------------------##
    '''
    var video_host = '447.gt3.vkadre.ru';
    var video_uid = '0';
    var video_vtag = '2638f17ddd39-';
    var video_no_flv = 0;
    var video_max_hd = '0';
    var video_title = 'newCine.NET+-+neWG.Es+%7C+Chicken+Little';

    
    patronvideos = 'src="(http://[^\/]+\/video_ext.php[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        ok = True
        print " encontro VK.COM :%s" %matches[0]

        videourl =     vk.geturl(matches[0])
        xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+"[VK]", videourl , thumbnail , plot )        
    '''
    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces a video en el servidor Dailymotion                             #
    ## --------------------------------------------------------------------------------------##
    patronvideos = 'http://www.dailymotion.com/swf/video/([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    playWithSubt = "play"
    subtit = ""
    if len(matches)>0:
        daily = 'http://www.dailymotion.com/video/%s'%matches[0]
        data2 = scrapertools.cachePage(daily)
        
        # Busca los subtitulos en espa�ol 
        subtitulo = re.compile('%22es%22%3A%22(.+?)%22').findall(data2)
        if len(subtitulo)>0:
            subtit = urllib.unquote(subtitulo[0])
            subtit = subtit.replace("\/","/")
        
                
        # Busca el enlace al video con formato FLV     
        Lowres=re.compile('%22sdURL%22%3A%22(.+?)%22').findall(data2)
        if len(Lowres)>0:
            videourl = urllib.unquote(Lowres[0])
            videourl = videourl.replace("\/","/")
            if len(subtit)>0:
                videourl = videourl + "|" + subtit
                playWithSubt = "play2"
            subtitle = "[FLV-Directo-Dailymotion]"
            xbmctools.addnewvideo( __channel__ , playWithSubt , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
        
        # Busca el enlace al video con formato HQ (H264)        
        Highres=re.compile('%22hqURL%22%3A%22(.+?)%22').findall(data2)
        if len(Highres)>0:
            videourl = urllib.unquote(Highres[0])
            videourl = videourl.replace("\/","/")
            if len(subtit)>0:
                videourl = videourl + "|" + subtit
                playWithSubt = "play2"            
            subtitle = "[h264-Directo-Dailymotion-este video no es soportado en versiones antiguas o xbox plataforma]"
            xbmctools.addnewvideo( __channel__ , playWithSubt , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )

    if not ok:
        patron = "SeriesPage"
        matches = re.compile(patron,re.DOTALL).findall(datafull)
        if len(matches)>0:
            ListadoCapitulosSeries(params,url,category)
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def play(params,url,category):
    logger.info("[pelisflv.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]

    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)

def play2(params,url,category):
    logger.info("[pelisflv.py] play2")
    url1 = url
    if "|" in url:
        urlsplited = url.split("|")
        url1 = urlsplited[0]
        urlsubtit = urlsplited[1]
        subt_ok = "0"
        count = 0
        while subt_ok == "0":
            if count==0:
                subt_ok = downloadstr(urlsubtit)
                count += 1 
            print "subtitulo subt_ok = %s" % str(subt_ok)
            if subt_ok is None: # si es None la descarga del subtitulo esta ok
                config.set_setting("subtitulo", "true")
                break
    play(params,url1,category)

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
        
def downloadstr(urlsub):
    
    from core import downloadtools
    
    fullpath = os.path.join( config.get_data_path() , 'subtitulo.srt' )
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

        
