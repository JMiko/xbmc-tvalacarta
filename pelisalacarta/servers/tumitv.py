# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para tumi.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import urllib

from core import scrapertools
from core import logger

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("pelisalacarta.tumitv get_video_url(page_url='%s')" % page_url)

    video_urls = []

    data = scrapertools.cache_page(page_url)

    '''
    <script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('2("1u").1t({q:"5://k.j.h.4:g/p/v.o",n:"5",1s:"5://k.j.h.4:g/i/1r/1q/1p.1o",1n:"1m",1l:1k,1j:1i,1h:\'16:9\',1g:\'1f\',1e:\'s\',1d:[{f:"s",1c:"5://1b.1a/r/r.19"},{f:"18",17:{q:\'5://k.j.h.4:g/p/v.o\',\'n\':\'5\'}},{f:"15"}]});e 7;e d=0;e 3=0;2().14(6(x){8(3>0)d+=x.m-3;3=x.m;8(0!=0&&d>=0){3=-1;2().13();2().12(11);$(\'#10\').c();$(\'b.a\').c()}});2().z(6(x){3=-1});2().y(6(x){l(x)});2().w(6(){$(\'b.a\').c()});6 l(x){$(\'b.a\').u();8(7)t;7=1;}',36,67,'||jwplayer|p075075||http|function|vvplay|if||video_ad|div|show|tt75075|var|type|8777|38||95|209|doPlay|position|provider|flv|3gbut4vo4ifgthgl45cpgfpwpbfpvomsgptxiiypbnju3mgg6vp5tkf57ska|file|player|flash|return|hide||onComplete||onPlay|onSeek|play_limit_box|false|setFullscreen|stop|onTime|download||config|html5|swf|tv|tumi|src|modes|primary|glow|skin|aspectratio|540|height|980|width|3139|duration|jpg|4i1v6wcudvog|00015|01|image|setup|vplayer'.split('|')))
    </script>
    #<script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('2("1u").1t({p:"4://j.h.g.12:f/o/v.n",m:"4",1s:"4://j.h.g.12:f/i/1r/1q/1p.1o",1n:"1m",1l:1k,1j:1i,1h:\'16:9\',1g:\'1f\',1e:\'r\',1d:[{e:"r",1c:"4://1b.1a/q/q.19"},{e:"18",17:{p:\'4://j.h.g.12:f/o/v.n\',\'m\':\'4\'}},{e:"15"}]});d 6;d c=0;d 3=0;2().14(5(x){7(3>0)c+=x.l-3;3=x.l;7(0!=0&&c>=0){3=-1;2().13();2().11(10);$(\'#z\').b();$(\'a.8\').b()}});2().y(5(x){3=-1});2().w(5(x){k(x)});2().u(5(){$(\'a.8\').b()});5 k(x){$(\'a.8\').t();7(6)s;6=1;}',36,67,'||jwplayer|p071971|http|function|vvplay|if|video_ad||div|show|tt71971|var|type|8777|35|95||209|doPlay|position|provider|flv|3wbuteus4ifgthgl45c7gfnghulkbodggmc32yruoallmdif2ctjaalh4ghq|file|player|flash|return|hide|onComplete||onPlay||onSeek|play_limit_box|false|setFullscreen||stop|onTime|download||config|html5|swf|tv|tumi|src|modes|primary|glow|skin|aspectratio|540|height|980|width|2621|duration|jpg|49tbnwiplgjh|00014|01|image|setup|vplayer'.split('|')))
                                            #</script>

    '''

    patron = 'eval\(function\(p,a,c,k,e,d\)(.*?)split'
    jsScript = scrapertools.find_single_match( data , patron)

    #('2("1u").1t({q:"5://k.j.h.4:g/p/v.o
    patron = '\(' + "'" + '2\("1u"\).1t\({.:".*?://([^"]+)",'
    ipMask = scrapertools.find_single_match( jsScript, patron)
    ipMask = 'http://'+re.sub('[a-q]', '%s', ipMask)

    #|type|8777|35|95||209|doPlay|position|provider|flv|3wbuteus4ifgthgl45c7gfnghulkbodggmc32yruoallmdif2ctoqddh4ghq|file|player|flash
    #|type|8777|35|95||209|doPlay|position|provider|flv|3wbuteus4ifgthgl45c7gfnghulkbodggmc32yruoallmdif2ctpkdlh4ghq|file|player|flash|r
    #|type|8777|38||95|209|doPlay|position|provider|flv|3gbut4vo4ifgthgl45cpgfpwpbfpvomsgptxiiypbnju3mgg6vp5tkf57ska|file|
    #patron = '|type|([^|]+)|([^|]+)|([^|]+)|([^|]+)|([^|]+)|doPlay|position|provider|([^|]+)|([^|]+)|file|'.replace('|','\|')

    patron = 'type(.*?)file'
    matches = re.compile(patron,re.DOTALL).findall(jsScript)
    matches = matches[0].split('|')

    port = matches[1]
    ip4 = matches[2]
    ip3 = matches[3]
    ip2 = matches[4]
    ip1 = matches[5]
    ext = matches[9]
    path = matches[10]

    url = ipMask %(ip1,ip2+ip3,ip4,port,path,ext)
    video_url = ["flv [tumi.tv]", url ]
    video_urls.append( video_url )

    for video_url in video_urls:
        logger.info("pelisalacarta.tumitv %s - %s" % (video_url[0],video_url[1]))



    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.tumi.tv/rzy0xuus6esv
    patronvideos  = 'tumi.tv/([a-z0-9]+)'
    logger.info("pelisalacarta.tumitv find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[tumi.tv]"
        if match!="iframe":
            #url = "http://www.tumi.tv/iframe-"+match+"-600x400.html"
            url = "http://www.tumi.tv/embed-"+match+".html"
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'tumitv' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://www.tumi.tv/iframe-rzy0xuus6esv-600x400.html
    patronvideos  = 'tumi.tv/iframe-([a-z0-9]+)'
    logger.info("pelisalacarta.tumitv find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[tumi.tv]"
        #url = "http://www.tumi.tv/iframe-"+match+"-600x400.html"
        url = "http://www.tumi.tv/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tumitv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve