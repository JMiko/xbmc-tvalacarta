# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,reimport os, sys

from core import loggerfrom core import configfrom core import scrapertoolsfrom core.item import Itemfrom servers import servertools
__channel__ = "hispantv"
__category__ = "F"
__type__ = "generic"
__title__ = "hispantv"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://www.dw.de/cssi/dwlogo-print.gif"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):    logger.info("[hispantv.py] mainlist")        # Descarga la página    data = scrapertools.cachePage("http://217.218.67.151/programs.aspx")    #<a href='section.aspx?id=351010509'><img src='images/prog_logos/351010509.jpg' /><div class='title'>Al-Ándalus</div>    patron = '<a href=\'([^"]+)\'><img src=\'([^"]+)\' /><div class=\'title\'>(.*?)</div>'    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)	    itemlist = []    for match in matches:        scrapedtitle = scrapertools.htmlclean(match[2])        scrapedthumbnail = 'http://217.218.67.151/'+match[1]        scrapedurl   = 'http://217.218.67.151/'+match[0]        itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,  folder=True))    return itemlistdef videos(item):    logger.info("[hispantv.py] episodios")    # Descarga la página    data = scrapertools.cachePage(item.url)    data = data.replace("\n", " ")    data = data.replace("\r", " ")    logger.info(data)    #<a href='/detail/2012/08/25/192620/al-ndalus-parte-34-hispantv'>Al-Ándalus - Granada, el último Reino Nazarí</a></div><img src='http://www.hispantv.ir/sp_photo/20120818/Al Andalus P33.jpg' /></a></div>    #<a href='/detail/2012/09/01/193426/al-ndalus---la-alhambra---parte-35'>Al-Ándalus - La Alhambra</a></div><div class='sectionDatetime'>01/09/2012 06:09</div>    patron = "<div class='sectionTitle'><a href='(.*?)'>(.*?)</a>"    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)	    itemlist = []    for match in matches:        scrapedurl   = 'http://217.218.67.151'+match[0]        scrapedtitle = scrapertools.htmlclean(match[1])        scrapedthumbnail = '' #match[3]        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, folder=False) )            return itemlistdef play(item):    logger.info("[hispantv.py] play")        data = scrapertools.cachePage(item.url)	    logger.info(data)    itemlist = []        #'file', 'http://www.hispantv.ir/video/20120825/al_andalus_p34_(granada,_el_ultimo_reino_nazari).flv'    patron = "'file', '(.*?)'"    matches = re.compile(patron,re.DOTALL).findall(data)    if DEBUG: scrapertools.printMatches(matches)    for match in matches:        scrapedurl = match        itemlist.append( Item(channel=__channel__, action="play",  server="directo",  title=item.title, url=scrapedurl, folder=False))    return itemlist