# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import base64
import json

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriesly"
__category__ = "S,A"
__type__ = "generic"
__title__ = "Series.ly"
__language__ = "ES"
__creationdate__ = "20111119"

DEBUG = config.get_setting("debug")
SESION = config.get_setting("session","seriesly")
LOGIN = config.get_setting("login","seriesly")
PASSWORD = config.get_setting("password","seriesly")

def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct

    return json.loads(data, object_hook=to_utf8)

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesly.py] mainlist")

    itemlist = []
    
    itemlist.append( Item(channel=__channel__, title="Buscar", action="search"))
    itemlist.append( Item(channel=__channel__, title="Mis series", action="series"))
    itemlist.append( Item(channel=__channel__, title="Mis pelis", action="mispelis"))

    if SESION=="true":
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion (" + LOGIN + ")", action="logout") )
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login") )

    return itemlist

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión finalizada", action="mainlist"))
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

    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
    config_canal.close();

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    return itemlist

def series(item):

    logger.info("[seriesly.py] Mis Series")

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=no&auth_token=%s&action=perm" % (LOGIN, PASSWORD, auth_token)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token = data.strip()
    
    #Series Usuario
    
    url="http://series.ly/api/userSeries.php?auth_token=" + auth_token + "&user_token=" + user_token + "&type=&format=json"
    
    # Extrae las entradas (carpetas)
    # {"idSerie":"?", "title":"?", "seasons":?d, "episodes":?d, "poster":"http:?", "thumb":"http:?, "small_thumb":"http:?", "status":"Pending/Watching/Finished"}
    
    serieList = load_json(scrapertools.cache_page(url))
    if serieList == None : serieList = []
    
    logger.info('hay %d series' % len(serieList))
    
    itemlist = []
    for serieItem in serieList:
        status = serieItem['status'] 
        if status == 'Pending' : serieItem['estado'] = 'Pendiente'
        elif status == 'Watching' : serieItem['estado'] = 'Viendo'
        elif status == 'Finished' : serieItem['estado'] = 'Finalizada'
        else : serieItem['estado'] = '?'
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=item.channel,
                 action = "capitulos",
                 title = '%(title)s (%(seasons)d Temporadas) (%(episodes)d Episodios) [%(estado)s]' % serieItem,
                 url = 'http://series.ly/api/detailSerie.php?auth_token=' + auth_token + '&user_token=' + user_token + '&idSerie=' + serieItem['idSerie'] + "&caps=1&format=json",
                 thumbnail = serieItem['thumb'],
                 plot = "",
                 extra = auth_token + "|" + user_token
            )
        )
    return itemlist

def mispelis(item):

    logger.info("[seriesly.py] Mis Pelis")

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=no&auth_token=%s" % (LOGIN, PASSWORD, auth_token)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    #Peliculas Usuario
    
    url="http://series.ly/api/userMovies.php?auth_token=" + auth_token + "&user_token=" + user_token + "&format=json"
    
    # Extrae las entradas (carpetas)
    # [ {"idFilm":"?","title":"?","year":"?","genre":"?","poster":"http://?","thumb":"http://?","small_thumb":"http://?","status":"Watched/Favourite/Pending"} ]
    
    movieList = load_json(scrapertools.cache_page(url))
    if movieList == None : movieList = []
    
    logger.info("hay %d peliculas" % len(movieList))

    # compare function. 2 steps: First: by status, Second: by name
    status_order = { 'Pending': 0, 'Favourite': 1, 'Watched': 3}
    def movie_compare_criteria( x, y) :
        sx = status_order[x['status']]
        sy = status_order[y['status']]
        if sx == None : sx = 999
        if sy == None : sy = 999
        if sx == sy :
            strx = x['title'].lower()
            stry = y['title'].lower()
            if strx == stry : return 0
            elif strx < stry : return -1
            else : return 1
        else :
            return sx - sy

    itemlist = []
    for movieItem in sorted(movieList, lambda x, y: movie_compare_criteria(x, y)):
        status = movieItem['status'] 
        if status == 'Pending' : movieItem['estado'] = 'Pendiente';
        elif status == 'Watched' : movieItem['estado'] = 'Vista';
        elif status == 'Favourite' : movieItem['estado'] = 'Favorita';
        else : movieItem['estado'] = '?';
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=item.channel,
                 action = "pelis",
                 title = '%(title)s (%(year)s) [%(estado)s]' % movieItem,
                 url = 'http://series.ly/api/detailMovie.php?auth_token=' + auth_token + '&user_token=' + user_token + '&idFilm=' + movieItem['idFilm'] + "&format=json",
                 thumbnail = movieItem['poster'],
                 plot = "",
                 extra = auth_token + "|" + user_token
            )
        )
    
    return itemlist

def capitulos(item):

    logger.info("[seriesly.py] Capitulos")
    
    # TOKENS
    
    auth_token, user_token = item.extra.split("|")
    
    # Extrae las entradas (carpetas)
    
    # {"title":"?", "ids":"?", "synopsis":"?", "seriesly_score":?d, "participants_score":"?d", "poster":"http:?, "thumb":"http:?", "small_thumb":"http:?", "episode":
    #           [   {"idc":"?","title":"?","season":"?","viewed":"1/0"} ]
    
    serieInfo = load_json(scrapertools.cache_page(item.url))
    if serieInfo == None : serieInfo = {}
    if (not serieInfo.has_key('episode')) or serieInfo['episode'] == None : serieInfo['episode'] = []
    
    logger.info("hay %d capitulos" % len(serieInfo['episode']))
  
    itemlist = []
    for episode in serieInfo['episode'] :
        if episode.has_key('viewed'):
            viewed = episode['viewed'] 
            if viewed == '0' : episode['estado'] = ' [Visto]'
            elif viewed == '1' : episode['estado'] = ' [Pte]'
            else : episode['estado'] = ' [?]'
        else:
            episode['estado'] = ''
        
        itemlist.append(
            Item(channel=item.channel,
                action = "buscavideos",
                title = '%(season)s - %(title)s%(estado)s' % episode,
                url = 'http://series.ly/api/linksCap.php?auth_token=' + auth_token + '&user_token=' + user_token + '&idCap=' + episode['idc'] +  "&format=json",
                thumbnail = item.thumbnail,
                plot = "",
                extra = auth_token + "|" + user_token + "|" + episode['idc']
            )
        )
    
    return itemlist

def buscavideos(item):

    logger.info("[seriesly.py] Buscavideos")
    
    # TOKENS
    
    auth_token, user_token, idc = item.extra.split("|")
     
    # Extrae las entradas (carpetas)
    # [ {"language":"?","subtitles":"?","hd":"0/1","url_cineraculo":"http://?","url_megavideo":"http://?"} ]
    
    linkList = load_json(scrapertools.cache_page(item.url))
    if linkList == None : linkList = []
    
    logger.info("hay %d videos" % len(linkList))
    
    itemlist = []
    for link in linkList:
        
        hd = link['hd']
        if hd == '0' : link['hdtag'] = ''
        elif hd == '1' : link['hdtag'] = ' (HD)'
        else : link['hdtag'] = ' (?)'
        
        link['titletag'] = item.title; 
        
        itemlist.append(
            Item(channel=item.channel,
                action = "links",
                title = '%(titletag)s (%(language)s(Subtítulos %(subtitles)s)%(hdtag)s' % link,
                url = link['url_megavideo'],
                thumbnail = item.thumbnail,
                plot = "",
                extra = auth_token + "|" + user_token + "|" + link['url_megavideo']
            )
        )

    return itemlist

def links(item):
    
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos :
        #scrapedtitle = title.strip() + " " + match[1] + " " + match[2] + " " + video[0]
        scrapedtitle = video[0]
        srapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedurl = video[1]
        server = video[2]
            
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot="", server=server, extra="", category=item.category, fanart=item.thumbnail, folder=False))
    
    
    return itemlist

def pelis(item):

    logger.info("[seriesly.py] Pelis")
    
    # TOKENS
    
    auth_token, user_token = item.extra.split("|")
    
    # Extrae las entradas (carpetas)
    # {"title":"?","idp":"?", "synopsis":"?", "year":"?", "seriesly_score":?d, "participants_score":"?", "genre":"terror", "poster":"http://?","thumb":"http://?","small_thumb":"http://?","links":
    #   [{"language":"?","subtitles":"yes/no","quality":"?","part":"?","uploader":"?","highDef":"0/1","server":"?","url_cineraculo":"?","url_megavideo":"?"}]
    # }
    
    movieInfo = load_json(scrapertools.cache_page(item.url))
    if movieInfo == None : movieInfo = {}
    if (not movieInfo.has_key('links')) or movieInfo['links'] == None : movieInfo['links'] = []
    
    logger.info("hay %d links" % len(movieInfo['links']))
    
    itemlist = []
    for link in movieInfo['links']:
        link['titleTag'] = movieInfo['title']
        link['yearTag'] = movieInfo['year']
        
        part = link['part']
        if part == '0' : link['partTag'] = ''
        else : link['partTag'] = '(Parte %(part)s)' % link 
        
        hd = link['highDef']
        if hd == '0' : link['hdTag'] = ''
        elif hd == '1' : link['hdTag'] = ' (HD)'
        else : link['hdTag'] = ' (?)'
        
        itemlist.append(
            Item(channel=item.channel,
                action = "links",
                title = '%(titleTag)s (%(yearTag)s) (%(quality)s) (%(language)s)(Sub: %(subtitles)s)%(partTag)s%(hdTag)s' % link,
                url = "http://series.ly/api/goLink.php?auth_token=" + auth_token + "&user_token=" + user_token + "&enc=" + link['url_megavideo'].strip(),
                thumbnail = item.thumbnail,
                plot = movieInfo['synopsis'],
                extra = auth_token + "|" + user_token
            )
        )
          
    return itemlist

def search(item,texto, categoria="*"):
    
    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()

    # UserToken
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=no&auth_token=%s" % (LOGIN, PASSWORD, auth_token)
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    res = search_series(auth_token, user_token, item, texto)
    res.extend(search_films(auth_token, user_token, item, texto))
    return res
    
def search_series(auth_token, user_token, item, texto):
    logger.info("[seriesly.py] search")
    
    url="http://series.ly/api/search.php?auth_token=" + auth_token + "&search=" + texto + "&type=serie&format=json"
    
    # Extrae las entradas (carpetas)
    # [{"idSerie":"?","title":"?","seasons":?d,"episodes":?d,"poster":"http://?","thumb":"http://?","small_thumb":"http://?"}
    
    serieList = load_json(scrapertools.cache_page(url))
    if serieList == None : serieList = []
    
    logger.info("hay %d series" % len(serieList))
    
    itemlist = []
    for serieItem in serieList:
        
        itemlist.append(
            Item(channel=item.channel,
                action = "capitulos",
                title = 'Serie: %(title)s (%(seasons)d Temporadas) (%(episodes)d Episodios)' % serieItem,
                url = "http://series.ly/api/detailSerie.php?caps=1&auth_token=" + auth_token + "&user_token=" + user_token + "&idSerie=" + serieItem['idSerie'] + "&format=json",
                thumbnail = serieItem['poster'],
                plot = '',
                extra = auth_token + "|" + user_token
            )
        )
          
    return itemlist

def search_films(auth_token, user_token, item, texto):
    logger.info("[seriesly.py] search_films")
    
    url="http://series.ly/api/search.php?auth_token=" + auth_token + "&search=" + texto + "&type=film&format=json"
    
    # Extrae las entradas (carpetas)
    # [{"idFilm":"?","title":"?","year":"?","genre":"?","poster":"http://?","thumb":"http://?","small_thumb":"http://?"}
    
    movieList = load_json(scrapertools.cache_page(url))
    if movieList == None : movieList = []
    
    logger.info("hay %d peliculas" % len(movieList))
    
    itemlist = []
    for movieItem in movieList:
        
        itemlist.append(
            Item(channel=item.channel,
                action = "pelis",
                title = 'Peli: %(title)s (%(year)s) (%(genre)s)' % movieItem,
                url = "http://series.ly/api/detailMovie.php?auth_token=" + auth_token + "&user_token=" + user_token + "&idFilm=" + movieItem['idFilm'] + "&format=json",
                thumbnail = movieItem['poster'],
                plot = '',
                extra = auth_token + "|" + user_token
            )
        )
          
    return itemlist
