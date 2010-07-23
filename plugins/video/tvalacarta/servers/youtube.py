# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib2,urllib,re,httplib
import xbmc,xbmcplugin,xbmcgui
import scrapertools

import gdata.youtube
import gdata.youtube.service

from item import Item

_VALID_URL = r'^((?:http://)?(?:\w+\.)?youtube\.com/(?:(?:v/)|(?:(?:watch(?:\.php)?)?\?(?:.+&)?v=)))?([0-9A-Za-z_-]+)(?(1).+)?$'
AVAILABLE_FORMATS  = ['13','17','34','5','18','35','22','37']
AVAILABLE_FORMATS2 = {'13':'Baja','17':'Media (3gp)','34':'High (FLV)','5':'360p','18':'480p','35':'1227KBS (FLV)','22':'720p','37':'1080p'}
std_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
	'Accept-Language': 'en-us,en;q=0.5',
}

def getuploads(user,startindex,maxresults):
	xbmc.output("[youtube.py] getuploads")

	# Obtiene el feed según el API de YouTube
	url = "http://gdata.youtube.com/feeds/api/users/%s/uploads?orderby=updated&start-index=%d&max-results=%d" % (user,startindex,maxresults)
	xbmc.output("[youtube.py] url="+url)
	yt_service = gdata.youtube.service.YouTubeService()
	feed = yt_service.GetYouTubeVideoFeed(url)
	
	itemlist = []
	for entry in feed.entry:
		'''
		print 'Video title: %s' % entry.media.title.text
		print 'Video published on: %s ' % entry.published.text
		print 'Video description: %s' % entry.media.description.text
		print 'Video category: %s' % entry.media.category[0].text
		print 'Video tags: %s' % entry.media.keywords.text
		print 'Video watch page: %s' % entry.media.player.url
		print 'Video flash player URL: %s' % entry.GetSwfUrl()
		print 'Video duration: %s' % entry.media.duration.seconds
		
		# non entry.media attributes
		#print 'Video geo location: %s' % entry.geo.location()
		#print 'Video view count: %s' % entry.statistics.view_count
		#print 'Video rating: %s' % entry.rating.average
		
		# show alternate formats
		#for alternate_format in entry.media.content:
		#	if 'isDefault' not in alternate_format.extension_attributes:
		#		print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)
		
		# show thumbnails
		for thumbnail in entry.media.thumbnail:
			print 'Thumbnail url: %s' % thumbnail.url
		'''
		
		item = Item(title=entry.title.text, url=entry.media.player.url, thumbnail = entry.media.thumbnail[len(entry.media.thumbnail)-1].url , plot = entry.media.description.text )
		itemlist.append( item )
	
	return itemlist

def getplaylists(user,startindex,maxresults):
	xbmc.output("[youtube.py] getplaylists")

	# Obtiene el feed segun el API de YouTube
	url = "http://gdata.youtube.com/feeds/api/users/%s/playlists?start-index=%d&max-results=%d" % (user,startindex,maxresults)
	xbmc.output("[youtube.py] url="+url)
	yt_service = gdata.youtube.service.YouTubeService()
	playlist_feed = yt_service.GetYouTubePlaylistFeed(uri=url)

	itemlist = []
	for entry in playlist_feed.entry:
		item = Item(title=entry.title.text, url=entry.id.text, thumbnail = "" , plot = "" )
		itemlist.append( item )

	return itemlist

def getplaylistvideos(url,startindex,maxresults):
	xbmc.output("[youtube.py] getplaylistvideos")
	# Extrae el ID de la playlist
	patron = 'http://.*?/([^/]+)/$'
	matches = re.compile(patron,re.DOTALL).findall(url+"/")
	idplaylist = matches[0]
	print idplaylist
	
	# Obtiene el feed segun el API de YouTube
	url = "http://gdata.youtube.com/feeds/api/playlists/%s?start-index=%d&max-results=%d" % (idplaylist,startindex,maxresults)
	xbmc.output("[youtube.py] url="+url)
	yt_service = gdata.youtube.service.YouTubeService()
	playlist_video_feed = yt_service.GetYouTubePlaylistVideoFeed(uri=url)

	itemlist = []
	for entry in playlist_video_feed.entry:
		item = Item(title=entry.title.text, url=entry.media.player.url, thumbnail = entry.media.thumbnail[len(entry.media.thumbnail)-1].url , plot = entry.media.description.text )
		itemlist.append( item )
	
	return itemlist

#### Busca las Urls originales de los formatos de calidad del video
def geturls(id,data):
	reglink = re.compile(r'fmt_stream_map=([^\&]+)\&')
	match = reglink.search(data)
	print 'Encontrado : %s'%str(match)
	if match is not None:
		reglink = match.group(1)
		reglink = urllib.unquote_plus(reglink)
		print 'los links : %s' %reglink
		reglinks= reglink.split(",")
		opciones = []
		links = []
		format = []
		for link in reglinks:
			try:
				fmt = link.split('|')
				opciones.append("Calidad %s" %AVAILABLE_FORMATS2[fmt[0]])
				links.append(fmt[1])
				format.append(fmt[0])
			except:
				pass
				
		dia = xbmcgui.Dialog()
		seleccion = dia.select("Elige una Calidad", opciones)
		xbmc.output("seleccion=%d calidad : (%s) %s " % (seleccion,format[seleccion],AVAILABLE_FORMATS2[format[seleccion]]))
		if seleccion == -1: return ""
		return links[seleccion]
	else:
		alertaNone()
	return ""
	
	
def geturl( id ):
	print '[pelisalacarta] youtube.py Modulo: geturl(%s)' %id
	quality = int(xbmcplugin.getSetting("quality_youtube"))
	if id != "":
		url = "http://www.youtube.com/watch?v=%s&fmt=18" % id
		print 'esta es la url: %s'%url
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response=urllib2.urlopen(req)
		data = response.read()
		response.close()
		if data != "":
			if quality == 8:
				videourl = geturls(id,data)
				return videourl
			regexp = re.compile(r'\&t=([^\&]+)\&')
			match = regexp.search(data)
			print 'match : %s'%str(match)
			videourl = ""
			if match is not None:
				tParam = match.group(1)
				while True:
					Tquality = AVAILABLE_FORMATS[quality]
					
					videourl1 = "http://www.youtube.com/get_video?video_id=%s&t=%s&fmt=%s" % ( id, tParam ,Tquality)
					try:
						videourl = verify_url( videourl1.encode( 'utf-8' ) ).decode( 'utf-8' )
						break
					except:
						quality -= 1
				print "Quality Found: (%s) %s " % (AVAILABLE_FORMATS[quality],AVAILABLE_FORMATS2[AVAILABLE_FORMATS[quality]])
				if videourl == "":
					alertaCalidad()
					return "" 
				return videourl
			else:
				alertaNone()
		else:
			alertaNone()
		
	else:
		alertaIDerror(id)
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
	try:
		conn = httplib.HTTPConnection("www.youtube.com")
		conn.request("GET","/get_video_info?&%s"%params)
		response = conn.getresponse()
		data = response.read()
	except:
		alertaNone()
		return ""
	video_info = dict((k,urllib.unquote_plus(v)) for k,v in
                               (nvp.split('=') for nvp in data.split('&')))
	
	conn.request('GET','/get_video?video_id=%s&t=%s&fmt=18' %
                         ( video_info['video_id'],video_info['token']))
	response = conn.getresponse()
	direct_url = response.getheader('location')
	return direct_url,video_info
	
def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: URL invalida: %s' % url
		#ventana = xbmcgui.Dialog()
		#ok= ventana.ok ("Plugin Pelisalacarta", "Lo sentimos, no se pudo extraer la ID",'del video: %s' %url,"La URL es invalida ")
		#return ""
	id = mobj.group(2)
	return id

def verify_url( url ):
	# Extract real URL to video
	request = urllib2.Request(url, None, std_headers)
	data = urllib2.urlopen(request)
	data.read(1)
	url = data.geturl()
	data.close()
	return url

def alertaCalidad():
	ventana = xbmcgui.Dialog()
	ok= ventana.ok ("Conector de Youtube", "La calidad elegida en configuracion",'no esta disponible o es muy baja',"elijá otra calidad distinta y vuelva a probar")
	
def alertaNone():
	ventana = xbmcgui.Dialog()
	ok= ventana.ok ("Conector de Youtube", "!Aviso¡","El video no se encuentra disponible",'es posible que haya sido removido')
	
def alertaIDerror():
	ventana = xbmcgui.Dialog(id)
	ok= ventana.ok ("Conector de Youtube", "Lo sentimos, no se pudo extraer la ID: %s" %id,'del video, la URL es invalida ')