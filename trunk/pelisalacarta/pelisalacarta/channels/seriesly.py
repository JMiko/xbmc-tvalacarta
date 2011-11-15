# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import base64

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "seriesly"
DEBUG = True
SESION = config.get_setting("session","seriesly")
LOGIN = config.get_setting("login","seriesly")
PASSWORD = config.get_setting("password","seriesly")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesly.py] mainlist")

    itemlist = []

    itemlist.append( Item(channel=CHANNELNAME, title="Mis series", action="series"))

    if SESION=="true":
        itemlist.append( Item(channel=CHANNELNAME, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=CHANNELNAME, title="Iniciar sesion", action="login"))

    return itemlist

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , CHANNELNAME+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Sesión finalizada", action="mainlist"))
    return itemlist

def login(item):
    import xbmc
    keyboard = xbmc.Keyboard("","Login")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        login = keyboard.getText()

    keyboard = xbmc.Keyboard("","Password")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        password = keyboard.getText()

    nombre_fichero_config_canal = os.path.join( config.get_data_path() , CHANNELNAME+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Sesión iniciada", action="mainlist"))
    return itemlist

def series(item):
    logger.info("[seriesly.py] series")

    callback_url = "bbbb"

    # Genera el auth token
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # Descarga la página
    url = "http://series.ly/api/api_login.php?lg_login="+LOGIN+"&lg_pass="+PASSWORD+"&auth_token="+auth_token
    #url = "http://series.ly/scripts/login/login.php?auth_token="+auth_token+"&autologin=2&callback_url="+callback_url
    #url  = "http://series.ly/api/authUser.php?callback_url=bbbb&autologin=2&auth_token="+auth_token
    post = "lg_login=%s&lg_pass=%s" % (LOGIN, PASSWORD)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")

    '''
    patronvideos  = 'user_token\=([a-z0-9]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    '''
    user_token=data

    '''
    url = "http://series.ly/api/authUser.php?auth_token="+auth_token+"&callback_url="+callback_url+"&action=perm"
    data = scrapertools.cache_page(url,post=post)
    print "****"
    print data
    print "****"
    '''
    
    '''
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=%s" % (LOGIN, PASSWORD,"/api/authUser.php?auth_token="+auth_token+"&callback_url="+callback_url+"&action=perm")
    data = scrapertools.cache_page(url,post=post)
    print "****"
    print data
    print "****"
    '''

    url = "http://series.ly/api/userSeries.php?auth_token="+auth_token+"&user_token="+user_token+"&type=&format=xml"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")

    # Extrae las entradas
    '''
    <?xml version="1.0"?><root><item><idSerie>S3PV5C9REH</idSerie><title>House M.D.</title><seasons>8</seasons><episodes>157</episodes><poster>http://cdn.opensly.com/series/S3PV5C9REH.jpg</poster><thumb>http://cdn.opensly.com/series/S3PV5C9REH-p.jpg</thumb><small_thumb>http://cdn.opensly.com/series/S3PV5C9REH-xs.jpg</small_thumb><status>Watching</status></item><item><idSerie>935FP7U3RK</idSerie><title>Star Wars: The Clone Wars</title><seasons>3</seasons><episodes>66</episodes><poster>http://cdn.opensly.com/series/935FP7U3RK.jpg</poster><thumb>http://cdn.opensly.com/series/935FP7U3RK-p.jpg</thumb><small_thumb>http://cdn.opensly.com/series/935FP7U3RK-xs.jpg</small_thumb><status>Watching</status></item><item><idSerie>3PVHEZ237D</idSerie><title>StarGate Universe</title><seasons>2</seasons><episodes>40</episodes><poster>http://cdn.opensly.com/series/3PVHEZ237D.jpg</poster><thumb>http://cdn.opensly.com/series/3PVHEZ237D-p.jpg</thumb><small_thumb>http://cdn.opensly.com/series/3PVHEZ237D-xs.jpg</small_thumb><status>Watching</status></item></root>
    '''
    patron  = '<item>'
    patron += '<idSerie>([^<]+)</idSerie>'
    patron += '<title>([^<]+)</title>'
    patron += '<seasons>([^<]+)</seasons>'
    patron += '<episodes>([^<]+)</episodes>'
    patron += '<poster>([^<]+)</poster>'
    patron += '<thumb>([^<]+)</thumb>'
    patron += '<small_thumb>([^<]+)</small_thumb>'
    patron += '<status>([^<]+)</status></item>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]+" (%s) (%s temporadas, %s episodios)" % (match[7],match[2],match[3])
        scrapedplot = ""
        scrapedurl = "http://series.ly/api/detailSerie.php?auth_token=%s&idSerie=%s&user_token=%s&format=json" % ( auth_token , match[0] , user_token )
        scrapedthumbnail = match[4]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = auth_token+"|"+user_token , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[seriesly.py] episodios")

    # Descarga la ficha de la serie
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las entradas
    '''
    {"title":"House M.D.",
    "synopsis":"Serie de TV (2004-Actualidad). 5 Nominaciones a los premios Emmy \/ Serie sobre un...ctorio? No, es House.",
    "seriesly_score":5,
    "participants_score":"722",
    "poster":"http:\/\/cdn.opensly.com\/series\/S3PV5C9REH.jpg",
    "thumb":"http:\/\/cdn.opensly.com\/series\/S3PV5C9REH-p.jpg",
    "small_thumb":"http:\/\/cdn.opensly.com\/series\/S3PV5C9REH-xs.jpg",
    "episode":[
        {"title":"Piloto","season":"1x01","viewed":"0",
            "links":[
            {"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"Kv5mk8RD%2BChjLVDiYppgWTFRULFmHyloBbBszRChI1ptw2LByDTZ3KKAUGuz9fOSGgC6fc%3D","url_megavideo":"4sLNBGC7VFePo0zo2VTTWTFRULFjkgU%2Fa6WVw5%2FlVlLUtO86BuuXROOiKoc%2FanaTtgCf5A%3D"},
            {"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"tTWQH4VYcwQOsPoUhIurWTFRULFSX8ite%2FYofEpCpkbiQTBPrDsgcbR0Wm9QuASJuFoS5M%3D","url_megavideo":"WH%2Ftdqg2hRY1%2FA4RtVg3WTFRULF6KHwe1hxWaGAfwCOVfTzOmrveCs%2Fiql3uNYN%2BpMs520%3D"},
            {"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"bEdEdbLGKitL3zs%3D"}
            ]
        },
        {"title":"La Navaja De Occam","season":"1x03","viewed":"0","links":[{"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"VMpYak4vnYW5ftmoepgQWTFRULFMXJ1AsNOtEEZOGVQuBHCtmhzbCYWpJxbptng4YPUWi8%3D","url_megavideo":"dAycB%2Fw0pNf255O5pU%2FuWTFRULF0v2rAcw5isp0PBYyI9zL0SS6D2xRmv4rhFqOKbK0R9A%3D"},{"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"6H28ImzPXUBRsfXoHXwPWTFRULFyd771Qz8KQsw739ke0JOSB9we0xMvz3fbqHfQh2FsvM%3D","url_megavideo":"EtqzZJ%2F2gon4tHCyaxArWTFRULFcx7uw1MPx30DyVP3mWJ4NOY15Z0VdCHHJ2CKRvHnZa8%3D"},{"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"xgxIOA4vSa1eJ0%2BIkXe2WTFRULFbrcXGUP4KX6kGbYmFuzSHVJvpB6IbzjpWcPHkJtmBlU%3D","url_megavideo":"4Z7g%2FZfvtqatL1Iz10V9WTFRULFmB2Xeq7fY5WcamsdxFJmnjx4yh4lWngH0QnO5q4LHh0%3D"},{"language":"castellano","subtitles":"no","hd":"0","url_cineraculo":"nIqU37U6nMF4gZUuMbGwWTFRULF8N1HOUUpoM
    '''
    data = data.replace("false","False").replace("true","True")
    data = data.replace("null","None")
    jsondata = eval("("+data+")")

    itemlist = []
    for episode in jsondata['episode']:
        # Pasa los links en la URL, así no hay que volver a descargarlos
        scrapedurl = ""
        scrapedtitle = episode['season']+" "+episode['title']
        scrapedplot = jsondata['synopsis']
        scrapedthumbnail = jsondata['poster']
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="videos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=item.extra+"|"+str(episode['links']) , folder=True) )

    return itemlist

def videos(item):
    logger.info("[seriesly.py] videos")

    # Descarga la página
    logger.info("item.extra="+item.extra)
    auth_token = item.extra.split("|")[0]
    user_token = item.extra.split("|")[1]
    data=item.extra.split("|")[2]
    jsondata = eval("("+data+")")

    itemlist = []
    for link in jsondata:
        scrapedurl = "http://series.ly/api/goLink.php?auth_token=%s&user_token=%s&enc=%s" % (auth_token,user_token,link['url_megavideo'])
        scrapedtitle = link['language']+", subtítulos "+link['subtitles']
        if link['hd']=="1":
            scrapedtitle+=", HD"
        scrapedplot = item.plot
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        itemlist.append( Item(channel=CHANNELNAME, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, extra=item.extra, folder=False) )

    return itemlist

def play(item):
    logger.info("[seriesly.py] play")

    # Descarga la página
    partes = item.url.split("?")
    url = partes[0]
    post = partes[1]
    data = scrapertools.cachePage(url,post=post)
    logger.info(data)

    itemlist = []

    return itemlist
