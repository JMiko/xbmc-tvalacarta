# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para tuteve
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "tuteve"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.tuteve mainlist")

    item = Item(channel=CHANNELNAME, url="http://play.tuteve.tv")
    return secciones(item)

def secciones(item):
    logger.info("tvalacarta.channels.tuteve programas")
    itemlist = []

    '''
    <ul id="menuPrincipal" >
    <div class="container_12" id="listaMenu">
    <li class="item" href="#" style="display:none">Destacados</li>
    <li class="item" style="background-color:#000; color:#0477b6"><a href="/" style="background-color:#000; color:#0477b6; text-decoration:none">Se&ntilde;al en Vivo</a></li>
    <li class="item"><a href="http://play.tuteve.tv/canal/listado/todo/lo-ultimo" style="color:#6D7583; text-decoration:none">Lo &uacute;ltimo</a></li>
    <li class="item" onmouseout="verMenu('submenu_Novelas',0)" onmouseover="verMenu('submenu_Novelas',1)"> Novelas
    <div id="submenu_Novelas" class="submenu" style="width:403px; display:none; z-index:99">
    <div class="lista"> <a class="item" href="http://play.tuteve.tv/canal/programa/51784/avenida-peru">
    <div class="icoBullet"></div>
    <span class="titulo">Avenida Per&uacute;</span></a> <a class="item" href="http://play.tuteve.tv/canal/programa/51757/el-capo">
    '''

    # Extrae las series
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul id="menuPrincipal"(.*?)</ul>')
    patron  = "<li class=\"item\" onmouseout=\"verMenu\('([^']+)',0\)\" onmouseover=\"verMenu\('[^']+',1\)\">([^<]+)<"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = ""
        plot = ""
        url = scrapedurl

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="programas" , url=item.url , extra=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=True ) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.tuteve programas")
    itemlist = []

    '''
    <ul id="menuPrincipal" >
    <div class="container_12" id="listaMenu">
    <li class="item" href="#" style="display:none">Destacados</li>
    <li class="item" style="background-color:#000; color:#0477b6"><a href="/" style="background-color:#000; color:#0477b6; text-decoration:none">Se&ntilde;al en Vivo</a></li>
    <li class="item"><a href="http://play.tuteve.tv/canal/listado/todo/lo-ultimo" style="color:#6D7583; text-decoration:none">Lo &uacute;ltimo</a></li>
    <li class="item" onmouseout="verMenu('submenu_Novelas',0)" onmouseover="verMenu('submenu_Novelas',1)"> Novelas
    <div id="submenu_Novelas" class="submenu" style="width:403px; display:none; z-index:99">
    <div class="lista"> <a class="item" href="http://play.tuteve.tv/canal/programa/51784/avenida-peru">
    <div class="icoBullet"></div>
    <span class="titulo">Avenida Per&uacute;</span></a> <a class="item" href="http://play.tuteve.tv/canal/programa/51757/el-capo">
    '''
    '''
    <a class="item" href="http://play.tuteve.tv/canal/programa/51810/somos-empresa">
    <div class="icoBullet"></div>
    <span class="titulo">Somos Empresa</span></a> 
    '''

    # Extrae las series
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<ul id="menuPrincipal"(.*?)</ul>')
    data = scrapertools.get_match(data,"<li class=\"item\" onmouseout=\"verMenu\('"+item.extra+"',0\)\" onmouseover=\"verMenu\('"+item.extra+"',1\)\">(.*?)</li")
    patron  = ' <a class="item" href="([^"]+)"[^<]+'
    patron += '<div class="icoBullet"></div[^<]+'
    patron += '<span class="titulo">([^<]+)</span></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = ""
        plot = ""
        url = scrapedurl+"/1"

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="episodios" , url=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=True ) )

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.tuteve episodios")
    itemlist=[]

    '''
    <a href="/videogaleria/programa/164741/2013-08-01-capitulo-74" id="itmVideo1" class="itmVideo">
    <div class="imgCont"><img src="http://cdn.tuteve.tv/files/2013/08/01/FN.jpg" width="300" height="225" class="imgVideo" border="0" title="Capítulo 74" alt=""/></div>
    <div class="itmDesc">
    <div class="infoItem"> <span class="fechaItem">1.08.2013</span>
    <div class="vistasItem">
    <div class="icoVistas" style="float:left"></div>
    <span style="float:left"><b style="font-size:13px">1727</b> visitas</span> </div>
    </div>
    <div class="tituloItem">Fina Estampa<br />
    <span style="font-size:13px">Capítulo 74</span></div>
    <div class="introItem">René besará a Griselda generando la sorpresa de todos. Además, Antenor se cruzará a Patricia en un restaurante y la verá con nuevo novio....</div>
    <div class="botonItem">
    <div class="icoBullet"></div>
    <span class="botonTexto">VER VIDEO</span></div>
    </div>
    </a>
    '''
    # Extrae los episodios
    logger.info("item.url="+item.url)
    data = scrapertools.cachePage( item.url )
    logger.info("data=#"+data+"#")
    patron  = '<a href="([^"]+)"[^<]+'
    patron += '<div class="imgCont"><img src="([^"]+)"[^<]+</div[^<]+'
    patron += '<div class="itmDesc".*?'
    patron += '<div class="tituloItem"[^<]+<br[^<]+'
    patron += '<span[^>]+>([^<]+)</span></div[^<]+'
    patron += '<div class="introItem">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip()
        title = scrapertools.htmlclean(title)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="partes" , url=url , thumbnail=thumbnail , plot=plot , show=item.title , fanart=thumbnail , folder=True ) )

    try:
        next_page=scrapertools.get_match(data,'<a class="botonNav" href="([^"]+)"[^<]+<div class="title">SIGUIENTE</div>')
        itemlist.append( Item( channel=item.channel , title=">> Página siguiente" , action="episodios" , url=urlparse.urljoin(item.url,next_page) ) )
    except:
        pass

    return itemlist

def partes(item):
    logger.info("tvalacarta.channels.tuteve partes")
    itemlist=[]

    '''
    <ul id="mycarousel" class="jcarousel-skin-tango">
    <li> 
    <script language="javascript">
    function setShare(indice){
    sUrl = "http://play.tuteve.tv/videogaleria/programa/164976/2013-08-02-capitulo-77?b=" + indice;
    document.getElementById('fblike').setAttribute('href', sUrl);
    FB.XFBML.parse(document.getElementById('fbdiv'));
    $('.twitter-share-button').attr('data-url',location.href + '?b=3');
    twttr.widgets.load();
    }
    </script>
    <div class="itmThumbFotos" onclick="setVideoFrame3('2a8e578f4cbe26a89701f7057592747f','oid=186741255&id=165693856&hash=3aad0b92ee9c0ba8&hd=1','vk','play*programa*fina-estampa',606,350,1,'Fina Estampa - Cap&iacute;tulo 77 (Parte 1)','true','nulo','');setShare(1)"> <img src="http://cs506507.vk.me/u186741255/video/l_860bb00e.jpg" width="150" height="113" class="imgThumb" />
    <div class="layer" id="layer_1">
    <div class="numero" id="num_1">1</div>
    </div>
    <div class="titulo" id="titulo_1">Fina Estampa - Capítulo 77 (Parte 1)</div>
    </div>
    </li>
    
    ...

    </ul>
    '''
    # Extrae los episodios
    data = scrapertools.cachePage(item.url)
    try:
        data = scrapertools.get_match(data,'<ul id="mycarousel" class="jcarousel-skin-tango">(.*?)</ul>')
        patron  = '<li[^<]+'
        patron += '<script language="javascript"[^<]+'
        patron += '</script[^<]+'
        patron += "<div class=\"itmThumbFotos\" onclick=\"setVideoFrame3\('([^']+)','([^']+)','([^']+)','([^']+)',\d+,\d+,\d+,'([^']+)'[^<]+"
        patron += '<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

        for id1,id2,server,id3,scrapedtitle,scrapedthumbnail in matches:
            title = scrapedtitle.strip()
            title = scrapertools.htmlclean(title)
            thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            plot = ""
            itemlist.append( get_item_video(item,title,thumbnail,id2,server) )
    except:
        pass

    if len(itemlist)==0:
        patron = "setVideoFrame\('([^']+)','([^']*)',\d+,'([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

        for id1,id2,server in matches:
            title = item.title
            title = scrapertools.htmlclean(title)
            thumbnail = ""
            plot = ""
            itemlist.append( get_item_video(item,title,thumbnail,id2,server) )

    try:
        #<a href="/programas/destacados/alaska-y-mario/episodios?start_20=20"><span class="link">Próximo</span>
        next_page=scrapertools.get_match(data,'<a href="([^"]+)"><span class="link">Pr')
        #/videos?prog=3798&#038;v=1&#038;pag=2
        itemlist.append( Item( channel=item.channel , title=">> Página siguiente" , action="episodios" , url=urlparse.urljoin(item.url,next_page) ) )
    except:
        pass

    return itemlist

def get_item_video(item,title,thumbnail,id,server):
    new_item = Item()

    if server=="vk":
        #setVideoFrame3('2a8e578f4cbe26a89701f7057592747f','oid=186741255&id=165693856&hash=3aad0b92ee9c0ba8&hd=1','vk','play*programa*fina-estampa',606,350,1,'Fina Estampa - Cap&iacute;tulo 77 (Parte 1)','true','nulo','')
        #http://vk.com/video_ext.php?oid=146263567&id=163818182&hash=2dafe3b87a4da653
        url = "http://vk.com/video_ext.php?"+id

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        new_item = Item( channel=item.channel , title=title , action="play" , server="vk" , url=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=False )

    elif server=="yt":
        #setVideoFrame3('2a8e578f4cbe26a89701f7057592747f','01SjStN4wx8','yt','play*programa*economia-en-directo',606,350,1,'  Econom&iacute;a en Directo 02-08-2013 (Parte 1)','true','nulo','')
        #http://www.youtube.com/watch?v=01SjStN4wx8
        url = "http://www.youtube.com/watch?v="+id

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        new_item = Item( channel=item.channel , title=title , action="play" , server="youtube" , url=url , thumbnail=thumbnail , show=title , fanart=thumbnail , folder=False )

    return new_item

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # El canal tiene estructura programas -> episodios -> play
    items_mainlist = mainlist(Item())
    items_programas = []

    # Todas las opciones del menu tienen que tener algo
    for item_mainlist in items_mainlist:
        exec "itemlist="+item_mainlist.action+"(item_mainlist)"
    
        if len(itemlist)==0:
            print "La sección '"+item_mainlist.title+"' no devuelve nada"
            return False

        items_programas = itemlist

    # Ahora recorre los programas hasta encontrar vídeos en alguno
    for item_programa in items_programas:
        print "Verificando "+item_programa.title
        items_episodios = episodios(item_programa)

        if len(items_episodios)>0:
            return True

    print "No hay videos en ningún programa"
    return False
