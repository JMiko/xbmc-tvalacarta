# -*- coding: utf-8 -*-
from Tkinter import *
import re

class MyDialog:

    def __init__(self, parent):
    
        top = self.top = parent
        
        Label(top, text="Introduzca la URL del video 3alacarta").pack()
        
        self.e = Entry(top)
        self.e.config(width="75")
        self.e.insert(0, "http://www.tv3.cat/3alacarta/#/videos/3262992")
        self.e.pack(padx=5)
        
        Label(top, text="Introduzca el directorio de descarga").pack()
        
        self.e2 = Entry(top)
        self.e2.config(width="75")

        import os
        confpath = os.path.join( os.path.expanduser('~') , "descargar-tv3.conf" )
        if os.path.exists( confpath ):
            print "Leyendo ruta anterior "+confpath
            fichero = open(confpath,"r")
            ruta = fichero.read()
            fichero.close()
        else:
            ruta=os.path.expanduser('~')

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
        confpath = os.path.join( os.path.expanduser('~') , "descargar-tv3.conf" )
        try:
            fichero = open(confpath,"w")
            fichero.write(output)
            fichero.close()
        except:
            print "Error al grabar "+confpath
            pass
        
        # Cierra el gui
        self.top.destroy()

        # Obtiene el código del vídeo
        
        # Primero separa la URL en trozos
        trozos = pageurl.split("/")
        
        # Busca el código, empezando por el final
        trozos.reverse()
        code = ""
        for trozo in trozos:
            print "Trozo: "+trozo
            patron = "^(\d+)$"
            matches = re.findall(patron,trozo,flags=re.DOTALL)
            if len(matches)>0:
                code = matches[0]
                print "Codigo:",code
                break
        
        # Descarga el descriptor
        import urllib
        destino = os.path.join( os.path.expanduser('~') , "page.html" )
        urllib.urlretrieve("http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint="+code,destino)
        fichero = open(destino,"r")
        data = fichero.read()
        fichero.close()

        # Extrae el título
        patron = "<title>([^<]+)</title>"
        matches = re.findall(patron,data,flags=re.DOTALL)
        titulo = matches[0]
        print "Titulo",titulo
        titulo = self.clean_title(titulo) 
        
        # Extrae el formato
        patron = '<video><format>([^<]+)</format><qualitat[^>]+>([^<]+)</qualitat>'
        matches = re.findall(patron,data,flags=re.DOTALL)
        formato = matches[0][0]
        calidad = matches[0][1]
        print "Calidad",calidad
        print "Formato",formato

        # Descarga el descriptor con el RTMP
        urllib.urlretrieve("http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+code+"&QUALITY="+calidad+"&FORMAT="+formato+"&rnd=8551",destino)
        fichero = open(destino,"r")
        data = fichero.read()
        fichero.close()

        # Extrae la url en rtmp
        patron = '<media[^>]+>([^<]+)</media>'
        matches = re.findall(patron,data,flags=re.DOTALL)
        rtmpurl = matches[len(matches)-1]
        print rtmpurl
        
        # Averigua la extension
        patron = '.*?\.([a-z0-9]+)\?'
        matches = re.findall(patron,rtmpurl,flags=re.DOTALL)
        extension = matches[0].lower()
        print "Extension",extension
        if extension=="mp4":
            extension="flv"
        print "Extension rectificada",extension

        import os
        salida = os.path.join( output , titulo+"."+extension )

        #rtmpurl = "rtmp://mp4-500-str.tv3.cat/ondemand/mp4:g/tvcatalunya/7/0/1292234279807.mp4"
        import shlex, subprocess
        args = shlex.split('./rtmpdump -r "'+rtmpurl+'" -o "'+salida+'"')
        p = subprocess.Popen(args) # Success!

    def clean_title(self,title):

        try:
            title = unicode(title,"iso-8859-1",errors="ignore").encode("utf-8")
        except:
            pass

        # Elimina caracteres no válidos 
        validchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÇçÑñÁÉÍÓÚáéíóí1234567890- "
        title = ''.join(c for c in title if c in validchars)

        # Sólo windows
        title = unicode(title,"utf-8",errors="ignore").encode("iso-8859-1")

        return title

root = Tk()

d = MyDialog(root)

root.wait_window(d.top)