# -*- coding: utf-8 -*-
import urllib2,urllib,re

from core import logger
from core import scrapertools
from core.item import Item
 
logger.info("[lasexta.py] init")

DEBUG = False
CHANNELNAME = "lasexta3"



def isGeneric():
    return True

def mainlist(item):
    logger.info("[lasexta.py] mainlist")
    itemlist = []
    getAllPrograms(1, itemlist)
    getAllPrograms(8, itemlist)
    getAllPrograms(16, itemlist)
    return itemlist

def getAllPrograms(pageNo, itemlist):
    logger.info("[lasexta.py] programs")
    ##function reload_programs(page)
    ##{
    ##     // inicializamos las variables
    ##     var url             = APP_URL+'sextatv/reload_programs';
    ##     var item_id_form     = 1;
    ##     var show_id_form     = 1;
    ##     var bd_id_form       = 1;
    ##
    ##     new Ajax.Request(url , {
    ##            method: 'post',
    ##            asynchronous: true,
    ##            encoding: 'utf-8',
    ##            parameters: {item_id  : item_id_form,
    ##                         show_id  : show_id_form,
    ##                         bd_id    : bd_id_form,
    ##                         pagina   : page,
    ##                         limit    : 3
    ##            },
    ##            onCreate: function(){
    ##
    ##                if( !$('list_programas').hasClassName('programas_listado_content_cargando') )
    ##                {
    ##                    $('list_programas').addClassName('programas_listado_content_cargando');
    ##                }
    ##
    ##        },
    ##            onSuccess: function(transport) {
    ##
    ##                var response = transport.responseText;
    ##
    ##                if( $('list_programas').hasClassName('programas_listado_content_cargando') )
    ##                {
    ##                  $('list_programas').removeClassName('programas_listado_content_cargando');
    ##                }
    ##
    ##              $('list_programas').innerHTML = response;
    ##
    ##            },
    ##            onComplete: function(transport) {
    ##                width_pagination('paginacion_programas_contenedor');
    ##                initialize();
    ##            }
    ##    });
    ##
    ##}// fin de reload

    url= 'http://www.lasexta.com/sextatv/reload_programs'
    #if the page numer is 1 ignore json request to get the first page
    if pageNo > 1:
            params = urllib.urlencode({"item_id": 1, "show_id": 1, "bd_id": 1 , "pagina": pageNo, "limit": 1 })
            req = urllib2.Request(url, params)
    else:
            req = urllib2.Request(url)

    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Content-type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    


    ##        	<div class="capaseccionl item_vip">

    ##	    	    <div class="player">

    ##	        	    <a href="http://www.lasexta.com/sextatv/mujeresricas">

    ##						<img src="http://www.lasexta.com/media/sextatv/img/sextatv_logo_mujeres_ricas.jpg" width="230" height="129" title="VÃ­deos de Mujeres Ricas" alt="Logotipo de Mujeres Ricas" />

    ##						<label class="item_vip_player_label">Mujeres Ricas</label>

    ##						<img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" class="item_vip_player_link" alt="Ir a videos de Mujeres Ricas"/>

    ##					</a>

    ##	            </div>

    ##	        </div>



    patron  = '<div class="player">[^<]+'
    patron += '<a href="(.+?)">[^<]+'
    patron += '<img src="(.+?)" width="230" height="129" title="(.+?)" alt="(.+?)" />[^<]+'
    patron += '<label class="item_vip_player_label">(.+?)</label>[^<]+'

    matches = re.compile(patron,re.DOTALL).findall(page)
            #if DEBUG: scrapertools.printMatches(matches)
    #print matches

    for match in matches:
                    scrapedtitle = urllib.unquote_plus(match[4])
                    scrapedurl = match[0]
                    scrapedthumbnail = match[1] 
                    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                    
                    # Añade al listado
                    itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getProgramsCategories" , url=scrapedurl, thumbnail=scrapedthumbnail , folder=True) )

    return itemlist

def getProgramsCategories(item):
    url = item.url
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()    
    #javascript:change_videos('4','programasCompletos');
    patron  = "href=\"javascript:change_videos\('(.+?)','(.+?)'\);[^<]+"
    matches = re.compile(patron,re.DOTALL).findall(page)
    itemlist = []
    print matches
    for match in matches:
                    programId = match[0]
                    title = match[1]
                    
                    if (DEBUG): logger.info("programId=["+programId+"], title=["+title+"]")
                    #HACK putting in extra as custom programId gets overwritten
                    
                    item = Item(channel=CHANNELNAME, title=title , extra=programId, action="getProgramCagetoryVideos", folder=True)
                    if item.title == 'programasCompletos':
                    # Añade al listado only programas completos
                        itemlist.append(item)
                        print item.tostring()
                    
    return itemlist

def getProgramCagetoryVideos(item):
    url = "http://www.lasexta.com/sextatv/change_videos/" + item.extra + "/" + item.title
    req = urllib2.Request(url)

    #Quick workaround we can use the ajax request to get all videos
##    function reload(valor)
##6{
##7
##8 if(valor)
##9 {
##10 // inicializamos las variables
##11 var url = APP_URL+'sextatv/reload';
##12 var section = false;
##13 var type = false;
##14 var page = 0;
##15 var section_id = false;
##16
##17 if(temp = valor.split('_'))
##18 {
##19
##20 if(temp[0]){ var section = temp[0];}
##21 if(temp[1]){ var type = temp[1];}
##22 if(temp[2]){ var page = temp[2];}
##23 if(temp[2]){ var section_id = temp[3];}
##24
##25 new Ajax.Request(url , {
##26 method: 'post',
##27 asynchronous: true,
##28 encoding: 'utf-8',
##29 parameters: {seccion: section, pagina: page, tipo:type, section_id:section_id },
##30 onCreate: function(){
##31
##32 if( !$('contenedor_videos').hasClassName('lsv_listado_videos_cargando') )
##33 {
##34 $('contenedor_videos').addClassName('lsv_listado_videos_cargando');
##35 }
##36
##37 },
##38 onSuccess: function(transport) {
##39
##40 var response = transport.responseText;
##41
##42 if( $('contenedor_videos').hasClassName('lsv_listado_videos_cargando') )
##43 {
##44 $('contenedor_videos').removeClassName('lsv_listado_videos_cargando');
##45 }
##46
##47 $('contenedor_videos').innerHTML = response;
##48
##49 },
##50 onComplete: function(transport) {
##51 width_pagination('paginacion_normal_contenedor');
##52 }
##53 });
##54
##55 }// fin del split
##56
##57 }
##58
##59}// fin de reload
##60 

    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
##     <div class="player_programas">
##			            <a href="http://www.lasexta.com/sextatv/supercasas/completos/supercasas__domingo__23_de_enero/358061/1"><img src="http://www.sitios.lasexta.com/pictures/239201/pictures_20110120_2106239201_crop1.jpg" width="170" height="127" title="supercasas__domingo__23_de_enero" alt="supercasas__domingo__23_de_enero" /></a>
##			            <a href="http://www.lasexta.com/sextatv/supercasas/completos/supercasas__domingo__23_de_enero/358061/1" class="item_cortina">
##							<img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" width="170" height="127" title="supercasas__domingo__23_de_enero" alt="supercasas__domingo__23_de_enero" />
##							<label class="item_cortina_text">Un programa de SUPERCASAS dedicado a futbolistas. En este capítulo se mostrará la impresionante casa&#8230;</label>
##							<label class="item_cortina_play">PLAY</label>
##						</a>
##
##			            			        </div>
##			        <h6 class="fecha">24/01/2011 </h6>
##			        <h5 class="titulo"><a href="http://www.lasexta.com/sextatv/supercasas/completos/supercasas__domingo__23_de_enero/358061/1" title="supercasas__domingo__23_de_enero">Supercasas. Domingo, 23 de enero</a></h5>
##			        			    </div>


    
    #patron  = '<div class="player_programas">[^<]+'
    #patron += '<a href=".+?"><img src="(.+?)" width="170" height="127" title=".+?" alt=".+?" /></a>.*?'
    patron = '<h5 class="titulo"><a href="(.+?)" title=".+?">(.+?)</a></h5>[^<]'
    matches = re.compile(patron,re.DOTALL).findall(page)
    itemlist = []
    print matches
    for match in matches:
                    scrapedtitle = match[1]
                    scrapedurl = match[0]
                    scrapedthumbnail = '' 
                    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                    
                    # Añade al listado
                    itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getVideos" , url=scrapedurl, thumbnail=scrapedthumbnail , folder=True) )

    return itemlist

def getVideos(item):
    urlGeneral = item.url
    print urlGeneral
  
    #http://www.lasexta.com/sextatv/seloquehicisteis/completos/se_lo_que_hicisteis____viernes__4_de_febrero/366561/1
    patron = 'http://www.lasexta.com/sextatv/.+?/.+?/.+?/(.+?)/1'
    matchedIds = re.compile(patron,re.DOTALL).findall(urlGeneral)
    itemlist = []
    count = 0
    for matchId in matchedIds:
        videoId = matchId
        videosUrl = 'http://www.lasexta.com/sextatv/playlist/' + videoId
        print videosUrl
        req = urllib2.Request(videosUrl)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        page = response.read()
        response.close()

##        	<video>
##				<id>357881</id>
##				<title>1 FLV 23 enero</title>
##				<description><![CDATA[]]></description>
##				<url>6a77ec0772d81456186cf91ab66e3384c993462e934320aa89a44a5b7eb636bde26211e0e96a9709b1809864c83da59ee90669280e2999643efca0377eb7eaf60807ad12a89a209d5e9a9b82535db4f8ca95a04e02989ca9547fee742735dda33c5bfad3583e7f629c6db861828e503f87b308</url>
##				<urlHD>http://lasexta.edgeboss.net/flash/lasexta/supercasas/hd/ppd0001564000601_supercasas_6_23_01_2011_23_19_57_h264.mp4</urlHD>
##			</video>
        
        patron = '<urlHD>(.+?)</urlHD>[^<]'
        matchedVideoParts = re.compile(patron,re.DOTALL).findall(page)
        
        for matchVideoPart in matchedVideoParts:
            count = count + 1
            scrapedtitle = "Part " + str(count)
            scrapedVideoUrl = matchVideoPart
           
            scrapedthumbnail = item.thumbnail
            scrapedplot = ''

            req = urllib2.Request(scrapedVideoUrl)
            req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            page = response.read()
            
            response.close()
##            <FLVPlayerConfig>
##  <serverName>cp61776.edgefcs.net</serverName>
##  <fallbackServerName>cp61776.edgefcs.net</fallbackServerName>
##  <appName>ondemand</appName>
##  <streamName>mp4:flash/supercasas/hd/.uid.MVHxAABEEE97k1ZrBw7c64b8c2bb7e83b937ce470f33f64c08.ppd0001564000601_supercasas_6_23_01_2011_23_19_57_h264.mp4</streamName>
##  <isLive>false</isLive>
##  <bufferTime>2</bufferTime>
##</FLVPlayerConfig>

            patron = '<serverName>([^<]+)</serverName>[^<]+'
            patron += '<fallbackServerName>([^<]+)</fallbackServerName>[^<]+'
            patron += '<appName><!\[CDATA\[(.+?)]]></appName>[^<]+'
            patron +='<streamName><!\[CDATA\[(.+?)]]></streamName>[^<]'
            matches = re.compile(patron,re.DOTALL).findall(page)
            for match in matches:
                serverName = match[0]
                
                appName = match[2]
                streamName = match[3]
                scrapedUrl = 'rtmp://' + serverName + '/' + appName + '/' + streamName
                # Añade al listado
                itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play", server="Directo" , url=scrapedUrl, thumbnail=scrapedthumbnail, plot=scrapedplot) )
    return itemlist 
