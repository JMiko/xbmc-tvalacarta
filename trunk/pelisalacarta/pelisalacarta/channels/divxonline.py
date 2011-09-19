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

from servers import servertools
from core import scrapertools
from core import config
from core import logger
from core.item import Item

#from pelisalacarta import buscador

CHANNELNAME = "divxonline"

DEBUG = True
Generate = False # poner a true para generar listas de peliculas
Notas = False # indica si hay que añadir la nota a las películas
LoadThumbs = True # indica si deben cargarse los carteles de las películas; en MacOSX cuelga a veces el XBMC

def isGeneric():
    return True

def mainlist(item):
    logger.info("[divxonline.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="novedades"     , title="Novedades",url="http://www.divxonline.info/"))
    itemlist.append( Item(channel=CHANNELNAME, action="megavideo"     , title="Películas en Megavideo",url="http://www.divxonline.info/"))
    itemlist.append( Item(channel=CHANNELNAME, action="pelisconficha" , title="Estrenos",url="http://www.divxonline.info/peliculas-estreno/1.html"))
    itemlist.append( Item(channel=CHANNELNAME, action="pelisporletra" , title="Películas de la A a la Z"))
    itemlist.append( Item(channel=CHANNELNAME, action="pelisporanio"  , title="Películas por año de estreno"))
    itemlist.append( Item(channel=CHANNELNAME, action="busqueda"      , title="Buscar"))
    return itemlist

def search(item):    
    buscador.listar_busquedas(item)

def searchresults(params,tecleado,category):
    logger.info("[divxonline.py] search")

    buscador.salvar_busquedas(params,tecleado,category)
    tecleado = tecleado.replace(" ", "+")
    #searchUrl = "http://documentalesatonline.loquenosecuenta.com/search/"+tecleado+"?feed=rss2&paged=1"
    busqueda(CHANNELNAME,tecleado,category)

def busqueda(item):
    logger.info("busqueda")
    tecleado = ""
    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return
    
    tecleado = tecleado.replace(" ", "+")
    data=scrapertools.cachePagePost("http://www.divxonline.info/buscador.html",'texto=' + tecleado + '&categoria=0&tipobusqueda=1&Buscador=Buscar')

    #logger.info(data)
    data=data[data.find('Se han encontrado un total de'):]
    
    #<li><a href="/pelicula/306/100-chicas-2000/">100 chicas (2000)</a></li>
    patronvideos  = '<li><a href="(.+?)">(.+?)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: 
        scrapertools.printMatches(matches)
    
    for match in matches:
        xbmctools.addnewfolder( CHANNELNAME , "findvideos" , category , match[1] , 'http://www.divxonline.info' + match[0] , 'scrapedthumbnail', 'scrapedplot' )
    
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def novedades(item):
    logger.info("[divxonline.py] novedades")
    itemlist=[]
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    '''
    <td class="contenido"><a href="/pelicula/8853/Conexion-Tequila-1998/"><img src="http://webs.ono.com/jeux/divxonline.info_conexiontequila.jpg" style="padding: 5px;"  border="0" width="150" height="200" align="left" alt="Conexión Tequila (1998)" title="Conexión Tequila (1998)" />
    <font color="#000000"><b>Género:</b></font> <a href="/peliculas/50/Accion-Megavideo/"><font color="#0066FF">Accion (Megavideo)</font></a><br />
    <b>Título:</b> <a href="/pelicula/8853/Conexion-Tequila-1998/"><font color="#0066FF"><b>Conexión Tequila (1998) - </b></font></a>
    <b>Director(es):</b> <a href="/director/2917/Robert-Towne/"><font color="#0066FF">Robert Towne </font></a>
    <b> - Año de estreno:</b><a href="/peliculas-anho/1998/1.html"><font color="#0066FF"> 1998</a></font> -
    <b>Autorizada:</b> <a href="/peliculas/Todos-los-publicos/1/"><font color="#0066FF"> Todos los publicos - </a></font>
    <b>Vista:</b><font color="#0066FF"> 1103 veces - </font><b>Colaborador(es):</b><font color="#0066FF"> jacinto</font><br /><BR><b>Sinopsis:</b> Nick y McKussic son amigos desde niños, pero ahora Nick es teniente de policía y McKussic el mejor traficante de drogas de la ciudad. Se prepara una operación de mil doscientos kilos de cocaína y la Brigada Antinarcóticos cree que McKussic va a coordinar la entrega.
    <a href="/pelicula/8853/Conexion-Tequila-1998/"> <font color="#0066FF">(leer más)</font></a><br><br>
    <a href="/pelicula/8853/Conexion-Tequila-1998/" style="font-weight: bold; font-size: 11pt">
    <img src="http://webs.ono.com/divx/imagenes/flecha.png" border="0"> <font size="3" color="#0066FF">Conexión Tequila (1998)</font></a></td>
    <td>
    '''
    patron  = '<td class="contenido"><a href="([^"]+)"><img src="([^"]+)".*?title="([^"]+)"[^>]+>.*?'
    patron += '<b>Sinopsis:</b>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[2]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción
        scrapedthumbnail = "" # = match[1]
        scrapedplot = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patron = '<a href="[^"]+" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: white[^>]+>[^<]+</a><a href="([^"]+)" style="border: 1px solid rgb(0, 51, 102); margin: 2px; padding: 2px; text-decoration: none; color: black[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!Página siguiente" , url=urlparse.urljoin(url,matches[0][0]) , folder=True) )

    return itemlist

def megavideo(item):
    logger.info("[divxonline.py] megavideo")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    patron = '<a href="(/peliculas.*?-megavideo/)">([^<]+)</a><br>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="movielist", title=match[1], url = urlparse.urljoin(item.url,match[0])))

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
        itemlist.append( Item(channel=CHANNELNAME, action="pelisconfichaB", title=str(letra), url = "http://www.divxonline.info/verpeliculas/"+str(letra)+"_pagina_1.html"))

    return itemlist

def pelisporanio(item):
    logger.info("[divxonline.py] pelisporanio")
    itemlist = []

    #for anio in range(2009,1915,-1):
    for anio in range(datetime.datetime.today().year,1915,-1):
        itemlist.append( Item(channel=CHANNELNAME, action="pelisconficha", title=str(anio), url = "http://www.divxonline.info/peliculas-anho/"+str(anio)+"/1.html"))

    return itemlist
    
def pelisconficha(item): # fichas en listados por año y en estrenos
    logger.info("[divxonline.py] pelisconficha")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    if(data.find('Películas del  año') > 0):
        ##data=data[data.find('<!-- MENU IZQUIERDO -->'):]
        data=data[data.find('Películas del  año'):]
    
    logger.info(data.find('<!-- MENU IZQUIERDO -->'))
    #logger.info(data)
    # Extrae las entradas
    patronvideos  = '<td class="contenido"><a href="(.*?)">' # link
    patronvideos += '<img src="(.*?)"' # cartel
    patronvideos += '.*?title="(.*?)"' # título
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[2])
        if (not Generate and Notas):
            score = anotador.getscore(match[2])
            if (score != ""):
                scrapedtitle += " " + score

        scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción
        scrapedthumbnail = ""
        if LoadThumbs:
            scrapedthumbnail = match[1]
        scrapedplot = "" #match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # añade siguiente página
    match = re.search('(.*?)(\d+?)(\.html)',url)
    logger.info("url="+url)
    pag = match.group(2)
    newpag = match.group(1) + str(int(pag)+1) + match.group(3)
    logger.info("newpag="+newpag)
    itemlist.append( Item(channel=CHANNELNAME, action="pelisconficha", title="Siguiente" , url=newpag , folder=True) )

    return itemlist

import time
def pelisconfichaB(item): # fichas con formato en entradas alfabéticas
    logger.info("[divxonline.py] pelisconfichaB")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    patronvideos  = '<td class="contenido"><img src="(.*?)"' # cartel
    patronvideos += '.*?alt="(.*?)"' # título
    patronvideos += '.*?<b>Sinopsis.*?<a href="(.*?)"' # url
        
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = unicode(match[1],"iso-8859-1").encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle) # 7.49 seg 
        if (not Generate and Notas):
            score = anotador.getscore(match[1])
            if (score != ""):
                scrapedtitle += " " + score
        scrapedurl = urlparse.urljoin(item.url,match[2]) # url de la ficha divxonline
        scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción
        scrapedthumbnail = ""
        if LoadThumbs:
            scrapedthumbnail = match[0]
        scrapedplot = "" # match[3]

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # añade siguiente página
    #
    patron = '<a href="([^"]+)" class="paginacion"[^>]+>\&gt\;\&gt\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        itemlist.extend( pelisconfichaB( Item(channel=CHANNELNAME, action="pelisconfichaB", title="Siguiente" , url=urlparse.urljoin(item.url,matches[0]) , folder=True) ) )

    return itemlist

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def movielist(item): # pelis sin ficha (en listados por género)
    logger.info("[divxonline.py] movielist")

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    data = stepinto(url,data,'Ver página:(.*?)</p>')

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
        scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
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
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if (Generate):
        f.close()

    return itemlist

def findvideos(item):
    logger.info("[divxonline.py] findvideos(%s)" % item.tostring())

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info("***********************************************************************************************************************")
    patron = "<title>([^<]+)</title>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        cadena = matches[0]
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~.<>"
        cadena = ''.join(c for c in cadena if c in validchars)
        logger.info(  cadena  )

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
    for item in itemlist:
        item.channel=channel=CHANNELNAME
    
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
