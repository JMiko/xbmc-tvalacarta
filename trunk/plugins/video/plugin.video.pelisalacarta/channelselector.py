# -*- coding: iso-8859-1 -*-

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import config
import logger
import parametrizacion

DEBUG = True

CHANNELNAME = "channelselector"

if config.getSetting("thumbnail_type")=="0":
	IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' ) )
else:
	IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'banners' ) )

if config.getSetting("thumbnail_type")=="0":
	WEB_PATH = "http://www.mimediacenter.info/xbmc/pelisalacarta/posters/"
else:
	WEB_PATH = "http://www.mimediacenter.info/xbmc/pelisalacarta/banners/"

def listchannels(params,url,category):
	logger.info("[channelselector.py] listchannels")

	# Verifica actualizaciones solo en el primer nivel
	try:
		import updater
	except ImportError:
		logger.info("[channelselector.py] No disponible modulo actualizaciones")
	else:
		if config.getSetting("updatecheck2") == "true":
			logger.info("[channelselector.py] Verificar actualizaciones activado")
			updater.checkforupdates()
		else:
			logger.info("[channelselector.py] Verificar actualizaciones desactivado")

	addfolder(config.getLocalizedString(30118),CHANNELNAME,"mainlist")
	addfolder(config.getLocalizedString(30102),"favoritos","mainlist")     # Favoritos
	if (parametrizacion.DOWNLOAD_ENABLED):
		addfolder(config.getLocalizedString(30101),"descargados","mainlist")   # Descargas
	addfolder(config.getLocalizedString(30100),"configuracion","mainlist") # Configuracion
	addfolder(config.getLocalizedString(30104),"ayuda","mainlist")         # Ayuda

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def mainlist(params,url,category):
	catlist = [config.getLocalizedString(30121),config.getLocalizedString(30122),config.getLocalizedString(30123),config.getLocalizedString(30124),config.getLocalizedString(30125),config.getLocalizedString(30126),config.getLocalizedString(30103),"Megavideo ("+config.getLocalizedString(30127)+")","Megaupload ("+config.getLocalizedString(30127)+")"]
	catlistv = ["","F","S","A","D","M","B","V","U"]
	langlist = [config.getLocalizedString(30121),config.getLocalizedString(30129),config.getLocalizedString(30130),config.getLocalizedString(30131),config.getLocalizedString(30132)+" (BR)"]
	langlistv = ["","ES","EN","IT","BR"]

	channelslist = channels_list()

	listfilters = [ [ config.getLocalizedString(30119) , catlist ,  catlistv , "" ] , [ config.getLocalizedString(30120) , langlist ,  langlistv , "" ] ]
	for filter in listfilters:
		n = listfilters.index(filter)
		searchtype = xbmcgui.Dialog()
		seleccion = searchtype.select(filter[0]+":",filter[1])
		if n==0:
			if seleccion>5:
				category = filter[1][seleccion]
			else:
				category = config.getLocalizedString(30118)
		if seleccion<=0:
			continue

		filter[3] = filter[2][seleccion]

		if config.getLocalizedString(30118) in category:
			category = category+" - "+filter[1][seleccion]
		if n==0:
			if seleccion>5:
				break
			elif seleccion>0:
				#Check: orden alfabético salvo en el listado completo
				#channelslist.sort()
				#Con Stagevu (Check: disponible para todos los idiomas y categorías)
				#no es patente el filtrado de idiomas por categorías...
				langlistf = [config.getLocalizedString(30121)]
				langlistvf = [""]
				for lang in langlistv:
					if lang=="":
						continue
					n=langlistv.index(lang)
					for channel in channelslist:
						if filter[3] in channel[4] and lang in channel[3]:
							langlistvf.append(lang)
							langlistf.append(langlist[n])
							break
				listfilters[1][1]=langlistf
				listfilters[1][2]=langlistvf

	catv = listfilters[0][3]
	idiomav = listfilters[1][3]

	for channel in channelslist:
		if catv<>"" and catv not in channel[4]:
			continue
		if idiomav<>"" and idiomav not in channel[3]:
			continue
		addfolder(channel[0] , channel[1] , "mainlist" , channel[2])
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def channels_list():
	channelslist = []
	channelslist.append([ "Cinetube" , "cinetube" , "" , "ES" , "F" ])
	channelslist.append([ "Peliculasyonkis" , "peliculasyonkis" , "" , "ES" , "F" ])
	#channelslist.append([ "Divx Online" , "divxonline" , "" , "ES" , "F" ]) # added by ermanitu
	channelslist.append([ "Cinegratis" , "cinegratis" , "" , "ES" , "F,S,A,D" ])
	channelslist.append([ "tumejortv.com" , "tumejortv" , "" , "ES" , "F,S" ])
	channelslist.append([ "Peliculas21" , "peliculas21" , "" , "ES" , "F" ])
	channelslist.append([ "Dospuntocerovision" , "dospuntocerovision" , "" , "ES" , "F,S" ])
	channelslist.append([ "Cine15" , "cine15" , "" , "ES" , "F" ])
	#channelslist.append([ "Eduman Movies" , "edumanmovies" , "" , "ES" , "F" ])
	#channelslist.append([ "SesionVIP" , "sesionvip" , "" , "ES" , "F" ])
	channelslist.append([ "Peliculasid" , "peliculasid" , "" , "ES" , "F" ])
	channelslist.append([ "Cinegratis24h" , "cinegratis24h" , "" , "ES" , "F" ])
	channelslist.append([ "Cine-Adicto" , "cineadicto" , "" , "ES" , "F,D" ])
	channelslist.append([ "PelisFlv" , "pelisflv" , "" , "ES" , "F" ])  
	channelslist.append([ "NoloMires" , "nolomires" , "" , "ES" , "F" ])
	channelslist.append([ "NewDivx" , "newdivx" , "" , "ES" , "F,D" ])
	channelslist.append([ "Peliculas Online FLV" , "peliculasonlineflv" , "" , "ES" , "F,D" ])
	#channelslist.append([ "Pelis-Sevillista56" , "sevillista" , "" , "ES" , "F" ])
	channelslist.append([ "FilmesOnlineBr [Portugues]" , "filmesonlinebr" , "" , "BR" , "F" ])
	channelslist.append([ "TVShack.cc (VO)" , "tvshack" , "" , "EN" , "F,S,A,D,M" ])
	channelslist.append([ "DeLaTV" , "delatv" , "" , "ES" , "F" ])
	channelslist.append([ "Pelis24" , "pelis24" , "" , "ES" , "F,S" ])
	channelslist.append([ "Veocine" , "veocine" , "" , "ES" , "F,A,D" ])
	channelslist.append([ "Pintadibujos" , "pintadibujos" , "" , "ES" , "F,A" ])
	channelslist.append([ "Pelis Pekes" , "pelispekes" , "" , "ES" , "F,A" ])
	channelslist.append([ "Descarga Cine Clásico" , "descargacineclasico" , "" , "ES" , "F,S" ])
	channelslist.append([ "Capitan Cinema" , "capitancinema" , "" , "ES" , "F" ])
	channelslist.append([ "Film Streaming [IT]" , "filmstreaming" , "" , "IT" , "F,A" ])
	channelslist.append([ "No Megavideo" , "nomegavideo" , "" , "ES" , "F" ])
	channelslist.append([ "LetMeWatchThis" , "letmewatchthis" , "" , "EN" , "F,S" ])
	channelslist.append([ "Cineblog01" , "cineblog01" , "" , "IT" , "F,S,A" ])
	if config.getSetting("enableadultmode") == "true":
		channelslist.append([ "PeliculasEroticas" , "peliculaseroticas" , "" , "ES" , "F" ])
		channelslist.append([ "MocosoftX" , "mocosoftx" , "" , "ES" , "F" ])
		channelslist.append([ "Anifenix.com" , "anifenix" , "" , "ES" , "F" ])
		channelslist.append([ "tuporno.tv" , "tupornotv" , "" , "ES" , "F" ])
	channelslist.append([ "Seriesyonkis" , "seriesyonkis" , "Series" , "ES" , "S,A" ]) #Modificado por JUR para añadir la categoría
	channelslist.append([ "Seriespepito" , "seriespepito" , "" , "ES" , "S" ])
	#channelslist.append([ "seriesonline.us" , "seriesonline" , "" , "ES" , "S" ])
	channelslist.append([ "Series21" , "series21" , "" , "ES" , "S" ])
	channelslist.append([ "DeLaTV Series" , "bancodeseries" , "" , "ES" , "S" ])
	#channelslist.append([ "Newcineonline" , "newcineonline" , "" , "ES" , "S" ])
	channelslist.append([ "CastTV" , "casttv" , "" , "ES,EN" , "S" ])
	channelslist.append([ "Ver Telenovelas Online" , "vertelenovelasonline" , "" , "ES" , "S" ])
	channelslist.append([ "Anime Foros" , "animeforos" , "" , "ES", "A" ])
	channelslist.append([ "Yotix.tv" , "yotix" , "" , "ES" , "A" ])
	channelslist.append([ "MCAnime" , "mcanime" , "" , "ES" , "A" ])
	channelslist.append([ "Animetakus" , "animetakus" , "" , "ES" , "A" ])
	channelslist.append([ "Ver-anime" , "veranime" , "" , "ES" , "A" ])
	channelslist.append([ "Watchanimeon [EN]" , "watchanimeon" , "" , "EN" , "A" ])
	channelslist.append([ "Animeid" , "animeid" , "" , "ES" , "A" ])
	channelslist.append([ "Ovasid" , "ovasid" , "" , "ES" , "A" ])
	channelslist.append([ "dibujosanimadosgratis.net" , "dibujosanimadosgratis" , "" , "ES" , "A" ])
	channelslist.append([ "DocumaniaTV" , "documaniatv" , "" , "ES" , "D" ])
	channelslist.append([ "DocumentariesTV [EN]" , "documentariestv" , "" , "EN", "D" ])
	channelslist.append([ "Documentalesyonkis" , "documentalesyonkis" , "" , "ES" , "D" ])
	channelslist.append([ "Documentalesatonline" , "documentalesatonline" , "" , "ES" , "D" ])
	channelslist.append([ "Discoverymx.Wordpress" , "discoverymx" , "" , "ES" , "D" ])
	channelslist.append([ "Gratisdocumentales" , "gratisdocumentales" , "" , "ES" , "D" ])
	channelslist.append([ "Redes.tv" , "redestv" , "" , "ES" , "D" ])
	channelslist.append([ config.getLocalizedString(30128)+" (Youtube)" , "trailertools" , "" , "ES,EN,IT,BR" , "F" ])
	channelslist.append([ "ecartelera (Trailers)" , "ecarteleratrailers" , "" , "ES,EN" , "F" ])
	channelslist.append([ "Stagevu" , "stagevusite" , "" , "ES,EN,IT,BR" , "F,S,A,D,M" ]) #Check: Idiomas y Categorías
	channelslist.append([ "tu.tv" , "tutvsite" , "" , "ES", "F,S,A,D,M" ])
	searchwebs=": Cinetube,Peliculasyonkis,Cinegratis,tumejortv.com,Peliculas21,Cine15,Seriesyonkis,Yotix.tv,DocumaniaTV,Discoverymx,Stagevu,tu.tv"
	channelslist.append([ config.getLocalizedString(30103)+searchwebs , "buscador" , "Buscador" , "" , "B" ])# Buscador
	channelslist.append([ "Megavideo ("+config.getLocalizedString(30127)+")" , "megavideosite" , "" , "" , "V" ])
	channelslist.append([ "Megaupload ("+config.getLocalizedString(30127)+")" , "megauploadsite" , "" , "" , "U" ])

	#channelslist.append([ "PeliculasHD" , "peliculashd" , "" , "ES" , "F" ])
	#channelslist.append([ "Wuapi" , "wuapisite" , "" , "ES" , "F" ])
	#channelslist.append([ "Frozen Layer" , "frozenlayer" , "" , "ES" , "A" ])
	return channelslist

def addfolder(nombre,channelname,accion,category=""):
	if category == "":
		try:
			category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
		except:
			pass
	
	# Preferencia: primero JPG
	thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".jpg")
	# Preferencia: segundo PNG
	if not os.path.exists(thumbnail):
		thumbnail = thumbnailImage=os.path.join(IMAGES_PATH, channelname+".png")
	# Preferencia: tercero WEB
	if not os.path.exists(thumbnail):
		thumbnail = thumbnailImage=WEB_PATH+channelname+".png"
	#Si no existe se usa el logo del plugin
	#if not os.path.exists(thumbnail):
	#	thumbnail = thumbnailImage=WEB_PATH+"ayuda.png" #Check: ruta del logo

	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
	itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
