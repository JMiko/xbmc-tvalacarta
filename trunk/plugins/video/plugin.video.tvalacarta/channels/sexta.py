# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para la sexta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import logger
import scrapertools
from item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "sexta"

def isGeneric():
	return True

def mainlist(item):
	logger.info("[sexta.py] mainlist")

	# Descarga la p�gina
	url = "http://www.lasexta.com/sextatv"
	
	itemlist = []
	
	getprogramaspagina(url,"item_id=1&show_id=1&bd_id=1&pagina=&limit=3",itemlist)
	getprogramaspagina(url,"item_id=1&show_id=1&bd_id=1&pagina=8&limit=3",itemlist)
	getprogramaspagina(url,"item_id=1&show_id=1&bd_id=1&pagina=16&limit=3",itemlist)
	
	return itemlist

def getprogramaspagina(url,post,itemlist):
	logger.info("[sexta.py] getprogramaspagina")
	
	headers = [
			['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],
			['X-Requested-With','XMLHttpRequest'],
			['X-Prototype-Version','1.6.0.3'],
			['Referer','http://www.lasexta.com/sextatv']
			]
	
	data = scrapertools.cachePagePost(url,post,headers)
	#logger.info(data)

	'''
	<div class="capaseccionl item_vip">
	<div class="player">
	<a href="http://www.lasexta.com/sextatv/seloquehicisteis">
	<img src="http://www.lasexta.com/media/sextatv/img/sextatv_logo_slqh.jpg" width="230" height="129" title="Vídeos de Sé lo que Hicísteis" alt="logotipo de Sé lo que hicísteis" />
	<label class="item_vip_player_label">Sé lo que Hicísteis</label>
	<img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" class="item_vip_player_link" alt="Ir a videos de Sé lo que Hicísteis"/>
	</a>
	</div>
	'''

	# Extrae las entradas
	patron  = '<div class="capaseccionl item_vip">[^<]+'
	patron += '<div class="player">[^<]+'
	patron += '<a href="([^"]+)">[^<]+'
	patron += '<img src="([^"]+)"[^>]+>[^<]+'
	patron += '<label class="item_vip_player_label">([^<]+)</label>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[2]
		try:
			scrapedtitle = unicode( scrapedtitle , "utf-8" ).encode("iso-8859-1")
		except:
			pass
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

def videosportada(item,id):
	logger.info("[a3.py] videosportada")
	
	print item.tostring()
	
	# Descarga la p�gina
	data = scrapertools.cachePagePost(item.url)
	#logger.info(data)

	# Extrae las entradas
	patron = '<div id="'+id+'"(.*?)</div><!-- .visor -->'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)
	data = matches[0]
	
	'''
	<div>
	<a title="V�deos de El Internado - Cap�tulo 8 - Temporada 7" href="/videos/el-internado/temporada-7/capitulo-8.html">
	<img title="V�deos de El Internado - Cap�tulo 8 - Temporada 7" 
	src="/clipping/2010/07/21/00048/10.jpg"
	alt="El �ltimo deseo"
	href="/videos/el-internado/temporada-7/capitulo-8.html"
	/>
	<strong>El Internado</strong>
	<p>El �ltimo deseo</p></a>  
	</div>
	'''

	patron  = '<div>[^<]+'
	patron += '<a title="([^"]+)" href="([^"]+)">[^<]+'
	patron += '<img.*?src="([^"]+)"[^<]+'
	patron += '<strong>([^<]+)</strong>[^<]+'
	patron += '<p>([^<]+)</p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[3]+" - "+match[4]+" ("+match[0]+")"
		scrapedurl = urlparse.urljoin(item.url,match[1])
		scrapedthumbnail = urlparse.urljoin(item.url,match[2])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def ultimasemana(item):
	logger.info("[a3.py] ultimasemana")
	
	print item.tostring()
	
	# Descarga la p�gina
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Extrae las entradas (series)
	'''
	<div>
	<em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
	<a title="V�deos de Noticias 1 - 19 de Agosto de 2.010" href="/videos/noticias/noticias-1-19-agosto.html">
	<img title="V�deos de Noticias 1 - 19 de Agosto de 2.010"  
	src="/clipping/2010/05/21/00055/10.jpg"
	alt="19 de agosto"
	href="/videos/noticias/noticias-1-19-agosto.html"
	/>
	</a>
	<a title="V�deos de Noticias 1 - 19 de Agosto de 2.010" href="/videos/noticias/noticias-1-19-agosto.html">
	<strong>Noticias 1</strong>
	<p>19 de agosto</p></a>  
	</div>
	'''
	patron  = '<div>[^<]+'
	patron += '<em[^>]+><img[^>]+></em>[^<]+'
	patron += '<a title="([^"]+)" href="([^"]+)">[^<]+'
	patron += '<img title="[^"]+"[^<]+'  
	patron += 'src="([^"]+)"[^>]+>[^<]+'
	patron += '</a>[^<]+'
	patron += '<a[^>]+>[^<]+'
	patron += '<strong>([^<]+)</strong>[^<]+'
	patron += '<p>([^<]+)</p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[3]+" - "+match[4]+" ("+match[0]+")"
		scrapedurl = urlparse.urljoin(item.url,match[1])
		scrapedthumbnail = urlparse.urljoin(item.url,match[2])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def series(item):
	logger.info("[a3.py] series")
	
	print item.tostring()
	
	# Descarga la p�gina
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Extrae las entradas (series)
	'''
	<div>
	<a title="V�deos de Share - Cap�tulos Completos" href="/videos/share.html">
	<img title="V�deos de Share - Cap�tulos Completos" href="/videos/share.html"
	src="/clipping/2010/08/06/00246/10.jpg"
	alt="Share"
	/>
	<a title="V�deos de Share - Cap�tulos Completos" href="/videos/share.html"><p>Share</p></a>                    
	</a>
	</div>
	</li>
	'''
	patron  = '<div>[^<]+'
	patron += '<a\W+title="[^"]+" href="([^"]+)"[^<]+'
	patron += '<img.*?src="([^"]+)"[^<]+'
	patron += '<a[^<]+<p>([^<]+)</p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[2]
		scrapedurl = urlparse.urljoin(item.url,match[0])
		scrapedthumbnail = urlparse.urljoin(item.url,match[1])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="capitulos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def capitulos(item):
	logger.info("[a3.py] capitulos")
	
	print item.tostring()
	
	# Descarga la p�gina
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Capitulos
	'''
	<div>
	<a  title="V�deos de El Internado - Cap�tulo 8 - Temporada 7"
	href="/videos/el-internado/temporada-7/capitulo-8.html">
	<img title="V�deos de El Internado - Cap�tulo 8 - Temporada 7" 
	src="/clipping/2010/07/21/00048/10.jpg"
	alt="EL INTERNADO T7 C8"
	href="/videos/el-internado/temporada-7/capitulo-8.html"
	/>
	<em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
	<strong>EL INTERNADO T7 C8</strong>
	<p>El �ltimo deseo</p>
	</a>	
	</div>
	'''
	patron  = '<div>[^<]+'
	patron += '<a.*?href="([^"]+)"[^<]+'
	patron += '<img.*?src="([^"]+)".*?'
	patron += '<strong>([^<]+)</strong>[^<]+'
	patron += '<p>([^<]+)</p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[2]+" - "+match[3]
		scrapedurl = urlparse.urljoin(item.url,match[0])
		scrapedthumbnail = urlparse.urljoin(item.url,match[1])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	# Otras temporadas
	patron = '<dd class="paginador">(.*?)</dd>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)
	subdata = matches[0]
	
	'''
	<ul>
	<li  class="active" >
	<a 	title="V�deos de El Internado - Temporada 7 - Cap�tulos Completos"
	href="/videos/el-internado.html" >7
	</a>
	</li>
	'''
	patron  = '<li[^<]+'
	patron += '<a.*?href="([^"]+)" >([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(subdata)
	
	#if DEBUG: scrapertools.printMatches(matches)
	for match in matches:
		scrapedtitle = "Temporada "+match[1].strip()
		scrapedurl = urlparse.urljoin(item.url,match[0])
		scrapedthumbnail = item.thumbnail
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="capitulos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist

def noticias(item):
	logger.info("[a3.py] noticias")
	
	print item.tostring()
	
	# Descarga la p�gina
	data = scrapertools.cachePage(item.url)
	#logger.info(data)

	# Extrae las entradas (series)
	'''
	<div>
	<a title="V�deos de Noticias Fin de Semana - 22 de Agosto de 2.010" 
	href="/videos/noticias/noticias-fin-semana-22082010.html">
	<img title="V�deos de Noticias Fin de Semana - 22 de -1 de 2.010" 
	src="/clipping/2010/06/01/00105/10.jpg"
	alt="Noticias fin de semana 22-08-2010 "
	href="/videos/noticias/fin-de-semana-completo/2010-agosto-22.html"
	/>
	<em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
	<a 
	title="V�deos de Noticias Fin de Semana - 22 de Agosto de 2.010"
	href="/videos/noticias/noticias-fin-semana-22082010.html"
	>
	<strong>Noticias Fin de Semana</strong>
	<p>22 de agosto 15.00h</p>
	</a>                    
	'''
	patron  = '<div>[^<]+'
	patron += '<a.*?href="([^"]+)">[^<]+'
	patron += '<img.*?src="([^"]+)"[^>]+>.*?'
	patron += '<strong>([^<]+)</strong>[^<]+'
	patron += '<p>([^<]+)</p>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	#if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		scrapedtitle = match[2]+" - "+match[3]
		scrapedurl = urlparse.urljoin(item.url,match[0])
		scrapedthumbnail = urlparse.urljoin(item.url,match[1])
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado
		itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

	return itemlist
	
def programas(item):
	logger.info("[a3.py] programas")
	return series(item)
	
def tvmovies(item):
	logger.info("[a3.py] tvmovies")
	return series(item)

def detalle(item):
	logger.info("[a3.py] detalle")
	print item.tostring()

	# Descarga la p�gina de detalle
	data = scrapertools.cachePage(item.url)

	patron="<source src='([^']+)'"
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)
	scrapedurl = urlparse.urljoin(item.url,matches[0])
	itemlist = []
	itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=scrapedurl, page = item.url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , folder=False) )

	'''
	# Extrae el xml
	patron = 'so.addVariable\("xml","([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)
	scrapedurl = urlparse.urljoin(item.url,matches[0])
	logger.info("url="+scrapedurl)
	
	# Descarga la p�gina del xml
	data = scrapertools.cachePage(scrapedurl)

	# Extrae las entradas del video y el thumbnail
	patron = '<urlHttpVideo><\!\[CDATA\[([^\]]+)\]\]>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	baseurlvideo = matches[0]
	logger.info("baseurlvideo="+baseurlvideo)
	
	patron = '<urlImg><\!\[CDATA\[([^\]]+)\]\]>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	baseurlthumb = matches[0]
	logger.info("baseurlthumb="+baseurlthumb)
	
	patron  = '<archivoMultimediaMaxi>[^<]+'
	patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapedthumbnail = urlparse.urljoin(baseurlthumb,matches[0])
	logger.info("scrapedthumbnail="+scrapedthumbnail)
	
	patron  = '<archivoMultimedia>[^<]+'
	patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
	matches = re.compile(patron,re.DOTALL).findall(data)

	itemlist = []
	i = 1
	for match in matches:
		scrapedurl = urlparse.urljoin(baseurlvideo,match)
		logger.info("scrapedurl="+scrapedurl)
		itemlist.append( Item(channel=CHANNELNAME, title="(%d) %s" % (i,item.title) , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail , plot=item.plot , server = "directo" , folder=False) )
		i=i+1
	'''
	return itemlist

def test():
	itemsmainlist = mainlist(None)

	# Listado principal
	#itemsmasvistos = losmasvistos(itemsmainlist[0])
	
if __name__ == "__main__":
	test()
