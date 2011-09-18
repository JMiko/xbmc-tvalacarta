# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import config
from core import logger
from core import samba
from core import favoritos
from core.item import Item

CHANNELNAME = "descargas"
DEBUG = True

DOWNLOAD_LIST_PATH = config.get_setting("downloadlistpath")
IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' )
ERROR_PATH = os.path.join( DOWNLOAD_LIST_PATH, 'error' )
usingsamba = DOWNLOAD_LIST_PATH.upper().startswith("SMB://")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[descargados.py] mainlist")
    itemlist=[]

    # Lee la ruta de descargas
    downloadpath = config.get_setting("downloadpath")

    logger.info("[descargados.py] downloadpath=" + downloadpath)
    #logger.info("[descargados.py] pluginhandle=" + pluginhandle)

    itemlist.append( Item( channel="descargas", action="pendientes", title="Descargas pendientes"))
    itemlist.append( Item( channel="descargas", action="errores", title="Descargas con error"))

    # Añade al listado de XBMC
    try:
        ficheros = os.listdir(downloadpath)
        for fichero in ficheros:
            logger.info("[descargados.py] fichero=" + fichero)
            if fichero!="lista" and fichero!="error" and fichero!=".DS_Store" and not fichero.endswith(".nfo") and not fichero.endswith(".tbn") and os.path.join(downloadpath,fichero)!=config.get_setting("downloadlistpath"):
                url = os.path.join( downloadpath , fichero )
                itemlist.append( Item( channel="descargados", action="play", title=fichero, url=url, server="local", folder=False))

    except:
        logger.info("[descargados.py] exception on mainlist")
        pass

    return itemlist

def pendientes(item):
    logger.info("[descargas.py] pendientes")
    itemlist=[]

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
            titulo,thumbnail,plot,server,url = favoritos.readbookmark(fichero,DOWNLOAD_LIST_PATH)

            # Crea la entrada
            # En la categoría va el nombre del fichero para poder borrarlo
            itemlist.append( Item( channel=CHANNELNAME , action="play" , url=url , server=server, title=titulo, thumbnail=thumbnail, plot=plot, fanart=thumbnail, extra=os.path.join( DOWNLOAD_LIST_PATH, fichero ), folder=False ))

        except:
            pass
            logger.info("[descargas.py] error al leer bookmark")
            for line in sys.exc_info():
                logger.error( "%s" % line )

    itemlist.append( Item( channel=CHANNELNAME , action="downloadall" , title="(Empezar la descarga de la lista)", thumbnail=os.path.join(IMAGES_PATH, "Crystal_Clear_action_db_update.png") , folder=False ))

    return itemlist

def errorlist(item):
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
            titulo,thumbnail,plot,server,url = favoritos.readbookmark(fichero,ERROR_PATH)

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
                titulo,thumbnail,plot,server,url = favoritos.readbookmark(fichero,DOWNLOAD_LIST_PATH)
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
                        favoritos.savebookmark(titulo, url, thumbnail, server, plot, ERROR_PATH)
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
                    favoritos.savebookmark(titulo, url, thumbnail, server, plot, ERROR_PATH)
                    favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def savebookmark(titulo,url,thumbnail,server,plot,savepath=DOWNLOAD_LIST_PATH):
    favoritos.savebookmark(titulo,url,thumbnail,server,plot,savepath)

def deletebookmark(fullfilename,deletepath=DOWNLOAD_LIST_PATH):
    favoritos.deletebookmark(fullfilename,deletepath)

def borrar_descarga(fullfilename):
    os.remove(fullfilename)

def mover_descarga_error_a_pendiente(fullfilename):
    # La categoría es el nombre del fichero en favoritos, así que lee el fichero
    titulo,thumbnail,plot,server,url = favoritos,readbookmarkfile(fullfilename,"")
    # Lo añade a la lista de descargas
    descargadoslist.savebookmark(title,url,thumbnail,server,plot)
    # Y lo borra de la lista de errores
    os.remove(urllib.unquote_plus( extra ))
