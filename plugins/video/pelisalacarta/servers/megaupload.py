# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Megaupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, sys, os
import urlparse, urllib, urllib2
import os.path
import sys
import xbmc
import xbmcplugin
import megavideo
import scrapertools

DEBUG = True

# Convierte el c�digo de megaupload a megavideo
def convertcode(megauploadcode):
	# Descarga la p�gina de megavideo pas�ndole el c�digo de megaupload
	url = "http://www.megavideo.com/?d="+megauploadcode
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = 'flashvars.v = "([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	
	if len(matches)>0:
		megavideocode = matches[0]

	return megavideocode

def getvideo(code):
	return megavideo.Megavideo(convertcode(code))

def gethighurl(code):
	return megavideo.gethighurl(convertcode(code))

def getlowurl(code):
	return megavideo.getlowurl(convertcode(code))
