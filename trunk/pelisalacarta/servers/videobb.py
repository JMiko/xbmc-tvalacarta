# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,re
import base64

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videobb.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Obtiene el id
    code = Extract_id(page_url)
    if code == "":
        return []

    # Descarga el json con los detalles del vídeo
    controluri = "http://videobb.com/player_control/settings.php?v=%s&fv=v1.1.58"  %code
    datajson = scrapertools.cachePage(controluri)
    logger.info("response="+datajson);

    # Convierte el json en un diccionario
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    
    # Formatos
    formatos = datadict["settings"]["res"]

    cipher = datadict["settings"]["video_details"]["sece2"]
    logger.info("cipher="+cipher);
    
    keyTwo = str(datadict["settings"]["config"]["rkts"])
    logger.info("keyTwo="+keyTwo);

    c = decrypt32byte(cipher, int(keyTwo), int(base64.decodestring("MjI2NTkz")));
    
    for formato in formatos:
        uri = base64.decodestring(formato["u"]) + "&c="+c+"&start=0"
        resolucion = formato["l"]
    
        video_urls.append( ["%s [videobb]" % resolucion , uri ])

    for video_url in video_urls:
        logger.info("[videobb.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def Extract_id(url):
    # Extract video id from URL
    patron = "http\://www.videobb.com/watch_video.php\?v=([a-zA-Z0-9]{12})"
    matches = re.compile(patron,re.DOTALL).findall(url)
    if len(matches)>0:
        return matches[0]
    else:
        _VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:(?:e/)|(?:video/))|(?:f/))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
        mobj = re.match(_VALID_URL, url)
        if mobj is None:
            logger.info('[videobb.py] ERROR: URL invalida: %s' % url)
            return ""
        else:        
            return mobj.group(2)
            
# Crypt routines ported from Java VideoBbCom.java from jDownloader
# Thank you .bismarck ;)

def convertBin2Str(s):
    # 11111111 -> FF
    BI = int(s, 2)
    dev = "%x" % BI
    return dev

def convertStr2Bin(s):
    # FF -> 11111111
    BI = int(s, 16)

    # Convierte a binario    
    result = ''
    if BI == 0: return '0'
    while BI > 0:
        result = str(BI % 2) + result
        BI = BI >> 1
    
    while len(result) < 256:
        result = "0" + result

    return result

def decrypt32byte(cipher, keyOne, keyTwo):
    '''
    int x = 0, y = 0, z = 0;
    '''
    x = 0; y = 0; z = 0
    
    '''
    final char[] C = convertStr2Bin(cipher).toCharArray();
    '''
    C = list(convertStr2Bin(cipher))
    
    '''
    final int[] B = new int[384];
    '''
    B = []
    
    '''
    final int[] A = new int[C.length];
    '''
    A = []

    '''
    int i = 0;
    for (final char c : C) {
        A[i++] = Character.digit(c, 10);
    }
    '''
    i = 0
    for i in range(0,len(C)):
        A.append( int(C[i],10) )
    
    '''
    i = 0;
    while (i < 384) {
        keyOne = (keyOne * 11 + 77213) % 81371;
        keyTwo = (keyTwo * 17 + 92717) % 192811;
        B[i] = (keyOne + keyTwo) % 128;
        i++;
    }
    '''
    i = 0
    while i<384:
        keyOne = (keyOne * 11 + 77213) % 81371
        keyTwo = (keyTwo * 17 + 92717) % 192811
        B.append( (keyOne + keyTwo) % 128 )
        i=i+1

    '''
    i = 256;
    while (i >= 0) {
        x = B[i];
        y = i % 128;
        z = A[x];
        A[x] = A[y];
        A[y] = z;
        i--;
    }
    '''
    i = 256
    while i >= 0:
        x = B[i]
        y = i % 128
        z = A[x]
        A[x] = A[y]
        A[y] = z
        i=i-1
    '''
    i = 0;
    while (i < 128) {
        A[i] = A[i] ^ B[i + 256] & 1;
        i++;
    }
    '''
    i = 0
    while i < 128:
        A[i] = A[i] ^ B[i + 256] & 1
        i=i+1

    '''
    i = 0;
    final StringBuilder sb = new StringBuilder();
    while (i < A.length) {
        sb.append(A[i]);
        i++;
    }
    '''
    i = 0
    result = ""
    while i < len(A):
        result = result + str(A[i])
        i = i + 1

    return convertBin2Str(result)

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = "(http\:\/\/(?:www\.)?videobb.com\/(?:(?:e/)|(?:(?:video/|f/)))?[a-zA-Z0-9]{12})"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "(http\://www.videobb.com/watch_video.php\?v=[a-zA-Z0-9]{12})"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve