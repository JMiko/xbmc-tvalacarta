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
    para_probar.append("adnstream")

    funcionan = []
    no_funcionan = []
    
    no_probados = []
    #no_probados.append("justintv")

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
    
def descargar_programa_aragontv( channel_id , episodes_action , url , output_folder ):
    from servers import aragontv as servermodule
    exec "from tvalacarta.channels import "+channel_id+" as channelmodule"
    exec "itemlist = channelmodule."+episodes_action+"(Item(url=url))"
    
    resultados = []
    
    for item in itemlist:
        mediaurl = servermodule.get_video_url(item.url)
        resultados.append( [ item.title, mediaurl[0][1] , clean_title(item.title) + mediaurl[0][1][-4:] ] )

    for title,url,localfile in resultados:
        print title,url,localfile
        
        ejecutable = "/Users/jesus/Downloads/rtmpdump/rtmpdump-2.4"
        salida = os.path.join( output_folder , localfile )

        if not os.path.exists(salida):
            print "Comando: "+ejecutable+' -r "'+url+'" --live -o "'+salida+'"'
            import shlex, subprocess
            args = shlex.split(ejecutable+' -r "'+url+'" --live -o "'+salida+'"')
            print args
            p = subprocess.call(args) # Success!
        else:
            print "Ya existe "+salida

def descargar_programa_antena3( channel_id , episodes_action , url ):
    
    # Items que tiene que visitar
    from servers import aragontv as servermodule
    exec "from tvalacarta.channels import "+channel_id+" as channelmodule"
    exec "itemlist = channelmodule."+episodes_action+"(Item(url=url))"

    pendientes = []
    for item in itemlist:
        pendientes.append(item)
    
    # Items que ya ha visitado
    visitados = set()

    # Lo que finalmente va a descargar
    resultados = []

    # Recorre la lista de pendientes    
    indice = 0
    while True:

        # Lee el siguiente de la lista
        item = pendientes[indice]
        
        # Si no lo ha visitado
        if item.url not in visitados:

            # Lo marca como visitado
            visitados.add(item.url)

            # Lo visita y si es el que tiene los episodios, obtiene los links
            if item.action=="detalle":
                media_url_itemlist = channelmodule.detalle(item)
                for media_url_item in media_url_itemlist:
                    resultados.append( [ item.title, media_url_item.url , clean_title(media_url_item.title) + media_url_item.url[-4:] ] )
            else:
                exec "itemlist = channelmodule."+item.action+"(item)"
                for item in itemlist:
                    pendientes.append(item)

        # Avanza en la lista
        indice = indice + 1
        
        # Si no quedan elementos, acaba
        if indice>=len(pendientes):
            print "Fin de la lista"
            break

    # Ahora descarga uno por uno los links
    for title,url,localfile in resultados:
        print title,url,localfile
        
        ejecutable = "/Users/jesus/Downloads/rtmpdump-2.4"
        salida = "/Users/jesus/Downloads/Vaya casas/"+localfile

        # Solo si no existen ya...
        if not os.path.exists(salida):
            print "Comando: "+ejecutable+' -r "'+url+'" -o "'+salida+'"'
            import shlex, subprocess
            args = shlex.split(ejecutable+' -r "'+url+'" -o "'+salida+'"')
            print args
            p = subprocess.call(args) # Success!
        else:
            print "Ya existe "+salida

def clean_title(title):

    '''
    try:
        title = unicode(title,"iso-8859-1",errors="ignore").encode("utf-8")
    except:
        pass
    '''

    # Elimina caracteres no válidos 
    validchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÇçÑñÁÉÍÓÚáéíóí1234567890- "
    title = ''.join(c for c in title if c in validchars)

    # Sólo windows
    #title = unicode(title,"utf-8",errors="ignore").encode("iso-8859-1")

    return title

if __name__ == "__main__":
    '''
    from servers import telefe
    
    #video_urls = telefe.get_video_url("http://www.telefe.com/2010/10/09/lo-que-el-tiempo-nos-dejo-un-mundo-mejor/")
    video_urls = telefe.get_video_url("http://elelegido.telefe.com/2011/10/26/capitulo-152-26-10-11/")
    
    for video_url in video_urls:
        print './rtmpdump-2.4 -r "'+video_url[1]+'" -s "http://www.telefe.com/wp-content/plugins/fc-velocix-video/flowplayer/flowplayer.rtmp-3.1.3.swf" -o out.mp4'
    '''
    
    #from servers import tvg    
    #video_urls = tvg.get_video_url("http://www.crtvg.es/tvg/a-carta/cap-35")
    
    #descargar_programa_aragontv("aragontv","episodios","http://alacarta.aragontelevision.es/programas/vaughan-ingles-4.0/","/Users/jesus/Downloads/PROGRAMAS/Vaughan/")
    #descargar_programa_antena3("antena3","episodios","http://www.antena3.com/videos/vaya-casa.html")
    #descargar_programa_aragontv("aragontv","episodios","http://alacarta.aragontelevision.es/programas/aragoneses-por-el-mundo/","/Users/jesus/Downloads/PROGRAMAS/Aragoneses por el mundo/")
    test_channels()
