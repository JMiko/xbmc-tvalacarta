# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para rtpa
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib
import os

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "rtpa"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtpa.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Más vistos" , url="http://www.rtpa.es/alacarta" , action="masvistos" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Más valorados" , url="http://www.rtpa.es/alacarta" , action="masvalorados" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Lo último" , url="http://www.rtpa.es/alacarta" , action="novedades" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , url="http://www.rtpa.es/alacarta" , action="programas" , folder=True) )

    return itemlist

def masvistos(item):
    logger.info("[rtpa.py] masvistos")

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="seccion">[^<]+<h3>M.aacute.s vistos</h3>.*?<ul class="videos">(.*?)</ul>')
    
    return get_videos(item,data)

def masvalorados(item):
    logger.info("[rtpa.py] masvalorados")

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="seccion">[^<]+<h3>M.aacute.s valorados</h3>.*?<ul class="videos">(.*?)</ul>')
    
    return get_videos(item,data)

def novedades(item):
    logger.info("[rtpa.py] novedades")

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="seccion">[^<]+<h3>Lo .uacute.ltimo</h3>.*?<ul class="videos">(.*?)</ul>')
    
    return get_videos(item,data)

def get_videos(item,data):
    logger.info("[rtpa.py] get_videos")
    itemlist = []
    patron  = '<li class="video"><a href="([^"]+)"><img[^<]+<img src="([^"]+)"[^<]+</a>(.*?)<img'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle.replace("</h4>"," ")).strip()
        title = unicode( title , "iso-8859-1" , errors="ignore").encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl).replace(" ","%20")
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , server="", action="play" , show = item.title , folder=False) )

    return itemlist

def programas(item):
    '''
    <div class="seccion programas">
    <h3>Nuestros programas</h3>
    <div id="nuestros_arriba">&nbsp;</div><div id="nuestros_central"><ul class="primera_columna"> <li> <a href="http://www.rtpa.es/programa:24x30_1274722527.html"> <p class="programa">24x30 [44]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Animalandia_1274866478.html"> <p class="programa">Animalandia [21]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Asturianos en el mundo_1277888777.html"> <p class="programa">Asturianos en el mundo [48]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Asturias en 25_1274778299.html"> <p class="programa">Asturias en 25 [118]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Caballos de metal_1347360906.html"> <p class="programa">Caballos de metal [5]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Camín _1274785780.html"> <p class="programa">Camín  [34]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Cañas y aparejos_1274785850.html"> <p class="programa">Cañas y aparejos [23]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Clave de fondo_1339149390.html"> <p class="programa">Clave de fondo [20]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Cocinado en Asturias_1291383874.html"> <p class="programa">Cocinado en Asturias [6]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Conexión Asturias_1274338341.html"> <p class="programa">Conexión Asturias [303]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Conexión Asturias Fin de semana_1274772892.html"> <p class="programa">Conexión Asturias Fin de semana [75]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:De folixa en folixa_1337344832.html"> <p class="programa">De folixa en folixa [20]</p> </a> </li>  <li> <a href="http://www.rtpa.es/programa:Debate en 30_1330605784.html"> <p class="programa">Debate en 30 [120]</p> </a> </li> </ul><ul class="segunda_columna"> <li> <a href="http://www.rtpa.es/programa:Documentales_1278053616.html">  <p class="programa">Documentales [34]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Dónde estabas cuándo..._1307104079.html">  <p class="programa">Dónde estabas cuándo... [7]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:El gusto es mío_1274777762.html">  <p class="programa">El gusto es mío [341]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:En el camino_1307104554.html">  <p class="programa">En el camino [45]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Ende_1339149690.html">  <p class="programa">Ende [13]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Especiales_1316522632.html">  <p class="programa">Especiales [8]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:La Mar de Asturias_1283777047.html">  <p class="programa">La Mar de Asturias [6]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:La Quintana de Pola_1329394981.html">  <p class="programa">La Quintana de Pola [123]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Los olvidados_1280988905.html">  <p class="programa">Los olvidados [11]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Mensaje del Presidente del Principado_1283258858.html">  <p class="programa">Mensaje del Presidente del Principado [1]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Mirasturies: el pasáu recién_1280215540.html">  <p class="programa">Mirasturies: el pasáu recién [68]</p></a> </li>  <li> <a href="http://www.rtpa.es/programa:Mochileros_1283778127.html">  <p class="programa">Mochileros [49]</p></a> </li> </ul><ul class="tercera_columna"> <li> <a href="http://www.rtpa.es/programa:Momentos contados_1283431950.html">  <p class="programa">Momentos contados [8]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Nos_1274945579.html">  <p class="programa">Nos [5]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Objetivo Asturias_1317382496.html">  <p class="programa">Objetivo Asturias [54]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Pieces_1274784299.html">  <p class="programa">Pieces [62]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Sección homicidios_1307104038.html">  <p class="programa">Sección homicidios [3]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Sentirse bien_1299226607.html">  <p class="programa">Sentirse bien [16]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Sones_1274865975.html">  <p class="programa">Sones [34]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:Tiende a infinito_1314951696.html">  <p class="programa">Tiende a infinito [5]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:TPA Noticias 1. Fin de semana _1274869775.html">  <p class="programa">TPA Noticias 1. Fin de semana  [5]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:TPA Noticias 2. Fin de semana _1274869971.html">  <p class="programa">TPA Noticias 2. Fin de semana  [5]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:TPA Noticias. Primera Edición_1274868140.html">  <p class="programa">TPA Noticias. Primera Edición [6]</p> </a></li>  <li> <a href="http://www.rtpa.es/programa:TPA Noticias. Segunda Edición_1274869001.html">  <p class="programa">TPA Noticias. Segunda Edición [6]</p> </a></li> </ul><div class="separador">&nbsp;</div></div><div id="nuestros_abajo">&nbsp;</div>                    
    <div class="separador"></div>
    </div>
    '''
    logger.info("[rtpa.py] programas")

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="seccion programas">[^<]+<h3>Nuestros programas</h3>(.*?)<div class="separador">')

    itemlist = []
    patron  = '<li[^<]+<a href="([^"]+)"[^<]+<p[^>]+>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        title = unicode( title , "iso-8859-1" , errors="ignore").encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl).replace(" ","%20")
        thumbnail = ""
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail , action="episodios" , show = item.title , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[rtpa.py] episodios")
    itemlist = []

    item.url = item.url.replace(" ","%20")
    data = scrapertools.cache_page(item.url)

    # Episodio actual
    try:
        title = scrapertools.get_match(data,'<div id="sobreElVideo">[^<]+<h3>([^<]+)</h3>')
    except:
        title = scrapertools.get_match(data,'<div id="sobreElVideo">[^<]+<h3[^<]+</h3>[^<]+<p[^<]+</p>[^<]+<h4 class="programa">([^<]+)</h4>')
        title = title + " " + scrapertools.get_match(data,'<div id="sobreElVideo">[^<]+<h3[^<]+</h3>[^<]+<p class="fecha">([^<]+)</p>')
    title = unicode( title , "iso-8859-1" , errors="ignore").encode("utf-8")
    url = scrapertools.get_match(data,"'file'\: '([^']+)'")
    thumbnail = scrapertools.get_match(data,"'image'\: '([^']+)'")
    thumbnail = urlparse.urljoin(item.url,thumbnail)
    itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail, server="directo", action="play" , show = item.title , folder=False) )

    # Los 4 anteriores
    #<li class="videos_programa"><h4><a href="http://www.rtpa.es/video:Asturianos en el mundo_551349134403.html">Noruega</a></h4>
    #<p class="programa"><a href="http://www.rtpa.es/video:Asturianos en el mundo_551349134403.html">Asturianos en el mundo</a></p>
    #<p><img src="imagesVOD/valoracion4.jpg" align="absmiddle" alt="Voraci�n de 4 estrellas" class="estrallas" />8 votos</p>
    #<p class="reproducciones">982 reproducciones</p><p class="fecha">01-10-2012</p><p class="duracion">60 min</p>
    data1 = scrapertools.get_match(data,'<div class="seccion"><h3>Los[^<]+</h3><ul class="videos">(.*?)</ul>')
    logger.info("data1="+data1)
    patron  = '<li[^<]+'
    patron += '<h4><a href="([^"]+)">([^<]+)</a></h4>'
    patron += '<p class="programa"><a[^<]+</a></p>'
    patron += '<p><img[^<]+</p>'
    patron += '<p[^<]+</p><p class="fecha">([^<]+)</p><p class="duracion">([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data1)
    for scrapedurl,scrapedtitle,fecha,duracion in matches:
        title = scrapedtitle.strip()+" ("+fecha+") ("+duracion+")"
        title = unicode( title , "iso-8859-1" , errors="ignore").encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl).replace(" ","%20")
        thumbnail = ""
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url, server="", thumbnail=thumbnail , action="play" , show = item.title , folder=False) )

    # Archivo
    try:
        url = scrapertools.get_match(data,'<a id="ver_mas_videos" href="([^"]+)">')
        url = urlparse.urljoin(item.url,url).replace(" ","%20")
    except:
        return itemlist
    
    data = scrapertools.cache_page(url)
    '''
    <li class="video"><div class="img_busqueda"><a href="http://www.rtpa.es/video:Asturianos en el mundo_551344899472.html">
    <img class="play" src="imagesVOD/play.png">
    <img src="fotos//12/05/871337343792_CabeceraAsturianosMundo2012.jpg" alt="Fotograma del v&iacute;deo" class="fotograma"/></div class="text_busqueda"></a><div class="text_busqueda"><p class="fecha">13-08-2012</p> <p class="programa">  </p> <p class="titulo">Minnesota</p></div></li>
    '''
    patron  = '<li class="video"><div class="img_busqueda"><a href="([^"]+)">[^<]+'
    patron += '<img[^<]+'
    patron += '<img src="([^"]+)"[^<]+</div class="text_busqueda"></a><div class="text_busqueda"><p class="fecha">([^<]+)</p[^<]+<p class="programa"[^<]+</p[^<]+<p class="titulo">([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl,scrapedthumbnail,fecha,scrapedtitle in matches:
        title = scrapedtitle.strip()+" ("+fecha+")"
        title = unicode( title , "iso-8859-1" , errors="ignore").encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl).replace(" ","%20")
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        itemlist.append( Item(channel=CHANNELNAME, title=title , url=url,  thumbnail=thumbnail, server="", action="play" , show = item.title , folder=False) )

    return itemlist

def play(item):
    logger.info("[rtpa.py] play")

    itemlist = []
    if item.server=="directo":
        itemlist.append(item)
    else:
        data = scrapertools.cache_page(item.url.replace(" ","%20"))
        #'file': 'http://rtpa.ondemand.flumotion.com/rtpa/ondemand/vod/27171_1.mp4',
        try:
            filepart = scrapertools.get_match(data,"'file'\: '([^']+)'")
            streamerpart =  scrapertools.get_match(data,"'streamer'\: '([^']+)'")
            url = streamerpart+filepart
        except:
            url = scrapertools.get_match(data,"'file'\: '([^']+)'")
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , server = "directo" , action="play" , url=url, thumbnail=item.thumbnail, folder=False) )

    return itemlist

def test():

    # Al entrar sale una lista de categorias
    categorias_items = mainlist(Item())
    if len(categorias_items)==0:
        print "No devuelve categorias"
        return False

    programas_items = programas(categorias_items[-1])
    if len(programas_items)==0:
        print "No devuelve programas en "+categorias_items[0]
        return False

    episodios_items = episodios(programas_items[0])
    if len(episodios_items)==1:
        print "No devuelve videos en "+programas_items[0].title
        return False

    return True