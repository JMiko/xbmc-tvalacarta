# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para El Trece (Argentina)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item

CHANNEL = "eltrece"
MAIN_URL = "http://www.eltrecetv.com.ar/"
DEBUG = (config.get_setting("debug")=="true")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[eltrece.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=CHANNEL, title="Destacadas" , action="novedades", url=MAIN_URL, extra=". Comentados", folder=True) )
    itemlist.append( Item(channel=CHANNEL, title="Capítulos completos" , action="novedades", url=MAIN_URL, extra="Capitulos completos", folder=True) )
    itemlist.append( Item(channel=CHANNEL, title="+ Vistos" , action="novedades", url=MAIN_URL, extra="Notas m", folder=True) )
    itemlist.append( Item(channel=CHANNEL, title="Últimos" , action="novedades", url=MAIN_URL, extra="Últimos", folder=True) )
    itemlist.append( Item(channel=CHANNEL, title="Exclusivo eltrecetv.com" , action="novedades", url=MAIN_URL, extra="En exclusivo", folder=True) )
    itemlist.append( Item(channel=CHANNEL, title="Programas" , action="programas", url=MAIN_URL, folder=True) )

    return itemlist

def novedades(item):
    logger.info("[eltrece.py] novedades")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    try:
        pagina_siguiente = scrapertools.get_match(data,'<div class="grid960-list".*?<div class="item-list"><ul class="pager pager-load-more[^<]+<li class="pager-next first last"><a href="([^"]+)">Mostrar m')
    except:
        pagina_siguiente=""
    logger.info("pagina_siguiente="+pagina_siguiente)

    try:
        data = scrapertools.get_match(data,'<div class="view-content"[^<]+<div class="grid960-list"[^<]+<h3>'+item.extra+'(.*?)</div>\s+</div>[^<]+')
    except:
        pass
    logger.info("data="+data)

    '''
    <div class="views_row views_row_5 views_row_odd grid_3 alpha">  
    <a href="/farsantes/pedro-esta-lleno-de-dudas-y-solo-piensa-en-guillermo_062712"><img typeof="foaf:Image" src="http://static.eltrecetv.com.ar/sites/default/files/styles/180x101/public/fa_3.jpg" width="180" height="101" alt="Pedro, personaje interpretado por Benjamín Vicuña en Farsantes" title="Pedro está lleno de dudas y sólo piensa en Guillermo" /></a>    
    <h5><a href="/farsantes">Farsantes</a></h5>    
    <h4><a href="/farsantes/pedro-esta-lleno-de-dudas-y-solo-piensa-en-guillermo_062712">Pedro está lleno de dudas y sólo piensa en Guillermo</a></h4> 
    '''
    patron  = '<a href="([^"]+)"><img typeof="[^"]+" src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<h5><a href="[^"]+">([^<]+)</a></h5>[^<]+'
    patron += '<h4><a href="[^"]+">([^<]+)</a></h4>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,show,title in matches:
        show_name = show.strip()
        if show_name!="":
            show_name = show_name+": "
        scrapedtitle = show_name+title.strip()
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, title=scrapedtitle , action="play" , server="eltrece", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    # Paginación
    if pagina_siguiente!="":
        itemlist.append( Item(channel=CHANNEL, title=">> Página siguiente" , action="novedades", url=urlparse.urljoin(item.url,pagina_siguiente), folder=True) )

    return itemlist

def programas(item):
    logger.info("[eltrece.py] programas")

    itemlist=[]

    # Descarga la página y parsea los programas que aparecen
    data = scrapertools.cache_page( item.url )
    bloque = scrapertools.get_match(data,"<h3>Programas</h3>(.*?)</ul>")
    new_itemlist = parse_programas(bloque,item)
    
    # Obtiene el resto de páginas por AJAX
    num_page = 1
    while len(new_itemlist)>0:

        # Añade el último bloque
        itemlist.extend(new_itemlist)

        # Descarga el siguiente
        bloque = programas_page(num_page)
        num_page = num_page + 1

        # Lo parsea
        new_itemlist = parse_programas(bloque,item)

    return itemlist

def programas_page(num_page):
    post = "view_name=menu_programas&view_display_id=block&view_args=&view_path=homepage&view_base_path=null&view_dom_id=0da8f6f4dc0b220c56bbd942110034da&pager_element=100&page=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C"+str(num_page)+"&ajax_html_ids%5B%5D=LR1&ajax_html_ids%5B%5D=facebook-jssdk&ajax_html_ids%5B%5D=twttrHubFrameSecure&ajax_html_ids%5B%5D=twttrHubFrame&ajax_html_ids%5B%5D=page&ajax_html_ids%5B%5D=header-top-wrapper&ajax_html_ids%5B%5D=header-top&ajax_html_ids%5B%5D=eplAdDivTop950x50&ajax_html_ids%5B%5D=eplParentContainer416054&ajax_html_ids%5B%5D=ifrab2493ec13af6709_852f43336d5b948e&ajax_html_ids%5B%5D=block-views-grilla-block-grilla-reducida&ajax_html_ids%5B%5D=block-eltrecetv-login-button-login&ajax_html_ids%5B%5D=eltrecetv-login-loading&ajax_html_ids%5B%5D=eltrecetv-login-user&ajax_html_ids%5B%5D=eltrecetv-login-user-data&ajax_html_ids%5B%5D=header-bottom-wrapper&ajax_html_ids%5B%5D=header&ajax_html_ids%5B%5D=block-eltrecetv-encabezado-sitio&ajax_html_ids%5B%5D=block-menu-menu-menu-superior&ajax_html_ids%5B%5D=content-wrapper&ajax_html_ids%5B%5D=eplAdDivSkyDER120x600&ajax_html_ids%5B%5D=eplParentContainer344575&ajax_html_ids%5B%5D=ifrf97ad35b2c2f4201_d2bd4a1f8421a23e&ajax_html_ids%5B%5D=eplAdDivSkyIZQ120x600&ajax_html_ids%5B%5D=eplParentContainer344575&ajax_html_ids%5B%5D=ifrf97ad35b2c2f4201_6e84ec010ca3c2c9&ajax_html_ids%5B%5D=content-left&ajax_html_ids%5B%5D=block-views-menu-programas-block&ajax_html_ids%5B%5D=eplAdDivLeft160x600&ajax_html_ids%5B%5D=widget-radios-eltrecetv_160x256&ajax_html_ids%5B%5D=bloque-caja-shopping&ajax_html_ids%5B%5D=content-top&ajax_html_ids%5B%5D=block-search-form&ajax_html_ids%5B%5D=search-block-form&ajax_html_ids%5B%5D=edit-search-block-form--2&ajax_html_ids%5B%5D=edit-actions&ajax_html_ids%5B%5D=edit-submit&ajax_html_ids%5B%5D=block-eltrecetv-seguinos-sitio&ajax_html_ids%5B%5D=block-tags-temas&ajax_html_ids%5B%5D=temas&ajax_html_ids%5B%5D=ver_mas_temas&ajax_html_ids%5B%5D=main-wrapper&ajax_html_ids%5B%5D=main-content&ajax_html_ids%5B%5D=block-views-grilla-block-vivo-home&ajax_html_ids%5B%5D=block-views-grilla-block-vivo-home-player&ajax_html_ids%5B%5D=block-views-notas-home-block-sticky&ajax_html_ids%5B%5D=eplAdDiv728x90&ajax_html_ids%5B%5D=eplParentContainer308137&ajax_html_ids%5B%5D=ifrda95f8a10298b029_45641682e5b5c7d7&ajax_html_ids%5B%5D=block-quicktabs-notas-home&ajax_html_ids%5B%5D=quicktabs-notas_home&ajax_html_ids%5B%5D=quicktabs-tab-notas_home-0&ajax_html_ids%5B%5D=quicktabs-tab-notas_home-1&ajax_html_ids%5B%5D=quicktabs-tab-notas_home-2&ajax_html_ids%5B%5D=quicktabs-tab-notas_home-3&ajax_html_ids%5B%5D=quicktabs-tab-notas_home-4&ajax_html_ids%5B%5D=quicktabs-container-notas_home&ajax_html_ids%5B%5D=quicktabs-tabpage-notas_home-0&ajax_html_ids%5B%5D=quicktabs-tabpage-notas_home-1&ajax_html_ids%5B%5D=quicktabs-tabpage-notas_home-2&ajax_html_ids%5B%5D=quicktabs-tabpage-notas_home-3&ajax_html_ids%5B%5D=quicktabs-tabpage-notas_home-4&ajax_html_ids%5B%5D=content-bottom&ajax_html_ids%5B%5D=eplAdDiv2x728x90&ajax_html_ids%5B%5D=eplParentContainer344568&ajax_html_ids%5B%5D=ifrf01eb687270ed3dd_8a548f0858499f4e&ajax_html_ids%5B%5D=block-eltrecetv-ajax-poll-encuesta&ajax_html_ids%5B%5D=block-poll-recent&ajax_html_ids%5B%5D=load-poll-form&ajax_html_ids%5B%5D=poll-view-voting&ajax_html_ids%5B%5D=edit-choice&ajax_html_ids%5B%5D=edit-choice-702&ajax_html_ids%5B%5D=edit-choice-703&ajax_html_ids%5B%5D=edit-vote&ajax_html_ids%5B%5D=load-poll-result&ajax_html_ids%5B%5D=block-views-link-libres-home-block&ajax_html_ids%5B%5D=footer-wrapper2&ajax_html_ids%5B%5D=footer&ajax_html_ids%5B%5D=block-views-destacados-home-block&ajax_html_ids%5B%5D=eplAdDivBottom1x300x250&ajax_html_ids%5B%5D=eplParentContainer309424&ajax_html_ids%5B%5D=ifr6dd5f2e3d8e9e896_d139683922ad9635&ajax_html_ids%5B%5D=block-tags-mas-buscados&ajax_html_ids%5B%5D=footer-wrapper1&ajax_html_ids%5B%5D=footer-bottom&ajax_html_ids%5B%5D=block-eltrecetv-pie-sitio&ajax_html_ids%5B%5D=footer-links&ajax_html_ids%5B%5D=epl4iframe&ajax_html_ids%5B%5D=fb-root&ajax_html_ids%5B%5D=fb_xdm_frame_http&ajax_html_ids%5B%5D=fb_xdm_frame_https&ajax_html_ids%5B%5D=fancybox-tmp&ajax_html_ids%5B%5D=fancybox-loading&ajax_html_ids%5B%5D=fancybox-overlay&ajax_html_ids%5B%5D=fancybox-wrap&ajax_html_ids%5B%5D=fancybox-outer&ajax_html_ids%5B%5D=fancybox-bg-n&ajax_html_ids%5B%5D=fancybox-bg-ne&ajax_html_ids%5B%5D=fancybox-bg-e&ajax_html_ids%5B%5D=fancybox-bg-se&ajax_html_ids%5B%5D=fancybox-bg-s&ajax_html_ids%5B%5D=fancybox-bg-sw&ajax_html_ids%5B%5D=fancybox-bg-w&ajax_html_ids%5B%5D=fancybox-bg-nw&ajax_html_ids%5B%5D=fancybox-content&ajax_html_ids%5B%5D=fancybox-close&ajax_html_ids%5B%5D=fancybox-title&ajax_html_ids%5B%5D=fancybox-left&ajax_html_ids%5B%5D=fancybox-left-ico&ajax_html_ids%5B%5D=fancybox-right&ajax_html_ids%5B%5D=fancybox-right-ico&ajax_page_state%5Btheme%5D=eltrecetv2012&ajax_page_state%5Btheme_token%5D=vF59WMgH8-A0zqpd7znlhi9ReXg5amBfPU_i7gn-EPQ&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.base.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.theme.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Flibraries%2Fjquery.fancybox%2Ffancybox%2Fjquery.fancybox-1.3.4.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv%2Fcss%2Feltrecetv.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fcss%2Feltrecetv_comment.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_galleria%2Fcss%2Feltrecetv_galleria.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_grilla%2Fcss%2Fgrilla_reducida.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_grilla%2Fcss%2Fgrilla_vivo.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_jwplayer%2Fcss%2Fjwplayer.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fcss%2Flogin.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fcss%2Fwizard.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fcss%2Ffacebook.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_twitter%2Fcss%2Ftwitter.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fentrevistas%2Fcss%2Fentrevistas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Flink_libres%2Fcss%2Flink_libres.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fnotas%2Fcss%2Fnotas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fprogramas%2Fcss%2Fprogramas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fcss%2Fsocial_widgets.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_eltrecetv%2Fcss%2Fsocial_widgets_eltrecetv.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_facebook%2Fcss%2Fsocial_widgets_facebook.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_google%2Fcss%2Fsocial_widgets_google.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_pinterest%2Fcss%2Fsocial_widgets_pinterest.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_twitter%2Fcss%2Fsocial_widgets_twitter.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fcomment%2Fcomment.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_api%2Fdate.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_popup%2Fthemes%2Fdatepicker.1.7.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_repeat_field%2Fdate_repeat_field.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffield%2Ftheme%2Ffield.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fnode%2Fnode.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fpoll%2Fpoll.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsearch%2Fsearch.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fuser%2Fuser.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fcss%2Fviews.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Ftags%2Fcss%2Ftags.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fquicktabs%2Fcss%2Fquicktabs.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fckeditor%2Fckeditor.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fctools%2Fcss%2Fctools.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdhtml_menu%2Fdhtml_menu.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fextlink%2Fextlink.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fhtml.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Flayout.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fstyle.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fquicktabs.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fprint.css%5D=1&ajax_page_state%5Bjs%5D%5B0%5D=1&ajax_page_state%5Bjs%5D%5B1%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fjquery%2Fjquery.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.once.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fdrupal.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fjquery.fancybox%2Ffancybox%2Fjquery.fancybox-1.3.4.pack.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fswfobject%2Fswfobject.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fjquery.countdown%2Fjquery.countdown1.2.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fjs%2Fga_social_tracking_min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fjs%2Fsocialwidgets.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_eltrecetv%2Fjs%2Fsocialwidgets.eltrecetv.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_facebook%2Fjs%2Fsocialwidgets.facebook.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_google%2Fjs%2Fsocialwidgets.google.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_pinterest%2Fjs%2Fsocialwidgets.pinterest.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_twitter%2Fjs%2Fsocialwidgets.twitter.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fui%2Fexternal%2Fjquery.cookie.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fmisc%2Fjquery.form.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fajax.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv%2Fjs%2Feltrecetv.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fjs%2Feltrecetv_comment.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fjs%2Feltrecetv_comment_validate.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_galleria%2Fjs%2Feltrecetv_galleria.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_grilla%2Fjs%2Feltrecetv.grilla.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_jwplayer%2Fjs%2Feltrecetv.jwplayer.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fjs%2Feltrecetv.login.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fjs%2Ffb_connect.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fjs%2Feltrecetv.login.facebook.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_twitter%2Fjs%2Feltrecetv.login.twitter.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fentrevistas%2Fjs%2Feltrecetv_entrevistas.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feplanning4%2Fjs%2Feplanning4.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fprogramas%2Fjs%2Feltrecetv_programas.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fviews_ajax_refresh%2Fjs%2Fviews_ajax_refresh.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fviews_load_more%2Fviews_load_more.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Flanguages%2Fes_jYWsqXmILN_z1Ny5EhmoXZbo1PGwKV6IlxIi-05DMyA.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Ffb%2Ffb_stream.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdhtml_menu%2Fdhtml_menu.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fextlink%2Fextlink.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fbase.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fprogress.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fajax_view.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fajax_poll%2Fajax_poll.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_ajax_poll%2Feltrecetv_ajax_poll.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.form.js%5D=1&ajax_page_state%5Bjs%5D%5Bhttp%3A%2F%2Fwww.eltrecetv.com.ar%2Fsites%2Fall%2Fmodules%2Fcontrib%2Fpinned_site%2Fjs%2Fpinned_site.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fquicktabs%2Fjs%2Fquicktabs.js%5D=1"
    data = scrapertools.cache_page( "http://www.eltrecetv.com.ar/views/ajax" , post=post )
    logger.info("data="+data)

    data_json = jsontools.load_json(data)
    bloque=data_json[1]['data']
    logger.info("bloque="+bloque)

    return bloque

def parse_programas(bloque,item):
    patron  = '<li class="views-row views-row-[^"]+">[^<]+'
    patron += '<a href="([^"]+)">([^<]+)</a>\s+</li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, title=scrapedtitle , action="secciones", url=scrapedurl, folder=True) )

    return itemlist

def secciones(item):
    logger.info("[eltrece.py] secciones")
    itemlist = []

    '''
    <div id="block-eltrecetv-temporada-menu-temporada" class="block block-eltrecetv-temporada">
    <div class="item-list"><ul id="menu-temporada" class="menu-interno-programa grid_12 clearfix compentencia">
    <li class="active doubletext first"><a href="/el-diario-de-mariana-0">Momentos culminantes</a></li>
    <li class=" singletext"><a href="/el-diario-de-mariana/en-exclusiva">En exclusiva</a></li>
    <li class=" singletext last"><a href="/el-diario-de-mariana/conduccion">Conducción</a></li>
    </ul></div>
    </div>
    '''
    data=scrapertools.cache_page(item.url)
    data=scrapertools.get_match(data,'<ul id="menu-temporada" class="menu-interno-programa[^"]+">(.*?)</ul>')
    patron = '<li[^<]+<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for url,titulo in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=CHANNEL, title=titulo , action="episodios", url=scrapedurl, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[eltrece.py] episodios")

    # Descarga la página
    if item.extra=="":
        data = scrapertools.cache_page( item.url )
        data = scrapertools.get_match(data,'<div class="view-content"[^<]+<div class="grid960-list"[^<]+<h3>Últimos(.*?)</div>\s+</div>[^<]+')
    else:
        data = scrapertools.cache_page( item.url , post=item.extra)

        data_json = jsontools.load_json(data)
        logger.info("data_json="+str(data_json))
        data=data_json[1]['data']
        logger.info("data="+data)

    '''
    <div class="views_row views_row_4 views_row_even grid_3 alpha">  
    <a href="/periodismo-para-todos/periodismo-para-todos/00053539/megaminer%C3%AD-pol%C3%ADtica-y-negocios"><img typeof="foaf:Image" src="http://cdn.eltrecetv.com.ar/sites/default/files/styles/180x101/public/famatina-2.jpg" width="180" height="101" alt="" /></a>    
    <h5>        <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2012-07-15T21:30:00-03:00">15/07/2012</span>  </h5>  
    <h4><a href="/periodismo-para-todos/periodismo-para-todos/00053539/megaminer%C3%AD-pol%C3%ADtica-y-negocios">Megaminería, política y negocios</a></h4>    
    <span class="total_views">9,383</span>  </div>
    '''
    patron  = '<div class="views_row views_row_\d+ views_row_[^<]+'
    patron += '<a href="([^"]+)"><img typeof="foaf.Image" src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<h5>\s+<span[^>]+>([^<]+)</span>\s+</h5>[^<]+'
    patron += '<h4><a href="[^"]+">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,fecha,title in matches:
        scrapedtitle = title+" ("+fecha+")"
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, title=scrapedtitle , action="play" , server="eltrece", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=False) )

    # Paginación
    try:
        pagina_siguiente = "http://www.eltrecetv.com.ar/views/ajax"

        if item.extra=="":
            post = "view_name=temporada_notas&view_display_id=ultimos&view_args=57654%2F11&view_path=node%2F57654%2F11&view_base_path=null&view_dom_id=d8d00678dbab51e313e2d1fa657ded93&pager_element=0&page=1&ajax_html_ids%5B%5D=LR1&ajax_html_ids%5B%5D=facebook-jssdk&ajax_html_ids%5B%5D=twttrHubFrameSecure&ajax_html_ids%5B%5D=twttrHubFrame&ajax_html_ids%5B%5D=page&ajax_html_ids%5B%5D=header-top-wrapper&ajax_html_ids%5B%5D=header-top&ajax_html_ids%5B%5D=eplAdDivTop950x50&ajax_html_ids%5B%5D=eplParentContainer416054&ajax_html_ids%5B%5D=ifrab2493ec13af6709_e638aac69da1bff1&ajax_html_ids%5B%5D=block-views-grilla-block-grilla-reducida&ajax_html_ids%5B%5D=block-eltrecetv-login-button-login&ajax_html_ids%5B%5D=eltrecetv-login-loading&ajax_html_ids%5B%5D=eltrecetv-login-user&ajax_html_ids%5B%5D=eltrecetv-login-user-data&ajax_html_ids%5B%5D=header-bottom-wrapper&ajax_html_ids%5B%5D=header&ajax_html_ids%5B%5D=block-eltrecetv-encabezado-sitio&ajax_html_ids%5B%5D=block-menu-menu-menu-superior&ajax_html_ids%5B%5D=content-wrapper&ajax_html_ids%5B%5D=eplAdDivSkyDER120x600&ajax_html_ids%5B%5D=eplParentContainer344575&ajax_html_ids%5B%5D=ifrf97ad35b2c2f4201_849cb69ade8d1de4&ajax_html_ids%5B%5D=eplAdDivSkyIZQ120x600&ajax_html_ids%5B%5D=eplParentContainer344575&ajax_html_ids%5B%5D=ifrf97ad35b2c2f4201_a318cf1da6bd0bd2&ajax_html_ids%5B%5D=content-left&ajax_html_ids%5B%5D=block-views-menu-programas-block&ajax_html_ids%5B%5D=eplAdDivLeft160x600&ajax_html_ids%5B%5D=content-top&ajax_html_ids%5B%5D=block-search-form&ajax_html_ids%5B%5D=search-block-form&ajax_html_ids%5B%5D=edit-search-block-form--2&ajax_html_ids%5B%5D=edit-actions--2&ajax_html_ids%5B%5D=edit-submit--2&ajax_html_ids%5B%5D=block-eltrecetv-seguinos-sitio&ajax_html_ids%5B%5D=block-tags-temas&ajax_html_ids%5B%5D=temas&ajax_html_ids%5B%5D=ver_mas_temas&ajax_html_ids%5B%5D=block-eltrecetv-temporada-menu-temporada&ajax_html_ids%5B%5D=menu-temporada&ajax_html_ids%5B%5D=main-wrapper&ajax_html_ids%5B%5D=main-content&ajax_html_ids%5B%5D=node-57654&ajax_html_ids%5B%5D=quicktabs-temporada_notas&ajax_html_ids%5B%5D=quicktabs-tab-temporada_notas-0&ajax_html_ids%5B%5D=quicktabs-tab-temporada_notas-1&ajax_html_ids%5B%5D=quicktabs-tab-temporada_notas-2&ajax_html_ids%5B%5D=quicktabs-tab-temporada_notas-3&ajax_html_ids%5B%5D=quicktabs-container-temporada_notas&ajax_html_ids%5B%5D=quicktabs-tabpage-temporada_notas-0&ajax_html_ids%5B%5D=block-views-temporada-notas-ultimos&ajax_html_ids%5B%5D=quicktabs-tabpage-temporada_notas-1&ajax_html_ids%5B%5D=block-views-temporada-notas-mas-comentados&ajax_html_ids%5B%5D=quicktabs-tabpage-temporada_notas-2&ajax_html_ids%5B%5D=block-views-temporada-notas-mas-vistos&ajax_html_ids%5B%5D=quicktabs-tabpage-temporada_notas-3&ajax_html_ids%5B%5D=block-views-temporada-notas-mas-votados&ajax_html_ids%5B%5D=comments&ajax_html_ids%5B%5D=ver_comentarios&ajax_html_ids%5B%5D=comment-969451&ajax_html_ids%5B%5D=comment-969278&ajax_html_ids%5B%5D=comment-969172&ajax_html_ids%5B%5D=comment-969105&ajax_html_ids%5B%5D=comment-969062&ajax_html_ids%5B%5D=content-comment-form&ajax_html_ids%5B%5D=comment-form&ajax_html_ids%5B%5D=edit-name&ajax_html_ids%5B%5D=edit-mail&ajax_html_ids%5B%5D=edit-homepage&ajax_html_ids%5B%5D=edit-comment-shared&ajax_html_ids%5B%5D=edit-comment-shared-und&ajax_html_ids%5B%5D=edit-comment-shared-und-facebook&ajax_html_ids%5B%5D=edit-comment-shared-und-twitter&ajax_html_ids%5B%5D=edit-comment-body&ajax_html_ids%5B%5D=comment-body-add-more-wrapper&ajax_html_ids%5B%5D=edit-comment-body-und-0-value&ajax_html_ids%5B%5D=switch_edit-comment-body-und-0-value&ajax_html_ids%5B%5D=edit-comment-body-und-0-format&ajax_html_ids%5B%5D=edit-actions&ajax_html_ids%5B%5D=edit-submit&ajax_html_ids%5B%5D=content-bottom&ajax_html_ids%5B%5D=eplAdDiv2x728x90&ajax_html_ids%5B%5D=eplParentContainer344568&ajax_html_ids%5B%5D=ifrf01eb687270ed3dd_701ad6722c79688c&ajax_html_ids%5B%5D=content-right&ajax_html_ids%5B%5D=block-temporadas-bloque-programa-temporadas&ajax_html_ids%5B%5D=f307d3ecb&ajax_html_ids%5B%5D=___plusone_0&ajax_html_ids%5B%5D=I0_1375033738636&ajax_html_ids%5B%5D=footer-wrapper2&ajax_html_ids%5B%5D=footer&ajax_html_ids%5B%5D=block-views-destacados-home-block-1&ajax_html_ids%5B%5D=eplAdDivBottom1x300x250&ajax_html_ids%5B%5D=eplad_Bottom1x300x250_718791d37ff92ebc_image&ajax_html_ids%5B%5D=eplAdDivBottom2x300x250&ajax_html_ids%5B%5D=eplbbccad11e9916be99_object&ajax_html_ids%5B%5D=eplbbccad11e9916be99_embed&ajax_html_ids%5B%5D=block-tags-mas-buscados&ajax_html_ids%5B%5D=footer-wrapper1&ajax_html_ids%5B%5D=footer-bottom&ajax_html_ids%5B%5D=block-eltrecetv-pie-sitio&ajax_html_ids%5B%5D=footer-links&ajax_html_ids%5B%5D=epl4iframe&ajax_html_ids%5B%5D=fb-root&ajax_html_ids%5B%5D=fb_xdm_frame_http&ajax_html_ids%5B%5D=fb_xdm_frame_https&ajax_html_ids%5B%5D=fancybox-tmp&ajax_html_ids%5B%5D=fancybox-loading&ajax_html_ids%5B%5D=fancybox-overlay&ajax_html_ids%5B%5D=fancybox-wrap&ajax_html_ids%5B%5D=fancybox-outer&ajax_html_ids%5B%5D=fancybox-bg-n&ajax_html_ids%5B%5D=fancybox-bg-ne&ajax_html_ids%5B%5D=fancybox-bg-e&ajax_html_ids%5B%5D=fancybox-bg-se&ajax_html_ids%5B%5D=fancybox-bg-s&ajax_html_ids%5B%5D=fancybox-bg-sw&ajax_html_ids%5B%5D=fancybox-bg-w&ajax_html_ids%5B%5D=fancybox-bg-nw&ajax_html_ids%5B%5D=fancybox-content&ajax_html_ids%5B%5D=fancybox-close&ajax_html_ids%5B%5D=fancybox-title&ajax_html_ids%5B%5D=fancybox-left&ajax_html_ids%5B%5D=fancybox-left-ico&ajax_html_ids%5B%5D=fancybox-right&ajax_html_ids%5B%5D=fancybox-right-ico&ajax_page_state%5Btheme%5D=eltrecetv2012&ajax_page_state%5Btheme_token%5D=CU7ScY2YBAuQjfXfOBMESutX0eQZA6wTYrMqLsWnf_I&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.base.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.theme.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Flibraries%2Fjquery.fancybox%2Ffancybox%2Fjquery.fancybox-1.3.4.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv%2Fcss%2Feltrecetv.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fcss%2Feltrecetv_comment.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_galleria%2Fcss%2Feltrecetv_galleria.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_grilla%2Fcss%2Fgrilla_reducida.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_jwplayer%2Fcss%2Fjwplayer.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fcss%2Flogin.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fcss%2Fwizard.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fcss%2Ffacebook.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_twitter%2Fcss%2Ftwitter.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fentrevistas%2Fcss%2Fentrevistas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Flink_libres%2Fcss%2Flink_libres.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fnotas%2Fcss%2Fnotas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fprogramas%2Fcss%2Fprogramas.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fcss%2Fsocial_widgets.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_eltrecetv%2Fcss%2Fsocial_widgets_eltrecetv.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_facebook%2Fcss%2Fsocial_widgets_facebook.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_google%2Fcss%2Fsocial_widgets_google.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_pinterest%2Fcss%2Fsocial_widgets_pinterest.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_twitter%2Fcss%2Fsocial_widgets_twitter.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fcomment%2Fcomment.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_api%2Fdate.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_popup%2Fthemes%2Fdatepicker.1.7.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_repeat_field%2Fdate_repeat_field.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffield%2Ftheme%2Ffield.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fnode%2Fnode.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fpoll%2Fpoll.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsearch%2Fsearch.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fuser%2Fuser.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fcss%2Fviews.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Ftags%2Fcss%2Ftags.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fquicktabs%2Fcss%2Fquicktabs.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffilter%2Ffilter.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Ffield_group%2Ffield_group.field_ui.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fckeditor%2Fckeditor.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fctools%2Fcss%2Fctools.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdhtml_menu%2Fdhtml_menu.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fextlink%2Fextlink.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fmorecomments%2Fmorecomments.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fhtml.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Flayout.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fstyle.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fquicktabs.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Feltrecetv2012%2Fcss%2Fprint.css%5D=1&ajax_page_state%5Bjs%5D%5B0%5D=1&ajax_page_state%5Bjs%5D%5B1%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fjquery%2Fjquery.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.once.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fdrupal.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fjquery.fancybox%2Ffancybox%2Fjquery.fancybox-1.3.4.pack.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fswfobject%2Fswfobject.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fjquery.countdown%2Fjquery.countdown1.2.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fjs%2Fga_social_tracking_min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets%2Fjs%2Fsocialwidgets.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_eltrecetv%2Fjs%2Fsocialwidgets.eltrecetv.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_facebook%2Fjs%2Fsocialwidgets.facebook.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_google%2Fjs%2Fsocialwidgets.google.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_pinterest%2Fjs%2Fsocialwidgets.pinterest.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fsocial_widgets_twitter%2Fjs%2Fsocialwidgets.twitter.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fui%2Fexternal%2Fjquery.cookie.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_library%2Freplace%2Fmisc%2Fjquery.form.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fajax.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv%2Fjs%2Feltrecetv.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fjs%2Feltrecetv_comment.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_comment%2Fjs%2Feltrecetv_comment_validate.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_galleria%2Fjs%2Feltrecetv_galleria.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_grilla%2Fjs%2Feltrecetv.grilla.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_jwplayer%2Fjs%2Feltrecetv.jwplayer.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login%2Fjs%2Feltrecetv.login.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fjs%2Ffb_connect.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_facebook%2Fjs%2Feltrecetv.login.facebook.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feltrecetv_login_twitter%2Fjs%2Feltrecetv.login.twitter.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fentrevistas%2Fjs%2Feltrecetv_entrevistas.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Feplanning4%2Fjs%2Feplanning4.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fprogramas%2Fjs%2Feltrecetv_programas.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fviews_ajax_refresh%2Fjs%2Fviews_ajax_refresh.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcustom%2Fviews_load_more%2Fviews_load_more.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Flanguages%2Fes_jYWsqXmILN_z1Ny5EhmoXZbo1PGwKV6IlxIi-05DMyA.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Ffb%2Ffb_stream.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdhtml_menu%2Fdhtml_menu.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fextlink%2Fextlink.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fmorecomments%2Fmorecomments.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fbase.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fprogress.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fajax_view.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fckeditor%2Fincludes%2Fckeditor.utils.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Flibraries%2Fckeditor%2Fckeditor.js%5D=1&ajax_page_state%5Bjs%5D%5Bhttp%3A%2F%2Fwww.eltrecetv.com.ar%2Fsites%2Fall%2Fmodules%2Fcontrib%2Fpinned_site%2Fjs%2Fpinned_site.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fquicktabs%2Fjs%2Fquicktabs.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Ftextarea.js%5D=1&ajax_page_state%5Bjs%5D%5Bmodules%2Ffilter%2Ffilter.js%5D=1"
        else:
            post = item.extra
            numero_pagina = scrapertools.get_match(data,"page\=(\d+)")
            numero_pagina = str(int(numero_pagina)+1)
            post = re.compile("page=\d+",re.DOTALL).sub("page="+numero_pagina,post)

        itemlist.append( Item(channel=CHANNEL, title=">> Página siguiente" , action="episodios", url=pagina_siguiente, extra=post, folder=True) )
    except:
        import traceback
        logger.info(traceback.format_exc())

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Busca videos en alguna de las opciones del menu (excepto en programas)
    mainlist_items = mainlist(Item())
    mainlist_item_programas = mainlist_items.pop()

    alguno = False
    for mainlist_item in mainlist_items:
        exec "itemlist="+mainlist_item.action+"(mainlist_item)"
    
        if len(itemlist)>0:
            alguno = True
            break

    if not alguno:
        print "No hay videos en las secciones del menu"
        return False

    # Comprueba que primer programa devuelve episodios
    programas_items = programas(mainlist_item_programas)
    secciones_items = secciones(programas_items[0])
    episodios_items = episodios(secciones_items[0])

    if len(episodios_items)==0:
        return False

    return True
