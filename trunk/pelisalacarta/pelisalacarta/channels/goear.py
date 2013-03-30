# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para goear
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "goear"
__category__ = "M"
__type__ = "xbmc"
__title__ = "goear"
__language__ = "ES"

DEBUG = config.get_setting("debug")

IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'goear' )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[goear.py] mainlist")

############################################## GENERA EL MENU PRINCIPAL###########################################################

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar Canciones"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por "Mas Escuchadas"'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por "Mejor Calidad"'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por "Mas Recientes"'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar PlayList"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar PlayList y ordenar por "Número de Canciones"'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar PlayList y ordenar por "Más Reciente"'     
    ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title="Mostrar los PlayList de un Usuario"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user_azul.png')))
    return itemlist
    
#################################################################################################################################


def search(item,texto):
    logger.info("[goear.py] search")
    try:
        
        if item.title=="Buscar Canciones":
            item.url = "http://www.goear.com/search/%s" % texto
            
        if item.title=='Buscar y ordenar por "Mas Escuchadas"':
            item.url = "http://www.goear.com/search/%s" % texto + "/0/played/"
            
        if item.title=='Buscar y ordenar por "Mas Recientes"':
            item.url = "http://www.goear.com/search/%s" % texto + "/0/recent/"    
                        
        if item.title=='Buscar y ordenar por "Mejor Calidad"':
            item.url = "http://www.goear.com/search/%s" % texto + "/0/quality/"
            
        if item.title=="Buscar PlayList":
            item.url = "http://www.goear.com/playlist-search/%s" % texto
        
        if item.title=='Buscar PlayList y ordenar por "Número de Canciones"':
            item.url = "http://www.goear.com/playlist-search/%s" % texto + "/0/size/"
            
        if item.title=='Buscar PlayList y ordenar por "Más Reciente"':
            item.url = "http://www.goear.com/playlist-search/%s" % texto + "/0/recent/"
            
        if item.title=='Mostrar los PlayList de un Usuario':
            item.url = "http://www.goear.com/%s" % texto + "/playlist/1"
            
        if item.title=="Buscar Canciones":
            return search_results(item)
            
        if item.title=='Buscar y ordenar por "Mas Escuchadas"':
            return search_results(item)
            
        if item.title=='Buscar y ordenar por "Mas Recientes"':
            return search_results(item)
                        
        if item.title=='Buscar y ordenar por "Mejor Calidad"':
            return search_playlist_results(item)
            
        if item.title=="Buscar PlayList":
            return search_playlist_results(item)
        
        if item.title=='Buscar PlayList y ordenar por "Número de Canciones"':
            return search_playlist_results(item)
            
        if item.title=='Buscar PlayList y ordenar por "Más Reciente"':
            return search_playlist_results(item)
            
        if item.title=='Mostrar los PlayList de un Usuario':
            return list_my_playlist(item)
        
 
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

#################################################################################################################################
#                                      BUSCA RESULTADOS PARA CANCIONES SUELTAS                                                  #
#################################################################################################################################

def search_results(item):
    logger.info("[goear.py] search_results")
    data = scrapertools.cachePage(item.url)
    patron = '<a title="([^"]+)" href="([^/]+/[^/]+)/[^"]+"><span class="songtitleinfo">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedtitle, scrapedurl in matches:
        # fabrica el link tipo http://www.goear.com/tracker758.php?f=My_ID de http://www.goear.com/listen/My_ID/blablabla 
        scrapedurl = scrapedurl.replace("listen/","http://www.goear.com/tracker758.php?f=")
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace("Escuchar","")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="play_cancion" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
   
   # EXTRAE EL TOTAL DE PAGINAS DE RESULTADOS
    patron = '<li><a class="radius_3" href="[^"]+">([^<]+)</a></li><!-- Última página'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedlastplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL NUMERO DE PAGINA ACTUAL
    patron = '<li class="active"><a class="radius_3" href="[^"]+">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedactiveplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL LINK DE LA SIGUIENTE PAGINA
    patron = '<li><a class="next" href="([^"]+)"><img alt="Siguiente"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = match
        scrapedurl = scrapedurl.replace("search","http://www.goear.com/search")
        scrapedtitle = "Pagina " +scrapedactiveplot+ " de " +scrapedlastplot
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="search_results" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
    return itemlist
    

###############################################################################################################################
#                                   EXTRAE EL LINK FINAL DEL MP3 Y LO REPRODUCE                                               #
###############################################################################################################################
def play_cancion(item):
    logger.info("[goear.py] play_cancion")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patronmp3  = '<song path="([^"]+)" bild="[^"]+" artist="[^"]+" title="([^"]+)"/>'
    matches = re.compile(patronmp3,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot))
    return itemlist
#################################################################################################################################    



#################################################################################################################################    
#################################################################################################################################    
#################################################################################################################################
#                                                    BLOQUE PLAYLIST                                                            #
#################################################################################################################################


def search_playlist_results(item):
    logger.info("[goear.py] search_playlist_results")
    data = scrapertools.cachePage(item.url)
    patron = '<a title="[^"]+" href="[^/]+/([^/]+)/[^"]+"><span class="song">(.*?)</p></li>'
    
    #<a title="Escuchar Mike Oldfield 01" href="playlist/0d9ead9/mike-oldfield-01"><span class="song">Mike Oldfield 01</span></span></a><p class="comment">Playlist con 12 canciones</p></li><li >
    #<a title="Escuchar Mike Oldfield" href="playlist/c1ad5c2/mike-oldfield"><span class="song">Mike Oldfield</span></span></a><p class="comment">Playlist con 1 canciones</p></li>          </ol><!-- los resultados se mostrarán de 10 en 10 -->
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedurl,scrapedtitle in matches:
        # fabrica el link tipo http://www.goear.com/apps/android/playlist_songs_json.php?v=d4f07b7
        scrapedurl =  "http://www.goear.com/apps/android/playlist_songs_json.php?v="+scrapedurl
        scrapedplot = ""
        scrapedtitle = scrapedtitle.replace("</span>","")
        scrapedtitle = scrapedtitle.replace("</a>","")
        scrapedtitle = scrapedtitle.replace('<p class="comment">'," - ")
        scrapedtitle = scrapedtitle
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="playlist_play" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
        
   
   # EXTRAE EL TOTAL DE PAGINAS DE RESULTADOS
    patron = '<li><a class="radius_3" href="[^"]+">([^<]+)</a></li><!-- Última página'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedlastplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL NUMERO DE PAGINA ACTUAL
    patron = '<li class="active"><a class="radius_3" href="[^"]+">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedactiveplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL LINK DE LA SIGUIENTE PAGINA
    patron = '<li><a class="next" href="([^"]+)"><img alt="Siguiente"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = match
        scrapedurl = scrapedurl.replace("playlist-search","http://www.goear.com/playlist-search")
        scrapedtitle = "Pagina " +scrapedactiveplot+ " de " +scrapedlastplot
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="search_playlist_results" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
    return itemlist



###############################################################################################################################
#                                  LEE EL NOMBRE DEL USUARIO Y MUESTRA SUS PLAYLIST                                           #
###############################################################################################################################


#def obtener_user_de_un_playlist(item):
#    logger.info("[goear.py] obtener_user_de_un_playlist")
#    data = scrapertools.cachePage(item.url)
#    patron = '<span class="user">([^<]+)</span>'
    #<span class="user">Yuneta</span>
#    matches = re.compile(patron,re.DOTALL).findall(data)
#    if DEBUG: scrapertools.printMatches(matches)
#    itemlist = []
#    for scrapedurl in matches:
        # fabrica el link tipo item.url = "http://www.goear.com/USUARIO/playlist/1"
#        scrapedurl = "http://www.goear.com/" + scrapedurl + "/playlist/1"
#        scrapedtitle = "hola"
#        scrapedplot=""
#        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
#        itemlist.append( Item(channel=__channel__, action="list_my_playlist" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
#    return itemlist



###############################################################################################################################
#                                LISTA los PLAYLIST DE un USUARIO     (UTILIZA API)                                           #
###############################################################################################################################

def list_my_playlist(item):
    logger.info("[goear.py] list_my_playlist")
    data = scrapertools.cachePage(item.url)
    patron = '<a href="http://www.goear.com/playlist/([^/]+)/([^/]+)/">[^<]+</a>.*?<span class="track">([^"]+)</span>.*?</li>'
    
    # <a href="http://www.goear.com/playlist/([^/]+)/([^/]+)/">[^<]+</a>.*?<span class="track">([^"]+)</span>.*?</li>
    #<li>
    #              <a href="http://www.goear.com/playlist/0afa804/peliculas/">peliculas</a>
    #              <span class="track">21 canciones</span>
    #                              </li>
                              
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedurl,scrapedtitle, scrapedplot in matches:
        # fabrica el link tipo http://www.goear.com/apps/android/playlist_songs_json.php?v=fdc5e49
        scrapedurl = "http://www.goear.com/apps/android/playlist_songs_json.php?v="+scrapedurl
        scrapedtitle = scrapedtitle + " - Playlist con " +scrapedplot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="playlist_play" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
   
   # EXTRAE EL TOTAL DE PAGINAS DE RESULTADOS
    patron = '<li><a class="radius_3" href="[^"]+">([^<]+)</a></li><!-- Última página'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedlastplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL NUMERO DE PAGINA ACTUAL
    patron = '<li class="active"><a class="radius_3" href="[^"]+">([^<]+)</a></li>'
              
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = ""
        scrapedtitle = ""
        scrapedthumbnail = ""
        scrapedactiveplot = match
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
   
   # EXTRAE EL LINK DE LA SIGUIENTE PAGINA
    #patron = '<li><a class="next" href="([^"]+)"><img alt="Siguiente"'
    patron = '<li class="active"><a class="radius_3" href="[^"]+">[^<]+</a></li><li><a class="radius_3" href="([^"]+)">[^<]+</a></li'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = match
        scrapedtitle = "Pagina " +scrapedactiveplot+ " de " +scrapedlastplot
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="list_my_playlist" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
    return itemlist


###############################################################################################################################
#                                   EXTRAE EL LINK DEL PLAYLIST Y LO REPRODUCE                                                #
###############################################################################################################################

#################################################################################################################################    

def playlist_play(item):
    logger.info("[goear.py] playlist_play")
    data = scrapertools.cachePage(item.url)
    patron = '"id":"[^"]+","title":"(.*?),"mp3path":"([^"]+)","imgpath"'
  
    #{"id":"053eee9","title":"DINASTIA","artist":"series tv","mp3path":"http:\/\/live3.goear.com\/listen\/ea2cc54efa02be506cf891c6890799a1\/51460ec2\/sst\/mp3files\/06082006\/78313386a704d28e8ac0c6a0bf1e7848.mp3","imgpath":"http:\/\/userserve-ak.last.fm\/serve\/_\/11714861\/Series+TV+mejoresseriesempire1.jpg","songtime":"1:17"},
            
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedtitle, scrapedurl in matches:
    
        scrapedurl = scrapedurl.replace("\\","")
        scrapedtitle = scrapedtitle.replace('","artist":"',' - ')
        scrapedtitle = scrapedtitle.replace('"',' ')
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedtitle = scrapedtitle
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot))
    return itemlist
    
        
# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false
    
    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = novedades(mainlist_items[0])
    
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien