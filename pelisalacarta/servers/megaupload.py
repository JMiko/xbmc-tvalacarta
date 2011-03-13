# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Megaupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urlparse, urllib, urllib2,socket
import megavideo


try:
	from core import scrapertools
	from core import logger
	from core import config
except:
	from Code.core import scrapertools
	from Code.core import logger
	from Code.core import config

import os
COOKIEFILE = os.path.join(config.get_data_path() , "cookies.lwp")

DEBUG = False

# Convierte el código de megaupload a megavideo
def convertcode(megauploadcode):
	# Descarga la página de megavideo pasándole el código de megaupload
	url = "http://www.megavideo.com/?d="+megauploadcode
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas (carpetas)
	patronvideos  = 'flashvars.v = "([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)
	
	megavideocode = ""
	if len(matches)>0:
		megavideocode = matches[0]

	return megavideocode

# Extrae directamente la URL del vídeo de Megaupload
def getmegauploaduser(login,password):

	# ---------------------------------------
	#  Inicializa la librería de las cookies
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
	url="http://www.megaupload.com/?c=login"
	#print url
	#print "-------------------------------------------------------"
	theurl = url
	# an example url that sets a cookie,
	# try different urls here and see the cookie collection you can make !

	passwordesc=password.replace("&","%26")
	txdata = "login=1&redir=1&username="+login+"&password="+passwordesc
	# if we were making a POST type request,
	# we could encode a dictionary of values here,
	# using urllib.urlencode(somedict)

	txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
				  'Referer':'http://www.megaupload.com'}
	# fake a user agent, some websites (like google) don't like automated exploration

	req = Request(theurl, txdata, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies)					 # save the cookies again	
	data=handle.read()
	handle.close()

	cookiedatafile = open(ficherocookies,'r')
	cookiedata = cookiedatafile.read()
	cookiedatafile.close();

	'''
	logger.info("----------------------")
	logger.info("Cookies despues")
	logger.info("----------------------")
	logger.info(cookiedata)
	logger.info("----------------------")
	'''

	patronvideos  = 'user="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(cookiedata)
	if len(matches)==0:
		patronvideos  = 'user=([^\;]+);'
		matches = re.compile(patronvideos,re.DOTALL).findall(cookiedata)

	if len(matches)==0 and DEBUG:
		logger.info("No se ha encontrado la cookie de Megaupload")
		logger.info("----------------------")
		logger.info("Respuesta de Megaupload")
		logger.info("----------------------")
		logger.info(data)
		logger.info("----------------------")
		logger.info("----------------------")
		logger.info("Cookies despues")
		logger.info("----------------------")
		logger.info(cookiedata)
		logger.info("----------------------")
		devuelve = ""
	else:
		devuelve = matches[0]

	return devuelve

import exceptions

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		raise ImportError(302,headers.getheader("Location"))

def getmegauploadvideo(code,user):
	logger.info("getmegauploadvideo0")
	req = urllib2.Request("http://www.megaupload.com/?d="+code)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Cookie', 'l=es; user='+user)
	try:
		opener = urllib2.build_opener(SmartRedirectHandler())
		response = opener.open(req)
	except ImportError, inst:	
		status,location=inst
		logger.info(str(status) + " " + location)	
		mediaurl = location
	else:
		#logger.info(response)
		#logger.info(response.info() + " es el info")
		data=response.read()
		response.close()

		patronvideos  = '<div class="down_ad_pad1">[^<]+<a href="([^"]+)"'
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		mediaurl = ""
		if len(matches)>0:
			mediaurl = matches[0]
			# Timeout del socket a 60 segundos
			socket.setdefaulttimeout(10)

			h=urllib2.HTTPHandler(debuglevel=0)
			request = urllib2.Request(mediaurl)

			opener = urllib2.build_opener(h)
			urllib2.install_opener(opener)
			try:
			
				connexion = opener.open(request)
				mediaurl= connexion.geturl()
			
			except urllib2.HTTPError,e:
				print ("[megaupload.py]  error %d (%s) al abrir la url %s" % (e.code,e.msg,mediaurl))
			
				print e.read()	
			
	return mediaurl

def getvideo(code):
	return megavideo.Megavideo(convertcode(code))

def gethighurl(code):
	megavideologin = config.get_setting("megavideouser")
	if DEBUG:
		logger.info("[megaupload.py] megavideouser=#"+megavideologin+"#")
	megavideopassword = config.get_setting("megavideopassword")
	if DEBUG:
		logger.info("[megaupload.py] megavideopassword=#"+megavideopassword+"#")
	cookie = getmegauploaduser(megavideologin,megavideopassword)
	if DEBUG:
		logger.info("[megaupload.py] cookie=#"+cookie+"#")

	if len(cookie) == 0:
		import xbmcgui
		advertencia = xbmcgui.Dialog()
		resultado = advertencia.ok('Cuenta de Megaupload errónea' , 'La cuenta de Megaupload que usas no es válida' , 'Comprueba el login y password en la configuración')
		return ""

	return getmegauploadvideo(code,cookie)

def getlowurl(code):
	return megavideo.getlowurl(convertcode(code))
