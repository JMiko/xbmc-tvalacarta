# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "cuevana"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cuevana.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Películas"  , action="peliculas", url="http://www.cuevana.tv/web/peliculas?&todas"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series"     , action="seriesMenu",    url="http://www.cuevana.tv/web/series?&todas"))
    #itemlist.append( Item(channel=CHANNELNAME, title="Buscar"     , action="search_options") )
    
    return itemlist
    
def seriesMenu(item):
    logger.info("[cuevana.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=CHANNELNAME, title="Lista Completa"  , action="series", url="http://www.cuevana.tv/web/series?&todas"))
    #itemlist.append( Item(channel=CHANNELNAME, title="Populares"  , action="series", url="http://www.cuevana.tv/web/series?&populares"))
    #itemlist.append( Item(channel=CHANNELNAME, title="Ranking"  , action="series", url="http://www.cuevana.tv/web/series?&ranking"))

    return itemlist
    

def peliculas(item):
    logger.info("[cuevana.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=CHANNELNAME, title="Lista Completa"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&todas"))
    itemlist.append( Item(channel=CHANNELNAME, title="Recientes"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&recientes"))
    itemlist.append( Item(channel=CHANNELNAME, title="Estrenos"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&estrenos"))
    itemlist.append( Item(channel=CHANNELNAME, title="Populares"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&populares"))
    itemlist.append( Item(channel=CHANNELNAME, title="Ranking"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&ranking"))
    itemlist.append( Item(channel=CHANNELNAME, title="HD"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&hd"))
#    itemlist.append( Item(channel=CHANNELNAME, title="Por Género"     , action="porGenero",    url="http://www.cuevana.tv/peliculas/genero/"))
#    itemlist.append( Item(channel=CHANNELNAME, title="Listado Alfabético"     , action="listadoAlfabetico",    url="http://www.cuevana.tv/peliculas/lista/"))	

    return itemlist

def porGenero(item):
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Acción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=5"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Animación",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=7"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Aventura",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=14"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Bélica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=19"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Ciencia Ficción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=6"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Cine Negro",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=23"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=2"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Dramática",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=27"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=15"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Negra",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=26"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Romántica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=16"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Stand Up",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=24"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Crimen",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=18"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Deporte",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=20"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Documental",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=10"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Dogma",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=22"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Drama",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=1"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Fantasía",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=13"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Humor",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=12"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Infantil",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=8"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Intriga",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=25"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=11"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Romance",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=9"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Suspenso",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=3"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Terror",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=4"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Thriller",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=17"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Western",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=21"))

    return itemlist	

def listadoAlfabetico(item):
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="0-9",url="http://www.cuevana.tv/peliculas/lista/letra=num"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="A",url="http://www.cuevana.tv/peliculas/lista/letra=a"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="B",url="http://www.cuevana.tv/peliculas/lista/letra=b"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="C",url="http://www.cuevana.tv/peliculas/lista/letra=c"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="D",url="http://www.cuevana.tv/peliculas/lista/letra=d"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="E",url="http://www.cuevana.tv/peliculas/lista/letra=e"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="F",url="http://www.cuevana.tv/peliculas/lista/letra=f"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="G",url="http://www.cuevana.tv/peliculas/lista/letra=g"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="H",url="http://www.cuevana.tv/peliculas/lista/letra=h"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="I",url="http://www.cuevana.tv/peliculas/lista/letra=i"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="J",url="http://www.cuevana.tv/peliculas/lista/letra=j"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="K",url="http://www.cuevana.tv/peliculas/lista/letra=k"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="L",url="http://www.cuevana.tv/peliculas/lista/letra=l"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="M",url="http://www.cuevana.tv/peliculas/lista/letra=m"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="N",url="http://www.cuevana.tv/peliculas/lista/letra=n"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="O",url="http://www.cuevana.tv/peliculas/lista/letra=o"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="P",url="http://www.cuevana.tv/peliculas/lista/letra=p"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Q",url="http://www.cuevana.tv/peliculas/lista/letra=q"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="R",url="http://www.cuevana.tv/peliculas/lista/letra=r"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="S",url="http://www.cuevana.tv/peliculas/lista/letra=s"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="T",url="http://www.cuevana.tv/peliculas/lista/letra=t"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="U",url="http://www.cuevana.tv/peliculas/lista/letra=u"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="V",url="http://www.cuevana.tv/peliculas/lista/letra=v"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="W",url="http://www.cuevana.tv/peliculas/lista/letra=w"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="X",url="http://www.cuevana.tv/peliculas/lista/letra=x"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Y",url="http://www.cuevana.tv/peliculas/lista/letra=y"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Z",url="http://www.cuevana.tv/peliculas/lista/letra=z"))

    return itemlist

def novedades(item):
    logger.info("[cuevana.py] login")
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    # Extrae las entradas
    patron  = '<script type="text/javascript">(.*?)</script>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    data = data.replace("\\","")
    patron  = '\{\"(.*?)}'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for datos in matches:
        try:
            scrapedtitle  = re.compile('"tit":"([^"]+)"',re.DOTALL).findall(datos)[0]
        except:
            scrapedtitle  = ""
        try:
            scrapedplot   = re.compile('"txt":"([^"]+)"',re.DOTALL).findall(datos)[0]
        except:
            scrapedplot   = ""
        try:
            scrapedurl    = re.compile('url":"([^"]+)"',re.DOTALL).findall(datos)[0]
            scrapedurl = re.compile('peliculas/([^/]+)',re.DOTALL).findall(scrapedurl)[0]
            scrapedthumbnail = "http://sc.cuevana.tv/box/"+scrapedurl+".jpg"
        except:
            scrapedurl    = ""
            scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, extra="pelicula") )
    return itemlist

def series(item):
    logger.info("[cuevana.py] series")
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    patron  = '<script type="text/javascript">(.*?)</script>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = matches[0]
    
    #{"id":"3478","url":"#!\/series\/3478\/american-dad","tit":"American Dad!","duracion":"30","ano":"2005","temporadas":"7","episodios":"120","rate":"3.9887976646423340","genero":"Animaci\u00f3n","idioma":"Ingl\u00e9s"}
		# {"url":"#!\/series\/3622\/game-of-thrones","tit":"Game of Thrones","duracion":"60","temporadas":"1","episodios":"10","genero":" Fantas\u00eda"}
    data = data.replace("\\","")
    # patron  = '{"id":"([^"]+)","url":"([^"]+)","tit":"([^"]+)","duracion":"([^"]+)","ano":"([^"]+)","temporadas":"([^"]+)","episodios":"([^"]+)","rate":"([^"]+)","genero":"([^"]+)","idioma":"([^"]+)"}'
    patron  = '{(.*?)"url":"([^"]+)","tit":"([^"]+)","duracion":"([^"]+)",(.*?)"temporadas":"([^"]+)","episodios":"([^"]+)",(.*?)"genero":"([^"]+)"(.*?)}'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    itemlist = []
    for id,url,tit,duracion,ano,temporadas,episodios,rate,genero,idioma in matches:
        scrapedtitle = tit
        scrapedplot = ""
        # url es "#!/series/3478/american-dad"
        # el destino es "http://www.cuevana.tv/web/series?&3478&american-dad"
        
        #   #!/series/3478/american-dad
        scrapedurl = url.replace("/","&")
        #   !&series&3478&american-dad

        scrapedurl = scrapedurl.replace("#!&series","http://www.cuevana.tv/web/series?")
        #   http://www.cuevana.tv/web/series?&3478&american-dad

        # scrapedthumbnail = "http://sc.cuevana.tv/box/"+id+".jpg"
        scrapedthumbnail = scrapedurl.replace("http://www.cuevana.tv/web/series?&","http://sc.cuevana.tv/box/")
        scrapedthumbnail = scrapedthumbnail.replace("&",".jpg?")
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle) )

    return itemlist

def episodios(item):
    logger.info("[cuevana.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae el argumento
    patron  = '<div class="txt">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = matches[0]

    data = data.replace("\\","")
    patron = "serieList\(\{l\:(.*?)\,e\:\$\('\#episodios'\)\}\)\;"
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    logger.info("data="+data)
    
    import simplejson as json
    seasons = json.loads(data)
    
    for season_id in seasons:
        print seasons[season_id]
        
        for episode in seasons[season_id]:
            num = episode["num"]
            if len(num)==1: num="0"+num
            scrapedtitle = "%sx%s %s" % (season_id,num,episode["tit"])
            if episode["hd"]=="1":
                scrapedtitle = scrapedtitle + " (HD)"
            scrapedplot = item.plot
            scrapedurl = episode["id"]
            scrapedthumbnail = item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+item.show)
    
            itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=item.fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.show, extra="serie") )

    itemlist = sorted(itemlist, key=lambda item: item.title)

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[cuevana.py] findvideos")

    id = item.url
    logger.info(item.extra)
    tipo=item.extra

    if tipo=="pelicula":
        pathSubtitle="http://sc.cuevana.tv/files/sub/"
    else:
        pathSubtitle="http://sc.cuevana.tv/files/s/sub/"

    # Obtiene las fuentes compatibles
    '''
    var sources = {"720":{"2":["megaupload","glumbo","wupload"]},"360":{"2":["megaupload","glumbo","wupload"]}}, sel_source = 0;
    var label = {
        '360': 'SD (360p)',
        '480': 'SD (480p)',
        '720': 'HD (720p)',
        '1080': 'HD (1080p)'
    };
    var labeli = {"1":"Espa\u00f1ol","2":"Ingl\u00e9s","3":"Portugu\u00e9s","4":"Alem\u00e1n","5":"Franc\u00e9s","6":"Coreano","7":"Italiano","8":"Tailand\u00e9s","9":"Ruso","10":"Mongol","11":"Polaco","12":"Esloveno","13":"Sueco","14":"Griego","15":"Canton\u00e9s","16":"Japon\u00e9s","17":"Dan\u00e9s","18":"Neerland\u00e9s","19":"Hebreo","20":"Serbio","21":"\u00c1rabe","22":"Hindi","23":"Noruego","24":"Turco","26":"Mandar\u00edn","27":"Nepal\u00e9s","28":"Rumano","29":"Iran\u00ed","30":"Est\u00f3n","31":"Bosnio","32":"Checo","33":"Croata","34":"Fin\u00e9s","35":"H\u00fanagro"};
    var labelh = {
        'megaupload': 'Megaupload',
        'glumbo': 'Glumbo',
        'filepost': 'Filepost',
        'wupload': 'Wupload'
    };
    '''
    url = "http://www.cuevana.tv/player/sources?id="+id+"&tipo="+tipo

    data = scrapertools.cache_page(url)
    
    # Fuentes
    patron = 'var sources \= (.*?)\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    cadena = matches[0].replace(", sel_source = 0","")
    import simplejson as json
    sources = json.loads(cadena)

    # Calidades
    patron = 'var label \= (.*?)\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    cadena = matches[0]
    cadena = re.compile("\s+",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("'",'"')

    import simplejson as json
    qualities = json.loads(cadena)

    # Idiomas
    language_labels = {}
    language_labels["1"]="Espanol"
    language_labels["2"]="Ingles"

    # Presenta las opciones
    itemlist = []
    i=1
    for quality_id in sources:
        languages = sources[quality_id]

        for language_id in languages:
            print language_id
            mirrors = sources[quality_id][language_id]

            for mirror in mirrors:
                titulo = "Opcion %d: %s %s (%s)" % (i, mirror , qualities[quality_id], language_labels[language_id])
                i=i+1
                url = "def=%s&audio=%s&host=%s&id=%s&tipo="+tipo
                url = url % (quality_id,language_id,mirror,id)
                
                subtitulo = pathSubtitle+id+"_ES.srt"
                
                itemlist.append( Item(channel=CHANNELNAME, action="play" , title=titulo, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, extra=id, subtitle=subtitulo, folder=False))

    return itemlist

def play(item):
    logger.info("[cuevana.py] play")
    url = "http://www.cuevana.tv/player/source_get"
    post = item.url
    id = item.extra
    headers = []
    headers.append( ["Host","www.cuevana.tv"])
    headers.append( ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0) Gecko/20100101 Firefox/8.0"])
    headers.append( ["Accept","*/*"])
    headers.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"])
    headers.append( ["Accept-Encoding","gzip, deflate"])
    headers.append( ["Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"])
    headers.append( ["Connection","keep-alive"])
    headers.append( ["Content-Type","application/x-www-form-urlencoded; charset=UTF-8"])
    headers.append( ["X-Requested-With","XMLHttpRequest"])
    headers.append( ["Referer","http://www.cuevana.tv/player/sources?id="+id+"&tipo=serie"])
    headers.append( ["Content-Length", len(post) ])
    headers.append( ["Pragma","no-cache"])
    headers.append( ["Cache-Control","no-cache"])

    data = scrapertools.cache_page(url=url, post=post)

    itemlist = servertools.find_video_items(data=data)
    for returnitem in itemlist:
        returnitem.channel=item.channel
        returnitem.subtitle=item.subtitle

    return itemlist

def search_options(item):
    logger.info("[cuevana.py] search_options")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Titulo"   , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Titulo"))
    itemlist.append( Item(channel=CHANNELNAME, title="Episodio" , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Episodio"))
    itemlist.append( Item(channel=CHANNELNAME, title="Actor"    , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Actor"))
    itemlist.append( Item(channel=CHANNELNAME, title="Director" , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Director"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto, categoria="*"):
    logger.info("[cuevana.py] search")
    
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.cuevana.tv/buscar/?q=%s&cat=Titulo"
    
        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return listar(item, categoria)
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def listar(item, categoria="*"):
    logger.info("[cuevana.py] listar")

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    patronvideos  = "<div class='result'>[^<]+"
    patronvideos += "<div class='right'><div class='tit'><a href='([^']+)'>([^<]+)</a>"
    patronvideos += ".*?<div class='txt'>([^<]+)<div class='reparto'>.*?"
    patronvideos += "<div class='img'>.*?<img src='([^']+)'[^>]+></a>"


    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = match[2]
        scrapedurl = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[0])
        scrapedthumbnail = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        ## <-- Trata diferenciadamente a las series y usa filtro de categoria para búsquedas generales
        if "tv/series/" in scrapedurl and categoria in ("S","*"):
           code = re.compile("/series/([0-9]+)/").findall(scrapedurl)[0]
           scrapedurl = "http://www.cuevana.tv/list_search_id.php?serie="+code
           itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , extra=code, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )
        elif "tv/peliculas/" in scrapedurl and categoria in ("F","*"):
           itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="listar", title="Página siguiente" , url=scrapedurl) )

    return itemlist
