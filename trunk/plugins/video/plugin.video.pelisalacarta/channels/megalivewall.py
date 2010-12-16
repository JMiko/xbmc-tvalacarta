# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculashd
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools
import config
import logger
import megalive

CHANNELNAME = "megalivewall"
_VALID_URL = r'http\:\/\/www.megalive\.com/\?(?:s=.+?&(?:amp;)?)?((?:(?:v\=)))?([A-Z0-9]{8})'

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[megalivewall.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[megalivewall.py] mainlist")
	
	if url=="":
		url="http://www.megalive.com/"
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	patron = "flashvars.xmlurl = '([^']+)'"
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		xmlurl = urllib.unquote_plus(matches[0])
		#logger.info(data)
		#<image click_url="?v=7RJPHQN0" images="http://img6.megalive.com/f29efb78905a482f00dacb5f5e41e953.jpg^
		#http://img6.megalive.com/eecd5b9bda6035095ef672b7c5e6dd5a.jpg" description="Expansion Ixcan TV" time="" thumb="http://img6.megalive.com/568a3de4a6b15fddce5c0f9609334529.jpg" hq="1" icon="ml">
		# Extrae las entradas (carpetas)
		patron  = '<image click_url="\?v=([^"]+)".*?'
		patron += 'description="([^"]+)" time="" '
		patron += 'thumb="([^"]+)" '
		patron += 'hq="([^"]+)"'
		data = scrapertools.cachePage(xmlurl)
		matches = re.compile(patron,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)

		for match in matches:
			# Titulo
			scrapedtitle = decodeHtmlentities(match[1]).encode("utf-8")
			# URL
			scrapedurl = match[0]
			# Thumbnail
			scrapedthumbnail = match[2]
			# Argumento
			scrapedplot = ""
			if match[3]=="1":
				hq=" (HQ)"
			else:
				hq=""

			# Depuracion
			if (DEBUG):
				logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

			# Añade al listado de XBMC
			addnewvideo( CHANNELNAME , "play" , category ,"Directo", scrapedtitle+hq , scrapedurl , scrapedthumbnail , scrapedplot )





	xbmcplugin.setPluginCategory( handle=pluginhandle, category="Streaming Live" )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def play(params,url,category):
	
	icon = "DefaultVideo.png"
	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	livelink = megalive.getLiveUrl(url)
	if len(livelink)<=0:
		
		print "Error de conexion: "+livelink
		
	else:
		item=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumbnail, path=livelink)
		item.setInfo( type="Video",infoLabels={ "Title": title, "Plot": plot})
		
		xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ,Serie=""):
	if DEBUG:
		try:
			logger.info('[xbmctools.py] addnewvideo( "'+canal+'" , "'+accion+'" , "'+category+'" , "'+server+'" , "'+title+'" , "' + url + '" , "'+thumbnail+'" , "'+plot+'")" , "'+Serie+'")"')
			title = title.encode("utf-8")
		except:
			logger.info('[xbmctools.py] addnewvideo(<unicode>)')
	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : title, "Plot" : plot, "Studio" : canal } )
	listitem.setProperty('IsPlayable', 'true')
	
	itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s&Serie=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server , Serie)
	#logger.info("[xbmctools.py] itemurl=%s" % itemurl)
	xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem)

def decodeHtmlentities(string):
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]