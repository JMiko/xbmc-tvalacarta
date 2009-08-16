# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
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
import tutv
import stagevu
import vreel

xbmc.output("[servertools.py] init")

def findvideos(data):
	xbmc.output("[servertools.py] findvideos")
	encontrados = set()
	devuelve = []

	# Megavideo - Vídeos con título
	xbmc.output("1) Megavideo con titulo...")
	patronvideos  = '<div align="center">([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "Sin título"
		titulo = titulo + " (id "+match[1]+")"
		url = match[1]
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - Vídeos sin título
	xbmc.output("2) Megavideo sin titulo...")
	patronvideos  = '<param name="movie" value="http://wwwstatic.megavideo.com/mv_player.swf\?v=([^"]+)">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título (id "+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Vreel - Vídeos con título
	xbmc.output( "3) Vreel con título...")
	patronvideos  = '<div align="center"><b>([^<]+)</b>.*?<a href\="(http://beta.vreel.net[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "Sin título"
		url = match[1]
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Vreel - Vídeos con título
	xbmc.output("4) Vreel con titulo...")
	patronvideos  = '<div align="center">([^<]+)<.*?<a href\="(http://beta.vreel.net[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = match[0].strip()
		if titulo == "":
			titulo = "Sin título"
		url = match[1]
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# WUAPI
	xbmc.output("5) wuapi sin título")
	patronvideos  = '<a href\="(http://wuapi.com[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título ("+match[23:]+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Wuapi' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# WUAPI
	xbmc.output("6) wuapi sin título...")
	patronvideos  = '(http://wuapi.com[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título ("+match[23:]+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Wuapi' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# STAGEVU
	xbmc.output("7) Stagevu sin título...")
	patronvideos  = '"(http://stagevu.com[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título ("+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# TU.TV
	xbmc.output("8) Tu.tv sin título...")
	patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título ("+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'tu.tv' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# TU.TV
	xbmc.output("9) Tu.tv sin título...")
	#<param name="movie" value="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS0xLTYtbGEtbC5mbHY=&xtp=669149_VIDEO"
	patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin título ("+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'tu.tv' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - Vídeos sin título
	xbmc.output("10 ) Megavideo sin titulo...")
	patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin titulo (id "+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - Vídeos sin título
	xbmc.output("11) Megavideo sin titulo...")
	patronvideos  = '"http://www.megavideo.com/v/([A-Z0-9]{8})[^"]+"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin titulo (id "+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# STAGEVU
	xbmc.output("12) Stagevu...")
	patronvideos  = '(http://stagevu.com[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin titulo (id "+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)
		
	# Vreel - Vídeos sin título
	xbmc.output("13) Vreel sin titulo...")
	patronvideos  = '(http://beta.vreel.net[^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		titulo = "Sin titulo (id "+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Vreel' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	# Megavideo - Vídeos con título
	xbmc.output("14) Megavideo con titulo...")
	patronvideos  = '<a href="http://www.megavideo.com/\?v\=([^"]+)".*?>(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = match[1].strip()
		if titulo == "":
			titulo = "Sin título"
		titulo = titulo + " (id "+match[0]+")"
		url = match[0]
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			xbmc.output("  url duplicada="+url)

	xbmc.output("0) Stagevu...")
	patronvideos  = '"http://stagevu.com.*?uid\=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = "Sin título ("+match+")"
		url = "http://stagevu.com/video/"+match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Stagevu' ] )
			encontrados.add(url)
		else:
			logFile.info("  url duplicada="+url)


	xbmc.output("0) Megavideo... formato d=XXXXXXX")
	patronvideos  = '"http://www.megavideo.com/.*?\&d\=([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		titulo = "Megavideo ("+match+")"
		url = match
		if url not in encontrados:
			devuelve.append( [ titulo , url , 'Megavideo' ] )
			encontrados.add(url)
		else:
			logFile.info("  url duplicada="+url)

	return devuelve

	

def findurl(code,server):
	mediaurl = "ERROR"
	if server == "Megavideo":
		mediaurl = megavideo.Megavideo(code)
		
	if server == "Wuapi":
		mediaurl = wuapi.Wuapi(code)
		
	if server == "Vreel":
		mediaurl = vreel.Vreel(code)

	if server == "Stagevu":
		mediaurl = stagevu.Stagevu(code)
	
	if server == "tu.tv":
		mediaurl = tutv.Tutv(code)
	
	if server == "Directo":
		mediaurl = code
	return mediaurl

def getmegavideolow(code):
	return megavideo.getlowurl(code)

def getmegavideohigh(code):
	return megavideo.gethighurl(code)
