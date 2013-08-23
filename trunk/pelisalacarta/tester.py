# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# tester
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import re,urllib,urllib2,sys,os
sys.path.append ("lib")

from core import platform_name
platform_name.PLATFORM_NAME="developer"

from core import config
config.set_setting("debug","true")

from core import scrapertools
from core.item import Item
from servers import servertools

def test_add_documaniatv_to_download_list():
    from core import descargas
    from pelisalacarta.channels import documaniatv as channel
    mainlist_items = channel.mainlist(Item())
    mainlist_items[0].url="http://www.documaniatv.com/newvideos.html"
    pendientes = channel.novedades(mainlist_items[0])
    i = 0
    while True:

        os.remove("/Users/jesus/.developer/cookies.dat")
        try:
            # Los elementos "play" son para descargar
            if pendientes[i].action=="play":

                playitem = channel.play(pendientes[i])[0]

                title = pendientes[i].title
                url = playitem.url
                server = playitem.server
                thumbnail = pendientes[i].thumbnail
                plot = pendientes[i].plot
                fulltitle = pendientes[i].title

                print "Añadiendo "+title+", server="+server+", url="+url

                descargas.savebookmark(titulo=title,url=url,thumbnail=thumbnail,server=server,plot=plot,fulltitle=title,savepath="/Users/jesus/Downloads/documaniatv/list/")
            
            # Los elementos "novedades" son páginas
            else:
                pendientes.extend( channel.novedades(pendientes[i]) )
        except:
            pass

        i = i + 1

        if i>len(pendientes):
            break

def test_download_all_episodes():
    from pelisalacarta.channels import seriespepito as channel
    item = Item(show="Last resort", extra="episodios", url="http://last-resort.seriespepito.com/")
    from platformcode.xbmc import launcher
    launcher.download_all_episodes(item,channel,first_episode="")

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
    #test_download_all_episodes()
    test_add_documaniatv_to_download_list()
    #test_channels()

    #test_cineraculo()
    #test_samba()
    #test_fileserver_premium()
    #test_filenium()
    #test_json()
    #test_wupload()
    #test_encode()
    
    #from servers import streamcloud
    #print streamcloud.get_video_url("http://streamcloud.eu/5hfpkvjaunkg/ElSkyDVDRIP.avi.html")
    
    #from servers import divxstage
    #print divxstage.get_video_url("http://www.divxstage.eu/video/t9ed8enzrq2n3")
