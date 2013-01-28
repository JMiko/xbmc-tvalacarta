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

from core import config
from core import logger

cacheactiva = False

def cachePage(url):

	# Si la cache está desactivada, lo descarga siempre
	if not cacheactiva:
		logger.info("[scrapertools.py] cache desactivada")
		data = downloadpage(url)
	else:
		logger.info("[scrapertools.py] cache activada")
		# Fichero con la cache
		localFileName = binascii.hexlify(md5.new(url).digest()) + ".cache"
		logger.info("[scrapertools.py] cacheFile="+localFileName)

		# La crea en TEMP
		# TODO:crear subdirectorio nuevo (adnstream_plugin_cache)
		localFileName = xbmc.translatePath( os.path.join( "special://temp/", localFileName ))
		logger.info("[scrapertools.py] cacheDir="+localFileName)
		
		# Si el fichero existe en cache, lo lee
		if os.path.exists(localFileName):
			logger.info("[scrapertools.py] Leyendo de cache " + localFileName)
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
			logger.info("[scrapertools.py] Grabado a " + localFileName)
	return data

def cachePage2(url,headers):

	logger.info("[scrapertools.py] cachePage2 - " + url)
	inicio = time.clock()
	req = urllib2.Request(url)
	for header in headers:
		logger.info(header[0]+":"+header[1])
		req.add_header(header[0], header[1])

	try:
		response = urllib2.urlopen(req)
	except:
		req = urllib2.Request(url.replace(" ","%20"))
		for header in headers:
			logger.info(header[0]+":"+header[1])
			req.add_header(header[0], header[1])
		response = urllib2.urlopen(req)
	data=response.read()
	response.close()
	fin = time.clock()
	logger.info("Descargado en %d segundos " % (fin-inicio+1))

	'''
		outfile = open(localFileName,"w")
		outfile.write(data)
		outfile.flush()
		outfile.close()
		logger.info("Grabado a " + localFileName)
	'''
	return data

def cachePagePost(url,data):

	logger.info("[scrapertools.py] cachePagePost - " + url)
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
	logger.info("Descargado en %d segundos " % (fin-inicio+1))

	'''
		outfile = open(localFileName,"w")
		outfile.write(data)
		outfile.flush()
		outfile.close()
		logger.info("Grabado a " + localFileName)
	'''
	return data

def cachePagePostCookies(url,data):
	logger.info("[scrapertools.py] cachePagePostCookies - " + url)
	logger.info("[scrapertools.py] cachePagePostCookies - data="+data)
	inicio = time.clock()
	#  Inicializa la librería de las cookies
	ficherocookies = os.path.join( os.getcwd(), 'cookies.lwp' )
	logger.info("[scrapertools.py] cachePagePostCookies - Cookiefile="+ficherocookies)

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
	theurl = url
	# an example url that sets a cookie,
	# try different urls here and see the cookie collection you can make !

	#txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
	#			  'Referer':'http://www.megavideo.com/?s=signup'}
	txheaders =  {	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

	# fake a user agent, some websites (like google) don't like automated exploration

	req = Request(theurl, data, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies) # save the cookies again

	data=handle.read()
	handle.close()
	fin = time.clock()
	logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))

	return data

def downloadpage(url):
	logger.info("[scrapertools.py] downloadpage - " + url)
	
	inicio = time.clock()
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')
	#if referer!="":
	#	logger.info("[scrapertools.py] Referer=" + referer)
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
	logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))
	return data

def downloadpagewithcookies(url):
	logger.info("[scrapertools.py] downloadpagewithcookies - " + url)
	inicio = time.clock()
	#  Inicializa la librería de las cookies
	ficherocookies = os.path.join( os.getcwd(), 'cookies.lwp' )
	logger.info("[scrapertools.py] cachePagePostCookies - Cookiefile="+ficherocookies)

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
	theurl = url
	# an example url that sets a cookie,
	# try different urls here and see the cookie collection you can make !

	#txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
	#			  'Referer':'http://www.megavideo.com/?s=signup'}
	txheaders =  {
	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	#'Host':'www.meristation.com',
	'Accept-Language':'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3',
	'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Keep-Alive':'300',
	'Connection':'keep-alive'}

	# fake a user agent, some websites (like google) don't like automated exploration

	req = Request(theurl, None, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies) # save the cookies again

	data=handle.read()
	handle.close()
	fin = time.clock()
	logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))

	return data

def printMatches(matches):
	i = 0
	for match in matches:
		logger.info("[scrapertools.py] %d %s" % (i , match))
		i = i + 1

def entityunescape(cadena):
	cadena = cadena.replace('&amp;','&')
	cadena = cadena.replace('&Agrave;','À')
	cadena = cadena.replace('&Aacute;','Á')
	cadena = cadena.replace('&Eacute;','É')
	cadena = cadena.replace('&Iacute;','Í')
	cadena = cadena.replace('&Oacute;','Ó')
	cadena = cadena.replace('&Uacute;','Ú')
	cadena = cadena.replace('&ntilde;','ñ')
	cadena = cadena.replace('&Ntilde;','Ñ')
	cadena = cadena.replace('&agrave;','à')
	cadena = cadena.replace('&aacute;','á')
	cadena = cadena.replace('&eacute;','é')
	cadena = cadena.replace('&iacute;','í')
	cadena = cadena.replace('&oacute;','ó')
	cadena = cadena.replace('&uacute;','ú')
	cadena = cadena.replace('&iexcl;','¡')
	cadena = cadena.replace('&iquest;','¿')
	cadena = cadena.replace('&ordf;','ª')
	cadena = cadena.replace('&quot;','"')
	cadena = cadena.replace('&hellip;','...')
	cadena = cadena.replace('&#39;','\'')
	cadena = cadena.replace('&Ccedil;','Ç')
	cadena = cadena.replace('&ccedil;','ç')
	return cadena

def getRandom(str):
	return binascii.hexlify(md5.new(str).digest())

def getLocationHeaderFromResponse(url):
	logger.info("[scrapertools.py] getLocationHeaderFromResponse")

	if url=='':
		return None

	parsedurl = urlparse.urlparse(url)
	print "parsedurl=",parsedurl

	try:
		host = parsedurl.netloc
	except:
		host = parsedurl[1]
	print "host=",host

	try:
		print "1"
		query = parsedurl.path+";"+parsedurl.query
	except:
		print "2"
		query = parsedurl[2]+";"+parsedurl[3]+"?"
	print "query=",query
	query = urllib.unquote( query )
	print "query = " + query

	import httplib
	conn = httplib.HTTPConnection(host)
	conn.request("GET", query)
	response = conn.getresponse()
	location = response.getheader("location")
	conn.close()
	
	print "location=",location

	if location!=None:
		print "Encontrado header location"
	
	return location

def htmlclean(cadena):
	cadena = cadena.replace("<center>","")
	cadena = cadena.replace("</center>","")
	cadena = cadena.replace("<em>","")
	cadena = cadena.replace("</em>","")
	cadena = cadena.replace("<b>","")
	cadena = cadena.replace("</b>","")
	cadena = cadena.replace("<p>","")
	cadena = cadena.replace("</p>","")
	cadena = cadena.replace("</span>","")
	cadena = cadena.replace("</a>","")
	cadena = cadena.replace("<strong>","")
	cadena = cadena.replace("</strong>","")
	cadena = cadena.replace("</ul>","")
	cadena = cadena.replace("<li>","")
	cadena = cadena.replace("</li>","")
	cadena = cadena.replace("</dd>","")
	cadena = cadena.replace("</div>","")

	cadena = re.compile("<div[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<dd[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<img[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<font[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<span[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<a[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<ul[^>]*>",re.DOTALL).sub("",cadena)
	cadena = re.compile("<br[^>]*>",re.DOTALL).sub("",cadena)
	cadena = cadena.replace("\t","")
	cadena = entityunescape(cadena)
	return cadena

def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]
