# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# tester
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import re,urllib,urllib2,sys
from core import scrapertools
from core.item import Item
from servers import servertools

def test_channels():
    
    funcionan = []
    no_funcionan = []
    no_probados = []
    
    #animeforos - xbmc only
    no_probados.append("animeforos")

    # animeid
    try:
        from pelisalacarta.channels import animeid
        itemlist = animeid.mainlist(Item())
        itemlist = animeid.destacados(itemlist[0])  # Destacados -> lista de series
        itemlist = animeid.serie(itemlist[0])  # Primera serie destacada -> lista de episodios
        itemlist = servertools.find_video_items(itemlist[0]) # Primer episodios -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("animeid")
    else: no_funcionan.append("animeid")

    # asiateam
    no_probados.append("asiateam")

    # buenaisla
    try:
        from pelisalacarta.channels import buenaisla
        itemlist = buenaisla.mainlist(Item())    
        itemlist = buenaisla.novedades(itemlist[0])  # Novedades -> lista de episodios
        itemlist = buenaisla.videos(itemlist[0])
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("buenaisla")
    else: no_funcionan.append("buenaisla")

    # casttv
    no_probados.append("casttv")
    
    # cineadicto
    try:
        from pelisalacarta.channels import cineadicto
        itemlist = cineadicto.mainlist(Item())    
        itemlist = cineadicto.listvideos(itemlist[0])  # Novedades -> lista de episodios
        itemlist = cineadicto.detail(itemlist[4])
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("cineadicto")
    else: no_funcionan.append("cineadicto")
    
    # cineblog01
    try:
        from pelisalacarta.channels import cineblog01
        itemlist = cineblog01.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = cineblog01."+itemlist[0].action+"(itemlist[0])"  # Novedades -> lista de pelis
        itemlist = servertools.find_video_items(itemlist[0]) # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("cineblog01")
    else: no_funcionan.append("cineblog01")

    # cinegratis
    try:
        from pelisalacarta.channels import cinegratis
        itemlist = cinegratis.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = cinegratis."+itemlist[0].action+"(itemlist[0])"  # Novedades -> lista de pelis
        itemlist = servertools.find_video_items(itemlist[0]) # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("cinetube")
    else: no_funcionan.append("cinetube")

    # cinetube
    try:
        from pelisalacarta.channels import cinetube
        itemlist = cinetube.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = cinetube.peliculas(itemlist[0],paginacion=True)"  # Novedades -> lista de pelis
        exec "itemlist = cinetube."+itemlist[0].action+"(itemlist[0])"  ## Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("cinetube")
    else: no_funcionan.append("cinetube")

    # cuevana
    try:
        from pelisalacarta.channels import cuevana
        itemlist = cuevana.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = cuevana."+itemlist[0].action+"(itemlist[0])"  # Peliculas -> lista de opciones de peliculas
        exec "itemlist = cuevana."+itemlist[0].action+"(itemlist[1])"  # Novedades -> lista de pelis
        exec "itemlist = cuevana."+itemlist[0].action+"(itemlist[1])"  # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("cuevana")
    else: no_funcionan.append("cuevana")

    # delatv
    try:
        from pelisalacarta.channels import delatv
        itemlist = delatv.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = delatv."+itemlist[0].action+"(itemlist[0])"  # Novedades -> lista de pelis
        exec "itemlist = delatv."+itemlist[0].action+"(itemlist[0])"  # peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("delatv")
    else: no_funcionan.append("delatv")

    # descargacineclasico
    try:
        from pelisalacarta.channels import descargacineclasico
        itemlist = descargacineclasico.mainlist(Item()) # -> lista categorias
        exec "itemlist = descargacineclasico."+itemlist[0].action+"(itemlist[0])"  # categoria -> lista de pelis
        itemlist = servertools.find_video_items(itemlist[0]) # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("descargacineclasico")
    else: no_funcionan.append("descargacineclasico")

    # descargapelis
    try:
        from pelisalacarta.channels import descargapelis
        itemlist = descargapelis.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = descargapelis."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de pelis
        exec "itemlist = descargapelis."+itemlist[0].action+"(itemlist[0])" # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("descargapelis")
    else: no_funcionan.append("descargapelis")

    # dibujosanimadosgratis
    try:
        from pelisalacarta.channels import dibujosanimadosgratis
        itemlist = dibujosanimadosgratis.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = dibujosanimadosgratis."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de pelis
        itemlist = servertools.find_video_items(itemlist[0]) # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("dibujosanimadosgratis")
    else: no_funcionan.append("dibujosanimadosgratis")

    # discoverymx
    try:
        from pelisalacarta.channels import discoverymx
        itemlist = discoverymx.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = discoverymx."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales
        exec "itemlist = discoverymx."+itemlist[0].action+"(itemlist[0])" # Primer documental -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("discoverymx")
    else: no_funcionan.append("discoverymx")

    # divxonline
    try:
        from pelisalacarta.channels import divxonline
        itemlist = divxonline.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = divxonline."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de pelis
        exec "itemlist = divxonline."+itemlist[0].action+"(itemlist[0])" # Primera peli -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("divxonline")
    else: no_funcionan.append("divxonline")

    # documaniatv
    try:
        from pelisalacarta.channels import documaniatv
        itemlist = documaniatv.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = documaniatv."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales
        exec "itemlist = documaniatv."+itemlist[0].action+"(itemlist[0])" # Primer documental -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("documaniatv")
    else: no_funcionan.append("documaniatv")

    # documentalesatonline2
    try:
        from pelisalacarta.channels import documentalesatonline2
        itemlist = documentalesatonline2.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = documentalesatonline2."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales
        exec "itemlist = documentalesatonline2."+itemlist[0].action+"(itemlist[0])" # Primer documental -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("documentalesatonline2")
    else: no_funcionan.append("documentalesatonline2")

    # documentalesyonkis
    try:
        from pelisalacarta.channels import documentalesyonkis
        itemlist = documentalesyonkis.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = documentalesyonkis."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales
        exec "itemlist = documentalesyonkis."+itemlist[0].action+"(itemlist[0])" # Primer documental -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("documentalesyonkis")
    else: no_funcionan.append("documentalesyonkis")

    # documentariestv
    try:
        from pelisalacarta.channels import documentariestv
        itemlist = documentariestv.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = documentariestv."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales
        exec "itemlist = documentariestv."+itemlist[0].action+"(itemlist[0])" # Primer documental -> lista de vídeos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("documentariestv")
    else: no_funcionan.append("documentariestv")

    # gratisdocumentales
    try:
        from pelisalacarta.channels import gratisdocumentales
        itemlist = gratisdocumentales.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = gratisdocumentales."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de documentales (videos directos)
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("gratisdocumentales")
    else: no_funcionan.append("gratisdocumentales")

    # internapoli
    try:
        from pelisalacarta.channels import internapoli
        itemlist = internapoli.mainlist(Item()) # -> novedades
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("internapoli")
    else: no_funcionan.append("internapoli")

    # islapeliculas
    try:
        from pelisalacarta.channels import islapeliculas
        itemlist = islapeliculas.mainlist(Item()) # -> lista opciones del canal
        exec "itemlist = islapeliculas."+itemlist[0].action+"(itemlist[0])"  # novedades -> lista de pelis
        exec "itemlist = islapeliculas."+itemlist[0].action+"(itemlist[0])"  # pelicula -> lista de videos
    except:
        itemlist=[]

    if len(itemlist)>0: funcionan.append("islapeliculas")
    else: no_funcionan.append("islapeliculas")

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
    post = "loginUserName=aaa&loginUserPassword=bbb&autoLogin=on&ppp=102&loginFormSubmit=Login"
    data = scrapertools.cache_page(url, post=post)

    url = "http://www.fileserve.com/file/uzSn5He"
    post = "download=premium"
    data = scrapertools.cache_page(url)

if __name__ == "__main__":
    #test_server_connectors()
    #test_cineraculo()
    #test_channels()
    #test_samba()
    test_fileserver_premium()