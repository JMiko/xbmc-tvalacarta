# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para la sexta
#------------------------------------------------------------
import urlparse,re

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "lasexta"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[sexta.py] mainlist")

    # Descarga la pagina
    url = "http://www.lasexta.com/sextatv"
    data = scrapertools.cachePage(url)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title='F1' , action="getF1Videos" , url='', thumbnail='http://www.lasexta.com/media/sextatv/img/player_f1.jpg', plot='' , show='' , folder=True) )
    salir = False
    pagina = 0
    while not salir:
        pageitems = getprogramaspagina("http://www.lasexta.com/sextatv/reload_programs","item_id=1&show_id=1&bd_id=1&pagina=%d&limit=3" % pagina)
        itemlist.extend( pageitems )
        pagina = pagina + 15
        salir = len(pageitems)<15
    
    return itemlist

def getprogramaspagina(url,post):
    logger.info("[sexta.py] getprogramaspagina post="+post)
    
    headers = [
            ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],
            ['X-Requested-With','XMLHttpRequest'],
            ['X-Prototype-Version','1.6.0.3'],
            ['Referer','http://www.lasexta.com/sextatv']
            ]
    
    # Esta peticion no se puede cachear
    data = scrapertools.cachePage(url,post,headers)
    #logger.info(data)

    # Extrae las entradas
    '''
    <div class="capaseccionl item_vip">
    <div class="player">
    <a href="http://www.lasexta.com/sextatv/seloquehicisteis">
    <img src="http://www.lasexta.com/media/sextatv/img/sextatv_logo_slqh.jpg" width="230" height="129" title="Vídeos de Sé lo que Hicísteis" alt="logotipo de Sé lo que hicísteis" />
    <label class="item_vip_player_label">Sé lo que Hicísteis</label>
    <img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" class="item_vip_player_link" alt="Ir a videos de Sé lo que Hicísteis"/>
    </a>
    </div>
    '''
    patron  = '<div class="capaseccionl item_vip">[^<]+'
    patron += '<div class="player">[^<]+'
    patron += '<a href="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^>]+>[^<]+'
    patron += '<label class="item_vip_player_label">([^<]+)</label>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        scrapedshow = scrapedtitle
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="secciones" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedshow , folder=True) )

    return itemlist

def secciones(item):
    logger.info("[sexta.py] secciones")
    
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Ahora extrae las pestañas
    patron  = '<li class="lsv_pestanas_li"><a id="[^"]+" href="javascript.change_videos.\'([^\']+)\',\'([^\']+)\'.."[^>]+><b class="left"></b>([^<]+)<b class="right"></b></a></li>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for match in matches:
        scrapedurl = "http://www.lasexta.com/sextatv/change_videos/"+match[0]+"/"+match[1]
        scrapedtitle = match[2]
        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, show=item.show , folder=True) )

    return itemlist

def videos(item):
    logger.info("[sexta.py] videos")
    
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    itemlist = parsevideos(item,data)

    # Paginacion
    # El id es 11_ultimos_15
    # La pagina es un POST a http://www.lasexta.com/sextatv/reload con "seccion=11&pagina=15&tipo=ultimos&section_id"
    while True:
        patron = '<a href="javascript.reload.\'([^\']+)\'.;" class="siguiente" title="P&aacute;gina siguiente">P&aacute;gina siguiente</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        if len(matches)>0:
            partes = matches[0].split("_")
            url = "http://www.lasexta.com/sextatv/reload"
            post = "seccion=%s&pagina=%s&tipo=%s&section_id" % (partes[0],partes[2],partes[1])
            data = scrapertools.cachePage(url,post)
            newitems = parsevideos(item,data)
            itemlist.extend(newitems)
        else:
            break

    # Caso especial "Ver todos los videos"
    patron = '<a href="javascript.reload.\'([^\']+)\'.;">Ver todos'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return itemlist
    
    partes = matches[0].split("_")
    url = "http://www.lasexta.com/sextatv/reload"
    post = "seccion=%s&pagina=%s&tipo=%s&section_id=%s" % (partes[0],partes[2],partes[1],partes[3])
    data = scrapertools.cachePage(url,post)
    
    # Paginacion
    # El id es 11_ultimos_15_1234
    # La pagina es un POST a http://www.lasexta.com/sextatv/reload con "seccion=11&pagina=15&tipo=ultimos&section_id=1234"
    while True:
        patron = '<a href="javascript.reload.\'([^\']+)\'.;" class="siguiente" title="P&aacute;gina siguiente">P&aacute;gina siguiente</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        if len(matches)>0:
            partes = matches[0].split("_")
            url = "http://www.lasexta.com/sextatv/reload"
            post = "seccion=%s&pagina=%s&tipo=%s&section_id=%s" % (partes[0],partes[2],partes[1],partes[3])
            data = scrapertools.cachePage(url,post)
            newitems = parsevideos(item,data)
            itemlist.extend(newitems)
        else:
            break


    return itemlist

def parsevideos(item,data):
    logger.info("[sexta.py] parsevideos")
    #print data
    
    # Extrae los videos
    '''
    <div class="capaseccionl item">
    <div class="player_programas">
    <a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1"><img src="http://www.sitios.lasexta.com/pictures/215481/pictures_20101020_1601215481_crop1.jpg" width="170" height="127" title="quien_vive_ahi___jueves__21_de_octubre" alt="quien_vive_ahi___jueves__21_de_octubre" /></a>
    <a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1" class="item_cortina">
    <img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" width="170" height="127" title="quien_vive_ahi___jueves__21_de_octubre" alt="quien_vive_ahi___jueves__21_de_octubre" />
    <label class="item_cortina_text">El programa visit del campo o un&#8230;</label>
    <label class="item_cortina_play">PLAY</label>
    </a>
    </div>
    <h6 class="fecha">22/10/2010 </h6>
    <h5 class="titulo"><a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1" title="quien_vive_ahi___jueves__21_de_octubre">aaaaaJueves, 21 de octubre</a></h5>
    </div>
    '''
    patron  = '<div class="capaseccionl item">[^<]+'
    patron += '<div class="player_programas">[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^>]+></a>.*?'
    patron += '<label class="item_cortina_text">([^<]*)</label>.*?'
    patron += '<h6 class="fecha">([^<]+)</h6>[^<]+'
    patron += '<h5 class="titulo"><a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[4]+" "+match[3]
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[2] 
        scrapedpage = scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getVideos" , url=scrapedurl, page=scrapedpage, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )
    
    return itemlist

def getVideos(item):
    logger.info("[lasexta.py] getVideos")
    
    import urllib2
    
    urlGeneral = item.url
    logger.info("url1="+urlGeneral)
  
    #http://www.lasexta.com/sextatv/seloquehicisteis/completos/se_lo_que_hicisteis____viernes__4_de_febrero/366561/1
    patron = 'http://www.lasexta.com/sextatv/.+?/.+?/.+?/(.+?)/1'
    matchedIds = re.compile(patron,re.DOTALL).findall(urlGeneral)
    itemlist = []
    count = 0
    for matchId in matchedIds:
        videoId = matchId
        videosUrl = 'http://www.lasexta.com/sextatv/playlist/' + videoId
        logger.info("url2="+videosUrl)
        req = urllib2.Request(videosUrl)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        page = response.read()
        response.close()

        ##            <video>
        ##                <id>357881</id>
        ##                <title>1 FLV 23 enero</title>
        ##                <description><![CDATA[]]></description>
        ##                <url>6a77ec0772d81456186cf91ab66e3384c993462e934320aa89a44a5b7eb636bde26211e0e96a9709b1809864c83da59ee90669280e2999643efca0377eb7eaf60807ad12a89a209d5e9a9b82535db4f8ca95a04e02989ca9547fee742735dda33c5bfad3583e7f629c6db861828e503f87b308</url>
        ##                <urlHD>http://lasexta.edgeboss.net/flash/lasexta/supercasas/hd/ppd0001564000601_supercasas_6_23_01_2011_23_19_57_h264.mp4</urlHD>
        ##            </video>
        
        patron = '<urlHD>(.+?)</urlHD>[^<]'
        matchedVideoParts = re.compile(patron,re.DOTALL).findall(page)
        
        for matchVideoPart in matchedVideoParts:
            count = count + 1
            scrapedtitle = "Part " + str(count)
            scrapedVideoUrl = matchVideoPart
           
            scrapedthumbnail = item.thumbnail
            scrapedplot = ''

            logger.info("url3="+scrapedVideoUrl)

            if (scrapedVideoUrl.startswith("rtmp")):
                scrapedVideoUrl = scrapedVideoUrl.replace("mp4:", " playpath=mp4:")
                scrapedVideoUrl = scrapedVideoUrl + " swfvfy=true swfurl=http://www.lasexta.com/media/swf/reproductor_sextatv/player_overlay.swf"

                itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=scrapedVideoUrl, thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )
            else:
    
                req = urllib2.Request(scrapedVideoUrl)
                req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                page = response.read()
                
                response.close()
                ##            <FLVPlayerConfig>
                ##  <serverName>cp61776.edgefcs.net</serverName>
                ##  <fallbackServerName>cp61776.edgefcs.net</fallbackServerName>
                ##  <appName>ondemand</appName>
                ##  <streamName>mp4:flash/supercasas/hd/.uid.MVHxAABEEE97k1ZrBw7c64b8c2bb7e83b937ce470f33f64c08.ppd0001564000601_supercasas_6_23_01_2011_23_19_57_h264.mp4</streamName>
                ##  <isLive>false</isLive>
                ##  <bufferTime>2</bufferTime>
                ##</FLVPlayerConfig>

                patron = '<serverName>([^<]+)</serverName>[^<]+'
                patron += '<fallbackServerName>([^<]+)</fallbackServerName>[^<]+'
                patron += '<appName><!\[CDATA\[(.+?)]]></appName>[^<]+'
                patron +='<streamName><!\[CDATA\[(.+?)]]></streamName>[^<]'
                matches = re.compile(patron,re.DOTALL).findall(page)
                for match in matches:
                    serverName = match[0]
                    appName = match[2]
                    streamName = match[3]
                    scrapedUrl = 'rtmp://' + serverName + '/' + appName + '/' + streamName
                    logger.info("scrapedurl="+scrapedUrl)
                    # Añade al listado
                    itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=scrapedUrl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    return itemlist

def getF1Videos(item):
    logger.info("[sexta.py] getF1Videos")
    itemlist = []
    url_f1page = "http://www.lasextadeportes.com/formula1/tv/diferido/carrera"
    url_f1feed = "http://www.lasextadeportes.com/feeds/playlist/"
    data = scrapertools.cachePage(url_f1page)
    if data.find("_id_list=") != -1:
    id = data.split("_id_list=")[1].split("&")[0]
    data = scrapertools.cachePage(url_f1feed + id)
    vid_thumb = data.split("<picture>")[1].split("<")[0]
    vid_entries  = data.split("<video>")[1:]
    for vid_entry in vid_entries:
        vid_url = vid_entry.split("<url>")[1].split("<")[0]
        ext = "." + vid_url.split(".")[-1]
        if vid_url.find("/mp4:") != -1: vid_url = vid_url.replace("/mp4:", "/")
        if vid_url.find("/flv:") != -1: vid_url = vid_url.replace("/flv:", "/")
        vid_title = vid_entry.split("<title>")[1].split("<")[0].capitalize() + ext
        logger.info("[lasexta.py] Adding title=["+vid_title+"], url=["+vid_url+"], thumbnail=["+vid_thumb+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=vid_title , action="play", server="Directo" , url=vid_url, thumbnail=vid_thumb, plot='' , folder=False) )
    else:
    logger.info("[lasexta.py] No feed id found")
    return itemlist