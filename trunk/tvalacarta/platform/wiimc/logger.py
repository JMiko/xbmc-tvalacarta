# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# logger for wiimc
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# TODO:3.1: Log en fichero

def info(texto):
	try:
		texto = unicode(texto,"utf-8")
	except:
		try:
			texto = unicode(texto,"iso-8859-1")
		except:
			pass

	#print texto

def debug(texto):
	try:
		texto = unicode(texto,"utf-8")
	except:
		try:
			texto = unicode(texto,"iso-8859-1")
		except:
			pass

	#print texto

def error(texto):
	try:
		texto = unicode(texto,"utf-8")
	except:
		try:
			texto = unicode(texto,"iso-8859-1")
		except:
			pass

	#print texto
