# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal "Anime (foros)" by Lily
# http://www.mimediacenter.info/foro/viewtopic.php?f=14&t=401
# Last Updated:29/11/2010
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

import xbmc
import xbmcgui
import xbmcplugin

from servers import servertools
from core import scrapertools
from platform.xbmc import xbmctools

import casttv

CHANNELNAME = "animeforos"

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

urleRdM = "http://www.elrincondelmanga.com/foro/showthread.php?t=75282"

def mainlist(params,url,category):
    category = "Anime"
    categoryerdm = "El Rinc�n del Manga  -  Anime"
    aviso = "Esta carpeta contiene una peque�a selecci�n de series infantiles. En cuanto al resto, se recomienda supervisar los contenidos a los que los menores acceden. Al abrir la carpeta de cada Anime aparecen, antes de los v�deos, sus datos (Clasificaci�n,G�nero,etc.) o la opci�n de buscarlos en McAnime-Enciclopedia. En el aptdo -Informaci�n de la Pel�cula- encontrar� informaci�n procedente de la propia release y de McAnime."
    thumbchannel = "http://www.mimediacenter.info/xbmc/pelisalacarta/posters/animeforos.png"
    #addsimplefolder( CHANNELNAME , "seleccion" , category , "Anime  -  Selecci�n Cl�sicos Infantiles TV" , "" , thumbchannel , aviso)
    addsimplefolder( CHANNELNAME , "seleccion" , "AstroteamRG" , "Anime  -  AstroteamRG" , "" , thumbchannel , "Fuente: http://www.astroteamrg.org")
    #addsimplefolder( CHANNELNAME , "searcherdm" , categoryerdm , "Anime  -  El Rinc�n del Manga", "" , thumbchannel ,"Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
    addsimplefolder( CHANNELNAME , "genres" , "G�neros  -  McAnime-Enciclopedia" , "Anime  -  McAnime-Enciclopedia - El Rinc�n del Manga","http://www.mcanime.net/enciclopedia/anime", thumbchannel ,"Fuentes: http://www.mcanime.net/enciclopedia/anime y http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
    addsimplefolder( CHANNELNAME , "favoritos" , "Mis Favoritos" , "Anime  -  Mis Favoritos","",casttv.STARORANGE_THUMB,"" )
    addsimplefolder( CHANNELNAME , "searchvistos" , "Anime - Vistos" , "Anime  -  Vistos" , "" , thumbchannel , "" )
    addsimplefolder( CHANNELNAME , "favoritos" , "Todos Mis Favoritos" , "Todos Mis Favoritos","",casttv.STAR4COLORS_THUMB, "" )
    addsimplefolder( CHANNELNAME , "ayuda" , "Anime Foros - Ayuda" , "Ayuda" , "" , casttv.HELP_THUMB , "" )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------
    casttv.writetmplist(casttv.FAVCTV_FILE,[],"-1","")
    casttv.writetmplist(casttv.FAVANF_FILE,[],"-1","")
    casttv.writetmplist(casttv.NEWCTV_FILE,[],"-2","")
    casttv.writetmplist(casttv.NEWANF_FILE,[],"-2","")
    casttv.writetmplist(casttv.WCTV_FILE,[],"-2","")
    casttv.writetmplist(casttv.WANF_FILE,[],"-2","")
    casttv.writecache(casttv.FTDATA0,"")
    casttv.writecache(casttv.FTDATA1,"")
    casttv.writecache(casttv.FTDATA2,"")
    casttv.writecache(casttv.EZDATA,"")

def seleccion(params,url,category):
    if category=="Anime":
        listado = clasicoslist()
    else:
        listado = astroteamrglist()

    for item in listado:
        adderdmfolder( CHANNELNAME , "listados" , category , item[0] , item[1] , item[2] , item[3] , item[4] , item[5], item[6] )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------

def favoritos(params,url,category):
    series = []
    listanime = []
    OKxbmcfav="0"
    todostitulo = ""
    respuesta=""

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Espere por favor...'
    Dialogespera.create('pelisalacarta' , line1 , '' )

    if os.path.exists(casttv.FAVANF_FILE):
        listanime,nuevos,update = casttv.readtmplist(casttv.FAVANF_FILE,"-1")
        if update=="1":
            respuesta = casttv.alertreturnfav(category,update)
            if respuesta:
                respuesta="-1"
        if len(listanime)>0:
            nuevosep="0"
            if len(nuevos)>0:
                nuevosep="-1"
            casttv.writetmplist(casttv.FAVANF_FILE,listanime,"-1",nuevosep)
    if len(listanime)==0 or respuesta=="-1":
        listanime,nuevos = findfavoritos(category)
        Dialogespera.create('pelisalacarta' , line1 , '' )

    if category=="Todos Mis Favoritos":
        todostitulo = "Anime - "
        if os.path.exists(casttv.FAVCTV_FILE):
            series,seriesnuevos,updatectv = casttv.readtmplist(casttv.FAVCTV_FILE,"-1")
            if len(series)>0:
                nuevosep="0"
                if len(seriesnuevos)>0:
                    nuevosep="-1"
                casttv.writetmplist(casttv.FAVCTV_FILE,series,"-1",nuevosep)
        if len(series)==0 or respuesta=="-1":
            series,seriesnuevos = casttv.findfavoritos(category)
            Dialogespera.create('pelisalacarta' , line1 , '' )

        OKxbmcfav = casttv.readxbmcfav("0")

    if len(listanime)==0 and len(series)==0 and OKxbmcfav=="0":
        return

    if category=="Todos Mis Favoritos":
        if len(nuevos)>0 or len(seriesnuevos)>0:
            addsimplefolder( CHANNELNAME , "listadonuevos" , "Todos Mis Favoritos - Nuevos Contenidos" , "-*-Todos Mis Favoritos - Nuevos Contenidos Posteriores a [LW]" , "" , casttv.STARGREEN2_THUMB , "" )
        if OKxbmcfav=="-1":
            addsimplefolder( CHANNELNAME , "casttv.xbmcfav" , category , "--------------------------------------------- XBMC ---------------------------------------------" , "" , "" , "" )
        if len(listanime)>0:
            additem( CHANNELNAME , category , "-------------------------------------- ANIME - FOROS -------------------------------------" , "" , "" , "" )
    if len(nuevos)>0:
        addsimplefolder( CHANNELNAME , "listadonuevos" , todostitulo+"Mis Favoritos - Nuevos Contenidos" , "-*-"+todostitulo+"Nuevos Contenidos (Posteriores a [LW])" , "" , casttv.STARGREEN2_THUMB , "" )
    for anime in listanime:
        adderdmfolder( CHANNELNAME , "listados" , anime[0] , anime[1] , anime[2] , anime[3] , anime[4] , anime[5] , anime[6] , anime[7] )

    if category=="Todos Mis Favoritos" and len(series)>0:
        additem( CHANNELNAME , category , "---------------------- CASTTV - TVSHACK - SERIESYONKIS ---------------------" , "" , "" , "" )
        if len(seriesnuevos)>0:
            addsimplefolder( CHANNELNAME , "casttv.listadonuevos" , "Series VO - Mis Favoritas - Nuevos Episodios" , "-*-Series VO - Nuevos Episodios (Posteriores a [LW])" , "" , casttv.STARGREEN2_THUMB , "" )
        for serie in series:
            casttv.addseriefolder( CHANNELNAME , "casttv.listados" , serie[0] , serie[1] , serie[2] , serie[3] , "" , serie[4] , serie[5] )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,False)
    # ------------------------------------------------------------------------------------

def findfavoritos(category):
    #tipocontenido,tipolist e idioma posibilidad filtro
    tipocontenido = "[^<]+"
    tipolist = "Completo"
    idioma = ""
    thumbnail=""
    search = ""
    listaseries = []
    listaerdm = []
    nuevos = []
    listanime = []
    nuevosep="0"

    listafav = casttv.readfav("","","",CHANNELNAME)

    if len(listafav)==0:
        alertnofav()
        return listanime,nuevos

    listaseries=listafav
    for fav in listafav:
        matchurlfav=re.search('elrincondelmanga',fav[2],re.IGNORECASE)
        if (matchurlfav):
            titulo=re.sub('[\\\\]?(?P<signo>[^\w\s\\\\])','\\\\\g<signo>',fav[0])
            if search=="":
                search=titulo
            else:
                search=search+"|"+titulo
    if search<>"":
        search = re.sub('&','&(?:amp;)?',search)
        search = re.sub('\\\\"','(?:\\\\"|&quot;)',search)
        search = re.sub('\\\\!','(?:\\\\!|&#33;)',search)
        search="(?:"+search+")"
        listaerdm = finderdm(urleRdM,tipolist,tipocontenido,search,idioma)
        if len(listaerdm)==0:
            alertnoweb("El Rinc�n del Manga")
        else:
            listaerdm.sort(key=lambda erdm: erdm[0].lower())

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Buscando informaci�n de "'+category+'":'
    Dialogespera.create('pelisalacarta' , line1 , '0%  -  ')
    total = len(listaseries)
    i,j,n,m = casttv.progreso(total)
    OKmca = "-1"
    for serie in listaseries:
        url = serie[2]
        plot = ""
        tcsearch = ""
        titleerdm = ""
        titleinfo = ""
        category0 = ""

        if i>=n:
            i=0
            j=j+m
        if j>=100:
            j=95
        Dialogespera.update(j, line1 , str(j)+'%  -  '+serie[0] )
        i=i+1

        thumbnail=casttv.STARORANGE_THUMB
        if serie[3]=="1":
            thumbnail=casttv.STARGREY_THUMB
        if "elrincondelmanga" in url:
            if len(listaerdm)==0:
                continue
            encontrado = "0"
            for erdm in listaerdm:
                if serie[0]==erdm[0] and serie[2]==erdm[4]:
                    encontrado = "-1"
                    serie[1] = erdm[1]+" ["+erdm[5]+"]"+" ["+erdm[2]+"]"+erdm[3]
                    titleinfo = serie[0]
                    tcsearch = erdm[5]
                    titleerdm = erdm[6]
                    plot = "eRdM"
                    break
            if encontrado=="0":
                tcsearch = serie[1]
                #evita status desactualizado caso extremo de no encontrarse ya en eRdM
                serie[1] = ""
        elif "astroteamrg" in url:
            tcsearch = serie[1]
            serie[1] = ""
            match = re.search('\(by Chihiro\)$',serie[0],re.IGNORECASE)
            if (match):
                titleerdm = "astro"
                title2 = ftitleastrosearch(serie[0])
                if serie[0]<>title2:
                    titleinfo = title2
            else:
                titleerdm = "astro2"
        elif "mcanime" in url:
            if OKmca=="0":
                continue
            matchinfo = re.match('^([^\(]+)\s\((.*?)\)$',serie[0])
            if (matchinfo):
                titleinfo = matchinfo.group(1)
                tcsearch = matchinfo.group(2)
            titleerdm = "mc-anime-fav"
            category0 = category+" - "+titleinfo
            try:
                datamca = scrapertools.downloadpage(url)
            except:
                alertnoresultados(url)
                try:
                    scrapertools.downloadpage("http://www.mcanime.net")
                except:
                    alertnoweb("McAnime")
                    OKmca="0"
                continue
            matchstatus = re.search('<h3>([^<]+)</h3>',datamca)
            if (matchstatus):
                serie[1] = matchstatus.group(1)
        elif "tusdivx" in url:
            tcsearch = serie[1]
            serie[1] = ""
            titleerdm = "tusdivx"

        if category0=="":
            category0 = category+" - "+serie[0]
            category0 = re.sub('(?:\s+\(.*?\)\s+\[Mirror.*\]$|\s+\(.*?\)$)','',category0)
        status=""
        if serie[1]<>"":
            status="  -  "+serie[1]

        if serie[3]<>"1":
            listanuevos = []
            title = serie[0]
            if titleerdm=="mc-anime-fav":
                title = titleinfo
            else:
                title = re.sub('(?:\s+VOSE|\s*\-*\s+\[.*\]|\s+\(by \w+\)\s+\[Mirror.*\]$|\s+\(by \w+\)$|\s+$)','',title)
            titleserievisto = serie[0]
            matchurl2 = re.search('(?:\/showthread.php\?t[^\/]+|\/[^\/]+\/\d+)$',serie[2])
            if (matchurl2):    
                titleserievisto = titleserievisto+matchurl2.group(0)
            listanuevos=findnuevos(category,title,titleserievisto,serie[2],"1",titleerdm)
            if len(listanuevos)>0:
                thumbnail=casttv.STARGREEN_THUMB
                if serie[3]=="-2" and len(listanuevos)>3:
                    listanuevos0 = listanuevos
                    listanuevos = [ listanuevos0[0] , listanuevos0[1] , listanuevos0[2] ]
                if serie[3]=="-1" or serie[3]=="-2":
                    nuevos.extend(listanuevos)

        listanime.append([ category0 , serie[0]+status , serie[2] , thumbnail , plot , titleinfo , tcsearch , titleerdm  ])

    if len(nuevos)>0:
        nuevosep="-1"
    casttv.writetmplist(casttv.FAVANF_FILE,listanime,"-1",nuevosep)
    casttv.writetmplist(casttv.NEWANF_FILE,nuevos,"3","")
    return listanime,nuevos

def findnuevos(category,title,titleserievisto,url,todos,web):
    listanuevos = []

    listavistos = casttv.readvisto(titleserievisto,"LW",CHANNELNAME)

    if len(listavistos)>0:
        listavistos.sort(key=lambda visto: visto[5])
        if listavistos[0][5]=="4":
            return listanuevos

    if web == "astro":
        data = astrodata(title,url)
        if data=="":
            return listanuevos
    elif web == "astro2" or web == "mc-anime" or web == "mc-anime-fav" or web == "tusdivx":
        try:
            data = scrapertools.downloadpage(url)
        except:
            return listanuevos
    else:
        data,plot = erdmdata(url)
        if data=="":
            return listanuevos

    if web<>"mc-anime" and web<>"mc-anime-fav":
        listavideos = findvideos(data,title)
        urlOK="-1"
    else:
        listavideos = servertools.findvideos(data)
        #en el caso de mcanime, se a�aden las releases, por completar desde la Enciclopedia, extrayendo simplemente los v�deos usando servertools,
        # por eso muchos episodios no se identifican por el t�tulo y hay que usar tb la url...
        urlOK="0"

    if len(listavistos)==0:
        listanuevos.append([ category+";;New;;;;;;;"+titleserievisto+";"+listavideos[0][0]+";;"+urlOK , listavideos[0][2] , title+" - "+listavideos[0][0] , listavideos[0][1] ])
        return listanuevos

    listavideos.reverse()
    stop="0"
    for video in listavideos:
        OK="-1"
        for visto in listavistos:
            if urlOK=="-1" and video[0]==visto[1]:
                if visto[5]=="1" or visto[5]=="2":        
                    stop="-1"
                elif visto[5]=="4":
                    OK="0"
                break
            elif urlOK=="0" and video[0]==visto[1] and video[1]==visto[2]:
                if visto[5]=="1" or visto[5]=="2":        
                    stop="-1"
                elif visto[5]=="4":
                    OK="0"
                break
        if stop=="-1":
            break
        if OK=="-1":
            listanuevos.append([ category+";;New;;;;;;;"+titleserievisto+";"+video[0]+";;"+urlOK , video[2] , title+" - "+video[0] , video[1] ])
            if todos=="0":
                break

    listanuevos.reverse()
    return listanuevos

def detail(title,url,category,titleinfo,tcsearch,titleerdm,thumbnail,plot,listupdate):
    paramsback = {'title': title, 'titleinfo': titleinfo, 'tcsearch': tcsearch, 'titleerdm': titleerdm, 'thumbnail': thumbnail, 'plot': plot }
    autor = ""

    if titleerdm<>"mc-anime" and titleerdm<>"mc-anime-fav":
        match0 = re.search('\s+\((by \w+)\)$',title,re.IGNORECASE)
        if (match0):
            autor = " - "+match0.group(1)
        title = re.sub('(?:\s+VOSE|\s*\-*\s+\[.*\]|\s+\(by \w+\)\s+\[Mirror.*\]$|\s+\(by \w+\)$|\s+$)','',title)
    if titleerdm=="mc-anime":
        infos = titleinfo
        titleinfo = title
    if titleinfo=="":
        titleinfo = title

    if plot=="eRdM":
        title = titleinfo
        tcsearch = re.sub('�','i',tcsearch)
    if tcsearch=="":
        tcsearch = "[^\)]+"

    #Previo T�tulo Anime en Vistos
    titleinfo2 = titleinfo
    if titleerdm=="mc-anime" or titleerdm=="mc-anime-fav":
        titleinfo2 = titleinfo+" ("+tcsearch+")"
    elif titleerdm=="astro" or titleerdm=="astro2" or titleerdm=="tusdivx":
        titleinfo2 = paramsback['title']

    # Descarga la p�gina
    if titleerdm == "astro":
        data = astrodata(title,url)
        if data=="":
            alertnoresultados("")
            return
    elif titleerdm=="astro2" or titleerdm=="mc-anime" or titleerdm=="mc-anime-fav" or titleerdm=="tusdivx":
        try:
            data = scrapertools.downloadpage(url)
        except:
            alertnoresultados("")
            return
    else:
        data,plot = erdmdata(url)
        if data=="":
            alertnoresultados("")
            return

    if titleerdm<>"mc-anime" and titleerdm<>"mc-anime-fav":
        listavideos = findvideos(data,title)
        urlOK="-1"
    else:
        listavideos = servertools.findvideos(data)
        urlOK="0"

    if len(listavideos)==0:
        alertnoresultados("")
        return

    if titleerdm=="" or titleerdm=="astro" or titleerdm=="astro2" or titleerdm=="mc-anime-fav" or titleerdm=="tusdivx":
        titleerdm = ftitlesearch(titleinfo)
    elif titleerdm=="eRdM":
        titleerdm = ftitleerdmsearch(titleinfo)

    if titleerdm <> "mc-anime":
        # ------------------------------------------------------
        # Extrae informaci�n del contenido de McAnime - Enciclopedia Beta
        # ------------------------------------------------------
        listainfo = findinfo("",titleinfo,tcsearch,"0","",titleerdm)

        if len(listainfo)==1:
            if  thumbnail == "":
                thumbnail = listainfo[0][6]
            plot = plot+" "+listainfo[0][5]
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , listainfo[0][0]+": Informaci�n McAnime - Enciclopedia Beta" , "" , "" , listainfo[0][5] )
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Clasificaci�n: "+listainfo[0][1] , "" , "" , listainfo[0][5] )
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "G�neros: "+listainfo[0][2] , "" , "" , listainfo[0][5] )
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Contenido: "+listainfo[0][3] , "" , "" , listainfo[0][5] )
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "Sinopsis: "+listainfo[0][4] , "" , "" , listainfo[0][5] )
        else:    
            addsimplefolder( CHANNELNAME , "searchmc" , "McAnime-Enciclopedia" , "***Buscar Informaci�n en McAnime - Enciclopedia Beta" , "http://www.mcanime.net/enciclopedia/anime" , "" ,"Fuente: http://www.mcanime.net/enciclopedia/anime" )
    else:
        matchinfo = re.match('^([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)\|([^\|]*)$',infos)
        additem( CHANNELNAME , category , matchinfo.group(1) , "" , "" , plot )
        additem( CHANNELNAME , category , matchinfo.group(2) , "" , "" , plot )
        additem( CHANNELNAME , category , matchinfo.group(3) , "" , "" , plot )
        additem( CHANNELNAME , category , matchinfo.group(4) , "" , "" , plot )
        additem( CHANNELNAME , category , matchinfo.group(5) , "" , "" , plot )

    # T�tulo Anime en Vistos
    # En fav un anime se identifica por el nombre de la serie y la url (por duplicados en eRdM y no sirve el id de la release que va en status...)
    # En vistos caso eRdM y McAnime se anexa al nombre de la serie el final de la url.
    titleserievisto = titleinfo2
    matchurl = re.search('(?:\/showthread.php\?t[^\/]+|\/[^\/]+\/\d+)$',url)
    if (matchurl):
        titleserievisto = titleinfo2+matchurl.group(0)

    listavistos = casttv.readvisto(titleserievisto,"",CHANNELNAME)

    vistoid2 = ""
    vistotipo2 = "0"

    listavideos.reverse()
    listavideos2 = []

    for video in listavideos:
        tipovisto = ""
        if len(listavistos)>0:
            vistoid = vistoid2
            if vistoid2<>"":
                tipovisto="1A"
            formato = ""
            OK="0"                
            for visto in listavistos:
                if urlOK=="-1" and video[0]==visto[1]:
                    OK="-1"
                if urlOK=="0" and video[0]==visto[1] and video[1]==visto[2]:
                    OK="-1"
                if OK=="-1":
                    tipovisto = visto[5]
                    if visto[5]=="1":
                        if vistoid2=="":
                            vistoid = "[LW]"
                            vistoid2 = "[W]"
                    elif visto[5]=="2":
                        if vistotipo2=="0":
                            vistoid = "[LW]"
                            vistotipo2 = "-1"
                    elif visto[5]=="3":
                        vistoid = "[W]"
                        if vistoid2<>"":
                            tipovisto="31"
                    elif visto[5]=="4":
                        vistoid = "[NW]"
                        if vistoid2<>"":
                            tipovisto="41"
                    elif visto[5]=="5":
                        vistoid = "[UW]"
                        if vistoid2<>"":
                            tipovisto="51"
                    elif visto[5]=="0":
                        vistoid = ""
                        if vistoid2<>"":
                            tipovisto="01"
                    break
            if vistoid<>"":
                formato="  -  "
            tituloW = video[0]+formato+vistoid                            
        else:
            tipovisto = "N"
            tituloW = video[0]
        listavideos2.append([ video[0] , video[1] , video[2] , tituloW , tipovisto ])

    listavideos2.reverse()
    for video in listavideos2:
        addvideofolder( CHANNELNAME , "episodiomenu" , category+";"+url+";"+video[4]+";"+paramsback['title']+";"+paramsback['titleinfo']+";"+paramsback['tcsearch']+";"+paramsback['titleerdm']+";"+paramsback['thumbnail']+";"+paramsback['plot']+";"+titleserievisto+";"+video[0]+";"+autor+";"+urlOK , video[2] , title+" - "+video[3] , video[1] , thumbnail , plot )

    if "friki100" in autor:
        OKup = "0"
        # Extrae la fecha de la pr�xima actualizaci�n
        update = re.search('<font color="#ff0000"><b><font size="3">([^<]+)<',data)
        if (update):
            OKup = "-1"
        else:
            update = re.search('<span style=\'color: \#ff0000\'><strong class=\'bbc\'><span style=\'font-size: 15px;\'>([^<]+)</span>',data)
            if (update):
                OKup = "-1"
        if OKup=="-1":
            additem( CHANNELNAME , category , update.group(1) , "" , "" , plot )                    
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",listupdate,True)
    # ------------------------------------------------------------------------------------

def astrodata(title,url):
    data = ""

    if title == "Conan, el ni�o del futuro":    
        inicios = "fichaconan.jpg"
        fins = "fichacampeones.jpg"
    if title == "Campeones (Oliver y Benji)":    
        inicios = "fichacampeones.jpg"
        fins = "holmesficha.jpg"
    if title == "Sherlock Holmes":    
        inicios = "holmesficha.jpg"
        fins = "fichamaple.jpg"
    if title == "La Aldea del Arce":    
        inicios = "fichamaple.jpg"
        fins = "fichabebop.jpg"
    if title == "Cowboy Bebop":    
        inicios = "fichabebop.jpg"
        fins = "fichaponyo.jpg"
    if title == "Ponyo en el acantilado":    
        inicios = "fichaponyo.jpg"
        fins = "</div>"

    # ------------------------------------------------------
    # Descarga la p�gina
    # ------------------------------------------------------
    try:
        data = scrapertools.downloadpage(url)
    except:
        return data

    # ------------------------------------------------------
    # Extrae la serie
    # ------------------------------------------------------
    patronvideos = inicios+'(.*?)'+fins
    matches = re.compile(patronvideos,re.DOTALL).search(data)
    if (matches):
        data = matches.group(1)

    return data

def erdmdata(url):
    data = ""
    plot = ""

    # ------------------------------------------------------
    # Descarga la p�gina
    # ------------------------------------------------------
    try:
        data = scrapertools.downloadpage(url)
    except:
        return data,plot

    # ------------------------------------------------------
    # Busca la release
    # ------------------------------------------------------
    matchR0 = re.match('.*?#(\d+)$',url)
    if (matchR0):
        post = matchR0.group(1)    
        patronvideos = 'name="'+post+'">#</a>(.*?)<!-- / message -->'
        matches = re.compile(patronvideos,re.DOTALL).search(data)
        if (matches):
            data = matches.group(1)
        
    # ------------------------------------------------------
    # Extrae informaci�n del contenido, de su p�gina
    # ------------------------------------------------------        
    match6 = re.search('(Genero|G�nero)\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match6):
        plot = "G�nero: "+re.sub('\<.*?\>','',match6.group(2))+". "
    match7 = re.search('Episodios\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match7):
        plot = plot+"Episodios: "+re.sub('\<.*?\>','',match7.group(1))+". "
    match8 = re.search('(Duraci�n|Duracion)\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match8):
        plot = plot+"Duraci�n: "+re.sub('\<.*?\>','',match8.group(2))+". "
    match9 = re.search('A�o\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match9):
        plot = plot+"A�o: "+re.sub('\<.*?\>','',match9.group(1))+". "
    match10 = re.search('Idioma\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match10):
        plot = plot+"Idioma: "+re.sub('\<.*?\>','',match10.group(1))+". "
    match11 = re.search('Subt(?:�|i)tulos\:(.*?)(</tr>|<br />)',data,re.IGNORECASE)
    if (match11):
        plot = plot+"Subt�tulos: "+re.sub('\<.*?\>','',match11.group(1))+"."

    return data,plot
    
def findvideos(data,title):
    encontrados = set()
    devuelve = []

    # Extrae los enlaces a los v�deos - Megaupload - V�deos con t�tulo - Skait
    patronvideos  = '(<br /><b>|<br />)\s([^<]+)<br />\s'
    patronvideos += '<a href\="http\:\/\/www.megaupload.com/\?d\=([^"]+)" target="_blank">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]
        titulo = titulo.replace(' -  ' , '')
        titulo = titulo.replace(' - Ovas ' , ' Ovas')

        url = match[2]

        if url not in encontrados:
            devuelve.append( [ titulo , url , 'Megaupload' ] )
            encontrados.add(url)

    # Extrae los enlaces a los v�deos - Megaupload - V�deos con t�tulo
    patronvideos = '(\d\d\.\-\s<a|<a) href\=(?:\"|\')?http\:\/\/www.megaupload.com(?:\/es\/|\/)\?d\=(\w+)[^>]*>(<br[^<]+<img[^>]+>.*?|<img[^>]+>.*?|.*?)(?:</?a>|<img|</a<|</tr>)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:

        # Titulo quita c�digo html
        titulo = re.sub('\<.*?\>','',match[2])
        titulo = re.sub('^\s+','',titulo)
        titulo = re.sub('\s+$','',titulo)
        titulo = formatostring(titulo)
        
        # url
        url = match[1]

        # Sailor Moon
        foro = ""
        if title == "Sailor Moon":
            match0 = re.match('(\d\d\.\-\s)<a',match[0])
            if (match0):
                titulo = match0.group(1)+titulo
                foro = "AT"
            if titulo == "01.- La ni�a llorona se convierte en guerrero":
                titulo = titulo+" - VO (Japon�s)"
            match2 = re.match('\d',titulo)
            if match2 is None and foro=="AT":
                url = ""
        
        # Cross Game
        if title == "Cross Game":
            match1 = re.match('\[Rakuen~SnF\] Cross Game HDTV (\d{2,4})$',titulo,re.IGNORECASE)
            if (match1):
                titulo = match1.group(1)+ " - HDTV [Rakuen~SnF]"

        # Kochikame
        if title == "Kochikame":
            if titulo[0:3] == "Cap":
                titulo = titulo[9:]
            if titulo[0:3] == "000":
                url = ""

        # Identifica un tipo de formato con el t�tulo de la serie en el enlace y el id del episodio fuera.
        parte = ""
        match4 = re.match('(\s*\[TeU\-F\]|'+title+'[^\w]*$)',titulo,re.IGNORECASE)
        if (match4):
            parte = "-2"
        
        # Elimina el t�tulo de la serie del t�tulo del episodio (si aparece al ppio o al final)
        if parte <> "-2":
            titulo = re.sub('[^\w\]\)\"\']*'+title+'[^\w]*$','',titulo)
            titulo = re.sub('^'+title+'[^\w\[\(\"\']*','',titulo)
            titulo = re.sub('^1\[','[',titulo)
            
        # Identifica los videos en partes y sin t�tulo
        titulo0 = ""
        match3 = re.match('\s*(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\)|Dnf.*?)\s*$',titulo,re.IGNORECASE)
        if (match3):
            parte = "-1"
    
        # Busca el t�tulo para los casos anteriores
        if parte <> "":
            match7 = re.search('<img src="[^"]+"[^>]*>\s*(<font color=[^>]+>[^<]+<b>|<a href=[^>]+>[^<]+<b>(?:[^<]+</b></a>|[^<]+)|[^<]+<b>[^<]+</b>|[^<]+)(?:<font color="[^"]+"><i>[^<]+</i></font></font>|</font>|\s*)(?:</td><td align="right">\s*|\s*)<a href\="?http\:\/\/www.megaupload.com(\/es\/|\/)\?d\='+url,data,re.IGNORECASE)
            if (match7):
                    titulo0 = re.sub('\<.*?\>','',match7.group(1))
                    titulo0 = re.sub('^\s+','',titulo0)
                    titulo0 = re.sub('\s+$','',titulo0)
                    titulo0 = formatostring(titulo0)
                    titulo = titulo0+" "+titulo
            else:
                match5 = re.search('<img src="[^"]+"[^>]*>\s*((?:<font color="[^"]+">[^<]*|[^<]+<b>)\s*.*?)<a href\="?http\:\/\/www.megaupload.com(?:\/es\/|\/)\?d\=\w+(?<='+url+')',data,re.IGNORECASE)
                if (match5):
                    search0 = match5.group(1)
                    # Busca si no se trata de la 1� parte (el resto se modifican m�s abajo por si la 1� parte tiene titulo)
                    match6 = re.search('<a href\="?http\:\/\/www.megaupload.com',search0,re.IGNORECASE)
                    if match6 is None:
                        titulo0 = re.sub('\<.*?\>','',search0)
                        titulo0 = re.sub('^\s+','',titulo0)
                        titulo0 = re.sub('\s+$','',titulo0)
                        titulo0 = formatostring(titulo0)
                        titulo = titulo0+" "+titulo

        if url not in encontrados and url <> "":
            devuelve.append( [ titulo , url , 'Megaupload' , parte , titulo0 ] )
            encontrados.add(url)
            if parte == "-1" and titulo0 == "":
                n = devuelve.index([ titulo , url , 'Megaupload' , parte , titulo0 ])
                if devuelve[n-1][3] == "-1" and devuelve[n-1][4] <> "":
                    devuelve[n][0] = devuelve[n-1][4]+" "+devuelve[n][0]
                    devuelve[n][4] = devuelve[n-1][4]
                # Caso en que el que la 1� parte tiene t�tulo
                if devuelve[n-1][3] == "":
                    match32 = re.match('(.*?)(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\))\s*$',devuelve[n-1][0],re.IGNORECASE)
                    if (match32):
                        devuelve[n][0] = match32.group(1)+devuelve[n][0]
                        devuelve[n][4] = match32.group(1)
                # Caso
                if devuelve[n-1][3] == "-2":
                    match22 = re.match('(.*?)(?:\[.*?\]|\(?\s*Parte?\s*(?:\d+|\[[^\]]+\])\s*\)?|RAW|\(\d{1,2}\/\d{1,2}\)|\[TeU-F\].*?)\s*$',devuelve[n-1][0],re.IGNORECASE)
                    if (match22):
                        devuelve[n][0] = match22.group(1)+devuelve[n][0]
                        devuelve[n][4] = match22.group(1)
            

    return devuelve

def finderdm(url,tipolist,tipocontenido,search,idioma):
    serieslist = []

    try:
        data = scrapertools.downloadpage(url)
    except:
        alertnoresultados(url)
        return serieslist

    tipocontenido = tipocontenido.lower()
    tipocontenido = re.sub('pel(?:�|i)cula','Pel(?:�|i)cula',tipocontenido)
    tipocontenido = re.sub('web','(?:Ova|Web)',tipocontenido)

    if tipolist == "Emision":
        tipolist = "<td class=Em>"
    else:
        tipolist = "<td class=\w+>"
    if search == "#":
        search = "[^a-zA-Z]"
    
    patronvideos  = '<a href=([^\s]+)\sclass=\w+>('+search+'[^<]*)<span class=mt>([^<]+)</span>'
    patronvideos += '</a></td><td>('+tipocontenido+')</td><td>([^<]+)</td>('+tipolist+')</td>'
    matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

    for match in matches:
        # Titulo
        titulo = match[1]
        titulo = titulo.replace('&amp;' , '&')
        titulo = titulo.replace('&quot;' , '"')
        titulo = titulo.replace('&#33;' , '!')
        titulo = re.sub('\s+$','',titulo)

        # Titulo para b�squedas
        titleerdm = ftitleerdmsearch(titulo)
                
        # AnexoTitulo/idioma
        anextitulo = match[2]
        anextitulo = anextitulo.replace('&amp;' , '&')
        anextitulo = anextitulo.replace('&quot;' , '"')
        anextitulo = anextitulo.replace('&#33;' , '!')

        # URL
        url = urlparse.urljoin("http://www.elrincondelmanga.com/foro/",match[0])

        # Contenido
        contenido = match[3]

        # Capitulos
        capitulos = match[4]
        
        # En emisi�n
        enemision = ""
        if tipolist == "<td class=Em>":
            enemision = " [En Emisi�n]"
        elif match[5] == "<td class=Co>":
            enemision = " [Terminada]"
        elif match[5] == "<td class=Em>":
            enemision = " [En Emisi�n]"
        elif match[5] == "<td class=Fa>":
            enemision = " [Fansubing]"
        elif match[5] == "<td class=Up>":
            enemision = " [Uploading]"
        elif match[5] == "<td class=De>":
            enemision = " [Detenida]"

        if idioma == "Espa�ol":
            match2 = re.search('(Esp|esp|Castellano|Lat|lat)',anextitulo)
            if (match2):
                pass
            else:
                continue
        
        serieslist.append( [ titulo , anextitulo , capitulos , enemision , url , contenido , titleerdm ] )
    
    return serieslist

def searchvistos(params,url,category):
    listaseries = []
    respuesta = ""

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Espere por favor...'
    Dialogespera.create('pelisalacarta' , line1 , '' )

    if os.path.exists(casttv.WANF_FILE):
        listaseries,update = casttv.readtmplist(casttv.WANF_FILE,"-2")
        if update=="3":
            respuesta = casttv.alertreturnfav(category,update)
            if respuesta:
                respuesta="-1"
        if len(listaseries)>0 and update<>"3":
            casttv.writetmplist(casttv.WANF_FILE,listaseries,"3","")
    if len(listaseries)==0 or respuesta=="-1":
        listaseries = findvistos(category)
        Dialogespera.create('pelisalacarta' , line1 , '' )

    if len(listaseries)==0:
        casttv.writetmplist(casttv.WANF_FILE,listaseries,"-2","")
        alertnoresultadosearch()
        return 

    for serie in listaseries:
        adderdmfolder( CHANNELNAME , "listadosvistos" , category , serie[0] , serie[1] , serie[2] , serie[3] , serie[4] , serie[5] , serie[6] )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,False)
    # ------------------------------------------------------------------------------------

def findvistos(category):
    listaseries = []
    listaseries2 = []
    listavistos2 = []
    searcherdm = ""

    listavistos = casttv.readvisto("","",CHANNELNAME)
    if len(listavistos)==0:
        return listavistos

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Buscando informaci�n de "'+category+'"...'
    Dialogespera.create('pelisalacarta' , line1 , '' )

    listadoseries = astroteamrglist()
    #tusdivx = tusdivxlist()
    #listadoseries.extend(tusdivx)
    for visto in listavistos:
        encontrado="0"
        for serie in listadoseries:
            if visto[0]==serie[0]:
                encontrado="-1"
                if serie[4]=="":
                    serie[4]=serie[0]
                if listaseries.count(serie)==0:
                    listaseries.append(serie)
                break
        if encontrado=="0":
            listavistos2.append(visto)
    if len(listavistos2)>0:
        for visto in listavistos2:
            matchurl = re.match('^([^\/]+)(\/.*?)$',visto[0])
            if (matchurl):
                title = matchurl.group(1)
                titleinfo = title
                tcsearch = ""
                if "showthread" in matchurl.group(2):
                    urlvisto = "http://www.elrincondelmanga.com/foro"+matchurl.group(2)
                    titleerdm = "eRdM"
                    titlesearch=re.sub('[\\\\]?(?P<signo>[^\w\s\\\\])','\\\\\g<signo>',title)
                    if searcherdm=="":
                        searcherdm=titlesearch
                    else:
                        searcherdm=searcherdm+"|"+titlesearch
                else:
                    urlvisto = "http://www.mcanime.net/descarga_directa/anime/detalle"+matchurl.group(2)
                    titleerdm = "mc-anime-fav"
                    matchinfo = re.match('^([^\(]+)\s\((.*?)\)$',matchurl.group(1))
                    if (matchinfo):
                        titleinfo = matchinfo.group(1)
                        tcsearch = matchinfo.group(2)
                if listaseries.count([ title , urlvisto , "" , "" , titleinfo , tcsearch , titleerdm ])==0:
                    listaseries.append([ title , urlvisto , "" , "" , titleinfo , tcsearch , titleerdm ])

    if len(listaseries)==0:
        return listaseries

    if searcherdm<>"":
        searcherdm = re.sub('&','&(?:amp;)?',searcherdm)
        searcherdm = re.sub('\\\\"','(?:\\\\"|&quot;)',searcherdm)
        searcherdm = re.sub('\\\\!','(?:\\\\!|&#33;)',searcherdm)
        searcherdm="(?:"+searcherdm+")"
        listaerdm = finderdm(urleRdM,"Completo","[^<]+",searcherdm,"")
        if len(listaerdm)==0:
            alertnoweb("El Rinc�n del Manga")
        else:
            listaerdm.sort(key=lambda erdm: erdm[0].lower())

    OKmca="-1"
    for serie in listaseries:
        listafav = casttv.readfav(serie[0],serie[1],"",CHANNELNAME)
        if len(listafav)==0:
            if serie[6]<>"eRdM" and serie[6]<>"mc-anime-fav":
                listaseries2.append(serie)
                continue
            elif serie[6]=="mc-anime-fav":
                if OKmca=="0":
                    continue
                try:
                    datamca = scrapertools.downloadpage(serie[1])
                except:
                    alertnoresultados(serie[1])
                    try:
                        scrapertools.downloadpage("http://www.mcanime.net")
                    except:
                        alertnoweb("McAnime")
                        OKmca="0"
                    continue
                matchstatus = re.search('<h3>([^<]+)</h3>',datamca)
                if (matchstatus):
                    serie[0] = serie[0]+"  -  "+matchstatus.group(1)
                listaseries2.append(serie)
                continue
            for erdm in listaerdm:            
                if serie[0]==erdm[0] and serie[1]==erdm[4]:
                    serie[0] = serie[0]+"  -  "+erdm[1]+" ["+erdm[5]+"]"+" ["+erdm[2]+"]"+erdm[3]
                    serie[4] = erdm[0]
                    serie[5] = erdm[5]
                    serie[6] = erdm[6]
                    serie[3] = "eRdM"
                    listaseries2.append(serie)
                    break
    if len(listaseries2)==0:
        return listaseries2
    listaseries = listaseries2
    listaseries.sort()

    casttv.writetmplist(casttv.WANF_FILE,listaseries,"3","")
    return listaseries

def listadosvistos(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    titleback = title
    titleinfo = urllib.unquote_plus( params.get("titleinfo") )
    plot = urllib.unquote_plus( params.get("plot") )
    tcsearch = urllib.unquote_plus( params.get("tcsearch") )
    titleerdm = urllib.unquote_plus( params.get("titleerdm") )
    if titleerdm<>"mc-anime-fav":
        match = re.match('^(.*?)\s+\-\s+(.*?)$',title)
        if (match):
            titleinfo2 = match.group(1)
            status = match.group(2)    
        else:
            titleinfo2 = title
            status = tcsearch
    else:
        status = re.sub('^.*?\s+\-\s+','',title)
        titleinfo2 = titleinfo+" ("+tcsearch+")"
        title = titleinfo

    respuesta = casttv.serieupdate(titleinfo2,status,url,tcsearch,CHANNELNAME)

    if respuesta<>1 and respuesta<>2 and respuesta<>3 and respuesta<>4:
        category = category+" - "+titleinfo
        category = re.sub('(?:\s+\(.*?\)\s+\[Mirror.*\]$|\s+\(.*?\)$)','',category)
        detail(title,url,category,titleinfo,tcsearch,titleerdm,"",plot,False)
    else:
        #respuesta2 = casttv.alertreturnfav(category,"2")
        #if respuesta2:
        #    pass
        #else:
        series,update = casttv.readtmplist(casttv.WANF_FILE,"2")
        if respuesta==1:
            eliminar=[]
            for serie in series:
                if serie[0]==titleback and serie[1]==url:
                    eliminar=serie
                    break
            if len(eliminar)>0:
                series.remove(eliminar)
        casttv.writetmplist(casttv.WANF_FILE,series,"2","")

def searcherdm(params,url,category):
    searcherdmupdate(-2,"",category,"[^<]+","Completo","",False)

def searcherdmupdate(seleccion,tecleado,category,tipocontenido,tipolist,idioma,listupdate):
    letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    search = ""
    rtdos = 0
    back = "-1"
        
    if seleccion == -2:
        back = "0"
        opciones = []
        opciones.append("Mostrar Todo")
        opciones.append("Teclado (Busca en T�tulo y datos anexos)")
        for letra in letras:
            opciones.append(letra)
        searchtype = xbmcgui.Dialog()
        seleccion = searchtype.select("B�squeda por Teclado o por Inicial del T�tulo:", opciones)
    if seleccion == -1 :return
    if seleccion <> 1 and back <> "-1":
        tipocontenido = searchmctc()
        tipolist,idioma = searchmctl(tipocontenido)
        category = fcategory(tipocontenido,tipolist,idioma)

    if seleccion == 1:
        if len(tecleado)==0:
            keyboard = xbmc.Keyboard('')
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                tecleado = keyboard.getText()
                tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
                if len(tecleado)>0:
                    tipocontenido = searchmctc()
                    tipolist,idioma = searchmctl(tipocontenido)
                    category = fcategory(tipocontenido,tipolist,idioma)
                    category = category+" - Buscar"                
                    if len(tecleado) == 1:
                        search = tecleado            
            if keyboard.isConfirmed() is None or len(tecleado)==0:
                return
        if len(tecleado)==1:
            category = category+" - Buscar"
            search = tecleado
    
    if seleccion > 1:
        search = letras[seleccion-2]
        category = category+" - Buscar - "+letras[seleccion-2]

    listaseries = finderdm(urleRdM,tipolist,tipocontenido,search,idioma)

    if len(listaseries)==0:
        alertnoresultadosearch()
        return

    listafav = casttv.readfav("","","",CHANNELNAME)

    listaseries.sort(key=lambda serie: serie[0].lower())
    for serie in listaseries:
        foldertitle = serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3]
        if len(tecleado)>1:
            match = re.search(tecleado,foldertitle,re.IGNORECASE)
            if (match):
                pass
            else:
                continue
        thumbnail=""
        if len(listafav)>0:
            for fav in listafav:
                if serie[0]==fav[0] and serie[4]==fav[2]:
                    if fav[3]=="1":
                        thumbnail=casttv.STARGREY_THUMB
                        break
                    thumbnail=casttv.STARORANGE_THUMB
                    break
        if tipolist=="Completo":
            if tipocontenido == "[^<]+":
                titulo = foldertitle
            else:
                if tipocontenido == "Pelicula":
                    titulo = serie[0]+"  -  "+serie[1]
                else:
                    titulo = serie[0]+"  -  "+serie[1]+" ["+serie[2]+"]"+serie[3]
        else:
            if tipocontenido == "[^<]+":
                titulo = serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"
            else:
                titulo = serie[0]+"  -  "+serie[1]+" ["+serie[2]+"]"

        adderdmfolder( CHANNELNAME , "listadoserdmsearch" , str(seleccion)+";"+tecleado+";"+tipocontenido+";"+tipolist+";"+idioma , titulo , serie[4] , thumbnail , "eRdM" , serie[0] , serie[5] , serie[6] )

    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",listupdate,True)
    # ------------------------------------------------------------------------------------

def listados(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    titleback = title
    plot = urllib.unquote_plus( params.get("plot") )
    status = ""
    titleerdm = ""
    if params.has_key("titleerdm"):
        titleinfo = urllib.unquote_plus( params.get("titleinfo") )
        tcsearch = urllib.unquote_plus( params.get("tcsearch") )
        titleerdm = urllib.unquote_plus( params.get("titleerdm") )
        if titleerdm<>"mc-anime-fav":
            match = re.match('^(.*?)\s+\-\s+(.*?)$',title)
            if (match):
                titleinfo2 = match.group(1)
                status = match.group(2)    
            else:
                titleinfo2 = title
                status = tcsearch
    if params.has_key("info1"):
        matchcat = re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',category)
        category = matchcat.group(1)
        titleinfo2 = matchcat.group(2)
        status = matchcat.group(3)
        title = matchcat.group(4)
        tcsearch = matchcat.group(5)
    if titleerdm=="mc-anime-fav":
        status = re.sub('^.*?\s+\-\s+','',title)
        titleinfo2 = titleinfo+" ("+tcsearch+")"
        title = titleinfo
    #elif titleerdm=="mc-anime-list":
    #    titleinfo2 = titleinfo+" ("+tcsearch+")"
    #    status = tcsearch
    #    titleerdm = "mc-anime-fav"
    
    if category=="AstroteamRG" or category=="Anime" or params.has_key("info1"):
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    else:
        thumbnail = ""

    respuesta = casttv.serieupdate(titleinfo2,status,url,tcsearch,CHANNELNAME)

    if respuesta<>1 and respuesta<>2 and respuesta<>3 and respuesta<>4:
        if "Fav" in category:
            favnoupdate(category,"1")
            category = re.sub('^Todos ','',category)
        if params.has_key("titleerdm"):
            detail(title,url,category,titleinfo,tcsearch,titleerdm,thumbnail,plot,False)
        else:
            info1 = urllib.unquote_plus( params.get("info1") )
            info2 = urllib.unquote_plus( params.get("info2") )    
            info3 = urllib.unquote_plus( params.get("info3") )
            info4 = urllib.unquote_plus( params.get("info4") )
            info5 = urllib.unquote_plus( params.get("info5") )
            info = info1+"|"+info2+"|"+info3+"|"+info4+"|"+info5
            detail(title,url,category,info,tcsearch,"mc-anime",thumbnail,plot,False)
    elif "Fav" in category:
        #category = re.sub('\s\-\s.*?$','',category)
        #respuesta2 = casttv.alertreturnfav(category,"0")
        #if respuesta2:
        #    pass
        #else:
        listanime,nuevos,update = casttv.readtmplist(casttv.FAVANF_FILE,"0")
        if len(nuevos)>0:
            nuevosep = "-1"
        else:
            nuevosep = "0"
        eliminar=[]
        if respuesta==1 or respuesta==2:
            for anime in listanime:
                if anime[1]==titleback and anime[2]==url:
                    if respuesta==2:
                        if anime[3]==casttv.STARGREY_THUMB:
                            anime[3]=casttv.STARORANGE_THUMB
                        else:
                            anime[3]=casttv.STARGREY_THUMB
                    else:
                        eliminar=anime
                    break
        if len(eliminar)>0:
            listanime.remove(eliminar)
        casttv.writetmplist(casttv.FAVANF_FILE,listanime,"0",nuevosep)
        favnoupdate(category,"0")

def favnoupdate(category,value):
    if value<>"0":
        listanime,nuevos,update = casttv.readtmplist(casttv.FAVANF_FILE,value)
        if len(nuevos)>0:
            nuevosep = "-1"
        else:
            nuevosep = "0"
        casttv.writetmplist(casttv.FAVANF_FILE,listanime,value,nuevosep)
    if "Todos" in category or "Anime" in category:
        series,seriesnuevos,update = casttv.readtmplist(casttv.FAVCTV_FILE,value)
        if len(seriesnuevos)>0:
            nuevosep = "-1"
        else:
            nuevosep = "0"
        casttv.writetmplist(casttv.FAVCTV_FILE,series,value,nuevosep)

def nuevosnoupdate(category,value):
    if value<>"2":
        animenuevos,update = casttv.readtmplist(casttv.NEWANF_FILE,value)
        casttv.writetmplist(casttv.NEWANF_FILE,animenuevos,value,"")
    if "Todos" in category:
        nuevos,update = casttv.readtmplist(casttv.NEWCTV_FILE,value)
        casttv.writetmplist(casttv.NEWCTV_FILE,nuevos,value,"")

def listadoserdmsearch(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    titleinfo = urllib.unquote_plus( params.get("titleinfo") )
    plot = urllib.unquote_plus( params.get("plot") )
    tcsearch = urllib.unquote_plus( params.get("tcsearch") )
    titleerdm = urllib.unquote_plus( params.get("titleerdm") )
    status = ""
    match = re.match('^(.*?)\s+\-\s+(.*?)$',title)
    if (match):
        titleinfo = match.group(1)
        status = match.group(2)
    match1 = re.match('^(\d+);([^;]*);([^;]*);([^;]*);([^;]*)$',category)
    seleccion = int(match1.group(1))
    tecleado = match1.group(2)
    tipocontenido = match1.group(3)
    tipolist = match1.group(4)
    idioma = match1.group(5)
    category0 = fcategory(tipocontenido,tipolist,idioma)

    respuesta = casttv.serieupdate(titleinfo,status,url,tcsearch,CHANNELNAME)

    if respuesta==1 or respuesta==2 or respuesta==3 or respuesta==4:
        searcherdmupdate(seleccion,tecleado,category0,tipocontenido,tipolist,idioma,True)
    else:
        category = "El Rinc�n del Manga - "+titleinfo
        detail(title,url,category,titleinfo,tcsearch,titleerdm,"",plot,False)

def listadonuevos(params,url,category):
    nuevos = []
    seriesnuevos=[]
    category2 = re.sub(r".*?\s\-\s([^\-]+)$",lambda micat: micat.group(1),category)
    respuesta=""

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Espere por favor...'
    Dialogespera.create('pelisalacarta' , line1 , '' )

    favnoupdate(category,"1")

    if os.path.exists(casttv.NEWANF_FILE):
        nuevos,update = casttv.readtmplist(casttv.NEWANF_FILE,"-2")
        if update=="3":
            if len(nuevos)==0 and "Todos" not in category:
                pass
            else:
                respuesta = casttv.alertreturnfav(category2,update)
                if respuesta:
                    respuesta="-1"
        if len(nuevos)>0 and update<>"3":
            casttv.writetmplist(casttv.NEWANF_FILE,nuevos,"3","")
    if len(nuevos)==0 or respuesta=="-1":
        nuevos = findlistadonvos(category,category2)
        Dialogespera.create('pelisalacarta' , line1 , '' )

    if "Todos" in category:
        tipo = 4
        if os.path.exists(casttv.NEWCTV_FILE):
            seriesnuevos,update = casttv.readtmplist(casttv.NEWCTV_FILE,"-2")
            if len(seriesnuevos)>0 and update<>"3":
                casttv.writetmplist(casttv.NEWCTV_FILE,seriesnuevos,"3","")
        if len(seriesnuevos)==0 or respuesta=="-1":
            seriesnuevos = casttv.findlistadonvos(category2)
            Dialogespera.create('pelisalacarta' , line1 , '' )

    if len(nuevos)==0 and len(seriesnuevos)==0:
        casttv.alertnoepisodios(4)
        return

    if "Todos" in category and len(nuevos)>0:
        additem( CHANNELNAME , category , "------------------------------------- ANIME - FOROS -------------------------------------" , "" , "" , "" )
    for item in nuevos:
        addvideofolder( CHANNELNAME , "episodiomenu" , item[0] , item[1] , item[2] , item[3] , "" , "" )

    if len(seriesnuevos)>0:
        additem( CHANNELNAME , category , "--------------------- CASTTV - TVSHACK - SERIESYONKIS ---------------------" , "" , "" , "" )
        for item in seriesnuevos:
            casttv.addnewfolder( CHANNELNAME , "casttv.episodiomenu" , category , item[0] , item[1] , item[2] , "" , item[3] , item[4] , item[5] , item[6] , item[7] , item[8] , item[9] , ";" , "New" )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,False)
    # ------------------------------------------------------------------------------------

def findlistadonvos(category,category2):
    listafav = casttv.readfav("","","-1|-2",CHANNELNAME)
    nuevos = []

    if len(listafav)==0:
        casttv.writetmplist(casttv.NEWANF_FILE,nuevos,"3","")
        return nuevos

    Dialogespera = xbmcgui.DialogProgress()
    line1 = 'Buscando "'+category2+'":'
    Dialogespera.create('pelisalacarta' , line1 , '0%  -  ')

    total = len(listafav)
    i,j,n,m = casttv.progreso(total)
    for serie in listafav:
        if i>=n:
            i=0
            j=j+m
        if j>=100:
            j=95
        Dialogespera.update(j, line1 , str(j)+'%  -  '+serie[0] )
        i=i+1

        #T�tulo Anime en Vistos
        titleserievisto = serie[0]
        matchurl2 = re.search('(?:\/showthread.php\?t[^\/]+|\/[^\/]+\/\d+)$',serie[2])
        if (matchurl2):
            titleserievisto = titleserievisto+matchurl2.group(0)

        #T�tulo Anime
        title = serie[0]

        #Web y urlOK
        web = ""
        urlOK="-1"
        if "mcanime" in serie[2]:
            matchtitle=re.match('^([^\(]+)\s\(.*?\)$',serie[0])
            if (matchtitle):
                title = matchtitle.group(1)
            web = "mc-anime"
            urlOK="0"
        elif "astroteam" in serie[2]:
            matchtitle1=re.search('\(by Chihiro\)$',serie[0],re.IGNORECASE)
            if (matchtitle1):
                web = "astro"
            else:
                web = "astro2"
        elif "tusdivx" in serie[2]:
            web = "tusdivx"

        if web<>"mc-anime":
            title = re.sub('(?:\s+VOSE|\s*\-*\s+\[.*\]|\s+\(by \w+\)\s+\[Mirror.*\]$|\s+\(by \w+\)$|\s+$)','',title)

        listanuevos=findnuevos(category,title,titleserievisto,serie[2],"-1",web)
        if len(listanuevos)>0:
            if serie[3]=="-2" and len(listanuevos)>3:
                listanuevos0 = listanuevos
                listanuevos = [ listanuevos0[0] , listanuevos0[1] , listanuevos0[2] ]
            nuevos.extend(listanuevos)
    casttv.writetmplist(casttv.NEWANF_FILE,nuevos,"3","")
    return nuevos

def fcategory(tipocontenido,tipolist,idioma):
    if tipocontenido<>"[^<]+":
        category = "El Rinc�n del Manga - "+tipocontenido+"s - "+tipolist+idioma
    else:
        category = "El Rinc�n del Manga - "+tipolist+idioma
    category = re.sub('ls','les',category)
    category = re.sub('CompletoEspa�ol','Espa�ol/Dual',category)
    category = re.sub('Completo$','Listado Completo',category)
    category = re.sub('Emision$','En Emisi�n',category)            

    return category    

def findinfo(data,title,tcsearch,todos,genre,titleerdm):
    animemclist = []
    listinfomc = []
    infoencontrada = []
    url = genre
    tcsearch = tcsearch.lower()
    tcsearch = re.sub('pel(?:�|i)cula','Pel(?:�|i)cula',tcsearch)
    tcsearch = re.sub('ova','(?:Ova|Web)',tcsearch)

    # Inicial
    inicial = "#"
    titleinicial = finicialformca(title)
    match0 = re.match('(?:The\s+|Las?\s+|Los\s+|An?\s+|[^\w\#]*)(\w|\#)',titleinicial,re.IGNORECASE)
    if (match0):
        inicial = match0.group(1)
    
    if url == "":
        match01 = re.match('[^a-zA-Z]',inicial)
        if (match01):
            url = "http://www.mcanime.net/enciclopedia/anime/lista/9"
        else:
            url = urlparse.urljoin("http://www.mcanime.net/enciclopedia/anime/lista/",inicial.lower())
        try:
            data = scrapertools.downloadpage(url)
        except:
            alertnoresultados(url)
            return animemclist
    else:
        try:
            data0 = scrapertools.downloadpage(url)
        except:
            alertnoresultados(url)
            return animemclist

        if len(title)==1:
            patronvideos = '<div class="letter">'+inicial.upper()+'</div>.*?<a name="\w">'
            match03 = re.compile(patronvideos,re.DOTALL).search(data0)
            if (match03):                
                data = match03.group(0)
        else:
            data = data0    

    patronvideos = '<a href\=\"([^\"]+)\">(?:<b>|\s*)([^<]+)(?:</b></a>|</a>)\s*<i>(\('+tcsearch+'\))</i>\s*</h5>'
    matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

    for match in matches:
        
        # Titulo
        titlemc = match[1]
        titlemc = re.sub('\s+$','',titlemc)
        titlemc = formatostring(titlemc)
        titulomc = titlemc+" "+match[2]

        # Titulo para b�squedas
        titlemcanime = ftitlesearch(titlemc)

        # Tipo contenido
        tpcontenidomc = re.sub('(?:\(|\))','',match[2])
                        
        # url
        urlmc = urlparse.urljoin("http://www.mcanime.net/",match[0])

        animemclist.append( [ titulomc , urlmc , titlemc , tpcontenidomc , titlemcanime ] )

    if todos=="-1":

        if len(animemclist) > 0 and len(title) > 1:
            for animemc in animemclist:
                forinfo = re.search(title,animemc[2],re.IGNORECASE)
                if (forinfo):
                    infoencontrada.append(animemc)
            animemclist = infoencontrada
                
        return animemclist

    if todos=="0":
        if len(animemclist) > 0:
            itemencontrado = casttv.searchgate(animemclist,titleerdm,"","titleerdm")
            if len(itemencontrado)==1:
                titulomc2 = itemencontrado[0][0]
                urlmc2 = itemencontrado[0][1]
                listinfomc = findlistinfo("",titulomc2,urlmc2)
                
        return listinfomc

def findlistinfo(data,title,url):
    infomclist = []

    if data == "":
        data = scrapertools.downloadpage(url)

    sinopsis = ""    
    match1 = re.search('<h6>Sinopsis.*?</h6>\n\s*([^<]+)<br />',data,re.IGNORECASE)
    if (match1):
        try:
            sinopsis = unicode( match1.group(1), "utf-8" ).encode("iso-8859-1")
        except:
            sinopsis = match1.group(1)

        sinopsis = formatostring(sinopsis)

    clasf = ""    
    match2 = re.search('<b>Clasificaci\&oacute\;n\:</b>([^<]+)<br />',data,re.IGNORECASE)
    if (match2):
        try:
            clasf = unicode( match2.group(1), "utf-8" ).encode("iso-8859-1")
        except:
            clasf = match2.group(1)

        clasf = clasf.replace('Adolecentes' , 'Adolescentes')
        clasf = formatostring(clasf)

    genre = ""    
    match3 = re.search('<b>G\&eacute\;neros\:</b>(.*?)<br />',data,re.IGNORECASE)
    if (match3):
        try:
            genre = unicode( match3.group(1), "utf-8" ).encode("iso-8859-1")
            genre = re.sub('\<.*?\>','',genre)
        except:
            genre = re.sub('\<.*?\>','',match3.group(1))

        genre = re.sub('^\s+','',genre)
        genre = re.sub('\s+$','',genre)
        genre = re.sub(',\s[^\w]{5}',', ',genre)
        genre = formatostring(genre)

    contenido = ""    
    match4 = re.search('<b>Contenido\:</b>\s*([^<]+)<br />',data,re.IGNORECASE)
    if (match4):
        try:
            contenido = unicode( match4.group(1), "utf-8" ).encode("iso-8859-1")
        except:
            contenido = match4.group(1)
    
        contenido = re.sub(',\s[^\w]{5}',', ',contenido)
        contenido = formatostring(contenido)

    thumbnail = ""    
    match5 = re.search('<img src="([^"]+)"[^c]+class="title_pic"',data,re.IGNORECASE)
    if (match5):
        thumbnail = match5.group(1)

    plot = ".***MCANIME-Enciclopedia sobre "+title+". Sinopsis: "+sinopsis+". Clasificaci�n: "+clasf+". G�neros: "+genre+". Contenido: "+contenido+".--"
    try:
        plotmc = unicode( plot, "utf-8" ).encode("iso-8859-1")
    except:
        plotmc = plot

    infomclist.append([ title , clasf , genre , contenido , sinopsis , plotmc , thumbnail ])
    
    return infomclist

def findinfo2(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    title = re.sub('\s+\-\s+\[McAnime\-Enciclopedia\]','',title)
    plot = urllib.unquote_plus( params.get("plot") )
    titleinfo = urllib.unquote_plus( params.get("titleinfo") )
    titlesearch = ""
    matchtitlesearch = re.match('\w',titleinfo)
    if (matchtitlesearch):
        titlesearch = matchtitlesearch.group(0)
    titlemcanime = urllib.unquote_plus( params.get("titlemcanime") )
    tcsearch = urllib.unquote_plus( params.get("tcsearch") )
    listaseries = []
    listaseriesmc = []
    seriesencontradas = []
    genero = category

    listainfomc = findlistinfo("",title,url)

    if plot == "McAnime-Enciclopedia":
        listaseries = finderdm(urleRdM,"Completo",tcsearch,titlesearch,"")
        urltodas = re.sub('enciclopedia','descarga_directa',url)
        listaseriesmc = findseriesmc(urltodas)
            
    # A�ade al listado de XBMC
    additem( CHANNELNAME , category , listainfomc[0][0]+": Informaci�n McAnime - Enciclopedia Beta" , "" , "" , listainfomc[0][5] )
    additem( CHANNELNAME , category , "Clasificaci�n: "+listainfomc[0][1] , "" , "" , listainfomc[0][5] )
    additem( CHANNELNAME , category , "G�neros: "+listainfomc[0][2] , "" , "" , listainfomc[0][5] )
    additem( CHANNELNAME , category , "Contenido: "+listainfomc[0][3] , "" , "" , listainfomc[0][5] )
    additem( CHANNELNAME , category , "Sinopsis: "+listainfomc[0][4] , "" , "" , listainfomc[0][5] )

    if len(listaseries)>0:
        listaseries.sort(key=lambda serie: serie[6].lower())
        tituloencontrado = "0"
        tituloencontrado2 = "0"
        titlemcanimesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',titlemcanime)
        for serie in listaseries:
            titleerdm = serie[6]            
            forgenre = re.match(titlemcanimesearch+'$',titleerdm,re.IGNORECASE)
            if (forgenre):
                seriesencontradas.append(serie)
                tituloencontrado = "-1"
            else:
                forgenre1 = re.match('^'+titlemcanimesearch+'.+$',titleerdm,re.IGNORECASE)
                if (forgenre1):
                    if tituloencontrado == "-1":
                        break
                    elif tituloencontrado2 == "-1" and serie[0]<>seriesencontradas[-1][0]:
                        break
                    else:
                        seriesencontradas.append(serie)
                        tituloencontrado2 == "-1"
                                                    
        if len(seriesencontradas)>0:
            additem( CHANNELNAME , category , "Releases encontradas en El Rinc�n del Manga: " , "" , "" , "" )
            seriesencontradas.sort(key=lambda serie: serie[0].lower())
            for serie in seriesencontradas:    
                adderdmfolder( CHANNELNAME , "listados" , genero+"  -  El Rinc�n del Manga" , serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , listainfomc[0][6] , "eRdM" , serie[0] , serie[5] , serie[6] )
    
    if plot == "McAnime-Enciclopedia":
        category = category+"  -  McAnime-Enciclopedia  -  Releases"
        addsimplefolder( CHANNELNAME , "searcherdm" , "El Rinc�n del Manga  -  Anime" , "[+] Buscar en El Rinc�n del Manga", "" , "" ,"Fuente: http://www.elrincondelmanga.com/foro/showthread.php?t=75282")
    else:
        category = "McAnime-Enciclopedia"

    if len(listaseriesmc)>0:
        additem( CHANNELNAME , category , "Releases en McAnime: " , "" , "" , "" )
        for seriemc in listaseriesmc:    
            addmcarelfolder( CHANNELNAME , "listados" , genero+"  -  McAnime;"+title+";"+seriemc[0]+";"+titleinfo+";"+tcsearch , seriemc[0]+seriemc[2] , seriemc[1] , listainfomc[0][6] , listainfomc[0][5] , listainfomc[0][0]+": Informaci�n McAnime - Enciclopedia Beta" , "Clasificaci�n: "+listainfomc[0][1] , "G�neros: "+listainfomc[0][2] , "Contenido: "+listainfomc[0][3] , "Sinopsis: "+listainfomc[0][4] )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------    

def searchmc(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    plot = urllib.unquote_plus( params.get("plot") )
    category = "McAnime-Enciclopedia"
    resultado = ""
    tecleado = ""
    seriesencontradas = []
    tcsearch = "[^\)]+"
    genreurl = ""
    genre = ""
    tecseleccion = 0
    opciones = []
    letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if plot == "genreTodos":
        genre = "McAnime-Enciclopedia"
    if plot == "genre":
        opciones.append("Listado b�squeda directa en El Rinc�n del Manga")
        opciones.append("Mostrar Todos")
        tecseleccion = 2
        genreurl = url
        genre = "McAnime-Enciclopedia"
        category = title+"  -  McAnime-Enciclopedia"
    opciones.append("Teclado")
    for letra in letras:
        opciones.append(letra)
    searchtype = xbmcgui.Dialog()
    if plot == "genre":
        seleccion = searchtype.select("B�squeda por T�tulo o Inicial en McAnime-Enciclopedia:", opciones)
    else:
        seleccion = searchtype.select("B�squeda por Inicial del T�tulo en McAnime-Enciclopedia:", opciones)
    if seleccion == -1 :return
    if seleccion == 0 and tecseleccion == 2:
        inicial = searchinicial()    
    if seleccion <> tecseleccion:
        tipocontenido = searchmctc()
        if tipocontenido<>"[^<]+":
            tcsearch = tipocontenido
    if seleccion == 0 and tecseleccion == 2:
        category = unicode( title, "utf-8" ).encode("iso-8859-1")+"  -  El Rinc�n del Manga"
        listainfo = findinfo("",inicial,tcsearch,"-1",genreurl,"")
        # Cuadro de di�logo de espera
        if len(listainfo) > 300:
            respuesta = alertcontinuar(inicial,selecciontc)
            if respuesta:
                Dialogespera = xbmcgui.DialogProgress()
                resultado = Dialogespera.create('pelisalacarta' , 'Espere por favor, la b�squeda puede llevar muchos' , 'minutos...')
            else:
                return
        listaseries = finderdm(urleRdM,"Completo",tipocontenido,inicial,"")
        listaseries.sort(key=lambda serie: serie[6].lower())
        for info in listainfo:
            tituloencontrado = "0"
            tituloencontrado2 = "0"
            titlemcanimesearch = re.sub('(?<=[a-z])\d+(?=[a-z])','\d*',info[4])
            for serie in listaseries:
                tcok = "0"
                if info[3][0:3].lower()==serie[5][0:3].lower():
                    tcok = "-1"
                elif info[3][0:3].lower()=="w" and serie[5][0:3].lower()=="ova":
                    tcok = "-1"
                if seriesencontradas.count(serie)==0 and tcok=="-1":
                    titleerdm = serie[6]            
                    forgenre = re.match(titlemcanimesearch+'$',titleerdm,re.IGNORECASE)
                    if (forgenre):
                        seriesencontradas.append(serie)
                        tituloencontrado = "-1"
                    else:
                        forgenre1 = re.match('^'+titlemcanimesearch+'.+$',titleerdm,re.IGNORECASE)
                        if (forgenre1):
                            if tituloencontrado == "-1":
                                break
                            elif tituloencontrado2 == "-1" and serie[0]<>seriesencontradas[-1][0]:
                                break
                            else:
                                seriesencontradas.append(serie)
                                tituloencontrado2 == "-1"


    elif seleccion == 1 and tecseleccion == 2:
        listainfo = findinfo("","",tcsearch,"-1",genreurl,"")

    elif seleccion == tecseleccion:
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            tecleado = re.sub('[\\\\]?(?P<signo>[^#\w\s\\\\])','\\\\\g<signo>',tecleado)
            if len(tecleado)>0:
                tipocontenido = searchmctc()
                if tipocontenido<>"[^<]+":
                    tcsearch = tipocontenido
                listainfo = findinfo("",tecleado,tcsearch,"-1",genreurl,"")
        if keyboard.isConfirmed() is None or len(tecleado)==0:
            return
    else:
        listainfo = findinfo("",letras[seleccion-1-tecseleccion],tcsearch,"-1",genreurl,"")

    if len(listainfo)==0:
        alertnoresultadosearch()
        return

    if len(seriesencontradas)==0:    
        for info in listainfo:
            addmcafolder( CHANNELNAME , "findinfo2" , title , info[0]+"  -  [McAnime-Enciclopedia]" , info[1] , "" , genre , info[2] , info[3] , info[4] )
    else:
        seriesencontradas.sort(key=lambda serie: serie[0].lower())
        for serie in seriesencontradas:    
            adderdmfolder( CHANNELNAME , "listados" , category , serie[0]+"  -  "+serie[1]+" ["+serie[5]+"]"+" ["+serie[2]+"]"+serie[3] , serie[4] , "" , "eRdM" , serie[0] , serie[5] , serie[6] )
                    
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------
    if len(listainfo)>300 and resultado<>"":
        Dialogespera.close()

def searchmctc():
    selecciontctx = "[^<]+"
    opciones = []
    opciones.append("Todos  (opci�n por defecto)")
    opciones.append("Series")
    opciones.append("Ovas")
    opciones.append("Pel�culas")
    opciones.append("Especiales")
    searchtype = xbmcgui.Dialog()
    seleccion = searchtype.select("Seleccione un Tipo de Contenido:", opciones)

    if seleccion == 1:
        selecciontctx = "Serie"
    elif seleccion == 2:
        selecciontctx = "Ova"
    elif seleccion == 3:
        selecciontctx = "Pelicula"
    elif seleccion == 4:
        selecciontctx = "Especial"
    
    return selecciontctx

def searchmctl(selecciontc):
    selecciontltx = "Completo"
    idioma = ""
    opciones = []
    opciones.append("Listado Completo (opci�n por defecto)")
    opciones.append("Espa�ol/Dual")
    if selecciontc<>"Pelicula" and selecciontc<>"Especial":
        opciones.append("Actualmente en Emision")
    searchtype = xbmcgui.Dialog()
    seleccion = searchtype.select("Seleccione un Tipo de Listado:", opciones)

    if seleccion == 1:
        idioma = "Espa�ol"
    elif seleccion == 2:
        selecciontltx = "Emision"
    
    return selecciontltx,idioma

def searchinicial():
    opciones = []
    letras = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    opciones.append("Mostrar Todos  (opci�n por defecto)")
    for letra in letras:
        opciones.append(letra)
    searchtype = xbmcgui.Dialog()
    seleccion = searchtype.select("Filtrado por Inicial del T�tulo:", opciones)

    selinicial = ""    
    if seleccion > 0:
        selinicial = letras[seleccion-1]

    return selinicial

def genres(params,url,category):
    try:
        data = scrapertools.downloadpage(url)
    except:
        alertnoresultados(url)
        return

    listagenres = findgenres(data)

    addsimplefolder( CHANNELNAME , "searchmc" , category , "Todos" , "" , "" , "genreTodos" )

    for genre in listagenres:
        addsimplefolder( CHANNELNAME , "searchmc" , category , genre[0] , genre[1] , "" , "genre" )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------

def findgenres(data):
    genreslist = []

    patronvideos  = '<a\s+href="(/enciclopedia/anime/genero/[^"]+)">([^<]+)</a>'
    matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

    for match in matches:
        # G�nero
        genre = match[1]
        if genre == "Suspenso":
            genre = "Suspense"
                
        # URL
        url = urlparse.urljoin("http://www.mcanime.net",match[0])

        genreslist.append( [ genre , url ] )

    return genreslist

def findseriesmc(url):
    seriesmclist = []
    data = scrapertools.downloadpage(url)

    patronvideos  = '<li class="dd_type"><img.*?title="([^"]+)"\s*/></li>\n'
    patronvideos += '\s+<li class="dd_update">[^<]+<img[^>]+>([^<]+)</li>\n'
    patronvideos += '\s+<li class="dd_title">\n\s+<h5><a href="(/descarga_directa/anime/detalle/[^"]+)">([^<]*[^\w]MU[^\w][^<]*)</a>'
    matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

    if len(matches)==0:
        patronvideos  = '<li class="dd_type"><img.*?title="([^"]+)"\s*/></li>\n'
        patronvideos += '\s+<li class="dd_update">[^<]+<img[^>]+>([^<]+)</li>\n'
        patronvideos += '\s+<li class="dd_title">\n\s+<h5><a href="(/descarga_directa/anime/detalle/[^"]+)">([^<]+)</a>'
        matches = re.compile(patronvideos,re.IGNORECASE).findall(data)

    for match in matches:
        # Titulo
        titulo = match[3]
        titulo = formatostring(titulo)

        # Fecha Actualizaci�n
        match0 = re.search('(\d{4}).(\d{2}).(\d{2})',match[1],re.IGNORECASE)
        if (match0):
            update = match0.group(3)+"-"+match0.group(2)+"-"+match0.group(1)
        else:
            update = match[1]
        
        # Status-Actualizaci�n
        status = "  -  ["+match[0]+" ("+update+")]"
        
        # URL
        url = urlparse.urljoin("http://www.mcanime.net",match[2])

        seriesmclist.append( [ titulo , url , status] )

    return seriesmclist

def episodiomenu(params,url,category):
    title = urllib.unquote_plus( params.get("title") )
    match = re.match('^([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*);([^;]*)$',category)
    categoryback = match.group(1)
    urlback = match.group(2)
    tipovisto = match.group(3)
    titleback = match.group(4)
    titleinfo = match.group(5)
    tcsearch = match.group(6)
    titleerdm = match.group(7)
    thumbnailback = match.group(8)
    plotback = match.group(9)
    titleserievisto = match.group(10)
    titleep = match.group(11)
    autor = match.group(12)
    urlOK = match.group(13)

    seleccion,accion,detener = casttv.episodiomenugnral("",titleep,url,"",titleserievisto,"","","0","0","",tipovisto,CHANNELNAME,urlOK)

    if seleccion>0:
        if tipovisto<>"New":
            if "Fav" in categoryback and detener<>"-1":
                casttv.writetmplist(casttv.NEWANF_FILE,[],"3","")
            detail(titleback,urlback,categoryback,titleinfo,tcsearch,titleerdm,thumbnailback,plotback,True)
        elif detener<>"-1":
            #category2 = re.sub(r".*?\s\-\s([^\-]+)$",lambda micat: micat.group(1),categoryback)
            #respuesta = casttv.alertreturnfav(category2,"2")
            #if respuesta:
            #    casttv.writetmplist(casttv.NEWANF_FILE,[],"2","")
            #    if "Todos" in categoryback:
            #        casttv.writetmplist(casttv.NEWCTV_FILE,[],"2","")
            #else:
            nuevos,update = casttv.readtmplist(casttv.NEWANF_FILE,"2")
            listaeliminar=[]
            serievisto = ";"+titleserievisto+";"
            for nuevo in nuevos:
                if serievisto in nuevo[0]:
                    if nuevo[2]==title and nuevo[3]==url:
                        listaeliminar.append(nuevo)
                        break
                    elif accion<>"4":
                        listaeliminar.append(nuevo)
            for nuevo in listaeliminar:
                nuevos.remove(nuevo)
            casttv.writetmplist(casttv.NEWANF_FILE,nuevos,"2","")
            nuevosnoupdate(categoryback,"2")
    elif seleccion==-1 or seleccion==0:
        title = re.sub('\s+\-\s+',' - ',title)
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
        plot = urllib.unquote_plus( params.get("plot") )
        server = params.get("server")
        title = re.sub('\s\-\s\['+server+'\]','',title)
        title = title+' - ['+server+']'+autor

        addnewvideo( CHANNELNAME , "play" , categoryback , server , title , url , thumbnail , plot )

        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=categoryback )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

        #Check: no se muestran los strings con el texto de las opciones...
        #xbmctools.play_video(CHANNELNAME,server,url,categoryback,title,thumbnail,plot)

        # Otra manera de continuar sin abrir nuevo directorio pero lento en listados grandes...
        # detail(titleback,urlbac...
        # play(params,url,categoryback)

def play(params,url,category):
    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]

    xbmctools.play_video(CHANNELNAME,server,url,category,title,thumbnail,plot)

def ftitleerdmsearch(title):
    title = re.sub('^El Patito Alfred$','Alfred J Quack',title)
    title = re.sub('^Sherlock Holmes$','Detective Holmes',title)
    title = re.sub('Shippuden','Shippuuden',title)
    title = ftitlesearch(title)
    return title

def finicialformca(title):
    title = re.sub('^El Patito Alfred$','Alfred J Quack',title)
    title = re.sub('^Sherlock Holmes$','Detective Holmes',title)
    return title

def ftitlesearch(title):
    title = title.lower()
    title = re.sub('^(?:the|el|las?|los?)[^\w]+','',title)
    title = re.sub('[^\w]+(?:the|el|las?|los?)[^\w]+',' ',title)
    title = re.sub('[^\w]+(?:pel(?:�|i)cula|movie|vs|versus)[^\w]+',' ',title)
    title = re.sub('[^\w]+(?:pel(?:�|i)cula|movie)$','',title)
    title = re.sub('[^\w]+','',title)
    return title

def ftitleastrosearch(title):
    title = re.sub('^Sherlock Holmes \(by Chihiro\)$','Detective Holmes',title)
    title = re.sub('^Ponyo en el acantilado \(by Chihiro\)$','Ponyo on the Cliff by the Sea',title)
    title = re.sub('^Conan, el ni�o del futuro \(by Chihiro\)$','Conan, the Boy in Future',title)
    return title

def formatostring(cadena):
    cadena = cadena.replace('\n' , '')
    cadena = re.sub('(?:&amp;|&#38;)','&',cadena)
    cadena = cadena.replace('&#33;' , '!')
    cadena = cadena.replace('&Aacute;' , '�')
    cadena = cadena.replace('&Eacute;' , '�')
    cadena = cadena.replace('&Iacute;' , '�')
    cadena = cadena.replace('&Oacute;' , '�')
    cadena = cadena.replace('&Uacute;' , '�')
    cadena = re.sub('(?:&ntilde;|&#241;)','�',cadena)
    cadena = cadena.replace('&Ntilde;' , '�')
    cadena = cadena.replace('&aacute;' , '�')
    cadena = cadena.replace('&#225;' , '�')
    cadena = cadena.replace('&eacute;' , '�')
    cadena = cadena.replace('&#233;' , '�')
    cadena = cadena.replace('&iacute;' , '�')
    cadena = cadena.replace('&#237;' , '�')
    cadena = cadena.replace('&oacute;' , '�')
    cadena = cadena.replace('&#243;' , '�')
    cadena = cadena.replace('&#333;' , 'o')
    cadena = cadena.replace('&uacute;' , '�')
    cadena = cadena.replace('&#250;' , '�')
    cadena = re.sub('(?:&iexcl;|&#161;)','�',cadena)
    cadena = re.sub('(?:&iquest;|&#191;)','�',cadena)
    cadena = re.sub('&#63;','\?',cadena)
    cadena = cadena.replace('&ordf;' , '�')
    cadena = cadena.replace('&quot;' , '"')
    cadena = cadena.replace('&nbsp;' , ' ')
    # cadena = cadena.replace('&hellip;' , '...')
    cadena = re.sub('(?:&#39;|&#039;)','\'',cadena)
    cadena = re.sub('&sup2;','^2',cadena)
    cadena = re.sub('&middot;','-',cadena)
    cadena = re.sub('&frac12;','1/2',cadena)
    cadena = re.sub('^X$','X- Clamp',cadena)
    cadena = re.sub('&#\d{3};','-',cadena)
    cadena = re.sub('&#\d{4};','',cadena)
    return cadena

def alertnoresultados(url):
    advertencia = xbmcgui.Dialog()
    linea2="No se han encontrado v�deos."
    if url<>"":
        linea2=url
    resultado = advertencia.ok('pelisalacarta' , 'Servidor o Contenido no disponible.' , linea2 )

def alertnoresultadosearch():
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('pelisalacarta' , 'La B�squeda no ha obtenido Resultados.' , '')

def alertnofav():
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('Anime Foros' , 'No se han a�adido contenidos a "Mis Favoritos".' , '')

def alertnoweb(web):
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('pelisalacarta' , 'No se mostrar�n contenidos de '+web+'.' , 'El sitio no est� disponible en estos momentos.')

def alertcontinuar(inicial,selecciontc):
    advertencia = xbmcgui.Dialog()
    linea2 = ""
    linea3 = "�Desea continuar?"
    if inicial=="" and selecciontc=="":
        linea2 = "Para buscar m�s r�pido seleccione una Inicial y/o"
        linea3 = "un Tipo de Contenido. �Desea continuar?"
    elif inicial=="" and selecciontc<>"":
        linea2 = "Para buscar m�s r�pido seleccione una Inicial."
    elif inicial<>"" and selecciontc=="":
        linea2 = "Para buscar m�s r�pido seleccione un Tipo de Contenido."
    resultado = advertencia.yesno('pelisalacarta' , 'La B�squeda puede llevar muchos minutos.' , linea2 , linea3 )
    return resultado

def addsimplefolder( canal , accion , category , title , url , thumbnail , plot ):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def adderdmfolder( canal , accion , category , title , url , thumbnail , plot , titleinfo , tcsearch , titleerdm):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&titleinfo=%s&tcsearch=%s&titleerdm=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( titleinfo ) , urllib.quote_plus( tcsearch ) , urllib.quote_plus( titleerdm ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addmcafolder( canal , accion , category , title , url , thumbnail , plot , titleinfo , tcsearch , titlemcanime):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&titleinfo=%s&tcsearch=%s&titlemcanime=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( titleinfo ) , urllib.quote_plus( tcsearch ) , urllib.quote_plus( titlemcanime ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addmcarelfolder( canal , accion , category , title , url , thumbnail , plot , info1 , info2 , info3 , info4 , info5):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot} )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&info1=%s&info2=%s&info3=%s&info4=%s&info5=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) ,  urllib.quote_plus( info1 ) , urllib.quote_plus( info2 ) , urllib.quote_plus( info3 ) , urllib.quote_plus( info4 ) , urllib.quote_plus( info5 ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url = itemurl , listitem=listitem, isFolder=True)

def addnewvideo( canal , accion , category , server , title , url , thumbnail, plot ):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def addvideofolder( canal , accion , category , server , title , url , thumbnail, plot ):
    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
    itemurl = '%s?channel=%s&action=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s&server=%s' % ( sys.argv[ 0 ] , canal , accion , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , server )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=True)

def additem( canal , category , title , url , thumbnail, plot ):
    listitem = xbmcgui.ListItem( title, iconImage=casttv.HD_THUMB, thumbnailImage=thumbnail )
    listitem.setInfo( "video", { "Title" : title, "Plot" : plot } )
    itemurl = '%s?channel=%s&category=%s&title=%s&url=%s&thumbnail=%s&plot=%s' % ( sys.argv[ 0 ] , canal , urllib.quote_plus( category ) , urllib.quote_plus( title ) , urllib.quote_plus( url ) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) )
    xbmcplugin.addDirectoryItem( handle = pluginhandle, url=itemurl, listitem=listitem, isFolder=False)

def ayuda(params,url,category):
    info1 = "Anime - Mis Favoritos: El primer v�deo de los Favoritos sin ning�n tipo de marca de Vistos se trata como Nuevo Contenido (al igual que los Posteriores a [LW])"
    additem( CHANNELNAME , category , "------------------------------------------- Leyenda -------------------------------------------" , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , "[LW]: �ltimo Episodio Visto [Last Watched]" , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , "[W]: Episodio Visto [Watched]" , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , "[UW]: Episodio No Visto [UnWatched]" , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , "[NW]: No para Ver [Not to Watch] (excluido de Nvos Episodios) " , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , "Mis Favoritos [Listados sin car�tula]" , "" , casttv.STARORANGE_THUMB , "" )
    additem( CHANNELNAME , category , "Mis Favoritos Desactivados [Listados sin car�tula]", "" , casttv.STARGREY_THUMB , "" )
    additem( CHANNELNAME , category , "Mis Favoritos con Nuevos Episodios [Aptdo Mis Favoritos]" , "" , casttv.STARGREEN_THUMB , "" )
    additem( CHANNELNAME , category , "Nuevos Episodios (posteriores a [LW]) [Aptdo Mis Favoritos]" , "" , casttv.STARGREEN2_THUMB , "" )
    additem( CHANNELNAME , category , "Mensaje o Encabezado (sin acci�n)" , "" , casttv.HD_THUMB , "" )
    additem( CHANNELNAME , category , "------------------------------------ Info: 29/11/2010 ------------------------------------" , "" , casttv.HELP_THUMB , "" )
    additem( CHANNELNAME , category , info1 , "" , casttv.HD_THUMB , "" )
    additem( CHANNELNAME , category , "Anime - Vistos: Distintos de Mis Favoritos" , "" , casttv.HD_THUMB , "" )
    # ------------------------------------------------------------------------------------
    EndDirectory(category,"",False,True)
    # ------------------------------------------------------------------------------------

def astroteamrglist():
    astrolist = []
    astrolist.append([ "Kochikame (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=15845" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=15845 por friki100. Colaboradores: curro1" , "" , "Serie", "astro2" ])
    astrolist.append([ "Kochikame (by friki100) [Mirror] [TusDivx]" , "http://www.tusdivx.org/anime-peliculas-series-y-ost-en-dd/23352-kochikame-%5B194-203-367%5D%5Bdd%5D%5Bmegaupload%5D.html" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.tusdivx.org/ por friki100" , "" , "Serie", "tusdivx" ])
    astrolist.append([ "Slam Dunk (by friki100)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16731" , "http://upload.wikimedia.org/wikipedia/en/b/b3/Slamdunk_cover1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16731 por friki100." , "" , "Serie", "astro2" ])
    astrolist.append([ "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Detective Holmes" , "Serie" , "astro" ])
    astrolist.append([ "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" , "astro" ])
    astrolist.append([ "Ponyo en el acantilado (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://www.caratulasdecine.com/Caratulas5/ponyoenelacantilado.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Ponyo on the Cliff by the Sea" , "Pel�cula" , "astro" ])
    astrolist.append([ "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" , "astro" ])
    astrolist.append([ "Conan, el ni�o del futuro (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img220.imageshack.us/img220/425/50332do7.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Conan, the Boy in Future" , "Serie" , "astro" ])
    astrolist.append([ "Cowboy Bebop (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://upload.wikimedia.org/wikipedia/en/3/37/CowboyBebopDVDBoxSet.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" , "astro" ])
    astrolist.append([ "Sailor Moon (by Tuxedo_Mask)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16406" , "http://upload.wikimedia.org/wikipedia/en/4/40/Sailor_Moon_S.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16406 por Tuxedo_Mask." , "" , "Serie", "astro2" ])
    astrolist.append([ "Master Keaton VOSE (by Tom_Bombadil)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16761" , "http://upload.wikimedia.org/wikipedia/en/f/f7/Master_Keaton_cover.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16761 por Tom_Bombadil" , "" , "Serie", "astro2" ])
    astrolist.append([ "Eureka Seven VOSE (by skait)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16784" , "http://upload.wikimedia.org/wikipedia/en/4/45/Eureka_Seven_DVD_1_-_North_America.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16784 por skait." , "" , "Serie", "astro2" ])
    astrolist.append([ "Cross Game VOSE (by gatest)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16808" , "http://upload.wikimedia.org/wikipedia/en/c/cf/Cross_Game_DVDv1.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16808 por gatest" , "" , "Serie", "astro2" ])
    return astrolist

def clasicoslist():
    clasiclist = []
    clasiclist.append([ "La Aldea del Arce (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://spe.fotolog.com/photo/46/13/24/soy_un_sol/1226490296711_f.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" , "astro" ])
    clasiclist.append([ "El Patito Alfred" , "http://www.elrincondelmanga.com/foro/showthread.php?t=63927#1" , "http://www.fotodiario.com/fotos/7596/75967b6200db43e76e7d2d87c3e90191_709x963.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Heidi" , "http://www.elrincondelmanga.com/foro/showthread.php?t=1173" , "http://images.mcanime.net/images/anime/433.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Marco, de los Apeninos a los Andes" , "http://www.elrincondelmanga.com/foro/showthread.php?t=65463#1" , "http://img115.imageshack.us/img115/8325/1612df65c4rs6.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Sherlock Holmes (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "Detective Holmes" , "Serie" , "astro" ])
    #clasiclist.append([ "Sherlock Holmes" , "http://www.elrincondelmanga.com/foro/showthread.php?t=2401" , "http://img515.imageshack.us/img515/1050/sherlock20dq.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Ulises 31" , "http://www.elrincondelmanga.com/foro/showthread.php?t=3294" , "http://img208.imageshack.us/img208/4820/ulyssesbox9sh.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Captain Tsubasa" , "http://www.elrincondelmanga.com/foro/showthread.php?t=85186#1" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.elrincondelmanga.com" , "" , "Serie" , "eRdM" ])
    clasiclist.append([ "Campeones (Oliver y Benji) (by Chihiro)" , "http://www.astroteamrg.org/foro/index.php?showtopic=16333" , "http://img135.imageshack.us/img135/3906/dvdcaptaintsubasaboxset3tp.jpg" , "Fuente: http://www.astroteamrg.org/foro/index.php?showtopic=16333 por Chihiro." , "" , "Serie" , "astro" ])
    return clasiclist

def tusdivxlist():
    tusdivx = []
    tusdivx.append([ "Kochikame (by friki100)" , "http://www.tusdivx.org/anime-peliculas-series-y-ost-en-dd/23352-kochikame-%5B194-203-367%5D%5Bdd%5D%5Bmegaupload%5D.html" , "http://img516.imageshack.us/img516/7731/kochikamepj9.jpg" , "Fuente: http://www.tusdivx.org/ por friki100" , "" , "Serie", "tusdivx" ])
    return tusdivx

def EndDirectory(category,sortmethod,listupdate,cachedisc):
    if sortmethod=="":
        sortmethod=xbmcplugin.SORT_METHOD_NONE
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=sortmethod)
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True , updateListing=listupdate , cacheToDisc=cachedisc  )