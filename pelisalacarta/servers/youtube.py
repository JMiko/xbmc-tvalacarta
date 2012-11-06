# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,httplib
from core import config
from core import logger
from core import scrapertools
from core.item import Item

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[youtube.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    #page_url = "http://www.youtube.com/get_video_info?&video_id=zlZgGlwBgro"
    if not page_url.startswith("http"):
        page_url = "http://www.youtube.com/watch?v=%s" % page_url
        
    # Descarga
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']] , )
    #logger.info("-------------------------------------------------------------------------------------------")
    #logger.info(data)
    #logger.info("-------------------------------------------------------------------------------------------")

    options = data.split("&")
    logger.info("-------------------------------------------------------------------------------------------")
    for option in options:
        logger.info(option)
    logger.info("-------------------------------------------------------------------------------------------")
    
    patron = 'fmt_list=([^\&]+)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return
    fmt_list = urllib.unquote(matches[0])
    logger.info(fmt_list)
    fmt_list_array = fmt_list.split(",")

    patron = 'fmt_stream_map=([^\&]+)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return
    fmt_stream_map = urllib.unquote(matches[0])
    logger.info(fmt_stream_map)
    fmt_stream_map_array = fmt_stream_map.split(",")

    logger.info("-------------------------------------------------------------------------------------------")
    logger.info("len(fmt_list_array)=%d" % len(fmt_list_array))
    logger.info("len(fmt_stream_map_array)=%d" % len(fmt_stream_map_array))

    CALIDADES = {'5':'240p','34':'360p','18':'360p','35':'480p','22':'720p','84':'720p','37':'1080p','38':'3072p','17':'144p','43':'360p','44':'480p','45':'720p'}

    for i in range(len(fmt_list_array)):
        try:
            video_url = urllib.unquote(fmt_stream_map_array[i])
            video_url = urllib.unquote(video_url[4:])
            video_url = video_url.split(";")[0]
            logger.info(" [%s] - %s" % (fmt_list_array[i],video_url))
            
            calidad = fmt_list_array[i].split("/")[0]
            video_url = video_url.replace("flv&itag="+calidad,"flv")
            video_url = video_url.replace("="+calidad+"&url=","")
            video_url = video_url.replace("sig=","signature=")
            video_url = re.sub("^=http","http",video_url)

            resolucion = fmt_list_array[i].split("/")[1]
    
            formato = ""
            patron = '&type\=video/([a-z0-9\-]+)'
            matches = re.compile(patron,re.DOTALL).findall(video_url)
            if len(matches)>0:
                formato = matches[0]
                if formato.startswith("x-"):
                    formato = formato[2:]
                formato = formato.upper()
    
            etiqueta = ""
            try:
                etiqueta = CALIDADES[calidad]
                if formato!="":
                    etiqueta = etiqueta + " (%s a %s) [youtube]" % (formato,resolucion)
                else:
                    etiqueta = etiqueta + " (%s) [youtube]" % (resolucion)
        
                video_urls.append( [ etiqueta , video_url ])
            except:
                pass
            
        except:
            pass
    
    video_urls.reverse()
    
    for video_url in video_urls:
        logger.info(str(video_url))
    
    return video_urls

def getuploads(user,startindex,maxresults,channel="",action="play"):
    logger.info("[youtube.py] getuploads")

    import gdata.youtube
    import gdata.youtube.service

    # Obtiene el feed según el API de YouTube
    url = "http://gdata.youtube.com/feeds/api/users/%s/uploads?orderby=updated&start-index=%d&max-results=%d" % (user,startindex,maxresults)
    logger.info("[youtube.py] url="+url)
    yt_service = gdata.youtube.service.YouTubeService()
    feed = yt_service.GetYouTubeVideoFeed(url)
    
    itemlist = []
    for entry in feed.entry:
        '''
        print 'Video title: %s' % entry.media.title.text
        print 'Video published on: %s ' % entry.published.text
        print 'Video description: %s' % entry.media.description.text
        print 'Video category: %s' % entry.media.category[0].text
        print 'Video tags: %s' % entry.media.keywords.text
        print 'Video watch page: %s' % entry.media.player.url
        print 'Video flash player URL: %s' % entry.GetSwfUrl()
        print 'Video duration: %s' % entry.media.duration.seconds
        
        # non entry.media attributes
        #print 'Video geo location: %s' % entry.geo.location()
        #print 'Video view count: %s' % entry.statistics.view_count
        #print 'Video rating: %s' % entry.rating.average
        
        # show alternate formats
        #for alternate_format in entry.media.content:
        #    if 'isDefault' not in alternate_format.extension_attributes:
        #        print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)
        
        # show thumbnails
        for thumbnail in entry.media.thumbnail:
            print 'Thumbnail url: %s' % thumbnail.url
        '''
        
        item = Item(channel=channel, action=action, title=entry.title.text, url=entry.media.player.url, thumbnail = entry.media.thumbnail[len(entry.media.thumbnail)-1].url , plot = entry.media.description.text )
        itemlist.append( item )
    
    return itemlist

def getplaylists(user,startindex,maxresults,channel="",action="playlist"):
    logger.info("[youtube.py] getplaylists")
    import gdata.youtube
    import gdata.youtube.service

    # Obtiene el feed segun el API de YouTube
    url = "http://gdata.youtube.com/feeds/api/users/%s/playlists?start-index=%d&max-results=%d" % (user,startindex,maxresults)
    logger.info("[youtube.py] url="+url)
    yt_service = gdata.youtube.service.YouTubeService()
    playlist_feed = yt_service.GetYouTubePlaylistFeed(uri=url)

    itemlist = []
    for entry in playlist_feed.entry:
        item = Item(channel=channel, action=action, title=entry.title.text, url=entry.id.text, thumbnail = "" , plot = "" )
        itemlist.append( item )

    return itemlist

def getplaylistvideos(url,startindex,maxresults,channel="",action="play"):
    logger.info("[youtube.py] getplaylistvideos")
    import gdata.youtube
    import gdata.youtube.service

    # Extrae el ID de la playlist
    patron = 'http://.*?/([^/]+)/$'
    matches = re.compile(patron,re.DOTALL).findall(url+"/")
    idplaylist = matches[0]
    logger.info(idplaylist)
    
    # Obtiene el feed segun el API de YouTube
    url = "http://gdata.youtube.com/feeds/api/playlists/%s?start-index=%d&max-results=%d" % (idplaylist,startindex,maxresults)
    logger.info("[youtube.py] url="+url)
    yt_service = gdata.youtube.service.YouTubeService()
    playlist_video_feed = yt_service.GetYouTubePlaylistVideoFeed(uri=url)

    itemlist = []
    for entry in playlist_video_feed.entry:
        item = Item(channel=channel, action=action, title=entry.title.text, url=entry.media.player.url, thumbnail = entry.media.thumbnail[len(entry.media.thumbnail)-1].url , plot = entry.media.description.text )
        itemlist.append( item )
    
    return itemlist

def GetYoutubeVideoInfo(videoID,eurl=None):
    '''
    Return direct URL to video and dictionary containing additional info
    >> url,info = GetYoutubeVideoInfo("tmFbteHdiSw")
    >>
    '''
    
    if not eurl:
        params = urllib.urlencode({'video_id':videoID})
    else :
        params = urllib.urlencode({'video_id':videoID, 'eurl':eurl})
    try:
        conn = httplib.HTTPConnection("www.youtube.com")
        conn.request("GET","/get_video_info?&%s"%params)
        response = conn.getresponse()
        data = response.read()
    except:
        alertaNone()
        return ""
    video_info = dict((k,urllib.unquote_plus(v)) for k,v in
                               (nvp.split('=') for nvp in data.split('&')))
    
    conn.request('GET','/get_video?video_id=%s&t=%s&fmt=18' %
                         ( video_info['video_id'],video_info['token']))
    response = conn.getresponse()
    direct_url = response.getheader('location')
    return direct_url,video_info
    
def Extract_id(url):
    # Extract video id from URL
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        logger.info('ERROR: URL invalida: %s' % url)
        alertaIDerror(url)
        return ""
    id = mobj.group(2)
    return id

def verify_url( url ):
    # Extract real URL to video
    request = urllib2.Request(url, None, std_headers)
    data = urllib2.urlopen(request)
    data.read(1)
    url = data.geturl()
    data.close()
    return url
        

def alertaCalidad():
    import xbmcgui
    ventana = xbmcgui.Dialog()
    ok= ventana.ok ("Conector de Youtube", "La calidad elegida en configuracion",'no esta disponible o es muy baja',"elija otra calidad distinta y vuelva a probar")
    
def alertaNone():
    import xbmcgui
    ventana = xbmcgui.Dialog()
    ok= ventana.ok ("Conector de Youtube", "!Aviso¡","El video no se encuentra disponible",'es posible que haya sido removido')
    
def alertaIDerror(url):
    import xbmcgui
    ventana = xbmcgui.Dialog()
    ok= ventana.ok ("Conector de Youtube", "Lo sentimos, no se pudo extraer la ID de la URL"," %s" %url,'la URL es invalida ')

def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = 'youtube(?:-nocookie)?\.com/(?:(?:(?:v/|embed/))|(?:(?:watch(?:_popup)?(?:\.php)?)?(?:\?|#!?)(?:.+&)?v=))?([0-9A-Za-z_-]{11})'#'"http://www.youtube.com/v/([^"]+)"'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match
        
        if url!='':
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'youtube' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)
    
    patronvideos  = 'www.youtube.*?v(?:=|%3D)([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.youtube.com/v/AcbsMOMg2fQ
    patronvideos  = 'youtube.com/v/([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve