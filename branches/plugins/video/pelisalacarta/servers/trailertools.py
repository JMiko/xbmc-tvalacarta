# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Buscador de Trailers en youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os.path
import sys
import xbmc
import scrapertools
import string
import xbmcgui


def gettrailer(titulovideo):
    devuelve = []
    # ---------------------------------------
    #  Busca el video en youtube
    # ---------------------------------------
    
    listyoutubeurl  = "http://www.youtube.com/results?search_query="
    listyoutubeurl += titulovideo.replace(" ","+")+"++trailer+en+espa%C3%B1ol&search_type=&aq=f"
    listyoutubeurl = listyoutubeurl.replace(" ","")
    titulo = re.sub(r'[(0-9)]','',titulovideo)
    titulo = re.sub(' $','',titulo)
    xbmc.output("Titulo del Trailer cortado : "+sinacentos(titulo))
    c = 0
    data = scrapertools.cachePage(listyoutubeurl)
    patronyoutube = '<a class="video-thumb-120" href="(.*?)"   ><img title="(.*?)"    src="(.*?)"'
    matches  = re.compile(patronyoutube,re.DOTALL).findall(data)
    if len(matches)>0:
		
		xbmc.output("Titulo del Trailer a buscar : "+titulovideo)
		for match in matches:
			xbmc.output("Trailer encontrado :  "+match[1])
			
			if (string.lower(sinacentos(titulo))) in (string.lower(sinacentos(match[1]))):
				c = c + 1
				devuelve.append( [match[0], match[1] , match[2]] )
				#scrapedthumbnail = match[2]
				#scrapedtitle     = match[1]
				#scrapedurl       = match[0]
				if c == 6 :
					break
		xbmc.output(" lista de links encontrados U "+str(len(match)))
    if c < 6:
		thumbnail=""
		patronyoutube = '<span><a class="hLink" title="(.*?)" href="(.*?)">'
		matches  = re.compile(patronyoutube,re.DOTALL).findall(data)
		if len(matches)>0:
			for match in matches:
				xbmc.output("Trailer Titulo encontrado :  "+match[0])
				xbmc.output("Trailer Url    encontrado :  "+match[1])
				if (string.lower(sinacentos(titulo))) in (string.lower(sinacentos(match[0]))):
					campo = match[1]
					longitud = len(campo)
					campo = campo[-11:]
					xbmc.output("codigo del video :  "+campo)
					patron    = "(http\:\/\/i[^/]+/vi/"+campo+"/default.jpg)"
					matches2  = re.compile(patron,re.DOTALL).findall(data)
					if len(matches2)>0:
						thumbnail = matches2[0] 
					c = c + 1
					devuelve.append( [match[1], match[0] , thumbnail] )
					#scrapedthumbnail = thumbnail
					#scrapedtitle     = match[0]
					#scrapedurl       = match[1]
					if c == 6 :
						break
			xbmc.output(" lista de links encontrados U "+str(len(match)))
				
		
		
			
			
    return devuelve
    
def trailerbykeyboard(titulo):
	
	keyboard = xbmc.Keyboard('default')
	keyboard.setDefault(titulo)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			return(gettrailer(tecleado))
			
def alertnoencontrado(titulo):
	advertencia = xbmcgui.Dialog()
	resultado = advertencia.yesno('Trailer no encontrado' , 'El Trailer para : "'+titulo+'"' , 'no se ha podido localizar, ','Deseas utilizar el teclado')
	return(resultado)
def sinacentos(title):

        title = title.replace("Â�", "")
        title = title.replace("Ã©","e")
        title = title.replace("Ã¡","a")
        title = title.replace("Ã³","o")
        title = title.replace("Ãº","u")
        title = title.replace("Ã­","i")
        title = title.replace("Ã±","�")
        title = title.replace("â€", "")
        title = title.replace("â€œÂ�", "")
        title = title.replace("â€œ","")
        title = title.replace("é","e")
        title = title.replace("á","a")
        title = title.replace("ó","o")
        title = title.replace("ú","u")
        title = title.replace("í","i")
        title = title.replace("ñ","�")
        title = title.replace("Ã“","O")
        title = title.replace(",","")
        title = title.replace("�","e")
        title = title.replace("�","a")
        title = title.replace("�","o")
        title = title.replace("�","u")
        title = title.replace("�","i")
        title = title.replace('�','n')
        title = title.replace(":","")
        title = title.replace("&","")
        title = title.replace('"','')
        title = title.replace('-','')
        title = title.replace('?','')
        title = title.replace("  "," ")
        return(title)