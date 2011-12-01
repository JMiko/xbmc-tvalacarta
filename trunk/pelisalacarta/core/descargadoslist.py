# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de descargas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import os
import sys

import downloadtools
import config
import logger
import samba
from platformcode.xbmc import xbmctools
import favoritos

from servers import servertools

CHANNELNAME = "descargadoslist"
DEBUG = True
DOWNLOAD_LIST_PATH = config.get_setting("downloadlistpath")
IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' )
ERROR_PATH = os.path.join( DOWNLOAD_LIST_PATH, 'error' )
usingsamba = DOWNLOAD_LIST_PATH.upper().startswith("SMB://")

if not usingsamba:
    # Crea el directorio de la lista de descargas si no existe
    try:
        os.mkdir(DOWNLOAD_LIST_PATH)
    except:
        pass
    try:
        os.mkdir(ERROR_PATH)
    except:
        pass

def mainlist(params,url,category):
    logger.info("[descargadoslist.py] mainlist")

    # Crea un listado con las entradas de favoritos
    if usingsamba:
        ficheros = samba.get_files(DOWNLOAD_LIST_PATH)
    else:
        ficheros = os.listdir(DOWNLOAD_LIST_PATH)

    # Ordena el listado por orden de incorporación
    ficheros.sort()
    
    # Crea un listado con las entradas de la lista de descargas
    for fichero in ficheros:
        logger.info("fichero="+fichero)
        try:
            # Lee el bookmark
            canal,titulo,thumbnail,plot,server,url,fulltitle = favoritos.readbookmark(fichero,DOWNLOAD_LIST_PATH)

            # Crea la entrada
            # En la categoría va el nombre del fichero para poder borrarlo
            xbmctools.addnewvideo( CHANNELNAME , "play" , os.path.join( DOWNLOAD_LIST_PATH, fichero ) , server , titulo , url , thumbnail, plot  , fanart=thumbnail)
        except:
            pass
            logger.info("[downloadall.py] error al leer bookmark")
            for line in sys.exc_info():
                logger.error( "%s" % line )

    xbmctools.addnewvideo( CHANNELNAME , "downloadall" , "category" , "server" , "(Empezar la descarga de la lista)" , "" , os.path.join(IMAGES_PATH, "Crystal_Clear_action_db_update.png"), "" )

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def errorlist(params,url,category):
    logger.info("[descargadoslist.py] errorlist")

    # Crea un listado con las entradas de favoritos
    if usingsamba:
        ficheros = samba.get_files(ERROR_PATH)
    else:
        ficheros = os.listdir(ERROR_PATH)

    # Ordena el listado por orden de incorporación
    ficheros.sort()
    
    # Crea un listado con las entradas de la lista de descargas
    for fichero in ficheros:
        logger.info("[downloadall.py] fichero="+fichero)
        try:
            # Lee el bookmark
            canal,titulo,thumbnail,plot,server,url,fulltitle = favoritos.readbookmark(fichero,ERROR_PATH)

            # Crea la entrada
            # En la categoría va el nombre del fichero para poder borrarlo
            xbmctools.addnewvideo( CHANNELNAME , "playerror" , os.path.join( ERROR_PATH, fichero ) , server , titulo , url , thumbnail, plot  , fanart=thumbnail)
        except:
            pass
            logger.info("[downloadall.py] error al leer bookmark")
            for line in sys.exc_info():
                logger.error( "%s" % line )

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setContent(int( sys.argv[ 1 ] ),"movies")
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def downloadall(params,url,category):
    logger.info("[downloadall.py] downloadall")

    # Lee la lista de ficheros
    if usingsamba:
        ficheros = samba.get_files(DOWNLOAD_LIST_PATH)
    else:
        ficheros = os.listdir(DOWNLOAD_LIST_PATH)

    logger.info("[downloadall.py] numero de ficheros=%d" % len(ficheros))

    # La ordena
    ficheros.sort()
    
    # Crea un listado con las entradas de favoritos
    for fichero in ficheros:
        # El primer video de la lista
        logger.info("[downloadall.py] fichero="+fichero)

        if fichero!="error":
            # Descarga el vídeo
            try:
                # Lee el bookmark
                canal,titulo,thumbnail,plot,server,url,fulltitle = favoritos.readbookmark(fichero,DOWNLOAD_LIST_PATH)
                logger.info("[downloadall.py] url="+url)

                # Averigua la URL del vídeo
                if (server=="Megavideo" or server=="Megaupload") and config.get_setting("megavideopremium")=="true":
                    if server=="Megaupload":
                        mediaurl = servertools.getmegauploadhigh(url)
                    else:
                        mediaurl = servertools.getmegavideohigh(url)
                else:
                    mediaurl = servertools.findurl(url,server)
                logger.info("[downloadall.py] mediaurl="+mediaurl)
                
                # Genera el NFO
                nfofilepath = downloadtools.getfilefromtitle("sample.nfo",titulo)
                outfile = open(nfofilepath,"w")
                outfile.write("<movie>\n")
                outfile.write("<title>"+titulo+")</title>\n")
                outfile.write("<originaltitle></originaltitle>\n")
                outfile.write("<rating>0.000000</rating>\n")
                outfile.write("<year>2009</year>\n")
                outfile.write("<top250>0</top250>\n")
                outfile.write("<votes>0</votes>\n")
                outfile.write("<outline></outline>\n")
                outfile.write("<plot>"+plot+"</plot>\n")
                outfile.write("<tagline></tagline>\n")
                outfile.write("<runtime></runtime>\n")
                outfile.write("<thumb></thumb>\n")
                outfile.write("<mpaa>Not available</mpaa>\n")
                outfile.write("<playcount>0</playcount>\n")
                outfile.write("<watched>false</watched>\n")
                outfile.write("<id>tt0432337</id>\n")
                outfile.write("<filenameandpath></filenameandpath>\n")
                outfile.write("<trailer></trailer>\n")
                outfile.write("<genre></genre>\n")
                outfile.write("<credits></credits>\n")
                outfile.write("<director></director>\n")
                outfile.write("<actor>\n")
                outfile.write("<name></name>\n")
                outfile.write("<role></role>\n")
                outfile.write("</actor>\n")
                outfile.write("</movie>")
                outfile.flush()
                outfile.close()
                logger.info("[downloadall.py] Creado fichero NFO")
                
                # Descarga el thumbnail
                logger.info("[downloadall.py] thumbnail="+thumbnail)
                thumbnailfile = downloadtools.getfilefromtitle(thumbnail,titulo)
                thumbnailfile = thumbnailfile[:-4] + ".tbn"
                logger.info("[downloadall.py] thumbnailfile="+thumbnailfile)
                try:
                    downloadtools.downloadfile(thumbnail,thumbnailfile)
                    logger.info("[downloadall.py] Thumbnail descargado")
                except:
                    logger.info("[downloadall.py] error al descargar thumbnail")
                    for line in sys.exc_info():
                        logger.error( "%s" % line )
                
                # Descarga el video
                dev = downloadtools.downloadtitle(mediaurl,titulo)
                if dev == -1:
                    # El usuario ha cancelado la descarga
                    logger.info("[downloadall.py] Descarga cancelada")
                    return
                elif dev == -2:
                    # Error en la descarga, lo mueve a ERROR y continua con el siguiente
                    logger.info("[downloadall.py] ERROR EN DESCARGA DE "+fichero)
                    if not usingsamba:
                        origen = os.path.join( DOWNLOAD_LIST_PATH , fichero )
                        destino = os.path.join( ERROR_PATH , fichero )
                        import shutil
                        shutil.move( origen , destino )
                    else:
                        favoritos.savebookmark(canal,titulo, url, thumbnail, server, plot, fulltitle , ERROR_PATH)
                        favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)
                else:
                    logger.info("[downloadall.py] Video descargado")
                    # Borra el bookmark e itera para obtener el siguiente video
                    filepath = os.path.join( DOWNLOAD_LIST_PATH , fichero )
                    if usingsamba:
                        os.remove(filepath)
                    else:
                        favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)
                    logger.info("[downloadall.py] "+fichero+" borrado")
            except:
                logger.info("[downloadall.py] ERROR EN DESCARGA DE "+fichero)
                if not usingsamba:
                    origen = os.path.join( DOWNLOAD_LIST_PATH , fichero )
                    destino = os.path.join( ERROR_PATH , fichero )
                    import shutil
                    shutil.move( origen , destino )
                else:
                    favoritos.savebookmark(canal,titulo, url, thumbnail, server, plot, fulltitle, ERROR_PATH)
                    favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def play(params,url,category):
    logger.info("[descargadoslist.py] play")

    import xbmc
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    play_video(CHANNELNAME,server,url,category,title,thumbnail,plot,desdefavoritos=False,desdedescargados=True,desderrordescargas=False)
    
def playerror(params,url,category):
    logger.info("[descargadoslist.py] play")

    import xbmc
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]

    xbmctools.play_video(channel=CHANNELNAME,server=server,url=url,category=category,title=title,thumbnail=thumbnail,plot=plot,desdefavoritos=False,desdedescargados=False,desderrordescargas=True)

def savebookmark(canal,titulo,url,thumbnail,server,plot,fulltitle,savepath=DOWNLOAD_LIST_PATH):
    favoritos.savebookmark(canal,titulo,url,thumbnail,server,plot,fulltitle,savepath)

def deletebookmark(fullfilename,deletepath=DOWNLOAD_LIST_PATH):
    favoritos.deletebookmark(fullfilename,deletepath)
