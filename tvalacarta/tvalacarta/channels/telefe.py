# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Telefe
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "telefe"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[telefe.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Vídeos"              , action="videos" , thumbnail = "" , url="http://www.telefe.com/videos/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Episodios completos" , action="completos" , thumbnail = "" , url="http://www.telefe.com/episodios-completos/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Exclusivo web"       , action="videos" , thumbnail = "" , url="http://www.telefe.com/exclusivo-web/"))

    return itemlist

def completos(item):
    logger.info("[telefe.py] completos")
    
    # Lo parsea como vídeos pero lo enlaza con el action "episodios"
    itemlist = videos(item)
    for item in itemlist:
        if item.action=="play":
            item.folder=True
            item.action="episodios"
            item.server=""
        else:
            item.action="completos"

    for item in itemlist:
        print item.action,item.folder,item.server

    return itemlist

def episodios(item):
    logger.info("[telefe.py] episodios")

    itemlist = play(item)
    
    if len(itemlist)>0:
        return itemlist
    
    data = scrapertools.cachePage(item.url)
    '''
    <h2 class="entry-title"><a href="http://unanopararecordar.telefe.com/2011/08/15/cap-90-la-carta/" title="Enlace permanente a Cap.90: La carta" rel="bookmark"><i>Cap.90</i>: La carta</a></h2>
    <img width="150" height="111" src="http://unanopararecordar.telefe.com/files/2011/07/cap-90-150x111.jpg" class="attachment-loop-thumb wp-post-image" alt="cap 90" title="cap 90" />
    <div class="entry-summary">
    <p>Ana  viaja al pasado. Escondida, observa a la madre de Mariano  escribir una carta y luego tirarse por la ventana.</p>
    </div><!-- .entry-summary -->
    '''
    patron  = '<h2 class="entry-title"><a href="([^"]+)"[^>]+>(.*?)</a></h2>[^<]+'
    patron += '<img width="[^"]+" height="[^"]+" src="([^"]+)".*?'
    patron += '<div class="entry-summary">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("<i>","")
        scrapedtitle = scrapedtitle.replace("</i>","")
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[3].strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    # Patron alternativo
    '''
    <h2 class="entry-title"><a href="http://elelegido.telefe.com/2011/10/26/capitulo-152-26-10-11/" title="Enlace permanente a Capítulo 152 (26-10-11)" rel="bookmark">Capítulo 152 (26-10-11)</a></h2>
    <div class="entry-meta">
    <span class="meta-prep meta-prep-author">Posted on</span> <a href="http://elelegido.telefe.com/2011/10/26/capitulo-152-26-10-11/" title="9:00" rel="bookmark"><span class="entry-date">26 octubre, 2011</span></a>			</div><!-- .entry-meta -->
    <div class="entry-content">
    <p>Roberto (Jorge Suárez) enfrenta a Andrés (Pablo Echarri) y Santiago (Martín Seefeld) por las escrituras. Llega la policía: Roberto queda detenido. El inspector le da 48 horas a Andrés para encontrar a Oscar (Lito Cruz).<br />
    Andrés y Santiago (Martín Seefeld) le revelan a Mariana (Paola Krum) la trampa que tienen para hacer caer a Nevares Sosa.</p>
    <p class="FacebookLikeButton"><iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Felelegido.telefe.com%2F2011%2F10%2F26%2Fcapitulo-152-26-10-11%2F&amp;layout=standard&amp;show_faces=yes&amp;width=450&amp;action=like&amp;colorscheme=light&amp;locale=es_ES" scrolling="no" frameborder="0" allowTransparency="true" style="border:none; overflow:hidden; width:450px; height: 25px"></iframe></p>
    </div><!-- .entry-content -->
    '''
    patron  = '<h2 class="entry-title"><a href="([^"]+)"[^>]+>(.*?)</a></h2>.*?'
    patron += '<div class="entry-content">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("<i>","")
        scrapedtitle = scrapedtitle.replace("</i>","")
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = match[2].strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    patron = '<a href="([^"]+)" class="nextpostslink"><span class="meta-nav">\&larr\;</span> Entradas m'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl = matches[0]
        scrapedtitle = "!Página siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot) )

    return itemlist

def videos(item):
    logger.info("[telefe.py] videos")
    
    itemlist=[]

    # Extrae los programas
    '''
    <div class="entry-thumbnails"><a class="entry-thumbnails-link" href="http://www.telefe.com/2011/10/27/justo-a-tiempo-kinesiologia-a-domicilio/"><img width="155" height="155" src="http://www.telefe.com/files/2011/10/UAAB5142-442-155x155.jpg" class="attachment-thumbnail-155 wp-post-image" alt="Justo a Tiempo" title="Justo a Tiempo" /></a></div><h3 class="entry-title"><a href="http://www.telefe.com/2011/10/27/justo-a-tiempo-kinesiologia-a-domicilio/" rel="bookmark"><i>Justo a Tiempo</i>: Kinesiología a domicilio</a></h3>				<div class="entry-summary">
    <div class="entry-info">    
    <abbr class="published" title="2011-10-27T11:50:45+00:00">Posteado el 27 octubre, 2011</abbr> | <span><span class='IDCommentsReplace' style='display:none'>20484</span>No hay comentarios<span style='display:none' id='IDCommentPostInfoPermalink20484'>http%3A%2F%2Fwww.telefe.com%2F2011%2F10%2F27%2Fjusto-a-tiempo-kinesiologia-a-domicilio%2F</span><span style='display:none' id='IDCommentPostInfoTitle20484'>%3Ci%3EJusto+a+Tiempo%3C%2Fi%3E%3A+Kinesiolog%C3%ADa+a+domicilio</span><span style='display:none' id='IDCommentPostInfoTime20484'>2011-10-27+14%3A50%3A45</span><span style='display:none' id='IDCommentPostInfoAuthor20484'>maria</span><span style='display:none' id='IDCommentPostInfoGuid20484'>http%3A%2F%2Fwww.telefe.com%2F%3Fp%3D20484</span></span>
    </div>
    Los hermanos y la abuela Olga se preparaban para jugar pero antes, Olga pudo tener sesión de kinesiología por teléfono. Comprobá si la ayudó o no.					<p class="quick-read-more"><a href="http://www.telefe.com/2011/10/27/justo-a-tiempo-kinesiologia-a-domicilio/" title="Permalink to <i>Justo a Tiempo</i>: Kinesiología a domicilio"><img src="http://www.telefe.com/wp-content/themes/arras-theme-telefecom/images/bt_mas.png" /></a></p>
    </div>	
    '''
    data = scrapertools.cache_page(item.url)
    logger.info("url="+item.url)
    logger.info("data="+data)
    patron  = '<div class="entry-thumbnails"><a class="entry-thumbnails-link" href="([^"]+)"><img width="155" height="155" src="([^"]+)".*?<h3 class="entry-title"><a href="[^"]+" rel="bookmark">(.*?)</a></h3>[^<]+<div class="entry-summary">[^<]+'
    patron += '<div class="entry-info">[^<]+'
    patron += '<abbr class="published"[^>]+>Posteado el ([^<]+)</abbr>.*?'
    patron += '</div>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[2].strip()+" ("+match[3]+")"
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapedtitle.replace("<i>","")
        scrapedtitle = scrapedtitle.replace("</i>","")
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[4].strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    patron = '<a href="([^"]+)" >\&laquo\; Anterior</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl = matches[0]
        scrapedtitle = "!Página siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot) )

    return itemlist

def play( item ):
    logger.info("[telefe.py] play")
    itemlist = []

    if item.url.startswith("rtmp"):
        itemlist.append( item )
    else:
        page_url=item.url
        data = scrapertools.cache_page(page_url)
        
        video_urls = []
        
        # Descarga el descriptor del vídeo
        # El vídeo:
        # <script type="text/javascript" src="http://flash.velocix.com/c1197/legacy/UAAA1582_X264_480x360.mp4?format=jscript2&protocol=rtmpe&vxttoken=00004EAA82A8000000000289A60672657573653D32EBF4321F280103EC9B2025F74095B4E74A0E459A" ></script>
        # El anuncio:
        # <script type="text/javascript" src="http://flash.velocix.com/bt/145e8eae1563f092fbdf905113f7c213ebefd8e6/flash?format=jscript2&protocol=rtmpte&vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB" ></script>
        patron  = '<script type="text/javascript" src="(http://flash.velocix.com/[^"]+)" ></script>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        print matches
        
        if len(matches)>0:
            page_url2 = matches[0]
            data2 = scrapertools.cache_page(page_url2)
            print("data2="+data2)
            '''
            var streamName = "mp4:bt-145e8eae1563f092fbdf905113f7c213ebefd8e6";
            var rtmpUrl = [];
            rtmpUrl.push("rtmpte://201.251.164.11/flash?vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB");
            rtmpUrl.push("rtmpte://201.251.118.11/flash?vxttoken=00004EAA693D0000000002897CEF72657573653D320830AA52351D57C26FFD6E55F9183C6342438DEB");
            '''
            patron = 'streamName \= "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data2)
            streamName = matches[0]
        
            patron = 'rtmpUrl\.push\("([^"]+)"\)'
            matches = re.compile(patron,re.DOTALL).findall(data2)
            if len(matches)>0:
                videourl = matches[0]+"/"+streamName
            
                logger.info(videourl)
                itemlist.append( Item(channel=CHANNELNAME, title=item.title, action="play" , server="directo", url=videourl, thumbnail=item.thumbnail, plot=item.plot, folder=False) )

    return itemlist
