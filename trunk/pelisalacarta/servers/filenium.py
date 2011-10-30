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

    if premium:     
        # Hace el login
        url = "http://filenium.com/welcome"
        post = "username=%s&password=%s" % (user,password)
        data = scrapertools.cache_page(url, post=post)
        link = urlencode({'filez':page_url})
        location = scrapertools.cache_page("http://filenium.com/?filenium&" + link)
        user = user.replace("@","%40")
        location = location.replace("http://filenium.com","http://"+user+":"+password+"@filenium.com")
    return location