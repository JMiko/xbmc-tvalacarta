# -*- coding: utf-8 -*-
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

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Lee la URL
    data = scrapertools.cache_page( page_url )
    bloque = scrapertools.get_match(data,'<Form method="POST"(.*)</.orm>')
    logger.info("bloque="+bloque)
    op = scrapertools.get_match(bloque,'<input type="hidden" name="op" value="([^"]+)"')
    usr_login = scrapertools.get_match(bloque,'<input type="hidden" name="usr_login" value="([^"]*)"')
    id = scrapertools.get_match(bloque,'<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(bloque,'<input type="hidden" name="fname" value="([^"]+)"')
    referer = scrapertools.get_match(bloque,'<input type="hidden" name="referer" value="([^"]*)"')
    method_free = scrapertools.get_match(bloque,'<input type="[^"]+" name="method_free" value="([^"]+)"')

    # Simula el botón
    #op=download1&usr_login=&id=buq4b8zunbm6&fname=Snow.Buddies-Avventura.In.Alaska.2008.iTALiAN.AC3.DVDRip.H264-PsYcOcReW.avi&referer=&method_free=Watch+Free%21
    post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free
    data = scrapertools.cache_page( page_url , post=post )
    logger.info("data="+data)
    
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
    location = scrapertools.get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"
    logger.info("location="+location)
    
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [allmyvideos]",location ] )

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/fg85ovidfwxx
    patronvideos  = '(allmyvideos.net/[a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
