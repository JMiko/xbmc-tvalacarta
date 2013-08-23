# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Tools for m3u file handling
#------------------------------------------------------------

import urlparse,urllib2,urllib
import time
import os
import sys
import re
import socket

import config
import logger
import downloadtools
import scrapertools
from item import Item

NO_CATEGORY = "Sin categoria"

def parse_items_from_m3u_list(data,category=NO_CATEGORY):
    logger.info("simpletv.parse_items_from_m3u_list category="+str(category))
    entries = []

    # Busca el bloque con los canales
    lines = data.split("\n")
    i=0

    # Recorre la lista
    while i<len(lines):

        # Cada entrada empieza por #EXTINF
        '''
        #EXTINF:-1 $ExtFilter="DIGITAL",DOCUMENTALES:NATIONAL GEOGRAPHIC
        rtmp://$OPT:rtmp-raw=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=1 pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK --live
        '''
        if lines[i].startswith("#EXTINF"):

            title = lines[i]
            try:
                entry_category = scrapertools.get_match(title,'\$ExtFilter\="([^"]+)"')
            except:
                entry_category = ""

            if entry_category == "":
                entry_category = NO_CATEGORY

            logger.info("title="+title+" category="+entry_category)

            if category == NO_CATEGORY or entry_category == category:

                title = re.compile('\$ExtFilter\="([^"]+)"',re.DOTALL).sub("",title)
                title = title.replace('#EXTINF:-1',"")
                title = title.strip()
                if title.startswith(","):
                    title = title[1:].strip()

                url = lines[i+1].strip()

                logger.info("----------------------------------------------------")
                logger.info("title="+title)
                logger.info("url1="+url)
                #url1=rtmp://$OPT:rtmp-raw=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=1 pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK --live

                #if url.startswith(("rtmp://", "rtmpt://", "rtmpe://", "rtmpte://", "rtmps://")):
                if url.startswith("rtmp"):
                    url = url.replace("rtmp://$OPT:rtmp-raw=","")
                    logger.info("url2="+url)
                    #url2=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=1 pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK --live

                    url = url.replace("live=1", "live=true")
                    logger.info("url3="+url)
                    #url3=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=true pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK --live

                    url = url.replace("--live","live=true")
                    logger.info("url4="+url)
                    #url4=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=true pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK live=true

                    if not re.search(" timeout=", url):
                        url = url + " timeout=300"
                        logger.info("url5="+url)
                        #url5=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=true pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:O timeout=300

                entries.append( Item(title=title,url=url,category=entry_category) )

        i = i + 1

    return entries

def parse_categories_from_m3u_list(data):
    logger.info("simpletv.parse_categories_from_m3u_list")
    entries = []
    encontradas = set()

    # Busca el bloque con los canales
    lines = data.split("\n")
    i=0

    # Recorre la lista
    while i<len(lines):

        # Cada entrada empieza por #EXTINF
        '''
        #EXTINF:-1 $ExtFilter="DIGITAL",DOCUMENTALES:NATIONAL GEOGRAPHIC
        rtmp://$OPT:rtmp-raw=rtmp://212.7.206.71/live playpath=showstreamintvtoros2222?id=40786 swfUrl=http://www.ucaster.eu/static/scripts/eplayer.swf live=1 pageUrl=http://www.ucaster.eu/embedded/showstreamintvtoros2222/1/650/400 conn=S:OK --live
        '''
        if lines[i].startswith("#EXTINF"):

            title = lines[i]
            logger.info("title="+title)
            try:
                entry_category = scrapertools.get_match(title,'\$ExtFilter\="([^"]+)"')
            except:
                entry_category = ""

            if entry_category == "":
                entry_category = NO_CATEGORY

            if entry_category not in encontradas:
                encontradas.add(entry_category)
                entries.append( Item(title=entry_category) )

        i = i + 1

    return entries
