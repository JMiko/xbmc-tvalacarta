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

def isGeneric():
    return True
'''
def mainlist(item):
    logger.info("[seriesyonkis.py] mainlist")
    server= "https://"+__server__+"/stormtv/public/"
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lastepisodes"      , title="Ultimos capítulos" , url="http://www.seriesyonkis.com/ultimos-capitulos",fanart=server+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="listalfabetico"    , title="Listado alfabetico", url="http://www.seriesyonkis.com",fanart=server+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="follow"    , title="Series Siguiendo", url="http://www.seriesyonkis.com/series-mas-vistas",fanart=server+"logo.jpg"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://www.seriesyonkis.com/buscar/serie",fanart=server+"logo.jpg"))

    return itemlist
'''
def search(item,texto, categoria="*"):
    logger.info("[stormtv.py] follow")
    itemlist = []
    server= "http://"+__server__+"/stormtv/public/"
    path=config.get_data_path()+"stormtv/temp/"
    if not os.path.exists(path):                                                                                                     
       print "Creating data_path "+path                                                                                   
       try:                                                                                                                          
          os.mkdirs(path)                                                                                                      
       
       except:
       	  print "[stormtv.py] search fallo crear directorio"                                                                                                                       
          pass                                           
    urllib.urlretrieve ("https://"+__server__+"/stormtv/public/tvseries/search/title/"+texto, path+"temp.xml")                             
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
    	seriesyonkis = id
    	plot=""
    	scrapedplot=plot      
        # Depuracion
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
    	itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=seriesyonkis, thumbnail=server+poster, plot=scrapedplot, viewmode="movie", show=id,fanart=server+fanart))

    return itemlist
def mkdir_p(path):
    try:
           os.makedirs(path)
    except OSError as exc: # Python >2.5
           if exc.errno == errno.EEXIST and os.path.isdir(path):
              pass
           else: raise    

def mainlist(item):
    logger.info("[stormtv.py] Mainlist")
    user_id = config.get_setting("stormtvuser")                                                                                                                                   
    user_pass = config.get_setting("stormtvpassword")                                                                                                                             
    server= "https://"+__server__+"/stormtv/public/"                                                                                                                              
    path=config.get_data_path()+"stormtv/temp/"
    if not os.path.exists(path): 
       logger.info ("[stormtv.py]Creating data_path "+path)
       try:            
          mkdir_p(path) 
       except:            
          logger.info("[stormtv.py] Mainlist  Fallo crear directorio")
          pass            

    #<li class="thumb-episode"> <a href="/serie/como-conoci-a-vuestra-madre" title="Cómo conocí a vuestra madre"><img class="img-shadow" src="/img/series/170x243/como-conoci-a-vuestra-madre.jpg" height="166" width="115"></a> <strong><a href="/serie/como-conoci-a-vuestra-madre" title="Cómo conocí a vuestra madre">Cómo conocí a vuestra madre</a></strong> </li> 
    #matches = re.compile('<li class="thumb-episode"> <a href="([^"]+)" title="([^"]+)".*?src="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search"    , thumbnail=server+"buscar.jpg", title="Buscar", url="",fanart=server+"logo.jpg"))
    urllib.urlretrieve (server+"tvseries/following/user/"+user_id+"/pass/"+user_pass, path+"temp.xml")                             
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
        print name                                                                                                         
    	seriesyonkis = id
    	plot=""
    	scrapedplot=plot
    	art=server+fanart      

        # Depuracion
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
    	itemlist.append( Item(channel=__channel__, action="channel" , title=name, fulltitle=name , url=seriesyonkis, thumbnail=server+poster, plot=scrapedplot, viewmode="movie", show=id ,fanart=art))

    return itemlist
def channel(item):
	storm_show=item.show
	storm_thumbnail=item.thumbnail
	storm_plot=item.plot
	storm_fanart=item.fanart
	name = ""
	url = ""
	action=""
	server = "https://"+__server__+"/stormtv/public/tvseries/getchannelsxml/id/"+storm_show
	#logger.info ("[stormtv] channel"+item.fanart+"#")
	path=config.get_data_path()+"stormtv/temp/"                                   
	urllib.urlretrieve (server, path+"temp.xml")            
        xml=path+"temp.xml"                                                                                              
        doc = minidom.parse(xml)                                                                                             
        node = doc.documentElement                                                                                           
        series = doc.getElementsByTagName("channel")  
        itemlist = []  
        #fanart = "https://"+__server__+"/stormtv/public/248943/fanart.jpg" 
        print "fanart="+item.fanart                                                                      
        for serie in series:                                                                                                 
	        name=serie.getElementsByTagName("name")[0].childNodes[0].data                                                 
                url=serie.getElementsByTagName("url")[0].childNodes[0].data
                #if (name=="seriespepito"):
                #	action="episodelist"
                #else:
                #	action="episodios"
                itemlist.append( Item(channel=__channel__, action="channeltvs" , title=name, fulltitle=name , url=url, thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show, fanart=storm_fanart, extra=action))                                                      
	
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
	# le quitamos el ultimo elemento que es a�adir a la biblioteca de xbmc solo si es seriespepito o seriesyonkis
	if (storm_channel_name in biblioteca):
		itemlist = itemlist_p[0:len(itemlist_p)-1]
	else:
		itemlist = itemlist_p
	storm_itemlist=[]
	if (config.get_setting("stormtvaccount")=="true"):
	        from core import stormlib
	        chap_dictionary=stormlib.getwatched(storm_show)
	                
	for item in itemlist:
		# comprobar si esta visto y a�adir visto.
		if (config.get_setting("stormtvaccount")=="true"):    
	                from core import stormlib                     
	                title, extra = stormlib.iswatched(item.title,chap_dictionary)
	        else:                                                           
	                extra=""                                                
	        logger.info("[seriesyonkis.py] extra="+extra)  	
		storm_itemlist.append( Item(channel=__channel__,action="findvideos", fulltitle=storm_channel_name, title=title, url=item.url,thumbnail=storm_thumbnail, plot=storm_plot, viewmode="movie", show=storm_show,fanart=storm_fanart, extra=extra))
	return storm_itemlist

def findvideos(item):
	logger.info("[stormtv.py] Findvideos")
        storm_fanart=item.fanart                                                                                                                                                        
        storm_plot=item.plot                                                                                                                                                            
        storm_thumbnail=item.thumbnail                                                                                                                                                  
        storm_chapter=item.extra                                                                                                                                                         
        storm_show=item.show                                                                                                                                                            
        storm_channel_name=item.fulltitle                                                                                                                                                   
        storm_title=item.title
        action="findvideos"                                                                                                                                                          
	item=Item(channel=__channel__,url=item.url)                                                                                                                               
        exec "import pelisalacarta.channels."+storm_channel_name+" as channel"                                                                                                          
        # El action nos devolvera el listado de posibles enlaces                                                                                             
        exec "itemlist = channel."+action+"(item)"                                                                                                                                
        storm_itemlist=[]                                                      
	for item in itemlist:
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
	                 	
# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    episode_items = lastepisodes(mainlist_items[0])
    bien = False
    for episode_item in episode_items:
        mediaurls = findvideos( episode_item )
        if len(mediaurls)>0:
            return True

    return False