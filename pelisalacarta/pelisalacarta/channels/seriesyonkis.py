# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

import xbmc
import xbmcgui
import xbmcplugin

from unicodedata import normalize

from core import DecryptYonkis as Yonkis
from core import config
from core import logger
from core import scrapertools
from core import xbmctools
from core import library

from servers import servertools

from pelisalacarta import buscador

CHANNELNAME = "seriesyonkis"
SERVER = {'pymeno2'   :'Megavideo' ,'pymeno3':'Megavideo','pymeno4':'Megavideo','pymeno5':'Megavideo','pymeno6':'Megavideo',
          'svueno'    :'Stagevu'   ,
          'movshare'   :'Movshare'  ,
          'videoweed' :'Videoweed' ,
          'veoh2'     :'Veoh'      ,
          'megaupload':'Megaupload',
          'pfflano'   :'Directo'   ,
          'descargar':'Megaupload',
          }

#xbmc.executebuiltin("Container.SetViewMode(57)")  #57=DVD Thumbs
#xbmc.executebuiltin("Container.SetViewMode(50)")  #50=full list
#xbmc.executebuiltin("Container.SetViewMode(51)")  #51=list
#xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
#xbmc.executebuiltin("Container.SetViewMode(54)")  #54=wide icons

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

logger.info("[seriesyonkis.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[seriesyonkis.py] mainlist")

    xbmctools.addnewfolder( CHANNELNAME , "lastepisodeslist" , category , "�ltimos cap�tulos","http://www.seriesyonkis.com/ultimos-capitulos.php","","")
    xbmctools.addnewfolder( CHANNELNAME , "listalfabetico"   , category , "Listado alfab�tico","","","")
    xbmctools.addnewfolder( CHANNELNAME , "alltvserieslist"  , category , "Listado completo de series","http://www.seriesyonkis.com/","","")
    xbmctools.addnewfolder( CHANNELNAME , "allcartoonslist"  , category , "Listado completo de dibujos animados","http://www.seriesyonkis.com/","","")
    xbmctools.addnewfolder( CHANNELNAME , "allanimelist"     , category , "Listado completo de anime","http://www.seriesyonkis.com/","","")
    xbmctools.addnewfolder( CHANNELNAME , "allminilist"      , category , "Listado completo de miniseries","http://www.seriesyonkis.com/","","")
    xbmctools.addnewfolder( CHANNELNAME , "search"           , category , "Buscar","","","")

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
    logger.info("[seriesyonkis.py] search")

    buscador.listar_busquedas(params,url,category)
    
def performsearch(texto):
    logger.info("[cine15.py] performsearch")
    url = "http://www.seriesyonkis.com/buscarSerie.php?s="+texto

    # Descarga la p�gina
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    patronvideos  = '<h2><li><a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)".*?'
    patronvideos += '<span[^>]+>(.*?)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    resultados = []

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[3]

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        resultados.append( [CHANNELNAME , "list" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
        
    return resultados

def searchresults(params,Url,category):
    logger.info("[seriesyonkis.py] searchresults")
    
    buscador.salvar_busquedas(params,Url,category)
    url = "http://www.seriesyonkis.com/buscarSerie.php?s="+Url.replace(" ", "+")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<h2><li><a href="http://www.seriesyonkis.com/serie/house/" title="House"><img height="84" src="http://images.seriesyonkis.com/images/house.jpg" alt="House" align="right" /><div align="left"><strong>House</strong></div></a></h2><span style="font-size: 0.7em">Descripci�n: <h2 align="center"><u><strong><a href="http://www.seriesyonkis.com/serie/house/" title="House">Dr House</a></strong></u></h2>
    #<center><a href='http://tienda.seriesyonkis.com/house.htm'><img src='http://images.seriesyonkis.com/tienda/dr-house.gif' /></a></center>
    #Serie de TV (2004-Actualidad). 5 Nominaciones a los premios Emmy / Serie sobre un antip�tico m�dico especializado en enfermedades infecciosas. Gregory House es, seguramente, el mejor medico del Hospital, pero su car�cter, rebeld�a y su honestidad con los pacientes y su equipo le hacen �nico. Prefiere evitar el contacto directo con los pacientes, le interesa por encima de todo la investigaci�n de las enfermedades. Adem�s de no cumplir las normas, se niega a ponerse la bata de m�dico. Es adicto a los calmantes y a las series de hospitales, �contradictorio? No, es House. (FILMAFFINITY)<br /></span><br /><br /><br /><br /></li>
    #<h2><li><a href="http://www.seriesyonkis.com/serie/dollhouse/" title="Dollhouse"><img 
    
    patronvideos  = '<h2><li><a href="([^"]+)" title="([^"]+)"><img.*?src="([^"]+)".*?'
    patronvideos += '<span[^>]+>(.*?)</span>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[3]
        
        Serie = scrapedtitle    # JUR-A�ade nombre serie para librer�a

        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("scrapedurl="+scrapedurl)
            logger.info("scrapedthumbnail="+scrapedthumbnail)
            logger.info("Serie="+Serie)

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "list" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot , Serie)

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):
    logger.info("[seriesyonkis.py] listalfabetico")

    itemlist = getlistalfabetico()
    
    for item in itemlist:
        xbmctools.addnewfolder(item.channel , item.action , category , item.title , item.url ,"","")

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def getlistalfabetico():
    logger.info("[seriesyonkis.py] getlistalfabetico")
    from core.item import Item
        
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="0-9", url="http://www.seriesyonkis.com/lista-series/listaSeriesNumeric.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="A"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesA.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="B"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesB.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="C"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesC.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="D"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesD.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="E"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesE.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="F"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesF.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="G"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesG.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="H"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesH.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="I"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesI.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="J"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesJ.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="K"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesK.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="L"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesL.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="M"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesM.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="N"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesN.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="O"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesO.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="P"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesP.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="Q"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesQ.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="R"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesR.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="S"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesS.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="T"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesT.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="U"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesU.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="V"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesV.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="W"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesW.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="X"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesX.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="Y"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesY.php"))
    itemlist.append( Item(channel=CHANNELNAME, action="listseriesthumbnails" , title="Z"  , url="http://www.seriesyonkis.com/lista-series/listaSeriesZ.php"))

    return itemlist

def listseriesthumbnails(params,url,category):
    logger.info("[seriesyonkis.py] listseriesthumbnails")
    
    title = urllib.unquote_plus( params.get("title") )

    from core.item import Item

    item = Item(channel=CHANNELNAME, title=title , url=url )
    itemlist = getlistseriesthumbnails(item)
    
    for item in itemlist:
        xbmctools.addnewfolder(item.channel , item.action , category , item.title , item.url , item.thumbnail, item.plot , item.extra)

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def getlistseriesthumbnails(item):
    logger.info("[seriesyonkis.py] listseriesthumbnails")
    
    from core.item import Item

    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<td><center><a href='http://www.seriesyonkis.com/serie/a-camara-super-lenta/' title='A c�mara s�per lenta'><img src='http://images.seriesyonkis.com/images/a-camara-super-lenta.jpg' alt='A c�mara s�per lenta'/><br />A c�mara s�per lenta</a></center></td>
    if 'Numeric' in item.url:
        patronvideos  = "<td><center><a href='([^']+)' title='([^']+)'><img src='([^']+)'.*?</td>"
        t=1
        h=0
    else:
        patronvideos  = "<td><center><a title='([^']+)' href='([^']+)'><img src='([^']+)'.*?</td>"
        t=0
        h=1
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[t]
        scrapedurl = match[h]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        Serie = scrapedtitle    # JUR-A�ade nombre serie para librer�a
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="list" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = Serie , show=item.show))

    return itemlist

def lastepisodeslist(params,url,category):
    logger.info("[seriesyonkis.py] lastepisodeslist")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<div class="ficha" style="background:url(http://images.seriesyonkis.com/images/house.jpg) #000000 center top no-repeat"><a href="http://www.seriesyonkis.com/capitulo/house/capitulo-01/44647/" title="(y 6x2) Broken">House - 6x01 - (y 6x2) Broken</a><br /><br /><img src="http://images.peliculasyonkis.com/images/tmegavideo.png" alt="Megavideo" style="vertical-align: middle;" /><img height="30" src="http://images.seriesyonkis.com/images/f/spanish.png" alt="Audio Espa�ol" title="Audio Espa�ol" style="vertical-align: middle;" /></div>
    #<div class="ficha" style="background:url(http://images.seriesyonkis.com/images/cinco-hermanos.jpg) #000000 center top no-repeat"><a href="http://www.seriesyonkis.com/capitulo/cinco-hermanos/capitulo-15/29162/" title="Capitulo 15">Cinco Hermanos - 3x15 - Capitulo 15</a><br /><br /><img src="http://images.peliculasyonkis.com/
    
    patronvideos  = '<div class="ficha" style="background:url\(([^\)]+)\)[^>]+><a.*?href="([^"]+)".*?>([^<]+)</a>(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        esp=eng=latino=vos= ""
        if "Audio Espa\xc3\xb1ol" in match[3]:
            esp = "(Esp)"
        if "Subt\xc3\xadtulos en Espa\xc3\xb1ol" in match[3]:
            vos = "(V.O.S)"
        if "Audio Latino" in match[3]:
            latino = "(Latino)"
        if "Audio Ingl\xc3\xa9s" in match[2]:
            eng = "(Eng)"            
        scrapedtitle = "%s    %s%s%s%s" %(match[2],esp,vos,eng,latino)
        
        scrapedtitle2 = match[2]

        # URL
        scrapedurl = match[1]
        
        # Thumbnail
        scrapedthumbnail = match[0]
        
        # procesa el resto
        scrapedplot = ""

        #Serie - Trata de extraerla del t�tulo (no hay carpeta de serie aqu�)
        #Esto son pruebas "muy preliminares" esto puede dar problemas con series a�adidas completas
        try:
            Serie = scrapedtitle2[:scrapedtitle2.find("- ")-1]
        except:
            logger.info ("[seriesyonkis.py] ERROR extrayendo y limpiando nombre de serie de:"+scrapedtitle)
            Serie = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot ,Serie)

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def alltvserieslist(params,url,category):
    allserieslist(params,url,category,"series")

def allcartoonslist(params,url,category):
    allserieslist(params,url,category,"dibujos")

def allanimelist(params,url,category):
    allserieslist(params,url,category,"anime")

def allminilist(params,url,category):
    allserieslist(params,url,category,"miniseries")

def allserieslist(params,url,category,clave):
    logger.info("[seriesyonkis.py] allserieslist")

    title = urllib.unquote_plus( params.get("title") )

    from core.item import Item

    item = Item(channel=CHANNELNAME, title=title , url=url , extra=clave )
    itemlist = getallserieslist(item)
    
    for item in itemlist:
        xbmctools.addnewfolder(item.channel , item.action , category , item.title , item.url , item.thumbnail, item.plot , item.extra )#, totalItems = item.totalItems)

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def getallserieslist(item):
    logger.info("[seriesyonkis.py] getallserieslist")

    from core.item import Item

    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae el bloque de las series
    patronvideos = '<h4><a.*?id="'+item.extra+'".*?<ul>(.*?)</ul>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li class="page_item_"><a href="(http://www.seriesyonkis.com/serie[^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    totalItems = len(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        Serie = scrapedtitle    # JUR-A�ade nombre serie para librer�a
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="list" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = Serie , show = scrapedtitle ))#, totalItems = totalItems))

    return itemlist

def list(params,url,category):
    logger.info("[seriesyonkis.py] list")

    title = urllib.unquote_plus( params.get("title") )

    if params.has_key("Serie"):
        Serie = params.get("Serie")
    else:
        Serie = ""

    if params.has_key("thumbnail"):
        thumbnail = params.get("thumbnail")
    else:
        thumbnail = ""

    from core.item import Item

    item = Item(channel=CHANNELNAME, title=title , url=url , thumbnail=thumbnail )
    itemlist = getlist(item)
    
    # A�ade "Agregar todos a la librer�a"
    xbmctools.addnewvideo( CHANNELNAME , "addlist2Library" , category , "Megavideo", "A�ADIR TODOS LOS EPISODIOS A LA BIBLIOTECA" , url , thumbnail , "" , Serie)

    for item in itemlist:
        xbmctools.addnewvideo(item.channel , item.action , category , "Megavideo" , item.title , item.url , item.thumbnail, item.plot , Serie)

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def getlist(item):
    logger.info("[seriesyonkis.py] getlist")
    
    from core.item import Item
    itemlist = []
    
    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Busca la descripci�n
    patronvideos  = '<h3>Descripci.n.</h3>([^<]+)<'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedplot = matches[0]
    else:
        scrapedplot = item.plot
    
    # Busca el thumbnail
    patronvideos = '<div class="post">.*?<img.*?src="(http\:\/\/images.seriesyonkis[^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedthumbnail = matches[0]
    else:
        scrapedthumbnail = item.thumbnail

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="(http://www.seriesyonkis.com/capitulo[^"]+)"[^>]+>([^<]+)</a>(.*?)</h5></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        esp=eng=latino=vos= ""
        if "Audio Espa\xc3\xb1ol" in match[2]:
            esp = "(Esp)"
        if "Subt\xc3\xadtulos en Espa\xc3\xb1ol" in match[2]:
            vos = "(V.O.S)"
        if "Audio Latino" in match[2]:
            latino = "(Latino)"
        if "Audio Ingl\xc3\xa9s" in match[2]:
            eng = "(Eng)"    
        scrapedtitle = "%s    %s%s%s%s" %(match[1],esp,vos,eng,latino)
        scrapedurl = match[0]
        
        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="detail" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show = scrapedtitle, folder=False))

    return itemlist

def detail(params,url,category):
    logger.info("[seriesyonkis.py] detail")
    logger.info("[seriesyonkis.py] detail url="+url)

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    Serie = urllib.unquote_plus( params.get("Serie") )
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    #server = "Megavideo"
    server,url = scrapvideoURL(url) 
    logger.info("[seriesyonkis.py] detail url="+url)
   
    if (":" in url):
        match = url.split(":")
        if match[0]!="http":
            url = choiceOnePart(match)
    logger.info("[seriesyonkis.py] detail url="+url)

    if url == "":return
   
    logger.info("[seriesyonkis.py] url="+url)
   
    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot,Serie=Serie)
    # ------------------------------------------------------------------------------------

def addlist2Library(params,url,category):
    logger.info("[seriesyonkis.py] addlist2Library")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    if params.has_key("Serie"):
        Serie = params.get("Serie")
    else:
        Serie = ""

    if params.has_key("server"):
        server = params.get("server")
    else:
        server = ""

    if params.has_key("thumbnail"):
        thumbnail = params.get("thumbnail")
    else:
        thumbnail = ""

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="(http://www.seriesyonkis.com/capitulo[^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('pelisalacarta', 'A�adiendo episodios...')
    pDialog.update(0, 'A�adiendo episodio...')
    totalepisodes = len(matches)
    logger.info ("[seriesyonkis.py - addlist2Library] Total Episodios:"+str(totalepisodes))
    i = 0
    errores = 0
    nuevos = 0
    for match in matches:
        # Titulo
        scrapedtitle = match[1]

        # PARTE NUEVA 

        # Nos quedamos por un lado con el nombre de la serie y 
        # por otro con el num capitulo

        mo = re.match("^(.*) ([\d]{1,2}[x|X][\d]{1,3}) (.*)$", scrapedtitle)

        if mo == None:
                errores = errores + 1
                continue		

        if (DEBUG):
                xbmc.output("CAPITULO="+ mo.group(2))	            
	
	
        scrapedtitle = mo.group(2)

        # FIN PARTE NUEVA

        i = i + 1
        pDialog.update(i*100/totalepisodes, 'A�adiendo episodio...',scrapedtitle)
        if (pDialog.iscanceled()):
            return

        # URL
        #  Tenemos 2 opciones. Scrapear todos los episodios en el momento de a�adirlos 
        #  a la biblioteca o bien dejarlo para cuando se vea cada episodio. Esto segundo
        #  a�ade los episodios mucho m�s r�pido, pero implica a�adir una funci�n
        #  strm_detail en cada m�dulo de canal. Por el bien del rendimiento elijo la
        #  segunda opci�n de momento (hacer la primera es simplemente descomentar un par de
        #  l�neas.
        #  QUIZ� SEA BUENO PARAMETRIZARLO (PONER OPCI�N EN LA CONFIGURACI�N DEL PLUGIN)
        #  PARA DEJAR QUE EL USUARIO DECIDA DONDE Y CUANDO QUIERE ESPERAR.
        url = match [0]
        # JUR-Las 3 l�neas siguientes son para OPCI�N 1
        #scrapedurl = scrapvideoURL(url)
        #if scrapedurl == "":
        #    errores = errores + 1
            
        # Thumbnail
        scrapedthumbnail = ""
        
        # procesa el resto
        scrapedplot = ""
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
#            logger.info("scrapedurl="+scrapedurl) #OPCION 1.
            logger.info("url="+url) #OPCION 2.
            logger.info("scrapedthumbnail="+scrapedthumbnail)
            logger.info("Serie="+Serie)
            logger.info("Episodio "+str(i)+" de "+str(totalepisodes)+"("+str(i*100/totalepisodes)+"%)")

        # A�ade a la librer�a #Comentada la opci�n 2. Para cambiar invertir los comentarios
        #OPCION 1:
        #library.savelibrary(scrapedtitle,scrapedurl,scrapedthumbnail,server,scrapedplot,canal=CHANNELNAME,category="Series",Serie=Serie,verbose=False)
        #OPCION 2
        try:
            nuevos = nuevos + library.savelibrary(scrapedtitle,url,scrapedthumbnail,server,scrapedplot,canal=CHANNELNAME,category="Series",Serie=Serie,verbose=False,accion="strm_detail",pedirnombre=False)
        except IOError:
            logger.info("Error al grabar el archivo "+scrapedtitle)
            errores = errores + 1
        
#    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    pDialog.close()
    
    #Actualizaci�n de la biblioteca
    if errores > 0:
        logger.info ("[seriesyonkis.py - addlist2Library] No se pudo a�adir "+str(errores)+" episodios") 
    library.update(totalepisodes,errores,nuevos)

    return nuevos
    

def strm_detail (params,url,category):
    logger.info("[seriesyonkis.py] strm_detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    #server = "Megavideo"
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    server,url = scrapvideoURL(url)
    if url == "":
        
        return
    logger.info("[seriesyonkis] strm_detail url="+url)
    
    xbmctools.playvideo("STRM_Channel",server,url,category,title,thumbnail,plot,1)
#<td><div align="center"><span style="font-size: 10px"><em><img src="http://simages.peliculasyonkis.com/images/tmegavideo.png" alt="Megavideo" style="vertical-align: middle;" /><img src='http://images.peliculasyonkis.com/images/tdescargar2.png' title='Tiene descarga directa' alt='Tiene descarga directa' style='vertical-align: middle;' /><a onmouseover="window.status=''; return true;" onmouseout="window.status=''; return true;" title="Seleccionar esta visualizacion" href="http://www.seriesyonkis.com/player/visor_pymeno4.php?d=1&embed=no&id=%CB%D8%DC%DD%C0%D3%E2%FC&al=%A6%B2%AC%B8%AC%A4%BD%A4" target="peli">SELECCIONAR ESTA</a> (flash desde megavideo)</em>          </span></div></td>          <td><div align="center"><img height="30" src="http://simages.seriesyonkis.com/images/f/spanish.png" alt="Audio Espa�ol" title="Audio Espa�ol" style="vertical-align: middle;" /></div></td>
#          <td><div align="center"><span style="font-size: 10px">Espa�ol (Spanish)</span></div></td>          <td><div align="center"><span style="font-size: 10px">no</span></div></td>          <td><div align="center"><span style="font-size: 10px">Formato AVI 270mb</span></div></td>          <td><div align="center"><span style="font-size: 10px">MasGlo<br />masglo</span></div></td>        </tr><tr>
 

def scrapvideoURL(urlSY):
    logger.info("[seriesyonkis.py] scrapvideoURL")
    data = scrapertools.cachePage(urlSY)
    patronvideos  = 'href="http://www.seriesyonkis.com/go/(mv)\/([^"]+)".*?alt="([^"]+)".*?'
    patronvideos += '<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+'
    patronvideos += '<td><div[^>]+><[^>]+>(.*?)</tr>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    patronvideos  = 'href="http://www.seriesyonkis.com/player/visor_([^\.]+).php.*?id=([^"]+)".*?alt="([^"]+)".*?'
    patronvideos += '<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+'
    patronvideos += '<td><div[^>]+><[^>]+>(.*?)</tr>'
    matches0 = re.compile(patronvideos,re.DOTALL).findall(data)
    matches = matches + matches0
    patronvideos1  = 'http://www.seriesyonkis.com/go/(d)/(.+?)".*?alt="([^"]+)".*?'
    patronvideos1 += 'Durac.+?:\s?([^>]+?)>'
    matches1 = re.compile(patronvideos1,re.DOTALL).findall(data)
    if (len(matches1) > 0):
        for j in matches1:
            matches.append(j)
    scrapertools.printMatches(matches)
    id=""
    #newdec = Yonkis.DecryptYonkis()
    #xbmc.output(newdec.ccM(newdec.charting(newdec.unescape("%B7%AC%A6%B1%B7%AD%A9%B1"))))
    
    if len(matches)==0:
        xbmctools.alertnodisponible()
        return "",""
        
    elif len(matches)==1:
        if  matches[0][0] == "d":
            player = "descargar"
            url = "http://www.seriesyonkis.com/go/%s/%s" % (matches[0][0],matches[0][1])
            id = getId(url)
        elif matches[0][0] == "mv":
            player = "pymeno2"
            url = "http://www.seriesyonkis.com/go/%s/%s" % (matches[0][0],matches[0][1])
            id = getId(url)
        else:
            player = matches[0][0]
            id = matches[0][1]
        server = SERVER[player]
        #print matches[0][1]
        if player == "svueno":
            id = matches[0][1]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.decryptALT(dec.charting(dec.unescape(id)))
            id = "http://stagevu.com/video/" + id
        elif player in ["pymeno2","pymeno3","pymeno4","pymeno5","pymeno6"]:
            cortar = matches[0][1].split("&")
            id = cortar[0]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.decryptID_series(dec.unescape(id))
        
        elif player == "descargar":
            cortar = matches[0][1].split("&")
            id = cortar[0]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.ccM(dec.unescape(id))

        else:pass
        #print 'codigo :%s' %id
        return server,id        
    else:
        
        
            
        server,id = choiceOne(matches)
        if len(id)==0:return "",""
        print 'codigo :%s' %id
        return server,id
        
        
def choiceOne(matches):
    logger.info("[seriesyonkis.py] choiceOne")
    opciones = []
    IDlist = []
    servlist = []
    Nro = 0
    fmt=duracion=id=""
    
    for server,codigo,audio,data in matches:
        try:
            print server
            if server in SERVER:
                servidor = SERVER[server]
                player = server
                id = codigo
            else:
                if server == "d":
                    player = "descargar"
                    id = "http://www.seriesyonkis.com/go/%s/%s" % (server,codigo)
                    
                    servidor = "Megaupload"
                    Server = "megaupload"
                elif server == "mv":
                    player = "pymeno2"
                    id = "http://www.seriesyonkis.com/go/%s/%s" % (server,codigo)
                    
                    servidor = "Megavideo"
                    Server = "megavideo"
                else:
                    servidor = "desconocido ("+server+")"
            Nro = Nro + 1
            
            regexp = re.compile(r"title='([^']+)'")
            match = regexp.search(data)
            if match is not None:
                fmt = match.group(1)
                fmt = fmt.replace("Calidad","").strip()
            regexp = re.compile(r"Duraci\xc3\xb3n:([^<]+)<")
            match = regexp.search(data)
            if match is not None:
                duracion = match.group(1).replace(".",":")        
            audio = audio.replace("Subt\xc3\xadtulos en Espa\xc3\xb1ol","Subtitulado") 
            audio = audio.replace("Audio","").strip()
            opciones.append("%02d) [%s] - (%s) - %s  [%s] " % (Nro , audio,fmt,duracion,servidor))
            IDlist.append(id)
            servlist.append(player)
        except:
            logger.info("[seriesyonkis.py] error (%s)" % server)
    dia = xbmcgui.Dialog()
    seleccion = dia.select("N�)[AUDIO]-(CALIDAD)-DURACION", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 : return "",""
    
    if servlist[seleccion]  in ["pymeno2","pymeno3","pymeno4","pymeno5","pymeno6"]:
        if "http" in IDlist[seleccion]:
            id = getId(IDlist[seleccion])
        else:
            id = IDlist[seleccion]
        cortar = id.split("&")
        id = cortar[0]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        if(len(id)==51):                     
            id = dec.decryptID(dec.charting(dec.unescape(id)))
        else:
            id = dec.decryptID_series(dec.unescape(id))
    elif servlist[seleccion] == "descargar":
        if "http" in IDlist[seleccion]:
            id = getId(IDlist[seleccion])
        else:
            id = IDlist[seleccion]
        cortar = id.split("&")
        id = cortar[0]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.ccM(dec.unescape(id))        
    elif servlist[seleccion] == "svueno":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptALT(dec.charting(dec.unescape(id)))
        id = "http://stagevu.com/video/" + id
    elif servlist[seleccion] == "movshare":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptALT(dec.charting(dec.unescape(id)))
    elif servlist[seleccion] == "videoweed":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptID(dec.charting(dec.unescape(id)))
        id = "http://www.videoweed.com/file/%s" %id                
    else:
        pass
    return SERVER[servlist[seleccion]],id

def choiceOnePart(matches):
    logger.info("[seriesyonkis.py] choiceOnePart")
    opciones = []
    Nro = 0
    for codigo in matches:
        Nro = Nro + 1
        opciones.append("Parte %s " % Nro)
       
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Selecciona uno ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 : return ""
    id = matches[seleccion]
    return id
    
def getId(url):
    logger.info("[seriesyonkis.py] getId")

    #print url
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        opener = urllib2.build_opener(SmartRedirectHandler())
        response = opener.open(req)
    except ImportError, inst:    
        status,location=inst
        logger.info(str(status) + " " + location)    
        movielink = location
    #print movielink

    try:
        id = re.compile(r'id=([A-Z0-9%]{0,})').findall(movielink)[0]
    except:
        id = ""
    
    return id
    
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise ImportError(302,headers.getheader("Location"))