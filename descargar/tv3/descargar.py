# -*- coding: utf-8 -*-
from Tkinter import *
import re

class MyDialog:

    def __init__(self, parent):
    
        top = self.top = parent
        
        Label(top, text="Introduzca la URL del video 3alacarta").pack()
        
        self.e = Entry(top)
        self.e.config(width="75")
        self.e.insert(0, "http://www.tv3.cat/3alacarta/#/videos/4179850")
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
        page_url = "http://www.tv3.cat/pvideo/FLV_bbd_dadesItem.jsp?idint="+code
        urllib.urlretrieve(page_url,"page.html")
        fichero = open("page.html","r")
        data = fichero.read()
        fichero.close()
        print "-------------------------------------------------------------------"
        print page_url
        print "-------------------------------------------------------------------"
        print data.strip()

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
        #page_url = "http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="+code+"&QUALITY="+calidad+"&FORMAT="+formato+"&rnd=8551"
        page_url = "http://www.tv3.cat/pvideo/FLV_bbd_media.jsp?ID="+code+"&QUALITY="+calidad+"&FORMAT="+formato+""
        urllib.urlretrieve(page_url,"page.html")
        fichero = open("page.html","r")
        data = fichero.read()
        fichero.close()
        print "-------------------------------------------------------------------"
        print page_url
        print "-------------------------------------------------------------------"
        print data.strip()

        # Extrae la url en rtmp
        patron = '<media[^>]+>([^<]+)</media>'
        matches = re.findall(patron,data,flags=re.DOTALL)
        rtmpurl = matches[len(matches)-1]
        print rtmpurl
        
        # Averigua la extension
        patron = '.*?\.([a-z0-9]+)\?'
        matches = re.findall(patron,rtmpurl,flags=re.DOTALL)
        if len(matches)>0:
            extension = matches[0].lower()
        else:
            extension = rtmpurl[-3:]

        print "Extension",extension
        if extension=="mp4":
            extension="flv"
        print "Extension rectificada",extension

        import os
        salida = os.path.join( output , titulo+"."+extension )

        #rtmpurl = "rtmp://mp4-es-500-strfs.fplive.net/mp4-es-500-str/mp4:g/tvcatalunya/6/9/1342385038696.mp4"
        # ./rtmpdump-2.4
        #     --tcUrl "rtmp://mp4-es-500-strfs.fplive.net:1935/mp4-es-500-str?ovpfv=1.1&ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Wind.ows%20NT%205.1%3B%20es-ES%3B%20rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        #     --app "mp4-es-500-str?ovpfv=1.1&ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Windows%20NT%205.1%3B%20es-ES%3B%20.rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        #     --playpath "mp4:g/tvcatalunya/6/9/1342385038696.mp4?ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Windows%20NT%205.1%3B%20es-.ES%3B%20rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        #     -o out.mp4 --host "mp4-es-500-strfs.fplive.net" --port "1935"
        patron = "rtmp\://(.*?)/(.*?)/(.*?)$"
        matches = re.findall(patron,rtmpurl,flags=re.DOTALL)
        
        host = matches[0][0]
        tcUrl = matches[0][1]
        playpath = matches[0][2]
    
        port = "1935"
        app = tcUrl + "?ovpfv=1.1&ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Windows%20NT%205.1%3B%20es-ES%3B%20.rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        tcUrl = "rtmp://"+host+":"+port+"/" + tcUrl + "?ovpfv=1.1&ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Wind.ows%20NT%205.1%3B%20es-ES%3B%20rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        playpath = playpath + "?ua=Mozilla/5.0%20%28Windows%3B%20U%3B%20Windows%20NT%205.1%3B%20es-.ES%3B%20rv%3A1.9.2.13%29%20Gecko/20101203%20Firefox/3.6.13"
        
        print "host="+host
        print "port="+port
        print "tcUrl="+tcUrl
        print "app="+app
        print "playpath="+playpath
        
        comando = './rtmpdump --host "'+host+'" --port "'+port+'" --tcUrl "'+tcUrl+'" --app "'+app+'" --playpath "'+playpath+'" -o "'+salida+'"'
        print comando
        
        import shlex, subprocess
        
        args = shlex.split(comando)
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