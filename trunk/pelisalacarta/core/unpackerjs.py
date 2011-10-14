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
    # Extrae el cuerpo de la funcion
    patron = "eval\(function\(p\,a\,c\,k\,e\,d\)\{[^\}]+\}(.*?)\.split\('\|'\)\)\)"
    matches = re.compile(patron,re.DOTALL).findall(texto)
    #scrapertools.printMatches(matches)
    
    # Separa el código de la tabla de conversion
    if len(matches)>0:
        data = matches[0]
        logger.info("[unpackerjs.py] bloque funcion="+data)
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
    claves = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"]
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
        return diccionario[match.group(0)]

    #lista = map(re.escape, diccionario)
    # Invierte las claves, para que tengan prioridad las más largas
    claves.reverse()
    cadenapatron = '|'.join(claves)
    #logger.info("[unpackerjs.py] cadenapatron="+cadenapatron)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    return descifrado
