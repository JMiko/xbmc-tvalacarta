# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal EURONEWS
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "euronews"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[euronews.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="English", action="categorias", url="http://www.euronews.com") )

    data = scrapertools.cache_page("http://www.euronews.com/")
    '''
    <option  dir="ltr" style="text-align:left" lang="en" value="http://www.euronews.com/">English</option>
    <option class="alt"  dir="ltr" style="text-align:left" lang="fr" value="http://fr.euronews.com/">Français</option>
    <option  dir="ltr" style="text-align:left" lang="de" value="http://de.euronews.com/">Deutsch</option>
    <option class="alt"  dir="ltr" style="text-align:left" lang="it" value="http://it.euronews.com/">Italiano</option>
    '''
    patron = '<option.*?value="(http\://[a-z]+\.euronews\.com/)">([^<]+)</option>'
    matches = re.findall(patron,data,re.DOTALL)
    for url,idioma in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=idioma, action="categorias", url=url) )

    return itemlist

def categorias(item):
    logger.info("[euronews.py] categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    # Enlace a "Programas"
    patron = '<li class="menu-element-programs"><a href="([^"]+)">([^<]+)</a>'
    matches = re.findall(patron,data,re.DOTALL)
    for url,titulo in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="programas", url=urlparse.urljoin(item.url,url)) )

    itemlist.append( Item(channel=CHANNELNAME, title="", action="videos", url="") )

    # Restringe la búsqueda al bloque del menú de categorias
    data2 = scrapertools.get_match(data,'<ol id="categoryNav">(.*?)</ol>')
    '''
    <ol id="categoryNav">
    <li><a class="firstNavLink" href="/news/">News</a></li>
    <li><a href="/business/">Business</a></li>
    <li><a href="/sport/">Sport</a></li>
    <li><a href="/culture/">Culture</a></li>
    <li><a href="/nocomment/">no comment</a></li>
    <li><a href="/european-union/">European Affairs</a></li>
    <li><a href="/sci-tech/">Sci-tech</a></li>
    <li><a href="/travel/">Travel</a></li>
    <li><a href="/in-vogue/">In vogue</a></li>
    <li id="lastNavLink"><a href="/weather/">weather</a></li>    
    </ol>
    '''
    patron = '<li><a.*?href="([^"]+)">([^<]+)</a>'
    matches = re.findall(patron,data2,re.DOTALL)
    
    for url,titulo in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="videos", url=urlparse.urljoin(item.url,url)) )

    itemlist.append( Item(channel=CHANNELNAME, title="", action="videos", url="") )

    # Restringe la búsqueda al bloque del menú por continentes
    data2 = scrapertools.get_match(data,'<ol id="geographicNav">(.*?)</ol>')
    patron = '<li><a.*?href="([^"]+)">([^<]+)</a>'
    matches = re.findall(patron,data2,re.DOTALL)
    
    for url,titulo in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="videos", url=urlparse.urljoin(item.url,url)) )

    return itemlist

def programas(item):
    logger.info("[euronews.py] programas")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    '''
    <li>
    <a name="europe weekly"></a>
    <a class="imgWrap" href="/programas/europe-weekly/">
    <img src="http://static.euronews.com/articles/programs/160x90_europe-weekly.jpg" alt="" title="La tragedia en Bélgica marca la agenda europea" />
    </a>
    <div class="titleWrap">
    <h2  class="programTitle"><a href="/programas/europe-weekly/">europe weekly</a></h2>
    <h3  class="artTitle"><a href="/2012/03/16/la-tragedia-en-belgica-marca-la-agenda-europea/">La tragedia en Bélgica marca la agenda europea</a></h2>
    <p>	Bélgica está de luto por los niños fallecidos en el accidente de?</p>
    <span class="more-link" style="position:absolute;padding-right:0;padding-top:0;bottom:0;right:0px;">
    <a href="/programas/europe-weekly/">Más europe weekly?</a>
    </span>
    </div>
    </li>
    '''
    patron  = '<li>[^<]+'
    patron += '<a name="([^"]+)"></a>[^<]+'
    patron += '<a class="imgWrap" href="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.findall(patron,data,re.DOTALL)
    
    for titulo,url,thumbnail in matches:
        itemlist.append( Item(channel=CHANNELNAME, title=titulo, action="videos", url=urlparse.urljoin(item.url,url), thumbnail=thumbnail) )

    return itemlist

def videos(item):
    logger.info("[euronews.py] videos")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    # Videos destacados
    itemlist.extend(get_videos_destacados(item,data))
    
    # Videos con thumbnail
    itemlist.extend(get_videos_con_thumbnail(item,data))

    # Videos sin thumbnail
    itemlist.extend(get_videos_sin_thumbnail(item,data))

    return itemlist

def get_videos_destacados(item,data):
    logger.info("[euronews.py] get_videos_destacados")
    itemlist = []

    patron = '<div class="topStoryWrapper(.*?)</div>[^<]+</div>'
    matches = re.findall(patron,data,re.DOTALL)
    logger.info("[euronews.py] %d bloques de videos destacados" % len(matches))

    for match in matches:
        data2 = match
        '''
        <h2 class="topStoryTitle"><a href="/2012/03/23/the-pirates-hug-grant-cambia-de-registro/">The Pirates!: Hug Grant cambia de registro</a></h2>
        <p class="cet" style="margin-bottom:6px; margin-top:-10px;">23/03 15:42 CET</p> 
        <a class="topStoryImgLink" href="/2012/03/23/the-pirates-hug-grant-cambia-de-registro/"><span class="vid"></span><img src="http://static.euronews.com/articles/179852/400x225_179852.jpg" alt=" The Pirates!: Hug Grant cambia de registro" title="The Pirates!: Hug Grant cambia de registro" /></a>
        <div class="topStoryProd noKeyword" style="position:relative;height:207px;">
        <p>	El actor británico, mundialmente conocido por sus papeles de galán en películas románticas, protagoniza su primer film de animación en tres dimensiones. Su título es The Pirates!, una cinta de Peter Lord para todos los públicos que cuenta la história de tres bucaneros que?</p>
        <p class="more-link" style="position:absolute;padding-right:0;padding-top:0;bottom:-20px;right:0px;"><a href="/programas/cinema/">Más Cinema?</a></p>              </div>
        '''
        '''
        <h2 class="topStoryTitle"><a  href="/2012/03/13/todos-los-caminos-llevan-a-ucrania/">Todos los caminos llevan a Ucrania</a></h2>
        <p class="cet" style="margin-bottom:6px; margin-top:-10px;">13/03 20:21 CET</p>
        <a class="topStoryImgLink" href="/2012/03/13/todos-los-caminos-llevan-a-ucrania/"><span class="vid"></span><img src="http://static.euronews.com/articles/178820/287x161_178820.jpg" alt=": Todos los caminos llevan a Ucrania" title="Todos los caminos llevan a Ucrania" /></a>
        <div class="topStoryProd noKeyword" style="position:relative;height:207px;">
        <p>	Por avión, en tren, y en coche. Tres alternativas para los aficionados que visiten Ucrania durante la próxima Eurocopa (8 de junio-1 de julio).
        Los transportes eran una de las grandes asignaturas pendientes del Comité Organizador.         
        Las distancias entre las cuatro sedes, Kiev, Donetsk, Lviv y Járkov, son importantes, y la UEFA había manifestado su preocupación, como?</p>
        '''
        patron  = '<h2 class="topStoryTitle"><a\s+href="([^"]+)">([^>]+)</a></h2>.*?'
        patron += '<p class="cet"[^>]+>([^<]+)</p>.*?'
        patron += '<img src="([^"]+)".*?<p>([^<]+)</p>'

        matches2 = re.findall(patron,data2,re.DOTALL)

        for url,title,emission_date,thumbnail,plot in matches2:
            scrapedtitle = title.strip()+" ("+scrapertools.htmlclean(emission_date)+")"
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

        '''
        <span class="vid"></span>              <img src="http://static.euronews.com/images_news/img_287X161_tim-burton-lemag.jpg" alt="Todo Tim Burton" title="Todo Tim Burton" />
        </a>
        <div class="themePromo noKeyword" style="position:relative;height:150px;">
        <p class="cet"><a href="/programas/lemag/">LE MAG</a> |07/03 15:59 CET</p>
        <h2 style="font-size: 18px;"><a href="/2012/03/07/todo-tim-burton/">Todo Tim Burton</a></h2>
        <p>	Tim Burton, sus personajes, dibujos, y cuadros nos esperan en París.
        La Cinemateca repasa sus 27 años de carrera cinematográfica a?</p>
        '''
        '''
        <span class="vid"></span>              <img src="http://static.euronews.com/images_news/img_287X161_1303-gaddafi-sarkozy-2007-france-campaign.jpg" alt="Resurgen las sospechas de que Gadafi financió la campaña de Sarkozy en 2007" title="Resurgen las sospechas de que Gadafi financió la campaña de Sarkozy en 2007" />
        </a>
        <div class="themePromo noKeyword" style="position:relative;height:150px;">
        <p class="cet">13/03 17:33 CET</p>
        <h2 style="font-size: 18px;"><a href="/2012/03/13/sarkozy-remonta-en-los-sondeos-mientras-aumentan-las-dudas-sobre-su-vinculacion/">Resurgen las sospechas de que Gadafi financió la campaña de Sarkozy en 2007</a></h2>
        <p>	Buenas y malas noticias para Nicolas Sarkozy. El presidente francés ha superado por primera vez a Francois Hollande en los sondeos. Al?</p>
        '''
        patron  = '<img src="([^"]+)" alt="([^"]+)".*?'
        patron += '<p class="cet">(.*?)</p>[^<]+'
        patron += '<h2 style="font-size: 18px;"><a href="([^"]+)">[^<]+</a></h2>[^<]+'
        patron += '<p>([^>]+)</p>'

        matches2 = re.findall(patron,data2,re.DOTALL)

        for thumbnail, title, show_emission_date, url, plot in matches2:
            scrapedtitle = title.strip()+" ("+scrapertools.htmlclean(show_emission_date)+")"
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

    return itemlist

def get_videos_con_thumbnail(item,data):
    logger.info("[euronews.py] get_videos_destacados")
    itemlist = []

    # Videos nocomment
    '''
    <a href="/nocomment/2011/04/10/aniversario/" class="topStory"><img src="http://static.euronews.com/images_news/img_287X161_nc-1004-KATYN-memorial.jpg" alt="Aniversario" width="287" height="161" /><span class="inner-overlay-wrap"><span class="inner-overlay"><strong>Aniversario</strong> <em>nocomment | 10/04 11:36 CET</em></span></span></a>
    '''
    patron  = '<a href="(/nocomment/[^"]+)" class="topStory"><img src="([^"]+)" alt="([^"]+)"'
    matches = re.findall(patron,data,re.DOTALL)

    for url,thumbnail,title in matches:
        scrapedtitle = title.strip()
        scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

    # Videos normales con thumbnail
    patron = '<div class="subcategoryList clear">(.*?)</div>[^<]+</div>'
    matches = re.findall(patron,data,re.DOTALL)
    logger.info("[euronews.py] %d bloques de videos con thumbnail" % len(matches))

    for match in matches:
        data2 = match
        '''
        <span class="artDate"><a    href="/programs/cinema/">CINEMA</a> | 22/03 17:24 CET</span>
        <h2  class="themeArtTitle"><a href="/2012/03/22/werner-herzog-tackles-texas-killings/">Werner Herzog tackles Texas killings</a></h2>
        <p>	After prehistoric cave paintings and bear enthusiasts, the acclaimed German filmmaker Werner Herzog has turned his attention to a triple?</p>                  </div>
        </li>
        '''
        '''
        <span class="vid"></span>                    <img src="http://static.euronews.com/articles/179862/130x73_179862.jpg" alt="world Obama nombra a Jim Yong King para presidir el Banco Mundial" title="Obama nombra a Jim Yong King para presidir el Banco Mundial" />
        </a>
        <div class="titleWrap" style="position:relative;height:77px;">
        <span class="artDate">23/03 16:49 CET</span>
        <h2  class="themeArtTitle"><a href="/2012/03/23/obama-nombra-a-jim-yong-king-para-presidir-el-banco-mundial/">Obama nombra a Jim Yong King para presidir el Banco Mundial</a></h2>
        <p>	Barack Obama nombra a un candidato sorpresa para presidir el Banco?</p>                  </div>
        </li>
        '''
        patron  = '<img src="([^"]+)".*?'
        patron += '<span class="artDate">(.*?)</span>[^<]+'
        patron += '<h2\s+class="themeArtTitle"><a href="([^"]+)">([^<]+)</a></h2>(.*?)</div>'
        matches2 = re.findall(patron,data2,re.DOTALL)

        for thumbnail, show_emission_date, url, title, plot in matches2:
            scrapedtitle = title.strip() + " (" + scrapertools.htmlclean(show_emission_date) + ")"
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

        '''
        <li>
        <a class="imgWrap" href="/2012/03/12/anja-parson-se-despide-del-esqui-alpino/">
        <span class="vid"></span>
        <img src="http://static.euronews.com/articles/178618/287x161_178618.jpg" alt="sport: Anja Pärson se despide del esquí alpino" title="Anja Pärson se despide del esquí alpino" />
        </a>
        <div class="titleWrap" style="position:relative;height:77px;">
        <span >12/03 14:54 CET</span>
        <h2  class="artTitle"><a href="/2012/03/12/anja-parson-se-despide-del-esqui-alpino/">Anja Pärson se despide del esquí alpino</a></h2>
        <p>	La esquiadora sueca ha anunciado su retirada después de 14 años en la?</p>
        </div>
        </li>
        '''
        patron  = '<img src="([^"]+)".*?'
        patron += '<span >(.*?)</span>[^<]+'
        patron += '<h2\s+class="artTitle"><a href="([^"]+)">([^<]+)</a></h2>(.*?)</div>'
        matches2 = re.findall(patron,data2,re.DOTALL)

        for thumbnail, show_emission_date, url, title, plot in matches2:
            scrapedtitle = title.strip() + " (" + scrapertools.htmlclean(show_emission_date) +")"
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

        '''
        <img src="http://static.euronews.com/articles/178066/287x161_178066.jpg" alt="El CNT rechaza el proyecto autonomista en el este de Libia" />
        </a>
        <div class="titleWrap" style="position:relative;height:77px;">
        <p class="cet">Libia - 07/03 05:03 CET</p>
        <h2  class="themeArtTitle"><a href="/2012/03/07/el-cnt-rechaza-el-proyecto-autonomista-en-el-este-de-libia/">El CNT rechaza el proyecto autonomista en el este de Libia</a></h2>
        <p>	El gobierno libio denuncia un compló árabe tras la declaración de?</p>
        '''
        patron  = '<img src="([^"]+)".*?'
        patron += '<p class="cet">(.*?)</p>[^<]+'
        patron += '<h2\s+class="themeArtTitle"><a href="([^"]+)">([^<]+)</a></h2>(.*?)</div>'
        matches2 = re.findall(patron,data2,re.DOTALL)

        for thumbnail, show_emission_date, url, title, plot in matches2:
            scrapedtitle = title.strip() + " (" + scrapertools.htmlclean(show_emission_date) +")"
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

        '''
        <span class="vid"></span>                        <img src="http://static.euronews.com/articles/179500/130x73_179500.jpg" alt="cinema: Vuelve Blancanieves con Julia Roberts en el papel de mala" title="Vuelve Blancanieves con Julia Roberts en el papel de mala" />
        </a>
        <div class="titleWrap">
        <h2 class="artTitle"><a href="/2012/03/20/vuelve-blancanieves-con-julia-roberts-en-el-papel-de-mala/">Vuelve Blancanieves con Julia Roberts en el papel de mala</a></h2>
        <p>	Vuelve el clásico de Blancanieves. Tarsem Singh regresa a la gran?</p>                        <span class="artDate">20/03 17:13 CET</span>
        </div>
        </li>
        '''
        patron  = '<img src="([^"]+)".*?'
        patron += '<h2\s+class="artTitle"><a href="([^"]+)">([^<]+)</a></h2>(.*?)</div>'
        matches2 = re.findall(patron,data2,re.DOTALL)

        for thumbnail, url, title, plot in matches2:
            scrapedtitle = title.strip()
            scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = thumbnail
            scrapedplot = scrapertools.htmlclean(plot).strip()
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )



    return itemlist

def get_videos_sin_thumbnail(item,data):
    logger.info("[euronews.py] get_videos_destacados")
    itemlist = []

    # <li>02/03 - <a href="/programas/lemag/"><span style="font-weight: normal;">le mag</span></a> -  <a href="/2012/03/02/el-color-echa-un-pulso-al-negro-en-las-pasarelas-de-paris/">El color echa un pulso al negro en las pasarelas de París</a></li>
    patron = '<li>([^<]+)<a[^>]+><span style="font-weight\: normal\;">([^<]+)</span></a> -  <a href="([^"]+)">([^<]+)</a></li>'
    matches = re.findall(patron,data,re.DOTALL)
    for emission_date, show, url, title in matches:
        scrapedtitle = title.strip() + " (" + show + ") " + emission_date
        scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )

    # <li>19/03 -   <a href="/2012/03/19/apple-repartira-dividendos-por-primera-vez-desde-1995/">Apple repartirá dividendos por primera vez desde 1995</a></li>
    # <li>16/03 - <a href="/programas/business-weekly/"><span style="font-weight: normal;">business weekly</span></a> -  <a href="/2012/03/16/la-fed-se-reserva-una-nueva-inyeccion-de-liquidez/">La Fed se reserva una nueva inyección de liquidez</a></li>
    patron = '<li>([^<]+)<a href="([^"]+)">([^<]+)</a></li>'
    matches = re.findall(patron,data,re.DOTALL)
    for emmision_date, url, title in matches:
        scrapedtitle = title.strip() + " " + emission_date
        scrapedtitle = scrapedtitle.replace("&#8220;",'"').replace("&#8221;",'"')
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle, action="play", url=urlparse.urljoin(item.url,url), thumbnail=scrapedthumbnail, plot=scrapedplot, folder=False) )
    
    return itemlist

def play(item):
    logger.info("[euronews.py] play")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    #swfobject.embedSWF("/media/Player6_1.swf", "article-player-new", 606, 371 , "9.0.0", "", {  videofile:"flv/lemag/120315_CISU_180C0_S" , preroll:1, autoplay:0, img:"/images_news/img_606X341_Cartoonmovie.jpg",nedstat:"lifestyle.cinema.179146",lng:"es", title:"cartoon-movie-shows-depth-of-european-talent"}, {"wmode":"opaque", "allowfullscreen":"true", "allowscriptaccess":"sameDomain"}, {});
    patron  = 'videofile\:"([^"]+)"'
    matches = re.findall(patron,data,re.DOTALL)
    
    #http://video.euronews.com/flv/lemag/120315_CISU_180C0_S.flv
    for url in matches:
        mediaurl = "http://video.euronews.com/"+url+".flv"
        itemlist.append( Item(channel=CHANNELNAME, title=item.title, action="play", url=mediaurl, thumbnail=item.thumbnail) )

    return itemlist
