# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Scraper Tools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import time
import binascii
import md5
import os
import xbmc

cacheactiva = False

def cachePage(url):

	# Si la cache está desactivada, lo descarga siempre
	if not cacheactiva:
		xbmc.output("[scrapertools.py] cache desactivada")
		data = downloadpage(url)
	else:
		xbmc.output("[scrapertools.py] cache activada")
		# Fichero con la cache
		localFileName = binascii.hexlify(md5.new(url).digest()) + ".cache"
		xbmc.output("[scrapertools.py] cacheFile="+localFileName)

		# La crea en TEMP
		# TODO:crear subdirectorio nuevo (adnstream_plugin_cache)
		localFileName = xbmc.translatePath( os.path.join( "special://temp/", localFileName ))
		xbmc.output("[scrapertools.py] cacheDir="+localFileName)
		
		# Si el fichero existe en cache, lo lee
		if os.path.exists(localFileName):
			xbmc.output("[scrapertools.py] Leyendo de cache " + localFileName)
			infile = open( localFileName )
			data = infile.read()
			infile.close();
		# Si no existe en cache, lo descarga y luego graba en cache
		else:
			# Lo descarga
			data = downloadpage(url)
			
			# Lo graba en cache
			outfile = open(localFileName,"w")
			outfile.write(data)
			outfile.flush()
			outfile.close()
			xbmc.output("[scrapertools.py] Grabado a " + localFileName)
	return data

def cachePage2(url,headers):

	xbmc.output("Descargando " + url)
	inicio = time.clock()
	req = urllib2.Request(url)
	for header in headers:
		xbmc.output(header[0]+":"+header[1])
		req.add_header(header[0], header[1])

	try:
		response = urllib2.urlopen(req)
	except:
		req = urllib2.Request(url.replace(" ","%20"))
		for header in headers:
			xbmc.output(header[0]+":"+header[1])
			req.add_header(header[0], header[1])
		response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	fin = time.clock()
	xbmc.output("Descargado en %d segundos " % (fin-inicio+1))

	'''
		outfile = open(localFileName,"w")
		outfile.write(data)
		outfile.flush()
		outfile.close()
		xbmc.output("Grabado a " + localFileName)
	'''
	return data

def cachePagePost(url,data):

	xbmc.output("Descargando " + url)
	inicio = time.clock()
	req = urllib2.Request(url,data)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

	try:
		response = urllib2.urlopen(req)
	except:
		req = urllib2.Request(url.replace(" ","%20"),data)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	fin = time.clock()
	xbmc.output("Descargado en %d segundos " % (fin-inicio+1))

	'''
		outfile = open(localFileName,"w")
		outfile.write(data)
		outfile.flush()
		outfile.close()
		xbmc.output("Grabado a " + localFileName)
	'''
	return data

def downloadpage(url):
	xbmc.output("[scrapertools.py] Descargando " + url)
	inicio = time.clock()
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')
	#if referer!="":
	#	xbmc.output("[scrapertools.py] Referer=" + referer)
	#	req.add_header('Referer', referer)
	try:
		response = urllib2.urlopen(req)
	except:
		req = urllib2.Request(url.replace(" ","%20"))
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')

		response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	fin = time.clock()
	xbmc.output("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))
	return data

def printMatches(matches):
	i = 0
	for match in matches:
		xbmc.output("[scrapertools.py] %d %s" % (i , match))
		i = i + 1

def entityunescape(cadena):
	cadena = cadena.replace('&Aacute;','Á')
	cadena = cadena.replace('&Eacute;','É')
	cadena = cadena.replace('&Iacute;','Í')
	cadena = cadena.replace('&Oacute;','Ó')
	cadena = cadena.replace('&Uacute;','Ú')
	cadena = cadena.replace('&ntilde;','ñ')
	cadena = cadena.replace('&Ntilde;','Ñ')
	cadena = cadena.replace('&aacute;','á')
	cadena = cadena.replace('&eacute;','é')
	cadena = cadena.replace('&iacute;','í')
	cadena = cadena.replace('&oacute;','ó')
	cadena = cadena.replace('&uacute;','ú')
	cadena = cadena.replace('&amp;','&')
	cadena = cadena.replace('&iexcl;','¡')
	cadena = cadena.replace('&iquest;','¿')
	cadena = cadena.replace('&ordf;','ª')
	return cadena

def getRandom(str):
	return binascii.hexlify(md5.new(str).digest())
