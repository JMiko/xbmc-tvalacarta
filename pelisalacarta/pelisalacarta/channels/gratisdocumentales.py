# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para gratisdocumentales
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

from pelisalacarta import buscador

CHANNELNAME = "gratisdocumentales" 
DEBUG = True
 
def isGeneric():
    return True

def mainlist(item):
    logger.info("[gratisdocumentales.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades", action="parseweb", url="http://www.gratisdocumentales.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Categorias", action="buscacategorias", url="http://www.gratisdocumentales.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Tags", action="buscatags", url="http://www.gratisdocumentales.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Búsqueda", action="search"))
    
    return itemlist

def search(item):
    logger.info("[gratisdocumentales.py] search")
    itemlist=[]

    keyboard = xbmc.Keyboard()
    #keyboard.setDefault('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            searchUrl = "http://www.gratisdocumentales.com/?s="+tecleado+"&searchsubmit="
            parseweb(params,searchUrl,category)

def buscacategorias(item):
    logger.info("[gratisdocumentales.py] buscacategorias")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    patronvideos = 'href="([^"]+)" title="[^"]+">([^<]+)</a>([^<]+)</li><li'
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="parseweb" , title=match[1]+match[2] , url = match[0] , folder = True) )

    return itemlist

def buscatags(item):
    logger.info("[gratisdocumentales.py] buscacategorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patronvideos  = 'href="(http://www.gratisdocumentales.com/tag/.*?/)" id="tag-link-.+?>(.+?)</a> <a'
    matches = re.compile(patronvideos).findall(data)

    if len(matches)>0:
        for i in range(len(matches)):
            itemlist.append( Item(channel=CHANNELNAME, action="parseweb" , title=matches[i][1] , url = matches[i][0] , folder = True) )

    return itemlist

def parseweb(item):
    logger.info("[gratisdocumentales.py] parseweb")
    itemlist = []

    # Descarga la página
    '''
    <h2  class="posttitle"><a
    href='http://www.gratisdocumentales.com/524/' class='entry-title' rel='bookmark' title='Grande mas grande el mas grande - El tunel ' >Grande mas grande el mas grande - El tunel </a></h2><div
    class="postdata"> <span
    class="category"><a
    href="http://www.gratisdocumentales.com/category/tecnologia/" title="Ver todas las entradas en TECNOLOGIA" rel="category tag">TECNOLOGIA</a></span> <span
    class="comments"><a
    href="http://www.gratisdocumentales.com/524/#respond" title="Comentarios en Grande mas grande el mas grande &#8211; El tunel">Ninguna Respuesta &#187;</a></span></div></div><div
    class="date"><span
    class="month">ago</span> <span
    class="day">25</span><span
    class="year">2011</span></div></div><div
    class="entry entry-content fix"><div
    class="ezAdsense adsense adsense-leadin" style="text-align:center;margin:12px;"><script type="text/javascript"><!--
    smowtion_size = "468x60";
    smowtion_section = "836441";
    //-->
    
    </script><script type="text/javascript"
    src="http://ads.smowtion.com/ad.js">
    </script></div><p><a
    onclick="javascript:pageTracker._trackPageview('/outgoing/www.megavideo.com/?v=A0APGW3H');"  href="http://www.megavideo.com/?v=A0APGW3H">Grande mas grande el mas grande &#8211; El tunel </a></p><p><center><object
    width="640" height="394"><param
    name="movie" value="http://www.megavideo.com/v/A0APGW3H9efeb11eaf45f31ef6730e26ec88e6482"></param><param
    name="allowFullScreen" value="true"></param><embed
    src="http://www.megavideo.com/v/A0APGW3H9efeb11eaf45f31ef6730e26ec88e6482" type="application/x-shockwave-flash" allowfullscreen="true" width="640" height="394"></embed></object></center></p> <iframe
    src='http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.gratisdocumentales.com%2F524%2F&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=recommend&amp;colorscheme=light&amp;height=35' scrolling='no' frameborder='0' style='border:none; overflow:hidden; width:450px; height:35px' allowTransparency='true'></iframe><div
    style="display: none">VN:F [1.9.10_1130]</div><div
    class="ratingblock "><div
    class="ratingheader "></div><div
    class="ratingstars "><div
    id="article_rater_524" class="ratepost gdsr-oxygen gdsr-size-24"><div
    class="starsbar gdsr-size-24"><div
    class="gdouter gdheight"><div
    id="gdr_vote_a524" style="width: 0px;" class="gdinner gdheight"></div><div
    id="gdr_stars_a524" class="gdsr_rating_as"><a
    id="gdsrX524X10X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="10 / 10" class="s10" rel="nofollow"></a><a
    id="gdsrX524X9X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="9 / 10" class="s9" rel="nofollow"></a><a
    id="gdsrX524X8X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="8 / 10" class="s8" rel="nofollow"></a><a
    id="gdsrX524X7X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="7 / 10" class="s7" rel="nofollow"></a><a
    id="gdsrX524X6X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="6 / 10" class="s6" rel="nofollow"></a><a
    id="gdsrX524X5X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="5 / 10" class="s5" rel="nofollow"></a><a
    id="gdsrX524X4X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="4 / 10" class="s4" rel="nofollow"></a><a
    id="gdsrX524X3X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="3 / 10" class="s3" rel="nofollow"></a><a
    id="gdsrX524X2X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="2 / 10" class="s2" rel="nofollow"></a><a
    id="gdsrX524X1X0XaXarticle_rater_524Xarticle_loader_524X0X24" title="1 / 10" class="s1" rel="nofollow"></a></div></div></div></div><div
    id="article_loader_524" style="display: none; width: 240px " class="ratingloaderarticle"><div
    class="loader flower " style="height: 24px"><div
    class="loaderinner" style="padding-top: 2px">please wait...</div></div></div></div><div
    class="ratingtext "><div
    id="gdr_text_a524">Rating: 0.0/<strong>10</strong> (0 votes cast)</div></div></div><div
    style="display: none">VN:F [1.9.10_1130]</div><div
    class="thumblock "><div
    id="gdsr_thumb_524_a_up" class="gdt-size-20 gdthumb gdup"><a
    id="gdsrX524XupXaX0X20XY" class="gdt-starrating" rel="nofollow"></a></div><div
    id="gdsr_thumb_524_a_loader_up" style="display: none; width: 20px " class="ratingloader loadup"><div
    class="loader flower thumb" style="width: 20px; height: 20px;"></div></div><div
    id="gdsr_thumb_524_a_dw" class="gdt-size-20 gdthumb gddw"><a
    id="gdsrX524XdwXaX0X20XY" class="gdt-starrating" rel="nofollow"></a></div><div
    id="gdsr_thumb_524_a_loader_dw" style="display: none; width: 20px " class="ratingloader loaddw"><div
    class="loader flower thumb" style="width: 20px; height: 20px;"></div></div><div
    class="ratingtext "><div
    id="gdsr_thumb_text_524_a" class="gdt-size-20 gdthumbtext">Rating: <strong>0</strong> (from 0 votes)</div></div><div
    class="raterclear"></div></div><div
    class="addtoany_share_save_container"><div
    class="a2a_kit a2a_target addtoany_list" id="wpa2a_3"><a
    class="a2a_dd addtoany_share_save" href="http://www.addtoany.com/share_save"><img
    src="http://www.gratisdocumentales.com/wp-content/plugins/add-to-any/share_save_171_16.png" width="171" height="16" alt="Share"/></a></div></div></div><div
    class="post-footer fix"> <span
    class="author">Publicado por <a
    href="http://www.gratisdocumentales.com/author/admin/">admin</a> a las 16:36</span> <span
    class="tags">Etiquetado en: <a
    href="http://www.gratisdocumentales.com/tag/construcciones/" rel="tag">construcciones</a>, <a
    href="http://www.gratisdocumentales.com/tag/tunel/" rel="tag">tunel</a><br
    /></span></div></div><div
    class="post-517 post type-post status-publish format-standard hentry category-historia tag-historia tag-mayas tag-national-geographic" id="post-517"><div
    class='title-container fix'><div
    class="title">
    '''
    data = scrapertools.cache_page(item.url)
    patron = '<h2  class="posttitle">(.*?)class="author">Publicado por <a'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        patron2 = "class='entry-title' rel='bookmark' title='([^']+)'"
        matches2 = re.compile(patron2,re.DOTALL).findall(match)
        scrapedtitle = matches2[0]
        videos = servertools.findvideos(match)
        
        for video in videos:
            itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle+" ["+video[2]+"]" , url = video[1], server=video[2] , folder=False) )

    patronvideos  = "class='current'>[^<]+</span><a\s+href='([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="parseweb" , title="!Página siguiente" , url = match , folder = True) )

    return itemlist
