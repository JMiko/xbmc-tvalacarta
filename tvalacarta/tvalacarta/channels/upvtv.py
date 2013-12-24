# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para UPV TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

logger.info("[upvtv.py] init")

DEBUG = False
CHANNELNAME = "upvtv"
MAIN_URL = "http://www.upv.es/pls/oreg/rtv_web.ListaProg?p_idioma=c"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[upvtv.py] mainlist")
    return programas(item)

def programas(item):
    logger.info("[upvtv.py] programas")
    itemlist=[]

    # Descarga la página
    item.url = MAIN_URL
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas de programas UPV TV)
    '''
    <div id="ventana">
    </div><!-- ventana -->
    <ul>
    <li><a href="javascript:getAjaxFile('1366');">Acto Institucional UPV</a></li>
    <li><a href="javascript:getAjaxFile('1510');">Ágora Valencia</a></li>
    '''
    
    #patron  = '<div id="ventana">[^<]+'
    #patron += '</div><!-- ventana -->[^<]+'
    #patron += '<ul>[^<]+'
    patron = '<li><a href="javascript:getAjaxFile([^"]+)' # [0] ID de la pagina del programa (se carga en un frame en javascript pero
                                  # monto la URL más abajo usando este ID)
    patron += ';">([^"]+)</a></li>' # [1] Título del programa
    #patron += '<img width=160 height=121 src="([^"]+)" alt="Img. del programa" /></a>[^<]+' # [1] Imagen del programa
    #patron += '<p>([^"]+)</p>[^<]+' # [3] Argumento del programa
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        # Atributos del vÃƒÂ­deo
        scrapedtitle = unicode( match[1].strip() , "iso-8859-1" , errors="ignore").encode("utf-8")
        scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFicha?p_id="+match[0][2:-2]+"&p_idioma=c" #urlparse.urljoin(url,)
        scrapedthumbnail = urlparse.urljoin(item.url,"http://mediaserver01.upv.es/UPRTV/TV/MC/img/"+match[0][2:-2]+".jpg") #urlparse.urljoin(url,match[1])
        scrapedplot = "Pulsa sobre el nombre de un programa para ver los detalles y escoger el capítulo que deseas ver en el histórico de sus emisiones." # match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[upvtv.py] episodios")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #xbmc.output(data) # hace un print de la captura del html en el log del XBMC
    #logger.info(data)

    # Extrae los capitulos
    '''
    <dt>20-01-2011</dt>
    <dd>
        <span class="archivo"><a href="javascript:getAjaxFile2('1366','35547');" onClick="scroll(0,0)" >
        Toma de posesión Nemesio Fernández [Dtor ETS Ingeniería Agronómica y Medio Natural]
    </a></span>
        <a target="_blank" href="http://mediaserver01.upv.es/UPRTV/TV/ActoInstitucionalUPV/2011-01-20 Acto_Insti Toma de posesión Nemesio Fernández [Dtor ETS Ingeniería Agronómica y Medio Natural].wmv"title="Descargar Programa" class="verPrograma">Ver programa</a>
    </dd>
    '''
    
    patron  = '<dt>([0-9][^\ ]+)+</dt>[^<]+' # [0] Fecha de emisión
    patron += '<dd>.*?'
    #patron += '<span class="archivo"><a href="[^"]+" onClick="([^"]+)" >' #[0] captura en blanco
    patron += '>([^<]+)'# [1] Título del capítulo
    patron += '</a></span>[^<]+'
    patron += '<a target="_blank" href="([^<]+)" title="Descargar Programa.*?' #[2] URL del vídeo
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        # Atributos del vídeo
        scrapedtitle = "["+match[0].strip()+"] "+match[1][1:-1] #match[2]#.strip()
        scrapedtitle = unicode( scrapedtitle , "iso-8859-1" , errors="ignore").encode("utf-8")

        #scrapedurl = urlparse.urljoin(url,match[2])
                
        URLqueMola = urllib.quote(match[2]) #urllib.quote("http://mediaserver01.upv.es/UPRTV/TV/ActoInstitucionalUPV/2010-04-08 Acto_Insti Toma de posesión decano ADE.wmv")[5:]
        logger.info("url="+URLqueMola)
        URLconHTTPok = URLqueMola.replace("http%3A","http:").replace(" ","%20")
        logger.info("url="+URLconHTTPok)
        scrapedurl = (URLconHTTPok)
        scrapedthumbnail = ""
        scrapedplot = "HAZ CLICK SOBRE EL NOMBRE PARA REPRODUCIR EL CAPÍTULO"
        if not scrapedurl.startswith("http"):
            scrapedurl = "http://"+scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=False) )

    #Mirar posible solución reemplazar caracteres extraños aquí:
    #http://gomputor.wordpress.com/2008/09/27/search-replace-multiple-words-or-characters-with-python/
    #http://www.python.org/dev/peps/pep-0263/


    # Extrae los capitulos de la página siguiente y/o anterior
    '''
    <div class="paginador"><ul>
    <li><a href="javascript:getAjaxFile3(1327,151)" class="anterior">Siguiente</a></li>
    <li class="numero">1/7</li>
    <li><a href="javascript:getAjaxFile3(1327,26)" class="siguiente">Anterior</a></li>
    </ul></div><!-- paginador (1) --><br class="clearFloat"/>
    '''

    
    #patron  = '<div class="paginador"><ul>'
    patron  = '<li><a href="javascript:getAjaxFile3\(([^"]+)\,([^"]+)\)" class="anterior".*?'#[0] y [1] id programa + id nº primer capítulo de la página anterior
    patron += '<li><a href="javascript:getAjaxFile3\(([^"]+)\,([^"]+)\)" class="siguiente".*?' #[2] y [3] id programa + id nº primer capítulo de la página anterior
    #patron  += '<li class="numero">([^"]+)</li>' #[2] y [3] número de página actual y número total de páginas
    #patron += '([^"]+),([^"]+).*?'
    #patron += ')" class="anterior".*?'# 
    #patron += '<li><a href="javascript:getAjaxFile3(([^"]+),([^"]+))" class="siguiente".*?'# [2] y [3] id programa + id nº primer programa de la página siguiente
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        # Atributos del "Paginador"
        scrapedtitle = "<<Página anterior<<"# ["+match[2]+"]" 
        #Meto prueba de la TV en directo pero no se la come
        scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFichaAnteriores?p_id="+match[0]+"&p_reg="+match[1]+"&p_idioma=c&rndval=" #urlparse.urljoin(url,match) #match 
        scrapedthumbnail = ""
        scrapedplot = "Emisiones Anteriores"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )
        
    for match in matches:
        # Atributos del "Paginador"
        scrapedtitle = ">>Página siguiente>>"# ["+match[2]+"]" 
        #Meto prueba de la TV en directo pero no se la come
        scrapedurl = "http://www.upv.es/pls/oreg/rtv_web.ProgFichaAnteriores?p_id="+match[2]+"&p_reg="+match[3]+"&p_idioma=c&rndval=" #urlparse.urljoin(url,match) #match 
        scrapedthumbnail = ""
        scrapedplot = "Emisiones Anteriores"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # Todas las opciones tienen que tener algo
    programas_items = mainlist(Item())
    if len(programas_items)==0:
        return False

    episodios_items = episodios(programas_items[0])
    if len(episodios_items)==0:
        return False

    return bien
