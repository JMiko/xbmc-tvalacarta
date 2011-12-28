# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesdanko.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

PLUGIN_NAME = "pelisalacarta"

__channel__ = "seriesdanko"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriesdanko"
__language__ = "ES"

DEBUG = config.get_setting("debug")

if config.get_system_platform() == "xbox":
    MaxResult = "55"
else:
    MaxResult = "500"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesdanko.py] mainlist")
    item.url = 'http://www.seriesdanko-rs.com/'

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Noticias", action="novedades"   , url=item.url))
    itemlist.append( Item(channel=__channel__, title="Lista alfanumerica", action="letras", url=item.url))
    itemlist.append( Item(channel=__channel__, title="Listado completo", action="allserieslist", url=item.url))
    itemlist.append( Item(channel=__channel__, title="Buscar", action="search" , url=item.url, thumbnail="http://www.mimediacenter.info/xbmc/pelisalacarta/posters/buscador.png"))

    return itemlist

def search(item,texto):
    logger.info("[seriesdanko.py] search")
    item.url = "http://www.seriesdanko-rs.com/gestion/pag_search.php"
    
    data = scrapertools.cache_page(item.url,post='q='+texto)
    
    return series(item,data)

def novedades(item):
    logger.info("[seriesdanko.py] novedades")

    itemlist = []
    extra = ""
    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url).replace("\n","")
    #print data
    patronvideos = "(<h3 class='post-title entry-title'>.*?<div class='post-body entry-content')"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    totalItems = len(matches)
    for match in matches:
        try:
            scrapedurl = urlparse.urljoin(item.url,re.compile(r"href=(serie.+?)>").findall(match)[0])
        except:continue
        try:
            scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[0]
        except:
            scrapedthumbnail = ""
        try:
            scrapedtitle = re.compile(r"class='post-title entry-title'>(.+?)<").findall(match)[0]
            scrapedtitle = decodeHtmlentities(scrapedtitle)
        except:
            scrapedtitle = "sin titulo"
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = extra , folder=True , totalItems = totalItems ) )
    
    return itemlist

def allserieslist(item):
    logger.info("[seriesdanko.py] allserieslist")

    Basechars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BaseUrl = "http://www.seriesdanko-rs.com/series.php?id=%s"
    action = "series"

    itemlist = []

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info(data)

    # Extrae el bloque de las series
    patronvideos = "Listado de series disponibles</h2>(.*?)<div class='clear'></div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    patronvideos  = "<a href='([^']+)'.+?>([^<]+)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    totalItems = len(matches)
    for url,title in matches:
        scrapedtitle = title.replace("\n","").replace("\r","")
        scrapedurl = url
        scrapedurl = urlparse.urljoin(item.url,scrapedurl.replace("\n","").replace("\r",""))
        scrapedthumbnail = ""
        scrapedplot = ""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        if title in Basechars or title == "0-9":
            
            scrapedurl = BaseUrl % title
        else:
            action = "episodios"

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action=action , title=scrapedtitle , show=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle = scrapedtitle , totalItems = totalItems))

    return itemlist

def letras(item):
    logger.info("[seriesdanko.py] letras")

    itemlist=[]
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action="series", title=str(letra), url = "http://www.seriesdanko-rs.com/series.php?id=%s" % letra))

    itemlist.append( Item(channel=item.channel, action="series", title="0-9", url = "http://www.seriesdanko-rs.com/series.php?id=0"))

    return itemlist

def series(item,data=""):
    logger.info("[seriesdanko.py] series")
    itemlist = []
    
    # Descarga la página
    if data=="":
        data = scrapertools.cache_page(item.url)
        #logger.info("data="+data)

    # Averigua el encoding
    try:
        patronvideos = "charset=(.+?)'"
        charset = re.compile(patronvideos,re.DOTALL).findall(matches[0])
    except:
        logger.info("charset desconocido")
        charset = "utf-8"

    if not "seriesdanko-rs.com" in item.url:
        patronvideos = "<div class='post hentry'>(.*?)<div style='clear: both;'></div>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    else:
        #<div style='float:left;width: 620px;'><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=745' title='Capitulos de: A c&aacutemara s&uacuteper lenta'>
        #<img class='ict' src='http://2.bp.blogspot.com/-9imlR7oVyK0/TomeSfjpmqI/AAAAAAAADz4/aDFpk_U_sMk/s400/a-camara-super-lenta-seriesdanko.jpg' alt='Capitulos de: A c&aacutemara s&uacuteper lenta' height='184' width='120'>
        #</a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=745' style='font-size: 11px;'>Capitulos de: A c&aacutemara s&uacuteper lenta</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=15' title='Capitulos de: A corazon abierto'><img class='ict' src='http://3.bp.blogspot.com/-Xqkd-zcer_s/Tb5gSm1Q0qI/AAAAAAAAFEA/Aq9yHwggL4E/s1600/a-corazon-abierto-seriesdanko.jpg' alt='Capitulos de: A corazon abierto' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=15' style='font-size: 11px;'>Capitulos de: A corazon abierto</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=779' title='Capitulos de: A dos metros bajo Tierra'><img class='ict' src='http://1.bp.blogspot.com/-3v_MMw9eieA/Tp_tXLtbzYI/AAAAAAAAAUk/iOO2E-b9oYY/s400/6ft_u.jpg' alt='Capitulos de: A dos metros bajo Tierra' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=779' style='font-size: 11px;'>Capitulos de: A dos metros bajo Tierra</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=773' title='Capitulos de: A Gifted Man'><img class='ict' src='http://3.bp.blogspot.com/-S89qbBiHOzE/TpXgKb1eebI/AAAAAAAABXQ/iUjcRn7s3GA/s200/nueva-serie-a-gifted-man-octubre-universal-channel-la.jpg' alt='Capitulos de: A Gifted Man' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=773' style='font-size: 11px;'>Capitulos de: A Gifted Man</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=746' title='Capitulos de: A trav&eacutes del tiempo (Quantum Leap)'><img class='ict' src='http://4.bp.blogspot.com/-7FGcUexZnSg/Tooj_Z9uZMI/AAAAAAAAD0Y/4J48gQNPyXg/s400/quantumleap-1-seriesdanko.jpg' alt='Capitulos de: A trav&eacutes del tiempo (Quantum Leap)' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=746' style='font-size: 11px;'>Capitulos de: A trav&eacutes del tiempo (Quantum Leap)</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=748' title='Capitulos de: Aaron Stone'><img class='ict' src='http://3.bp.blogspot.com/-0m9BHsd1Etc/To2PMvCRNeI/AAAAAAAAD1Y/ax3KPRNnJjY/s400/aaron-stone.jpg' alt='Capitulos de: Aaron Stone' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=748' style='font-size: 11px;'>Capitulos de: Aaron Stone</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=749' title='Capitulos de: Abducidos (Taken)'><img class='ict' src='http://1.bp.blogspot.com/-ypnitMQYCp0/TpLK7lXOtII/AAAAAAAAD3g/f5Sfn_QJ69E/s400/abducidos.jpg' alt='Capitulos de: Abducidos (Taken)' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=749' style='font-size: 11px;'>Capitulos de: Abducidos (Taken)</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=750' title='Capitulos de: Abuela de verano'><img class='ict' src='http://3.bp.blogspot.com/-qOuWLF5Pwh0/TpLdjRwdT5I/AAAAAAAAD3o/sVAkrmmIUxI/s400/abuela-de-verano.jpg' alt='Capitulos de: Abuela de verano' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=750' style='font-size: 11px;'>Capitulos de: Abuela de verano</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=16' title='Capitulos de: Abusos sexuales y el vaticano'><img class='ict' src='http://4.bp.blogspot.com/_HixxA9qiz98/TULBmi_l0yI/AAAAAAAADsM/24CKg_1aZX8/s1600/ABUSOS%2BSEXUALES%2BY%2BEL%2BVATICANO.jpg' alt='Capitulos de: Abusos sexuales y el vaticano' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=16' style='font-size: 11px;'>Capitulos de: Abusos sexuales y el vaticano</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=17' title='Capitulos de: Accused'><img class='ict' src='http://1.bp.blogspot.com/-QY39J7WYjqE/TnHFNJ8dSlI/AAAAAAAAG7U/eqQvDlMiwWw/s1600/accused-seriesdanko.jpg' alt='Capitulos de: Accused' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=17' style='font-size: 11px;'>Capitulos de: Accused</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=751' title='Capitulos de: Acorralada'><img class='ict' src='http://1.bp.blogspot.com/-WDSKVPZc3Wk/TpL7BzpVpUI/AAAAAAAAD3w/Y6YFsUFsJWE/s400/Acorraladajpg.jpg' alt='Capitulos de: Acorralada' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=751' style='font-size: 11px;'>Capitulos de: Acorralada</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=18' title='Capitulos de: Acusados'><img class='ict' src='http://www.megainfinity.net/img/acusados.jpg' alt='Capitulos de: Acusados' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=18' style='font-size: 11px;'>Capitulos de: Acusados</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=19' title='Capitulos de: Adolfo Suarez, el presidente'><img class='ict' src='http://4.bp.blogspot.com/-HAzP69quTMc/TnHGcK542sI/AAAAAAAAG7k/G4NQCyp2_7Q/s1600/adolfo-seriesdanko.jpg' alt='Capitulos de: Adolfo Suarez, el presidente' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=19' style='font-size: 11px;'>Capitulos de: Adolfo Suarez, el presidente</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=20' title='Capitulos de: Against The Wall'><img class='ict' src='http://3.bp.blogspot.com/-7FfTVy9xYrQ/TkTj1zqVPeI/AAAAAAAABIQ/-Hhin3jkFd4/s200/1Against_the_Wall_Serie_de_TV-945118868-large.jpg' alt='Capitulos de: Against The Wall' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=20' style='font-size: 11px;'>Capitulos de: Against The Wall</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=845' title='Capitulos de: Agencia Lovespring'><img class='ict' src='http://4.bp.blogspot.com/-cKscZvK417M/Ts-pKNtGRFI/AAAAAAAACQ8/w5S68lVsXyg/s500/Agencia_Lovespring_Serie_de_TV-344892203-large.jpg' alt='Capitulos de: Agencia Lovespring' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=845' style='font-size: 11px;'>Capitulos de: Agencia Lovespring</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=21' title='Capitulos de: Aguila roja'><img class='ict' src='http://2.bp.blogspot.com/-H-XXyCI4chY/Tnfk5J3k1-I/AAAAAAAADfU/FzSy0Yq83_g/s400/cartel-de-aguila-roja.jpg' alt='Capitulos de: Aguila roja' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=21' style='font-size: 11px;'>Capitulos de: Aguila roja</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=22' title='Capitulos de: Aida'><img class='ict' src='http://3.bp.blogspot.com/-9biaTTm0_GY/TnHA7_RYKsI/AAAAAAAAG6E/sHF2P56uG9Q/s1600/aida-seriesdanko-1.jpg' alt='Capitulos de: Aida' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=22' style='font-size: 11px;'>Capitulos de: Aida</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=23' title='Capitulos de: Al descubierto'><img class='ict' src='http://2.bp.blogspot.com/_HixxA9qiz98/TKWJcJqq7rI/AAAAAAAABRQ/M0W4wVkIZEQ/s1600/al-descubierto-seriesdanko.jpg' alt='Capitulos de: Al descubierto' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=23' style='font-size: 11px;'>Capitulos de: Al descubierto</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=7' title='Capitulos de: Al Qaeda'><img class='ict' src='http://3.bp.blogspot.com/_7GZ2zNkxpHM/TUsoBzo-KVI/AAAAAAAAABQ/RhOfAGvZ0n0/s1600/alqaeda_P.jpg' alt='Capitulos de: Al Qaeda' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=7' style='font-size: 11px;'>Capitulos de: Al Qaeda</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=24' title='Capitulos de: Alakrana'><img class='ict' src='http://4.bp.blogspot.com/-XyE39BYGZLA/Td4NHUq-AAI/AAAAAAAAFjg/AmRvqpMUa1U/s200/alakrana-seriesdanko.jpg' alt='Capitulos de: Alakrana' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=24' style='font-size: 11px;'>Capitulos de: Alakrana</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=816' title='Capitulos de: Alf'><img class='ict' src='http://3.bp.blogspot.com/-3FVVJthGZBI/TrhQ9uY-4fI/AAAAAAAAH3s/rp-qskusvV4/s400/Alf-seriesdanko.jpg' alt='Capitulos de: Alf' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=816' style='font-size: 11px;'>Capitulos de: Alf</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=25' title='Capitulos de: Alfonso,el principe maldito'><img class='ict' src='http://2.bp.blogspot.com/_HixxA9qiz98/TJO4z-wpmGI/AAAAAAAAA2w/Yjbs6bx7q0w/s1600/Alfonso-el-principe-maldito-seriesdanko.jpg' alt='Capitulos de: Alfonso,el principe maldito' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=25' style='font-size: 11px;'>Capitulos de: Alfonso,el principe maldito</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=26' title='Capitulos de: Alguien te mira'><img class='ict' src='http://1.bp.blogspot.com/_HixxA9qiz98/TKl6gGLdhPI/AAAAAAAABUA/Z7QvKueI3OA/s200/Alguien-Te-Mira-seriesdanko.jpg' alt='Capitulos de: Alguien te mira' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=26' style='font-size: 11px;'>Capitulos de: Alguien te mira</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=27' title='Capitulos de: Alice (2009)'><img class='ict' src='http://2.bp.blogspot.com/--e6gIBm22DA/TnHF25XTLxI/AAAAAAAAG7c/DHGcvmr6XxQ/s200/alice-seriesdanko.jpg' alt='Capitulos de: Alice (2009)' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=27' style='font-size: 11px;'>Capitulos de: Alice (2009)</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=842' title='Capitulos de: Alien Nation'><img class='ict' src='http://4.bp.blogspot.com/-uZlLCBEFWH4/Ts9rkDOWfdI/AAAAAAAACQk/hq2icxXmwPc/s500/alien_nation.jpg' alt='Capitulos de: Alien Nation' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=842' style='font-size: 11px;'>Capitulos de: Alien Nation</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=807' title='Capitulos de: Allen Gregory'><img class='ict' src='http://3.bp.blogspot.com/-29_Gd7oaI38/TrHr22FUMyI/AAAAAAAAEZI/9YInOqgLx-Y/s400/allen-gregory-0.jpg' alt='Capitulos de: Allen Gregory' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=807' style='font-size: 11px;'>Capitulos de: Allen Gregory</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=28' title='Capitulos de: Almost Heroes'><img class='ict' src='http://2.bp.blogspot.com/-l1IBB9UdPKI/TfcrPFnsRAI/AAAAAAAAA-o/P1loCdcGzqE/s1600/almost.jpg' alt='Capitulos de: Almost Heroes' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=28' style='font-size: 11px;'>Capitulos de: Almost Heroes</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=29' title='Capitulos de: Alphas'><img class='ict' src='http://3.bp.blogspot.com/-XMtT7BPcQ-8/Thymrkqm7XI/AAAAAAAAGJw/XIdoNZattus/s1600/alphas-serie-syfy-seriesdanko.jpeg' alt='Capitulos de: Alphas' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=29' style='font-size: 11px;'>Capitulos de: Alphas</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=772' title='Capitulos de: America Horror Story'><img class='ict' src='http://4.bp.blogspot.com/-7IoW5zNvZzg/TpXgzZ3vfMI/AAAAAAAABXc/G3XQeeLVVTQ/s200/american_horror_story_1.jpg' alt='Capitulos de: America Horror Story' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=772' style='font-size: 11px;'>Capitulos de: America Horror Story</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=30' title='Capitulos de: American dad'><img class='ict' src='http://1.bp.blogspot.com/_HixxA9qiz98/TKmmrYroDPI/AAAAAAAABU4/IcrsI8ZsBTI/s1600/american-dad-seriesdanko.jpg' alt='Capitulos de: American dad' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=30' style='font-size: 11px;'>Capitulos de: American dad</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=800' title='Capitulos de: Ana de las Tejas Verdes'><img class='ict' src='http://4.bp.blogspot.com/-OGE8uwE3C_E/Tq08HQkvTEI/AAAAAAAAB10/bL98xL7DRHM/s900/anne2.jpg' alt='Capitulos de: Ana de las Tejas Verdes' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=800' style='font-size: 11px;'>Capitulos de: Ana de las Tejas Verdes</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=31' title='Capitulos de: Anatomia de Grey'><img class='ict' src='http://3.bp.blogspot.com/-NSyQ8xuB2Bc/TnJiRCKOtYI/AAAAAAAAALI/vy-6v-r2fZk/s320/anatomia-de-grey-6-temporada.jpg' alt='Capitulos de: Anatomia de Grey' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=31' style='font-size: 11px;'>Capitulos de: Anatomia de Grey</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=32' title='Capitulos de: Andromeda Ascendant'><img class='ict' src='http://1.bp.blogspot.com/_KLLhWj6ZRrE/TPapvJpUeDI/AAAAAAAABsw/t8UzQRcfIvw/s200/andromeda-series-danko.jpg' alt='Capitulos de: Andromeda Ascendant' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=32' style='font-size: 11px;'>Capitulos de: Andromeda Ascendant</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=740' title='Capitulos de: Angel'><img class='ict' src='http://3.bp.blogspot.com/-imZzfi4lqyI/ToO1zcUE6zI/AAAAAAAABUE/-yoHD9Ikbk0/s200/ANGEL%2B2.jpg' alt='Capitulos de: Angel' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=740' style='font-size: 11px;'>Capitulos de: Angel</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=33' title='Capitulos de: Angel o demonio'><img class='ict' src='http://3.bp.blogspot.com/-6-sbY8M_Y8Y/TnG79MJv8oI/AAAAAAAADac/xzCxgIEC6-w/s400/angel-o-demonio-1-series-danko.jpg' alt='Capitulos de: Angel o demonio' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=33' style='font-size: 11px;'>Capitulos de: Angel o demonio</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=34' title='Capitulos de: Angeles en America'><img class='ict' src='http://2.bp.blogspot.com/-Qd2DIHJWmSQ/TnHHrthk7LI/AAAAAAAAG7s/c_XZUV-LH2E/s1600/angeles-en-america-seriesdanko.jpg' alt='Capitulos de: Angeles en America' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=34' style='font-size: 11px;'>Capitulos de: Angeles en America</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=36' title='Capitulos de: Any Human Heart'><img class='ict' src='http://2.bp.blogspot.com/_HixxA9qiz98/TSrRgyjOdyI/AAAAAAAADd8/lSNxGUxnKno/s1600/any-human-heart-seriesdanko.jpg' alt='Capitulos de: Any Human Heart' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=36' style='font-size: 11px;'>Capitulos de: Any Human Heart</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=37' title='Capitulos de: Apocalipsis de Stephen King'><img class='ict' src='http://4.bp.blogspot.com/-QTlHA7bK_SQ/TnHIMzxpIxI/AAAAAAAAG70/6XEXkaQGlqM/s200/apocalipsis-seriesdanko.jpg' alt='Capitulos de: Apocalipsis de Stephen King' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=37' style='font-size: 11px;'>Capitulos de: Apocalipsis de Stephen King</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=38' title='Capitulos de: Apocalipsis:La segunda guerra mundial'><img class='ict' src='http://1.bp.blogspot.com/_HixxA9qiz98/TMQYYH4-StI/AAAAAAAAB3o/XLRrDnVGpe0/s1600/Apocalipsis-La+segunda+guerra+mudial-seriesdanko.jpg' alt='Capitulos de: Apocalipsis:La segunda guerra mundial' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=38' style='font-size: 11px;'>Capitulos de: Apocalipsis:La segunda guerra mundial</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=734' title='Capitulos de: Appropiate Adult'><img class='ict' src='http://2.bp.blogspot.com/-GOgh__CpQkE/TnnhS6ZnBOI/AAAAAAAAHBU/JJCWViOp9Do/s400/appropriate-adult-seriesdanko.jpg' alt='Capitulos de: Appropiate Adult' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=734' style='font-size: 11px;'>Capitulos de: Appropiate Adult</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=39' title='Capitulos de: Aqui no hay quien viva'><img class='ict' src='http://3.bp.blogspot.com/-MiRd_HEeQFU/ToYzQVShs8I/AAAAAAAADww/3D6Ym9BDrNQ/s400/ANHQV%2BT1.bmp' alt='Capitulos de: Aqui no hay quien viva' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=39' style='font-size: 11px;'>Capitulos de: Aqui no hay quien viva</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=40' title='Capitulos de: Arena mix'><img class='ict' src='http://1.bp.blogspot.com/_KLLhWj6ZRrE/TDfGcZX2n5I/AAAAAAAAAYA/oUjLZJX7xXo/s200/arena-mix-seriesdanko.com' alt='Capitulos de: Arena mix' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=40' style='font-size: 11px;'>Capitulos de: Arena mix</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=41' title='Capitulos de: Armas del futuro'><img class='ict' src='http://4.bp.blogspot.com/_HixxA9qiz98/TUkhuZyn8gI/AAAAAAAADwc/l8vZvwWr9O8/s1600/armas%2Bdel%2Bfuturo.jpg' alt='Capitulos de: Armas del futuro' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=41' style='font-size: 11px;'>Capitulos de: Armas del futuro</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=42' title='Capitulos de: Army wives'><img class='ict' src='http://4.bp.blogspot.com/-ZNQx3dbCgdM/TnHOrblXnXI/AAAAAAAADa0/blDnB2TBQ98/s400/army_wives_1-seriesdanko.jpg' alt='Capitulos de: Army wives' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=42' style='font-size: 11px;'>Capitulos de: Army wives</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=43' title='Capitulos de: Arriba y Abajo'><img class='ict' src='http://2.bp.blogspot.com/-rDSPOZEzKuM/TZq_9fcowhI/AAAAAAAAEmY/2KsK9MGgNOA/s1600/mentes_en_shock-seriesdanko.jpg' alt='Capitulos de: Arriba y Abajo' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=43' style='font-size: 11px;'>Capitulos de: Arriba y Abajo</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=44' title='Capitulos de: Ashes to Ashes'><img class='ict' src='http://4.bp.blogspot.com/_HixxA9qiz98/TMp5jfkWekI/AAAAAAAACF4/2X5KST_mTWE/s1600/Ashes-to-Ashes-seriesdanko.jpg' alt='Capitulos de: Ashes to Ashes' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=44' style='font-size: 11px;'>Capitulos de: Ashes to Ashes</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=45' title='Capitulos de: Assassin´s Creed (Lineage)'><img class='ict' src='http://4.bp.blogspot.com/-uNiPWro4Lds/TnHIt1kJsUI/AAAAAAAAG78/gVuJdH4yJ1I/s1600/assasins-creed-seriesdanko.jpg' alt='Capitulos de: Assassin´s Creed (Lineage)' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=45' style='font-size: 11px;'>Capitulos de: Assassin´s Creed (Lineage)</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=46' title='Capitulos de: Atila'><img class='ict' src='http://2.bp.blogspot.com/_HixxA9qiz98/TIS3gKhzIaI/AAAAAAAAAsQ/B-k98k2eGLo/s1600/Atila-series-danko.jpg' alt='Capitulos de: Atila' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=46' style='font-size: 11px;'>Capitulos de: Atila</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=47' title='Capitulos de: Atlantis'><img class='ict' src='http://4.bp.blogspot.com/-ld3BVsUFjc0/Tcjc3m_n2ZI/AAAAAAAAFQ4/qnTlod5xcZo/s1600/atlantis-seriesdanko.jpg' alt='Capitulos de: Atlantis' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=47' style='font-size: 11px;'>Capitulos de: Atlantis</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=48' title='Capitulos de: Autopista hacia el cielo'><img class='ict' src='http://proteneo.files.wordpress.com/2009/03/autopistahaciaelcielo_dvd1.jpg' alt='Capitulos de: Autopista hacia el cielo' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=48' style='font-size: 11px;'>Capitulos de: Autopista hacia el cielo</a></div><br><br></div><div style='float:left;width: 33%;text-align:center;'><a href='serie.php?serie=49' title='Capitulos de: Awkward'><img class='ict' src='http://4.bp.blogspot.com/-aU-aU34Yi0A/TigchhoX8bI/AAAAAAAAGTY/lUwuGHKIPMY/s1600/Awkward-seriesdanko.jpg' alt='Capitulos de: Awkward' height='184' width='120'></a><br><div style='text-align:center;line-height:20px;height:20px;'><a href='serie.php?serie=49' style='font-size: 11px;'>Capitulos de: Awkward</a></div><br><br></div></div></td></tr></tbody></table><div style='clear: both;'></div>
        patronvideos = "<div[^<]+<a href='(serie.php[^']+)' title='Capitulos de\: ([^']+)'><img class='ict' src='([^']+)'"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
            scrapedtitle = unicode(scrapedtitle,"utf-8",errors="replace").encode("utf-8")
            scrapedtitle = scrapedtitle.replace("&aacute","&aacute;")
            scrapedtitle = scrapedtitle.replace("&eacute","&eacute;")
            scrapedtitle = scrapedtitle.replace("&iacute","&iacute;")
            scrapedtitle = scrapedtitle.replace("&oacute","&oacute;")
            scrapedtitle = scrapedtitle.replace("&uacute","&uacute;")
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            scrapedurl = urlparse.urljoin( item.url , scrapedurl )
            itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot="" , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[seriesdanko.py] episodios")
    
    if config.get_platform()=="xbmc" or config.get_platform()=="xbmcdharma":
        import xbmc
        if config.get_setting("forceview")=="true":
            xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
            #xbmc.executebuiltin("Container.Content(Movies)")
        
    if "|" in item.url:
        url = item.url.split("|")[0]
        sw = True
    else:
        url = item.url
        sw = False
    # Descarga la página
    if item.extra:
        
        contenidos = item.extra
        #print contenidos
    else:
        data = scrapertools.downloadpageWithoutCookies(url)

    # Extrae las entradas
        if sw:
            try:
                datadict = eval( "(" + data + ")" )    
                data = urllib.unquote_plus(datadict["entry"]["content"]["$t"].replace("\\u00","%"))
                matches=[]
                matches.append(data)
            except:
                matches = []
        else:
            patronvideos = "entry-content(.*?)<div class='blog-pager' id='blog-pager'>"
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            
        if len(matches)>0:
            contenidos = matches[0].replace('"',"'").replace("\n","")
        else:
            contenidos = item.url
            if sw:
                url = item.url.split("|")[1]
                if not url.startswith("http://"):
                    url = urlparse.urljoin("http://www.seriesdanko.com",url)
                # Descarga la página
                data = scrapertools.downloadpageGzip(url)
                patronvideos  = "entry-content(.*?)<div class='post-footer'>"
                matches = re.compile(patronvideos,re.DOTALL).findall(data)
                if len(matches)>0:
                    contenidos = matches[0]
                
    patronvideos  = "<a href='([^']+)'>([^<]+)</a> <img(.+?)/>"
    matches = re.compile(patronvideos,re.DOTALL).findall(contenidos.replace('"',"'"))
    #print contenidos        
    try:
        plot = re.compile(r'(Informac.*?/>)</div>').findall(contenidos)[0]
        if len(plot)==0:
            plot = re.compile(r"(Informac.*?both;'>)</div>").findall(contenidos)[0]
        plot = re.sub('<[^>]+>'," ",plot)
    except:
        plot = ""

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("\n","").replace("\r","")
        scrapedtitle = scrapertools.remove_show_from_title(scrapedtitle,item.show)
        
        #[1x01 - Capitulo 01]
        #patron = "(\d+x\d+) - Capitulo \d+"
        #matches = re.compile(patron,re.DOTALL).findall(scrapedtitle)
        #print matches
        #if len(matches)>0 and len(matches[0])>0:
        #    scrapedtitle = matches[0]

        if "es.png" in match[2]:
            subtitle = " (Español)"
        elif "la.png" in match[2]:
            subtitle = " (Latino)"
        elif "vo.png" in match[2]:
            subtitle = " (Version Original)"
        elif "vos.png" in match[2]:
            subtitle = " (Subtitulado)"
        elif "ca.png"  in match[2]:
            subtitle = " (Catalan)"
        elif "ga.jpg"  in match[2]:
            subtitle = " (Gallego)"
        elif "eu.jpg"  in match[2]:
            subtitle = " (Euskera)"
        elif "ba.png"  in match[2]:
            subtitle = " (Bable)"
        else:
            subtitle = ""
        scrapedplot = plot
        scrapedurl = urlparse.urljoin(item.url,match[0]).replace("\n","").replace("\r","")
        if not item.thumbnail:
            try:
                scrapedthumbnail = re.compile(r"src=([^']+)'").findall(contenidos)[0]
            except:
                    scrapedthumbnail = ""
        else:
            scrapedthumbnail = item.thumbnail
        scrapedthumbnail = scrapedthumbnail.replace("\n","").replace("\r","")
        if item.fulltitle == '':
            item.fulltitle = scrapedtitle + subtitle 
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle+subtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fulltitle = item.fulltitle, show = item.show , context="4", folder=True) )

    #xbmc.executebuiltin("Container.Content(Movies)")
    
    if len(itemlist)==0:
        listvideos = servertools.findvideos(contenidos)
        
        for title,url,server in listvideos:
            
            if server == "youtube":
                scrapedthumbnail = "http://i.ytimg.com/vi/" + url + "/0.jpg"
            else:
                scrapedthumbnail = item.thumbnail
            scrapedtitle = title
            scrapedplot = ""
            scrapedurl = url
            
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", server=server, title=item.title +" "+ scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = scrapedtitle , folder=False) )

    return itemlist

def findvideos(item):
    logger.info("[seriesdanko.py] findvideos")
    
    # Descarga la página
    if config.get_platform()=="xbmceden":
        from core.subtitletools import saveSubtitleName
        saveSubtitleName(item)
    
    if "seriesdanko-rs.com" in item.url:
        data = scrapertools.downloadpageGzip(item.url).replace("\n","")
        patronvideos = "<tr><td class=('tam12'>.*?)</td></tr>"
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #for match in matches:
            #print match
        itemlist = []
        for match in matches:
            try:
                scrapedurl = urlparse.urljoin(item.url,re.compile(r"href='(.+?)'").findall(match)[0])
            except:continue
           
            try:
                scrapedthumbnail = re.compile(r"src='(.+?)'").findall(match)[1]
                if "megavideo" in scrapedthumbnail:
                    mega = " [Megavideo]"
                elif "megaupload" in scrapedthumbnail:
                    mega = " [Megaupload]"
                else:
                    mega = ""
                if not scrapedthumbnail.startswith("http"):
                    scrapedthumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
            except:continue
            try:
                subtitle = re.compile(r"src='(.+?)'").findall(match)[0]
                if "es.png" in subtitle:
                    subtitle = " (Español)"
                elif "la.png" in  subtitle:
                    subtitle = " (Latino)"
                elif "vo.png" in  subtitle:
                    subtitle = " (Version Original)"
                elif "vos.png" in  subtitle:
                    subtitle = " (Subtitulado)"
                elif "ca.png"  in match[2]:
                    subtitle = " (Catalan)"
                elif "ga.jpg"  in match[2]:
                    subtitle = " (Gallego)"
                elif "eu.jpg"  in match[2]:
                    subtitle = " (Euskera)"
                elif "ba.png"  in match[2]:
                    subtitle = " (Bable)"
                else:
                    subtitle = "(desconocido)"
                
                try:
                    opcion = re.compile(r"(Ver|Descargar)").findall(match)[0]
                except:
                    opcion = "Ver"
                
                scrapedtitle = opcion + " video" + subtitle + mega
            except:
                scrapedtitle = item.title
            scrapedplot = ""
            #scrapedthumbnail = item.thumbnail
            #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot, fulltitle = item.fulltitle, extra = item.thumbnail , fanart=item.thumbnail , folder=False) )    
    
    else:
        from core import servertools
        itemlist = servertools.find_video_items( item )
    
    return itemlist

def play(item):
    logger.info("[seriesdanko.py] play")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    return servertools.find_video_items(data=data)

def decodeHtmlentities(string):
    string = entitiesfix(string)
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string
