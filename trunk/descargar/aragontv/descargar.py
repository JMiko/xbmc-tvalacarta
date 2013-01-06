# -*- coding: utf-8 -*-
from Tkinter import *
import re

from core import config

class MyDialog:

    def __init__(self, parent):
    
        top = self.top = parent
        
        Label(top, text="Introduzca la URL del video de Aragón TV").pack()
        
        self.e = Entry(top)
        self.e.config(width="75")
        self.e.insert(0, "http://alacarta.aragontelevision.es/programas/aragoneses-por-el-mundo/shangai-09062011-2123")
        self.e.pack(padx=5)
        
        Label(top, text="Introduzca el directorio de descarga").pack()
        
        self.e2 = Entry(top)
        self.e2.config(width="75")

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-aragontv.conf" )
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

        b = Button(top, text="Descargar", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):
        pageurl = self.e.get()
        print "Pagina", pageurl

        output = self.e2.get()
        print "Descargar en", output

        import os
        confpath = os.path.join( config.get_data_path() , "descargar-aragontv.conf" )
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
        pageurl = pageurl.encode("utf-8")
        data = scrapertools.cachePage(pageurl)
        patron = "<title>(.*?)</title>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            titulo = matches[0]
        print "Titulo = "+titulo
        
        from servers import aragontv
        video_urls = aragontv.get_video_url(pageurl)
        url = video_urls[0][1]

        import os
        salida = os.path.join( output , "%s.mp4" % self.clean_title(titulo,windows_mode) )
        print salida

        # Invoca a rtmpdump
        if windows_mode:
            print "Comando: "+'./rtmpdump.exe -r "'+url+'" -o "'+salida+'" --live'
            import shlex, subprocess
            args = shlex.split('./rtmpdump.exe -r "'+url+'" -o "'+salida+'" --live')
            p = subprocess.call(args) # Success!
        else:
            print "Comando: "+'./rtmpdump -r "'+url+'" -o "'+salida+'" --live'
            import shlex, subprocess
            args = shlex.split('./rtmpdump -r "'+url+'" -o "'+salida+'" --live')
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
root.title("Descargar de Aragón TV - v1.1")

d = MyDialog(root)

root.wait_window(d.top)
