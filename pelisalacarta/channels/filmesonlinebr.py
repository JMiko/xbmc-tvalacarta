# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para - Filmes Online BR
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

CHANNELNAME = "filmesonlinebr"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[filmesonlinebr.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[filmesonlinebr.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ultimos Filmes Subidos"    ,"http://www.filmesonlinebr.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listalfa" , category , "Lista Alfabética","http://www.filmesonlinebr.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Series","http://www.filmesonlinebr.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategorias" , category , "Categorias"        ,"http://www.filmesonlinebr.com/","","")
	if xbmcplugin.getSetting("enableadultmode") == "true":
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Filmes Adulto (+18)","http://www.filmesonlinebr.com/search/label/Filmes%20Adulto%20%28%2B18%29","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listcategorias(params,url,category):
	xbmc.output("[filmeonlinebr.py] listcategorias")


	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ação"    ,"http://www.filmesonlinebr.com/search/label/A%C3%A7%C3%A3o","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Aventura"    ,"http://www.filmesonlinebr.com/search/label/Aventura","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Comédia Romântica"    ,"http://www.filmesonlinebr.com/search/label/Com%C3%A9dia%20Rom%C3%A2ntica","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Comédia"    ,"http://www.filmesonlinebr.com/search/label/Com%C3%A9dia","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Documentário"    ,"http://www.filmesonlinebr.com/search/label/Document%C3%A1rio","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Drama"    ,"http://www.filmesonlinebr.com/search/label/Drama","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ficção Científica"    ,"http://www.filmesonlinebr.com/search/label/Fic%C3%A7%C3%A3o%20Cient%C3%ADfica","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Guerra"    ,"http://www.filmesonlinebr.com/search/label/Guerra","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Lançamentos 2010"    ,"http://www.filmesonlinebr.com/search/label/Lan%C3%A7amentos%202010","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Musical e Shows"    ,"http://www.filmesonlinebr.com/search/label/Musical","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Filmes Brasileiros"    ,"http://www.filmesonlinebr.com/search/label/Nacional","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Policial"    ,"http://www.filmesonlinebr.com/search/label/Policial","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Romance"    ,"http://www.filmesonlinebr.com/search/label/Romance","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Suspense"    ,"http://www.filmesonlinebr.com/search/label/Suspense","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Terror"    ,"http://www.filmesonlinebr.com/search/label/Terror","","")
	
    # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
        
def listalfa(params,url,category):
	xbmc.output("[filmesonlinebr.py] listalfa")
	
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "0-9","http://www.filmesonlinebr.com/search/label/0-9/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "A","http://www.filmesonlinebr.com/search/label/a/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "B","http://www.filmesonlinebr.com/search/label/B/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "C","http://www.filmesonlinebr.com/search/label/C/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "D","http://www.filmesonlinebr.com/search/label/D/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "E","http://www.filmesonlinebr.com/search/label/E/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "F","http://www.filmesonlinebr.com/search/label/F/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "G","http://www.filmesonlinebr.com/search/label/G/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "H","http://www.filmesonlinebr.com/search/label/H/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "I","http://www.filmesonlinebr.com/search/label/I/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "J","http://www.filmesonlinebr.com/search/label/J/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "K","http://www.filmesonlinebr.com/search/label/K/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "L","http://www.filmesonlinebr.com/search/label/L/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "M","http://www.filmesonlinebr.com/search/label/M/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "N","http://www.filmesonlinebr.com/search/label/N/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "O","http://www.filmesonlinebr.com/search/label/O/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "P","http://www.filmesonlinebr.com/search/label/P/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "Q","http://www.filmesonlinebr.com/search/label/Q/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "R","http://www.filmesonlinebr.com/search/label/R/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "S","http://www.filmesonlinebr.com/search/label/S/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "T","http://www.filmesonlinebr.com/search/label/T/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "U","http://www.filmesonlinebr.com/search/label/U/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "V","http://www.filmesonlinebr.com/search/label/V/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "W","http://www.filmesonlinebr.com/search/label/W/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "X","http://www.filmesonlinebr.com/search/label/X/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "Y","http://www.filmesonlinebr.com/","","","")
	xbmctools.addnewfolderextra( CHANNELNAME ,"listvideos", category , "Z","http://www.filmesonlinebr.com/search/label/Z/","","","")

        # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
	
def listvideos(params,url,category):
	xbmc.output("[filmesonlinebr.py] listvideos")
	adulto = xbmcplugin.getSetting("enableadultmode")
	if url=="":
		url = "http://www.peliculasid.com/"
                
	# Descarga la página
	data = scrapertools.cachePage(url)
	# Extrae la parte localizada del filme
	patronfilme  ='(<a onblur="try.*?[</embed></object>|Temporada]+.*?</h3>)'
	matchesfilme = re.compile(patronfilme,re.DOTALL).findall(data)
	
	
	# Extrae las entradas (videos) #
	
	# patron para: thumbnail , idioma , sinopsis y titulo
	patronthumb    = 'src="([^"]+)".*?alt='
	patronIdioma   = '>(Audio:|Idioma:)</span>([^<]+)<br />'
	patronSinopsis = '(<div><b>.*?|Sinopse.*?)<param name=.*?'
	patrontitle   = "<a href='[^']+'>([^<]+)</a>"
	
	# patron para los video de megavideo
	patronmega = 'http\:\/\/www.megavideo.com\/([\?v=|v/|\?d=]+)([A-Z0-9]{8}).*?'
	
	
	
	
	
	for match in matchesfilme:
		data1 = match.replace("\n","").replace("\r","")
		matchthumb = re.compile(patronthumb,re.DOTALL).findall(data1)
		matchIdioma = re.compile(patronIdioma,re.DOTALL).findall(data1)
		matchSinopsis = re.compile(patronSinopsis,re.DOTALL).findall(data1)
		matchtitle      = re.compile(patrontitle,re.DOTALL).findall(data1) # thumbnail , Idioma , Sinopsis y Titulo
		print 'video encontrado : %s' % matchtitle
		#print 'onblur %s' % match
		scrapertools.printMatches(matchthumb)
		scrapertools.printMatches(matchIdioma)
		scrapertools.printMatches(matchSinopsis)
		scrapertools.printMatches(matchtitle)
		matchmega    = re.compile(patronmega,re.DOTALL).findall(data1)   # Video en Megavideo
		print 'megavideo encontradoooo : %s' % str(len(matchmega))
		
		# Titulo
		for match1 in matchtitle:
			scrapedtitle = match1
			scrapedtitle = scrapedtitle.replace("&#8211;","-")
		for j in ["S\xc3\xa9ries","Serie","Anime"]:
			if j in scrapedtitle:
				matchmega = []
		if adulto == "false":
			for i in ["xxx","Porno","XXX"]:
				if  i  in scrapedtitle:
					matchmega = []
		
		
		# URL
		#scrapedurl = urlparse.urljoin(url,match1[0])
		# Thumbnail
		for match1 in matchthumb:
			scrapedthumbnail = match1
		#scrapedthumbnail = scrapedthumbnail.replace(" ","")
		# Argumento
		scrapedplot = ""
		for matchId in matchIdioma:
			scrapedplot = "Idioma : " + matchId[1] + "\n"
		for matchS in matchSinopsis:
			scrapedplot += matchS.replace("&#8211;","-")
			
		scrapedplot  = re.sub("<[^>]+>"," ",scrapedplot)
		if len(matchmega)>0:
			encontrados = set()
			c = 0
			title = scrapedtitle
			for match2 in matchmega:
				if match2[1] not in encontrados:
					c = c + 1
					encontrados.add(match2[1])
					for i in ["xxx","Porno","XXX"]:
						if  i  in scrapedtitle:
							scrapedtitle = title + " cd" + str(c)
					if "Desenhos" in scrapedtitle:
						scrapedtitle = title + " - Ep " + str(c)
						
					# Link
					scrapedurl = match2[1]
					if  "v" in match2[0]:
						server = "Megavideo"
					else:
						server = "Megaupload"
					# Depuracion
					if (DEBUG):
						xbmc.output("scrapedtitle="+scrapedtitle)
						xbmc.output("scrapedurl="+scrapedurl)
						xbmc.output("scrapedthumbnail="+scrapedthumbnail)

					# Añade al listado de XBMC
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , server, scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
			
				
	# Extrae la marca de siguiente página
	patronvideos  = "<a class='blog-pager-older-link' href='([^']+)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )


def play(params,url,category):
	xbmc.output("[filmesonlinebr.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def acentos(title):

        title = title.replace("Ã‚Â", "")
        title = title.replace("ÃƒÂ©","é")
        title = title.replace("ÃƒÂ¡","á")
        title = title.replace("ÃƒÂ³","ó")
        title = title.replace("ÃƒÂº","ú")
        title = title.replace("ÃƒÂ­","í")
        title = title.replace("ÃƒÂ±","ñ")
        title = title.replace("Ã¢â‚¬Â", "")
        title = title.replace("Ã¢â‚¬Å“Ã‚Â", "")
        title = title.replace("Ã¢â‚¬Å“","")
        title = title.replace("Ã©","é")
        title = title.replace("Ã¡","á")
        title = title.replace("Ã³","ó")
        title = title.replace("Ãº","ú")
        title = title.replace("Ã­","í")
        title = title.replace("Ã±","ñ")
        title = title.replace("Ãƒâ€œ","Ó")
        return(title)