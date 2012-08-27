# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para unsoloclic
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "unsoloclic"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Unsoloclic.info"
__language__ = "ES"
__creationdate__ = "20120703"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[unsoloclic.py] mainlist")
    item.url="http://unsoloclic.info";
    return novedades(item)

def novedades(item):
    logger.info("[unsoloclic.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="post-36592 post type-post status-publish format-standard hentry category-2012 category-blu-ray category-ciencia-ficcion category-estados-unidos category-hd-720p category-mkv-hd720p category-terror tag-2012 tag-ciencia-ficcion tag-estados-unidos tag-terror" id="post-36592">
    <h2 class="title"><a href="http://unsoloclic.info/2012/07/alien-origin-2012-hd720p/" rel="bookmark" title="Permanent Link to Alien Origin  (2012) HD720p">Alien Origin  (2012) HD720p</a></h2>
    <div class="postdate"><img src="http://unsoloclic.info/wp-content/themes/TinyWeb/images/date.png" /> July 2nd, 2012 <img src="http://unsoloclic.info/wp-content/themes/TinyWeb/images/user.png" /> sergoka </div>
    <div class="entry">
    <p><a href="http://unsoloclic.info/wp-content/uploads/2012/07/Alien-Origin-2012.jpg" ><img class="aligncenter size-full wp-image-36585" title="Alien Origin  (2012)" src="http://unsoloclic.info/wp-content/uploads/2012/07/Alien-Origin-2012.jpg" alt="" width="500" height="676" /></a><br />
    <div id="youtube_gallery_3" class="youtube_gallery"><div class="youtube_gallery_divider"></div><br />
    <div id="youtube_gallery_item_3" class="youtube_gallery_item">
    <a class="fancybox iframe" href="http://www.youtube.com/embed/ATC_lx-te3s?autoplay=1&hd=1" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.youtube.com']);" title="Trailer"><img src="http://unsoloclic.info/wp-content/plugins/youtube-simplegallery/ytsg_play.png" alt=" " class="ytsg_play" border="0" /><img src="http://img.youtube.com/vi/ATC_lx-te3s/0.jpg" border="0"></a><br /><div class="youtube_gallery_caption">Trailer</div></div>
    <br clear="all" style="clear: both;" /><div class="youtube_gallery_divider"></div><br clear="all" /></div></p>
    <p><a href="http://unsoloclic.info/wp-content/uploads/2012/05/720p-Hd6.jpg" ><img class="aligncenter size-full wp-image-34978" title="720p Hd" src="http://unsoloclic.info/wp-content/uploads/2012/05/720p-Hd6.jpg" alt="" width="167" height="100" /></a></p>
    <p style="text-align: center;"><strong><span style="color: blue;">TÍTULO ORIGINAL</span></strong> : Alien Origin<br />
    <strong><span style="color: blue;">DURACIÓN:</span></strong> 90 min.<br />
    <strong><span style="color: blue;">PAÍS :</span></strong> Estados Unidos<br />
    <strong><span style="color: blue;">DIRECTOR:</span></strong> Mark Atkins<br />
    <strong><span style="color: blue;">FORMATO:</span></strong><strong></strong><strong>MKV HD720p</strong><br />
    <strong><span style="color: blue;">CALIDAD:</span> </strong><strong></strong><strong>BLU-RAY</strong><br />
    <strong><span style="color: blue;">IDIOMA:</span> </strong><strong>Ingles</strong><br />
    <strong><span style="color: blue;">SUBTITULOS:</span> </strong><strong>Si</strong><strong></strong><br style="color: blue;" /> <strong><span style="color: blue;">TAMAÑO DEL ARCHIVO:</span></strong> 599 MB</p>
    <p style="text-align: center;"><strong><span style="color: blue;">REPARTO :</span></strong></p>
    <p style="text-align: center;">Philip Coc, Daniela Flynn, Andres Rash, Kent Noralez, Rupert Tablada, Saul Pech, Jon Frear, Dennis Johnson, Eric Darins, Alan UsheTrey McCurley, Peter Pedrero, Chelsea Vincent.</p>
    <p style="text-align: center;"><strong><span style="color: blue;">Ciencia ficción. Terror | Extraterrestres. Falso documental</span></strong></p>
    <p style="text-align: center;"><strong><span style="color: blue;">SINOPSIS:</span></strong></p>
    <p style="text-align: center;">Un material militar recientemente descubierto saca a la luz la horrible verdad tras el génesis de la vida en la Tierra.</p>
    <h2 style="text-align: center;"></h2>
    '''
    patron  = '<div class="post[^"]+" id="post-\d+">[^<]+'
    patron += '<h2 class="title"><a href="([^"]+)" rel="bookmark" title="[^"]+">([^<]+)</a></h2>[^<]+'
    patron += '<div class="postdate"><img[^<]+<img[^<]+</div>[^<]+'
    patron += '<div class="entry">[^<]+'
    patron += '<p><a[^<]+<img.*?src="([^"]+)"[^<]+</a><br />[^<]+'
    patron += '(.*?)</h2>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail,plot in matches:
        scrapedplot = scrapertools.htmlclean(plot).strip().replace("\n"," ")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    '''
    <div class="alignleft"><a href="http://unsoloclic.info/page/2/" >&laquo; Older Entries</a></div>
    '''
    patron  = '<div class="alignleft"><a href="([^"]+)" >\&laquo\; Older Entries</a></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[tusnovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    patron = '<a href="(http://[a-z0-9]+.linkbucks.com)"[^>]+><img class="[^"]+" title="([^"]+)" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for url,servertag,serverthumb in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="linkbucks", title=servertag+" [linkbucks]" , url=url , thumbnail=serverthumb , plot=item.plot , folder=False) )

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        if videoitem.server!="linkbucks":
            videoitem.channel=__channel__
            videoitem.action="play"
            videoitem.folder=False
            videoitem.title = "["+videoitem.server+"]"

    return itemlist

def play(item):
    logger.info("[tusnovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    if item.server=="linkbucks":
        logger.info("Es linkbucks")
        
        # Descarga la página de linkbucks
        data = scrapertools.cache_page(item.url)

        # Extrae la URL de adf.ly y descarga la página
        location = scrapertools.get_match(data,"Lbjs.TargetUrl \= '([^']+)'")
        logger.info("adf_url="+location)
        
        # Extrae la URL de saltar el anuncio en adf.ly
        if location.startswith("http://adf"):
            data = scrapertools.cache_page(location)
            adfskipad_url = urlparse.urljoin(location,scrapertools.get_match(data,"var url \= '(/go/[^']+)'"))
            logger.info("adfskipad_url="+adfskipad_url)
            
            # Obtiene la URL del video
            location = scrapertools.get_header_from_response(adfskipad_url,header_to_get="location")
            logger.info("location="+location)

        from servers import servertools
        itemlist=servertools.find_video_items(data=location)
        for videoitem in itemlist:
            videoitem.channel=__channel__
            videoitem.folder=False

    else:
        itemlist.append(item)

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    novedades_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors_items = findvideos( item=singleitem )
        for mirror_item in mirrors_items:
            video_items = play(mirror_item)
            if len(video_items)>0:
                return True

    return False
