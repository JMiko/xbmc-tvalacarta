# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# tester
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import re,urllib,urllib2,sys
sys.path.append ("lib")

from core import platform_name
platform_name.PLATFORM_NAME="developer"

from core import config
config.set_setting("debug","true")

from core import scrapertools
from core.item import Item
from servers import servertools

def test_one_channel(channelid):
    try:
        exec "from pelisalacarta.channels import "+channelid+" as channelmodule"
        resultado = channelmodule.test()
    except:
        import traceback
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                print line_split

        resultado = False

    return resultado

def test_channels():
    
    para_probar = []
    #para_probar.append("cineblog01")
    para_probar.append("animeflv")
    para_probar.append("animeid")
    para_probar.append("bajui")
    para_probar.append("beeg")
    para_probar.append("cinegratis")
    para_probar.append("cineonlineeu")
    para_probar.append("cinetemagay")
    para_probar.append("cinetux")
    #para_probar.append("cinevos")
    para_probar.append("cuevana")
    #para_probar.append("descargacineclasico")
    para_probar.append("descargaya")
    para_probar.append("discoverymx")
    para_probar.append("divxatope")
    para_probar.append("divxonline")
    #para_probar.append("dlmore")
    para_probar.append("documaniatv")
    para_probar.append("documentalesatonline2")
    #para_probar.append("ecarteleratrailers")
    para_probar.append("filmesonlinebr")
    para_probar.append("filmsenzalimiti")
    #para_probar.append("gaypornshare")
    para_probar.append("gnula")
    para_probar.append("internapoli")
    para_probar.append("italiafilm")
    para_probar.append("letmewatchthis")
    para_probar.append("los_simpsons_online")
    para_probar.append("mcanime")
    '''
    '''

    '''
    '''
    para_probar.append("moviezet")
    para_probar.append("newdivx")
    #para_probar.append("newhd")
    para_probar.append("peliculasonlineflv")
    para_probar.append("peliculasaudiolatino")
    para_probar.append("peliculaseroticas")
    para_probar.append("peliculasid")
    para_probar.append("peliculasyonkis_generico")
    para_probar.append("pelis24")
    para_probar.append("pelispekes")
    para_probar.append("robinfilm")
    para_probar.append("serieonline")
    para_probar.append("seriesid")
    #para_probar.append("serieshentai")
    para_probar.append("seriesdanko")
    para_probar.append("seriespepito")
    para_probar.append("seriesyonkis")
    para_probar.append("shurhd")
    para_probar.append("shurweb")
    para_probar.append("sipeliculas")
    para_probar.append("tumejortv")
    para_probar.append("tusnovelas")
    para_probar.append("unsoloclic")
    
    funcionan = []
    no_funcionan = []
    
    no_probados = []
    no_probados.append("gaypornshare")
    no_probados.append("justintv")
    no_probados.append("mocosoftx")
    no_probados.append("seriesly")
    no_probados.append("cinetube")
    no_probados.append("sonolatino")

    # Verifica los canales
    for canal in para_probar:
        resultado = test_one_channel(canal)
        if resultado:
            funcionan.append(canal)
        else:
            no_funcionan.append(canal)
    
    print "------------------------------------"
    print " funcionan: %d" % len(funcionan)
    for canal in funcionan:
        print "   %s" % canal
    print " no funcionan: %d" % len(no_funcionan)
    for canal in no_funcionan:
        print "   %s" % canal
    print " no probados: %d" % len(no_probados)
    for canal in no_probados:
        print "   %s" % canal
    

def test_one_server_connector(server,url,no_find_videos=False):
    exec "from servers import "+server+" as serverconnector"
    
    try:
        # Mira si el video existe
        if "test_video_exists" in dir(serverconnector):
            puede,motivo = serverconnector.test_video_exists(url)
        else:
            puede = True
        
        # Extrae la url
        if "get_video_url" in dir(serverconnector) and puede:
            video_urls = serverconnector.get_video_url(url)
            funciona = (puede and len(video_urls)>0)
        elif "get_long_url" in dir(serverconnector) and puede:
            video_url = serverconnector.get_long_url(url)
            funciona = True
        
    except:
        funciona = False
        import traceback
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                print line_split

    if not funciona and not no_find_videos:
        # Detecta la url usando find_videos
        detected_urls = serverconnector.find_videos(url)
        url = detected_urls[0][1]
        return test_one_server_connector(server,url,no_find_videos=True)

    return funciona

def test_server_connectors():
    funcionan = []
    no_funcionan = []
    no_probados = []
    
    para_probar = []
    para_probar.append(["twitvid","http://www.telly.com/KN995?fromtwitvid=1"])
    para_probar.append(["twitvid","http://www.telly.com/666IK?fromtwitvid=1"])
    para_probar.append(["videoweed","http://embed.videoweed.es/embed.php?v=jgos3ftj8a1zg"])
    para_probar.append(["videoweed","http://embed.videoweed.es/embed.php?v=76ev085tmn0m6"])
    para_probar.append(["nowvideo","http://www.nowvideo.eu/video/zwm0bilyhk0cl"])
    para_probar.append(["nowvideo","http://www.nowvideo.eu/video/hp8967i8oirnk"])
    para_probar.append(["novamov","http://www.novamov.com/video/tb6ira2dj029b"])
    para_probar.append(["novamov","http://www.novamov.com/video/yqesmw0th1ad9"])
    para_probar.append(["adfly","http://adf.ly/Fp6BF"])
    para_probar.append(["moevideos","http://moevideo.net/swf/letplayerflx3.swf?file=23885.2b0a98945f7aa37acd1d6a0e9713"])
    para_probar.append(["moevideos","http://www.moevideos.net/online/106249"])
    para_probar.append(["mediafire","http://www.mediafire.com/?aol88b96gm2rteb"])
    para_probar.append(["dailymotion","http://www.dailymotion.com/video/xrf96h"])
    '''
    '''
    
    '''
    para_probar.append(["videobam","http://videobam.com/FSxJO"])
    para_probar.append(["putlocker","http://www.putlocker.com/embed/CCA6C5AC98145138"])
    para_probar.append(["youtube","http://www.youtube.com/watch?v=nL-ww-XHtaY"])
    para_probar.append(["vk","http://vk.com/video_ext.php?oid=181111963&id=163409395&hash=86346c98c3176dab"])
    para_probar.append(["filebox","http://www.filebox.com/owif1u0k7ntq"])
    para_probar.append(["sockshare","http://www.sockshare.com/file/966B46C2C1150B7D"])
    para_probar.append(["allmyvideos","http://allmyvideos.net/ptatfdc3oego"])
    para_probar.append(["nosvideo","http://nosvideo.com/?v=7ir2lzpe5xf2"])
    para_probar.append(["streamcloud","http://streamcloud.eu/neuj4jw5w261"])
    para_probar.append(["movshare","http://www.movshare.net/video/tk2uynzhbbio5"])
    para_probar.append(["divxstage","http://www.divxstage.net/video/27wnoxhgtvmff"])
    '''

    # Verifica los conectores
    for server,url in para_probar:
        resultado = test_one_server_connector(server,url)
        if resultado:
            funcionan.append([server,url])
        else:
            no_funcionan.append([server,url])
    
    print "------------------------------------"
    print " funcionan: %d" % len(funcionan)
    for server,url in funcionan:
        print "   %s [%s]" % (server,url)
    print " no funcionan: %d" % len(no_funcionan)
    for server,url in no_funcionan:
        print "   %s [%s]" % (server,url)
    print " no probados: %d" % len(no_probados)
    for server,url in no_probados:
        print "   %s [%s]" % (server,url)
    

def test_cineraculo():
    data = scrapertools.cache_page("http://www.cineraculo.com/vermegavideolink.aspx")
    patron = '<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]+)" />.*?'
    patron += '<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    code1 = urllib.quote(matches[0][0]).replace("/","%2F")
    code2 = urllib.quote(matches[0][1]).replace("/","%2F")
    print code1
    print code2
    url=urllib.quote("http://www.megavideo.com/?v=GFC8JS93").replace("/","%2F")
    post = "__VIEWSTATE=%s&__EVENTVALIDATION=%s&txt_megavideo_url=%s&txt_movie_title=&btn_watch=Ver" % (code1,code2,url)
    
    data = scrapertools.cache_page("http://www.cineraculo.com/vermegavideolink.aspx", post = post , headers=[])
    print data
    patron = "unescape\('([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        print urllib.unquote(match)

def test_samba():
    from core import samba
    #print samba.file_exists("00000005.txt","smb://MEDIASERVER/DESCARGAS/XBMC/favoritos")
    #print samba.file_exists("00000004.txt","smb://MEDIASERVER/DESCARGAS/XBMC/favoritos")
    
    print samba.get_files("smb://MEDIASERVER/DESCARGAS/XBMC/favoritos")
    
    handle = samba.get_file_handle_for_reading("00000007.txt","smb://MEDIASERVER/DESCARGAS/XBMC/favoritos")
    lines = handle.readlines()
    for line in lines:
        print line
    handle.close()

    samba.remove_file("00000007.txt","smb://MEDIASERVER/DESCARGAS/XBMC/favoritos")

def test_fileserver_premium():
    url = "http://fileserve.com/index.php"
    data = scrapertools.cache_page(url)

    url = "http://fileserve.com/login.php"
    post = "loginUserName=aaaa&loginUserPassword=bbbb&autoLogin=on&ppp=102&loginFormSubmit=Login"
    data = scrapertools.cache_page(url, post=post)

    url = "http://www.fileserve.com/file/tvhFAxG"
    #scrapertools.downloadpage(url,follow_redirects=False)
    location = scrapertools.get_header_from_response(url,header_to_get="location")
    
    print "location=%s" % location

def test_filenium():
    url = "http://www.fileserve.com/file/asDbhwd"
    from servers import filenium
    video_url = filenium.get_video_url(url,premium=True,user="aaa@gmail.com",password="bbb")
    
    print video_url

def test_json():
    
    cadena = '{"480":{"2":["megaupload"]}}'
    import simplejson as json
    sources = json.loads(cadena)
    print sources
    for quality_id in sources:
        print quality_id
        languages = sources[quality_id]
        print languages
        
        for language_id in sources[quality_id]:
            print language_id
            mirrors = sources[quality_id][language_id]
            print mirrors

            for mirror in mirrors:
                print mirror

def test_videobb():
    from servers import videobb
    import base64
    import binascii

    '''
    sece2="621aa94bf809e87900e9e90799bedc281e81e2587e7bb6bb7a15f5a4ec9f0713"
    rkts="130979"
    c = videobb.decrypt32byte(sece2, int(rkts), int(base64.decodestring("MjI2NTkz")));
    print c
    #  20d90e4a60601383e7d6778ee082861d1e81e2587e7bb6bb7a15f5a4ec9f0713
    #->583b93ca1cd6adea3112c562f15460bc1e81e2587e7bb6bb7a15f5a4ec9f0713
    
    sece2="520674fa436cfe84ad275d37fd12dde91e81e2587e7bb6bb7a15f5a4ec9f0713"
    rkts="919774"
    c = videobb.decrypt32byte(sece2, int(rkts), int(base64.decodestring("MjI2NTkz")));
    print c
    #  b61f6fe75a78ca7e6c00a428bd1847eb1e81e2587e7bb6bb7a15f5a4ec9f0713
    #->edc96268979da2615d5cfdb56b569ac31e81e2587e7bb6bb7a15f5a4ec9f0713
    '''
    #videobb.get_video_url("http://videobb.com/e/itQbKhPJueqk")

def test_wupload():

    from servers import wupload
    #wupload.get_video_url("http://www.wupload.es/file/2610051647")
    wupload.get_video_url("http://www.wupload.es/file/2615687672")

def test_encode():
    url = "http://cdn.filenium.com/get/Oi8vbGV0/aXRiaXQu/bmV0L2Rv/d25sb2Fk/LzQzMzc0/LjRhOTNj/MjE1N2Y3/MmJhZDg0/NTBlZTE5/ZTkxYzcv/Q2FzdGxl/Ky0rNHgx/NystK09u/Y2UrdXBv/bithK2Ny/aW1lJTVC/Vk8uSERU/Vi5YdmlE/LUZRTSU1/RCU1Qnd3/dy5zZXJp/ZW9ubGlu/ZS5uZXQl/NUQuYXZp/Lmh0bWw_/3D/b0?user=tvalacarta%40gmail%2ecom&passwd=secreto"
    print urllib2.quote(url)
    print urllib2.quote(urllib2.quote(url))

if __name__ == "__main__":
    #test_server_connectors()
    #test_cineraculo()
    test_channels()
    #test_samba()
    #test_fileserver_premium()
    #test_filenium()
    #test_json()
    #test_wupload()
    #test_encode()
    
    #from servers import streamcloud
    #print streamcloud.get_video_url("")
    
    #from servers import divxstage
    #print divxstage.get_video_url("http://www.divxstage.eu/video/t9ed8enzrq2n3")