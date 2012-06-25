# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinetemagay.com por sdfasd
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

__channel__ = "cinetemagay"
__category__ = "D"
__type__ = "generic"
__title__ = "cinetemagay"
__language__ = "ES"

DEBUG = config.get_setting("debug")

IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'cinetemagay' )

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinetemagay.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Cine gay online" , url="http://www.cinegayonline.net/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://4.bp.blogspot.com/-jX_4yJbTpYw/T5GQHb5TgzI/AAAAAAAAAOE/GM4IHqBygb4/s938/cg2.jpg"))
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Latin Queer Channel" , url="http://latinqueerchannel.blogspot.com/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://3.bp.blogspot.com/-r8c6teBc_3I/TbmJiNtv0UI/AAAAAAAAC-0/KrthDgHEebM/banner-latin1.jpg"))
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Modo gay" , url="http://www.modogay.com/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://4.bp.blogspot.com/--oGFfDhcJg8/T4iGRMsNFOI/AAAAAAAABV4/oXKs9PMbrYU/s1600/mgbanner2.jpg"))         
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Películas gay online" , url="http://www.peliculasgayonline.com/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://4.bp.blogspot.com/-w6UbvMoq5aI/TxofB_ZAluI/AAAAAAAAEUg/j7_yYF0HNmc/s320/zonalogo.jpg"))               
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Tu nueva esquina gay" , url="http://www.tuesquinagay5.blogspot.com.es/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://2.bp.blogspot.com/_ErGLbQH-vrA/TM89_RA3I3I/AAAAAAAAANY/n7CKPO3oCoE/s0-R/4501630360_186f3cdc55_o.jpg"))           
    itemlist.append( Item(channel=__channel__, action="lista_2"  , title="[ESP] Crónicas de hefestion" , url="http://cronicasdehefestion.blogspot.com.es/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://4.bp.blogspot.com/-0lCbGrGkYzM/TyQ9a73qFcI/AAAAAAAAOK8/aQk2ZegBN9I/s1600/Banner%2B3.png"))           
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Cortosgay" , url="http://www.cortosgay.blogspot.com/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://2.bp.blogspot.com/-66icrLESK28/TjEWQFsSwKI/AAAAAAAAAZU/PYbNsjO8JSA/s890/cortosgay1%25282%2529.jpg"))         
    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ESP] Homoqueer" , url="http://homoqueer.blogspot.com.es/feeds/posts/default/?max-results=100&start-index=1",thumbnail="http://img269.imageshack.us/img269/1092/logotypeo.png"))         

#( no hay soporte para filesmonster)    itemlist.append( Item(channel=__channel__, action="lista"  , title="[ING] Rariteri" , url="http://rariteti.blogspot.com/feeds/posts/default/?max-results=100&start-index=1",thumbnail=""))         
   
    return itemlist









def lista(item):
    logger.info("[cinetemagay.py] lista")
    itemlist = []

   
  
         
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)



    # Extrae las entradas (carpetas)
   
    patronvideos  ='<title.*?src="([^"]+)"'
    patronvideos += "(.*?)<link rel='alternate' type='text/html' href='([^']+)' title='([^']+)'.*?>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)


    for match in matches:
        scrapedtitle = match[3]
        scrapedtitle = scrapedtitle.replace("&apos;","'")
        scrapedtitle = scrapedtitle.replace("@","a")
		
        scrapedtitle = scrapedtitle.replace("&quot;","'")
        scrapedtitle = scrapedtitle.replace("&lt;h1&gt;","")
        scrapedtitle = scrapedtitle.replace("&lt;/h1&gt;","")
        scrapedtitle = scrapedtitle.replace("3","e")
        scrapedtitle = scrapedtitle.replace("1","i")
        scrapedtitle = scrapedtitle.replace("0","o")
        
        scrapedurl = match[2]
        scrapedthumbnail = match[0]
        imagen = ""
        scrapedplot = match[1]  
        tipo = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        scrapedplot = "<"+scrapedplot     
        scrapedplot = scrapedplot.replace("&gt;",">")
        scrapedplot = scrapedplot.replace("&lt;","<")
        scrapedplot = scrapedplot.replace("</div>","\n")
        scrapedplot = scrapedplot.replace("<br />","\n")
        scrapedplot = scrapedplot.replace("&amp;","")
        scrapedplot = scrapedplot.replace("nbsp;","")
        scrapedplot=strip_tags(scrapedplot)
        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
   

    variable = item.url.split("index=")[1]
    variable=int(variable)
    variable+=100
    variable=str(variable)
    variable_url = item.url.split("index=")[0]
    url_nueva=variable_url+"index="+variable
    itemlist.append( Item(channel=__channel__, action="lista", title="Ir a la pÃ¡gina siguiente (desde "+variable+")" , url=url_nueva , thumbnail="" , plot="Pasar a la pÃ¡gina siguiente (en grupos de 100)\n\n"+url_nueva) )
   
    return itemlist









def lista_2(item):
    logger.info("[cinetemagay.py] lista")
    itemlist = []

   
  
         
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info(data)



    # Extrae las entradas (carpetas)
   
    patronvideos ='img.*?src="([^"]+)".*?' 
    patronvideos += "<link rel='replies' type='text/html' href='([^']+)' title='([^']+)'/><link"

    matches = re.compile(patronvideos,re.DOTALL).findall(data)


    for match in matches:
        scrapedtitle = "ver película"
        scrapedtitle = scrapedtitle.replace("&apos;","'")
        scrapedtitle = scrapedtitle.replace("@","a")
		
        scrapedtitle = scrapedtitle.replace("&quot;","'")
        scrapedtitle = scrapedtitle.replace("&lt;h1&gt;","")
        scrapedtitle = scrapedtitle.replace("&lt;/h1&gt;","")
        scrapedtitle = scrapedtitle.replace("3","e")
        scrapedtitle = scrapedtitle.replace("1","i")
        scrapedtitle = scrapedtitle.replace("0","o")
        
        scrapedurl = match[1]
        scrapedthumbnail = match[0]
        imagen = ""
        scrapedplot = match[1]  
        tipo = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        scrapedplot = "<"+scrapedplot     
        scrapedplot = scrapedplot.replace("&gt;",">")
        scrapedplot = scrapedplot.replace("&lt;","<")
        scrapedplot = scrapedplot.replace("</div>","\n")
        scrapedplot = scrapedplot.replace("<br />","\n")
        scrapedplot = scrapedplot.replace("&amp;","")
        scrapedplot = scrapedplot.replace("nbsp;","")
        scrapedplot=strip_tags(scrapedplot)
        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
   

    variable = item.url.split("index=")[1]
    variable=int(variable)
    variable+=100
    variable=str(variable)
    variable_url = item.url.split("index=")[0]
    url_nueva=variable_url+"index="+variable
    itemlist.append( Item(channel=__channel__, action="lista", title="Ir a la pÃ¡gina siguiente (desde "+variable+")" , url=url_nueva , thumbnail="" , plot="Pasar a la pÃ¡gina siguiente (en grupos de 100)\n\n"+url_nueva) )
   
    return itemlist




def detail(item):
    logger.info("[cinetemagay.py] detail")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    descripcion = ""
    plot = ""
    patrondescrip = 'SINOPSIS:(.*?)'
    matches = re.compile(patrondescrip,re.DOTALL).findall(data)
    if len(matches)>0:
        descripcion = matches[0]
        descripcion = descripcion.replace("&nbsp;","")
        descripcion = descripcion.replace("<br/>","")
        descripcion = descripcion.replace("\r","")
        descripcion = descripcion.replace("\n"," ")
        descripcion = descripcion.replace("\t"," ")
        descripcion = re.sub("<[^>]+>"," ",descripcion)
        descripcion = descripcion
        try :
            plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
        except:
            plot = descripcion

    # Busca los enlaces a los videos de : "Megavideo"
    video_itemlist = servertools.find_video_items(data=data)
    for video_item in video_itemlist:
        itemlist.append( Item(channel=__channel__ , action="play" , server=video_item.server, title=item.title+video_item.title,url=video_item.url, thumbnail=item.thumbnail, plot=item.plot, folder=False))

    # Extrae los enlaces a los videos (Directo)
    patronvideos = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        if not "www.youtube" in matches[0]:
            itemlist.append( Item(channel=__channel__ , action="play" , server="Directo", title=item.title+" [directo]",url=matches[0], thumbnail=item.thumbnail, plot=item.plot))

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    onesite_items = lista(mainlist_items[0])
    bien = False
    for onesite_item in onesite_items:
        mirrors = servertools.find_video_items( item=onesite_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien