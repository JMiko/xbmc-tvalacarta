# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Shurweb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "gnula"
__category__ = "F"
__type__ = "generic"
__title__ = "Gnula"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[gnula.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades" , action="peliculas" , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="A-Z"       , action="letras"    , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Años"      , action="anyos"     , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Generos"   , action="generos"   , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Paises"    , action="paises"    , url="http://gnula.biz/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"    , action="search"))
    return itemlist

def generos(item):
    logger.info("[gnula.py] generos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<strong>PELICULAS SELECCIONADAS POR  CATEGORIAS</strong>(.*?)</dd></dl>")
    #<a href="genero/accion/" title="Acción">Acción</a> | - | <a href="genero/adolescencia/" title="Adolescencia">Adolescencia</a> | - | <a href="genero/adopcion/" title="Adopción">Adopción</a> | - | <a href="genero/amistad/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/animacion/" title="Animacion">Animacion</a> | - | <a href="genero/animales/" title="Animales">Animales</a> | - | <a href="genero/artes marciales/" title="Artes Marciales">Artes Marciales</a> | - | <a href="genero/aventuras/" title="Aventuras">Aventuras</a> | - | <a href="genero/baile/" title="Baile">Baile</a> | - | <a href="genero/basado en hechos reales/" title="Basado en Hechos Reales">Basado en Hechos Reales</a> | - | <a href="genero/belico/" title="Belico">Belico</a> | - | <a href="genero/biografico/" title="Biografico">Biografico</a> | - | <a href="genero/bodas/" title="Bodas">Bodas</a> | - | <a href="genero/catastrofes/" title="Catastrofes">Catastrofes</a> | - | <a href="genero/ciencia ficcion/" title="Ciencia Ficcion">Ciencia Ficcion</a> | - | <a href="genero/cocina/" title="Cocina">Cocina</a> | - | <a href="genero/comedia/" title="Comedia">Comedia</a> | - | <a href="genero/comic/" title="Comic">Comic</a> | - | <a href="genero/deporte/" title="Deporte">Deporte</a> | - | <a href="genero/discapacidad/" title="Discapacidad">Discapacidad</a> | - | <a href="genero/documental/" title="Documental">Documental</a> | - | <a href="genero/drama/" title="Drama">Drama</a> | - | <a href="genero/espionaje/" title="Espionaje">Espionaje</a> | - | <a href="genero/extraterrestres/" title="Extraterrestres">Extraterrestres</a> | - | <a href="genero/familia/" title="Familia">Familia</a> | - | <a href="genero/fantastico/" title="Fantastico">Fantastico</a> | - | <a href="genero/futbol/" title="Futbol">Futbol</a> | - | <a href="genero/gore/" title="Gore">Gore</a> | - | <a href="genero/historico/" title="Historico">Historico</a> | - | <a href="genero/infancia/" title="Infancia">Infancia</a> | - | <a href="genero/inmigracion/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/intriga/" title="Intriga">Intriga</a> | - | <a href="genero/juego/" title="Juego">Juego</a> | - | <a href="genero/karate/" title="Karate">Karate</a> | - | <a href="genero/mafia/" title="Mafia">Mafia</a> | - | <a href="genero/medicina/" title="Medicina">Medicina</a> | - | <a href="genero/melodrama/" title="Melodrama">Melodrama</a> | - | <a href="genero/mitologia/" title="Mitologia">Mitologia</a> | - | <a href="genero/monstruos/" title="Monstruos">Monstruos</a> | - | <a href="genero/musica/" title="Musica">Musica</a> | - | <a href="genero/musical/" title="Musical">Musical</a> | - | <a href="genero/nazismo/" title="Nazismo">Nazismo</a> | - | <a href="genero/navidad/" title="Navidad">Navidad</a> | - | <a href="genero/parodia/" title="Parodia">Parodia</a> | - | <a href="genero/pesca/" title="Pesca">Pesca</a> | - | <a href="genero/piratas/" title="Piratas">Piratas</a> | - | <a href="genero/policiaco/" title="Policiaco">Policiaco</a> | - | <a href="genero/politica/" title="Politica">Politica</a> | - | <a href="genero/precuela/" title="Precuela">Precuela</a> | - | <a href="genero/prehistoria/" title="Prehistoria">Prehistoria</a> | - | <a href="genero/religion/" title="Religion">Religion</a> | - | <a href="genero/remake/" title="Remake">Remake</a> | - | <a href="genero/romance/" title="Romance">Romance</a> | - | <a href="genero/rugby/" title="Rugby">Rugby</a> | - | <a href="genero/samurais/" title="Samurais">Samurais</a> | - | <a href="genero/secuela/" title="Secuela">Secuela</a> | - | <a href="genero/slasher/" title="Slasher">Slasher</a> | - | <a href="genero/sobrenatural/" title="Sobrenatural">Sobrenatural</a> | - | <a href="genero/sport/" title="Sport">Sport</a> | - | <a href="genero/superheroes/" title="Superheroes">Superheroes</a> | - | <a href="genero/supervivencia/" title="Supervivencia">Supervivencia</a> | - | <a href="genero/surf/" title="Surf">Surf</a> | - | <a href="genero/suspenso/" title="Suspenso">Suspenso</a> | - | <a href="genero/terror/" title="Terror">Terror</a> | - | <a href="genero/thriller/" title="Thriller">Thriller</a> | - | <a href="genero/vampiros/" title="Vampiros">Vampiros</a> | - | <a href="genero/vejez/" title="Vejez">Vejez</a> | - | <a href="genero/videojuego/" title="Videojuego">Videojuego</a> | - | <a href="genero/zombis/" title="Zombis">Zombis</a> | - | <a href="genero/3-D/" title="3-D">3-D</a> | </dd></dl>
    logger.info("data="+data)
 
    patron = '<a href="(genero/[^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle =  title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def letras(item):
    logger.info("[gnula.py] letras")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<strong>PELICULAS SELECCIONADAS POR  ALFABETO </strong>(.*?)</dd></dl>")
    #<a href="genero/accion/" title="Acción">Acción</a> | - | <a href="genero/adolescencia/" title="Adolescencia">Adolescencia</a> | - | <a href="genero/adopcion/" title="Adopción">Adopción</a> | - | <a href="genero/amistad/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/animacion/" title="Animacion">Animacion</a> | - | <a href="genero/animales/" title="Animales">Animales</a> | - | <a href="genero/artes marciales/" title="Artes Marciales">Artes Marciales</a> | - | <a href="genero/aventuras/" title="Aventuras">Aventuras</a> | - | <a href="genero/baile/" title="Baile">Baile</a> | - | <a href="genero/basado en hechos reales/" title="Basado en Hechos Reales">Basado en Hechos Reales</a> | - | <a href="genero/belico/" title="Belico">Belico</a> | - | <a href="genero/biografico/" title="Biografico">Biografico</a> | - | <a href="genero/bodas/" title="Bodas">Bodas</a> | - | <a href="genero/catastrofes/" title="Catastrofes">Catastrofes</a> | - | <a href="genero/ciencia ficcion/" title="Ciencia Ficcion">Ciencia Ficcion</a> | - | <a href="genero/cocina/" title="Cocina">Cocina</a> | - | <a href="genero/comedia/" title="Comedia">Comedia</a> | - | <a href="genero/comic/" title="Comic">Comic</a> | - | <a href="genero/deporte/" title="Deporte">Deporte</a> | - | <a href="genero/discapacidad/" title="Discapacidad">Discapacidad</a> | - | <a href="genero/documental/" title="Documental">Documental</a> | - | <a href="genero/drama/" title="Drama">Drama</a> | - | <a href="genero/espionaje/" title="Espionaje">Espionaje</a> | - | <a href="genero/extraterrestres/" title="Extraterrestres">Extraterrestres</a> | - | <a href="genero/familia/" title="Familia">Familia</a> | - | <a href="genero/fantastico/" title="Fantastico">Fantastico</a> | - | <a href="genero/futbol/" title="Futbol">Futbol</a> | - | <a href="genero/gore/" title="Gore">Gore</a> | - | <a href="genero/historico/" title="Historico">Historico</a> | - | <a href="genero/infancia/" title="Infancia">Infancia</a> | - | <a href="genero/inmigracion/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/intriga/" title="Intriga">Intriga</a> | - | <a href="genero/juego/" title="Juego">Juego</a> | - | <a href="genero/karate/" title="Karate">Karate</a> | - | <a href="genero/mafia/" title="Mafia">Mafia</a> | - | <a href="genero/medicina/" title="Medicina">Medicina</a> | - | <a href="genero/melodrama/" title="Melodrama">Melodrama</a> | - | <a href="genero/mitologia/" title="Mitologia">Mitologia</a> | - | <a href="genero/monstruos/" title="Monstruos">Monstruos</a> | - | <a href="genero/musica/" title="Musica">Musica</a> | - | <a href="genero/musical/" title="Musical">Musical</a> | - | <a href="genero/nazismo/" title="Nazismo">Nazismo</a> | - | <a href="genero/navidad/" title="Navidad">Navidad</a> | - | <a href="genero/parodia/" title="Parodia">Parodia</a> | - | <a href="genero/pesca/" title="Pesca">Pesca</a> | - | <a href="genero/piratas/" title="Piratas">Piratas</a> | - | <a href="genero/policiaco/" title="Policiaco">Policiaco</a> | - | <a href="genero/politica/" title="Politica">Politica</a> | - | <a href="genero/precuela/" title="Precuela">Precuela</a> | - | <a href="genero/prehistoria/" title="Prehistoria">Prehistoria</a> | - | <a href="genero/religion/" title="Religion">Religion</a> | - | <a href="genero/remake/" title="Remake">Remake</a> | - | <a href="genero/romance/" title="Romance">Romance</a> | - | <a href="genero/rugby/" title="Rugby">Rugby</a> | - | <a href="genero/samurais/" title="Samurais">Samurais</a> | - | <a href="genero/secuela/" title="Secuela">Secuela</a> | - | <a href="genero/slasher/" title="Slasher">Slasher</a> | - | <a href="genero/sobrenatural/" title="Sobrenatural">Sobrenatural</a> | - | <a href="genero/sport/" title="Sport">Sport</a> | - | <a href="genero/superheroes/" title="Superheroes">Superheroes</a> | - | <a href="genero/supervivencia/" title="Supervivencia">Supervivencia</a> | - | <a href="genero/surf/" title="Surf">Surf</a> | - | <a href="genero/suspenso/" title="Suspenso">Suspenso</a> | - | <a href="genero/terror/" title="Terror">Terror</a> | - | <a href="genero/thriller/" title="Thriller">Thriller</a> | - | <a href="genero/vampiros/" title="Vampiros">Vampiros</a> | - | <a href="genero/vejez/" title="Vejez">Vejez</a> | - | <a href="genero/videojuego/" title="Videojuego">Videojuego</a> | - | <a href="genero/zombis/" title="Zombis">Zombis</a> | - | <a href="genero/3-D/" title="3-D">3-D</a> | </dd></dl>
    logger.info("data="+data)
 
    patron = '<a href="(letra/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle =  title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def anyos(item):
    logger.info("[gnula.py] anyos")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<strong> PELICULAS SELECCIONADAS POR  A.O</strong>(.*?)</dd></dl>")
    #<a href="genero/accion/" title="Acción">Acción</a> | - | <a href="genero/adolescencia/" title="Adolescencia">Adolescencia</a> | - | <a href="genero/adopcion/" title="Adopción">Adopción</a> | - | <a href="genero/amistad/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/animacion/" title="Animacion">Animacion</a> | - | <a href="genero/animales/" title="Animales">Animales</a> | - | <a href="genero/artes marciales/" title="Artes Marciales">Artes Marciales</a> | - | <a href="genero/aventuras/" title="Aventuras">Aventuras</a> | - | <a href="genero/baile/" title="Baile">Baile</a> | - | <a href="genero/basado en hechos reales/" title="Basado en Hechos Reales">Basado en Hechos Reales</a> | - | <a href="genero/belico/" title="Belico">Belico</a> | - | <a href="genero/biografico/" title="Biografico">Biografico</a> | - | <a href="genero/bodas/" title="Bodas">Bodas</a> | - | <a href="genero/catastrofes/" title="Catastrofes">Catastrofes</a> | - | <a href="genero/ciencia ficcion/" title="Ciencia Ficcion">Ciencia Ficcion</a> | - | <a href="genero/cocina/" title="Cocina">Cocina</a> | - | <a href="genero/comedia/" title="Comedia">Comedia</a> | - | <a href="genero/comic/" title="Comic">Comic</a> | - | <a href="genero/deporte/" title="Deporte">Deporte</a> | - | <a href="genero/discapacidad/" title="Discapacidad">Discapacidad</a> | - | <a href="genero/documental/" title="Documental">Documental</a> | - | <a href="genero/drama/" title="Drama">Drama</a> | - | <a href="genero/espionaje/" title="Espionaje">Espionaje</a> | - | <a href="genero/extraterrestres/" title="Extraterrestres">Extraterrestres</a> | - | <a href="genero/familia/" title="Familia">Familia</a> | - | <a href="genero/fantastico/" title="Fantastico">Fantastico</a> | - | <a href="genero/futbol/" title="Futbol">Futbol</a> | - | <a href="genero/gore/" title="Gore">Gore</a> | - | <a href="genero/historico/" title="Historico">Historico</a> | - | <a href="genero/infancia/" title="Infancia">Infancia</a> | - | <a href="genero/inmigracion/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/intriga/" title="Intriga">Intriga</a> | - | <a href="genero/juego/" title="Juego">Juego</a> | - | <a href="genero/karate/" title="Karate">Karate</a> | - | <a href="genero/mafia/" title="Mafia">Mafia</a> | - | <a href="genero/medicina/" title="Medicina">Medicina</a> | - | <a href="genero/melodrama/" title="Melodrama">Melodrama</a> | - | <a href="genero/mitologia/" title="Mitologia">Mitologia</a> | - | <a href="genero/monstruos/" title="Monstruos">Monstruos</a> | - | <a href="genero/musica/" title="Musica">Musica</a> | - | <a href="genero/musical/" title="Musical">Musical</a> | - | <a href="genero/nazismo/" title="Nazismo">Nazismo</a> | - | <a href="genero/navidad/" title="Navidad">Navidad</a> | - | <a href="genero/parodia/" title="Parodia">Parodia</a> | - | <a href="genero/pesca/" title="Pesca">Pesca</a> | - | <a href="genero/piratas/" title="Piratas">Piratas</a> | - | <a href="genero/policiaco/" title="Policiaco">Policiaco</a> | - | <a href="genero/politica/" title="Politica">Politica</a> | - | <a href="genero/precuela/" title="Precuela">Precuela</a> | - | <a href="genero/prehistoria/" title="Prehistoria">Prehistoria</a> | - | <a href="genero/religion/" title="Religion">Religion</a> | - | <a href="genero/remake/" title="Remake">Remake</a> | - | <a href="genero/romance/" title="Romance">Romance</a> | - | <a href="genero/rugby/" title="Rugby">Rugby</a> | - | <a href="genero/samurais/" title="Samurais">Samurais</a> | - | <a href="genero/secuela/" title="Secuela">Secuela</a> | - | <a href="genero/slasher/" title="Slasher">Slasher</a> | - | <a href="genero/sobrenatural/" title="Sobrenatural">Sobrenatural</a> | - | <a href="genero/sport/" title="Sport">Sport</a> | - | <a href="genero/superheroes/" title="Superheroes">Superheroes</a> | - | <a href="genero/supervivencia/" title="Supervivencia">Supervivencia</a> | - | <a href="genero/surf/" title="Surf">Surf</a> | - | <a href="genero/suspenso/" title="Suspenso">Suspenso</a> | - | <a href="genero/terror/" title="Terror">Terror</a> | - | <a href="genero/thriller/" title="Thriller">Thriller</a> | - | <a href="genero/vampiros/" title="Vampiros">Vampiros</a> | - | <a href="genero/vejez/" title="Vejez">Vejez</a> | - | <a href="genero/videojuego/" title="Videojuego">Videojuego</a> | - | <a href="genero/zombis/" title="Zombis">Zombis</a> | - | <a href="genero/3-D/" title="3-D">3-D</a> | </dd></dl>
    logger.info("data="+data)
 
    patron = '<a href="(ano/[^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle =  title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def paises(item):
    logger.info("[gnula.py] paises")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<strong>PELICULAS SELECCIONADAS POR  PAIS</strong>(.*?)</dd></dl>")
    #<a href="genero/accion/" title="Acción">Acción</a> | - | <a href="genero/adolescencia/" title="Adolescencia">Adolescencia</a> | - | <a href="genero/adopcion/" title="Adopción">Adopción</a> | - | <a href="genero/amistad/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/animacion/" title="Animacion">Animacion</a> | - | <a href="genero/animales/" title="Animales">Animales</a> | - | <a href="genero/artes marciales/" title="Artes Marciales">Artes Marciales</a> | - | <a href="genero/aventuras/" title="Aventuras">Aventuras</a> | - | <a href="genero/baile/" title="Baile">Baile</a> | - | <a href="genero/basado en hechos reales/" title="Basado en Hechos Reales">Basado en Hechos Reales</a> | - | <a href="genero/belico/" title="Belico">Belico</a> | - | <a href="genero/biografico/" title="Biografico">Biografico</a> | - | <a href="genero/bodas/" title="Bodas">Bodas</a> | - | <a href="genero/catastrofes/" title="Catastrofes">Catastrofes</a> | - | <a href="genero/ciencia ficcion/" title="Ciencia Ficcion">Ciencia Ficcion</a> | - | <a href="genero/cocina/" title="Cocina">Cocina</a> | - | <a href="genero/comedia/" title="Comedia">Comedia</a> | - | <a href="genero/comic/" title="Comic">Comic</a> | - | <a href="genero/deporte/" title="Deporte">Deporte</a> | - | <a href="genero/discapacidad/" title="Discapacidad">Discapacidad</a> | - | <a href="genero/documental/" title="Documental">Documental</a> | - | <a href="genero/drama/" title="Drama">Drama</a> | - | <a href="genero/espionaje/" title="Espionaje">Espionaje</a> | - | <a href="genero/extraterrestres/" title="Extraterrestres">Extraterrestres</a> | - | <a href="genero/familia/" title="Familia">Familia</a> | - | <a href="genero/fantastico/" title="Fantastico">Fantastico</a> | - | <a href="genero/futbol/" title="Futbol">Futbol</a> | - | <a href="genero/gore/" title="Gore">Gore</a> | - | <a href="genero/historico/" title="Historico">Historico</a> | - | <a href="genero/infancia/" title="Infancia">Infancia</a> | - | <a href="genero/inmigracion/" title="Dramaticas">Dramaticas</a> | - | <a href="genero/intriga/" title="Intriga">Intriga</a> | - | <a href="genero/juego/" title="Juego">Juego</a> | - | <a href="genero/karate/" title="Karate">Karate</a> | - | <a href="genero/mafia/" title="Mafia">Mafia</a> | - | <a href="genero/medicina/" title="Medicina">Medicina</a> | - | <a href="genero/melodrama/" title="Melodrama">Melodrama</a> | - | <a href="genero/mitologia/" title="Mitologia">Mitologia</a> | - | <a href="genero/monstruos/" title="Monstruos">Monstruos</a> | - | <a href="genero/musica/" title="Musica">Musica</a> | - | <a href="genero/musical/" title="Musical">Musical</a> | - | <a href="genero/nazismo/" title="Nazismo">Nazismo</a> | - | <a href="genero/navidad/" title="Navidad">Navidad</a> | - | <a href="genero/parodia/" title="Parodia">Parodia</a> | - | <a href="genero/pesca/" title="Pesca">Pesca</a> | - | <a href="genero/piratas/" title="Piratas">Piratas</a> | - | <a href="genero/policiaco/" title="Policiaco">Policiaco</a> | - | <a href="genero/politica/" title="Politica">Politica</a> | - | <a href="genero/precuela/" title="Precuela">Precuela</a> | - | <a href="genero/prehistoria/" title="Prehistoria">Prehistoria</a> | - | <a href="genero/religion/" title="Religion">Religion</a> | - | <a href="genero/remake/" title="Remake">Remake</a> | - | <a href="genero/romance/" title="Romance">Romance</a> | - | <a href="genero/rugby/" title="Rugby">Rugby</a> | - | <a href="genero/samurais/" title="Samurais">Samurais</a> | - | <a href="genero/secuela/" title="Secuela">Secuela</a> | - | <a href="genero/slasher/" title="Slasher">Slasher</a> | - | <a href="genero/sobrenatural/" title="Sobrenatural">Sobrenatural</a> | - | <a href="genero/sport/" title="Sport">Sport</a> | - | <a href="genero/superheroes/" title="Superheroes">Superheroes</a> | - | <a href="genero/supervivencia/" title="Supervivencia">Supervivencia</a> | - | <a href="genero/surf/" title="Surf">Surf</a> | - | <a href="genero/suspenso/" title="Suspenso">Suspenso</a> | - | <a href="genero/terror/" title="Terror">Terror</a> | - | <a href="genero/thriller/" title="Thriller">Thriller</a> | - | <a href="genero/vampiros/" title="Vampiros">Vampiros</a> | - | <a href="genero/vejez/" title="Vejez">Vejez</a> | - | <a href="genero/videojuego/" title="Videojuego">Videojuego</a> | - | <a href="genero/zombis/" title="Zombis">Zombis</a> | - | <a href="genero/3-D/" title="3-D">3-D</a> | </dd></dl>
    logger.info("data="+data)
 
    patron = '<a title="[^"]+" href="(pais/[^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for url,title in matches:
        scrapedtitle =  title
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = ""
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='peliculas', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle) )
    
    return itemlist

def peliculas(item,paginacion=True):
    logger.info("[gnula.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    patron  = '<li class="video">[^<]+'
    patron += '<a href="([^"]+)">[^<]+'
    patron += '<b class="icon"></b>[^<]+'
    patron += '<img alt="[^"]+" src="([^"]+)">[^<]+'
    patron += '<span class="tit">([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for url,thumbnail,title in matches:
        scrapedtitle =  title
        fulltitle = scrapedtitle
        scrapedplot = ""
        scrapedurl = urlparse.urljoin("http://gnula.biz/",url)
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='findvideos', title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", extra=scrapedtitle) )

    patron = "<span \"\">[^<]+</span><a href='([^']+)'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action='peliculas', title=">> Página siguiente" , url=urlparse.urljoin(item.url,match)) )

    return itemlist

def findvideos(item):
    logger.info("[gnula.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Ver en "+videoitem.server
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    data = scrapertools.get_match(data,'<TABLE class="episodes"(.*?)</TABLE>')
    
    '''
    <TABLE class="episodes" width="900" align="center">
    <THEAD> 
    <TR> 
    <TH class="episode-title-chapter" width="135">Enlace</TH>
    <TH class="episode-server-img" width="158" align="center">Servidor</TH>
    <TH width="8" align="center"></TH>
    <TH class="center" width="87" align="center">&nbsp;</TH>
    <TH class="center" width="110" align="center">Enlaces</TH>
    <TH class="center" width="199" align="center">Compartir</TH>
    <TH class="episode-subtitle" width="171" align="center">Suscribite</TH>
    </TR> 
    </THEAD>
    <TBODY>
    <TR bgColor="#e6e3e3">
    <TD align="left"><A style="text-decoration: none;" title="Wonder Pets Ollies Slumber Party" 
    href="pelicula/wonder-pets-ollies-slumber-party.html" target="_blank"><IMG 
    src="http://www.terra.com/img/ico2006/i_video.gif" width="26" height="22"><B><FONT color="#555555">Opcion 1</FONT></B></A></TD> 
    <TD align="center"><B>Vk</B></TD> 
    <TD align="left"></TD> 
    <TD class="center" align="center"></TD> 
    <TD class="center" align="center"><A class="verLink" title="Wonder Pets Ollies Slumber Party" 
    href="pelicula/wonder-pets-ollies-slumber-party.html" target="_blank"><IMG 
    align="middle" src="http://2.bp.blogspot.com/-jsypRsEs_0s/UI3Pxb29dEI/AAAAAAAAABQ/R7-uEPFFYpA/s1600/ver.jpg" width="100" height="26"></A>    </TD> 
    <TD class="episode-uploader" align="center">
    <div class="fb-like" data-href="http://gnula.biz/wonder-pets-ollies-slumber-party.html" data-send="true" data-layout="button_count" data-width="450" data-show-faces="true"></div>
    </TD> 
    <TD style="overflow: hidden;" class="center" align="center">  <div class="fb-subscribe" data-href="http://www.facebook.com/inf.stork" data-layout="button_count" data-show-faces="true" data-width="450"></div></TD> 
    </TR></TBODY>
    </TABLE> <BR></DIV>
    <TABLE border="0" cellSpacing="0" cellPadding="6" width="960">
    <TBODY>
    '''
    
    patron  = '<TR[^<]+'
    patron += '<TD[^<]+<A.*?href="([^"]+)"[^<]+<IMG\s+src="([^"]+)"[^<]+<B><FONT[^>]+>([^<]+)</FONT></B></A></TD>[^<]+'
    patron += '<TD[^<]+<B>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,thumbnail,title,servidor in matches:
        scrapedtitle = "Ver en "+servidor.lower()+" ("+title.lower()+")"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action='play', title=scrapedtitle , fulltitle=item.title , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    return itemlist

def play(item):
    logger.info("[gnula.py] play")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    i=1
    for videoitem in itemlist:
        videoitem.title = "Mirror %d%s" % (i,videoitem.title)
        videoitem.fulltitle = item.fulltitle
        videoitem.channel=channel=__channel__
        i=i+1

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = servertools.find_video_items( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien