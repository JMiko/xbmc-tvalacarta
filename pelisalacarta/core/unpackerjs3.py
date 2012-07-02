# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Descifra el empaquetado javascript PACK de Dean Edwards
# No está bien probado, así que no garantizo que funcione aunque en los casos de este plugin va muy bien :)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os.path
import sys
import os

from core import scrapertools
from core import config
from core import logger

def unpackjs(texto):
    logger.info("unpackjs")
    
    patron = "return p\}(.*?)\.split"
    matches = re.compile(patron,re.DOTALL).findall(texto)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        data = matches[0]
        logger.info("[unpackerjs3.py] bloque funcion="+data)
    else:
        return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    cifrado = matches[0][0]
    logger.info("[unpackerjs.py] cifrado="+cifrado)
    logger.info("[unpackerjs.py] palabras="+matches[0][1])
    descifrado = ""
    
    # Crea el dicionario con la tabla de conversion
    claves = []
    claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    claves.extend(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        logger.info(claves[i]+"="+palabra)
        i=i+1

    # Sustituye las palabras de la tabla de conversion
    # Obtenido de http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            logger.info("[unpackerjs.py] Error al encontrar la clave "+match.group(0))
            return ""

    #lista = map(re.escape, diccionario)
    # Invierte las claves, para que tengan prioridad las más largas
    claves.reverse()
    cadenapatron = '|'.join(claves)
    #logger.info("[unpackerjs.py] cadenapatron="+cadenapatron)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)
    logger.info("descifrado="+descifrado);
    descifrado = descifrado.replace("\\","")
    logger.info("descifrado="+descifrado);

    return descifrado
