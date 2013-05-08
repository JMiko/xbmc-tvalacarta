# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para stormtv 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por JuRR
# v0.6
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import xml.dom.minidom as minidom
import urllib
import os,errno
from core import stormlib


__channel__ = "stormtv"
__category__ = "F,S,A"
__type__ = "generic"
__title__ = "stormtv2"
__language__ = "ES"
__server__ = "oc1.lopezepol.com"

DEBUG = config.get_setting("debug")
PREFERENCES  =stormlib.getpreferences()
LANG =stormlib.getlang()
SERVERS =stormlib.getservers()
SERVER = "https://"+__server__+"/stormtv/public/"

def isGeneric():
    return True

def searchtype(item):
	itemlist = []                                                                                                                                                             
        itemlist.append( Item(channel=__channel__, action="search"    , thumbnail=SERVER+"buscar.jpg", title="Buscar", url="",fanart=SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__,action="genresearch",thumbnail=SERVER+"buscar.jpg",title="Buscar por Genero", url="",fanart=SERVER+"logo.jpg"))
	itemlist.append( Item(channel=__channel__,action="yearsearch",thumbnail=SERVER+"buscar.jpg",title="Buscar por AÃ±o", url="",fanart=SERVER+"logo.jpg"))
	return itemlist


def search(item,texto, categoria="*"):
    logger.info("[stormtv.py] search "+texto )
    itemlist = []
    #server= "https://"+__server__+"/stormtv/public/"
    path=config.get_data_path()+"stormtv/temp/"
    if not os.path.exists(path):                                                                                                     
       logger.info("[stormtv.py] search Creating data_path "+path)                                                                       
       try:                                                                                                                          
          os.mkdirs(path)                                                                                                      
       
       except:
       	  logger.info( "[stormtv.py] search fallo crear directorio" )                                                                                                                      
          pass                                           
    urllib.urlretrieve (SERVER+"/tvseries/search/title/"+texto, path+"temp.xml")                             
    xml=path+"/"+"temp.xml"                                                                                                    
    doc = minidom.parse(xml)                                                                                                   
    node = doc.documentElement                                                                                                 
    series = doc.getElementsByTagName("serie")                                                                                 
    for serie in series:                                                                                                       
    	name = serie.getElementsByTagName("name")[0].childNodes[0].data
    	name = name.encode("utf-8")
    	id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                    
        fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                
        poster = serie.getElementsByTagName("poster")[0].childNodes[0].data
	type=serie.getElementsByTagName("type")[0].childNodes[0].data
	print "movies poster"+SERVER+fanart
	try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
        except:                                                                                                                                                           
                        plot=""                                               
    	itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie", show=id,fanart=SERVER+fanart))
    return itemlist

def mkdir_p(path):
    try:
           os.makedirs(path)
    except OSError , exc: 
           if exc.errno == errno.EEXIST and os.path.isdir(path):
              pass
           else: raise    

def mainlist(item):
    if (DEBUG): logger.info("[stormtv.py] Mainlist"+PREFERENCES)
    if (PREFERENCES=="0"):
    	user_id = config.get_setting("stormtvuser")                                                                                                                                   
    	user_pass = config.get_setting("stormtvpassword")                                                                                                                             
    	path=config.get_data_path()+"stormtv/temp/"
    	if not os.path.exists(path): 
       		logger.info ("[stormtv.py]Creating data_path "+path)
       		try:            
          		mkdir_p(path) 
       		except:            
          		logger.info("[stormtv.py] Mainlist  Fallo crear directorio")
          		pass            

    	itemlist = []
	itemlist.append( Item(channel=__channel__,action="searchtype",thumbnail=SERVER+"buscar.jpg",title="Buscar", url="",fanart=SERVER+"logo.jpg"))
    	urllib.urlretrieve (SERVER+"tvseries/following/user/"+user_id+"/pass/"+user_pass, path+"temp.xml")                             
    	xml=path+"/"+"temp.xml"                                                                                                    
    	doc = minidom.parse(xml)                                                                                                   
    	node = doc.documentElement                                                                                                 
    	series = doc.getElementsByTagName("serie")                                                                                 
    	for serie in series:                                                                                                       
    		name = serie.getElementsByTagName("name")[0].childNodes[0].data
    		name = name.encode("utf-8")
    		id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                    
        	fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data
        	poster = serie.getElementsByTagName("poster")[0].childNodes[0].data
		print "movies fanart"+SERVER+fanart                                                
    		try:
			plot=serie.getElementsByTagName("plot")[0].childNodes[0].data
			plot=plot.encode("utf-8")
		except:
			plot=""
    		art=SERVER+fanart      

        	# Depuracion
        	#if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")            
    		itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie", show=id ,fanart=art))

    else:
    	itemlist=[]
    	itemlist.append( Item(channel=__channel__, action="channel" , title="Usuario o contraseña incorrectas", fulltitle="" , url="", thumbnail="", plot="", viewmode="movie", show="" ,fanart=""))
    return itemlist
def genresearch(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"
        urllib.urlretrieve (SERVER+"tvseries/genres", path+"temp.xml")                                                                        
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        genres = doc.getElementsByTagName("genre")
	if (DEBUG): print len(genres)
	itemlist=[]
	for genre in genres:
		name = genre.getElementsByTagName("name")[0].childNodes[0].data
		if (DEBUG): logger.info("###"+name+"$$")
		id = genre.getElementsByTagName("id")[0].childNodes[0].data
		itemlist.append( Item(channel=__channel__, action="genretvs" , title=name, fulltitle=name , url=id, thumbnail=SERVER+"logo.jpg", plot="", viewmode="movie", show=id ,fanart=SERVER+"logo.jpg"))
	return itemlist
def yearsearch(item):                                                                                                                                                            
        user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/years", path+"temp.xml")                                                                                                            
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        years = doc.getElementsByTagName("year")                                                                                                                                
        if (DEBUG): print len(years)                                                                                                                                                         
        itemlist=[]                                                                                                                                                               
        for year in years:                                                                                                                                                      
                name = year.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                if (DEBUG): logger.info("[stormtv.py] yearsearch ###"+name+"$$")                                                                                                                                             
                id = year.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                itemlist.append( Item(channel=__channel__, action="yeartvs" , title=name, fulltitle=name , url=id, thumbnail=SERVER+"logo.jpg", plot="", viewmode="movie_with_plot", show=id ,fanart=SERVER+"logo.jpg"))
        return itemlist
def yeartvs(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/yeartvs/year/"+item.url, path+"temp.xml")                                                                                          
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        series = doc.getElementsByTagName("serie")                                                                                                                                
        itemlist=[]                                                                                                                                                               
        for serie in series:                                                                                                                                                      
                name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                name = name.encode("utf-8")                                                                                                                                       
                id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                               
                poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                               
                try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
                except:                                                                                                                                                           
                        plot=""                                                                                                                                                   
                art=SERVER+fanart                                                                                                                                                 
                                                                                                                                                                                  
                # Depuracion                                                                                                                                                      
                #if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")                                                                                   
                itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie_with_plot", show=id ,fanart=art))
        return itemlist 
def genretvs(item):
	user_id = config.get_setting("stormtvuser")                                                                                                                               
        user_pass = config.get_setting("stormtvpassword")                                                                                                                         
        path=config.get_data_path()+"stormtv/temp/"                                                                                                                               
        urllib.urlretrieve (SERVER+"tvseries/genretvs/genre/"+item.url, path+"temp.xml")                                                                                                            
        xml=path+"/"+"temp.xml"                                                                                                                                                   
        doc = minidom.parse(xml)                                                                                                                                                  
        node = doc.documentElement                                                                                                                                                
        series = doc.getElementsByTagName("serie")
	itemlist=[]                                                                                                                                
        for serie in series:                                                                                                                                                      
                name = serie.getElementsByTagName("name")[0].childNodes[0].data                                                                                                   
                name = name.encode("utf-8")                                                                                                                                       
                id = serie.getElementsByTagName("id")[0].childNodes[0].data                                                                                                       
                fanart = serie.getElementsByTagName("fanart")[0].childNodes[0].data                                                                                               
                poster = serie.getElementsByTagName("poster")[0].childNodes[0].data                                                                                               
                try:                                                                                                                                                              
                        plot=serie.getElementsByTagName("plot")[0].childNodes[0].data                                                                                             
                        plot=plot.encode("utf-8")                                                                                                                                 
                except:                                                                                                                                                           
                        plot=""
                art=SERVER+fanart                                                                                                                                                 
                                                                                                                                                                                  
                # Depuracion                                                                                                                                                      
                #if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")                                                                                   
                itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie_with_plot", show=id ,fanart=art))
	return itemlist 

def channel(item):
	logger.info("[stormtv.py] Channel")
	storm_show=item.show
	storm_thumbnail=item.thumbnail
	storm_plot=item.plot
	storm_fanart=item.fanart
	name = ""
	url = ""
	action=""
	path=config.get_data_path()+"stormtv/temp/"                                   
	urllib.urlretrieve (SERVER+"tvseries/getchannelsxml/id/"+storm_show, path+"temp.xml")            
        xml=path+"temp.xml"                                                                                              
        doc = minidom.parse(xml)                                                                                             
        node = doc.documentElement                                                                                           
        series = doc.getElementsByTagName("channel")  
        itemlist = []  
        for serie in series:                                                                                                 
	        name=serie.getElementsByTagName("name")[0].childNodes[0].data
		type=serie.getElementsByTagName("type")[0].childNodes[0].data                                                 
                url=serie.getElementsByTagName("url")[0].childNodes[0].data
		if (type=="1"):
                	itemlist.append( Item(channel=__channel__, action="channeltvs" , title=name, fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))                                                      
		else:
			#Si es una pelicula u otra cosa
			if (name=="peliculasyonkis"):
				fulltitle="peliculasyonkis_generico"
			else:
				fulltitle=name
			itemlist.append( Item(channel=__channel__, action="findvideos" , title=name, fulltitle=fulltitle , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))	
	# Si no es una serie favorita añade el item para añadirla o para quitarla en caso de que este añadida como favorita	
	if (stormlib.isfollow(item.show)=='0'):	
		itemlist.append( Item(channel=__channel__, action="addfollow" , title="Add fav", show=item.show,fanart=item.fanart))
	else:
		itemlist.append( Item(channel=__channel__, action="removefollow" , title="Remove fav", show=item.show,fanart=item.fanart))
	return itemlist

def addfollow(item):
    logger.info("[stormtv.py] Addfollow "+item.show)
    from core import stormlib
    stormlib.addfollow(item.show)

def removefollow(item):
    logger.info("[stormtv.py] Removefollow "+item.show)	
    from core import stormlib                                                                                                                                                     
    stormlib.removefollow(item.show)  

def channeltvs(item):
	logger.info("[stormtv.py] Channeltvs")
	storm_fanart=item.fanart
	storm_plot=item.plot
	storm_thumbnail=item.thumbnail
	storm_show=item.show	
	storm_channel_name=item.fulltitle
	storm_title=item.title
        action="episodios"	
	item=Item(channel=__channel__,url=item.url)
	exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
	# El action nos devolvera el listado de capitulos (episodelist o episodios)
	exec "itemlist_p = channel."+action+"(item)"
	# le quitamos el ultimo elemento que es añadir a la biblioteca de xbmc solo si es seriespepito o seriesyonkis
	patternbiblio="esta serie a la biblioteca"
	patterndescarga="Descargar todos los episodios de la serie"
	#si el ultimo elemento de la lista es descargar la serie completa lo quitamos
	if (len(re.compile(patterndescarga,re.DOTALL).findall(itemlist_p[len(itemlist_p)-1].title))>0):
	   itemlist_p = itemlist_p[0:len(itemlist_p)-1] 

	#Si el ultimo elemento de la lista es añadir a la biblioteca lo quitamos	
	if (len(re.compile(patternbiblio,re.DOTALL).findall(itemlist_p[len(itemlist_p)-1].title))>0):                                                                                    
           itemlist_p = itemlist_p[0:len(itemlist_p)-1]
	itemlist=itemlist_p
	storm_itemlist=[]
	if (config.get_setting("stormtvaccount")=="true"):
	        from core import stormlib
	        chap_dictionary=stormlib.getwatched(storm_show)
	                
	for item in itemlist:
		# comprobar si esta visto y añadir visto.
		if (config.get_setting("stormtvaccount")=="true"):    
	                from core import stormlib                     
	                title, extra = stormlib.iswatched(item.title,chap_dictionary)
	                #hace falta saber cuantos hemos visto para dejar los n ultimos vistos
	        else:                                                           
	                extra=""                                                
	        logger.info("[stormtv.py] extra="+extra)  	
		storm_itemlist.append( Item(channel=__channel__,action="findvideos", server=item.server,fulltitle=storm_channel_name, title=title, url=item.url,thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show,fanart=storm_fanart, extra=extra))
	return storm_itemlist


def findvideos(item):
	logger.info("[stormtv.py] Findvideos - Filtro Idioma:"+LANG+" Filtro Servers:"+SERVERS)
        storm_fanart=item.fanart
        storm_plot=item.plot                                                                                                                                                            
        storm_thumbnail=item.thumbnail                                                                                                                                                  
        storm_chapter=item.extra                                                                                                                                                         
        storm_show=item.show                                                                                                                                                            
        storm_channel_name=item.fulltitle                                                                                                                                                   
        storm_title=item.title
        free_url=item.url
        action="findvideos"
        from servers import servertools                                                                                                                                                          
	item=Item(channel=__channel__,url=item.url)
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
        # El action nos devolvera el listado de posibles enlaces                                                                                             
        try:
        	exec "itemlist = channel."+action+"(item)"
        except:
        	#from servers import servertools
        	itemlist= servertools.find_video_items(item)                                                                                                                                
        storm_itemlist=[]
        #lang=LANG
       	#logger.info("[stormtv.py] Findvideos"+LANG) 
        # creamos la cadena de servidores free
        pat_free="("
        for fserver in servertools.FREE_SERVERS:
        	pat_free=pat_free+fserver+"|"
        pat_free=pat_free[:len(pat_free)-1]+")"
        
        # creamos la cadena de servidores filenium
        pat_filenium="("
        for filenium in servertools.FILENIUM_SERVERS:
        	pat_filenium=pat_filenium+filenium+"|"
        pat_filenium=pat_filenium[:len(pat_filenium)-1]+")"
        
        #creamos la cadena de servidores alldebrid
        pat_all="(" 
        for all in servertools.ALLDEBRID_SERVERS:
        	pat_all=pat_all+all+"|"
        pat_all=pat_all[:len(pat_all)-1]+")"
        
        #creamos la cadena de servidores real
        pat_real="("
        for real in servertools.REALDEBRID_SERVERS:
        	pat_real=pat_real+real+"|"
        pat_real=pat_real[:len(pat_real)-1]+")"
        
        #logger.info("pat_free"+pat_free)
        #server=SERVERS
        strue=0
        ltrue=0
        verified=[]
        vserver=""
  	excluded=[]
	excluded.append("letitbit") 
	for item in itemlist:
		#Si el canal es shurweb le añadimos (spa)
		if (storm_channel_name=="shurweb"):                                                                                                                               
                        item.title=item.title+" (spa)"
		fserver=item.server
		logger.info("[stormtv.py] title"+item.title)
		title=item.title.lower()
		if (SERVERS!="0"):
			if (SERVERS=="1"):
				#seriesdanko no tiene el nombre del server en el titulo, sino en el thumbnail
				if (storm_channel_name=="seriesdanko"):
					matches_free=re.compile(pat_free,re.DOTALL).findall(item.thumbnail)
					#logger.info("matches[0]"+matches_free[0])
					if (len(matches_free)>0):
					   item.title=item.title+" ("+matches_free[0]+")"
					
				else:
					matches_free= re.compile(pat_free,re.DOTALL).findall(title)
				if (len(matches_free)>0):
					vserver=matches_free[0]
					if (DEBUG):logger.info("free"+title)
					strue=1
				else:
					strue=0
			elif (SERVERS=="2"):
				if (config.get_setting("fileniumpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                            
					   matches_filenium=re.compile(pat_filenium,re.DOTALL).findall(item.thumbnail)
					   if (len(matches_filenium)>0):
						vserver=matches_filenium[0]
					   	item.title=item.title+" ("+matches_filenium[0]+")"
					   	#logger.info("matches[0]"+matches_filenium[0])                                                                       
					else:
						#if (storm_channel_name=="seriespepito"):
						#	matches_filenium= re.compile("Streamcloud",re.DOTALL).findall(item.title)
						#else:
						#titulo=item.title.lower()
					   	matches_filenium= re.compile(pat_filenium,re.DOTALL).findall(title)
					if (len(matches_filenium)>0):
						vserver=matches_filenium[0]
						if (DEBUG):logger.info("Filenium"+item.title)
						print ("[stormtv.py] findvideos"+matches_filenium[0])
						strue=1
					else:
						strue=0
				if (config.get_setting("alldebridpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                    
					   matches_all=re.compile(pat_all,re.DOTALL).findall(item.thumbnail)
					   if (len(matches_all)>0):                                              
					          item.title=item.title+" ("+matches_all[0]+")"                                                                   
					else:
					   matches_all=re.compile(pat_all,re.DOTALL).findall(title)
					if (len(matches_all)>0):
						vserver=matches_all[0]
						if (DEBUG): logger.info("Alldebrid"+item.title)
						strue=1
					else:
						strue=0
				if (config.get_setting("realdebridpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                    
					   matches_real=re.compile(pat_real,re.DOTALL).findall(item.thumbnail)                                                                    
					   if (len(matches_real)>0):                                              
					      item.title=item.title+" ("+matches_real[0]+")"	
					else:
					   matches_real=re.compile(pat_real,re.DOTALL).findall(title)
					if (len(matches_real)>0):
						vserver=matches_real[0]
						if (DEBUG):logger.info("Real"+item.title)
						strue=1
					else:
						strue=0
		else:
			if (DEBUG):logger.info("[stormtv.py] strue=1")
			strue=1
		#Comprobamos si el enlace existe
		# de momento solo para filenium
		#if (config.get_setting("fileniumpremium")=="true"):
			#logger.info("[stormtv.py] findvideos"+matches_filenium[0])	
			#exec "import servers."+matches_filenium[0]+" as tserver" 
			#res,test= tserver.test_vide_exists(item.url)                                                                                                   
			#logger.info("[stormtv.py] findvideos"+res+"#"+test)
		#Comprobamos el idioma
		if ((LANG!="0")&(strue==1)):
			logger.info("lang="+item.title)
			if (storm_channel_name=="serieonline"):                                                                                                                           
			   item.title=stormlib.audio_serieonline(item.title)	
			elif ((storm_channel_name=="seriesyonkis")or (storm_channel_name=="peliculasyonkis_generico")):
			   item.title=stormlib.audio_seriesyonkis(item.title)
			patron_vos='VOS|Sub'                                                                                                                                              
			matches_vos = re.compile(patron_vos,re.DOTALL).findall(item.title)	
			patron_vo='VO(?!S)'                                                                                                                                               
			matches_vo = re.compile(patron_vo,re.DOTALL).findall(item.title)
			patron_spa='Espa|spa'                                                                                                                                               
			matches_spa = re.compile(patron_spa,re.DOTALL).findall(item.title) 	
			if (len(matches_vos)>0):
				if (LANG in ["2","4","6","0"]):
					if (DEBUG):logger.info("[stormlib.py] findvideos: encontrado match vos")
					ltrue=1

				else:
					ltrue=0
			elif (len(matches_vo)>0):
				if (LANG in ["3","5","6","0"]):
					if (DEBUG):logger.info("[stormlib.py] findvideos: encontrado match vo")
					ltrue=1                                                                                                                                   
				else:
					ltrue=0
			elif (len(matches_spa)>0):
				if (LANG in ["1","4","5","0"]):
					if(DEBUG):logger.info("[stormlib.py] findvideos: encontrado match spa")
					ltrue=1
				else:
					ltrue=0
			else:
				if (DEBUG):logger.info("[stormlib.py] findvideos: No se ha encontrado ningun tipo.")
				ltrue=1
		else:
			if (DEBUG):logger.info("[stormtv.py] ltrue=0")
			ltrue=1
		if ((strue==1)&(ltrue==1)):                                                                                                                                           
                #seriesyonkis es un poco distinto para comprobar, de momento hacemos bypass :)                                                                                    
                 if ((storm_channel_name<>"seriesyonkis")and(storm_channel_name<>"peliculasyonkis_generico")):                                                                                                                          
                   if ((vserver not in verified)&(vserver not in excluded)):                                                                                                      
                           try:                                                                                                                                                   
                              exec "import servers."+vserver+" as tserver"                                                                                                        
                           except:                                                                                                                                                
                                print "[stormtv.py] Free Verify no existe el servidor"                                                                                            
                           try:                                                                                                                                                   
                              data =scrapertools.cache_page(item.url)                                                                                                             
                           except:                                                                                                                                                
                                print "[stormtv.py] Free Verify no se puede descargar la pagina"                                                                                  
                           #Shurweb y otros canales que usan la funcion generica de findvideos tienen el enlace directamente, no hay que descargar la pagina.                     
                           if ((storm_channel_name<>"shurweb")&(storm_channel_name<>"animeflv")):                                                                                 
                                print "dentro del if<>shurweb"                                                                                                                   
                                try:                                                                                                                                              
                                        resultado = tserver.find_videos(data)                                                                                                     
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verify no find_videos"                                                                                           
                                try:                                                                                                                                              
                                        res,test= tserver.test_video_exists(resultado[0][1])                                                                                      
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verified fallo test_video_exist "+vserver                                                                        
                                        res=False                                                                                                                                 
                           else:                                                                                                                                                  
                                print "dentro del else<>shurweb"                                                                                                                 
                                try:                                                                                                                                              
                                        res,test= tserver.test_video_exists(data)                                                                                                 
                                except:                                                                                                                                           
                                        print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           if (res):                                                                                                                                              
                              print("[stormtv.py] Free Verify"+"True#"+test)                                                                                                      
                              item.title="[Verificado]"+item.title                                                                                                                
                              verified.append(vserver)                                                                                                                            
                              strue=1                                                                                                                                             
                           else:                                                                                                                                                  
                              print("[stormtv.py] findvideos false")                                                                                                              
                              strue=0             
		if ((strue==1)&(ltrue==1)):                                                                                                                                       
                        storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail,  plot=storm_plot, folder=False, fanart=storm_fanart,show = storm_show,extra=storm_chapter, server=item.server)) 	 
	if (SERVERS=="2"):
		storm_itemlist.append( Item(channel=__channel__, action="free" , title="Buscar gratuitos", fulltitle=storm_channel_name , url=free_url, thumbnail=storm_thumbnail,plot=storm_plot, fanart=storm_fanart,show = storm_show,extra=storm_chapter))
	return sorted(storm_itemlist, key=lambda item: item.title,  reverse=True) 

def free(item):
        logger.info("[stormtv.py] Free")                                                                                                                                    
        storm_fanart=item.fanart                                                                                                                                                  
        storm_plot=item.plot                                                                                                                                                      
        storm_thumbnail=item.thumbnail                                                                                                                                            
        storm_chapter=item.extra                                                                                                                                                  
        storm_show=item.show                                                                                                                                                      
        storm_channel_name=item.fulltitle                                                                                                                                         
        storm_title=item.title                                                                                                                                                    
        free_url=item.url                                                                                                                                                         
        action="findvideos"                                                                                                                                                       
        item=Item(channel=__channel__,url=item.url)                                                                                                                               
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                    
        # El action nos devolvera el listado de posibles enlaces                                                                                                                  
        exec "itemlist = channel."+action+"(item)"                                                                                                                                
        storm_itemlist=[]                                                                                                                                                         
        #lang=1              
	# creamos la cadena de servidores free                                                                                                                                    
	pat_free="("                                                                                                                                                              
	for fserver in servertools.FREE_SERVERS:                                                                                                                                  
	    pat_free=pat_free+fserver+"|"                                                                                                                                     
	pat_free=pat_free[:len(pat_free)-1]+")"
	strue=0                                                                                                                                                                   
	ltrue=0 
	#Verified contendrá la lista de servidores que hemos podido comprobar
	verified=[]
	#Excluded contendrá los servidores que no podemos verificar
	excluded=[]
	excluded.append("letitbit")                                                                                                                                                                  
	for item in itemlist:
	    #Si el canal es shurweb le añadimos (spa)                                                                                                                         
            if (storm_channel_name=="shurweb"):                                                                                                                               
                item.title=item.title+" (spa)"
	    title=item.title.lower()
	    if (storm_channel_name=="seriesdanko"):                                                                                                           
	       matches_free=re.compile(pat_free,re.DOTALL).findall(item.thumbnail)
	       if (len(matches_free)>0):                                                                  
	          item.title=item.title+" ("+matches_free[0]+")"                                                                      
	    else:                                                                                                                                                     
	       matches_free= re.compile(pat_free,re.DOTALL).findall(title)                                                                                  
	    if (len(matches_free)>0):                                                                                                                         
	        logger.info("[stormtv.py] Free :"+item.title) 
		vserver=matches_free[0]                                                                                                           
	        strue=1                                                                                                                                   
	    else:                                                                                                                                             
	        strue=0 
        #Comprobamos el idioma                                                                                                                                            
	    if (LANG!="0"):                                                                                                                                                     
	   	if (storm_channel_name=="serieonline"):                                                                                                                   
	      		item.title=stormlib.audio_serieonline(item.title)                                                                                                      
	   	elif ((storm_channel_name=="seriesyonkis")or(storm_channel_name=="peliculasyonkis_generico")):
	   	        item.title=stormlib.audio_seriesyonkis(item.title)	
	   	patron_vos='VOS|Sub'                                                                                                                                      
	   	matches_vos = re.compile(patron_vos,re.DOTALL).findall(item.title)                                                                                        
	   	patron_vo='VO(?!S)'                                                                                                                                       
	   	matches_vo = re.compile(patron_vo,re.DOTALL).findall(item.title)                                                                                          
	   	patron_spa='Espa'                                                                                                                                         
	   	matches_spa = re.compile(patron_spa,re.DOTALL).findall(item.title)                                                                                        
	   	if (len(matches_vos)>0):
			if (LANG in ["2","4","6","0"]):                                                                                                                           
		    		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match vos")                                                                             
		    		ltrue=1                                                                                                                                   
			else:                                                                                                                                             
		    		ltrue=0                                                                                                                                   
	   	elif (len(matches_vo)>0):                                                                                                                                 
		  	if (LANG in ["3","5","6","0"]):                                                                                                                           
		     		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match vo")                                                                              
		     		ltrue=1                                                                                                                                   
		  	else:                                                                                                                                             
		     		ltrue=0
	   	elif (len(matches_spa)>0):                                                                                                                                
	          	if (LANG in ["1","4","5","0"]):                                                                                                                           
	             		if (DEBUG): logger.info("[stormlib.py] findvideos: encontrado match spa")                                                                             
	             		ltrue=1                                                                                                                                   
	          	else:                                                                                                                                             
	             		ltrue=0                                                                                                                                   
	   	else:                                                                                                                                                     
	          	if (DEBUG): logger.info("[stormlib.py] findvideos: No se ha encontrado ningun tipo.")                                                                         
      	          	ltrue=1                                                                                                                                           
	    else:                                                                                                                                                             
	    	ltrue=1
	
	    if ((strue==1)&(ltrue==1)):
		#seriesyonkis es un poco distinto para comprobar, de momento hacemos bypass :)
	        if ((storm_channel_name<>"seriesyonkis")and (storm_channel_name<>"peliculasyonkis_generico")):                                                        
                   if ((vserver not in verified)&(vserver not in excluded)):                         
                           try:                                                                      
                              exec "import servers."+vserver+" as tserver"                           
                           except:                                                                   
                                print "[stormtv.py] Free Verify no existe el servidor"                  
                           try:                                                                      
                              data =scrapertools.cache_page(item.url)                                
                           except:                                                                   
                                print "[stormtv.py] Free Verify no se puede descargar la pagina" 
			   #Shurweb y otros canales que usan la funcion generica de findvideos tienen el enlace directamente, no hay que descargar la pagina.       
                           if ((storm_channel_name<>"shurweb")&(storm_channel_name<>"animeflv")):                                                  
                                #print "dentro del if<>shurweb"                                       
                                try:                                                                 
                                        resultado = tserver.find_videos(data)                        
                                except:                                                              
                                        print "[stormtv.py] Free Verify no find_videos"                 
                                try:                                                                 
                                        res,test= tserver.test_video_exists(resultado[0][1])                                                                                      
                                except:                                                                                                                                           
                                        print "[stormtv.py] Free Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           else:                                                                                                                                                  
                                #print "dentro del else<>shurweb"                                                                                                                  
                                try:                                                                                                                                              
                                        res,test= tserver.test_video_exists(data)                                                                                                 
                                except:                                                                                                                                           
                                        print "[stormtv.py] Verified fallo test_video_exist "+vserver                                                                             
                                        res=False                                                                                                                                 
                           if (res):                                                                                                                                              
                              print("[stormtv.py] Free Verify"+"True#"+test)                                                                                                       
                              item.title="[Verificado]"+item.title                                                                                                                
                              verified.append(vserver)                                                                                                                            
                              strue=1                                                                                                                                             
                           else:                                                                                                                                                  
                              print("[stormtv.py] findvideos false")                                                                                                              
                              strue=0
		if ((strue==1)&(ltrue==1)):
             		storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail, plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter, server=item.server))	
	#return storm_itemlist
	return sorted(storm_itemlist, key=lambda item: item.title,  reverse=True)    	   
def play(item):
	logger.info("[stormtv.py] Play")
	storm_fanart=item.fanart
	storm_plot=item.plot
	storm_thumbnail=item.thumbnail
	storm_chapter=item.extra
	storm_show=item.show
	storm_channel_name=item.fulltitle
	storm_title=item.title
	action="play"
	if (config.get_setting("stormtvaccount")=="true"):                                                                                                                        
	   from core import stormlib                                                                                                                                        
	   stormlib.setwatched(storm_show,storm_chapter)
	item_storm=Item(channel=__channel__,url=item.url)
	exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                          
	# El action nos devolvera el enlace que se reproducira
	try:                                                                                                                  
		exec "itemlist = channel."+action+"(item_storm)"
		#return itemlist
	except:
		#from platformcode.xbmc import xbmctools
		itemlist=[]	
		itemlist.append(Item(channel="shurweb", server=item.server, url=item.url, category=item.category, title=item.title, thumbnail=item.thumbnail, plot=item.plot,  extra=item.extra, subtitle=item.subtitle,  fulltitle=item.fulltitle)) 
	return itemlist
	                 	
# VerificaciÃ³n automÃ¡tica de canales: Esta funciÃ³n debe devolver "True" si estÃ¡ ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vÃ­deos de "Novedades" devuelve mirrors
    episode_items = lastepisodes(mainlist_items[0])
    bien = False
    for episode_item in episode_items:
        mediaurls = findvideos( episode_item )
        if len(mediaurls)>0:
            return True

    return False