# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newdivx.net by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "newdivx"
__category__ = "F,D"
__type__ = "generic"
__title__ = "NewDivx"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[newdivx.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="peliculas", url="http://www.newdivx.net"))
    return itemlist

def peliculas(item):
    logger.info("[newdivx.py] peliculas")
    itemlist=[]

    # Descarga la p·gina
    data = scrapertools.cachePage(item.url)
    '''
    <td align="center" valign="middle" width="20%" class="short"> 
    <a href="http://www.newdivx.net/peliculas-online/comedia/4716-la-oportunidad-de-mi-vida-2010-lat.html"><img src="http://www.newhd.org/uploads/thumbs/1327685908_La_oportunidad_de_mi_vida-184333983-large.jpg"  alt='La oportunidad de mi vida (2010) [LAT]' title='La oportunidad de mi vida (2010) [LAT]'  style="max-width: 190px; "></a>
    <div><a href="http://www.newdivx.net/peliculas-online/comedia/4716-la-oportunidad-de-mi-vida-2010-lat.html">La oportunidad de mi vida (2010) [LAT]</a></div>
    '''

    # Patron de las entradas
    patronvideos  = '<td align="center" valign="middle" width="20%" class="short">[^<]+'
    patronvideos += '<a href="([^"]+)"><img src="([^"]+)"[^<]+</a>[^<]+'
    patronvideos += '<div><a [^>]+>([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # AÒade las entradas encontradas
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        # Atributos
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    #Extrae la marca de siguiente p·gina
    #<span>1</span> <a href="http://www.newdivx.net/peliculas-online/animacion/page/2/">2</a>
    patronvideos  = '</span> <a href="(http://www.newdivx.net.*?page/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P·gina siguiente >>"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def listvideos(params,url,category):
    logger.info("[newdivx.py] listvideos")

    if url=="":
        url = "http://www.newdivx.com/"
                
    # Descarga la p·gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

#<div class="news" title="Monsters (2010) [VOS]"><span class="title">&nbsp;&nbsp;&nbsp;<a href="http://www.newdivx.net/peliculas-online/terror/1589-monsters-2010-vos.html"></span title="3"><img src="http://www.newdivx.net/uploads/thumbs/1288901497_monsters-2010-poster-e1283548539539.jpg" style="border: medium none ;" width="184"; height="254" alt="" title=""><span class="title"></a></span>

    # Extrae las entradas (carpetas)
    patronvideos  = '<div class="news" title="([^"]+)"><span class="title">[^<]+<a href="([^"]+)">.*?<img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = match[1]
        scrapedthumbnail = match[2]
        scrapedplot = ""

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)

        
            # AÒade al listado de XBMC
            xbmctools.addnewfolder( __channel__ , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    #Extrae la marca de siguiente p·gina
    patronvideos  = '</span> <a href="(http://www.newdivx.net/videos/page/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "P·gina siguiente"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        xbmctools.addnewfolder( __channel__ , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
    logger.info("[newdivx.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )

    # Descarga la p·gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    patronvideos = '<p class="Estilo2">([^<]+)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        title = matches[0]   
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos en los servidores habilitados
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        if "stagevu.com/embed" not in video[1]:
            videotitle = video[0]
            url = video[1]
            server = video[2]
            xbmctools.addnewvideo( __channel__ , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
    # ------------------------------------------------------------------------------------
        #--- Busca los videos Directos
    ## ------------------------------------------------------------------------------------##
    #               Busca  enlaces en el servidor  przeklej                                 #
    ## ------------------------------------------------------------------------------------## 
        patronvideos = '<param name="src" value="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        if len(matches)>0:
            if len(matches)==1:
                subtitle = "[Divx-Directo-Przeklej]"
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, matches[0] , thumbnail , plot )
                 
            else:
                parte = 0
                subtitle = "[Divx-Directo-Przeklej]"
                for match in matches:
                    logger.info(" matches = "+match)
                    parte = parte + 1
                    xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle+" "+str(parte), match , thumbnail , plot )
                    
   ## --------------------------------------------------------------------------------------##
   #                   Busca enlaces en el servidor Fishker                                    #
   ## --------------------------------------------------------------------------------------##
    patronvideos = '<a href="(http\:\/\/www.fishker.com\/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data2 = scrapertools.cachePage(matches[0])
        #print data2
        #<param name="flashvars" value="comment=Q&amp;m=video&amp;file=http://fish14.st.fishker.com/videos/1249504.flv?c=3948597662&amp;st=/plstyle.txt?video=1"
        patron = 'file=([^"]+)"'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        if len(matches2)>0:
            videourl = matches2[0].replace("&amp;","&")
            subtitle = "[FLV-Directo-Fishker]"
            xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
            
   ## --------------------------------------------------------------------------------------##
   #                   Busca enlaces en el servidor Cinshare                                  #
   ## --------------------------------------------------------------------------------------##
    '''
    patronvideos = '<iframe src="(http://www.cinshare.com/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        ####
        #data2 = scrapertools.cachePage(matches[0])
        #print data2
        
        #patron = '<param name="src" value="([^"]+)"'
        #matches2 = re.compile(patron,re.DOTALL).findall(data2)
        #if len(matches2)>0:
        ####
        import cinshare
        videourl = matches[0]
        subtitle = "[divx-Directo-Cinshare]"
        xbmctools.addnewvideo( __channel__ , "play" , category ,"Cinshare", title + " - "+subtitle, videourl , thumbnail , plot )
    '''
    
    ## --------------------------------------------------------------------------------------##
    #               Busca enlaces a videos .flv o (.mp4 dentro de un xml)                     #
    ## --------------------------------------------------------------------------------------##
    patronvideos = 'file=(http\:\/\/[^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        subtitle = "[FLV-Directo]"
        if ("xml" in matches[0]):
            data2 = scrapertools.cachePage(matches[0])
            logger.info("data2="+data2)
            patronvideos  = '<track>.*?'
            patronvideos += '<title>([^<]+)</title>(?:[^<]+'
            patronvideos += '<annotation>([^<]+)</annotation>[^<]+|[^<]+)'
            patronvideos += '<location>([^<]+)</location>[^<]+'
            patronvideos += '</track>'
            matches = re.compile(patronvideos,re.DOTALL).findall(data2)
            scrapertools.printMatches(matches)

            for match in matches:
                if ".mp4" in match[2]:
                    subtitle = "[MP4-Directo]"
                scrapedtitle = '%s (%s) - %s  %s' %(title,match[1].strip(),match[0],subtitle)
                scrapedurl = match[2].strip()
                scrapedthumbnail = thumbnail
                scrapedplot = plot
                if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

                # AÒade al listado de XBMC
                xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )
        else:
            
            xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, matches[0] , thumbnail , plot )
            
    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces a video en el servidor Dailymotion                             #
    ## --------------------------------------------------------------------------------------##
    patronvideos = '<param name="movie" value="http://www.dailymotion.com/swf/video/([^\_]+)\_[^"]+"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    playWithSubt = "play"
    subtit = ""
    if len(matches)>0:
        daily = 'http://www.dailymotion.com/video/%s'%matches[0]
        data2 = scrapertools.cachePage(daily)
        
        # Busca los subtitulos en espaÒol 
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
    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces a video en el servidor Gigabyteupload.com                      #
    ## --------------------------------------------------------------------------------------##

    patronvideos = '<a href="(http://www.gigabyteupload.com/[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        print " encontro: %s" %matches[0]
        import gigabyteupload as giga
        videourl = giga.geturl(matches[0])
        if len(videourl)>0:
            subtitle = "[Divx-Directo-Gigabyteupload]"
            xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+subtitle, videourl , thumbnail , plot )
    ## --------------------------------------------------------------------------------------##
    #            Busca enlaces de videos para el servidor vk.com                             #
    ## --------------------------------------------------------------------------------------##
    '''
    var video_host = 'http://cs12644.vk.com/';
    var video_uid = '87155741';
    var video_vtag = 'fc697084d3';
    var video_no_flv = 1;
    var video_max_hd = '1'
    
    patronvideos = '<iframe src="(http:\/\/vk[^\/]+\/video_ext.php[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        print " encontro VKServer :%s" %matches[0]
        videourl =     vk.geturl(matches[0])
        xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+"[VKServer]", videourl , thumbnail , plot )
            
        data2 = scrapertools.cachePage(matches[0])
        print data2
        
        patron  = "var video_host = '([^']+)'.*?"
        patron += "var video_uid = '([^']+)'.*?"
        patron += "var video_vtag = '([^']+)'.*?"
        patron += "var video_no_flv = ([^;]+);.*?"
        patron += "var video_max_hd = '([^']+)'"
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        if len(matches2)>0:    #http://cs12387.vk.com/u87155741/video/fe5ee11ddb.360.mp4
            for match in matches2:
                if match[3].strip() == "0":
                    tipo = "flv"
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                    xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+"[VK] [%s]" %tipo, videourl , thumbnail , plot )
                else:
                    tipo = "360.mp4"
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                    xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+"[VK] [%s]" %tipo, videourl , thumbnail , plot )
                    tipo = "240.mp4"
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                    xbmctools.addnewvideo( __channel__ , "play" , category , "Directo" , title + " - "+"[VK] [%s]" %tipo, videourl , thumbnail , plot )
        '''    
    
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )



def play(params,url,category):
    logger.info("[newdivx.py] play")
    strmplay = False
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(__channel__,server,url,category,title,thumbnail,plot)

def play2(params,url,category):
    logger.info("[newdivx.py] play")
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

        title = title.replace("√Ç¬", "")
        title = title.replace("√É¬©","È")
        title = title.replace("√É¬°","·")
        title = title.replace("√É¬≥","Û")
        title = title.replace("√É¬∫","˙")
        title = title.replace("√É¬≠","Ì")
        title = title.replace("√É¬±","Ò")
        title = title.replace("√¢‚Ç¨¬ù", "")
        title = title.replace("√¢‚Ç¨≈ì√Ç¬", "")
        title = title.replace("√¢‚Ç¨≈ì","")
        title = title.replace("√©","È")
        title = title.replace("√°","·")
        title = title.replace("√≥","Û")
        title = title.replace("√∫","˙")
        title = title.replace("√≠","Ì")
        title = title.replace("√±","Ò")
        title = title.replace("√É‚Äú","”")
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
    ok = downloadtools.downloadfile(urlsub,fullpath)
    #xbmc.setSubtitles(fullpath)
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
def geturl(url):
    
    try:
        response = urllib.urlopen(url)
        trulink = response.geturl()
        return truelink
    except:
        return ""
