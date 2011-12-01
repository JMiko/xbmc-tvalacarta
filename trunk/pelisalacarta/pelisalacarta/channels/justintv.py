# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para justin.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import xbmc,xbmcgui,xbmcplugin

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
from platformcode.xbmc import xbmctools
try:
    import json
except:
    import simplejson as json

CHANNELNAME = "justintv"
DEBUG = True
pluginhandle = int(sys.argv[1])
IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'posters' ) )
fanart = xbmc.translatePath(os.path.join( config.get_runtime_path(), 'resources' , 'images' ,'fanart','justintv.png'))

all = config.get_localized_string(30419)
languages = [all,'Arabic','Català','Cerky','Dansk','Deutsch','Greek','English','Español','Eusti Keel','suomi','Francais',
            'Hindi' ,'Hrvatski','bahasa Indonesia','Italiano','Hebrew','Japanese','Korean','Lietuviu','Nederlands',
            'Norsk','Polski','Portugues','Romana','Russian','Serbian','Svenska','Talagog','Turkey','Tieng Viet',
            'Chinese','Taiwanese']
abbrev   = ['all','ar','ca','cs','da','de','el','en','es','et','fi','fr','hi','hr','id','it','iw','ja','ko','lt','nl','no','pl','pt',
            'ro','ru','sr','sv','tl','tr','vi','zh-CN','zh-TW']
limit = 50

def isGeneric():
    return True

def mainlist(item):
    logger.info("[justintv.py] mainlist")

    itemlist = []
    try:
        lang = config.get_setting('justin_lang')
        idx  = abbrev.index(lang)
    except:
        lang = 'all'
        idx  = abbrev.index(lang)
    lang = languages[idx]
    #itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30407), action="subCategories" ,url = "featured", thumbnail="http://www-cdn.jtvnw.net/images/categories/featured.png"))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30420) + ' (%s)' %lang, action="_language"     ,url = "", thumbnail = os.path.join(IMAGES_PATH, "language.jpg"),fanart = fanart,folder=False))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30408), action="subCategories" ,url = "social", thumbnail="http://www-cdn.jtvnw.net/images/categories/social.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30409), action="subCategories" ,url = "entertainment", thumbnail="http://www-cdn.jtvnw.net/images/categories/entertainment.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30410), action="subCategories" ,url = "gaming", thumbnail="http://www-cdn.jtvnw.net/images/categories/gaming.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30411), action="subCategories" ,url = "sports", thumbnail="http://www-cdn.jtvnw.net/images/categories/sports.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30412), action="subCategories" ,url = "news", thumbnail="http://www-cdn.jtvnw.net/images/categories/news.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30413), action="subCategories" ,url = "animals", thumbnail="http://www-cdn.jtvnw.net/images/categories/animals.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30414), action="subCategories" ,url = "science_tech", thumbnail="http://www-cdn.jtvnw.net/images/categories/science_tech.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30415), action="subCategories" ,url = "other", thumbnail="http://www-cdn.jtvnw.net/images/categories/other.png",fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30416), action="favorites"     ,url = "", thumbnail=os.path.join(IMAGES_PATH, "favoritos.png"),fanart = fanart))
    itemlist.append( Item(channel=CHANNELNAME, title=config.get_localized_string(30417), action="search"        ,url = "", thumbnail=os.path.join(IMAGES_PATH, "buscador.png"),fanart = fanart))
    


    return itemlist

def search(item,texto):
    
    texto = texto.replace(' ','+')
    item.title = 'search'
    item.url = url =  'http://api.justin.tv/api/stream/search/'+texto+'.json?offset=0&limit='+str(limit)
    itemlist = getlistchannel(item)
    xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
    return

def subCategories(item):
    logger.info("[justin.tv.py] subCategories")

    category = item.url
    
    url = "http://api.justin.tv/api/category/list.json"
    data = scrapertools.cache_page(url)
    logger.info(data)
    itemlist = []
    datadict = json.loads(data)
    scrapedthumbnail = ""
    scrapedplot = ""
    itemlist.append( Item(channel=item.channel , action="listchannel"   , title=config.get_localized_string(30421) , url="all" , thumbnail=scrapedthumbnail, plot=scrapedplot,category=category,fanart=fanart ))
    for match in datadict[category]['subcategories'].keys():
        scrapedurl = match
        scrapedtitle =datadict[category]['subcategories'][match]['name']

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A?ade al listado de XBMC
        itemlist.append( Item(channel=item.channel , action="listchannel"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot,category=category,fanart=fanart ))
    
    return itemlist

def favorites(item):
    if item.url == '':
        username = config.get_setting("justin_login")
    else:
        username = item.url
    if username == "":
        LoginEmpty()
        config.open_settings()
        item.url = config.get_setting("justin_login")
        if item.url == '':return
        favorites(item)
        return 
    item.title = "favorites"
    item.url = 'http://api.justin.tv/api/user/favorites/'+str(username)+'.json?offset=0&limit='+str(limit)+'&live=true'
    itemlist = getlistchannel(item)
    xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
    return 

def listchannel(item):
    
    if not "|Next Page >>" in item.title:
        try:
            lang = config.get_setting("justin_lang")
        except:
            lang = "all"
        item.title = item.url
        if lang == 'all':
            lang = ''
        else:
            lang = '&language='+lang
        if 'all' in item.url:
            item.url = "http://api.justin.tv/api/stream/list.json?category=%s%s&offset=0&limit=%d" %(item.category,lang,limit)
        else:
            item.url = "http://api.justin.tv/api/stream/list.json?subcategory=%s%s&offset=0&limit=%d" %(item.title,lang,limit)
    itemlist = getlistchannel(item)
    xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
    return 

def getlistchannel(item):
    logger.info("[justintv.py] getlistchannel")
    
    url = item.url
    title = item.title
    if "|Next Page >>" in item.title:
        item.title = item.title.split('|')[0]
    data = scrapertools.cache_page(url)
    #logger.info(data)
    datadict = json.loads(data)
    totalItems = len(datadict)
    itemlist = []
    #print item.action
    c = 0
    for match in datadict:
        try:
            scrapedtitle = match['name'].split('user_')[-1]
        except:
            try:
                scrapedtitle = match['channel']['login']
            except:
                scrapedtitle = match['login']
        try:
            title = match['title']
        except:
            title = match['channel']['title']
        try:
            title = scrapertools.unescape(title).decode('utf-8', "replace")
        except:
            try:
                title = scrapertools.unescape(match['channel']['tags']).decode('utf-8', "replace")
            except:
                try:
                    title = scrapertools.unescape(match['tags']).decode('utf-8', "replace").strip()
                except:
                    try:
                        title = scrapertools.unescape(match['channel']['status']).decode('utf-8', "replace").strip()
                    except:
                        try:
                            title = scrapertools.unescape(match['status']).decode('utf-8', "replace").strip()
                        except:
                            title = ''
        try:
            bitrate = str(match['video_bitrate']).split('.')[0]
        except:
            bitrate = ''
        try:
            lang = match['language']
        except:
            lang = ''
        try:
            scrapedthumbnail = match['channel']['screen_cap_url_medium']
        except:
            scrapedthumbnail = match['screen_cap_url_medium']
        scrapedurl = scrapedtitle
        scrapedtitle = title + ' [%s] BitRate: %s  Language: %s' %(scrapedtitle,bitrate,lang)

        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=item.channel , action="playVideo"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, totalItems=totalItems,fanart = scrapedthumbnail,  folder=False ))

    if totalItems >=limit:
        offset1 = re.compile('offset=(.+?)&').findall(url)[0]
        offset2 = str(int(offset1)+limit+1)
        scrapedurl = item.url.replace("offset="+offset1,"offset="+offset2)
        scrapedtitle = item.title+"|Next Page >>"
        scrapedthumbnail = ''
        scrapedplot = ''
        itemlist.append( Item(channel=item.channel , action="listchannel"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, category=item.category, fanart=fanart ))
    return itemlist

def playVideo(item):
    logger.info("[justin.tv.py] play")
    channelname=item.url
    req = urllib2.Request('http://justin.tv/')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match = re.compile('swfobject.embedSWF\("(.+?)"').findall(link)
    swf = ' swfUrl='+str(match[0])
    req = urllib2.Request('http://usher.justin.tv/find/'+channelname+'.json?type=live')
    req.addheaders = ('Referer', 'http://justin.tv/')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    logger.info(link)
    datadict = json.loads(link)
    try:
        token = ' jtv='+datadict[0]["token"].replace('\\','\\5c').replace('"','\\22').replace(' ','\\20')
        connect = datadict[0]["connect"]+'/'+datadict[0]["play"]
        Pageurl = ' Pageurl=http://www.justin.tv/'+channelname
        rtmp = connect+token+swf+Pageurl
        logger.info('rtmp = %s'%rtmp)
        listItem = xbmcgui.ListItem(path = rtmp)
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(pluginhandle, True, listItem)
    except:
        logger.info('canal %s esta offline'%channelname)
        channeloffline(channelname)

def _language(item):
    
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Choice a language", languages)
    if seleccion == -1:return
    print "seleccion :",seleccion
    abb = abbrev[seleccion]
    config.set_setting('justin_lang',abb)
    xbmc.executebuiltin( "Container.Refresh" )
    return
    
def LoginEmpty():
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ,"                  "+config.get_localized_string(30422))
def channeloffline(channelname):
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ,"     "+config.get_localized_string(30423) %channelname)