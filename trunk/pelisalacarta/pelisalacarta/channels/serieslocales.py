# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Series locales
# by @Chumy
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import scrapertools
from servers import servertools
from core import logger
from core import buscador
from core.item import Item
import os.path
import fnmatch
from core import DecryptYonkis as Yonkis

CHANNELNAME = "Series"
DEBUG = True
DIRNAME = config.get_setting("xbmc.library.path")
EXT = '*.strm'

def isGeneric():
    return True

def mainlist(item):
    logger.info("[series.py] getmainlist")

    itemlist = []
    # Listar entradas y meterlas en "files"
    files = os.listdir(DIRNAME)
    for f in files:
    # Si es un directorio
      if (os.path.isdir(os.path.join(DIRNAME, f))):
        itemlist.append( Item(channel=CHANNELNAME, title=f     , action="listpelisincaratula", url=f, folder=True) )
    return itemlist
    

def sortedlistdir(d, cmpfunc=cmp):
    l = os.listdir(d)
    l.sort(cmpfunc)
    return l

def getParam(contenido,param):
  contenido = contenido.split(param + "=")
  contenido = contenido[1].split("&")
  return contenido[0]

def listpelisincaratula(item):
    logger.info("[series.py] listpelisincaratula")

    url = item.url

    # Extrae las entradas
    itemlist = []
    seriepath = os.path.join(DIRNAME,url)
    logger.info(seriepath);
    
    matches = sortedlistdir(seriepath)
    for match in matches:
    # Si es un directorio
      if (os.path.isfile(os.path.join(seriepath, match))):
        if fnmatch.fnmatch(match, EXT):
          fileHandle = open ( os.path.join(seriepath, match) )
          contenido = fileHandle.readline()
          fileHandle.close()
          #Arreglamos la url
          contenido = urllib.unquote(contenido)
          
          nombre = getParam(contenido,"title").replace("+"," ")
          # Arreglamos la codificacion del titulo
          try:
              scrapedtitle = unicode( nombre, "utf-8" ).encode("iso-8859-1")
          except:
              scrapedtitle = nombre
          canal = getParam(contenido,"channel")
          urlFile = getParam(contenido,"url")
          servidor = getParam(contenido,"server")
          print urlFile
          #Anexamos el capitulo
          itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle    , action=canal, url=urlFile, server=servidor, folder=True ) )
    return itemlist
    
def seriesyonkis(item):
    logger.info("[series.py] findvideos")
    itemlist = []
    canal = item.channel
    servidor = item.server
    titulo = item.title
    servidor = item.server
    
    data = scrapertools.cachePage(item.url)
    
    patronvideos = 'href="http://www.seriesyonkis.com/player/visor_([^\.]+).php?(.*?)id=([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)==0:
        print "No hay videos"
        return ""
    else:
        #Solo lo pruebo con megavideo
        for match in matches:
            if match[0] in ["pymeno2","pymeno3","pymeno4","pymeno5","pymeno6"]:
              id = match[2]
              print "original " + id
              logger.info("[seriesyonkis.py]  id="+id)
              dec = Yonkis.DecryptYonkis()
              id = dec.decryptID_series(dec.unescape(id))
              print "decodificada " + id
              #Anexamos el capitulo
              itemlist.append( Item(channel=item.channel, title=item.server   , action="play", url=id , server=item.server, folder=True ) )

    return itemlist