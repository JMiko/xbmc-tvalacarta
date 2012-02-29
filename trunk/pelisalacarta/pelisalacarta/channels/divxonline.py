# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxonline
# ermanitu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from core import anotador
import base64
import datetime
import time

from servers import servertools
from core import scrapertools
from core import config
from core import logger
from core.item import Item

#from pelisalacarta import buscador

__channel__ = "divxonline"
__category__ = "F"
__type__ = "generic"
__title__ = "Divx Online"
__language__ = "ES"

DEBUG = config.get_setting("debug")

Generate = False # poner a true para generar listas de peliculas
Notas = False # indica si hay que añadir la nota a las películas
LoadThumbs = True # indica si deben cargarse los carteles de las películas; en MacOSX cuelga a veces el XBMC

def isGeneric():
    return True

def mainlist(item):
    logger.info("[divxonline.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas"     , title="Películas - Novedades",url="http://www.divxonline.info/"))
    #itemlist.append( Item(channel=__channel__, action="categorias"    , title="Películas - Categorías",url="http://www.divxonline.info/"))
    #itemlist.append( Item(channel=__channel__, action="peliculas"     , title="Películas - Estrenos",url="http://www.divxonline.info/peliculas-estreno/1.html"))
    #itemlist.append( Item(channel=__channel__, action="pelisporletra" , title="Películas - A-Z"))
    #itemlist.append( Item(channel=__channel__, action="pelisporanio"  , title="Películas - Por año de estreno"))
    #itemlist.append( Item(channel=__channel__, action="search"        , title="Buscar"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[divxonline.py] search")
    itemlist = []

    # Lanza la búsqueda
    data=scrapertools.cachePagePost("http://www.divxonline.info/buscador.html",'texto=' + texto + '&categoria=0&tipobusqueda=1&Buscador=Buscar')

    #logger.info(data)
    data=data[data.find('Se han encontrado un total de'):]
    
    #<li><a href="/pelicula/306/100-chicas-2000/">100 chicas (2000)</a></li>
    patronvideos  = '<li><a href="(.+?)">(.+?)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        scrapedurl = 'http://www.divxonline.info' + match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        data = scrapertools.cachePage(scrapedurl)
        patron  = '<td class="contenido"><center><h1>.+?<img src="([^"]+)".*?<b[^>]*?>Sinopsis:</b>([^<]+)<'
        ficha = re.compile(patron,re.DOTALL).findall(data)
        if len(ficha) > 0:
           scrapedthumbnail = ficha[0][0]
           scrapedplot = ficha[0][1]
        
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

        itemlist.append( Item(channel=__channel__, title = match[1], fulltitle=match[1], url=scrapedurl, action="findvideos", plot=scrapedplot, thumbnail=scrapedthumbnail ) )
    
    return itemlist

def peliculas(item):
    logger.info("[divxonline.py] peliculas")
    itemlist=[]
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    patron  = '<div class="ficha margen-inf1">[^<]+'
    patron += '<h2><a href="([^"]+)">([^<]+)</a></h2>[^<]+'
    patron += '<div class="foto-link">[^<]+'
    patron += '<img src="([^"]+)".*?'
    patron += '<li><span class="color_azul-ficha">Sinopsis:</span>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,title,thumbnail,plot in matches:
        # Titulo
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<a href="peliculas-online-divx-2.html" class="paginacion" style="color: #000000; background-color: #cad9ea;" class="paginacion" onmouseover="javascript:style.backgroundColor='#ececd9';" onmouseout="javascript:style.backgroundColor='#cad9ea';">&gt;&gt;</a>
    patron = '<a href="([^"]+)">&gt;&gt;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        itemlist.append( Item(channel=__channel__, action="peliculas", title="!Página siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True) )

    return itemlist

def peliculasb(item): # fichas con formato en entradas alfabéticas
    logger.info("[divxonline.py] peliculasb")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    patronvideos  = '<td class="contenido"><img src="(.*?)"' # cartel
    patronvideos += '.*?alt="(.*?)"' # título
    patronvideos += '.*?<b>Sinopsis(.*?)<a href="([^"]+)"' # url

    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = unicode(match[1],"iso-8859-1").encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle) # 7.49 seg 
        if (not Generate and Notas):
            score = anotador.getscore(match[1])
            if (score != ""):
                scrapedtitle += " " + score
        scrapedurl = urlparse.urljoin(item.url,match[3]) # url de la ficha divxonline
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción
        scrapedthumbnail = match[0]
        scrapedplot = scrapertools.htmlclean(match[2])

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # añade siguiente página
    #
    patron = '<a href="([^"]+)" class="paginacion"[^>]+>\&gt\;\&gt\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if len(matches)>0:
    #    itemlist.append( Item(channel=__channel__, action="peliculasb", title="!Página siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True) )
    if len(matches)>0:
        newitem = Item(channel=__channel__, action="peliculasb", title="!Página siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True)
        itemlist.extend( peliculasb(newitem) )

    return itemlist

def peliculasc(item):
    logger.info("[divxonline.py] peliculasc")
    itemlist=[]
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    patron  = '<td class="contenido"><a href="([^"]+)"><img src="([^"]+)".*?title="([^"]+)"[^>]+>.*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[2]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción
        scrapedthumbnail = match[1]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<a href="peliculas-online-divx-2.html" class="paginacion" style="color: #000000; background-color: #cad9ea;" class="paginacion" onmouseover="javascript:style.backgroundColor='#ececd9';" onmouseout="javascript:style.backgroundColor='#cad9ea';">&gt;&gt;</a>
    patron = '<a href="([^"]+)" class="paginacion" style="color[^>]+>\&gt\;\&gt\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        itemlist.append( Item(channel=__channel__, action="peliculasc", title="!Página siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True) )

    return itemlist

def categorias(item):
    logger.info("[divxonline.py] categorias")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron = '<a href="(/peliculas.*?-megavideo/)">([^<]+)</a><br>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="movielist", title=match[1], url = urlparse.urljoin(item.url,match[0])))

    return itemlist

def stepinto (url, data, pattern): # expand a page adding "next page" links given some pattern
    # Obtiene el trozo donde están los links a todas las páginas de la categoría
    match = re.search(pattern,data)
    trozo = match.group(1)
    #logger.info(trozo)

    # carga todas las paginas juntas para luego extraer las urls
    patronpaginas = '<a href="([^"]+)"'
    matches = re.compile(patronpaginas,re.DOTALL).findall(trozo)
    #scrapertools.printMatches(matches)
    res = ''
    for match in matches:
        urlpage = urlparse.urljoin(url,match)
        #logger.info(match)
        #logger.info(urlpage)
        res += scrapertools.cachePage(urlpage)
    return res

def pelisporletra(item):
    logger.info("[divxonline.py] pelisporletra")
    itemlist = []

    letras = "9ABCDEFGHIJKLMNÑOPQRSTUVWXYZ" # el 9 antes era 1, que curiosamente está mal en la web divxonline (no funciona en el navegador)
    for letra in letras:
        itemlist.append( Item(channel=__channel__, action="peliculasb", title=str(letra), url = "http://www.divxonline.info/verpeliculas/"+str(letra)+"_pagina_1.html"))

    return itemlist

def pelisporanio(item):
    logger.info("[divxonline.py] pelisporanio")
    itemlist = []

    #for anio in range(2009,1915,-1):
    for anio in range(datetime.datetime.today().year,1915,-1):
        itemlist.append( Item(channel=__channel__, action="peliculasc", title=str(anio), url = "http://www.divxonline.info/peliculas-anho/"+str(anio)+"/1.html"))

    return itemlist

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def movielist(item): # pelis sin ficha (en listados por género)
    logger.info("[divxonline.py] movielist")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    data = stepinto(item.url,data,'Ver página:(.*?)</p>')

    # Extrae las entradas (carpetas)
    patronvideos  = '<li><h2><a href="([^"]+?)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    if (Generate):
        f = open(config.DATA_PATH+'/films.tab', 'w') # fichero para obtener las notas

    for match in matches:
        # Titulo
        scrapedtitle = remove_html_tags(match[1])
        if (not Generate and Notas):
            score = anotador.getscore(remove_html_tags(match[1]))
            if (score != ""):
                scrapedtitle += " " + score

        # URL
        scrapedurl = urlparse.urljoin(item.url,match[0]) # url de la ficha divxonline
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

        # Thumbnail
        #scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedthumbnail = ""

        # procesa el resto
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        if (Generate):
            sanio = re.search('(.*?)\((.*?)\)',scrapedtitle)
            if (sanio): # si hay anio
                fareg = sanio.group(1) + "\t" + sanio.group(2) + "\t" + scrapedtitle
            else:
                fareg = scrapedtitle + "\t\t" + scrapedtitle
            f.write(fareg+"\n")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if (Generate):
        f.close()

    return itemlist

def findvideos(item):
    logger.info("[divxonline.py] findvideos(%s)" % item.tostring())
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url.replace("pelicula","pelicula-divx"))
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    patron  = '<td class="numMirror">[^<]+</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"[^>]+></a></td>[^<]+'
    patron += '<td class="uploaderParrilla">[^<]+</td>[^<]+'
    patron += '<td class="partesParrilla">([^<]+)</td>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,partes in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Ver online "+scrapedtitle + " ("+partes+" partes)"
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    # Descarga la página
    data = scrapertools.cachePage(item.url.replace("pelicula","descarga-directa"))
    patron = '<table class="parrillaDescargas">(.*?)</table>'
    data = scrapertools.get_match(data,patron)
    
    patron  = '<td class="numMirror">[^<]+</td>[^<]+'
    patron += '<td class="hostParrilla"><a target="_blank" href="([^"]+)"><img src="([^"]+)"[^>]+></a></td>[^<]+'
    patron += '<td class="uploaderParrilla">[^<]+</td>[^<]+'
    patron += '<td class="partesParrilla">([^<]+)</td>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url,thumbnail,partes in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedtitle = url
        try:
            scrapedtitle = scrapedtitle.split("/")[2]
        except:
            pass
        
        scrapedtitle = "Descarga directa "+scrapedtitle + " ("+partes+" partes)"
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=thumbnail , plot=item.plot , folder=False) )

    return itemlist

def play(item):
    logger.info("[divxonline.py] play")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)

    logger.info("***********************************************************************************************************************")
    patron  = "decodeBase64\('(.+?)'\)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        cadena = matches[0]
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~.<>"
        cadena = ''.join(c for c in cadena if c in validchars)
        logger.info(  cadena  )

    data=decryptinks(data);
    logger.info("***********************************************************************************************************************")
    logger.info(data)
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    logger.info("***********************************************************************************************************************")
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

def decryptinks(text):
    patronvideos  = "decodeBase64\('(.+?)'\)"
    matches = re.compile(patronvideos,re.DOTALL).findall(text)
    #string='yFA/B6/fgVeTFPS4NIqijSVtVUemN39H+e6EuYNxcNiHnCsZeU3W0iY29Fbye4GjyIrqXD9RTiVAU/gI7Pq7Qi1vnoRkLooganMExe36ySUofSME6cF5zgQPoQvnsRNQbp0owGrUZ0fx0EuMWghIg8PeCbyzW46jM/czf0neyBePLXvg6u0tYdvCHF7JdLLGpH20CWO6mX8bc2rDAz+bUNshJS/eHNhLCblzvrKbJcddzQRfOkyriWOTusBm3wDZ1kZMs2fEckZRMBvUIiQljZ0L1IV3wDkVQ9cbdDqEIHlWi/xmHtVsb4G+SAMpsBNpXJzfzle4IZaHWdt+GOsI+y1DiHdRJ9mizN0+mEUsIhGqgJMiIMzeFeSmRQ21PxDVXP0yLKcsX3IPfPlcIOGcAGXcpXLgchisgZoyej4aEk0MTsRFGto4kvGzHBAyFrsf+UfKZf4ZqYQmx1pFMl8A0CQbhAoOgKioUFNOASCSTpvNqwiL1aRJuYQo/MzOLjhTcwrTua5Cg50513LwRkC7BJcIsHKCuWvU3CyKKV5Iz1M4qB5C4dBISifGiaisjwmprQk4VWeLVmyba+lzpfDa7PjGs3Hh54cE6BoN4aJVqaUpLvbxJfd2A4ODlTrOQZmFa32dfZYEIpB5EejTqY6TU4AW3p9G+Kd4TNAjTE2KVfUIW5bhXSvEE5Gs8JCp1xxgPcwrSTVdqe+VsjhqKjihnMouWiXn5pQzv2DlsGzDB1jShTmdWvo9gv4kya16ZzBUalTPTXVVPlapL4OMIJgwXzGPkO+2mwjgdjF8jzaUjn3bowuDdMaix5xpfJmI5IlHAJYKL4T0oVBE+gMFJsUa09IuBMi48ARSa8hXDmGf9nCpcAJ8jCrBdtj0Apm3CgaNWwdhxJhGb5RCLenTvOwB81N7sbyuWI2XzlKdRuUddJgD+3YDFxh1/gkTFgPWyq4xMuEoiZGcVKvfXpIeIZR6JN7cX3kL1HYfJYyZUs6IsYqQOaOy+gjVVw6GgE25oBD9geh8cS5mx94XxIXmi/1KUcYztxx/+zPSihLJ404sVnaxQ2LfpM7QtUUFZnyz4olTEfdQXxaQPUzIbuceyGqJig1djjiGw5qAHYcQQ45gJC3Gs+bzo4xiIJQHSTvi1SP7b9Ge9bV9SjOJ5kt1Z4CZoehu9VYKc+PcUFwWVeWN2Xf+Xp8xf5txn6upEc0tiUbSsQCRkZmJVVJntibWDnq4MjeczapU/sBgsULj5h7+llwmaKgdTCAfOLqWWX69z7ncwXbg+Aws/t6W75nHeAMVbK+Xt+3zNgCQE8M='
    #logger.info(matches);
    result=base64.b64decode(matches[0])
    return(Procesa('cryptkey', result));

def Procesa (key, pt):
    j=0;
    i=0
    ct=''

    s = [255] * 257

    for i in range(0, 256):
            s[i] = i;
    for i in range(0, 256):
            j= ( j + s[i] + ord(key[i%len(key)]))%256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;

    i=0
    j=0
    for y in range(0, len(pt)):
            i = (i + 1) % 256;
            j = (j + s[i]) % 256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;
            ct += chr(ord(pt[y]) ^ s[(s[i] + s[j]) % 256]);
    return ct


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien