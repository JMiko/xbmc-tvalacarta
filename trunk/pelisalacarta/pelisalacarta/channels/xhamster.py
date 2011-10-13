# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por boludiko
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "xhamster"
DEBUG = True

def isGeneric():
	return True

def mainlist(item):
	logger.info("[xhamster.py] mainlist")
	itemlist = []
	itemlist.append( Item(channel=CHANNELNAME, action="videos"      , title="Útimos videos" , url="http://www.xhamster.com/"))
	itemlist.append( Item(channel=CHANNELNAME, action="listcategorias"    , title="Listado Categorias"))
	itemlist.append( Item(channel=CHANNELNAME, action="search"    , title="Buscar", url="http://xhamster.com/search.php?q=%s&qcat=video"))
	return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[xhamster.py] search")
    itemlist=[]
    if item.url=="":
        item.url="http://xhamster.com/search.php?q=%s&qcat=video"
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % texto
    return buscar(item)

# SECCION ENCARGADA DE BUSCAR

def buscar(item):
	logger.info("[xhamster.py] buscar")
	itemlist = []
 	data = scrapertools.downloadpageWithoutCookies(item.url)

# EXTRAE EL PAGINADOR
#<a href='search.php?q=sexo&qcat=video&page=3' class='last'>Next</a></td></tr></table></div></td>
	patronvideos  = '<a href=\'([^\']+)\' class=\'last\'>Next</a></td></tr></table></div></td>'
	siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(siguiente)			
	if len(siguiente)>0:
		direccion=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] )
		paginador = Item(channel=CHANNELNAME, action="buscar" , title="!Pagina siguiente" , url=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] ), thumbnail="", plot="", show="!Página siguiente")
	else:
		paginador = None

 	matches = re.compile('<td valign="top" id="video_title">.*?<script type="text/javascript">', re.S).findall(data)
 	itemlist = []
 	for match in matches:
 		datos = re.compile('<a href="([^"]+)".*?<img src=\'([^\']+).*?alt="([^"]+)"/>.*?</a>', re.S).findall(match)		
 		for video in datos:
 			try:
 				scrapedtitle = unicode( video[2], "utf-8" ).encode("iso-8859-1")
 			except:
 				scrapedtitle = video[2]
 			scrapedurl = urlparse.urljoin( "http://www.xhamster.com" , video[0] )
 			scrapedthumbnail = video[1]
 			scrapedplot = ""
 			# Depuracion
 			logger.info(video[1])
 			if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
 			itemlist.append( Item(channel=CHANNELNAME, action="obtienedir" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))
 		
 	# METE PAGINADOR
	if paginador is not None:
		itemlist.append( paginador )

	return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
	
def listcategorias(item):
	logger.info("[xhamster.py] listcategorias")
	itemlist = []
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Amateur", url="http://xhamster.com/channels/new-amateur-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Anal"  , url="http://xhamster.com/channels/new-anal-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Asian"  , url="http://xhamster.com/channels/new-asian-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="BBW"  , url="http://xhamster.com/channels/new-bbw-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="BDSM"  , url="http://xhamster.com/channels/new-bdsm-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Beach"  , url="http://xhamster.com/channels/new-beach-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Big Boobs"  , url="http://xhamster.com/channels/new-big_boobs-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Bisexuals"  , url="http://xhamster.com/channels/new-bisexuals-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Black and Ebony"  , url="http://xhamster.com/channels/new-ebony-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Blowjobs"  , url="http://xhamster.com/channels/new-blowjobs-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="British"  , url="http://xhamster.com/channels/new-british-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Cartoons"  , url="http://xhamster.com/channels/new-cartoons-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Celebrities"  , url="http://xhamster.com/channels/new-celebs-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Cream Pie"  , url="http://xhamster.com/channels/new-creampie-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Cuckold"  , url="http://xhamster.com/channels/new-cuckold-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Cumshots"  , url="http://xhamster.com/channels/new-cumshots-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Female"  , url="http://xhamster.com/channels/new-female_choice-1.html"))
 	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Femdom"  , url="http://xhamster.com/channels/new-femdom-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Flashing"  , url="http://xhamster.com/channels/new-flashing-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="French"  , url="http://xhamster.com/channels/new-french-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Gays"  , url="http://xhamster.com/channels/new-gays-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="German"  , url="http://xhamster.com/channels/new-german-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Grannies"  , url="http://xhamster.com/channels/new-grannies-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Group Sex"  , url="http://xhamster.com/channels/new-group-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Hairy"  , url="http://xhamster.com/channels/new-hairy-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Handjobs"  , url="http://xhamster.com/channels/new-handjobs-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Hidden Cam"  , url="http://xhamster.com/channels/new-hidden-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Interracial"  , url="http://xhamster.com/channels/new-interracial-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Japanese"  , url="http://xhamster.com/channels/new-japanese-1.html"))
 	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Latin"  , url="http://xhamster.com/channels/new-latin-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Lesbians"  , url="http://xhamster.com/channels/new-lesbians-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Massage"  , url="http://xhamster.com/channels/new-massage-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Men"  , url="http://xhamster.com/channels/new-men-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Masturbation"  , url="http://xhamster.com/channels/new-masturbation-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Matures"  , url="http://xhamster.com/channels/new-matures-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="MILFs"  , url="http://xhamster.com/channels/new-milfs-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Old and Young"  , url="http://xhamster.com/channels/new-old_young-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Public Nudity"  , url="http://xhamster.com/channels/new-public-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Sex Toys"  , url="http://xhamster.com/channels/new-toys-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Shemales"  , url="http://xhamster.com/channels/new-shemales-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Stockings"  , url="http://xhamster.com/channels/new-stockings-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Squirting"  , url="http://xhamster.com/channels/new-squirting-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Swingers"  , url="http://xhamster.com/channels/new-swingers-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Teens"  , url="http://xhamster.com/channels/new-teens-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Upskirts"  , url="http://xhamster.com/channels/new-upskirts-1.htm"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Vintage"  , url="http://xhamster.com/channels/new-vintage-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Voyeur"  , url="http://xhamster.com/channels/new-voyeur-1.html"))
	itemlist.append( Item(channel=CHANNELNAME, action="videos" , title="Webcams"  , url="http://xhamster.com/channels/new-webcams-1.html"))
	return itemlist
	
# FUNCION ENCARGADA DE BUSCAR VIDEOS DENTRO DE CADA PAGINA.

def videos(item):

 	logger.info("[xhamster.py] videos")
 	data = scrapertools.cache_page(item.url)
 
 	# EXTRAE EL PAGINADOR
#<a href='/channels/new-bisexuals-3.html' class='last'>Next</a></td></tr></table></div></td>
	patronvideos  = '<a href=\'([^\']+)\' class=\'last\'>Next</a></td></tr></table></div></td>'
	siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(siguiente)			
	if len(siguiente)>0:
		direccion=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] )
		paginador = Item(channel=CHANNELNAME, action="videos" , title="!Pagina siguiente" , url=urlparse.urljoin( "http://www.xhamster.com" , siguiente[0] ), thumbnail="", plot="", show="!Página siguiente")
	else:
		paginador = None

	# EXTRAE LOS VIDEOS
 	#<table cellspacing="0" cellpadding="0" width="100%" border="0" valign="top"...<div id="footer">
 	matches = re.compile('<table cellspacing="0" cellpadding="0" width="100%" border="0" valign="top".*?<div id="footer">', re.S).findall(data)
 	itemlist = []
	for match in matches:
		datos = re.compile('<a href="([^"]+)".*?<img src=\'([^\']+).*?alt="([^"]+)"/>.*?</a>', re.S).findall(match)		
		for video in datos:
			try:
				scrapedtitle = unicode( video[2], "utf-8" ).encode("iso-8859-1")
			except:
				scrapedtitle = video[2]
			scrapedurl = urlparse.urljoin( "http://www.xhamster.com" , video[0] )		
			scrapedthumbnail = video[1]
			scrapedplot = ""
			# Depuracion
			logger.info(video[1])
			if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
			itemlist.append( Item(channel=CHANNELNAME, action="obtienedir" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, server="Directo"))

	# METE PAGINADOR
	if paginador is not None:
		itemlist.append( paginador )
	return itemlist
	
# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def obtienedir(item):
	logger.info("[xhamster.py] obtienedir")
	itemlist = []
	data = scrapertools.cachePage(item.url)
	patron = '\'file\': \'([^\']+)\','
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		dir = "http://xhamster.com/flv2/" + matches[0]	
		logger.info("url="+dir)
		itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , url=dir, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="Directo", folder=False))
	return itemlist
	
def play(params,dir,category):
	logger.info("[xhamster.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"
	data = scrapertools.cachePage(url)
	patron = '\'file\': \'([^\']+)\','
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		dir = "http://xhamster.com/flv2/" + matches[0]	
	logger.info("url="+dir)

	xbmctools.playvideo(CHANNELNAME,server,dir,category,title,thumbnail,plot)