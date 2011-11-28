# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fileserve
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re,time
import os
import base64

from core import scrapertools
from core import logger
from core import config
from urllib import urlencode

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[filenium.py] get_video_url(page_url='%s')" % page_url)
    location=""
    
    if premium:
        # Hace el login
        url = "http://filenium.com/welcome"
        post = "username=%s&password=%s" % (user,password)
        data = scrapertools.cache_page(url, post=post)
        link = urlencode({'filez':page_url})
        location = scrapertools.cache_page("http://filenium.com/?filenium&" + link)
        user = user.replace("@","%40")
        location = location.replace("http://cdn.filenium.com","http://"+user+":"+password+"@cdn.filenium.com")
    
    return location

def extract_authorization_header(url):
    # Obtiene login y password, y lo añade como cabecera Authorization
    partes = url[7:].split("@")
    partes = partes[0].split(":")
    username = partes[0].replace("%40","@")
    password = partes[1]
    logger.info("[filenium.py] username="+username)
    logger.info("[filenium.py] password="+password)
    
    import base64
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    logger.info("[filenium.py] Authorization="+base64string)
    authorization_header = "Basic %s" % base64string
    
    # Ahora saca el login y password de la URL
    partes = url.split("@")
    url = "http://"+partes[1]
    logger.info("[filenium.py] nueva url="+url)

    return url,authorization_header