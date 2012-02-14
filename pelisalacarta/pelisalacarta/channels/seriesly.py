# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import os
import traceback
import urllib2

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
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct
    try :        
        from lib import simplejson
        json_data = simplejson.loads(data, object_hook=to_utf8)
        return json_data
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line ) 

''' URLEncode a string '''
def qstr(string):
    return string # urllib2.quote(string)   

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesly.py] mainlist")
    
    itemlist = []

    auth_token, user_token = perform_login(LOGIN,PASSWORD)
    
    extra_params = '%s|%s' % ( auth_token, user_token )

    itemlist.append( Item(channel=__channel__, title="Buscar", action="search") )
    itemlist.append( Item(channel=__channel__, title="Mis series", action="mis_series", extra=extra_params ) )
    itemlist.append( Item(channel=__channel__, title="Mis pelis", action="mis_pelis", extra=extra_params ) )
    itemlist.append( Item(channel=__channel__, title="Series Mas Votadas", action="series_mas_votadas", extra=extra_params ) )
    itemlist.append( Item(channel=__channel__, title="Peliculas Mas Vistas", action="pelis_mas_vistas", extra=extra_params ) )
    itemlist.append( Item(channel=__channel__, title="Ultimas Pelis Modificadas", action="ultimas_pelis_modificadas", extra=extra_params ) )

    if SESION=="true":
        itemlist.append( Item(channel=__channel__, title="Cerrar sesion ("+LOGIN+")", action="logout"))
    else:
        itemlist.append( Item(channel=__channel__, title="Iniciar sesion", action="login"))

    return itemlist

def logout(item):
    nombre_fichero_config_canal = os.path.join( config.get_data_path() ,__channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>false</session>\n<login></login>\n<password></password>\n</settings>")
    config_canal.close();    
    
    #Refrescamos variables globales
    SESION = config.get_setting("session","seriesly")
    LOGIN = config.get_setting("login","seriesly")
    PASSWORD = config.get_setting("password","seriesly")

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


    itemlist = []
    auth_token,user_token = perform_login(login,password)
    if(user_token == "invalid login"):
        itemlist.append( Item(channel=__channel__, title=user_token, action="mainlist"))
        return itemlist
    
    nombre_fichero_config_canal = os.path.join( config.get_data_path() , __channel__+".xml" )
    config_canal = open( nombre_fichero_config_canal , "w" )
    config_canal.write("<settings>\n<session>true</session>\n<login>"+login+"</login>\n<password>"+password+"</password>\n</settings>")
    config_canal.close();
    
    #Refrescamos variables globales
    SESION = config.get_setting("session","seriesly")
    LOGIN = config.get_setting("login","seriesly")
    PASSWORD = config.get_setting("password","seriesly")

    itemlist.append( Item(channel=__channel__, title="Sesión iniciada", action="mainlist"))
    return itemlist

def perform_login(login,password):

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()
    
    # UserToken
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=no&auth_token=%s&autologin=" % ( qstr(login), qstr(password), qstr(auth_token) )
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    return [auth_token,user_token]

def getCredentials(auth_token, user_token):
    logged = False
    old_auth_token = auth_token
    old_user_token = user_token
    try:
        if SESION != "true":
            return [old_auth_token,old_user_token, logged, "Sesión no iniciada"]
        
        count = 0
        while (not logged and count<3):
            if(count > 0):
                auth_token,user_token = perform_login(LOGIN,PASSWORD)
            post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
            url='http://series.ly/api/userSeries.php?type=&format=json'
            data = scrapertools.cache_page(url, post=post)
            patron = "User not logged.*?"
            matches = re.compile(patron,re.DOTALL).findall(data)
            patron2 = "ERROR: Auth required"
            matches2 = re.compile(patron2,re.DOTALL).findall(data)
            
            if (len(matches)>0 or len(matches2)>0):
                count = count + 1
            else:
                logged=True
    except:
        return [old_auth_token,old_user_token, logged, "Error al obtener credenciales"]  
    
    return [auth_token,user_token, logged, user_token]

def mis_series(item):
    
    logger.info("[seriesly.py] mis_series")
    
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    #Series Usuario
    url='http://series.ly/api/userSeries.php?type=&format=json'
    
    # Extrae las entradas (carpetas)
    # {"idSerie":"?", "title":"?", "seasons":?d, "episodes":?d, "poster":"http:?", "thumb":"http:?, "small_thumb":"http:?", "status":"Pending/Watching/Finished"}
    
    serieList = load_json(scrapertools.cache_page(url, post=post))
    if serieList == None : serieList = []
    
    logger.info('[seriesly.py] hay %d series' % len(serieList))
    
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
                 action = 'serie_capitulos',
                 title = '%(title)s (%(seasons)d Temporadas) (%(episodes)d Episodios) [%(estado)s]' % serieItem,
                 url = 'http://series.ly/api/detailSerie.php?idSerie=%(idSerie)s&caps=1&format=json' % serieItem,
                 thumbnail = serieItem['thumb'],
                 plot = "",
                 extra = item.extra
            )
        )
    return itemlist

def serie_capitulos(item):
    
    logger.info('[seriesly.py] serie_capitulos')
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    # Extrae las entradas (carpetas)
    
    # {"title":"?", "ids":"?", "synopsis":"?", "seriesly_score":?d, "participants_score":"?d", "poster":"http:?, "thumb":"http:?", "small_thumb":"http:?", "episode":
    #           [   {"idc":"?","title":"?","season":"?","viewed":"1/0"} ]
    
    serieInfo = load_json(scrapertools.cache_page(item.url, post=post))
    if serieInfo == None : serieInfo = {}
    if (not serieInfo.has_key('episode')) or serieInfo['episode'] == None : serieInfo['episode'] = []
    
    logger.info('hay %d capitulos' % len(serieInfo['episode']))
  
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
                action = 'capitulo_links',
                title = '%(season)s - %(title)s%(estado)s' % episode,
                url = 'http://series.ly/api/linksCap.php?idCap=%(idc)s&format=json' % episode,
                thumbnail = item.thumbnail,
                plot = "",
                extra = item.extra
            )
        )
    
    return itemlist

def capitulo_links(item):
    logger.info("[seriesly.py] capitulo_links")
    
    # TOKENS
    
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    # Extrae las entradas (carpetas)
    # data=[{"language":"versi\u00f3n original","subtitles":"castellano","hd":"0","url":"http:\/\/series.ly\/api\/goLink.php?auth_token=2ee35ed4a2x2b7f734a&user_token=2PDP;zP2xkPI0&enc=dkx.N6i\/j*3X","server":"wupload"},
    #{"language":"versi\u00f3n original","subtitles":"no","hd":"0","url":"http:\/\/series.ly\/api\/goLink.php?auth_token=2ee35ed4aaa&user_token=2PDP;aaaI0&enc=dkaaaR~H5?n%","server":"Novamov"}]
    data = scrapertools.cache_page(item.url, post=post)
    linkList = load_json(data)
    if linkList == None : linkList = []
    
    logger.info("hay %d videos" % len(linkList))
    
    itemlist = []        
    try:
        for link in linkList:
            
            hd = link['hd']
            if hd == '0' : link['hdtag'] = ''
            elif hd == '1' : link['hdtag'] = ' (HD)'
            else : link['hdtag'] = ' (?)'
            
            link['titletag'] = item.title; 
            
            itemlist.append(
                Item(channel=item.channel,
                    action = "links",
                    title = '%(titletag)s - %(server)s - %(language)s(sub %(subtitles)s)%(hdtag)s' % link,
                    url = link['url'],
                    thumbnail = item.thumbnail,
                    plot = "",
                    extra = ''
                )
            )
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
                
    return itemlist

def links(item):    
        
    itemlist = []
    try:
        count = 0
        exit = False
        while(not exit and count < 5):
            #A veces da error al intentar acceder
            try:
                page = urllib2.urlopen(item.url)
                urlvideo = "\"" + page.geturl() + "\""
                exit = True
            except:
                count = count + 1

        logger.info("urlvideo="+urlvideo)
        for video in servertools.findvideos(urlvideo) :
            #scrapedtitle = title.strip() + " " + match[1] + " " + match[2] + " " + video[0]
            scrapedtitle = scrapertools.htmlclean(video[0])
            scrapedurl = video[1]
            server = video[2]
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle, url=scrapedurl, thumbnail=item.thumbnail, plot="", server=server, extra="", category=item.category, fanart=item.thumbnail, folder=False))
    except:  
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line ) 
                
        
    return itemlist

def mis_pelis(item):
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    
    #Peliculas Usuario
    
    itemlist = []
    
    itemlist.append( Item(channel=__channel__, title="Vistas", action="mis_pelis_categoria", extra='%s|%s|%s' % (auth_token, user_token, 'Watched')) )
    itemlist.append( Item(channel=__channel__, title="Favoritas", action="mis_pelis_categoria", extra='%s|%s|%s' % (auth_token, user_token, 'Favourite')) )
    itemlist.append( Item(channel=__channel__, title="Pendientes", action="mis_pelis_categoria", extra='%s|%s|%s' % (auth_token, user_token, 'Pending')) )
    
    return itemlist

def mis_pelis_categoria(item):

    logger.info("[seriesly.py] mis_pelis_categoria")

    # TOKENS
    auth_token, user_token, cat_filter = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    #Peliculas Usuario (Filtradas por categoria)
    
    url='http://series.ly/api/userMovies.php?format=json'
    
    # Extrae las entradas (carpetas)
    #¬†[ {"idFilm":"?","title":"?","year":"?","genre":"?","poster":"http://?","thumb":"http://?","small_thumb":"http://?","status":"Watched/Favourite/Pending"} ]
    data = scrapertools.cache_page(url, post=post)
    movieList = load_json(data)
    if movieList == None : movieList = []
    
    logger.info("hay %d peliculas" % len(movieList))

    # compare function
    def movie_compare_criteria( x, y) :
        strx = x['title'].strip().lower()
        stry = y['title'].strip().lower()
        if strx == stry :
            return 0
        elif strx < stry :
            return -1
        else :
            return 1

    itemlist = []
    for movieItem in sorted(movieList, lambda x, y: movie_compare_criteria(x, y)):
        status = movieItem['status']
        if status == cat_filter:
            if status == 'Pending' : movieItem['estado'] = 'Pendiente';
            elif status == 'Watched' : movieItem['estado'] = 'Vista';
            elif status == 'Favourite' : movieItem['estado'] = 'Favorita';
            else : movieItem['estado'] = '?';
            # A√±ade al listado de XBMC
            itemlist.append(
                Item(channel=item.channel,
                     action = "peli_links",
                     title = '%(title)s (%(year)s) [%(estado)s]' % movieItem,
                     url = 'http://series.ly/api/detailMovie.php?idFilm=%s&format=json' % qstr(movieItem['idFilm']),
                     thumbnail = movieItem['poster'],
                     plot = "",
                     extra = '%s|%s' % ( qstr(auth_token), qstr(user_token) )
                )
            )
    
    return itemlist

def peli_links(item):

    logger.info("[seriesly.py] peli_links")
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    # Extrae las entradas (carpetas)
    #¬†{"title":"?","idp":"?", "synopsis":"?", "year":"?", "seriesly_score":?d, "participants_score":"?", "genre":"terror", "poster":"http://?","thumb":"http://?","small_thumb":"http://?","links":
    #   [{"language":"?","subtitles":"yes/no","quality":"?","part":"?","uploader":"?","highDef":"0/1","server":"?","url_cineraculo":"?","url_megavideo":"?"}]
    # }
    data = scrapertools.cache_page(item.url, post=post)
    linkList = load_json(data)
    if linkList == None : linkList = []
    
    logger.info("hay %d videos" % len(linkList))
    itemlist = []
    try:
        for link in linkList['links']:
            
            hd = link['highDef']
            if hd == '0' : link['hdtag'] = ''
            elif hd == '1' : link['hdtag'] = ' (HD)'
            else : link['hdtag'] = ' (?)'
            
            link['titletag'] = item.title; 
            
            itemlist.append(
                Item(channel=item.channel,
                    action = "links",
                    title = '%(titletag)s - %(server)s - %(language)s(sub %(subtitles)s)%(hdtag)s' % link,
                    url = 'http://series.ly/api/goLink.php?auth_token=%s&user_token=%s&enc=%s' % ( qstr(auth_token), qstr(user_token), qstr(link['url'].strip()) ),
                    thumbnail = item.thumbnail,
                    plot = linkList['synopsis'],
                    extra = ''
                )
            )
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        
    return itemlist

def series_mas_votadas(item):

    logger.info("[seriesly.py] series_mas_votadas")
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    url="http://series.ly/api/top.php?&format=json&id=1"
    
    # Extrae las entradas (carpetas)
    # {series_mes_votades":[{"nom_serie":"?", "vots":"?", "id_serie":"?"}]}
    
    topInfo = load_json(scrapertools.cache_page(url, post=post))
    if topInfo == None : topInfo = {}
    if topInfo['series_mes_votades'] == None : topInfo['series_mes_votades'] = []
    
    logger.info("hay %d series" % len(topInfo['series_mes_votades']))
    
    itemlist = []
    for serieItem in topInfo['series_mes_votades']:
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=item.channel,
                 action = 'serie_capitulos',
                 title = '%(nom_serie)s [%(vots)s Votos]' % serieItem,
                 url = 'http://series.ly/api/detailSerie.php?idSerie=%s&caps=1&format=json' % qstr(serieItem['id_serie']),
                 thumbnail = '',
                 plot = "",
                 extra = item.extra
            )
        )  
    return itemlist

def pelis_mas_vistas(item):

    logger.info("[seriesly.py] pelis_mas_vistas")
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    url="http://series.ly/api/top.php?&format=json&id=2"
    
    # Extrae las entradas (carpetas)
    # {pelis_mes_vistes":[{"nom_peli":"?", "id_peli":"?"}]}
    
    topInfo = load_json(scrapertools.cache_page(url, post=post))
    if topInfo == None : topInfo = {}
    if topInfo['pelis_mes_vistes'] == None : topInfo['pelis_mes_vistes'] = []
    
    logger.info("hay %d pelis" % len(topInfo['pelis_mes_vistes']))
    
    itemlist = []
    for movieItem in topInfo['pelis_mes_vistes']:
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=item.channel,
                 action = 'peli_links',
                 title = '%(nom_peli)s' % movieItem,
                 url = 'http://series.ly/api/detailMovie.php?idFilm=%s&format=json' % qstr(movieItem['id_peli']),
                 thumbnail = '',
                 plot = "",
                 extra = item.extra
            )
        )  
    return itemlist

def ultimas_pelis_modificadas(item):

    logger.info("[seriesly.py] ultimas_pelis_modificadas")
    
    # TOKENS
    auth_token, user_token = item.extra.split('|')
    auth_token, user_token, logged, nologgedmessage = getCredentials(auth_token, user_token)
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    url="http://series.ly/api/top.php?&format=json&id=3"
    
    # Extrae las entradas (carpetas)
    # {ultimes_pelis":[{"nom_peli":"?", "id_peli":"?"}]}
    
    topInfo = load_json(scrapertools.cache_page(url, post=post))
    if topInfo == None : topInfo = {}
    if topInfo['ultimes_pelis'] == None : topInfo['ultimes_pelis'] = []
    
    logger.info("hay %d pelis" % len(topInfo['ultimes_pelis']))
    
    itemlist = []
    for movieItem in topInfo['ultimes_pelis']:
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=item.channel,
                 action = 'peli_links',
                 title = '%(nom_peli)s [%(any)s]' % movieItem,
                 url = 'http://series.ly/api/detailMovie.php?idFilm=%s&format=json' % qstr(movieItem['id_peli']),
                 thumbnail = '',
                 plot = "",
                 extra = item.extra
            )
        )  
    return itemlist


def search(item,texto, categoria="*"):
    
    auth_token, user_token, logged, nologgedmessage = getCredentials("","")
    if (not logged):
        itemlist = []
        itemlist.append( Item(channel=__channel__, title=nologgedmessage, action="mainlist"))
        return itemlist 
    
    res = search_series(auth_token, user_token, item, texto)
    res.extend(search_films(auth_token, user_token, item, texto))
    
    return res
    
def search_series(auth_token, user_token, item, texto):
    logger.info("[seriesly.py] search")
    
    post = 'auth_token=%s' % ( qstr(auth_token) )
    
    url = 'http://series.ly/api/search.php?search=%s&type=serie&format=json' % ( qstr(texto) )
    
    # Extrae las entradas (carpetas)
    #¬†[{"idSerie":"?","title":"?","seasons":?d,"episodes":?d,"poster":"http://?","thumb":"http://?","small_thumb":"http://?"}
    
    serieList = load_json(scrapertools.cache_page(url, post=post))
    if serieList == None : serieList = []
    
    logger.info("hay %d series" % len(serieList))
    
    itemlist = []
    for serieItem in serieList:
        
        itemlist.append(
            Item(channel=item.channel,
                action = 'serie_capitulos',
                title = 'Serie: %(title)s (%(seasons)d Temporadas) (%(episodes)d Episodios)' % serieItem,
                url = "http://series.ly/api/detailSerie.php?caps=1&auth_token=" + auth_token + "&user_token=" + user_token + "&idSerie=" + serieItem['idSerie'] + "&format=json",
                thumbnail = serieItem['poster'],
                plot = '',
                extra = '%s|%s' % (auth_token, user_token)
            )
        )
          
    return itemlist

def search_films(auth_token, user_token, item, texto):
    logger.info("[seriesly.py] search_films")
    
    post = 'auth_token=%s' % ( qstr(auth_token) )
    
    url = 'http://series.ly/api/search.php?search=%s&type=film&format=json' % ( qstr(texto) )
    
    # Extrae las entradas (carpetas)
    # [{"idFilm":"?","title":"?","year":"?","genre":"?","poster":"http://?","thumb":"http://?","small_thumb":"http://?"}
    
    movieList = load_json(scrapertools.cache_page(url, post=post))
    if movieList == None : movieList = []
    
    logger.info("hay %d peliculas" % len(movieList))
    
    itemlist = []
    for movieItem in movieList:
        
        itemlist.append(
            Item(channel=item.channel,
                action = 'peli_links',
                title = 'Peli: %(title)s (%(year)s) (%(genre)s)' % movieItem,
                url = "http://series.ly/api/detailMovie.php?idFilm=" + movieItem['idFilm'] + "&format=json",
                thumbnail = movieItem['poster'],
                plot = '',
                extra = '%s|%s' % (auth_token, user_token)
            )
        )
          
    return itemlist
