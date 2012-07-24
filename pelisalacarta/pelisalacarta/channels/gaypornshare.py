# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para gaypornshare.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

#from pelisalacarta import buscador

__channel__ = "gaypornshare"
__category__ = "D"
__type__ = "generic"
__title__ = "gaypornshare"
__language__ = "ES"

DEBUG = config.get_setting("debug")

IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'gaypornshare' )

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("[gaypornshare.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lista"  , title="Todas las Películas" , url="http://gaypornshare.org/category/gay/movies-gay/",thumbnail="http://t1.pixhost.org/thumbs/3282/12031567_a152063_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="categorias"  , title="Pel�culas por categor�as", thumbnail="http://t4.pixhost.org/thumbs/1423/13368595_01776683.jpg" ))    
    itemlist.append( Item(channel=__channel__, title="Buscar"     , action="search") )
    return itemlist


def categorias(item):
    logger.info("[gaypornshare.py] categorias")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="lista"  , title="3D" , url="http://gaypornshare.org/category/movies-gay/3d",thumbnail="http://t3.pixhost.org/thumbs/2406/13287669_a145219_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="alt" , url="http://gaypornshare.org/category/movies-gay/alt",thumbnail="http://t1.pixhost.org/thumbs/3543/13374028_a152431_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="amateur" , url="http://gaypornshare.org/category/movies-gay/amateur",thumbnail="http://t2.pixhost.org/thumbs/3902/13350247_a145925_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="anal" , url="http://gaypornshare.org/category/movies-gay/anal",thumbnail="http://t3.pixhost.org/thumbs/2427/13376171_a159372_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="asian" , url="http://gaypornshare.org/category/movies-gay/asian",thumbnail="http://t2.pixhost.org/thumbs/3903/13354885_01774517.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="bareback" , url="http://gaypornshare.org/category/movies-gay/bareback",thumbnail="http://t4.pixhost.org/thumbs/1418/13350208_a144470_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="BDSM" , url="http://gaypornshare.org/category/movies-gay/bdsm",thumbnail="http://t4.pixhost.org/thumbs/1423/13368605_01776333.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="bear" , url="http://gaypornshare.org/category/movies-gay/bear",thumbnail="http://t1.pixhost.org/thumbs/3504/13184351_a43961_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="big dick" , url="http://gaypornshare.org/category/movies-gay/big-dick",thumbnail="http://t2.pixhost.org/thumbs/3903/13354953_a157347_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="black" , url="http://gaypornshare.org/category/movies-gay/black",thumbnail="http://t1.pixhost.org/thumbs/3543/13376214_a156490_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="blowjob" , url="http://gaypornshare.org/category/movies-gay/blowjob",thumbnail="http://t4.pixhost.org/thumbs/1010/11905861_a114953_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="boyfriends" , url="http://gaypornshare.org/category/movies-gay/boyfriends",thumbnail="http://t2.pixhost.org/thumbs/3892/13304361_a63320_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="brazilian" , url="http://gaypornshare.org/category/movies-gay/brazilian",thumbnail="http://t3.pixhost.org/thumbs/2352/13066777_a30748_bb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="british" , url="http://gaypornshare.org/category/movies-gay/british",thumbnail="http://t1.pixhost.org/thumbs/3516/13249470_a67790_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="classic" , url="http://gaypornshare.org/category/movies-gay/classic",thumbnail="http://t3.pixhost.org/thumbs/2337/13009291_a72331_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="compilation" , url="http://gaypornshare.org/category/movies-gay/compilation",thumbnail="http://t4.pixhost.org/thumbs/1318/12982381_a125517_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="cops" , url="http://gaypornshare.org/category/movies-gay/cops",thumbnail="http://t4.pixhost.org/thumbs/1401/13286683_a90254_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="cowboy" , url="http://gaypornshare.org/category/movies-gay/cowboy",thumbnail="http://t2.pixhost.org/thumbs/3820/12982546_a71904_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="cream pies" , url="http://gaypornshare.org/category/movies-gay/cream-pies",thumbnail="http://t4.pixhost.org/thumbs/1420/13354851_a159313_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="cumshots" , url="http://gaypornshare.org/category/movies-gay/cumshots",thumbnail="http://t4.pixhost.org/thumbs/1423/13368615_a118665_xlb.jpg"))    
    itemlist.append( Item(channel=__channel__, action="lista"  , title="czech" , url="http://gaypornshare.org/category/movies-gay/czech",thumbnail="http://t3.pixhost.org/thumbs/2421/13350148_a125949_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="dildo" , url="http://gaypornshare.org/category/movies-gay/dildo",thumbnail="http://t3.pixhost.org/thumbs/2422/13358326_a123226_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="euro" , url="http://gaypornshare.org/category/movies-gay/euro",thumbnail="http://t1.pixhost.org/thumbs/3543/13373875_a155079_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="extreme penetration" , url="http://gaypornshare.org/category/movies-gay/extreme-penetration",thumbnail="http://t2.pixhost.org/thumbs/3867/13185009_a142219_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="feature" , url="http://gaypornshare.org/category/movies-gay/feature",thumbnail="http://t2.pixhost.org/thumbs/3884/13262888_a158515_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="fetish" , url="http://gaypornshare.org/category/movies-gay/fetish",thumbnail="http://t2.pixhost.org/thumbs/3893/13307187_01769111.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="fratboys" , url="http://gaypornshare.org/category/movies-gay/fratboys",thumbnail="http://t4.pixhost.org/thumbs/1420/13358640_a104346_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="gangbang" , url="http://gaypornshare.org/category/movies-gay/ganbang",thumbnail="http://t2.pixhost.org/thumbs/3820/12982623_a158094_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="gloryhole" , url="http://gaypornshare.org/category/movies-gay/gloryhole",thumbnail="http://t1.pixhost.org/thumbs/3478/13054879_a158773_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="hardcore" , url="http://gaypornshare.org/category/movies-gay/hardcore",thumbnail="http://t2.pixhost.org/thumbs/3891/13298360_a22817_bb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="HD" , url="http://gaypornshare.org/category/movies-gay/hd",thumbnail="http://t4.pixhost.org/thumbs/1340/13054247_a158312_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="international" , url="http://gaypornshare.org/category/movies-gay/international",thumbnail="http://t4.pixhost.org/thumbs/1426/13376137_a159413_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="jocks" , url="http://gaypornshare.org/category/movies-gay/jocks",thumbnail="http://t4.pixhost.org/thumbs/1426/13376137_a159413_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="latin" , url="http://gaypornshare.org/category/movies-gay/latin",thumbnail="http://t2.pixhost.org/thumbs/3892/13307165_a144964_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="leather" , url="http://gaypornshare.org/category/movies-gay/leather",thumbnail="http://t4.pixhost.org/thumbs/1413/13327781_a104644_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="masturbation" , url="http://gaypornshare.org/category/movies-gay/masturbation",thumbnail="http://t1.pixhost.org/thumbs/3538/13350257_a97399_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="mature" , url="http://gaypornshare.org/category/movies-gay/mature",thumbnail="http://t2.pixhost.org/thumbs/3893/13307257_a155639_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="military" , url="http://gaypornshare.org/category/movies-gay/military",thumbnail="http://t2.pixhost.org/thumbs/3908/13376185_a87562_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="muscles" , url="http://gaypornshare.org/category/movies-gay/muscles",thumbnail="http://t4.pixhost.org/thumbs/1421/13359204_a143580_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="orgies" , url="http://gaypornshare.org/category/movies-gay/orgies",thumbnail="http://t4.pixhost.org/thumbs/1403/13293647_a33600_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="outdoors" , url="http://gaypornshare.org/category/movies-gay/oudoors",thumbnail="http://t1.pixhost.org/thumbs/3543/13373847_a154217_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="parody" , url="http://gaypornshare.org/category/movies-gay/parody",thumbnail="http://t3.pixhost.org/thumbs/2410/13304290_a15441_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="pigs" , url="http://gaypornshare.org/category/movies-gay/pigs",thumbnail="http://t4.pixhost.org/thumbs/1318/12982321_a158775_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="pssing" , url="http://gaypornshare.org/category/movies-gay/pissing",thumbnail="http://t4.pixhost.org/thumbs/1413/13328226_a145751_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="pre-condom" , url="http://gaypornshare.org/category/movies-gay/pre-condom",thumbnail="http://t3.pixhost.org/thumbs/2416/13328208_a72336_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="prision sex" , url="http://gaypornshare.org/category/movies-gay/prision-sex",thumbnail="http://t4.pixhost.org/thumbs/1404/13298242_a68180_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="str8 bait" , url="http://gaypornshare.org/category/movies-gay/str8-bait",thumbnail="http://t2.pixhost.org/thumbs/3908/13376185_a87562_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="thug" , url="http://gaypornshare.org/category/movies-gay/thug",thumbnail="http://t3.pixhost.org/thumbs/2419/13342156_a98904_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="twink" , url="http://gaypornshare.org/category/movies-gay/twink",thumbnail="http://t2.pixhost.org/thumbs/3903/13354867_a155525_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="uncut" , url="http://gaypornshare.org/category/movies-gay/uncut",thumbnail="http://t1.pixhost.org/thumbs/3543/13373875_a155079_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="uniform" , url="http://gaypornshare.org/category/movies-gay/uniform",thumbnail="http://t2.pixhost.org/thumbs/3903/13354938_a159141_xlb.jpg"))  
    itemlist.append( Item(channel=__channel__, action="lista"  , title="vintage" , url="http://gaypornshare.org/category/movies-gay/vintage",thumbnail="http://t1.pixhost.org/thumbs/3516/13250179_01759057.jpg"))  
  
    return itemlist





def lista(item):
    logger.info("[gaypornshare.py] lista")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info(data)



    # Extrae las entradas (carpetas)
    patronvideos ='<div class="thumb">.*?<a href="([^"]+)".*?<img src="([^"]+)".*?alt="([^"]+)".*?</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = scrapedtitle.replace("&#8211;","-")
        scrapedtitle = scrapedtitle.replace("&#8217;","'")
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        imagen = ""
        scrapedplot = match[0]  
        tipo = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        scrapedplot=strip_tags(scrapedplot)
        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
 
 
  
  # Extrae la marca de siguiente página

    patronvideos ="<a href='([^']+)' class='nextpostslink'>([^']+)</a>"
    matches2 = re.compile(patronvideos,re.DOTALL).findall(data)

    for match2 in matches2:
        scrapedtitle = ">> siguiente"
        scrapedurl = match2[0]
        scrapedthumbnail = ""
        imagen = ""
        scrapedplot = match2[0]  
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="lista", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
 
 
    return itemlist







def search(item,texto):
    logger.info("[gaypornshare.py] search")
    itemlist = []

    # descarga la pagina
    data=scrapertools.downloadpageGzip("http://gaypornshare.org/?s="+texto)

    
    # Extrae las entradas (carpetas)
    patronvideos ='<div class="thumb">.*?<a href="([^"]+)".*?<img src="([^"]+)".*?alt="([^"]+)".*?</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = scrapedtitle.replace("&#8211;","-")
        scrapedtitle = scrapedtitle.replace("&#8217;","'")
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        imagen = ""
        scrapedplot = match[0]  
        tipo = match[1]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        scrapedplot=strip_tags(scrapedplot)
        itemlist.append( Item(channel=__channel__, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
 

   
  # Extrae la marca de siguiente página
    patronvideos ="<a href='([^']+)' class='nextpostslink'>([^']+)</a>"
    matches2 = re.compile(patronvideos,re.DOTALL).findall(data)

    for match2 in matches2:
        scrapedtitle = ">> página siguiente"
        scrapedurl = match2[0]
        scrapedthumbnail = ""
        imagen = ""
        scrapedplot = match2[0]  
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="lista", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
 
 

    return itemlist



def detail(item):
    logger.info("[gaypornshare.py] detail")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.downloadpageGzip(item.url)
    descripcion = ""
    plot = ""
    patrondescrip = 'SINOPSIS:(.*?)'
    matches = re.compile(patrondescrip,re.DOTALL).findall(data)
    if len(matches)>0:
        try :
            plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
        except:
            plot = descripcion

    # Busca los enlaces a los videos de : "Megavideo"
    video_itemlist = servertools.find_video_items(data=data)
    for video_item in video_itemlist:
        itemlist.append( Item(channel=__channel__ , action="play" , server=video_item.server, title=item.title+video_item.title,url=video_item.url, thumbnail=item.thumbnail, plot=item.plot, folder=False))

    # Extrae los enlaces a los videos (Directo)
    patronvideos = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        if not "www.youtube" in matches[0]:
            itemlist.append( Item(channel=__channel__ , action="play" , server="Directo", title=item.title+" [directo]",url=matches[0], thumbnail=item.thumbnail, plot=item.plot))

    return itemlist
    
    

