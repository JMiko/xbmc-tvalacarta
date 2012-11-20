# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import os
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

def isGeneric():
    return True

"""Handler para library_service"""
def episodios(item):
    # Obtiene de nuevo los tokens
    episode_list = serie_capitulos(item)
    for episode in episode_list:
        episode.extra = item.extra

"""Handler para launcher (library)"""
def findvideos(item):
    return capitulo_links(item)

"""Handler para launcher (library)"""
def play(item):
    return links(item)

def mainlist(item):
    logger.info("[seriesly.py] mainlist")
    
    itemlist = []

    if config.get_setting("serieslyaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        auth_token, user_token = perform_login()
        if not "invalid login" in user_token:
            extra_params = '%s|%s' % ( auth_token, user_token )
        
            itemlist.append( Item(channel=__channel__, title="Buscar", action="search") )
            itemlist.append( Item(channel=__channel__, title="Mis series", action="mis_series", extra=extra_params ) )
            itemlist.append( Item(channel=__channel__, title="Mis pelis", action="mis_pelis", extra=extra_params ) )
            itemlist.append( Item(channel=__channel__, title="Series Mas Votadas", action="series_mas_votadas", extra=extra_params ) )
            itemlist.append( Item(channel=__channel__, title="Peliculas Mas Vistas", action="pelis_mas_vistas", extra=extra_params ) )
            itemlist.append( Item(channel=__channel__, title="Ultimas Pelis Modificadas", action="ultimas_pelis_modificadas", extra=extra_params ) )
        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )

    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def getCredentials():
    logged = False
    
    try:
        count = 0
        while (not logged and count<6):
            auth_token,user_token = perform_login()
            post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
            url='http://series.ly/api/isUserLogged.php?type=&format=json'
            logresult = load_json(scrapertools.cache_page(url, post=post))
            if logresult == None or logresult['result'] != '1': 
                count = count + 1
            else:
                logged=True
    except:
        return [auth_token,user_token, logged, "Error al obtener credenciales"]
      
    if(not logged):
        return [auth_token,user_token, logged, "Despues de 5 intentos no hemos podido loguear"]
    
    return [auth_token,user_token, logged, user_token]

def mis_pelis(item):
    
    logger.info("[seriesly.py] mis_pelis")

    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )

    # Peliculas Usuario (Filtradas por categoria)
    url='http://series.ly/api/userMovies.php?format=json'
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
    try:
        movieList = limpia_lista(movieList, 'title')
        sortedlist = sorted(movieList, lambda x, y: movie_compare_criteria(x, y))
    except: 
        sortedlist = movieList
        
    for movieItem in sortedlist:
        status = movieItem['status']
        if status == 'Pending' : movieItem['estado'] = 'Pendiente'
        elif status == 'Watched' : movieItem['estado'] = 'Vista'
        elif status == 'Favourite' : movieItem['estado'] = 'Favorita'
        else : movieItem['estado'] = '?';
        # Añade al listado de XBMC
        itemlist.append(
            Item(channel=__channel__,
                action = "peli_links",
                title = '%(title)s (%(year)s) [%(estado)s]' % movieItem,
                url = 'http://series.ly/api/detailMovie.php?idFilm=%s&format=json' % qstr(movieItem['idFilm']),
                thumbnail = movieItem['poster'],
                plot = "",
                extra = '%s|%s' % ( qstr(auth_token), qstr(user_token) )
            )
        )
    
    return itemlist

def mis_series(item):
    
    logger.info("[seriesly.py] mis_series")

    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    
    # Series Usuario
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    url='http://series.ly/api/userSeries.php?type=&format=json'
    serieList = load_json(scrapertools.cache_page(url, post=post))
    if serieList == None : serieList = []
    
    logger.info('[seriesly.py] hay %d series' % len(serieList))
    
    itemlist = []
    for serieItem in serieList:
        logger.info("serieItem="+str(serieItem))
        #serieItem={u'status': 'Watching', u'thumb': 'http://cdn.opensly.com/series/HV9RTVP6XN-p.jpg', u'title': 'Digimon: Digital Monsters', u'poster': 'http://cdn.opensly.com/series/HV9RTVP6XN.jpg', u'episodes': 343, u'small_thumb': 'http://cdn.opensly.com/series/HV9RTVP6XN-xs.jpg', u'seasons': 7, u'idSerie': 'HV9RTVP6XN'}

        if serieItem['title'] is not None:
            status = serieItem['status'] 
            if status == 'Pending' : serieItem['estado'] = 'Pendiente'
            elif status == 'Watching' : serieItem['estado'] = 'Viendo'
            elif status == 'Finished' : serieItem['estado'] = 'Finalizada'
            else : serieItem['estado'] = '?'
            # Añade al listado de XBMC
            itemlist.append(
                Item(channel=__channel__,
                     action = 'serie_capitulos',
                     title = '%(title)s (%(seasons)d Temporadas) (%(episodes)d Episodios) [%(estado)s]' % serieItem,
                     url = 'http://series.ly/api/detailSerie.php?idSerie=%(idSerie)s&caps=1&format=json' % serieItem,
                     thumbnail = serieItem['thumb'],
                     plot = "",
                     show = serieItem['title'],
                     extra = item.extra
                )
            )
            
    itemlist = sorted( itemlist , key=lambda item: item.title)
        
    return itemlist

def serie_capitulos(item):
    
    logger.info('[seriesly.py] serie_capitulos')
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    serieInfo = load_json(scrapertools.cache_page(item.url, post=post))
    if serieInfo == None : serieInfo = {}
    if (not serieInfo.has_key('episode')) or serieInfo['episode'] == None : serieInfo['episode'] = []
    
    logger.info('hay %d capitulos' % len(serieInfo['episode']))
  
    itemlist = []
    for episode in serieInfo['episode'] :
        if episode.has_key('viewed'):
            viewed = episode['viewed'] 
            if viewed == '0' : episode['estado'] = ' [Pendiente]'
            elif viewed == '1' : episode['estado'] = ' [Visto]'
            else : episode['estado'] = ' [?]'
        else:
            episode['estado'] = ''
        
        itemlist.append(
            Item(channel=__channel__,
                action = 'capitulo_links',
                title = '%(season)s - %(title)s%(estado)s' % episode,
                url = 'http://series.ly/api/linksCap.php?idCap=%(idc)s&format=json' % episode,
                thumbnail = item.thumbnail,
                plot = "",
                show = item.show,
                extra = item.extra
            )
        )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel='seriesly', title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="serie_capitulos###", show=item.show) )

    return itemlist

def capitulo_links(item):
    logger.info("[seriesly.py] capitulo_links")
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    data = scrapertools.cache_page(item.url+"&"+post)
    linkList = load_json(data)
    if linkList == None : linkList = []
    
    logger.info("hay %d videos" % len(linkList))
    
    itemlist = []        
    for link in linkList:

        #hd = link['hd']
        #if hd == '0' : link['hdtag'] = ''
        #elif hd == '1' : link['hdtag'] = ' (HD)'
        #else : link['hdtag'] = ' (?)'

        itemlist.append(
            Item(channel=__channel__,
                action = "links",
                title = '%(info)s - %(host)s - %(lang)s(sub %(sub)s)' % link,
                url = link['url'],
                thumbnail = item.thumbnail,
                plot = "",
                extra = ''
            )
        )

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

def limpia_lista(movielist, campo):
        
    cleanlist = []
    for movieItem in movielist:
        if(movieItem[campo] is not None):
            cleanlist.append( movieItem)
    return cleanlist 

def peli_links(item):

    logger.info("[seriesly.py] peli_links")
   
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
   
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    data = scrapertools.cache_page(item.url, post=post)
    linkList = load_json(data)
    if linkList == None : linkList = []
   
    logger.info("hay %d videos" % len(linkList))
    itemlist = []
    try:
        for link in linkList['links']:
           
            #hd = link['highDef']
            #if hd == '0' : link['hdtag'] = ''
            #elif hd == '1' : link['hdtag'] = ' (HD)'
            #else : link['hdtag'] = ' (?)'
           
            #Neofreno: Cambio a partir de aquí
            link['titletag'] =linkList['title'];
           
            itemlist.append(
                Item(channel=item.channel,
                    action = "links",
                    title = '%(host)s - %(lang)s %(quality)s' % link,
                    url = qstr(link['url'].strip()),
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
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
   
    # Extrae las entradas (carpetas)
    url="http://series.ly/api/top.php?&format=json&id=1"
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
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
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    # Extrae las entradas (carpetas)
    url="http://series.ly/api/top.php?&format=json&id=2"
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
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    
    
    # Extrae las entradas (carpetas)
    url="http://series.ly/api/top.php?&format=json&id=3"
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
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    
    item.channel="seriesly"
    
    res = search_series(auth_token, user_token, item, texto)
    res.extend(search_films(auth_token, user_token, item, texto))
    
    return res
    
def search_series(auth_token, user_token, item, texto):
    logger.info("[seriesly.py] search")
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
    post = 'auth_token=%s' % ( qstr(auth_token) )
    
    url = 'http://series.ly/api/search.php?search=%s&type=serie&format=json' % ( qstr(texto) )
    
    # Extrae las entradas (carpetas)
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
    
    # Obtiene de nuevo los tokens
    auth_token, user_token, logged, loginmessage = getCredentials()
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
        import json
        json_data = json.loads(data, object_hook=to_utf8)
        return json_data
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line ) 

''' URLEncode a string '''
def qstr(string):
    return string # urllib2.quote(string)   

def perform_login():

    LOGIN = config.get_setting("serieslyuser")
    PASSWORD = config.get_setting("serieslypassword")

    # AuthToken
    url = "http://series.ly/api/auth.php?api=8&secret=N5X54c4OeDUwU8dWBbMW"
    data = scrapertools.cache_page(url)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    auth_token = data.strip()
    
    # UserToken
    url = "http://series.ly/scripts/login/login.php"
    post = "lg_login=%s&lg_pass=%s&callback_url=no&auth_token=%s&autologin=" % ( qstr(LOGIN), qstr(PASSWORD), qstr(auth_token) )
    data = scrapertools.cache_page(url,post=post)
    logger.info("****")
    logger.info(data)
    logger.info("****")
    user_token=data.strip()
    
    return [auth_token,user_token]