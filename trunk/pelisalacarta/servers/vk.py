# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para VK Server
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vk.py] get_video_url(page_url='%s')" % page_url)

    # Lee la página y extrae el ID del vídeo
    data = scrapertools.cache_page(page_url.replace("amp;",""))
    videourl = ""
    regexp =re.compile(r'vkid=([^\&]+)\&')
    match = regexp.search(data)
    vkid = ""
    if match is not None:
        vkid = match.group(1)
    else:
        logger.info("no encontro vkid")
    
    # Extrae los parámetros del vídeo y añade las calidades a la lista
    patron  = "var video_host = '([^']+)'.*?"
    patron += "var video_uid = '([^']+)'.*?"
    patron += "var video_vtag = '([^']+)'.*?"
    patron += "var video_no_flv = ([^;]+);.*?"
    patron += "var video_max_hd = '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    video_urls = []

    if len(matches)>0:    
        for match in matches:
            if match[3].strip() == "0" and match[1] != "0":
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                else:
                    videourl = "http://%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                
                # Lo añade a la lista
                video_urls.append( ["FLV [vk]",videourl])

            elif match[1]== "0" and vkid != "":     #http://447.gt3.vkadre.ru/assets/videos/2638f17ddd39-75081019.vk.flv 
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                else:
                    videourl = "http://%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                
                # Lo añade a la lista
                video_urls.append( ["FLV [vk]",videourl])
                
            else:                                   #http://cs12385.vkontakte.ru/u88260894/video/d09802a95b.360.mp4
                #Si la calidad elegida en el setting es HD se reproducira a 480 o 720, caso contrario solo 360, este control es por la xbox
                if match[4]=="0":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                elif match[4]=="1":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                elif match[4]=="2":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p [vk]",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                elif match[4]=="3":
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])
                    video_urls.append( ["480p [vk]",get_mp4_video_link(match[0],match[1],match[2],"480.mp4")])
                    video_urls.append( ["720p [vk]",get_mp4_video_link(match[0],match[1],match[2],"720.mp4")])
                else:
                    video_urls.append( ["240p [vk]",get_mp4_video_link(match[0],match[1],match[2],"240.mp4")])
                    video_urls.append( ["360p [vk]",get_mp4_video_link(match[0],match[1],match[2],"360.mp4")])

    for video_url in video_urls:
        logger.info("[vk.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def get_mp4_video_link(match0,match1,match2,tipo):
    if match0.endswith("/"):
        videourl = "%su%s/video/%s.%s" % (match0,match1,match2,tipo)
    else:
        videourl = "%s/u%s/video/%s.%s" % (match0,match1,match2,tipo)
    return videourl

def find_videos(data):
    encontrados = set()
    devuelve = []

    #vk tipo "http://vk.com/video_ext.php?oid=70712020&amp;id=159787030&amp;hash=88899d94685174af&amp;hd=3"
    patronvideos = '<iframe src="(http://[^\/]+\/video_ext.php[^"]+)"'
    logger.info("[vk.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[vk]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vk' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '(http\:\/\/vk.+?\/video_ext\.php[^"]+)"'
    logger.info("[vk.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #print data
    for match in matches:
        titulo = "[vk]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vk' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve