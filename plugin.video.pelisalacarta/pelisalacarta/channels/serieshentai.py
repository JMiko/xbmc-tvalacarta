# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para serieshentai
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

try:
    from core import logger
    from core import config
    from core import scrapertools
    from core.item import Item
    from servers import servertools
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import config
    from Code.core import scrapertools
    from Code.core.item import Item
    

CHANNELNAME = "serieshentai"
BASEURL = "http://series-hentai.net"
DEBUG=True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[serieshentai.py] mainlist")
    itemlist = []
    # Añade al listado de XBMC    
    itemlist = AddOnlineMovies(BASEURL + "/indice-online2.html")
    
    return itemlist

def AddOnlineMovies(url):
        logger.info("[serieshentai.py] WebParse")

        itemlist = []
        scrapedplot = ""
        scrapedthumbnail = ""
        # Descarga la página
        data = get_ExternalPage(url)
        
        aContent =re.compile('<div class="article-content">.*?</div>', re.S).findall(data)        
        if (len(aContent)>0):
            content = aContent[0]
            movies = re.compile('<tr class=.*?</tr>', re.S).findall(content)
            
            for movie in movies:
                patron = '<a href="([^"]+)">([^<]+)</a>'
                matches = re.compile(patron,re.DOTALL).findall(movie)
                for match in matches:
                    scrapedurl = match[0]
                    scrapedtitle = match[1]
                    itemlist.append( Item( channel=CHANNELNAME , title=scrapedtitle , action="WebMovie" , url=scrapedurl , plot=scrapedplot, thumbnail=scrapedthumbnail, folder=True ) )
        else:
            itemlist.append( Item( channel=CHANNELNAME , title="AddOnlineMovies Parsing Error" , action="AddOnlineMovies" , url="", folder=True ) )
       

        return itemlist
    
def WebMovie(item):
        itemlist = []
        scrapedplot = ""
        scrapedthumbnail = ""
        logger.info("[serieshentai.py] WebParse")    
        # Descarga la página
        data = get_ExternalPage(BASEURL+item.url)
       
        aContent =re.compile('<div class="article-content">.*?</div>', re.S).findall(data)        
        if (len(aContent)>0):
            content = aContent[0]
            patron = '<img src="([^"]+)"([^<]+)/>'
            matches = re.compile(patron,re.DOTALL).findall(content)
            if (len(matches)>0):
                 scrapedthumbnail=matches[0][0]  
            
            videos = findvideos(data)    
            if(len(videos)>0):
                numvideo=0
                for video in videos:                    
                    numvideo+=1                        
                    if (len(videos)>1):
                        vtitle= str(numvideo) + ".- " + item.title  
                    else:
                        vtitle= item.title                    
                    itemlist.append( Item(channel=CHANNELNAME, action="play" , title= vtitle +" ["+video[2]+"]", url=video[1], thumbnail=scrapedthumbnail, plot="", server=video[2], folder=False))
        else:
            itemlist.append( Item( channel=CHANNELNAME , title="WebMovie Parsing Error" , action="WebMovie" , url="", folder=True ) )
       

        return itemlist

def findvideos(data):
    logger.info("[serieshentai.py] findvideos")
    devuelve = []
    encontrados = set()
    
    #Series Hentai Base    
    patronvideos = "v\=([A-Z0-9a-z]{8})"
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megavideo')   
           
            
    #http://www.youtube.com/v/3_ptGFK8vTo&amp;hl=es&amp;fs=1    
    logger.info ("0) Enlace estricto a Youtube")
    patronvideos = 'youtube.com\/v\/([^ \t\n\r\f\v]{11})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'youtube')   
        
    #http://www.youtube.com/watch?v=HjjqZFfVXoU     
    logger.info ("1) Enlace estricto a Youtube")
    patronvideos = 'youtube.com\/watch.*?v=([^ \t\n\r\f\v]{11})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'youtube')     
        
                
    #videobb tipo "http://www.videobb.com/f/szIwlZD8ewaH.swf"
    logger.info ("0) Enlace estricto a VideoBB")
    patronvideos = 'videobb.com\/f\/([A-Z0-9a-z]{12}).swf'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'','http://videobb.com/video/'+match,'videobb') 
  
    #videobb tipo "http://www.videobb.com/video/ZIeb370iuHE4"
    logger.info ("1) Enlace estricto a VideoBB")
    patronvideos = 'videobb.com\/video\/([A-Z0-9a-z]{12})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'','http://videobb.com/video/'+match,'videobb')
         
    #videobb tipo "http://videobb.com/e/LLqVzhw5ft7T"
    logger.info ("2) Enlace estricto a VideoBB")
    patronvideos = 'videobb.com\/e\/([A-Z0-9a-z]{12})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'','http://videobb.com/video/'+match,'videobb') 
    
    
    #Megavideo tipo "http://www.megavideo.com/?v=CN7DWZ8S"
    logger.info ("0) Enlace estricto a megavideo")
    patronvideos = 'http\:\/\/www.megavideo.com\/.*?v\=([A-Z0-9a-z]{8})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megavideo') 
            
    #Megavideo tipo "http://www.megavideo.com/v/CN7DWZ8S"
    logger.info ("1) Enlace estricto a megavideo")
    patronvideos = 'http\:\/\/www.megavideo.com\/v\/([A-Z0-9a-z]{8})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megavideo')  
            
    #Megavideo tipo "http://www.megaupload.com/?d=CN7DWZ8S"
    logger.info ("2) Enlace estricto a megaupload")
    patronvideos = 'http\:\/\/www.megaupload.com\/.*?d\=([A-Z0-9a-z]{8})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megaupload')
    
    #Megavideo tipo "http://www.megaupload.com/?d=CN7DWZ8S"
    logger.info ("3) Enlace estricto a megaupload")
    patronvideos = 'http\:\/\/www.megavideo.com\/.*?d\=([A-Z0-9a-z]{8})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megaupload')
            
    #Megavideo tipo "http://www.megaupload.com/?d=CN7DWZ8S"
    logger.info ("4) Enlace estricto a megavideo")
    patronvideos = 'http\:\/\/wwwstatic.megavideo.com\/mv_player.swf\?v\=([A-Z0-9a-z]{8})'
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        AddVideoID(devuelve,encontrados,'',match,'Megavideo')

    videosarray = servertools.findvideos(data)
    for videoa in videosarray:
        AddVideoID(devuelve,encontrados,videoa[0],videoa[1],videoa[2])
                      
    return devuelve

def AddVideoID(devuelve,encontrados,title,id,servidor):  
    if id not in encontrados:
        devuelve.append( [title, id , servidor] )
        encontrados.add(id)
    else:
        logger.info(" id duplicado="+id) 
        
    return

# Request the given URL and return the response page, sin usar the cookie jar
def get_ExternalPage(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    response = urllib2.urlopen(request)
    html = response.read()
    response.close()
    return html