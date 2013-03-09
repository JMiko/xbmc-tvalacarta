# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para stormtv 
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por JuRR
# v0.1
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
__category__ = "S,A"
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
'''
def mainlist(item):
    logger.info("[seriesyonkis.py] mainlist")
    #server= "https://"+__server__+"/stormtv/public/"
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lastepisodes"      , title="Ultimos capÃ­tulos" , url="http://",fanart=SERVER+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"    , title="Listado alfabetico", url="http://",fanart=server+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="follow"    , title="Series Siguiendo", url="http://",fanart=server+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://",fanart=server+"logo.jpg"))

    return itemlist
'''
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
    	#seriesyonkis = id
    	#plot=""
    	#scrapedplot=plot      
        # Depuracion
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
    	itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot="", viewmode="movie", show=id,fanart=SERVER+fanart))

    return itemlist

def mkdir_p(path):
    try:
           os.makedirs(path)
    except OSError as exc: # Python >2.5
           if exc.errno == errno.EEXIST and os.path.isdir(path):
              pass
           else: raise    

def mainlist(item):
    if (DEBUG): logger.info("[stormtv.py] Mainlist"+PREFERENCES)
    if (PREFERENCES=="0"):
    	user_id = config.get_setting("stormtvuser")                                                                                                                                   
    	user_pass = config.get_setting("stormtvpassword")                                                                                                                             
    	#server= "https://"+__server__+"/stormtv/public/"                                                                                                                              
    	path=config.get_data_path()+"stormtv/temp/"
    	if not os.path.exists(path): 
       		logger.info ("[stormtv.py]Creating data_path "+path)
       		try:            
          		mkdir_p(path) 
       		except:            
          		logger.info("[stormtv.py] Mainlist  Fallo crear directorio")
          		pass            

    	itemlist = []
    	itemlist.append( Item(channel=__channel__, action="search"    , thumbnail=SERVER+"buscar.jpg", title="Buscar", url="",fanart=SERVER+"logo.jpg"))
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
        	#plot = serie.getElementsByTagName("plot")[0].childNodes[0].data 
    		plot=""
    		art=SERVER+fanart      

        	# Depuracion
        	#if (DEBUG): logger.info("title=["+name+"], url=["+id+"], thumbnail=["+art+"]")            
    		itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=id, thumbnail=SERVER+poster, plot=plot, viewmode="movie", show=id ,fanart=art))

    else:
    	itemlist=[]
    	itemlist.append( Item(channel=__channel__, action="channel" , title="Usuario o contraseña incorrectas", fulltitle="" , url="", thumbnail="", plot="", viewmode="movie", show="" ,fanart=""))
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
	#server = "https://"+__server__+"/stormtv/public/tvseries/getchannelsxml/id/"+storm_show
	path=config.get_data_path()+"stormtv/temp/"                                   
	urllib.urlretrieve (SERVER+"tvseries/getchannelsxml/id/"+storm_show, path+"temp.xml")            
        xml=path+"temp.xml"                                                                                              
        doc = minidom.parse(xml)                                                                                             
        node = doc.documentElement                                                                                           
        series = doc.getElementsByTagName("channel")  
        itemlist = []  
        #print "fanart="+item.fanart                                                                      
        for serie in series:                                                                                                 
	        name=serie.getElementsByTagName("name")[0].childNodes[0].data                                                 
                url=serie.getElementsByTagName("url")[0].childNodes[0].data
                itemlist.append( Item(channel=__channel__, action="channeltvs" , title=name, fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))                                                      
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
	biblioteca= {"seriesyonkis":1,"seriespepito":2}
	logger.info("[stormtv.py] Channeltvs")
	storm_fanart=item.fanart
	storm_plot=item.plot
	storm_thumbnail=item.thumbnail
	storm_show=item.show	
	storm_channel_name=item.fulltitle
	storm_title=item.title
	#fulltitle=item.fulltitle
	if (storm_channel_name=="seriespepito"):                                                                                                                                        
           action="episodelist"                                                                                                                                      
        else:                                                                                                                                                             
           action="episodios"	
	item=Item(channel=__channel__,url=item.url)
	exec "import pelisalacarta.channels."+storm_channel_name+" as channel"
	# El action nos devolvera el listado de capitulos (episodelist o episodios)
	exec "itemlist_p = channel."+action+"(item)"
	# le quitamos el ultimo elemento que es añadir a la biblioteca de xbmc solo si es seriespepito o seriesyonkis
	if (storm_channel_name in biblioteca):
		itemlist = itemlist_p[0:len(itemlist_p)-1]
	else:
		itemlist = itemlist_p
	storm_itemlist=[]
	if (config.get_setting("stormtvaccount")=="true"):
	        from core import stormlib
	        chap_dictionary=stormlib.getwatched(storm_show)
	                
	for item in itemlist:
		# comprobar si esta visto y añadir visto.
		if (config.get_setting("stormtvaccount")=="true"):    
	                from core import stormlib                     
	                title, extra = stormlib.iswatched(item.title,chap_dictionary)
	        else:                                                           
	                extra=""                                                
	        logger.info("[stormtv.py] extra="+extra)  	
		storm_itemlist.append( Item(channel=__channel__,action="findvideos", fulltitle=storm_channel_name, title=title, url=item.url,thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show,fanart=storm_fanart, extra=extra))
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
	item=Item(channel=__channel__,url=item.url)                                                                                                                               
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                          
        # El action nos devolvera el listado de posibles enlaces                                                                                             
        exec "itemlist = channel."+action+"(item)"                                                                                                                                
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
	for item in itemlist:
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
					if (DEBUG):logger.info("free"+title)
					strue=1
				else:
					strue=0
			elif (SERVERS=="2"):
				if (config.get_setting("fileniumpremium")=="true"):
					if (storm_channel_name=="seriesdanko"):                                                                                                            
					   matches_filenium=re.compile(pat_filenium,re.DOTALL).findall(item.thumbnail)
					   if (len(matches_filenium)>0):
					   	item.title=item.title+" ("+matches_filenium[0]+")"
					   	#logger.info("matches[0]"+matches_filenium[0])                                                                       
					else:
						#if (storm_channel_name=="seriespepito"):
						#	matches_filenium= re.compile("Streamcloud",re.DOTALL).findall(item.title)
						#else:
						#titulo=item.title.lower()
					   	matches_filenium= re.compile(pat_filenium,re.DOTALL).findall(title)
					if (len(matches_filenium)>0):
						if (DEBUG):logger.info("Filenium"+item.title)
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
						if (DEBUG):logger.info("Real"+item.title)
						strue=1
					else:
						strue=0
		else:
			if (DEBUG):logger.info("[stormtv.py] strue=1")
			strue=1
			
		#Comprobamos el idioma
		if (LANG!="0"):
			logger.info("lang="+item.title)
			if (storm_channel_name=="serieonline"):                                                                                                                           
			   item.title=stormlib.audio_serieonline(item.title)	
			elif (storm_channel_name=="seriesyonkis"):
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
					#storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail,  plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter))
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
			if (DEBUG):logger.info("[stormtv.py] ltrue=1")
			ltrue=1
			#storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail, plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter))
		if ((strue==1)&(ltrue==1)):
			storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail, plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter))
	if (SERVERS=="2"):
		storm_itemlist.append( Item(channel=__channel__, action="free" , title="Buscar gratuitos", fulltitle=storm_channel_name , url=free_url, thumbnail=storm_thumbnail,plot=storm_plot, fanart=storm_fanart,show = storm_show,extra=storm_chapter))
	return storm_itemlist

#hacer que saque los enlaces free
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
	for item in itemlist:
	    title=item.title.lower()
	    if (storm_channel_name=="seriesdanko"):                                                                                                           
	       matches_free=re.compile(pat_free,re.DOTALL).findall(item.thumbnail)
	       if (len(matches_free)>0):                                                                  
	          item.title=item.title+" ("+matches_free[0]+")"                                                                      
	    else:                                                                                                                                                     
	       matches_free= re.compile(pat_free,re.DOTALL).findall(title)                                                                                  
	    if (len(matches_free)>0):                                                                                                                         
	        logger.info("[stormtv.py] Free :"+item.title)                                                                                                            
	        strue=1                                                                                                                                   
	    else:                                                                                                                                             
	        strue=0 
        #Comprobamos el idioma                                                                                                                                            
	    if (LANG!="0"):                                                                                                                                                     
	   	if (storm_channel_name=="serieonline"):                                                                                                                   
	      		item.title=stormlib.audio_serieonline(item.title)                                                                                                      
	   	elif (storm_channel_name=="seriesyonkis"):
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
             	storm_itemlist.append( Item(channel=__channel__, action="play" , title=item.title, fulltitle=storm_channel_name , url=item.url, thumbnail=storm_thumbnail, plot=storm_plot, folder=False,fanart=storm_fanart,show = storm_show,extra=storm_chapter))	
	return storm_itemlist    	   
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
	item=Item(channel=__channel__,url=item.url)
	exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                          
	# El action nos devolvera el enlace que se reproducira                                                                                                                  
	exec "itemlist = channel."+action+"(item)"                                                                                                                                
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