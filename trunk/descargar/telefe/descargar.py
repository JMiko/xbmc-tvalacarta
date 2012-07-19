# -*- coding: utf-8 -*-
from Tkinter import *
import re

from core import config

class MyDialog:

    def __init__(self, parent):
    
        top = self.top = parent
        
        Label(top, text="Introduzca la URL del video de Telefe").pack()
        
        self.e = Entry(top)
        self.e.config(width="75")
        self.e.insert(0, "http://www.telefe.com/2010/10/09/lo-que-el-tiempo-nos-dejo-un-mundo-mejor/")
        self.e.pack(padx=5)
        
        Label(top, text="Introduzca el directorio de descarga").pack()
        
        self.e2 = Entry(top)
        self.e2.config(width="75")

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-telefe.conf" )
        if os.path.exists( confpath ):
            print "Leyendo ruta anterior "+confpath
            fichero = open(confpath,"r")
            ruta = fichero.read()
            fichero.close()
        else:
            import os
            ruta=os.path.expanduser("~")

        self.e2.insert(0, ruta)
        self.e2.pack(padx=5)

        Label(top, text="Proxy SOCKS de Argentina\n(sólo si descargas programas geobloqueados y no estás en Argentina)\n(Formato host:puerto)").pack()
    
        self.e3 = Entry(top)
        self.e3.config(width="75")
        self.e3.pack(padx=5)
        
        b = Button(top, text="Descargar", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):
        pageurl = self.e.get()
        print "Pagina", pageurl

        output = self.e2.get()
        print "Descargar en", output

        proxysocks = self.e3.get()
        print "Proxy SOCKS", proxysocks

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-telefe.conf" )
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

        # Obtiene el titulo y la URL del vídeo
        windows_mode = os.path.exists("rtmpdump.exe")
        from core import scrapertools
        data = scrapertools.cachePage(pageurl)
        patron = "<title>(.*?)</title>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            titulo = matches[0]
        print "Titulo = "+titulo
        
        from servers import telefe
        video_urls = telefe.get_video_url(pageurl,page_data=data)
        url = video_urls[0][1]

        import os
        salida = os.path.join( output , "%s.mp4" % self.clean_title(titulo,windows_mode) )
        print salida

        proxyparameter = ""
        if proxysocks!="":
            proxyparameter = " -S "+proxysocks

        # Invoca a rtmpdump
        if windows_mode:
            print "Comando: "+'./rtmpdump.exe -r "'+url+'" -o "'+salida+'" --live' + proxyparameter
            import shlex, subprocess
            args = shlex.split('./rtmpdump.exe -r "'+url+'" -o "'+salida+'" --live' + proxyparameter)
            p = subprocess.call(args) # Success!
        else:
            print "Comando: "+'./rtmpdump -r "'+url+'" -o "'+salida+'" --live' + proxyparameter
            import shlex, subprocess
            args = shlex.split('./rtmpdump -r "'+url+'" -o "'+salida+'" --live' + proxyparameter)
            p = subprocess.call(args) # Success!

    def clean_title(self,title,windows_mode):

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
        if windows_mode:
            title = unicode(title,"utf-8",errors="ignore").encode("iso-8859-1")

        return title

root = Tk()

d = MyDialog(root)

root.wait_window(d.top)
