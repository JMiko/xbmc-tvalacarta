# -*- coding: utf-8 -*-
from Tkinter import *
import re

from core import config

class MyDialog:

    def __init__(self, parent):
    
        top = self.top = parent
        
        Label(top, text="Introduzca la URL del video de Antena 3").pack()
        
        self.e = Entry(top)
        self.e.config(width="75")
        self.e.insert(0, "http://www.antena3.com/videos/karlos-arguinano/2011-junio-1.html")
        self.e.pack(padx=5)
        
        Label(top, text="Introduzca el directorio de descarga").pack()
        
        self.e2 = Entry(top)
        self.e2.config(width="75")

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-antena3.conf" )
        if os.path.exists( confpath ):
            print "Leyendo ruta anterior "+confpath
            fichero = open(confpath,"r")
            ruta = fichero.read()
            fichero.close()
        else:
            ruta=config.get_data_path()

        self.e2.insert(0, ruta)
        self.e2.pack(padx=5)
        
        b = Button(top, text="Descargar", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):
        pageurl = self.e.get()
        print "Pagina", pageurl

        output = self.e2.get()
        print "Descargar en", output

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-antena3.conf" )
        try:
            fichero = open(confpath,"w")
            fichero.write(output)
            fichero.close()
        except:
            print "Error al grabar "+confpath
            pass
        
        # Cierra el gui
        self.top.destroy()

        # Desactiva la cache
        config.set_setting("cache.mode","2")

        # Obtiene el código del vídeo
        from servers import antena3
        itemlist = antena3.get_movie_links(pageurl)

        contador = 1
        for item in itemlist:
            print item.url
            import os
            salida = os.path.join( output , "%s (Parte %d).mp4" % ( self.clean_title(item.title) , contador) )
            print salida
            contador = contador + 1

            # Invoca a rtmpdump
            print "Comando: "+'./rtmpdump.exe -r "'+item.url+'" -o "'+salida+'"'
            import shlex, subprocess
            args = shlex.split('./rtmpdump.exe -r "'+item.url+'" -o "'+salida+'"')
            p = subprocess.call(args) # Success!

    def clean_title(self,title):

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
        title = unicode(title,"utf-8",errors="ignore").encode("iso-8859-1")

        return title

root = Tk()

d = MyDialog(root)

root.wait_window(d.top)