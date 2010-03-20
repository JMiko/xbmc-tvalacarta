# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,httplib
_VALID_URL = r'^((?:http://)?(?:\w+\.)?youtube\.com/(?:(?:v/)|(?:(?:watch(?:\.php)?)?\?(?:.+&)?v=)))?([0-9A-Za-z_-]+)(?(1).+)?$'


def geturl( id ):
	
	if id != "":
		url = "http://www.youtube.com/watch?v=%s" % id
		print 'esta es la url: %s'%url
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response=urllib2.urlopen(req)
		data = response.read()
		response.close()
		if data != "":
			regexp = re.compile(r', "t": "([^"]+)"')
			match = regexp.search(data)
			print 'match : %s'%str(match)
			if match is not None:
				tParam = match.group(1)
				videourl = "http://www.youtube.com/get_video?video_id=%s&t=%s&fmt=18" % ( id, tParam )
				videourl = urllib.urlopen( videourl ).geturl()
				return videourl
	return ""

def GetYoutubeVideoInfo(videoID,eurl=None):
	'''
	Return direct URL to video and dictionary containing additional info
	>> url,info = GetYoutubeVideoInfo("tmFbteHdiSw")
	>>
	'''
	
	if not eurl:
		params = urllib.urlencode({'video_id':videoID})
	else :
		params = urllib.urlencode({'video_id':videoID, 'eurl':eurl})
	conn = httplib.HTTPConnection("www.youtube.com")
	conn.request("GET","/get_video_info?&%s"%params)
	response = conn.getresponse()
	data = response.read()
	video_info = dict((k,urllib.unquote_plus(v)) for k,v in
                               (nvp.split('=') for nvp in data.split('&')))
	conn.request('GET','/get_video?video_id=%s&t=%s' %
                         ( video_info['video_id'],video_info['token']))
	response = conn.getresponse()
	direct_url = response.getheader('location')
	return direct_url,video_info
	
def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: URL invalida: %s' % url
		return ""
	id = mobj.group(2)
	return id