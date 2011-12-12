# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesdanko.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

PLUGIN_NAME = "pelisalacarta"
CHANNELNAME = "seriesdanko"
DEBUG = config.get_setting("debug")

if config.get_system_platform() == "xbox":
    MaxResult = "55"
else:
    MaxResult = "500"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesdanko.py] mainlist")
    item.url = 'http://www.seriesdanko-rs.com/'
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Noticias"       , action="novedades"   , url=item.url))
    #itemlist.append( Item(channel=CHANNELNAME, title="Series actualizadas"    , action="ListVideos", url="http://www.blogger.com/feeds/5090863330072217342/posts/default/-/sd?start-index=1&max-results=%s&alt=json" %MaxResult))
    itemlist.append( Item(channel=CHANNELNAME, title="Lista alfanumerica" , action="ListByLetters", url=item.url))
    itemlist.append( Item(channel=CHANNELNAME, title="Listado completo"    , action="allserieslist", url=item.url))
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"               , action="search" , url=item.url, thumbnail="http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png"))
    return itemlist

def search(item,texto):
    logger.info("[seriesdanko.py] search")
    item.url = "http://www.seriesdanko-rs.com/gestion/pag_search.php"
    data = scrapertools.cachePagePost(item.url,'q='+texto)
    #print data
    return listvideos(item,data)


def novedades(item):
    logger.info("[seriesdanko.py] novedades")

    itemlist = []
    extra = ""
    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url).replace("\n","")
    #print data
    patronvideos = "(<h3 class='post-title entry-title'>.*?<div class='post-body entry-content')"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    totalItems = len(matches)
    for match in matches:
        try:
            scrapedurl = urlparse.urljoin(item.url,re.compile(r"href=(serie.+?)>").findall(match)[0])
        except:continue
        try:
            scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[0]
        except:
            scrapedthumbnail = ""
        try:
            scrapedtitle = re.compile(r"class='post-title entry-title'>(.+?)<").findall(match)[0]
            scrapedtitle = decodeHtmlentities(scrapedtitle)
        except:
            scrapedtitle = "sin titulo"
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = extra , folder=True , totalItems = totalItems ) )
    
    return itemlist
    

def ListByLetters(item):
    logger.info("[seriesdanko.py] ListByLetter")
    
    BaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    BaseUrl = "http://www.seriesdanko-rs.com/series.php?id=%s"
    action = "listvideos"
    bynum = "0"

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action=action, title="0-9" , url=BaseUrl % bynum , thumbnail="" , plot="" , folder=True) )
    for letra in BaseChars:
        scrapedtitle = letra
        scrapedplot = ""
        scrapedurl = BaseUrl % letra
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action=action, title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def allserieslist(item):
    logger.info("[seriesdanko.py] allserieslist")

    Basechars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl = "http://www.seriesdanko-rs.com/series.php?id=%s"
    action = "listvideos"

    itemlist = []

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info(data)

    # Extrae el bloque de las series
    patronvideos = "Listado de series disponibles</h2>(.*?)<div class='clear'></div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    patronvideos  = "<a href='([^']+)'.+?>([^<]+)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    totalItems = len(matches)
    for url,title in matches:
        scrapedtitle = title.replace("\n","").replace("\r","")
        scrapedurl = url
        scrapedurl = urlparse.urljoin(item.url,scrapedurl.replace("\n","").replace("\r",""))
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if title in Basechars or title == "0-9":
            
            scrapedurl = BaseUrl % title
        else:
            action = "capitulos"

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action=action , title=scrapedtitle , show=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle = scrapedtitle , totalItems = totalItems))

    return itemlist


def listvideos(item,extra=""):
    logger.info("[seriesdanko.py] ListVideos")
    
    if extra:
        data = extra
    else:
        # Descarga la página
        data = scrapertools.downloadpageGzip(item.url)
    patronvideos = "charset=(.+?)'"
    try:
        charset = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    except:
        logger.info("charset desconocido")
        charset = "utf-8"
    if not "seriesdanko-rs.com" in item.url:
        patronvideos = "<div class='post hentry'>(.*?)<div style='clear: both;'></div>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    else:
        patronvideos = "post-body entry-content(.*?)<div class='blog-pager' id='blog-pager'>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        if len(matches)>0:
            patronvideos = "<div(.*?)</div>"
            matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
        
    itemlist = []
    for match in matches:
        info = match.replace("\n","").replace('"',"'")
        try:
            if "seriesdanko-rs.com" in item.url:
                title = re.compile(r"title='(.+?)'").findall(info)[0]
                title = title.replace("Capitulos de: ","")
            else:
                title = re.compile("entry-title'><a href='.+?'>(.+?)</a>",re.DOTALL).findall(info)[0]
           
        except:
            title = item.title
        title = decodeHtmlentities(title)
        try:
            title = title.decode(charset).encode("utf-8")
        except:pass
        try:
            if "seriesdanko-rs.com" in item.url:
                url = urlparse.urljoin(item.url,re.compile("href='(.+?)'").findall(info)[0])
            else:
                url = re.compile("href='([^']+)'><img").findall(info)[0]
        except:
            continue
        try:
            thumbnail = re.compile("src='(.+?)'").findall(info)[0]
        except:
            thumbnail = ""

        
            
        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="capitulos", title=title , url=url , thumbnail=thumbnail , plot="" , folder=True) )
    return itemlist

def capitulos(item):
    logger.info("[seriesdanko.py] capitulos")
    
    if config.get_platform()=="xbmc" or config.get_platform()=="xbmcdharma":
        import xbmc
        if config.get_setting("forceview")=="true":
            xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
            #xbmc.executebuiltin("Container.Content(Movies)")
        
    if "|" in item.url:
        url = item.url.split("|")[0]
        sw = True
    else:
        url = item.url
        sw = False
    # Descarga la página
    if item.extra:
        
        contenidos = item.extra
        #print contenidos
    else:
        data = scrapertools.downloadpageWithoutCookies(url)

    # Extrae las entradas
        if sw:
            try:
                datadict = eval( "(" + data + ")" )    
                data = urllib.unquote_plus(datadict["entry"]["content"]["$t"].replace("\\u00","%"))
                matches=[]
                matches.append(data)
            except:
                matches = []
        else:
            patronvideos = "entry-content(.*?)<div class='blog-pager' id='blog-pager'>"
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            
        if len(matches)>0:
            contenidos = matches[0].replace('"',"'").replace("\n","")
        else:
            contenidos = item.url
            if sw:
                url = item.url.split("|")[1]
                if not url.startswith("http://"):
                    url = urlparse.urljoin("http://www.seriesdanko.com",url)
                # Descarga la página
                data = scrapertools.downloadpageGzip(url)
                patronvideos  = "entry-content(.*?)<div class='post-footer'>"
                matches = re.compile(patronvideos,re.DOTALL).findall(data)
                if len(matches)>0:
                    contenidos = matches[0]
                
    patronvideos  = "<a href='([^']+)'>([^<]+)</a> <img(.+?)/>"
    matches = re.compile(patronvideos,re.DOTALL).findall(contenidos.replace('"',"'"))
    #print contenidos        
    try:
        plot = re.compile(r'(Informac.*?/>)</div>').findall(contenidos)[0]
        if len(plot)==0:
            plot = re.compile(r"(Informac.*?both;'>)</div>").findall(contenidos)[0]
        plot = re.sub('<[^>]+>'," ",plot)
    except:
        plot = ""

    itemlist = []
    for match in matches:
    

        scrapedtitle = match[1].replace("\n","").replace("\r","")
        scrapedtitle = scrapertools.remove_show_from_title(scrapedtitle,item.show)
        
        #[1x01 - Capitulo 01]
        #patron = "(\d+x\d+) - Capitulo \d+"
        #matches = re.compile(patron,re.DOTALL).findall(scrapedtitle)
        #print matches
        #if len(matches)>0 and len(matches[0])>0:
        #    scrapedtitle = matches[0]

        if "es.png" in match[2]:
            subtitle = " (Español)"
        elif "la.png" in match[2]:
            subtitle = " (Latino)"
        elif "vo.png" in match[2]:
            subtitle = " (Version Original)"
        elif "vos.png" in match[2]:
            subtitle = " (Subtitulado)"
        elif "ca.png"  in match[2]:
            subtitle = " (Catalan)"
        elif "ga.jpg"  in match[2]:
            subtitle = " (Gallego)"
        elif "eu.jpg"  in match[2]:
            subtitle = " (Euskera)"
        elif "ba.png"  in match[2]:
            subtitle = " (Bable)"
        else:
            subtitle = ""
        scrapedplot = plot
        scrapedurl = urlparse.urljoin(item.url,match[0]).replace("\n","").replace("\r","")
        if not item.thumbnail:
            try:
                scrapedthumbnail = re.compile(r"src=([^']+)'").findall(contenidos)[0]
            except:
                    scrapedthumbnail = ""
        else:
            scrapedthumbnail = item.thumbnail
        scrapedthumbnail = scrapedthumbnail.replace("\n","").replace("\r","")
        if item.fulltitle == '':
            item.fulltitle = scrapedtitle + subtitle 
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle+subtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fulltitle = item.fulltitle, show = item.show , context="4", folder=True) )

    #xbmc.executebuiltin("Container.Content(Movies)")
    
    if len(itemlist)==0:
        listvideos = servertools.findvideos(contenidos)
        
        for title,url,server in listvideos:
            
            if server == "youtube":
                scrapedthumbnail = "http://i.ytimg.com/vi/" + url + "/0.jpg"
            else:
                scrapedthumbnail = item.thumbnail
            scrapedtitle = title
            scrapedplot = ""
            scrapedurl = url
            
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=CHANNELNAME, action="play", server=server, title=item.title +" "+ scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = scrapedtitle , folder=False) )

    return itemlist
    
def capitulos2(item):
    logger.info("[seriesdanko.py] capitulos")
    
    # Descarga la página
    url = item.url.split("|")[0]
    data = scrapertools.downloadpageGzip(url)
    # Convertimos los datos en json a diccionario
    datadict = eval( '(' + data + ')' )    
    #print datadict
    matches = []
    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )    
    return itemlist

def findvideos(item):
    logger.info("[seriesdanko.py] findvideos2")
    
    # Descarga la página
    if "xbmc" in config.get_platform():
        from core.subtitletools import saveSubtitleName
        saveSubtitleName(item)
    
    if "seriesdanko-rs.com" in item.url:
        data = scrapertools.downloadpageGzip(item.url).replace("\n","")
        patronvideos = "<tr><td class=('tam12'>.*?)</td></tr>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #for match in matches:
            #print match
        itemlist = []
        for match in matches:
            try:
                scrapedurl = urlparse.urljoin(item.url,re.compile(r"href='(.+?)'").findall(match)[0])
            except:continue
           
            try:
                scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[1]
                if "megavideo" in scrapedthumbnail:
                    mega = " [Megavideo]"
                elif "megaupload" in scrapedthumbnail:
                    mega = " [Megaupload]"
                else:
                    mega = ""
                if not scrapedthumbnail.startswith("http"):
                    scrapedthumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            except:continue
            try:
                subtitle = re.compile(r"src='(.+?)'").findall(match)[0]
                if "es.png" in subtitle:
                    subtitle = " (Español)"
                elif "la.png" in  subtitle:
                    subtitle = " (Latino)"
                elif "vo.png" in  subtitle:
                    subtitle = " (Version Original)"
                elif "vos.png" in  subtitle:
                    subtitle = " (Subtitulado)"
                elif "ca.png"  in match[2]:
                    subtitle = " (Catalan)"
                elif "ga.jpg"  in match[2]:
                    subtitle = " (Gallego)"
                elif "eu.jpg"  in match[2]:
                    subtitle = " (Euskera)"
                elif "ba.png"  in match[2]:
                    subtitle = " (Bable)"
                else:
                    subtitle = "(desconocido)"
                
                try:
                    opcion = re.compile(r"(Ver|Descargar)").findall(match)[0]
                except:
                    opcion = "Ver"
                
                scrapedtitle = opcion + " video" + subtitle + mega
            except:
                scrapedtitle = item.title
            scrapedplot = ""
            #scrapedthumbnail = item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            itemlist.append( Item(channel=CHANNELNAME, action="play2", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = item.fulltitle, extra = item.thumbnail , fanart=item.thumbnail , folder=False) )    
    
    else:
        from core import servertools
        itemlist = servertools.find_video_items( item )
    
    return itemlist

def play2(item):
    logger.info("[seriesdanko.py] play")

    # Descarga la página

    data = scrapertools.downloadpageGzip(item.url)

    listavideos = servertools.findvideos(data)
    itemlist = []
    from platformcode.xbmc import xbmctools 
    for video in listavideos:
        scrapedtitle = item.fulltitle.strip() + " - " + video[0]
        scrapedurl = video[1]
        server = video[2]
        
        xbmctools.play_video(channel=CHANNELNAME, server=server, url=scrapedurl, category=item.category, title=scrapedtitle, thumbnail=item.extra, plot=item.plot, extra=item.extra, subtitle=item.subtitle, video_password = item.password, fulltitle=item.fulltitle)

    return

def decodeHtmlentities(string):
    string = entitiesfix(string)
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string
