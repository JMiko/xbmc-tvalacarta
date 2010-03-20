# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para divxden
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os.path
import sys
import xbmc
import os
import scrapertools

COOKIEFILE = xbmc.translatePath( "special://home/plugins/video/pelisalacarta/cookies.lwp" )

def geturl(urlvideo):
	xbmc.output("[divxlink.py] url="+urlvideo)
	# ---------------------------------------
	#  Inicializa la libreria de las cookies
	# ---------------------------------------
	ficherocookies = COOKIEFILE
	try:
		os.remove(ficherocookies)
	except:
		pass
	# the path and filename to save your cookies in

	cj = None
	ClientCookie = None
	cookielib = None

	# Let's see if cookielib is available
	try:
		import cookielib
	except ImportError:
		# If importing cookielib fails
		# let's try ClientCookie
		try:
			import ClientCookie
		except ImportError:
			# ClientCookie isn't available either
			urlopen = urllib2.urlopen
			Request = urllib2.Request
		else:
			# imported ClientCookie
			urlopen = ClientCookie.urlopen
			Request = ClientCookie.Request
			cj = ClientCookie.LWPCookieJar()

	else:
		# importing cookielib worked
		urlopen = urllib2.urlopen
		Request = urllib2.Request
		cj = cookielib.LWPCookieJar()
		# This is a subclass of FileCookieJar
		# that has useful load and save methods

	# ---------------------------------
	# Instala las cookies
	# ---------------------------------

	if cj is not None:
	# we successfully imported
	# one of the two cookie handling modules

		if os.path.isfile(ficherocookies):
			# if we have a cookie file already saved
			# then load the cookies into the Cookie Jar
			cj.load(ficherocookies)

		# Now we need to get our Cookie Jar
		# installed in the opener;
		# for fetching URLs
		if cookielib is not None:
			# if we use cookielib
			# then we get the HTTPCookieProcessor
			# and install the opener in urllib2
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			urllib2.install_opener(opener)

		else:
			# if we use ClientCookie
			# then we get the HTTPCookieProcessor
			# and install the opener in ClientCookie
			opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
			ClientCookie.install_opener(opener)

	#print "-------------------------------------------------------"
	url=urlvideo
	#print url
	#print "-------------------------------------------------------"
	theurl = url
	# an example url that sets a cookie,
	# try different urls here and see the cookie collection you can make !

	txdata = None
	# if we were making a POST type request,
	# we could encode a dictionary of values here,
	# using urllib.urlencode(somedict)

	txheaders =  {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'}
	# fake a user agent, some websites (like google) don't like automated exploration

	req = Request(theurl, txdata, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies)                     # save the cookies again    

	data=handle.read()
	handle.close()
	#print data

	# Lo pide una segunda vez, como si hubieras hecho click en el banner
	patron = 'http\:\/\/www\.divxlink\.com/([^\/]+)/(.*?)\.html'
	matches = re.compile(patron,re.DOTALL).findall(url)
	xbmc.output("[divxlink.py] fragmentos de la URL")
	scrapertools.printMatches(matches)
	
	codigo = ""
	nombre = ""
	if len(matches)>0:
		codigo = matches[0][0]
		nombre = matches[0][1]

	patron = '<input type="hidden" name="rand" value="([^"]+)">'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	randomstring=""
	if len(matches)>0:
		randomstring=matches[0]
	xbmc.output("[divxlink.py] randomstring="+randomstring)

	txdata = "op=download2&id="+codigo+"&rand="+randomstring+"&referer=&method_free=&method_premium=&down_direct=1"
	xbmc.output(txdata)
	req = Request(theurl, txdata, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies)                     # save the cookies again    

	data=handle.read()
	handle.close()
	#print data
	patron = '<div id="embedcontmvshre"[^>]+>(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	data = ""
	if len(matches)>0:
		data = matches[0]
		xbmc.output("[divxlink.py] bloque packed="+data)
	else:
		return ""
	
	# Extrae el cuerpo de la funcion
	patron = "eval\(function\(p\,a\,c\,k\,e\,d\)\{[^\}]+\}(.*?)\.split\('\|'\)\)\)"
	matches = re.compile(patron,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	
	# Separa el código de la tabla de conversion
	if len(matches)>0:
		data = matches[0]
		xbmc.output("[divxlink.py] bloque funcion="+data)
	else:
		return ""
	patron = "(.*)'([^']+)'"
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	cifrado = matches[0][0]
	xbmc.output("[divxlink.py] cifrado="+cifrado)
	xbmc.output("[divxlink.py] palabras="+matches[0][1])
	descifrado = ""
	
	# Crea el dicionario con la tabla de conversion
	claves = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"]
	palabras = matches[0][1].split("|")
	diccionario = {}

	i=0
	for palabra in palabras:
		if palabra!="":
			diccionario[claves[i]]=palabra
		else:
			diccionario[claves[i]]=claves[i]
		xbmc.output(claves[i]+"="+palabra)
		i=i+1

	# Sustituye las palabras de la tabla de conversion
	# Obtenido de http://rc98.net/multiple_replace
	def lookup(match):
		return diccionario[match.group(0)]

	lista = map(re.escape, diccionario)
	lista.reverse()
	compiled = re.compile('|'.join(lista))
	descifrado = compiled.sub(lookup, cifrado)
	
	xbmc.output("descifrado="+descifrado)
	# Extrae la URL
	patron = '<param name="src"value="([^"]+)"/>'
	matches = re.compile(patron,re.DOTALL).findall(descifrado)
	scrapertools.printMatches(matches)
	
	url = ""
	
	if len(matches)>0:
		url = matches[0]

	xbmc.output("[divxlink.py] url="+url)
	return url

def multiple_replace(dict, text): 

	""" Replace in 'text' all occurences of any key in the given
	dictionary by its corresponding value.  Returns the new tring.""" 

	# Create a regular expression  from the dictionary keys
	regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

	# For each match, look-up corresponding value in dictionary
	return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

