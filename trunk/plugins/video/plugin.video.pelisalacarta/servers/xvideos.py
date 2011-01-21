# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para xvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import logger
import socket

# Obtiene la id del video
def geturl(id):
	url = "http://www.xvideos.com/video"+id
	logger.info("[xvideos.py] url="+url)
	devuelve = ""
	# Primero obtenemos la url verdadera del video con un redireccionamiento
	# Timeout del socket a 60 segundos
	socket.setdefaulttimeout(10)

	h=urllib2.HTTPHandler(debuglevel=0)
	request = urllib2.Request(url)

	opener = urllib2.build_opener(h)
	urllib2.install_opener(opener)
	try:
		connexion = opener.open(request)
		url = connexion.geturl()
	except urllib2.HTTPError,e:
		logger.info("[xvideos.py]  error %d (%s) al abrir la url %s" % (e.code,e.msg,url))
		
		print e.read()
		return devuelve

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	data=response.read()
	response.close()

	patronvideos = "flv_url=([^&]+)&"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		devuelve = urllib.unquote_plus(matches[0])


	logger.info("[xvideos.py] url="+devuelve)

	return devuelve
