# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documaniatv.com
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

CHANNELNAME = "documaniatv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[documaniatv.py] init")
tecleadoultimo = ""
DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'documaniatv' ) )
#############----------------------------------------------------------#############

def mainlist(params,url,category):
	xbmc.output("[documaniatv.py] mainlist")
	
	xbmctools.addnewfolder( CHANNELNAME , "documentalesnuevos" , category , "Documentales Online Nuevos","http://www.documaniatv.com/newvideos.html",os.path.join(IMAGES_PATH, 'nuevos.png'),"")
	xbmctools.addnewfolder( CHANNELNAME , "TipoDocumental"   , category , "Tipo de Documental","",os.path.join(IMAGES_PATH, 'tipo.png'),"")
	xbmctools.addnewfolder( CHANNELNAME , "tagdocumentales"  , category , "Tag de Documentales","http://www.documaniatv.com/index.html",os.path.join(IMAGES_PATH, 'tag.png'),"")
	xbmctools.addnewfolder( CHANNELNAME , "toplist"  , category , "Top Documentales Online","http://www.documaniatv.com/topvideos.html",os.path.join(IMAGES_PATH, 'top.png'),"")
	xbmctools.addnewfolder( CHANNELNAME , "listatipodocumental"     , category , "Documentales Siendo Vistos Ahora","http://www.documaniatv.com/index.html",os.path.join(IMAGES_PATH, 'viendose.png'),"")
        xbmctools.addnewfolder( CHANNELNAME , "documentaldeldia"     , category , "Documental del dia","http://www.documaniatv.com/index.html",os.path.join(IMAGES_PATH, 'deldia.png'),"")
	xbmctools.addnewfolder( CHANNELNAME , "search"           , category , "Buscar",tecleadoultimo,os.path.join(IMAGES_PATH, 'search_icon.png'),"")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

################-----------------------------------------------------##############

#def volvermenu(params,url,category):
        #xbmcplugin.openSettings(url=sys.argv[1])
        #xbmc.executebuiltin("Container.Refresh")
        #mainlist(params,url,category)
        # Label (top-right)...
	#xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	#xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

        
##############------------------------------------------------------#################        

def search(params,url,category):
	xbmc.output("[documaniatv.py] search")

        ultimo = params.get("url")
	keyboard = xbmc.Keyboard(ultimo)
        keyboard.doModal()
        
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
                        tecleadoultimo = tecleado
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
                        #keyboard.setHeading(tecleadoultimo)
                        xbmc.output("tecleadoultimo = "+tecleadoultimo)
			searchUrl = "http://www.documaniatv.com/search.php?keywords="+tecleado+"&btn=Buscar"
			searchresults(params,searchUrl,category)



###############---------------------------------------------------#####################

                          

def searchresults(params,url,category):
	xbmc.output("[documaniatv.py] searchresults")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)"[^"]+"([^"]+)"  alt="([^"]+)"[^/]+/><div class="tag".*?</div>[^<]+<span class="artist_name">([^<]+)</span>'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[2]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[1]
		
		# procesa el resto
		scrapedplot = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle+" - "+scrapedplot)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )


                #llama a la rutina paginasiguiente
        cat = 'busca'
        paginasiguientes(patronvideos,url,category,cat)
    
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############		


def TipoDocumental(params, url, category):
        xbmc.output("[documaniatv.py] TipoDocumental")

	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Arte y cine","http://www.documaniatv.com/browse-arte-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Biografia","http://www.documaniatv.com/browse-biografias-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Ciencia y tecnologia","http://www.documaniatv.com/browse-tecnologia-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Deporte","http://www.documaniatv.com/browse-deporte-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "en ingles","http://www.documaniatv.com/browse-ingles-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Historia","http://www.documaniatv.com/browse-historia-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Naturaleza","http://www.documaniatv.com/browse-naturaleza-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Politica","http://www.documaniatv.com/browse-politica-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Social","http://www.documaniatv.com/browse-social-videos-1-date.html","","")
	xbmctools.addnewfolder(CHANNELNAME , "listatipodocumental" , category , "Viajes","http://www.documaniatv.com/browse-viajes-videos-1-date.html","","")
	

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

 





#############--------------------------------------------------------###########
def tagdocumentales(params,url,category):
        xbmc.output("[documaniatv.py] tagdocumentales")

        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "2gm","http://www.documaniatv.com/tags/2gm/","","")
	xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "la2","http://www.documaniatv.com/tags/la2/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category ,"tve","http://www.documaniatv.com/tags/tve/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "ciencia","http://www.documaniatv.com/tags/ciencia/","","") 
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "usa","http://www.documaniatv.com/tags/usa/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "ovnis","http://www.documaniatv.com/tags/ovnis/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "history channel","http://www.documaniatv.com/tags/history-channel/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category ,"egipto","http://www.documaniatv.com/tags/history-channel/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "national geographic","http://www.documaniatv.com/tags/national-geographic/","","") 
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "discovery channel","http://www.documaniatv.com/tags/discovery-channel/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "bbc","http://www.documaniatv.com/tags/bbc/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "politica","http://www.documaniatv.com/tags/politica/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category ,"historia","http://www.documaniatv.com/tags/historia/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "biografias","http://www.documaniatv.com/tags/biografias/","","") 
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "guerra mundial","http://www.documaniatv.com/tags/guerra-mundial/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "cuatro","http://www.documaniatv.com/tags/cuatro/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "españa","http://www.documaniatv.com/tags/espana/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category ,"social","http://www.documaniatv.com/tags/social/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "noche tematica","http://www.documaniatv.com/tags/noche-tematica/","","") 
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "redes","http://www.documaniatv.com/tags/redes/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "GUERRA","http://www.documaniatv.com/tags/guerra/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "tecnologia","http://www.documaniatv.com/tags/tecnologia/","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category ,"viaje","http://www.documaniatv.com/tags/viajes","","")
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "naturaleza","http://www.documaniatv.com/tags/naturaleza/","","") 
        xbmctools.addnewfolder(CHANNELNAME , "tagdocumentaleslist" , category , "nazis","http://www.documaniatv.com/tags/nazis/","","")
 

        # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

       
############---------------------------------------------------------###########
def listatipodocumental(params,url,category):
	xbmc.output("[documaniatv.py] listatipodocumental")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	#</script></center><br>
		
#<a href="http://www.documaniatv.com/historia/caballeros-templarios-la-defensa-de-tierra-santa-video_1b90a4ba0.html">
#			<img src="http://www.documaniatv.com/uploads/thumbs/1b90a4ba0-1.jpg"  alt="Caballeros templarios: La defensa de tierra santa" class="imag" #width="116" height="87" /><div class="tag"><span class="new">new</span></div>
#			<span class="artist_name">Historia</span> Caballeros templarios: La defensa de tierra santa
#			</a>
#
#			</div>
#			</li>
#			<li class="video">
#			<div class="video_i">
#			<a href="http://www.documaniatv.com/historia/cronicas-la-guerra-que-nos-contaron-video_bbb9c3a21.html">
#			<img src="http://4.bp.blogspot.com/_w_xVhyISDmk/StprFkppZyI/AAAAAAAAC88/Zy6hE2-T5BI/s320/Cronicas+-+La+guerra+que+no+nos+contaron+%#28Reportaje+TVE+del+11-10-09%29+%5BDVBRip%5D%5Bxvid-mp3%5D.48m.jpg"  alt="Cronicas: La guerra que nos contaron" class="imag" width="116" height="87" /><div #class="tag"></div>
#			<span class="artist_name">Historia</span> Cronicas: La guerra que nos contaron
#			</a>

#			</div>

        if url == "http://www.documaniatv.com/index.html":
	        patronvideos = '<li class="item">[^<]+<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)" class="imag".*?/></a>'
                cat = "viendose"
        else:  
	        patronvideos  = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)"[^"]+"([^"]+)"  alt="([^"]+)"[^/]+/><div class="tag".*?</div>[^<]+<span class="artist_name">([^<]+)</span>'
                cat = "tipo"
			
			
	#patronvideos += '>.*?<img src="([^"]+)">'
        #patronvideos += 'alt="([^"]+)".*?<span class="'
        #patronvideos += 'artist_name">([^<]+)</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
        #xbmc.output("matches = "+matches[0])
        scrapedplot = ""
	for match in matches:
		# Titulo
		scrapedtitle = match[2]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[1]
		
		# procesa el resto
                if cat == "tipo":
		   scrapedplot = match[3]
                else:
                   for campo in re.findall("/(.*?)/",match[0]):
                        scrapedplot = campo
		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )
  ####  -------------------------------------------
 #         Busqueda de la siguiente pagina
        
        if cat == "tipo":
               patron_pagina_sgte = '</span><a href="([^"]+)"'
               paginasiguientes(patron_pagina_sgte,data,category,cat)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

##############---------------------------------------------------------##############

def documentalesnuevos(params,url,category):
	xbmc.output("[documaniatv.py] DocumentalesNuevos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)


	
	patronvideos  = '<tr><td.*?a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)".*?width="250">([^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#xbmc.output("matches = "+str(matches))
        if DEBUG:
                scrapertools.printMatches(matches)
	for match in matches:
		# Titulo
		# Titulo
		scrapedtitle = match[2]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[1]
		imagen = ""
		# procesa el resto
		scrapeddescription = match[3]
                tipo = match[3]

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		        xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle+" - "+tipo, scrapedurl , scrapedthumbnail, "detail" )
        

        # Busca enlaces de paginas siguientes...
        cat = "nuevo"
        patronvideo = patronvideos
        paginasiguientes(patronvideo,data,category,cat)     

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
##########---------------------------------------------------------------#############
def documentaldeldia(params,url,category):
#	list(params,url,category,patronvideos)
        xbmc.output("[documaniatv.py] Documentaldeldia")
               
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
        
        patronvideos = 'Documental del dia:<br> <a href="([^"]+)">([^<]+)</a>'
        matches =  re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        for match in matches:
		# Titulo
		# Titulo
		scrapedtitle = match[1]

		# URL
		scrapedurl = match[0]
                  
	        # Thumbnail
		scrapedthumbnail = ""

                # scrapedplot
                scrapedplot = ""
                if (DEBUG):
                        xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
 
                xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot ) 
        # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True ) 

################---------------------------------------------------------###########





def tagdocumentaleslist(params,url,category):
	xbmc.output("[documaniatv.py] tagdocumentaleslist")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)



	# Extrae los tag de los documentales
	patronvideos = '<li class="video">[^<]+<div class="video_i">[^<]+<a href="([^"]+)"[^"]+"([^"]+)"  alt="([^"]+)"[^/]+/><div class="tag".*?</div>[^<]+<span class="artist_name">([^<]+)</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

         

	for match in matches:
		# Titulo
		scrapedtitle = match[2]

		# URL
		scrapedurl = match[0]
		
		# Thumbnail
		scrapedthumbnail = match[1]
		
                # procesa el resto
		scrapeddescription = match[3]

		# procesa el resto
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle+" - "+scrapeddescription , scrapedurl , scrapedthumbnail , scrapedplot )

        #Busca la pagina siguiente
        cat = "tag"
        patronvideo = patronvideos
        paginasiguientes(patronvideo,data,category,cat)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############

def toplist(params,url,category):
	xbmc.output("[documaniatv.py] list")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)




	# Extrae las entradas (carpetas)
	patronvideos = '<tr>[^>]+>([^<]+)</td>[^>]+><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"[^>]+></a></td>[^>]+>([^<]+)</td>[^>]+><a href="[^"]+">[^>]+></td>[^>]+>([^<]+)</td>'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[3]

		# URL
		scrapedurl = match[1]
		
		# Thumbnail
		scrapedthumbnail = match[2]
		
		# procesa el resto
		scrapedplot = match[4]+" - " + "Vistas : "+match[5]+" veces"

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		#        xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "directo" , match[0]+") "+scrapedtitle + " - " + scrapedplot , scrapedurl , scrapedthumbnail , scrapedplot )

                xbmctools.addthumbnailfolder( CHANNELNAME , match[0]+") "+scrapedtitle+" - "+scrapedplot, scrapedurl , scrapedthumbnail, "detail" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

#############----------------------------------------------------------#############

def detail(params,url,category):
	xbmc.output("[documaniatv.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	thumnbail = thumbnail
	xbmc.output("[prueba.py] title="+title)
	xbmc.output("[prueba.py] thumbnail="+thumbnail)
        patrondescrip = '<h3>Descripcion</h3>(.*?)<br><br><script'
	# Descarga la página
	data = scrapertools.cachePage(url)
	descripcion = ""
        plot = ""
        matches = re.compile(patrondescrip,re.DOTALL).findall(data)
        if DEBUG:
          if len(matches)>0:
		descripcion = matches[0]
		descripcion = descripcion.replace("&nbsp;","")
		descripcion = descripcion.replace("<br/>","")
		descripcion = descripcion.replace("\r","")
		descripcion = descripcion.replace("\n"," ")
		descripcion = re.sub("<[^>]+>"," ",descripcion)
                xbmc.output("descripcion="+descripcion)
                descripcion = descripcion.replace("Ã‚Â", "")
                descripcion = descripcion.replace("ÃƒÂ©","é")
                descripcion = descripcion.replace("ÃƒÂ¡","á")
                descripcion = descripcion.replace("ÃƒÂ³","ó")
                descripcion = descripcion.replace("ÃƒÂº","ú")
                descripcion = descripcion.replace("ÃƒÂ­","í")
                xbmc.output("descripcion="+descripcion)
                try :
                    plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
                except:
                    plot = descripcion
	# ----------------------------------------------------------------------------
	# Busca los enlaces a los videos de : "Megavideo"
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
                
        #       titulo = title.replace("%28"," ")
        #       titulo = titulo.replace("%29"," ")
        #	xbmctools.addvideo( CHANNELNAME , video[0], video[1] , category ,         #plot )
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Megavideo" , title.strip().replace("(Megavideo)","").replace("+"," ") +" - "+video[0]  , video[1] ,thumbnail, plot )
       # xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , match[1] , match[0] , thumbnail , plot )
	# ------------------------------------------------------------------------------------
       #  ---- Extrae los videos directos ----- 

       # Extrae los enlaces a los vídeos (Directo)
        patronvideos = "file: '([^']+)'"
        servidor = "Directo"
        extraevideos(patronvideos,data,category,title+" - directo",thumbnail,plot,servidor)
       # ---------------------------------------




       #  --- Extrae los videos de veoh  ----
        patronvideos = 'var embed_code[^>]+>   <param name="movie" value="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf.*?permalinkId=(.*?)&player=videodetailsembedded&videoAutoPlay=0&id=anonymous"></param>'
        servidor = "Veoh"
        extraevideos(patronvideos,data,category,title+" - Video en Veoh no funciona de momento",thumbnail,plot,servidor)
       # ---------------------------------------


         
#var embed_code =  '<embed id="VideoPlayback" src="http://video.google.com/googleplayer.swf?docid=1447612366747092264&hl=en&fs=true" style="width:496px;height:401px" allowFullScreen="true" allowScriptAccess="always" type="application/x-shockwave-flash" wmode="window">  </embed>' ;

       #  --- Extrae los videos de google  ----
        patronvideos = '<embed id="VideoPlayback" src="http://video.google.com/googleplayer.swf.*?docid=(.*?)&hl=en&'
        servidor = "Google"
        extraevideos(patronvideos,data,category,title+" - Video en google",thumbnail,plot,servidor)
       # --------------------------------------- 

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

#############----------------------------------------------------------#############

def extraevideos(patronvideos,data,category,title,thumbnail,plot,servidor):
	xbmc.output("patron="+patronvideos)
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)		

        if len(matches)>0 :
		# Añade al listado de XBMC
              if servidor == "Directo":
                   
		   xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title, matches[0] , thumbnail , plot )

              elif servidor == "Veoh":
                   veohurl = "http://www.flashvideodownloader.org/download.php?u=http://www.veoh.com/browse/videos/category/entertainment/watch/"+matches[0]
                   xbmc.output(" veohurl = " +veohurl) 
                   veohdata = scrapertools.cachePage(veohurl)
                   newpatron = '><a href="(.*?)" title="Click to Download"><font color=red>'
                   newmatches = re.compile(newpatron,re.DOTALL).findall(veohdata)
                   if len(newmatches)>0:
                     xbmc.output(" newmatches = "+newmatches[0])
                     xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title, newmatches[0] , thumbnail , plot )

              elif servidor == "Google":
                   url = "http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+matches[0]
                   xbmc.output(" Url = "+url)
                   data = scrapertools.cachePage(url)
                   newpatron = '<a href="(.*?)" title="Click to Download">'
                   newmatches = re.compile(newpatron,re.DOTALL).findall(data)
                   if len(newmatches)>0:
                      xbmc.output(" newmatches = "+newmatches[0])
                      xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title, newmatches[0] , thumbnail , plot )  
#############----------------------------------------------------------#############

def play(params,url,category):
	xbmc.output("[documaniatv.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
        plot = urllib.unquote_plus( params.get("plot") )

        try:
	    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
        except:
            plot = xbmc.getInfoLabel( "ListItem.Plot" )

        server = params["server"]
	xbmc.output("[documaniatv.py] thumbnail="+thumbnail)
	xbmc.output("[documaniatv.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)


#############----------------------------------------------------------#############

def paginasiguientes(patronvideos,data,category,cat):

# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	patron    = '</span><a href="([^"]+)"' 
	matches   = re.compile(patron,re.DOTALL).findall(data)
        #menutitle = "Volver Al Menu Principal"
        #menurl    = "http://www.documaniatv.com/"
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = "http://www.documaniatv.com/" + match
		scrapedthumbnail = os.path.join(IMAGES_PATH, 'next.png')
		scrapeddescription = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

                if cat == 'tipo':   
		# Añade al listado de XBMC
		        xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "listatipodocumental" )
                elif cat == 'nuevo':
                        xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "documentalesnuevos" )
                elif cat == 'tag':
                        xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , "http://www.documaniatv.com"+match , scrapedthumbnail, "tagdocumentaleslist" )
                elif cat == 'busca':
                        xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "searchresults" )
                       

        #xbmctools.addthumbnailfolder( CHANNELNAME , menutitle , menurl , "", "volvermenu" )
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
  
