# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Megavideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# A partir del código de Voinage y Coolblaze
#------------------------------------------------------------

import re, xbmc
import urlparse, urllib, urllib2

try:
    from core import scrapertools
    from core import logger
    from core import config
except:
    from Code.core import scrapertools
    from Code.core import logger
    from Code.core import config

import os
COOKIEFILE = os.path.join(config.get_data_path() , "cookies.lwp")

logger.debug("[megavideo.py] Cookiefile="+COOKIEFILE) 

#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.

DEBUG = False

#Megavideo - Coolblaze # Part 1 put this below VIDEOLINKS function. Ctrl & C after highlighting.

def ajoin(arr):
    strtest = ''
    for num in range(len(arr)):
        strtest = strtest + str(arr[num])
    return strtest

def asplit(mystring):
    arr = []
    for num in range(len(mystring)):
        arr.append(mystring[num])
    return arr
        
def decrypt(str1, key1, key2):

    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        if (holder == "0"):
            __reg1.append("0000")
        else:
            if (__reg0 == "1"):
                __reg1.append("0001")
            else:
                if (__reg0 == "2"): 
                    __reg1.append("0010")
                else: 
                    if (__reg0 == "3"):
                        __reg1.append("0011")
                    else: 
                        if (__reg0 == "4"):
                            __reg1.append("0100")
                        else: 
                            if (__reg0 == "5"):
                                __reg1.append("0101")
                            else: 
                                if (__reg0 == "6"):
                                    __reg1.append("0110")
                                else: 
                                    if (__reg0 == "7"):
                                        __reg1.append("0111")
                                    else: 
                                        if (__reg0 == "8"):
                                            __reg1.append("1000")
                                        else: 
                                            if (__reg0 == "9"):
                                                __reg1.append("1001")
                                            else: 
                                                if (__reg0 == "a"):
                                                    __reg1.append("1010")
                                                else: 
                                                    if (__reg0 == "b"):
                                                        __reg1.append("1011")
                                                    else: 
                                                        if (__reg0 == "c"):
                                                            __reg1.append("1100")
                                                        else: 
                                                            if (__reg0 == "d"):
                                                                __reg1.append("1101")
                                                            else: 
                                                                if (__reg0 == "e"):
                                                                    __reg1.append("1110")
                                                                else: 
                                                                    if (__reg0 == "f"):
                                                                        __reg1.append("1111")

        __reg3 = __reg3 + 1

    mtstr = ajoin(__reg1)
    __reg1 = asplit(mtstr)
    __reg6 = []
    __reg3 = 0
    while (__reg3 < 384):
    
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        __reg6.append((int(key1) + int(key2)) % 128)
        __reg3 = __reg3 + 1
    
    __reg3 = 256
    while (__reg3 >= 0):

        __reg5 = __reg6[__reg3]
        __reg4 = __reg3 % 128
        __reg8 = __reg1[__reg5]
        __reg1[__reg5] = __reg1[__reg4]
        __reg1[__reg4] = __reg8
        __reg3 = __reg3 - 1
    
    __reg3 = 0
    while (__reg3 < 128):
    
        __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
        __reg3 = __reg3 + 1

    __reg12 = ajoin(__reg1)
    __reg7 = []
    __reg3 = 0
    while (__reg3 < len(__reg12)):

        __reg9 = __reg12[__reg3:__reg3 + 4]
        __reg7.append(__reg9)
        __reg3 = __reg3 + 4
        
    
    __reg2 = []
    __reg3 = 0
    while (__reg3 < len(__reg7)):
        __reg0 = __reg7[__reg3]
        holder2 = __reg0
    
        if (holder2 == "0000"):
            __reg2.append("0")
        else: 
            if (__reg0 == "0001"):
                __reg2.append("1")
            else: 
                if (__reg0 == "0010"):
                    __reg2.append("2")
                else: 
                    if (__reg0 == "0011"):
                        __reg2.append("3")
                    else: 
                        if (__reg0 == "0100"):
                            __reg2.append("4")
                        else: 
                            if (__reg0 == "0101"): 
                                __reg2.append("5")
                            else: 
                                if (__reg0 == "0110"): 
                                    __reg2.append("6")
                                else: 
                                    if (__reg0 == "0111"): 
                                        __reg2.append("7")
                                    else: 
                                        if (__reg0 == "1000"): 
                                            __reg2.append("8")
                                        else: 
                                            if (__reg0 == "1001"): 
                                                __reg2.append("9")
                                            else: 
                                                if (__reg0 == "1010"): 
                                                    __reg2.append("a")
                                                else: 
                                                    if (__reg0 == "1011"): 
                                                        __reg2.append("b")
                                                    else: 
                                                        if (__reg0 == "1100"): 
                                                            __reg2.append("c")
                                                        else: 
                                                            if (__reg0 == "1101"): 
                                                                __reg2.append("d")
                                                            else: 
                                                                if (__reg0 == "1110"): 
                                                                    __reg2.append("e")
                                                                else: 
                                                                    if (__reg0 == "1111"): 
                                                                        __reg2.append("f")
                                                                    
        __reg3 = __reg3 + 1

    endstr = ajoin(__reg2)
    return endstr

########END OF PART 1

#Part 2
# Paste this into your Default.py
# To activate it just call Megavideo(url) - where url is your megavideo url.
def getcode(mega):
    logger.info("[megavideo.py] mega="+mega)
    if mega.startswith('http://www.megavideo.com/?v='):
        # FIXME: (3.1) Esto no funciona con url que tienen distintos parámetros, hay que usar ER para extraer el código
        mega = mega[-8:]
    logger.info("[megavideo.py] mega="+mega)
    return mega

def Megavideo(mega):

    mega = getcode(mega)

    logger.info("[megavideo.py] Megavideo")
    modoPremium = config.get_setting("megavideopremium")
    logger.info("[megavideo.py] modoPremium="+modoPremium)
    
    if modoPremium == "false":
        movielink = getlowurl(mega)
    else:
        movielink = gethighurl(mega)

    logger.info("[megavideo.py] movielink="+movielink)
        
    return movielink
#####END of part 2

def getlowurl(code,password=None):
    logger.info("[megavideo.py] Baja calidad")
    
    code=getcode(code)
    try:
        quality = config.get_setting("quality_flv")
    except:
        quality = "0"
    
    modoPremium = config.get_setting("megavideopremium")
    logger.info("[megavideo.py] modoPremium="+modoPremium)
    if modoPremium == "false":
        logger.info("[megavideo.py] usando modo normal para baja calidad")
        req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+code)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        req.add_header('Referer', 'http://www.megavideo.com/')
        page = urllib2.urlopen(req);response=page.read();page.close()
        logger.info("response="+response)	
        errort = re.compile(' errortext="(.+?)"').findall(response)	
        if len(errort) <= 0:
            password_data = re.compile('password_required="(.*?)"').findall(response)
            if len(password_data) > 0:
                if password_data[0]=="1":
                    if password is not None:
                        keyboard = xbmc.Keyboard(password,"Contraseña:")
                        keyboard.doModal()
                    else:
                        keyboard = xbmc.Keyboard("","Contraseña:")
                        keyboard.doModal()
                    if (keyboard.isConfirmed()):
                        tecleado = keyboard.getText()
                        if len(tecleado)<=0:
                            return
                        logger.info("Teclado : "+tecleado)						
                        req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+code+"&password="+tecleado)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        req.add_header('Referer', 'http://www.megavideo.com/')
                        page = urllib2.urlopen(req);response=page.read();page.close()
                        logger.info("Data URL : "+response)			
        '''
        logger.info("response="+response)
        hd = re.compile(' hd="(.+?)"').findall(response)
        if len(hd)>0 and hd[0]=="1":
            logger.info("hd="+hd[0])
            movielink = re.compile(' hd_url="(.+?)"').findall(response)[0]
            movielink = movielink.replace("%3A",":")
            movielink = movielink.replace("%2F","/")
            movielink = movielink + "?.flv"
            logger.info("movielink="+movielink)
        else:
        '''
        errort = re.compile(' errortext="(.+?)"').findall(response)
        movielink = ""
        if len(errort) <= 0:
            
            if quality == "1":
                hd = re.compile(' hd="(.+?)"').findall(response)
                if len(hd)>0 and hd[0]=="1":
                    s = re.compile(' hd_s="(.+?)"').findall(response)
                    k1 = re.compile(' hd_k1="(.+?)"').findall(response)
                    k2 = re.compile(' hd_k2="(.+?)"').findall(response)
                    un = re.compile(' hd_un="(.+?)"').findall(response)
                    movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
                    return movielink        
            
            s = re.compile(' s="(.+?)"').findall(response)
            k1 = re.compile(' k1="(.+?)"').findall(response)
            k2 = re.compile(' k2="(.+?)"').findall(response)
            un = re.compile(' un="(.+?)"').findall(response)
            movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
            #addLink(name, movielink+'?.flv','')
    else:
        logger.info("[megavideo.py] usando modo premium para baja calidad")
        megavideocookie = config.get_setting("megavideocookie")
        if DEBUG: logger.info("[megavideo.py] megavideocookie=#"+megavideocookie+"#")

        logger.info("[megavideo.py] Averiguando cookie...")
        megavideologin = config.get_setting("megavideouser")
        if DEBUG: logger.info("[megavideo.py] megavideouser=#"+megavideologin+"#")

        megavideopassword = config.get_setting("megavideopassword")
        if DEBUG: logger.info("[megavideo.py] megavideopassword=#"+megavideopassword+"#")

        megavideocookie = GetMegavideoUser(megavideologin, megavideopassword)
        if DEBUG: logger.info("[megavideo.py] megavideocookie=#"+megavideocookie+"#")

        if len(megavideocookie) == 0:
            try:
                import xbmcgui
                advertencia = xbmcgui.Dialog()
                resultado = advertencia.ok('Cuenta de Megavideo errónea' , 'La cuenta de Megavideo que usas no es válida' , 'Comprueba el login y password en la configuración')
            except:
                pass
            return ""

        req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+code+"&u="+megavideocookie)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        req.add_header('Referer', 'http://www.megavideo.com/')
        page = urllib2.urlopen(req);response=page.read();page.close()
        errort = re.compile(' errortext="(.+?)"').findall(response)
        movielink = ""

        if len(errort) <= 0:
            if quality == "1":
                hd = re.compile(' hd="(.+?)"').findall(response)
                if len(hd)>0 and hd[0]=="1":
                    s = re.compile(' hd_s="(.+?)"').findall(response)
                    k1 = re.compile(' hd_k1="(.+?)"').findall(response)
                    k2 = re.compile(' hd_k2="(.+?)"').findall(response)
                    un = re.compile(' hd_un="(.+?)"').findall(response)
                    movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
                    return movielink

            s = re.compile(' s="(.+?)"').findall(response)
            k1 = re.compile(' k1="(.+?)"').findall(response)
            k2 = re.compile(' k2="(.+?)"').findall(response)
            un = re.compile(' un="(.+?)"').findall(response)
            movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
            #addLink(name, movielink+'?.flv','')
    
    return movielink

def gethighurl(code):
    logger.info("[megavideo.py] Usa modo premium")
    
    code = getcode(code)

    megavideocookie = config.get_setting("megavideocookie")
    if DEBUG:
        logger.info("[megavideo.py] megavideocookie=#"+megavideocookie+"#")
    #if megavideocookie=="":
    logger.info("[megavideo.py] Averiguando cookie...")
    megavideologin = config.get_setting("megavideouser")
    if DEBUG: logger.info("[megavideo.py] megavideouser=#"+megavideologin+"#")
    megavideopassword = config.get_setting("megavideopassword")
    if DEBUG: logger.info("[megavideo.py] megavideopassword=#"+megavideopassword+"#")
    megavideocookie = GetMegavideoUser(megavideologin, megavideopassword)
    if DEBUG: logger.info("[megavideo.py] megavideocookie=#"+megavideocookie+"#")

    if len(megavideocookie) == 0:
        try:
            import xbmcgui
            advertencia = xbmcgui.Dialog()
            resultado = advertencia.ok('Cuenta de Megavideo errónea' , 'La cuenta de Megavideo que usas no es válida' , 'Comprueba el login y password en la configuración')
        except:
            pass
        return ""

    req = urllib2.Request("http://www.megavideo.com/xml/player_login.php?u="+megavideocookie+"&v="+code)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    
    # saca los enlaces
    patronvideos  = 'downloadurl="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    movielink = matches[0]
    movielink = movielink.replace("%3A",":")
    movielink = movielink.replace("%2F","/")
    movielink = movielink.replace("%20"," ")
    
    return movielink

def GetMegavideoUser(login, password):
    logger.info("GetMegavideoUser")
    # ---------------------------------------
    #  Inicializa la librería de las cookies
    # ---------------------------------------
    ficherocookies = COOKIEFILE
    # Borra el fichero de cookies para evitar errores
    try:
        os.remove(ficherocookies)
    except:
        pass

    # the path and filename to save your cookies in

    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        import cookielib
    except ImportError:
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            import ClientCookie
        except ImportError:
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.LWPCookieJar()

    else:
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.LWPCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    # ---------------------------------
    # Instala las cookies
    # ---------------------------------

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules

        if os.path.isfile(ficherocookies):
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            cj.load(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    #print "-------------------------------------------------------"
    url="http://www.megavideo.com/?c=login"
    #print url
    #print "-------------------------------------------------------"
    theurl = url
    # an example url that sets a cookie,
    # try different urls here and see the cookie collection you can make !

    #passwordesc=password.replace("&","%26")
    passwordesc = urllib.quote(password)
    
    txdata = "login=1&redir=1&username="+login+"&password="+passwordesc
    # if we were making a POST type request,
    # we could encode a dictionary of values here,
    # using urllib.urlencode(somedict)

    txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Referer':'http://www.megavideo.com/?s=signup'}
    # fake a user agent, some websites (like google) don't like automated exploration

    req = Request(theurl, txdata, txheaders)
    handle = urlopen(req)
    cj.save(ficherocookies)                     # save the cookies again    

    data=handle.read()
    '''
    logger.info("----------------------")
    logger.info("Respuesta de Megavideo")
    logger.info("----------------------")
    logger.info(data)
    logger.info("----------------------")
    '''
    handle.close()

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    '''
    logger.info("----------------------")
    logger.info("Cookies despues")
    logger.info("----------------------")
    logger.info(cookiedata)
    logger.info("----------------------")
    '''

    patronvideos  = 'user="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(cookiedata)
    if len(matches)==0:
        patronvideos  = 'user=([^\;]+);'
        matches = re.compile(patronvideos,re.DOTALL).findall(cookiedata)
    
    if len(matches)==0:
        logger.info("No se ha encontrado la cookie de Megavideo")
        logger.info("----------------------")
        logger.info("Respuesta de Megavideo")
        logger.info("----------------------")
        logger.info(data)
        logger.info("----------------------")
        logger.info("----------------------")
        logger.info("Cookies despues")
        logger.info("----------------------")
        logger.info(cookiedata)
        logger.info("----------------------")
        return ""
    else:
        return matches[0]