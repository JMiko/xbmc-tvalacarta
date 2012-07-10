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
    '''
    '''
    
    para_probar.append("animeflv")
    para_probar.append("animeid")
    para_probar.append("bajui")
    para_probar.append("beeg")
    para_probar.append("cineblog01")
    para_probar.append("cinetemagay")
    para_probar.append("cuevana")
    para_probar.append("cinevos")
    para_probar.append("discoverymx")
    para_probar.append("divxonline")
    para_probar.append("documaniatv")
    para_probar.append("documentariestv")
    para_probar.append("filmsenzalimiti")
    para_probar.append("gnula")
    para_probar.append("internapoli")
    para_probar.append("italiafilm")
    para_probar.append("documentalesatonline2")
    para_probar.append("letmewatchthis")
    para_probar.append("los_simpsons_online")
    para_probar.append("mcanime")
    para_probar.append("moviezet")
    para_probar.append("newdivx")
    para_probar.append("newhd")
    para_probar.append("peliculasonlineflv")
    para_probar.append("peliculasaudiolatino")
    para_probar.append("peliculaseroticas")
    para_probar.append("peliculasflv")
    para_probar.append("peliculasid")
    para_probar.append("peliculasyonkis_generico")
    para_probar.append("pelis24")
    para_probar.append("pelispekes")
    para_probar.append("robinfilm")
    para_probar.append("serieonline")
    para_probar.append("seriesid")
    para_probar.append("serieshentai")
    para_probar.append("seriesdanko")
    para_probar.append("seriespepito")
    para_probar.append("seriesyonkis")
    para_probar.append("shurhd")
    para_probar.append("shurweb")
    para_probar.append("sipeliculas")
    para_probar.append("tubutakadecine")
    para_probar.append("tumejortv")
    para_probar.append("filmesonlinebr")
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
    

def test_server_connectors():
    from servers import adnstream
    from servers import bliptv
    from servers import facebook
    from servers import fourshared
    from servers import gigabyteupload
    from servers import megaupload
    from servers import megavideo
    from servers import movshare
    from servers import stagevu
    from servers import tutv
    from servers import userporn
    from servers import veoh
    from servers import videobb
    from servers import videoweed
    from servers import videozer
    from servers import vidxden
    from servers import vimeo
    from servers import vk
    from servers import yahoo
    from servers import youtube

    # Comprueba que el conector funciona
    #adnstream.get_video_url("zisLliNceS")
    #bliptv.get_video_url("http://blip.tv/play/h45Xgs23eQI.html")    
    #vidxden.get_video_url("http://www.vidxden.com/3360qika02mo/whale.wars.s04e10.hdtv.xvid-momentum.avi.html")    
    #videobb.get_video_url("http://videobb.com/video/QEmaAV4W6PF5")    
    #videozer.get_video_url("http://www.videozer.com/video/FuxQQP")
    #videozer.get_video_url("http://videozer.com/embed/VojJbb")
    #fourshared.get_video_url("http://www.4shared.com/embed/392975628/ff297d3f")
    #gigabyteupload.get_video_url("http://www.gigabyteupload.com/download-0f1142b188b0866b")
    #movshare.get_video_url("http://www.movshare.net/video/066km1u5mwvec")
    #stagevu.get_video_url("http://stagevu.com/video/lgnxzviiiarc")
    #tutv.get_video_url("http://tu.tv/videos/avatar-1x19-el-asedio-del-norte-i")
    #tutv.get_video_url("http://tu.tv/tutv.swf?skin=skins/skin&xtp=18726")
    #userporn.get_video_url("http://www.userporn.com/e/1gMOyqXd4Ld0")
    #veoh.get_video_url("v21212001qyZAhXyp")
    #videoweed.get_video_url("http://www.videoweed.es/file/yk6r8czj7gsk6")
    #vimeo.get_video_url("http://vimeo.com/27307766")
    #vk.get_video_url("http://vk.com/video_ext.php?oid=108221761&id=160708641&hash=489fb82ac0d63aa0&hd=1")
    #yahoo.get_video_url("http://es.video.yahoo.com/juegos-1305738/ps3-4750064/ridge-racer-unbounded-gamescom-26319245.html")
    youtube.get_video_url("http://www.youtube.com/watch?v=zlZgGlwBgro&feature=fvhl")
    
    # Comprueba que find_videos funciona
    #data = scrapertools.cache_page("http://www.tvshows4all.com/whale-wars-season-4-episode-10-delivering-the-final-blow/")
    #print videoweed.find_videos(data)

    # Tiene videobb, videozer y vk en 2 calidades
    #data = scrapertools.cache_page("http://www.newdivx.net/peliculas-online/animacion/2402-los-pitufos-2011.html")
    #print videobb.find_videos(data) 
    #print videozer.find_videos(data)
    #print vk.find_videos(data) 

    # Megavideo en formato ?d
    #from core import config
    #data = scrapertools.cache_page("http://house.seriespepito.com/capitulos-primera-temporada-1/capitulo-12-medicina-deportiva/")
    #data = scrapertools.cache_page("http://star-wars-the-clone-wars.seriespepito.com/capitulos-tercera-temporada-3/capitulo-3/")
    #data = scrapertools.cache_page("http://star-wars-the-clone-wars.seriespepito.com/capitulos-tercera-temporada-3/capitulo-8/")
    #videos = megavideo.find_videos(data)
    #data = scrapertools.cache_page("http://www.seriesdanko.com/2010/06/eureka-4x18-capitulo-18.html")
    
    # Vuelca todos los vídeos que encuentra
    #video_urls = megavideo.get_video_url("http://www.megavideo.com/?d=UDHMBYAQ",True,"","")
    #video_urls = megaupload.get_video_url("http://www.megaupload.com/?d=S2Q8NWDM",True,"","")
    #for video_url in video_urls:
    #    print video_url
    '''
    videos_encontrados = []
    videos = servertools.findvideos(data)
    for video in videos:
        server = video[2]
        exec "from servers import %s as serverconnector" % server
        video_urls = serverconnector.get_video_url( video[1] , premium = False)
        for video_url in video_urls:
            videos_encontrados.append( [server,video_url[0],video_url[1]])
    
    for entrada in videos_encontrados:
        print entrada
    '''

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