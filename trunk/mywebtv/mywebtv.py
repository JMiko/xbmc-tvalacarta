# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Main
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urllib
import os
import sys
import xbmc
from core import config
from core import logger

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    logger.info("get_params")
    
    param_string = sys.argv[2]
    
    logger.info("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            logger.info("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = urllib.unquote_plus(split_command[1])
                    commands[key] = value
                else:
                    commands[command] = ""
    
    logger.info("get_params "+repr(commands))
    return commands

def run():
    logger.info("[mywebtv.py] run")
    
    # Imprime en el log los parámetros de entrada
    logger.info("[mywebtv.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    params = get_params()
    logger.info("[mywebtv.py] params=%s" % str(params))
    
    # Extrae la url de la página
    if (params.has_key("url")):
        url = urllib.unquote_plus( params.get("url") )
    else:
        url=''
    logger.info("[mywebtv.py] url="+url)

    # Extrae la accion
    if (params.has_key("action")):
        action = params.get("action")
    else:
        action = "selectchannel"
    logger.info("[mywebtv.py] action="+action)

    # Extrae la categoria
    if (params.has_key("category")):
        category = urllib.unquote_plus( params.get("category") )
    else:
        if params.has_key("channel"):
            category = params.get("channel")
        else:
            category = ""
    logger.info("[mywebtv.py] category="+category)


    # Accion por defecto - elegir canal
    if ( action=="selectchannel" ):
        import channelselector as plugin
        plugin.listchannels(params, url, category)
    # Actualizar version
    elif ( action=="update" ):
        from core import updater
        updater.update(params)
        import channelselector as plugin
        plugin.listchannels(params, url, category)
    # El resto de acciones vienen en el parámetro "action", y el canal en el parámetro "channel"
    else:
        try:
            exec "from channels import "+params.get("channel")+" as plugin"
            exec "plugin."+action+"(params, url, category)"
        except:
            exec "from lib import "+params.get("channel")+" as plugin"
            exec "plugin."+action+"(params, url, category)"
