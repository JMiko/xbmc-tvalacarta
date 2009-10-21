# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

def geturl( id ):
	if id != "":
		url = "http://www.youtube.com/watch?v=%s" % id
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response=urllib2.urlopen(req)
		data = response.read()
		response.close()
		if data != "":
			regexp = re.compile(r', "t": "([^"]+)"')
			match = regexp.search(data)
			if match is not None:
				tParam = match.group(1)
				videourl = "http://www.youtube.com/get_video?video_id=%s&t=%s&fmt=18" % ( id, tParam )
				videourl = urllib.urlopen( videourl ).geturl()
				return videourl
	return False

