# -*- coding: UTF-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Channel SKAI NEW FOLDERS
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import binascii

from core import scrapertools
from platformcode.xbmc import xbmctools

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.log("[skai_folders.py] init")

print "LANG="
print xbmc.getLanguage



DEBUG = True
CHANNELNAME = "Σκαι: Οι Νεοι Φακελοι"
CHANNELCODE = "skai_folders"

def unescape(s):
	s = s.replace("&quot;", "\"")
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	# this has to be last:
	s = s.replace("&amp;", "&")
	return s


def mainlist(params,url,category):
	xbmc.log("[skai_folders.py] mainlist")

	url = "http://folders.skai.gr/main"
	locale = "el"
	
	url_loc = url + "?locale=" + locale

	# --------------------------------------------------------
	# Download page
	# --------------------------------------------------------
	data = scrapertools.cachePage(url_loc)
	#xbmc.log(data)

	# --------------------------------------------------------
	# Extrae los programas
	# --------------------------------------------------------
	
	pattern = '<p class="title"><a href="(.*?)" title="Δείτε.*?Φάκελοι»">([^<]+)</a></p>'
		
	matches = re.compile(pattern,re.DOTALL).findall(data)
	if DEBUG:
		print 'matches are: ...............'
		print matches
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = unescape(match[1])
		try:
			scrapedtitle = unicode( scrapedtitle, "UTF-8", "ignore" ).encode("UTF-8")
		except:
			pass
		scrapedurl = urlparse.urljoin(url,unescape(match[0]))
		
		scrapedthumbnail = ""
		scrapedplot = ""

		# purification
		if (DEBUG):
			xbmc.log("scrapedtitle="+scrapedtitle)
			xbmc.log("scrapedurl="+scrapedurl)
			xbmc.log("scrapedthumbnail="+scrapedthumbnail)

		#Add to the list of XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):

	xbmc.log("[skai_folders.py] videolist")

	# --------------------------------------------------------
	# DDownload page
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)


	# Extrae los vídeos
	patron  = '<p><a href=\'(.*?)\' title=.*?<img alt="([^<]+)" src="(.*?)" /></a></p>'
	
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: 
		scrapertools.printMatches(matches)
		
		
	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,unescape(match[0]))
		scrapedthumbnail = urlparse.urljoin(url,match[2])
	#	scrapedplot = scrapertools.entityunescape(match[2])
		scrapedplot = "XXX XXXX XXXXXXXXXXX XXXXXXXXX XXXXXXXXX XXXXXXXXX        X           X XXX  X  X X X X X X X  X"
		
		
		if (DEBUG): xbmc.log("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Add to the list of XBMC
		xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
		
	# Next Page
	pattern  = 'class="next_page" rel="next" href="(.*?)">Επόμενη</a></p>'
	matches = re.compile(pattern,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	if len(matches)>0:
		match = matches[0]
		
	
		scrapedtitle = ">>> Next Page >>>"
		scrapedurl = urlparse.urljoin(url,match)
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.log("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Add to the list of XBMC
		xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.log("[skai_folders.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"
	
    # --------------------------------------------------------
	# DDownload page
	# --------------------------------------------------------
	
	data = scrapertools.cachePage(url)
	pattern = 'rtmp://cp67754.edgefcs.net/ondemand/mp4:content/Fakeloi/20.*?mp4'
	matches = re.compile(pattern,re.DOTALL).findall(data)
	
	
	if len(matches)==0:
		xbmctools.alerterrorpagina()
		return

	url = matches[0]
	xbmc.log("url="+url)
	
	

	xbmctools.play_video(CHANNELCODE,server,url,category,title,thumbnail,plot)
