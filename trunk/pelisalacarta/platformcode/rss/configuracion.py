# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuración
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import downloadtools
from core import config
from core import logger
from core.item import Item

CHANNELNAME = ""
logger.info("[configuracion.py] init")

def mainlist(params,url="",category=""):
    global CHANNELNAME
    logger.info("[configuracion.py] mainlist")
    
    config.open_settings( )

    CHANNELNAME = params.url.split("/")[0]
    return respuesta()


def respuesta():
    
    itemlist = []
 
    salir = config.get_localized_string(30167)
    salvar = config.get_localized_string(30166)
    itemlist.append( Item(channel="", title=salir , action="EXIT") )
    nuevo_item(itemlist, "megavideopremium", 30013, "bool", CHANNELNAME)    
    nuevo_item(itemlist, "megavideouser", 30014, "text", CHANNELNAME)    
    nuevo_item(itemlist, "megavideopassword", 30015, "text", CHANNELNAME)    
    nuevo_item(itemlist, "enableadultmode", 30002, "bool", CHANNELNAME)    
    nuevo_item(itemlist, "updatechannels", 30170, "bool", CHANNELNAME)    
    nuevo_item(itemlist, "downloadpath", 30017, "text", CHANNELNAME)    
    nuevo_item(itemlist, "downloadlistpath", 30018, "text", CHANNELNAME)    
    nuevo_item(itemlist, "bookmarkpath", 30030, "text", CHANNELNAME)    
    nuevo_item(itemlist, "jdownloader", 30022, "text", CHANNELNAME)    
    nuevo_item(itemlist, "limite_busquedas", 30024, "text", CHANNELNAME)    
    nuevo_item(itemlist, "enablemedia-translate", 31000, "bool", CHANNELNAME)    
    itemlist.append( Item(channel=CHANNELNAME, title=salvar , action="salvar" , url="salvar" , extra="none", server="SALVAR") )

    return itemlist

def nuevo_item(itemlist, campo, codigo, tipo, canal):
    
    valor = config.get_setting(campo)
    
    titulo = config.get_localized_string(codigo)+" "
    if campo=="megavideopassword": titulo += "*****"
    else: titulo += valor
    
    campo = "%s=%s" % (campo,codigo)
    if tipo == "bool": 
       accion = "setup"
    else:
       accion = "search"
    itemlist.append( Item(channel=canal, title=titulo , action=accion , url=campo ,  extra=tipo) )
    

def setup(item):
    
    campo = item.url.split("=")[0]
    codigo = item.url.split("=")[1]
    valor = config.get_setting(campo)
    if item.extra == "bool":
       if valor == "true": valor="false"
       else: valor = "true"
    config.set_setting(campo,valor)
    
    return respuesta()

def search(item,texto):
    
    campo = item.url.split("=")[0]
    codigo = item.url.split("=")[1]
    valor = config.get_setting(campo)
    if valor != texto:
       config.set_setting(campo,texto)
    
    return respuesta()

def salvar(item):
    
    config.save_settings()
    
    titulo = config.get_localized_string(30168)
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="mainlist") )

    return itemlist

