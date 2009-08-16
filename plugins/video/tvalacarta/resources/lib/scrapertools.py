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

def cachePage(url):

	'''
	localFileName = binascii.hexlify(md5.new(url).digest()) + ".cache"
	xbmc.output("cacheFile="+localFileName)

	# TODO:crear subdirectorio nuevo (adnstream_plugin_cache)
	localFileName = xbmc.translatePath( os.path.join( "special://temp/", localFileName ))
	xbmc.output("cacheDir="+localFileName)
	if os.path.exists(localFileName):
		xbmc.output("Leyendo de cache " + localFileName)
		infile = open( localFileName )
		data = infile.read()
		infile.close();
	else:
	'''
	xbmc.output("Descargando " + url)
	inicio = time.clock()
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	try:
		response = urllib2.urlopen(req)
	except:
		req = urllib2.Request(url.replace(" ","%20"))
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

def printMatches(matches):
	i = 0
	for match in matches:
		xbmc.output("%d %s" % (i , match))
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
	return cadena