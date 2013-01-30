﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs,unpackerjs3

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def form(data, page_url):
    try:
        patron  = '<input type="hidden" name="op" value="([^"]+)">[^<]+'
        patron += '<input type="hidden" name="usr_login" value="">[^<]+'
        patron += '<input type="hidden" name="id" value="([^"]+)">[^<]+'
        patron += '<input type="hidden" name="fname" value="([^"]+)">[^<]+'
        patron += '<input type="hidden" name="referer" value="">[^<]+'
        patron += '<input type="hidden" name="method_free" value="([^"]+)">[^<]+'
        patron += '<input type="image"  id="submitButton" src="[^"]+" value="([^"]+)" />.*?'
        patron += '<input name="confirm" type="submit" value="([^"]+)" disabled=.*?>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)==0:
            return []
        
        video_urls = []
        op = matches[0][0]
        usr_login = ""
        id = matches[0][1]
        fname = matches[0][2]
        referer = ""
        method_free = matches[0][3]
        submitbutton = matches[0][4]
        submit = matches[0][5].replace(" ","+")
            
        headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free+"&submitButton="+submitbutton+"&confirm="+submit
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        
        #<script type='text/javascript'>eval(/* unpacking function - this is the boot strap function */ /* data extracted from this packing routine is passed to */ /* this function when decoded in the target */ function(p, a, c, k, e, d) { while (c--) if (k[c]) p = p.replace(new RegExp('\\b' + c.toString(a) + '\\b', 'g'), k[c]); /* RS_Debug = p; */ /* {RS} !!!!!!!!! */ return p; } (' c b=$.3k(\'3j\'); m (b==3i) b=0; 3h(\'3g\').3f({ \'3e\' : \'3d\', \'3c\' : \'w\', \'3b\' : \'3a\', \'t\' : \'4://39.9.8:y/d/38/37.36\', \'35\' : \'4://z.9.8/i/x/g.34\', \'33\' : \'32\', \'31\' : \'30\', \'2z\' : \'4\', \'4.2y\' : \'13\', \'q\' : \'11\', \'14.2x\' : \'u\', \'14.2w\' : \'2v\', \'13\' : b, \'2u\' : \'2t-2,2s-1,12-3,f-3,2r-1\', \'12.2q\' : { \'2p\' : 11, \'2o\' : \'4://z.9.8:y/p/x/g/\', \'2n\' : \'2m\', \'2l\' : 5, \'2k\': 10, \'2j\': 2i }, \'f.s\' : \'4://9.8/g\', \'f.2h\' : \'<v 2g="4://9.8/2f-2e-2d.r" 2c=0 2b=0 2a=0 29=28 27=w 26=25></v>\', \'24\' : \'/6/23.22\', \'a.21\' : \'u\', \'a.e\' : \'20-o\', \'a.t\' : \'/6/1z.1y\', \'a.s\' : \'/1x.r\', \'1w\' : \'/6/1v/1u.1t\', \'q.e\' : \'o\', \'1s.e\' : \'1r\', \'1q\': [ {n: \'1p\', 1o: \'/6/6.1n\'}, {n: \'1m\'} ] }); c 7 = 1l.1k(); c 1j = \'1i 1h 1g 6 \' + 7.l + \'.\' + 7.1f + \'.\' + 7.1e + \' 1d\'; m ((7.l < 1 ) && (k.j.h(\'1c\')==-1) && (k.j.h(\'1b\')==-1)) { 1a.19(\'18\').17.16 = \'15\'; } ',36,129,'||||http||player|playerVersion|net|allmyvideos|logo|starttime|var||position|sharing|0ah5ph2vxm8w|indexOf||appVersion|navigator|major|if|type|left||dock|html|link|file|false|IFRAME|720|00027|182|d3220||true|timeslidertooltipplugin|start|viral|block|display|style|flashnotinstalled|getElementById|document|Android|iPhone|installed|release|minor|Flash|have|You|output|getFlashPlayerVersion|swfobject|html5|swf|src|flash|modes|bottom|controlbar|zip|bekle|skins|skin|premium|png|gopremium|top|hide|xml|ova|config|403|HEIGHT|WIDTH|NO|SCROLLING|MARGINHEIGHT|MARGINWIDTH|FRAMEBORDER|720x383|h08ml8bdrpvw|embed|SRC|code|100|spritelength|linelength|frequency|0ah5ph2vxm8w_|prefix|path|enabled|preview|lightsout|fbit|captions|plugins|none|callout|onpause|startparam|provider|lighttpd|streamscript|4250|duration|jpg|image|mp4|video|y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdiegq4nk|d2739|383|height|width|playerID|id|setup|flvplayer|jwplayer|undefined|vpos0ah5ph2vxm8w|cookie'.split('|')))
        #</script>
        packed = scrapertools.get_match( data , "(<script type='text/javascript'>eval\(.*?function\(p,\s*a,\s*c,\s*k,\s*e,\s*d.*?)</script>",1)
        logger.info("packed="+packed)
        
        from core import unpackerjs
        unpacked = unpackerjs.unpackjs(packed)
        logger.info("unpacked="+unpacked)
        if unpacked=="":
            unpacked = unpackerjs3.unpackjs(packed,tipoclaves=2)
            logger.info("unpacked3="+unpackerjs3.unpackjs(packed,tipoclaves=2))
    
        #('var starttime=$.cookie(\'vposm7p03lbkysdw\');if(starttime==undefined)starttime=0;jwplayer(\'flvplayer\').setup({\'id\':\'playerID\',\'width\':\'960\',\'height\':\'511\',\'file\':\'http://66.220.4.230:182/d/3omdq77yq5dh6lnhlgzlnwmpjsz6jak4r4dalwptfh3auyzpfu2og6u/video.mp4\',\'image\':\'http://66.220.4.230/i/00012/m7p03lbkysdw.jpg\',\'duration\':\'5836\',\'streamscript\':\'lighttpd\',\'provider\':\'http\',\'http.startparam\':\'start\',\'dock\':\'true\',\'viral.onpause\':\'false\',\'viral.callout\':\'none\',\'start\':starttime,\'plugins\':\'captions-2,fbit-1,timeslidertooltipplugin-3,/player/ova-jw.swf,sharing-3\',\'timeslidertooltipplugin.preview\':{\'enabled\':true,\'path\':\'http://66.220.4.230:182/p/00012/m7p03lbkysdw/\',\'prefix\':\'m7p03lbkysdw_\'},\'sharing.link\':\'http://allmyvideos.net/m7p03lbkysdw\',\'sharing.code\':\'<IFRAME SRC="http://allmyvideos.net/embed-h08ml8bdrpvw-960x511.html" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=960 HEIGHT=531></IFRAME>\',\'config\':\'/player/ova.xml\',\'logo.hide\':\'false\',\'logo.position\':\'top-left\',\'logo.file\':\'/player/gopremium.png\',\'logo.link\':\'/premium.html\',\'skin\':\'/player/skins/bekle.zip\',\'dock.position\':\'left\',\'controlbar.position\':\'bottom\',\'modes\':[{type:\'flash\',src:\'/player/player.swf\'},{type:\'html5\'}]});var playerVersion=swfobject.getFlashPlayerVersion();var output=\'You have Flash player \'+playerVersion.major+\'.\'+playerVersion.minor+\'.\'+playerVersion.release+\' installed\';if((playerVersion.major<1)&&(navigator.appVersion.indexOf(\'iPhone\')==-1)&&(navigator.appVersion.indexOf(\'Android\')==-1)){document.getElementById(\'flashnotinstalled\').style.display=\'block\'}',511,00012player,
        unpacked = unpacked.replace("\\","")
        
        #'file' : 'http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjumszgt/video.mp4'
        #http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjtww5ha/video.mp4?start=0
        #http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjumszgt/video.mp4
        try:
            location = scrapertools.get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        except:
            location = scrapertools.get_match(unpacked,'"file"\s*\:\s*"([^"]+)"')+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        logger.info("location="+location)
        
        
        video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [allmyvideos]",location ] )
    
        for video_url in video_urls:
            logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))
    except:
        return []

    return video_urls

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Lee la URL
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers)
    video_urls = form(data, page_url)
    if len(video_urls) > 0:
        return video_urls
    
    
    patron =  "'file'\s*\:\s*'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        location = scrapertools.get_match(data,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [allmyvideos]",location ] )
        return video_urls
    
    
    for line in data.split('\n'):
        line2 = line
    
    #<script type='text/javascript'>eval(/* unpacking function - this is the boot strap function */ /* data extracted from this packing routine is passed to */ /* this function when decoded in the target */ function(p, a, c, k, e, d) { while (c--) if (k[c]) p = p.replace(new RegExp('\\b' + c.toString(a) + '\\b', 'g'), k[c]); /* RS_Debug = p; */ /* {RS} !!!!!!!!! */ return p; } (' c b=$.3k(\'3j\'); m (b==3i) b=0; 3h(\'3g\').3f({ \'3e\' : \'3d\', \'3c\' : \'w\', \'3b\' : \'3a\', \'t\' : \'4://39.9.8:y/d/38/37.36\', \'35\' : \'4://z.9.8/i/x/g.34\', \'33\' : \'32\', \'31\' : \'30\', \'2z\' : \'4\', \'4.2y\' : \'13\', \'q\' : \'11\', \'14.2x\' : \'u\', \'14.2w\' : \'2v\', \'13\' : b, \'2u\' : \'2t-2,2s-1,12-3,f-3,2r-1\', \'12.2q\' : { \'2p\' : 11, \'2o\' : \'4://z.9.8:y/p/x/g/\', \'2n\' : \'2m\', \'2l\' : 5, \'2k\': 10, \'2j\': 2i }, \'f.s\' : \'4://9.8/g\', \'f.2h\' : \'<v 2g="4://9.8/2f-2e-2d.r" 2c=0 2b=0 2a=0 29=28 27=w 26=25></v>\', \'24\' : \'/6/23.22\', \'a.21\' : \'u\', \'a.e\' : \'20-o\', \'a.t\' : \'/6/1z.1y\', \'a.s\' : \'/1x.r\', \'1w\' : \'/6/1v/1u.1t\', \'q.e\' : \'o\', \'1s.e\' : \'1r\', \'1q\': [ {n: \'1p\', 1o: \'/6/6.1n\'}, {n: \'1m\'} ] }); c 7 = 1l.1k(); c 1j = \'1i 1h 1g 6 \' + 7.l + \'.\' + 7.1f + \'.\' + 7.1e + \' 1d\'; m ((7.l < 1 ) && (k.j.h(\'1c\')==-1) && (k.j.h(\'1b\')==-1)) { 1a.19(\'18\').17.16 = \'15\'; } ',36,129,'||||http||player|playerVersion|net|allmyvideos|logo|starttime|var||position|sharing|0ah5ph2vxm8w|indexOf||appVersion|navigator|major|if|type|left||dock|html|link|file|false|IFRAME|720|00027|182|d3220||true|timeslidertooltipplugin|start|viral|block|display|style|flashnotinstalled|getElementById|document|Android|iPhone|installed|release|minor|Flash|have|You|output|getFlashPlayerVersion|swfobject|html5|swf|src|flash|modes|bottom|controlbar|zip|bekle|skins|skin|premium|png|gopremium|top|hide|xml|ova|config|403|HEIGHT|WIDTH|NO|SCROLLING|MARGINHEIGHT|MARGINWIDTH|FRAMEBORDER|720x383|h08ml8bdrpvw|embed|SRC|code|100|spritelength|linelength|frequency|0ah5ph2vxm8w_|prefix|path|enabled|preview|lightsout|fbit|captions|plugins|none|callout|onpause|startparam|provider|lighttpd|streamscript|4250|duration|jpg|image|mp4|video|y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdiegq4nk|d2739|383|height|width|playerID|id|setup|flvplayer|jwplayer|undefined|vpos0ah5ph2vxm8w|cookie'.split('|')))
    #</script>
    try:
        packed = scrapertools.get_match( data , "(<script type='text/javascript'>eval\(.*?function\(p,\s*a,\s*c,\s*k,\s*e,\s*d.*?)</script>",1)
        logger.info("packed="+packed)
        
        from core import unpackerjs
        unpacked = unpackerjs.unpackjs(packed)
        logger.info("unpacked="+unpacked)
        if unpacked=="":
            unpacked = unpackerjs3.unpackjs(packed,tipoclaves=2)
            logger.info("unpacked3="+unpackerjs3.unpackjs(packed,tipoclaves=2))
    
        #('var starttime=$.cookie(\'vposm7p03lbkysdw\');if(starttime==undefined)starttime=0;jwplayer(\'flvplayer\').setup({\'id\':\'playerID\',\'width\':\'960\',\'height\':\'511\',\'file\':\'http://66.220.4.230:182/d/3omdq77yq5dh6lnhlgzlnwmpjsz6jak4r4dalwptfh3auyzpfu2og6u/video.mp4\',\'image\':\'http://66.220.4.230/i/00012/m7p03lbkysdw.jpg\',\'duration\':\'5836\',\'streamscript\':\'lighttpd\',\'provider\':\'http\',\'http.startparam\':\'start\',\'dock\':\'true\',\'viral.onpause\':\'false\',\'viral.callout\':\'none\',\'start\':starttime,\'plugins\':\'captions-2,fbit-1,timeslidertooltipplugin-3,/player/ova-jw.swf,sharing-3\',\'timeslidertooltipplugin.preview\':{\'enabled\':true,\'path\':\'http://66.220.4.230:182/p/00012/m7p03lbkysdw/\',\'prefix\':\'m7p03lbkysdw_\'},\'sharing.link\':\'http://allmyvideos.net/m7p03lbkysdw\',\'sharing.code\':\'<IFRAME SRC="http://allmyvideos.net/embed-h08ml8bdrpvw-960x511.html" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=960 HEIGHT=531></IFRAME>\',\'config\':\'/player/ova.xml\',\'logo.hide\':\'false\',\'logo.position\':\'top-left\',\'logo.file\':\'/player/gopremium.png\',\'logo.link\':\'/premium.html\',\'skin\':\'/player/skins/bekle.zip\',\'dock.position\':\'left\',\'controlbar.position\':\'bottom\',\'modes\':[{type:\'flash\',src:\'/player/player.swf\'},{type:\'html5\'}]});var playerVersion=swfobject.getFlashPlayerVersion();var output=\'You have Flash player \'+playerVersion.major+\'.\'+playerVersion.minor+\'.\'+playerVersion.release+\' installed\';if((playerVersion.major<1)&&(navigator.appVersion.indexOf(\'iPhone\')==-1)&&(navigator.appVersion.indexOf(\'Android\')==-1)){document.getElementById(\'flashnotinstalled\').style.display=\'block\'}',511,00012player,
        unpacked = unpacked.replace("\\","")
        
        #'file' : 'http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjumszgt/video.mp4'
        #"file" : "http://d2605.allmyvideos.net:182/d/36mn2pp3yq5dh6lnapg4t2wqemadodnmj7hfyytjnkudpjjmjo665ztb/video.mp4"
        #http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjtww5ha/video.mp4?start=0
        #http://d2739.allmyvideos.net:182/d/y6miech5yq5dh6lnfxg4rygup54sl2d4ofgqf76ftqli47fzdjumszgt/video.mp4
        try:
            location = scrapertools.get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        except:
            location = scrapertools.get_match(unpacked,'"file"\s*\:\s*"([^"]+)"')+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        logger.info("location="+location)
    except:
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)
        location=""
    
    if location!="":
        '''
        <input type="hidden" name="op" value="download1">
        <input type="hidden" name="usr_login" value="">
        <input type="hidden" name="id" value="mg0al8ud92jr">
        <input type="hidden" name="fname" value="AreBrripAc32012.mp4">
        <input type="hidden" name="referer" value="">
        <input type="hidden" name="method_free" value="1">
        <input type="image"  id="submitButton" src="/images/continue-to-video.png" value="method_free" />
        '''
    
        video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [allmyvideos]",location ] )

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/6lgjjav5cymi
    patronvideos  = '(allmyvideos.net/[a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://"+match
        if url not in encontrados and url!="http://allmyvideos.net/embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://allmyvideos.net/6lgjjav5cymi")

    return len(video_urls)>0