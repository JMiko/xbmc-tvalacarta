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
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , action="programas"  , thumbnail = "" , url="http://www.telefe.com/programas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Exclusivo web"       , action="videos"     , thumbnail = "" , url="http://www.telefe.com/exclusivo-web/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Vídeos"              , action="videos"     , thumbnail = "" , url="http://www.telefe.com/videos/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Episodios completos" , action="completos"  , thumbnail = "" , url="http://www.telefe.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Especiales"          , action="especiales" , thumbnail = "" , url="http://www.telefe.com/"))

    return itemlist

def programas(item):
    logger.info("[telefe.py] programas")
    
    itemlist = []
    data = scrapertools.cache_page(item.url)
    
    patron  = '<div class="foto_marco"[^<]+'
    patron += '<div class="foto">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"/></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail in matches:
        scrapedtitle = scrapertools.htmlclean(title)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def completos(item):
    logger.info("[telefe.py] completos")
    
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades", action="videos", url="http://www.telefe.com/episodios-completos/") )

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match( data , '<li[^<]+<a href="http\://www.telefe.com/episodios-completos/">Episodios completos</a>[^<]+<ul class="sub-menu">(.*?)</ul>')
    
    patron  = '<li[^<]+<a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title in matches:
        scrapedtitle = scrapertools.htmlclean(title)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=True) )

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
    '''
    <div class="entry-thumbnails">
    <a class="entry-thumbnails-link" href="http://www.telefe.com/2012/05/23/el-donante-capitulo-1/">
    <img width="155" height="144" src="http://www.telefe.com/wp-content/blogs.dir/10/files/2012/05/el-donante1-155x144.jpg" class="attachment-thumbnail-155 wp-post-image" alt="el donante" title="el donante" /></a></div><h3 class="entry-title"><a href="http://www.telefe.com/2012/05/23/el-donante-capitulo-1/" rel="bookmark">El Donante | Capítulo 1</a></h3>				<div class="entry-summary">
    <div class="entry-info">
    <abbr class="published" title="2012-05-23T14:17:27+00:00">Posteado el 23 mayo, 2012</abbr> | <span>22 comentarios</span>
    </div>
    Telefe presentó el primer episodio de “El Donante”, la ficción ganadora del concurso “Ficción para todos” propuesto por el INCAA en 2011, con el aporte del Ministerio de Planificación Federal inversión Pública y Servicios. El nuevo unitario de Telefe cuenta la historia de Bruno (Rafael...					<p class="quick-read-more"><a href="http://www.telefe.com/2012/05/23/el-donante-capitulo-1/" title="Permalink to El Donante | Capítulo 1"><img src="http://www.telefe.com/wp-content/themes/arras-theme-telefecom/images/bt_mas.png" /></a></p>
    </div>
    '''
    data = scrapertools.cache_page(item.url)
    logger.info("url="+item.url)
    logger.info("data="+data)
    
    patron  = '<div class="entry-thumbnails">'
    patron += '<a class="entry-thumbnails-link" href="([^"]+)">'
    patron += '<img width="\d+" height="\d+" src="([^"]+)".*?<h3 class="entry-title"><a href="[^"]+" rel="bookmark">(.*?)</a></h3>[^<]+<div class="entry-summary">[^<]+'
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
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="telefe", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    # Patron alternativo
    '''
    <div id="post-343" class="post-343 post type-post status-publish format-video hentry category-capitulos-completos row">
    <a href="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/" title="Enlace permanente a CAPITULO 10 HD (20-06-12)" rel="bookmark"><img width="135" height="76" src="http://laduena.telefe.com/wp-content/blogs.dir/27/files/2012/06/LA-DUENA-CAPITULO-10-HD-135x76.jpg" class="attachment-thumb-16:9-25% wp-post-image" alt="LA DUENA CAPITULO 10 HD" title="LA DUENA CAPITULO 10 HD" /></a></h2>
    <h2 class="entry-title"><a href="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/" title="Enlace permanente a CAPITULO 10 HD (20-06-12)" rel="bookmark">CAPITULO 10 HD (20-06-12)</a></h2>
    <div class="entry-meta">
    <a href="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/" title="14:05" rel="bookmark"><span class="entry-date">21 junio, 2012</span></a>			</div>
    <div class="entry-summary">
    <p>Sofía (Mirtha Legrand) le miente a Amparo (Florencia Bertotti) sobre su paradero del día anterior, le cuenta que estuvo reunida con empresarios, sin nombrar en ningún momento a Martín Braun (Jorge D´Elia). Mientras tanto, Juan (Raúl Taibo) revisando cámaras de <a href="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/" >Ver mas <span class="meta-nav">&rarr;</span></a></p>
    </div>
    <div class="entry-utility">
    <a href="https://twitter.com/share" class="twitter-share-button" data-url="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/" data-text="CAPITULO 10 HD (20-06-12)" data-via="telefecom" data-lang="es" data-related="telefecom" >Twittear</a>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
    <iframe src="//www.facebook.com/plugins/like.php?href=http%3A%2F%2Fladuena.telefe.com%2F2012%2F06%2F21%2Fcapitulo-10-hd-20-06-12%2F&amp;send=false&amp;layout=button_count&amp;width=120&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font&amp;height=21&amp;appId=165627566829126" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:120px; height:21px;" allowTransparency="true"></iframe>
    <span class="comments-link"><a href="http://laduena.telefe.com/2012/06/21/capitulo-10-hd-20-06-12/#comments" rel="nofollow" title="Comentarios en CAPITULO 10 HD (20-06-12)">3 comentarios</a></span>
    </div>
    </div>
    '''
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<a href="([^"]+)" title="[^"]+" rel="bookmark"><img width="\d+" height="\d+" src="([^"]+)"[^<]+</a></h2>[^<]+'
    patron += '<h2 class="entry-title"><a[^<]+>([^<]+)</a></h2>[^<]+'
    patron += '<div class="entry-meta">[^<]+'
    patron += '<a[^<]+<span[^<]+</span></a>[^<]+</div>[^<]+'
    patron += '<div class="entry-summary">(.*?)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,thumbnail,title,plot in matches:
        scrapedtitle = title
        scrapedplot = scrapertools.htmlclean(plot)
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="telefe", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )

    '''
    <div id="post-3802" class="post-3802 post type-post status-publish format-video hentry category-capitulos-completos">
    <h2 class="entry-title"><a href="http://dulceamor.telefe.com/2012/07/16/capitulo-121-hd/" title="Enlace permanente a Capítulo 121 (HD)" rel="bookmark">Capítulo 121 (HD)</a></h2>
    
    <img width="150" height="111" src="http://dulceamor.telefe.com/wp-content/blogs.dir/23/files/2012/07/121-HD-Capitulo-dulce-amor-150x111.jpg" class="attachment-loop-thumb wp-post-image" alt="121 HD Capitulo dulce amor" title="121 HD Capitulo dulce amor" />
    <div class="entry-summary">
    <p>VIDEO SÓLO VISIBLE EN ARGENTINA. Para visualizarlo recomendamos tener la última versión de Flash Player. Para bajarlo hacé click aquí Aire 13-7-12</p>
    </div><!-- .entry-summary -->
    
    <div class="entry-utility">
    Publicado el <a href="http://dulceamor.telefe.com/2012/07/16/capitulo-121-hd/" title="15:21" rel="bookmark"><span class="entry-date">16 julio, 2012</span></a>									<span class="cat-links">
    en <a href="http://dulceamor.telefe.com/capitulos-completos/" title="Ver todas las entradas en Capítulos Completos HD" rel="category tag">Capítulos Completos HD</a>					</span>
    
    <span class="meta-sep">|</span>
    <span class="comments-link"><a href="http://dulceamor.telefe.com/2012/07/16/capitulo-121-hd/#comments" rel="nofollow" title="Comentarios en Capítulo 121 (HD)">128 comentarios</a></span>
    </div><!-- .entry-utility -->
    </div><!-- #post-## -->
    '''
    patron  = '<div id="post-\d+"[^<]+'
    patron += '<h2 class="entry-title"><a href="([^"]+)" title="[^"]+" rel="bookmark">([^<]+)</a></h2>[^<]+'
    patron += '<img width="\d+" height="\d+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail in matches:
        scrapedtitle = title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="telefe", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=False) )


    # Si aún así no hay vídeos...
    # Cambia: http://www.telefe.com/programas/am/
    # Por: http://www.telefe.com/am/
    if len(itemlist)==0 and "programas" in item.url:
        item.url = item.url.replace("/programas/","/")
        itemlist = videos(item)

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
