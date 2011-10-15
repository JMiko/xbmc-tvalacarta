# -*- coding: iso-8859-1 -*-

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import xbmctools

xbmc.output("[channelselector.py] init")

DEBUG = True
if xbmctools.getPluginSetting("thumbnail_type")=="0":
	IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' ) )
else:
	IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'banners' ) )


#57=DVD Thumbs
#xbmc.executebuiltin("Container.SetViewMode(57)")
#50=full list
#xbmc.executebuiltin("Container.SetViewMode(50)")
#51=list
#xbmc.executebuiltin("Container.SetViewMode(51)")
#53=icons
#xbmc.executebuiltin("Container.SetViewMode(53)")
#54=wide icons
#xbmc.executebuiltin("Container.SetViewMode(54)")

def listchannels(params,url,category):
	xbmc.output("[channelselector.py] listchannels")

	# Verifica actualizaciones solo en el primer nivel
	if xbmctools.getPluginSetting("updatecheck2") == "true":
		xbmc.output("updatecheck2=true")
		import updater
		updater.checkforupdates()
	else:
		xbmc.output("updatecheck2=false")

#Lo pongo arriba para debuguear m�s facil, @jesus ponlo luego donde veas mejor.
	addfolder("Cinetube","cinetube","mainlist")
	addfolder("Peliculasyonkis","peliculasyonkis","mainlist")
	addfolder("Divx Online","divxonline","mainlist") # added by ermanitu
	addfolder("Cinegratis","cinegratis","mainlist")
	addfolder("tumejortv.com","tumejortv","mainlist")
	addfolder("Peliculas21","peliculas21","mainlist")
	addfolder("Dospuntocerovision","dospuntocerovision","mainlist")
	addfolder("Cine15","cine15","mainlist")
	#addfolder("SesionVIP","sesionvip","mainlist")
	addfolder("Peliculasid","peliculasid","mainlist")
	addfolder("Cinegratis24h","cinegratis24h","mainlist")
	addfolder("FilmesOnlineBr [Portugues]","filmesonlinebr","mainlist")
	addfolder("TVShack.net (VO)","tvshack","mainlist")
	addfolder("DeLaTV","delatv","mainlist")
	addfolder("Pelis24","pelis24","mainlist")
	addfolder("Veocine","veocine","mainlist")
	addfolder("Pintadibujos","pintadibujos","mainlist")
	addfolder("PeliculasEroticas","peliculaseroticas","mainlist")
	if xbmctools.getPluginSetting("enableadultmode") == "true":
		addfolder("MocosoftX","mocosoftx","mainlist")
	addfolder("Descarga Cine Cl�sico","descargacineclasico","mainlist")
	addfolder("Capitan Cinema","capitancinema","mainlist")
	addfolder("Film Streaming [IT]","filmstreaming","mainlist")
	addfolder("No Megavideo","nomegavideo","mainlist")
	addfolder("Seriesyonkis","seriesyonkis","mainlist","Series") #Modificado por JUR para a�adir la categor�a
	addfolder("Seriespepito","seriespepito","mainlist")
	addfolder("seriesonline.us","seriesonline","mainlist")
	addfolder("Series21","series21","mainlist")
	#addfolder("Newcineonline","newcineonline","mainlist")
	addfolder("CastTV [EN]","casttv","mainlist")
	addfolder("Ver Telenovelas Online","vertelenovelasonline","mainlist")
	addfolder("Anime Foros","animeforos","mainlist")
	addfolder("Yotix.tv","yotix","mainlist")
	addfolder("MCAnime","mcanime","mainlist")
	addfolder("Animetakus","animetakus","mainlist")
	addfolder("Ver-anime","veranime","mainlist")
	addfolder("Watchanimeon [EN]","watchanimeon","mainlist")
	addfolder("Animeid","animeid","mainlist")
	addfolder("Ovasid","ovasid","mainlist")
	addfolder("DocumaniaTV","documaniatv","mainlist")
	addfolder("DocumentariesTV [EN]","documentariestv","mainlist")
	addfolder("Documentalesyonkis","documentalesyonkis","mainlist")
	addfolder("Documentalesatonline","documentalesatonline","mainlist")
	addfolder("Discoverymx.Wordpress","discoverymx","mainlist")
	addfolder("Buscador de Trailers (Youtube)","trailertools","mainlist")
	addfolder("ecartelera (Trailers)","ecarteleratrailers","mainlist")
	addfolder("Stagevu","stagevusite","mainlist")
	addfolder("tu.tv","tutvsite","mainlist")
	addfolder("Megavideo","megavideosite","mainlist")
	addfolder("Megaupload","megauploadsite","mainlist")
	addfolder("Configuracion","configuracion","mainlist")
	addfolder("Descargas","descargados","mainlist")
	addfolder("Favoritos","favoritos","mainlist")
	addfolder("Buscador","buscador","mainlist")
	addfolder("Ayuda","ayuda","mainlist")
	

	#addfolder("Kochikame","kochikame","mainlist")
	#addfolder("PeliculasHD","peliculashd","mainlist")
	#addfolder("Pelis-Sevillista56","sevillista","mainlist")
	#addfolder("Wuapi","wuapisite","mainlist")
	#addfolder("Frozen Layer","frozenlayer","mainlist")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="Canales" )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def addfolder(nombre,channelname,accion,category="Varios"):

	#Si no se indica categor�a poner "Otros" por defecto
	if category == "":
		category = "Otros"
	
	#Preferir cartel en jpg a png (para ir sustituyendo)
	thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".jpg")
	if not os.path.exists(thumbnail):
		thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".png")
	
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , urllib.quote_plus(category) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)