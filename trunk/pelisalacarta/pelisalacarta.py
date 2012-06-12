#! /usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
print "pelisalacarta server init..."

import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Inicia el core
from core import platform_name
PLATFORM_NAME = platform_name.PLATFORM_NAME

from core import config
config.force_platform(PLATFORM_NAME)

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger(PLATFORM_NAME)

PORT=int(config.get_setting("server.port"))
PLUGIN_NAME = 'pelisalacarta'

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        logger.info("-----------------------------------------------------------------")
        logger.info(" PATH: "+self.path)
        logger.info(" HEADERS:")
        for header in self.headers:
            logger.info("  "+header+"="+self.headers[header])
        
        try:
            host = self.headers.get("Host")
        except:
            host = ""
        
        if not host.endswith(str(PORT)):
            host = host + ":" + str(PORT)
        
        logger.info(" HOST: "+host)
        logger.info("-----------------------------------------------------------------")

        if self.path.startswith("/mediaserver/resources/images") and self.path.endswith(".jpg"):
            f=open( os.path.join ( config.get_runtime_path() , self.path.replace("/mediaserver/","") ) )
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.startswith("/mediaserver/resources/images") and self.path.endswith(".png"):
            f=open( os.path.join ( config.get_runtime_path() , self.path.replace("/mediaserver/","") ) )
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.startswith("/css"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ) )
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.startswith("/js"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ) )
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".html"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "mediaserver" , "template" , self.path[1:] ) )
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.startswith("/"+PLATFORM_NAME):
            exec "from platformcode."+PLATFORM_NAME+" import launcher"
            respuesta = launcher.controller(plugin_name=PLUGIN_NAME,port=PORT,host=host,path=self.path,headers=self.headers)

            self.send_response(200)
            self.send_header('Content-Type', launcher.get_content_type())
            self.end_headers()
            self.wfile.write(respuesta)
            self.wfile.close()

        return
    
    def address_string(self):
        # Disable reverse name lookups
        return self.client_address[:2][0] 

# IP
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.mimediacenter.info', 80))
    myip = s.getsockname()[0]
except:
    myip = "0.0.0.0"

# Crea el directorio cache si no existe    
cachedir = os.path.join( config.get_data_path() , "tmp" , "cache" )
if not os.path.exists(cachedir):
    os.mkdir(os.path.join( config.get_data_path() , "tmp" ))
    os.mkdir(os.path.join( config.get_data_path() , "tmp" , "cache" ))

# Borra la cache de la sesion anterior
for fichero in os.listdir( cachedir ):
    os.remove( os.path.join( cachedir , fichero ) )

try:
    # FIXME: Mejora multithread - http://blog.doughellmann.com/2007/12/pymotw-basehttpserver.html - http://stackoverflow.com/questions/2398144/python-basehttpserver-httpserver-concurrency-threading)
    
    print "Iniciando el servidor en http://"+myip+":"+str(PORT) 
    print "La URL para "+PLATFORM_NAME+" es http://"+myip+":"+str(PORT)+"/"+PLATFORM_NAME
    # Levanta el servidor
    server = HTTPServer(('', PORT), Handler)
    #print server.server_address
    
    # Verifica que las rutas son correctas
    config.verify_directories_created()

    # Force download path if empty
    logger.info("download_path = %s" % config.get_setting("downloadpath") )
    logger.info("download_list_path = %s" % config.get_setting("downloadlistpath") )
    logger.info("bookmark_path = %s" % config.get_setting("bookmarkpath") )

    # Da por levantado el servicio
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down server'
    # FIXME: Aún así a veces no se muere. Probar con esto http://stackoverflow.com/questions/10613194/how-to-deal-with-python-basehttpserver-killed-but-the-port-is-still-be-occupied
    server.socket.close()
    server.shutdown()
    import sys
    sys.exit()
    raise SystemExit
    os._exit(0)
    print "Sigo aqui" 
