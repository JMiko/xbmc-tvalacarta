#! /usr/bin/env python
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from core import config

PORT=int(config.get_setting("server.port"))

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print "-----------------------------------------------------------------"
        print self.path
        print self.headers
        print "-----------------------------------------------------------------"
        
        try:
            host = self.headers.get("Host")
        except:
            host = ""
        
        if not host.endswith(str(PORT)):
            host = host + ":" + str(PORT)
        
        print "host="+host

        respuesta = ""

        respuesta += "version=7\n"
        #self.wfile.write("background=http://www.mimediacenter.info/xbmc/tvalacarta/icon.jpg")
        respuesta += "logo=http://www.mimediacenter.info/xbmc/tvalacarta/icon.jpg\n"
        respuesta += "title=tvalacarta 3.0.1 (WiiMC)\n"
        respuesta += "\n"

        if self.path == "/":
            import channelselector
            channelslist = channelselector.getmainlist()

            for channel in channelslist:
                respuesta += "type=playlist\n"
                respuesta += "name="+channel[0]+"\n"
                respuesta += "thumb=http://www.mimediacenter.info/xbmc/tvalacarta/posters/"+channel[1]+".png\n"
                respuesta += "URL=http://"+host+"/"+channel[1]+"/"+channel[2]+"/none/none/playlist.plx\n"
                respuesta += "\n"
        
        elif self.path.startswith("/channelselector/channeltypes"):
            
            import channelselector
            channelslist = channelselector.getchanneltypes()
            
            for channel in channelslist:
                respuesta += "type=playlist\n"
                respuesta += "name="+channel[0]+"\n"
                respuesta += "thumb=http://www.mimediacenter.info/xbmc/tvalacarta/posters/"+channel[4]+".png\n"
                respuesta += "URL=http://"+host+"/"+channel[1]+"/"+channel[2]+"/"+channel[3]+"/none/playlist.plx\n"
                respuesta += "\n"
        
        elif self.path.startswith("/channelselector/listchannels"):
            
            category = self.path.split("/")[3]
            print "##category="+category

            import channelselector
            channelslist = channelselector.filterchannels(category)
            
            for channel in channelslist:
                if channel[5]=="generic":
                    respuesta += "type=playlist\n"
                    respuesta += "name="+channel[0]+"\n"
                    respuesta += "thumb=http://www.mimediacenter.info/xbmc/tvalacarta/posters/"+channel[1]+".png\n"
                    respuesta += "URL=http://"+host+"/"+channel[1]+"/mainlist/none/none/playlist.plx\n"
                    respuesta += "\n"

        else:
            from platform.wiimc import wiitools
            itemlist,channel = wiitools.getitems(self.path)
            
            import urllib
            for item in itemlist:
                if item.folder or item.action=="play":
                    if item.server=="": item.server="none"
                    if item.url=="": item.url="none"
                    if item.title=="": item.title="Ver el video-"

                    url = "http://%s/%s/%s/%s/%s/playlist.plx" % ( host , channel , item.action , urllib.quote_plus(item.url) , item.server )
                    respuesta += "type=playlist\n"
                    respuesta += "name=%s\n" % item.title
                    if item.thumbnail != "":
                        respuesta += "thumb=%s\n" % item.thumbnail
                    respuesta += "URL=%s\n" % url
                    respuesta += "\n"
                else:
                    respuesta += "type=video\n"
                    respuesta += "name=%s\n" % item.title
                    respuesta += "URL=%s\n" % item.url
                    respuesta += "\n"

        print "--------------------------------------------"
        print respuesta
        print "--------------------------------------------"
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(respuesta)
        self.wfile.close()

        return
    
    def address_string(self):
        # Disable reverse name lookups
        return self.client_address[:2][0] 

def run():
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
    
    # Levanta el servidor
    try:
        server = HTTPServer(('', PORT), MyHandler)
        #print server.server_address
        print "Servidor iniciado en http://"+myip+":"+str(PORT) 
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
        server.shutdown()
        import sys
        sys.exit()
        raise SystemExit
        os._exit(0)
        print "Sigo aqui"

if __name__ == '__main__':
    run()













