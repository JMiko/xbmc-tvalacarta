# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re

from core import scrapertools
from core import config
from core import logger

# Función genérica para encontrar vídeos en una página
def find_video_items(item=None, data=None):
    logger.info("[launcher.py] findvideos")

    # Descarga la página
    if data is None:
        from core import scrapertools
        data = scrapertools.cache_page(item.url)
        #logger.info(data)
    
    # Busca los enlaces a los videos
    from core.item import Item
    from servers import servertools
    listavideos = servertools.findvideos(data)

    if item is None:
        item = Item()

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0]
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist

def findvideos(data):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []

    # Megavideo
    import megavideo
    devuelve.extend(megavideo.find_videos(data))
        
    # Megaupload
    import megaupload
    devuelve.extend(megaupload.find_videos(data))

    # ---------------------------
    
    import directo
    devuelve.extend(directo.find_videos(data))
    
    # adnstream
    import adnstream
    devuelve.extend(adnstream.find_videos(data))

    # bitshare
    if config.get_setting("fileniumpremium")=="true":
        import bitshare
        devuelve.extend(bitshare.find_videos(data))

    # blip.tv
    import bliptv
    devuelve.extend(bliptv.find_videos(data))

    # divxstage
    import divxstage
    devuelve.extend(divxstage.find_videos(data))

    # downupload
    import downupload
    devuelve.extend(downupload.find_videos(data))

    # facebook
    import facebook
    devuelve.extend(facebook.find_videos(data))

    # filejungle
    if config.get_setting("fileniumpremium")=="true":
        import filejungle
        devuelve.extend(filejungle.find_videos(data))

    # fileserve
    import fileserve
    devuelve.extend(fileserve.find_videos(data))

    # fourshared
    import fourshared
    devuelve.extend(fourshared.find_videos(data))

    # googlevideo
    import googlevideo
    devuelve.extend(googlevideo.find_videos(data))

    # gigabyteupload
    import gigabyteupload
    devuelve.extend(gigabyteupload.find_videos(data))

    # movshare
    import movshare
    devuelve.extend(movshare.find_videos(data))
 
    # stagevu
    import stagevu
    devuelve.extend(stagevu.find_videos(data))
 
    # tutv
    import tutv
    devuelve.extend(tutv.find_videos(data))
    
    # tutv
    import userporn
    devuelve.extend(userporn.find_videos(data))

    # uploaded.to
    if config.get_setting("fileniumpremium")=="true":
        import uploadedto
        devuelve.extend(uploadedto.find_videos(data))

    # uploadstation
    if config.get_setting("fileniumpremium")=="true":
        import uploadstation
        devuelve.extend(uploadstation.find_videos(data))

    # veoh
    import veoh
    devuelve.extend(veoh.find_videos(data))

    # videobam
    import videobam
    devuelve.extend(videobam.find_videos(data))

    # vidbux
    import vidbux
    devuelve.extend(vidbux.find_videos(data))

    # videobb
    import videobb
    devuelve.extend(videobb.find_videos(data))

    # videoweed
    import videoweed
    devuelve.extend(videoweed.find_videos(data))

    # videozer
    import videozer
    devuelve.extend(videozer.find_videos(data))

    # vidxden
    import vidxden
    devuelve.extend(vidxden.find_videos(data))

    # vimeo
    import vimeo
    devuelve.extend(vimeo.find_videos(data))

    # vk
    import vk
    devuelve.extend(vk.find_videos(data))

    # wupload
    if config.get_setting("fileniumpremium")=="true":
        import wupload
        devuelve.extend(wupload.find_videos(data))

    # ---------------------------

    logger.info("0) Directo - myspace")
    patronvideos  = 'flashvars="file=(http://[^\.]+.myspacecdn[^\&]+)&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Directo - myspace")
    patronvideos  = '(http://[^\.]+\.myspacecdn.*?\.flv)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Directo - ning")
    patronvideos  = '(http://api.ning.com.*?\.flv)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) YouTube...")
    patronvideos  = 'http://www.youtube(?:-nocookie)?\.com/(?:(?:(?:v/|embed/))|(?:(?:watch(?:_popup)?(?:\.php)?)?(?:\?|#!?)(?:.+&)?v=))?([0-9A-Za-z_-]{11})?'#'"http://www.youtube.com/v/([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = match
        
        if url!='':
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'youtube' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)
    
    logger.info(") YouTube formato buenaisla")  #www.youtube.com%2Fwatch%3Fv%3DKXpGe0ds5r4
    patronvideos  = 'www.youtube.*?v(?:=|%3D)([0-9A-Za-z_-]{11})'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #file=http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv&
    #http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv
    logger.info("0) netlogicstat...")
    patronvideos  = "file\=(http\:\/\/es.video.netlogstatic[^\&]+)\&"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    logger.info("0) Videos animeid...") #http%3A%2F%2Fmangaid.com%2Ff.php%3Fh3eqiGdkh3akY2GaZJ6KpqyDaWmJ%23.mp4
    patronvideos  = "file=http.*?mangaid.com(.*?)&amp;backcolor="
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    cont = 0
    for match in matches:
        cont = cont + 1 
        titulo = " Parte %s [Directo]" % (cont)
        url = "http://mangaid.com"+match
        url = url.replace('%2F','/').replace('%3F','?').replace('%23','#')
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)    
            
    return devuelve
    
def findurl(code,server):
    mediaurl = "ERROR"
    server = server.lower() #Para hacer el procedimiento case insensitive

    if server == "megavideo":
        import megavideo
        mediaurl = megavideo.Megavideo(code)

    elif server == "megaupload":
        import megaupload
        mediaurl = megaupload.gethighurl(code)
        
    elif server == "directo":
        mediaurl = code

    elif server == "4shared":
        import fourshared
        mediaurl = fourshared.geturl(code)
        
    elif server == "xml":
        import xmltoplaylist
        mediaurl = xmltoplaylist.geturl(code)

    else:
        try:
            exec "import "+server+" as serverconnector"
            mediaurl = serverconnector.geturl(code)
        except:
            mediaurl = "ERROR"
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
        
    return mediaurl

def getmegavideolow(code, password=None):
    import megavideo
    if password is not None:
        return megavideo.getlowurl(code,password)
    else:
        return megavideo.getlowurl(code,password)

def getmegavideohigh(code):
    import megavideo
    return megavideo.gethighurl(code)

def getmegauploadhigh(page_url, video_password=""):
    logger.info("getmegauploadhigh "+page_url)
    import megaupload
    if config.get_setting("megavideopremium")=="true":
        logger.info("modo premium")
        return megaupload.get_video_url( page_url , True , config.get_setting("megavideouser") , config.get_setting("megavideopassword") , video_password )
    else:
        logger.info("modo no premium")
        return megaupload.get_video_url( page_url , False , "" , "" , video_password )

def getmegauploadlow(code, password=None):
    import megaupload
    if password is not None:
        return megaupload.getlowurl(code,password)
    else:
        return megaupload.getlowurl(code)
