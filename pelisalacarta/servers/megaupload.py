# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Megaupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urlparse, urllib, urllib2
import exceptions

from core import scrapertools
from core import logger
from core import config

DEBUG=True
PREMIUM=0
GRATIS=1
ANONIMO=2

def get_video_url( page_url , user="" , password="" , video_password="" ):
    if DEBUG:
        logger.info("[megaupload.py] get_video_url( page_url='%s' , user='%s' , password='%s')" % (page_url , user , password) )
    else:
        logger.info("[megaupload.py] get_video_url(page_url='%s')" % page_url)
    
    # Si sólo viene el código, se convierte a URL completa
    if len(page_url)==8:
        page_url = "http://www.megaupload.com/?d="+page_url

    # page_url es del tipo "http://www.megaupload.com/?d="+code
    # Si el usuario es premium utiliza el método antiguo
    # Si el usuario es gratis o anónimo utiliza el método nuevo
    tipo_usuario , cookie = login(user,password)

    if tipo_usuario == PREMIUM:
        video_url = get_premium_video_url(page_url,cookie,video_password)
    else:
        video_url = get_free_video_url(page_url,tipo_usuario,video_password)
        
    logger.info("[megaupload.py] get_video_url returns %s" % video_url)
    
    return video_url

# Extrae directamente la URL del vídeo de Megaupload
def login(user,password):
    if DEBUG:
        logger.info("[megaupload.py] login( user='%s' , password='%s')" % (user , password) )
    else:
        logger.info("[megaupload.py] login")

    # Parámetros
    url="http://www.megaupload.com/?c=login"
    post = "login=1&redir=1&username="+user+"&password="+urllib.quote(password)
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.megaupload.com']]

    # Invocación
    data = scrapertools.cache_page(url=url,post=post,headers=headers,modo_cache=scrapertools.CACHE_NUNCA)

    # Extrae el tipo de usuario
    login = re.search('Welcome', data)
    premium = re.search('flashvars.status = "premium";', data)        

    # Si no está el welcome, no es una cuenta válida
    if login is None:
        tipo_usuario = ANONIMO
    else:
        # Si no es premium, es una cuenta gratis
        if premium is None:
            tipo_usuario = GRATIS
        else:
            tipo_usuario = PREMIUM
    
    # Saca la cookie del fichero
    cookie_data = config.get_cookie_data()
    patron  = 'user="([^"]+)".*?domain=".megaupload.com"'
    matches = re.compile(patron,re.DOTALL).findall(cookie_data)
    if len(matches)==0:
        patron  = 'user=([^\;]+);.*?domain=".megaupload.com"'
        matches = re.compile(patron,re.DOTALL).findall(cookie_data)
    if len(matches)==0:
        cookie = ""
    else:
        cookie = matches[0]

    usuarios = ['PREMIUM','GRATIS','ANONIMO']
    logger.info("[megaupload.py] login returns tipo_usuario=%d (%s), cookie=%s" % (tipo_usuario , usuarios[tipo_usuario] , cookie) )

    return tipo_usuario , cookie

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise ImportError(302,headers.getheader("Location"))

def get_premium_video_url(page_url,cookie,video_password):
    if DEBUG:
        logger.info("[megaupload.py] get_premium_video_url( page_url='%s' , cookie=%s )" % (page_url , cookie))
    else:
        logger.info("[megaupload.py] get_premium_video_url( page_url='%s' )" % page_url)

    req = urllib2.Request(page_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Cookie', 'l=es; user='+cookie)
    try:
        opener = urllib2.build_opener(SmartRedirectHandler())
        response = opener.open(req)
    except ImportError, inst:    
        status,location=inst
        logger.info(str(status) + " " + location)    
        mediaurl = location
    else:
        data=response.read()
        response.close()

        patronvideos  = '<div class="down_ad_pad1">[^<]+<a href="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        mediaurl = ""
        if len(matches)>0:
            mediaurl = matches[0]
            # Timeout del socket a 60 segundos
            import socket
            socket.setdefaulttimeout(10)

            h=urllib2.HTTPHandler(debuglevel=0)
            request = urllib2.Request(mediaurl)

            opener = urllib2.build_opener(h)
            urllib2.install_opener(opener)
            try:
            
                connexion = opener.open(request)
                mediaurl= connexion.geturl()
            
            except urllib2.HTTPError,e:
                logger.error( "[megaupload.py]  error %d (%s) al abrir la url %s" % (e.code,e.msg,mediaurl) )
                logger.error(e.read())

    return mediaurl

def get_free_video_url(page_url , tipo_usuario , video_password=None):
    logger.info("[megaupload.py] get_free_video_url( page_url='%s' )" % page_url)

    # Descarga la página de MU
    data = scrapertools.cache_page(page_url,modo_cache=scrapertools.CACHE_NUNCA)
    
    # Si tiene password lo pide
    password_data = re.search('filepassword',data)
    if password_data is not None:
        teclado = password_mega(video_password)
        
        # Vuelve a descargar la página con password
        if teclado is not None:
            data = scrapertools.cache_page(page_url, post="filepassword="+teclado,modo_cache=scrapertools.CACHE_NUNCA)
        else:
            return None

    # Comprueba si es un enlace premium
    match1=re.compile('<a href="(.+?)" class="down_ad_butt1">').findall(data)
    if str(match1)=='[]':
        match2=re.compile('id="downloadlink"><a href="(.+?)" class=').findall(data)
        try:
            url=match2[0]
        except:
            return None
    else:
        url=match1[0]

    # TODO ¿?
    #Si es un archivo .divx lo sustituye por .avi
    if url.endswith('divx'):
        url = url[:-4]+'avi'

    if url is None:
        return None
    else:
        if tipo_usuario == GRATIS:
            espera = handle_wait(26,'Megaupload','Cargando video.')    
        else:
            espera = handle_wait(46,'Megaupload','Cargando video.')
    
        if espera == True:
            return url
        else:
            import xbmcgui
            advertencia = xbmcgui.Dialog()
            resultado = advertencia.ok('pelisalacarta','Se canceló la reproducción')        
            return None

def handle_wait(time_to_wait,title,text):
    logger.info ("[megaupload.py] handle_wait(time_to_wait=%d)" % time_to_wait)
    if config.get_platform()=="xbmc" or config.get_platform()=="xbmcdharma" or config.get_platform()=="boxee":
        logger.info('Esperando %d segundos' %time_to_wait )
        import xbmc,xbmcgui
        espera = xbmcgui.DialogProgress()
        ret = espera.create(' '+title)
    
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
    
        cancelled = False
        while secs < time_to_wait:
            secs = secs + 1
            percent = increment*secs
            secs_left = str((time_to_wait - secs))
            remaining_display = ' Espera '+secs_left+' segundos para que comience el vídeo...'
            espera.update(percent,' '+text,remaining_display)
            xbmc.sleep(1000)
            if (espera.iscanceled()):
                 cancelled = True
                 break
        if cancelled == True:     
             logger.info ('Espera cancelada')
             return False
        else:
             logger.info ('Espera finalizada')
             return True
    else:
        logger.info ('Espera de %d segundos' % time_to_wait)
        import time
        time.sleep(time_to_wait)
        return True

def password_mega(password):
    logger.info ("[megaupload.py] password_mega()")

    if password is not None:
        keyboard = xbmc.Keyboard(password,"Contraseña:")
    else:
        keyboard = xbmc.Keyboard("","Contraseña:")
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return
        else:
            return tecleado

# Convierte el código de megaupload a megavideo
def convertcode(megaupload_page_url):
    logger.info("[megaupload.py] convertcode "+megaupload_page_url)

    # Si sólo viene el código, convierte a URL completa
    if len(megaupload_page_url)==8:
        megaupload_page_url = "http://www.megaupload.com/?d="+megaupload_page_url

    # Descarga la página de megavideo pasándole el código de megaupload
    url = megaupload_page_url.replace("megaupload","megavideo")
    data = scrapertools.cache_page(url,modo_cache=scrapertools.CACHE_NUNCA)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = 'flashvars.v = "([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.logger.infoMatches(matches)
    
    megavideocode = ""
    if len(matches)>0:
            megavideocode = matches[0]

    return megavideocode

def getlowurl(code , password=None):
    import megavideo
    return megavideo.getlowurl(convertcode(code),password)

# Encuentra vídeos de megaupload en el texto pasado
# Los devuelve con URL "http://www.megaupload.com/?d=AQW9ED93"
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos  = '<a.*?href="http://www.megaupload.com/\?d=([A-Z0-9a-z]{8})".*?>(.*?)</a>'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        titulo = scrapertools.htmlclean(match[1].strip())+" [Megaupload]"
        url = "http://www.megaupload.com/?d="+match[0]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    patronvideos  = 'http\://www.megaupload.com/(?:es/)?\?.*?d\=([A-Z0-9a-z]{8})(?:[^>]*>([^<]+)</a>)?'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        if match[1]<>"":
            titulo = match[1].strip()+" - [Megaupload]"
        else:
            titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match[0]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    # Código especial cinetube
    #xrxa("BLYT2ZC9=d?/moc.daolpuagem.www//:ptth")
    patronvideos  = 'xrxa\("([A-Z0-9a-z]{8})=d\?/moc.daolpuagem.www//\:ptth"\)'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match[::-1]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://www.megavideo.com/\?d\=([^"]+)"'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve