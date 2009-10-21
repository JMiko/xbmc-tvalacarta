import os
import xbmc

ROOT_DIR = os.getcwd()

def readsavedsearches():
	xbmc.output("[savedsearch.py] readsavedsearches")

	# Lee el fichero de configuracion
	searchesfilepath = os.path.join(ROOT_DIR,'searches.txt')
	xbmc.output("[savedsearch.py] searchesfilepath="+searchesfilepath)
	searchesfile = open(searchesfilepath)
	lines = searchesfile.readlines()
	for line in lines:
		xbmc.output("[savedsearch.py] <"+line)
	searchesfile.close();

	return lines

def addsavedsearch(newsearch):
	xbmc.output("[savedsearch.py] addsavedsearch "+newsearch)

	# Lee el fichero de configuracion
	searchesfilepath = os.path.join(ROOT_DIR,'searches.txt')
	xbmc.output("[savedsearch.py] searchesfilepath="+searchesfilepath)
	searchesfile = open(searchesfilepath)
	lines = searchesfile.readlines()
	for line in lines:
		xbmc.output("[savedsearch.py] <"+line)
	searchesfile.close();

	outfile = open(searchesfilepath,"w")

	# Graba todas las búsquedas
	for line in lines:
		if line.strip()!="":
			if line.strip()!=newsearch.strip():
				xbmc.output("[savedsearch.py] >"+line.strip())
				outfile.write(line.strip())
				outfile.write('\n')
			else:
				xbmc.output("[savedsearch.py] omitida "+line.strip())

	# Y esta la última
	xbmc.output("[savedsearch.py] >"+newsearch.strip())
	outfile.write(newsearch.strip())
	outfile.write('\n')
	
	outfile.flush()
	outfile.close()
