# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Android One
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "android1"
__type__ = "generic"
__title__ = "Android One"
__language__ = "ES"

DEBUG = config.get_setting("debug")
LOCAL_FILE = os.path.join( config.get_data_path() , "android1.json" )

def isGeneric():
    return True

def mainlist(item,data=""):
    logger.info("mywebtv.channels.android1.mainlist")
    itemlist = []

    recursividad_permitida = False
    if data=="":
        recursividad_permitida = True
        request_headers = []
        request_headers.append(["Content-Type","application/x-www-form-urlencoded"])
        request_headers.append(["Content-Length","55"])
        post = "SELECT nombre, link, icono FROM canales order by nombre"
        data = scrapertools.cache_page("http://www.jaserdevelopments.com/tdtdirectotvics/canales/conexion2.php" , headers = request_headers, post=post)
        #logger.info("body="+body)

    try:
        json_object = scrapertools.load_json(data)

        for entry in json_object:
            #logger.info("entry="+str(entry))
            #{u'nombre': 'Tv Bilbao', u'icono': 'http://www.jaserdevelopments.com/images/channels/tvbilbaon.png', u'link': 'rtmp://149.11.34.6/live/telebilbao.stream'}
            itemlist.append( Item( channel=__channel__ , action="play" , title=entry['nombre'] , url=entry['link'], thumbnail=entry['icono'], folder=False))
    except:
        itemlist = []

    # Si ha encontrado canales, graba el fichero actualizado por si en el futuro falla
    if len(itemlist)>0:
        f = open(LOCAL_FILE,"w")
        f.write(data)
        f.flush()
        f.close()

    # Si no ha encontrado canales, lee el fichero grabado la última vez y carga de nuevo la lista
    elif recursividad_permitida:
        infile = open(LOCAL_FILE,"r")
        data = infile.read()
        infile.close()
        itemlist = mainlist(item,data)

    '''
    POST /tdtdirectotvics/canales/conexion2.php HTTP/1.1
    Content-Length: 55
    Content-Type: application/x-www-form-urlencoded
    Host: www.jaserdevelopments.com
    Connection: Keep-Alive

    SELECT nombre, link, icono FROM canales order by nombreHTTP/1.1 200 OK
    Date: Mon, 24 Jun 2013 15:19:12 GMT
    Server: Apache
    X-Powered-By: PHP/5.2.17
    Connection: close
    Transfer-Encoding: chunked
    Content-Type: text/html

    2720
    [{"nombre":"13 Tv","link":"rtmp:\/\/xiiitvlivefs.fplive.net\/xiiitvlive-live\/stream13tv","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/13tvn.png"},{"nombre":"Andalucia Tv","link":"http:\/\/195.10.10.220\/rtva\/andaluciatelevisionh264.flv","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/andaluciatvn.png"},{"nombre":"Andorra TV","link":"mms:\/\/194.158.91.91\/Atv","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/andorratvn.png"},{"nombre":"Antena 3","link":"rtmp:\/\/antena3fms35livefs.fplive.net:1935\/antena3fms35live-live\/stream-antena3","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/antena3n.png"},{"nombre":"Antena 3 link2","link":"http:\/\/antena3-aos1-apple-live.adaptive.level3.net\/apple\/antena3\/channel01\/index.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/antena3n.png"},{"nombre":"Aragon Tv","link":"rtmp:\/\/aragontvlivefs.fplive.net\/aragontvlive-live\/stream_normal_abt","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/aragontvn.png"},{"nombre":"Astro Canal","link":"rtsp:\/\/flash3.todostreaming.es\/telelinea1\/mystream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/astrocanaln.png"},{"nombre":"Canal 24h Tve","link":"http:\/\/iphonelive.rtve.es\/24H_LV3_IPH\/24H_LV3_IPH.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/canal24tven.png"},{"nombre":"Canal Diocesano","link":"rtmp:\/\/flash3.todostreaming.es\/edesco\/livestream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/canaldiocesanon.png"},{"nombre":"Canal Sur","link":"http:\/\/iphone-andaluciatelevision.rtva.stream.flumotion.com\/rtva\/andaluciatelevision-iphone-multi\/main.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/canalsurn.png"},{"nombre":"Canal Vasco","link":"rtmp:\/\/cp70268.live.edgefcs.net\/live\/eitb-CanalVasco@5519","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/canalvascon.png"},{"nombre":"Cuatro","link":"http:\/\/telecinco-channel6-nogeo.hls.adaptive.level3.net\/telecinco\/channel6-nogeo\/esmediaset12\/bitrate_1.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/cuatron.png"},{"nombre":"Cuatro link2","link":"rtmp:\/\/173.192.200.116\/live\/7377772747?id=32553","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/cuatron.png"},{"nombre":"Deluxe Music","link":"http:\/\/flash.cdn.deluxemusic.tv\/deluxemusic.tv-live\/web_850.stream\/playlist.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/deluxemn.png"},{"nombre":"Divinity","link":"http:\/\/telecinco-channel9.hls.adaptive.level3.net\/telecinco\/channel9\/esmediaset31\/esmediaset31.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/divinityn.png"},{"nombre":"Esport 3","link":"rtmp:\/\/tv-geoespanya-flashlivefs.fplive.net:1935\/tv-geoespanya-flashlive-live?ovpfv=1.1\/stream_ES_ES3_FLV","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/esport3n.png"},{"nombre":"etb Sat","link":"rtmp:\/\/cp70268.live.edgefcs.net\/live\/eitb-ETBSat@5219","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/etbsatn.png"},{"nombre":"Extremadura Tv","link":"http:\/\/iphonelive.canalextremadura.es\/tv\/tv.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/extremaduratvn.png"},{"nombre":"Gran Hermano","link":"http:\/\/telecinco-channel10.hls.adaptive.level3.net\/telecinco\/channel10\/esmediaset32\/esmediaset32.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/granhermanon.png"},{"nombre":"Hogar Util","link":"http:\/\/hogarutilhdflash-lh.akamaihd.net\/Hogarutil_flash_500@101082?apid=428885&v=2.8.0&fp=WIN 11,5,502,135&r=BLPMW&g=PKUHGJFSWWOS","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/hogarutiln.png"},{"nombre":"Huesca Tv","link":"rtmp:\/\/streaming2.radiohuesca.com\/live\/huescatv","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/huescatvn.png"},{"nombre":"IB3","link":"http:\/\/ibsatiphone.ib3tv.com\/iphoneliveIB3\/IB3\/IB3.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/ib3n.png"},{"nombre":"Intereconomia","link":"rtmp:\/\/media.intereconomia.com\/live\/intereconomiatv1","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/intereconomian.png"},{"nombre":"Intereconomia Bussines","link":"rtmp:\/\/media.intereconomia.com\/live\/business2","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/interbussinesn.png"},{"nombre":"Intereconomia HD","link":"rtmp:\/\/media.intereconomia.com\/live\/intereconomiatv2","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/intereconomian.png"},{"nombre":"Kiss Tv","link":"http:\/\/kisstelevision.es.flash3.glb.ipercast.net\/kisstelevision.es-live\/mp4:live\/playlist.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/kisstvn.png"},{"nombre":"La 1","link":"http:\/\/iphonelive.rtve.es\/LA1_LV3_IPH\/LA1_LV3_IPH.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/la1n.png"},{"nombre":"La 2","link":"http:\/\/iphonelive.rtve.es\/LA2_LV3_IPH\/LA2_LV3_IPH.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/la2n.png"},{"nombre":"la Sexta","link":"rtmp:\/\/antena3fms35livefs.fplive.net:1935\/antena3fms35live-live\/stream-lasexta","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/lasextan.png"},{"nombre":"la Sexta link2","link":"http:\/\/antena3-aos1-apple-live.adaptive.level3.net\/apple\/antena3\/channel02\/index.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/lasextan.png"},{"nombre":"Libertad Digital","link":"http:\/\/149.11.34.6:1935\/live\/ldtv.stream\/playlist.m3u8?wowzasessionid=348498751","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/libertaddigitaln.png"},{"nombre":"Marca Tv","link":"http:\/\/universalhdlive.marca.com\/i\/dr21_1@100203\/index_4_av-b.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/marcatvn.png"},{"nombre":"Nou 24h","link":"http:\/\/rtvv.stream.flumotion.com\/rtvv\/main.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/nou24hn.png"},{"nombre":"OndaJerez Tv","link":"mmsh:\/\/w2k8video.jesytel.com\/ondajereztv?MSWMExt=.asf","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/ondajereztvn.png"},{"nombre":"RT","link":"rtmp:\/\/rt.fms.visionip.tv\/live?autostart=true\/RT_Spanish_3","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/rtn.png"},{"nombre":"RTPA","link":"http:\/\/iphone.rtpa.stream.flumotion.com\/rtpa\/tv-iphone\/main.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/rtpan.png"},{"nombre":"RTV Canaria net","link":"rtsp:\/\/streamrtvc.mad.idec.net\/rtvc1\/rtvc_1.sdp","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/rtvcanarianetn.png"},{"nombre":"RTVida","link":"rtsp:\/\/flash3.todostreaming.es\/radiovida\/mobile","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/rtvidan.png"},{"nombre":"Sevilla FC Tv","link":"http:\/\/www1.c80137.dna.qbrick.com\/80137\/live\/sfc\/sfc_iphone.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/sevillafctvn.png"},{"nombre":"Solidaria Tv","link":"rtsp:\/\/flash3.todostreaming.es\/solidariatv\/mystream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/solidariatvn.png"},{"nombre":"STV Rioja","link":"mms:\/\/www.riojasintonia.com\/stv","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/stvriojan.png"},{"nombre":"Super 3","link":"rtmp:\/\/tv-geoespanya-flashlivefs.fplive.net:1935\/tv-geoespanya-flashlive-live?ovpfv=1.1\/stream_ES_33D_FLV","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/super3n.png"},{"nombre":"Teleasturias","link":"rtmp:\/\/149.11.34.6\/live\/teleasturias.stream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/teleasturiasn.png"},{"nombre":"Telecinco","link":"http:\/\/telecinco-channel5-nogeo.hls.adaptive.level3.net\/telecinco\/channel5-nogeo\/esmediaset11\/esmediaset11.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/telecincon.png"},{"nombre":"Teledeporte","link":"http:\/\/iphonelive.rtve.es\/TDP_LV3_IPH\/TDP_LV3_IPH.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/teledeporten.png"},{"nombre":"TeleMadrid","link":"http:\/\/iphone.telemadrid.es.edgesuite.net\/telemadridsat_iphone.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/telemadridn.png"},{"nombre":"Tv Bilbao","link":"rtmp:\/\/149.11.34.6\/live\/telebilbao.stream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tvbilbaon.png"},{"nombre":"Tv Galicia","link":"http:\/\/media3.crtvg.es\/live\/tvge\/playlist.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tvgalician.png"},{"nombre":"Tv Galicia America","link":"http:\/\/media3.crtvg.es\/live\/tvga\/playlist.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tvgaliciaamerican.png"},{"nombre":"Tv Huelva","link":"rtmp:\/\/flash3.todostreaming.es\/huelvatv\/livestream","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tvhuelvan.png"},{"nombre":"Tv3","link":"rtmp:\/\/tv-geoespanya-flashlivefs.fplive.net:1935\/tv-geoespanya-flashlive-live?ovpfv=1.1\/stream_ES_TV3_FLV","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tv3n.png"},{"nombre":"Tv3 CAT","link":"http:\/\/www.tv3.cat\/directetv3cat\/tv3cat.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tv3catn.png"},{"nombre":"tvA","link":"http:\/\/195.219.98.243\/livetva\/Tva\/playlist.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/tvan.png"},{"nombre":"Xplora","link":"rtmp:\/\/antena3fms35geobloqueolivefs.fplive.net:1935\/antena3fms35geobloqueolive-live\/stream-xplora","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/xploran.png"},{"nombre":"Xplora link2","link":"http:\/\/antena3-aos1-apple-live.adaptive.level3.net\/apple\/antena3\/channel03\/index.m3u8","icono":"http:\/\/www.jaserdevelopments.com\/images\/channels\/xploran.png"}]
    0
    '''
    return itemlist
