# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Argia Multimedia
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[argia.py] init")

DEBUG = False
CHANNELNAME = "argia"
CHANNELCODE = "argia"

MAINURL = "http://www.argia.com"
VIDEOURL = "http://www.argia.com/multimedia"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[antena3.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Denak"            , action="videolist" , url="http://www.argia.com/multimedia?p=1", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Gomendatuak"      , action="recommended" , url=VIDEOURL, folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Asteko ikusienak" , action="mostviewed" , url=VIDEOURL, folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Bideoak"          , action="videolist" , url="http://www.argia.com/multimedia/bideoak?p=1", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Ekitaldiak"       , action="videolist" , url="http://www.argia.com/multimedia/ekitaldiak?p=1", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Film laburrak"    , action="videolist" , url="http://www.argia.com/multimedia/laburrak?p=1", folder=True) )
    
    return itemlist

def videolist(item):
    logger.info("[argia.py] videolist")
    itemlist = []

    # Page downloading
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Get #Next url
    '''
    <a href="?p=2" title="Hurrengo orria">Hurrengoak»</a>
    '''
    pattern = '<a href="([^"]+)" title="Hurrengo orria">Hurrengoak'    # 0: url
    matches = re.compile(pattern,re.DOTALL).findall(data)
    
    try:
        urlnextpage = item.url[:-4]+matches[0]
    except:
        urlnextpage = ""
    
    if (DEBUG):
        logger.info("urlnextpage="+urlnextpage)
    
    if urlnextpage != "":
        # Add NEXT (as first item)
        scrapedtitle = "#Hurrengoak"
        scrapedurl = urlnextpage
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, folder=True) )

    # Parse first video item
    '''
    <div class="titularplayer"><h1><a href="/multimedia/bideoa/pello-urizar">Pello Urizar</a></h1>
    <p>Arrasate, 1968. Gazte Abertzaleak-eko idazkari nagusia izana. Arrasateko Udalean zinegotzia da. Elektronika eta Informatika ingeniari teknikoa. Kooperatibismoaren lan esperientzian zaildua, eta politikaren goi-mailara iritsia. Egun, Eusko Alkartasuneko idazkari nagusia da.</p>
    '''
    pattern =    '''(?x)                                                            # Activate VERBOSE
        <div\ class="titularplayer"><h1>                                        #
        <a\ href="([^"]+)"                                                        # $0 = video page url
        >([^<]+)</a></h1>.*?                                                    # $1 = title
        <p>([^<]+)<                                                                # $2 = description
                '''
    matches = re.compile(pattern,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    
    if len(matches) > 0:
        scrapedtitle = matches[0][1]+" (BERRIA!)".replace("&#39;","'").strip()
        scrapedurl = MAINURL+matches[0][0].replace("&amp;","&")
        scrapedthumbnail = ""
        scrapedplot = matches[0][2].replace("&#39;","'").strip()
        
        try:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )
        except:
            logger.info("[argia.py] videolist: ERROR, i can't found first special video")
    
    # Parse video list
    '''
    <div class="infoBideo">
    <p><a href="/multimedia/bideoa/larraulgo-eskola-12-urtera-arte"><img src="/multimedia/docs/bideoak/t_larrauljaurlaritza.jpg" alt="irudia" border="0" height="82" width="136"></a>
    <span class="titularpestaina"><a href="/multimedia/bideoa/larraulgo-eskola-12-urtera-arte">Larraulgo eskola 12 urtera arte</a></span><br> 
    Larraulgo (Gipuzkoa) eskolan Haur Hezkuntza (6 urtera artekoa) ematen da 2008an ireki zenetik. Larraulgo udalaren eta guraso elkartearen eskaria beti izan da Lehen Hezkuntza osoa (12 urtera artekoa)...</p>
    </div>
    
    <div class="infoBideo">
    <p><a href="/multimedia/laburra/raskaana"><img src="/multimedia/docs/bideoak/t_raskaana.jpg" alt="irudia" width="136" height="82" border="0" /></a>
    
    <span class="titularpestaina" ><a href="/multimedia/laburra/raskaana">Raskaana</a></span><br /> 
    Egilea: Oier U. (<a href="http://anpulubila.tximinia.net" title="Ireki esteka leiho berri batean" target="_blank">anpulubila.tximinia.net</a>)</p>
    </div>
    '''
    
    pattern =    '''(?x)                                                            # Activate VERBOSE
        <div\ class="info.*?">.*?                                                #
        <p><a\ href="([^"]+)">                                                    # $0 = video page url
        <img\ src="([^"]+)".*?                                                    # $1 = thumbnail url
        <span\ class="titular.*?".*?><.*?                                        #
        >([^<]+)</a><.*?><.*?                                                    # $2 = title
        >([^<]+)<                                                                # $3 = description
                '''
    matches = re.compile(pattern,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        # Is it a video? Suuure?
        if match[0].split('/')[2] != 'galeria' and match[0].split('/')[2] != 'diaporama':
            scrapedtitle = match[2].replace("&#39;","'").strip()
            scrapedurl = MAINURL+match[0].replace("&amp;","&")
            scrapedthumbnail = MAINURL+match[1].replace("&amp;","&")
            scrapedplot = match[3].replace("&#39;","'").strip()
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], description=["+scrapedplot+"]")

            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def recommended(item):
    logger.info("[argia.py] recommended")
    itemlist = []
    # Page downloading
    data = scrapertools.cachePage(item.url)
    
    # Parse data
    '''
    <div class="itemtxuri">
                    <p><a href="/multimedia/diaporama/zabor-mendietako-bizitzak"><img src="/multimedia/docs/diaporamak/t_zaborraZabalza.jpg" alt="irudia" width="135" height="82" border="0" /></a>
                    <a href="/multimedia/diaporama/zabor-mendietako-bizitzak"><span class="titularpestaina">Zabor mendietako bizitzak</span></a><br /> 
                      Zakarra azkenaldiko eztabaidagai nagusi bilakatzeak ondorio garbi bat dakar: baztertu, estali eta...</p>
                  </div>

    '''
    
    pattern =    '''(?x)                                                            # Activate VERBOSE
        <div\ class="item.*?">.*?                                                #
        <p><a\ href="([^"]+)">                                                    # $0 = video page url
        <img\ src="([^"]+)".*?                                                    # $1 = thumbnail url
        <span\ class="titular.*?"                                                #
        >([^<]+)</span></a><.*?                                                    # $2 = title
        >([^<]+)</p>                                                            # $3 = description
                '''
    matches = re.compile(pattern,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    
    matchid = 0
    for match in matches:
        # Only first 15 elements are "Recommended"
        if matchid < 15:
            # Is it a video? Suuure?
            ##logger.info("[argia.py] recommended: Split"+match[0].split('/')[2])
            if match[0].split('/')[2] != 'galeria' and match[0].split('/')[2] != 'diaporama':
                scrapedtitle = match[2].replace("&#39;","'").strip()
                scrapedurl = MAINURL+match[0].replace("&amp;","&")
                scrapedthumbnail = MAINURL+match[1].replace("&amp;","&")
                scrapedplot = match[3].replace("&#39;","'").strip()
                #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], description=["+scrapedplot+"]")
                # Add item
                itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )
        matchid = matchid+1
    
    return itemlist

def mostviewed(item):
    logger.info("[argia.py] mostviewed")
    itemlist = []
    # Page downloading
    data = scrapertools.cachePage(item.url)
    
    # Parse data
    '''
    <div class="itemtxuri">
                    <p><a href="/multimedia/diaporama/zabor-mendietako-bizitzak"><img src="/multimedia/docs/diaporamak/t_zaborraZabalza.jpg" alt="irudia" width="135" height="82" border="0" /></a>
                    <a href="/multimedia/diaporama/zabor-mendietako-bizitzak"><span class="titularpestaina">Zabor mendietako bizitzak</span></a><br /> 
                      Zakarra azkenaldiko eztabaidagai nagusi bilakatzeak ondorio garbi bat dakar: baztertu, estali eta...</p>
                  </div>

    '''
    
    pattern =    '''(?x)                                                            # Activate VERBOSE
        <div\ class="item.*?">.*?                                                #
        <p><a\ href="([^"]+)">                                                    # $0 = video page url
        <img\ src="([^"]+)".*?                                                    # $1 = thumbnail url
        <span\ class="titular.*?"                                                #
        >([^<]+)</span></a><.*?                                                    # $2 = title
        >([^<]+)</p>                                                            # $3 = description
                '''
    matches = re.compile(pattern,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    matchid = 0
    for match in matches:
        # First 15 elements are "Recommended"
        if matchid > 14:
            # Is it a video? Suuure?
            ##logger.info("[argia.py] recommended: Split"+match[0].split('/')[2])
            if match[0].split('/')[2] != 'galeria' and match[0].split('/')[2] != 'diaporama':
                scrapedtitle = match[2].replace("&#39;","'").strip()
                scrapedurl = MAINURL+match[0].replace("&amp;","&")
                scrapedthumbnail = MAINURL+match[1].replace("&amp;","&")
                scrapedplot = match[3].replace("&#39;","'").strip()
                #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], description=["+scrapedplot+"]")
                # Add item
                itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )
        matchid = matchid+1
    
    return itemlist

def getvideo(item):
    logger.info("[argia.py] play")
    itemlist = []
    
    # Page downloading
    data = scrapertools.cachePage(item.url)
    
    ##
    ## PARSE VIDEO DATA
    ##
    '''
    s1.addParam('flashvars','file=/multimedia/docs/bideoak/EricCantona.flv&image=/multimedia/docs/bideoak/EricCantona.jpg');
    '''
    pattern = "s1.addParam.'flashvars','file\=([^\&]+)\&"
    matches = re.compile(pattern,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    try:
        url = MAINURL+matches[0]
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail, plot=item.plot , server="Directo" , folder=False) )
    except:
        url = ""

    return itemlist