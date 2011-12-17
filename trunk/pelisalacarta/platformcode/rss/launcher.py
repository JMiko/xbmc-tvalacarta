# -*- coding: utf-8 -*-
###### ! /usr/bin/env python
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import os
import binascii
import md5

from core.scrapertools import entityunescape
from core import config
from core.item import Item
from rsstools import DepuraTitulo as DepuraTitulo
#from rsstools import LimpiarTitulo as LimpiarTitulo

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("rss")

#from lib import cerealizer
#cerealizer.register(Item)

def controller(plugin_name,port,host,path,headers):
        respuesta = '<?xml version=\'1.0\' encoding="UTF-8" ?>\n<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        respuesta += "<channel>\n"
        respuesta += "<link>%s</link>\n\n" % path
        
        if path == "/rss" or path == "/rss/":
            import channelselector
            channelslist = channelselector.getmainlist()

            respuesta += "<title>Menú Principal</title>\n\n"     # Parametrizar

            # Actualización automática de canales, actualiza la lista
            if config.get_setting("updatechannels")=="true":
                try:
                   from core import updater
                   actualizado = updater.updatechannel("channelselector")

                   if actualizado:
                       respuesta += "<title>¡Lista de canales actualizada!</title>\n"
                       respuesta += "<image></image>\n"
                       respuesta += "<link>http://"+host+"/rss/</link>\n"
                       respuesta += "\n"
                except:
                   pass

            for channel in channelslist:
	           respuesta += "<item>\n"
	           respuesta += "<title>"+channel.title+"</title>\n"
	           respuesta += "<image>http://"+plugin_name+".mimediacenter.info/posters/"+channel.channel+".png</image>\n"
	           
	           if channel.channel=="trailertools":
                	enlace = "http://"+host+"/rss/"+channel.channel+"/search/none/none/none/none/none/none/none/playlist.rss"
                	respuesta += "<link>rss_command://search</link>"
                	respuesta += "<search url=\""+enlace+"%s\" />"
	           else:
                	respuesta += "<link>http://"+host+"/rss/"+channel.channel+"/"+channel.action+"/none/none/none/none/none/none/none/playlist.rss</link>\n"
                
	           respuesta += "</item>\n"
	           respuesta += "\n"
      
        elif path.startswith("/rss/channelselector/channeltypes"):
            
            import channelselector
            channelslist = channelselector.getchanneltypes()
            
            respuesta += "<title>Tipo de contenido</title>\n\n"     # Parametrizar
            for channel in channelslist:
                respuesta += "<item>\n"
                respuesta += "<title>"+channel.title+"</title>\n"
                respuesta += "<link>http://"+host+"/rss/"+channel.channel+"/"+channel.action+"/"+channel.category+"/none/none/none/none/none/playlist.rss</link>\n"
                respuesta += "<image>http://"+plugin_name+".mimediacenter.info/wiimc/"+channel.thumbnail+".png</image>\n"
                respuesta += "</item>\n"
                respuesta += "\n"
        
        elif path.startswith("/rss/channelselector/listchannels"):
            
            category = path.split("/")[4]
            logger.info("##category="+category)

            import channelselector
            channelslist = channelselector.filterchannels(category)
            
            respuesta += "<title>Canales</title>\n\n"     # Parametrizar
            for channel in channelslist:
                if channel.type=="generic" or channel.type=="rss": # or channel.type=="wiimc":
                    respuesta += "<item>\n"
                    respuesta += "<title>"+channel.title.replace("_generico","").replace(" (Multiplataforma)","")+"</title>\n"
                    respuesta += "<link>http://"+host+"/rss/"+channel.channel+"/mainlist/none/none/none/none/none/none/playlist.rss</link>\n"
                    respuesta += "<image>http://"+plugin_name+".mimediacenter.info/posters/"+channel.channel+".png</image>\n"
                    respuesta += "</item>\n"
                    respuesta += "\n"
        else:
            import rsstools
            itemlist,channel = rsstools.getitems(path)

            # Las listas vacías son problemáticas, añade un elemento dummy
            if len(itemlist)==0:
               itemlist.append( Item(title="(No hay elementos)", action=path.split("/")[3]) ) ## <---
        
            import urllib
             
            respuesta += "<title>%s</title>\n" % channel.replace("_generico","").replace(" (Multiplataforma)","")
            
            for item in itemlist:
                respuesta += "<item>\n"
                if item.server=="": item.server="none"
                if item.url=="": item.url="none"
                if item.extra=="": item.extra="none"
                if item.title=="": item.title="none"
                if item.fulltitle=="": item.fulltitle="none"
                if item.category=="": item.category="none"
                if item.channel=="": item.channel=channel
                
                if item.action == "search":
                   url = "http://%s/rss/%s/%s/%s/%s/%s/%s/%s/%s/playlist.rss" % ( host , channel , item.action , urllib.quote_plus(item.url) , item.server, urllib.quote_plus(item.title),urllib.quote_plus(item.extra),urllib.quote_plus(item.category),urllib.quote_plus(item.fulltitle))               
                   respuesta += "<title>%s</title>\n" % entityunescape(item.title)
                   if item.fulltitle  not in ("","none"): respuesta += "<fulltitle>%s</fulltitle>\n" % item.fulltitle
                   if item.thumbnail != "":    respuesta += "<image>%s</image>\n" % item.thumbnail
                   respuesta += "<link>rss_command://search</link>\n"
                   respuesta += "<search url=\""+url+"%s\" />\n"
                   respuesta += "\n"
                   
                elif item.action=="EXIT":
                    respuesta += "<title>%s</title>\n" % entityunescape(item.title)
                    if item.thumbnail != "": respuesta += "<image>%s</image>\n" % item.thumbnail
                    url = "http://%s/rss/" %  host
                    respuesta += "<link>%s</link>\n" % url
                    respuesta += "\n"
                
                elif item.folder or item.action=="play" or item.action=="downloadall":
                    logger.info("  Nivel intermedio")
                    item.fulltitle = DepuraTitulo(item.fulltitle, "false", "false")

                    from core.scrapertools import slugify
                    play_name = "%s_%s.dat" % ( item.channel ,  urllib.quote(item.fulltitle) )
                    play_name = slugify(play_name)
                    if item.plot not in ("none",""):
                        item.plot = item.plot.replace("\n"," ") 
                        salva_descripcion(play_name, item.fulltitle, item.plot, item.thumbnail)
                    else:
                        fulltitle,plot,thumbnail = recupera_descripcion(play_name)
                        if fulltitle != "" and item.fulltitle in ("","none"): item.fulltitle = fulltitle
                        if plot      != "" and item.plot == "":               item.plot = plot
                        if thumbnail != "" and item.thumbnail == "":          item.thumbnail = thumbnail
                    if item.title=="none": item.title="Ver el video"
                    url = "http://%s/rss/%s/%s/%s/%s/%s/%s/%s/%s/playlist.rss" % ( host , item.channel , item.action , urllib.quote_plus(item.url) , item.server , urllib.quote(item.title),urllib.quote_plus(item.extra),urllib.quote_plus(item.category),urllib.quote_plus(item.fulltitle) )
                    respuesta += "<title><![CDATA[%s]]></title>\n" % unicode(item.title,"iso-8859-1",errors="ignore").encode("utf-8")
                    if item.fulltitle not in ("","none"): respuesta += "<fulltitle><![CDATA[%s]]></fulltitle>\n" % unicode(item.title,"iso-8859-1",errors="ignore").encode("utf-8")
                    if item.plot != "":                   respuesta += "<description><![CDATA[ %s ]]></description>\n" % unicode(item.plot,"iso-8859-1",errors="ignore").encode("utf-8")
                    if item.thumbnail != "":              respuesta += "<image>%s</image>\n" % item.thumbnail
                    respuesta += "<link>%s</link>\n" % url
                    respuesta += "\n"
                else:
                    logger.info("  Video")
                    from core.scrapertools import slugify
                    play_name = "%s_%s.dat" % ( item.channel ,  urllib.quote(item.fulltitle) )
                    play_name = slugify(play_name)
                    fulltitle,plot,thumbnail = recupera_descripcion(play_name)
                    if fulltitle != "" and item.fulltitle in ("","none"): item.fulltitle = fulltitle
                    if plot      != "" and item.plot == "":               item.plot = plot
                    if thumbnail != "" and item.thumbnail == "":          item.thumbnail = thumbnail
                    #respuesta += "<title><![CDATA[%s]]></title>\n" % entityunescape(item.title)
                    respuesta += "<title><![CDATA[%s]]></title>\n" % unicode(fulltitle,"iso-8859-1",errors="ignore").encode("utf-8")
                    respuesta += "<fulltitle><![CDATA[%s]]></fulltitle>\n" % unicode(item.title,"iso-8859-1",errors="ignore").encode("utf-8")
                    respuesta += "<description><![CDATA[%s]]></description>\n" % unicode(plot,"iso-8859-1",errors="ignore").encode("utf-8")
                    respuesta += "<enclosure url=\"%s\" type=\"video/x-flv\" />\n" % item.url
                    respuesta += "<image>%s</image>\n" % thumbnail
                respuesta += "</item>\n\n"

        respuesta += "</channel>\n"
        respuesta += "</rss>\n"
        print "--------------------------------------------"
        print respuesta
        print "--------------------------------------------"
        return respuesta
    
def salva_descripcion(play_name,fulltitle,plot,thumbnail):
    if fulltitle == "none": fulltitle == ""
    # Obtiene un nombre válido para la cache
    #hashed_url = binascii.hexlify(md5.new(play_name).digest())
    #cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , hashed_url )
    cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , play_name )
    fichero = open( cached_file ,"w")
    fichero.write(thumbnail+"\n")
    fichero.write(fulltitle+"\n")
    fichero.write(plot)
    fichero.close()
    # if os.path.exists(cached_file):

def recupera_descripcion(play_name):
    plot=""
    thumbnail=""
    fulltitle=""
    # Obtiene un nombre válido para la cache
    #hashed_url = binascii.hexlify(md5.new(play_name).digest())
    #cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , hashed_url )
    cached_file = os.path.join( config.get_data_path() , "tmp" , "cache" , play_name )
    if os.path.exists(cached_file):
        fichero = open( cached_file ,"r")
        thumbnail = fichero.readline().replace("\n","")
        fulltitle = fichero.readline().replace("\n","")
        plot = fichero.read().replace("\n"," ")
        fichero.close()
    return fulltitle,plot,thumbnail


