# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# tvshack.cc - Pel�culas, series, Anime, Documentales y M�sica en VO
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribuci�n de jurrabi
#----------------------------------------------------------------------
import urllib
import re
import sys
import xbmc
import xbmcplugin
import xbmcgui
import scrapertools
import xbmctools
import os
import library
import string
import config
import logger
#TODO:!@jurrabi Limpiar variables y m�dulos no utilizados

CHANNELNAME = "tvshack"

IMAGEN_MEGAVIDEO = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' , "megavideosite.png") )

SERVIDORES_PERMITIDOS = ['megavideo','veoh','tudou','movshare','stagevu','smotri']
#No soportados comprobados por el momento 56.com,zshare

BUSCADOR_THUMBNAIL = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters','buscador.png' ) )


FANART_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'fanart' ) )

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
logger.info("[tvshack.py] init")


#fanartfile = xbmc.translatePath( os.path.join( FANART_PATH, 'tvshack'+ str (random.randint(1,5))+'.png' ) )
fanartfile = xbmc.translatePath( os.path.join( FANART_PATH, 'tvshack.jpg' ) )
logger.info("[tvshac.py] init pluginhandle: "+str(pluginhandle))
logger.info("[tvshac.py] init fanart: "+fanartfile)
xbmcplugin.setPluginFanart(pluginhandle, fanartfile)

DEBUG = True

##############################################################################
def mainlist(params,url,category):
    """Lista las categor�as principales del canal

    """
    logger.info("[tvshac.py] mainlist")


    # Lista de Categor�as 
    xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Series" , "Series TV (VO)" , "http://tvshack.cc/tv" , thumbnail="" , plot="" )
    xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Cine" , "Pel�culas (VO)" , "http://tvshack.cc/movies" , thumbnail="" , plot="" )
    xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Documentales" , "Documentales (VO)" , "http://tvshack.cc/documentaries" , thumbnail="" , plot="" )
    xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Anime" , "Anime (VO)" , "http://tvshack.cc/anime" , thumbnail="" , plot="" )
    xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Musica" , "M�sica " , "http://tvshack.cc/music" , thumbnail="" , plot="" )
    xbmctools.addnewfolder( CHANNELNAME , "Buscar" , "" , "Busqueda Global en TVShack" , "http://tvshack.cc/search/" , thumbnail=BUSCADOR_THUMBNAIL , plot="" )

    # Opciones adicionales si modo canal �nico
    if config.getSetting ("singlechannel")=="true":
        xbmctools.addSingleChannelOptions (params , url , category)

    logger.info("[tvshac.py] mainlist finalizaplugin handle: "+str(pluginhandle))
    FinalizaPlugin (pluginhandle,category)

def Buscar (params,url,category):
    '''Busca en todo el canal y muestra lista de resultados
    '''
    logger.info("[tvshac.py] Buscar")
    
    keyboard = xbmc.Keyboard()
    keyboard.doModal()
    if not (keyboard.isConfirmed()):
        return
    text = keyboard.getText()
    if len(text) < 3:
        return
  
    #Limpiar entrada
    text = string.capwords(text).replace(" ", "+")
    searchUrl = url+text
  
    # Abrimos la p�gina
    data = ""
    try:
        furl = urllib.urlopen(searchUrl)
        newurl = furl.geturl()
        if newurl != searchUrl:
            dlog ('[tvshack] buscar: solo un resultado: '+ newurl)
            #El resultado de b�squeda redirigi� a la p�gina del �nico resultado.
            if newurl.find('/tv/') == 18: #Una serie
                data = '<li><a href="%s">Television - <strong>%s</strong></a><a href="%s"><span>0 episodes</span></a></li>' % (newurl,newurl[22:-1],newurl)
            elif newurl.find("/movies/") == 18: #Una Pel�cula
                data = '<li><a href="%s">Movies - <strong>%s</strong></a><a href="%s"><span>%s</span></a></li>' % (newurl,newurl[26:-8],newurl,newurl[-6:-2])   
            elif newurl.find("/music/") == 18: #Un cantante
                data = '<li><a href="%s">Music - <strong>%s</strong></a><a href="%s"></a></li>' % (newurl,newurl[25:-1],newurl)   
        else:            
            data = furl.read()
            
        furl.close()
    except:
        pass    
    if len(data) == 0:
        dlog ("[tvshac.py] Buscar - No se encontraron resultados con :"+text)
        error = xbmcgui.Dialog()
        error.ok('pelisalacarta - Canal TVShack','No se produjeron resultados de b�squeda')
        return


# Ej. Serie:  <li><a href="http://tvshack.cc/tv/The_Big_Bang_Theory/">Television - <strong>The Big Bang Theory</strong></a><a href="http://tvshack.cc/tv/The_Big_Bang_Theory/"><span>57 episodes</span></a></li>
# Ej. Cine:   <li><a href="http://tvshack.cc/movies/Bang_Bang_You_re_Dead__2002_/">Movies - <strong>Bang Bang You're Dead</strong></a><a href="http://tvshack.cc/movies/Bang_Bang_You_re_Dead__2002_/"><span>2002</span></a></li>
# Ej. Musica: <li><a href="http://tvshack.cc/music/Mr__Big/">Music - <strong>Mr. Big</strong></a><a href="http://tvshack.cc/music/Mr__Big/"></a></li>
    patronvideos = '''(?x)                                  #      Activa opci�n VERBOSE.
        <li><a\ href="                                      #      Basura
        (?P<url>[^"]+)">                                    # $0 = url del contenido
        ([^\ ]+)\ -\                                        # $1 = Tipo de contenido: Television, Movies o Music
        <strong>                                            #      Basura
        ([^<]+)                                             # $2 = Nombre del contenido
        </strong></a>                                       #      Basura
        (?:<a\ href=")                                      #      Basura
        (?P=url)">                                          # $0 = url del contenido (REPETICI�N)
        (?:<span>)?                                         #      Basura
        ([0-9]+)?                                           # $3 = N� Episodios o A�o Producci�n
        (?:\ episodes)?                                     #      Basura
        (?:</span>)?</a></li>                               #      Basura
        ''' 
    matches = re.findall(patronvideos,data)
            
    totalmatches = len(matches)
    if totalmatches == 0:
        dlog ("[tvshac.py] Buscar - No se encontraron resulta2 con :"+text)
        error = xbmcgui.Dialog()
        error.ok('pelisalacarta - Canal TVShack','No se produjeron resultados de b�squeda')
        return

    for match in matches:
        if match[1]== 'Television':
            # A�ade al listado de XBMC
            if match[3] != '0':
                scrapedtitle = 'Serie - %s (%s episodios)' % (match[2],match[3])
            else:
                scrapedtitle = 'Serie - ' + match[2]
            xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , "Series" , scrapedtitle , match[0] , "" , "" , Serie=match[2] , totalItems=totalmatches)
        elif match[1] == 'Movies':
            scrapedtitle = 'Cine - %s (%s)' % (match[2],match[3])
            xbmctools.addnewfolder( CHANNELNAME , "listaVideosEpisodio" , "Cine" , scrapedtitle , match[0] , "" , "" , totalItems=totalmatches)
        else: #Musica
            xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , "Musica" , "M�sica - "+match[2] , match[0] , "" , "" , totalItems=totalmatches)

    FinalizaPlugin (pluginhandle,category)


# FIN Buscar
###########################################################################
def ListaSeries(params,url,category):
  """Crea el listado de series,Anime o m�sica y lo muestra para selecci�n
  """
  logger.info("[tvshack.py] ListaSeries")

  # Iniciamos un cruadro de di�logo de espera.
  pDialog = xbmcgui.DialogProgress()
  text1 = 'Leyendo %s...' %(category,)
  ret = pDialog.create('pelisalacarta' , text1)
  pDialog.update(0, text1)

  # Descargamos la p�gina
  data = scrapertools.cachePage(url)

  # Extraemos las series por medio de expresiones regulares (patr�n)
  # Ej. Serie:  <li><a href="/tv/30_Rock/">30 Rock <font class="new-updated">Updated!</font><span style="margin-top:0px;">69 episodes</span></a></li> 
  # Ej. Anime:  <li><a href="http://tvshack.cc/anime/Avatar__The_Abridged_Series/">Avatar: The Abridged Series<span style="margin-top:0px;">5 episodes</span></a></li>
  # Ej. M�sica: <li><a href="http://tvshack.cc/music/Michael_Jackson/">Michael Jackson<span style="margin-top:0px;">27 songs</span></a></li>
  patronvideos = '''(?x)                                #      Activa opci�n VERBOSE.
    <li><a\ href="                                      #      Basura
    (?:http://tvshack\.cc)?([^"]+)">                   # $0 = Path (relativo) de la serie Ej. "/tv/The_Wire/"
    ([^<]+)                                             # $1 = Nombre de la serie Ej. Wire, The
    (?:\ <font\ class="new-new">(New)!</font>)?         # $2 = 'New' si la serie es nueva.
    (?:\ <font\ class="new-updated">(Updated)!</font>)? # $3 = 'Updated' si la serie ha sido actualizada
    <span\ style="margin-top:0px;">                     #      Basura
    ([0-9]+)                                            # $4 = N�mero de episodios Ej. 59
    \ ((?:episodes)|(?:songs))                          # $5 = Indicador de episodios o canciones
                 ''' 
  matches = re.compile(patronvideos).findall(data) # Paso del DOTALL-no hace falta para nada.

  totalseries = len(matches)
  if totalseries == 0:
    pDialog.close()
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se encontr� nada que listar')
    FinalizaPlugin_con_error(pluginhandle,category)
    return
  i = 0
  step = 100 / totalseries
  for match in matches:
    #Serie
    scrapedserie = match[1]  

    #Actualizados el di�logo de espera. Esto muestra el avance y por cual serie vamos
    i = i + step
    pDialog.update(i, text1+scrapedserie)

    #URL de la serie
    scrapedurl = "http://tvshack.cc" + match[0]

    # En el t�tulo (que se mostrar� en la siguiente pantalla) elaboramos 
    # un poquito m�s a�adiendo informaci�n sobre:
    #   * El n�mero de episodios almacenados.
    #   * Si la serie ha sido a�adida recientemente.
    #   * Si se han a�adido episodios recientemente.
    if match[5]=='episodes':
      tipo_singular = 'episodio'
      tipo_plural = 'episodios'
    else: #'songs'
      tipo_singular = 'canci�n'
      tipo_plural = 'canciones'
    if match[4]=='1': #Como soy puntilloso no me gusta cuando pone "1 episodios"
      scrapedtitle =  "%s (1 %s)" % (match[1],tipo_singular) # Ej. House (1 episodio)
    else:
      scrapedtitle = "%s (%s %s)" % (match[1], match[4], tipo_plural) # Ej. House (69 episodios)

    if match[2]: #Serie Nueva
      scrapedtitle = scrapedtitle + " (Nuevo)"
    if match[3]: #Nuevos episodios
      scrapedtitle = scrapedtitle + " (Nuevos contenidos)"
      
    # �sta web no tiene informaci�n de cada serie en la lista de selecci�n.
    #   Esa informaci�n est� en la p�gina del listado de episodios.
    #   Obtenerla en este momento seguramente ser�a muy costoso (en tiempo),
    #   sobretodo habiendo m�s de 1300 series. Quiz� sea interesante para busquedas
    #   m�s limitadas... De todas formas lo programo para evaluar
#    scrapedthumbnail, scrapednote = LeeDatosSerie (scrapedurl)
    scrapedthumbnail = ""
    scrapednote = ""
    
    # A�ade al listado de XBMC
    xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapednote , Serie=scrapedserie , totalItems=totalseries)

  pDialog.update(100, text1)
  FinalizaPlugin (pluginhandle,category)
  pDialog.close()

# FIN ListaSeries
###########################################################################
def ListaEpisodios(params,url,category):
  """Muestra los episodios de una serie
  """
  logger.info("[tvshack.py] ListaEpisodios")
  
  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  # A�ade "Agregar todos a la librer�a"
  if category != 'Musica':
    xbmctools.addnewvideo( CHANNELNAME , "addlist2Library" , category , "", "A�ADIR TODOS LOS EPISODIOS A LA BIBLIOTECA" , url , "" , "" , serie)

  listaEp = devuelveListaEpisodios (params,url,category)

  for ep in listaEp:
    xbmctools.addnewvideo( CHANNELNAME , "listaVideosEpisodio" , category , "" , ep['title'] , ep['url'] , ep['thumbnail'] , ep['plot'] , Serie=serie)

  FinalizaPlugin (pluginhandle,category)

def addlist2Library(params,url,category,verbose=True):
  """A�ade todos los episodios de una serie a la biblioteca
  """
  logger.info("[tvshack.py] addlist2Library")

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""
  
  if verbose:
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('pelisalacarta', 'A�adiendo episodios...')

  listaEp = devuelveListaEpisodios (params,url,category)
  episodios = 0
  errores = 0
  nuevos = 0
  for i,ep in enumerate(listaEp):
    if verbose:
      pDialog.update(i*100/len(listaEp), 'A�adiendo episodio...',ep['title'])
      if (pDialog.iscanceled()):
        return
    try:
      nuevos = nuevos + library.savelibrary(ep['title'],ep['url'],ep['thumbnail'],"",ep['plot'],canal=CHANNELNAME,category="Series",Serie=serie,verbose=False,accion="strm_detail",pedirnombre=False)
      episodios = episodios + 1
    except IOError:
      logger.info("Error al grabar el archivo "+ep['title'])
      errores = errores + 1

  if verbose:
    pDialog.close()
  if errores > 0:
    logger.info ("[tvshack.py - addlist2Library] No se pudo a�adir "+str(errores)+" episodios") 

  if verbose:
    library.update(episodios,errores,nuevos)

  return nuevos
  
def devuelveListaEpisodios (params,url,category):
  """Scrapea la p�gina de episodios y la devuelve como lista de diccionarios
  
  --> Los habituales en los canales de pelisalacarta.
  <-- [{Episodio}]  Lista de diccionarios con los datos de cada episodio
      Al a�adir los episodios como diccionarios nos permite a�adir o borrar claves a voluntad
      dejando abierto el dise�o a poder a�adir informaci�n en los canales que
      �sta exista.
      Las clave b�sicas en el momento de escribir este canal son:
      'title' : T�tulo del episodio - Para la biblioteca peferiblemente en formato
                 NOMBRE_SERIE - TEMPORADAxEPISODIO T�TULO_EPISODIO LOQUESEA
      'url'   : URL del episodio
      'plot'  : Resumen del episodio (o de la serie si �ste no existe para este canal)
      'thumbnail' : Fotograma del episodio o car�tula de la serie 
  """

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  # Descarga la p�gina
  data = scrapertools.cachePage(url)

  # Primero debemos separar los datos por temporada
  patrontemporadas = '''(?x)                            #      Activa opci�n VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patr�n al ignorar los espacios.
                                                        #      Tambi�n permite comentarios como �ste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <h2\ class="h-list-title">Season\                   #      Basura
    ([0-9]+)                                            # $0 = Temporada
    <\/h2>                                              #      Basura
    ''' 
  splitdata = re.split(patrontemporadas,data)
  
  #Ahora tenemos la p�gina separada entre
  #  1. Secciones sin v�deos (La primera)
  #  2. Secciones de texto de temporada. De aqu� sacamos el n�mero de temporada
  #  3. Secci�n de videos de temporada.
  temporada = '0'
  # Extraemos los episodios por medio de expresiones regulares (patr�n)
  # Ej. Serie:  <li><a href="/tv/Family_Guy/season_1/episode_1/">ep1. Death Has a Shadow</a><a href=""><span>31/1/1999</span></a></li>
  # Ej. Anime:  <li><a href="http://tvshack.cc/anime/07_Ghost/season_1/episode_5/">ep5. Episode 5</a><a href=""><span>??/??/????</span></a></li> 
  # Ej. Musica: <li><a href="http://tvshack.cc/music/Michael_Jackson/C85E8225E45E/">Black Or White<span>2,301 views</span></a></li><li><a 
  patronepisodios = '''(?x)                             #      Activa opci�n VERBOSE. Esto permite
    <li><a\ href="                                      #      Basura
    (?:http://tvshack\.cc)?([^"]+)">                   #\g1 = Path (relativo) del episodio/video
    (?:ep([0-9]+)\.\ )?                                 #\g2 = N�mero de episodio
    ([^<]+)                                             #\g3 = Nombre del episodio
    (?:<\/a><a\ href="">)?<span>                        #      Basura
    ([0-9\?]+\/[0-9\?]+\/[0-9\?]+)?                     #\g4 = Fecha de emisi�n (s�lo series)
    (?:([0-9,]+)\ views)?                               #\g5 = Veces visto (s�lo m�sica)
    <\/span><\/a><\/li>                                 #      Basura
  ''' 
  episodiosREO = re.compile(patronepisodios) ## Objeto de Expresi�n Regular (REO)

  listaEp = [] # Lista de Episodios
  Ep = {}      # Diccionario con la info de cada episodio

  # Como en �ste canal no hay informaci�n por episodio, cogemos el argumento
  # y la car�tula de la serie como datos para cada episodio 
  Ep['thumbnail'],Ep['plot'] = LeeDatosSerie (data)

  for parte in splitdata:
    if re.match("[0-9]+", parte): #texto de temporada
      temporada = parte
    else: # Busquemos episodios
      # Recorremos un iterador por los matches de episodiosREO 
      # (m�s elegante y breve en este caso aunque hay que conocer los 
      # Objetos de Expresi�n Regular (REO) y los matchobjects)
      for match in episodiosREO.finditer (parte):
        if category != 'Musica':
          Ep['title'] = match.expand (serie + ' - ' + temporada + 'x\g<2> - \g<3> (\g<4>)') #con expand los grupos referenciaos empiezan en 1
        else:
          Ep['title'] = match.expand ('\g<3> (visto \g<5> veces)') #con expand los grupos referenciaos empiezan en 1
        #URL del episodio
        Ep['url'] = "http://tvshack.cc" + match.group(1)
        listaEp.append(Ep.copy()) #Se a�ade el episodio a la lista (hay que copiarlo)

  return listaEp
            
# FIN devuelveListaEpisodios
###########################################################################
def ListaDetallada(params,url,category):
  """Crea el listado de Espect�culos de las secciones de Cine y Docs.
  """
  logger.info("[tvshack.py] ListaDetallada")

  # Iniciamos un cruadro de di�logo de espera.
  pDialog = xbmcgui.DialogProgress()
  texto1 = 'Leyendo %s...' % (category,)
  ret = pDialog.create('pelisalacarta' , texto1)
  pDialog.update(0, texto1)

  # Descargamos la p�gina
  data = scrapertools.cachePage(url)

  # Extraemos los videos por medio de expresiones regulares (patr�n)
  # Ej. Cine: <li><a href="/movies/_Rec__2__2009_/">[Rec] 2<span style="margin-top:0px;">2009</span></a></li> 
  # Ej. Docu: <li><a href="/movies/Ancient_Aliens__2009_/">Ancient Aliens<span style="margin-top:0px;">2009</span></a></li>
  patronvideos = '''(?x)                                #      Activa opci�n VERBOSE.
    <li><a\ href="                                      #      Basura
    ([^"]+)">                                           # $0 = Path (relativo) del v�deo Ej. "/movies/Rec__2__2009_/"
    ([^<]+)                                             # $1 = Nombre del video Ej. [Rec] 2
    (?:\ <font\ class="new-new">(New)!</font>)?         # $2 = 'New' si el video es nuevo.
    (?:\ <font\ class="new-updated">(Updated)!</font>)? # $3 = 'Updated' Creo que no se usa. pero no hace da�o
    <span\ style="margin-top:0px;">                     #      Basura
    ([0-9]+)</span>                                     # $4 = A�o de la producci�n Ej. 2009
                 ''' 
  matches = re.compile(patronvideos).findall(data) # Paso del DOTALL-no hace falta para nada.

  totalmatches = len(matches)
  if totalmatches == 0:
    pDialog.close()
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se encontr� nada que listar')
    FinalizaPlugin_con_error(pluginhandle,category)
    return

  i = 0
  step = 100 / totalmatches
  for match in matches:
    #Serie
    scrapedserie = match[1]  

    #Actualizados el di�logo de espera. Esto muestra el avance y por cual serie vamos
    i = i + step
    pDialog.update(i, texto1+scrapedserie)

    #URL del video
    scrapedurl = "http://tvshack.cc" + match[0]

    # En el t�tulo (que se mostrar� en la siguiente pantalla) elaboramos 
    # un poquito m�s a�adiendo informaci�n sobre:
    #   * El a�o de producci�n.
    #   * Si el video ha sido a�adido recientemente.
    scrapedtitle = '%s (%s)' % (match[1],match[4])
    if match[2]: #Contenido Nuevo
      scrapedtitle = scrapedtitle + " (Nuevo)"
      
    # �sta web no tiene informaci�n de cada video en la lista de selecci�n.
    #   Esa informaci�n est� en la p�gina del video.
    #   Obtenerla en este momento seguramente ser�a muy costoso (en tiempo),
    #   Quiz� sea interesante para busquedas
    #   m�s limitadas... De todas formas lo programo para evaluar
#    scrapedthumbnail, scrapednote = LeeDatosSerie (scrapedurl)
    scrapedthumbnail = ""
    scrapednote = ""
    
    # A�ade al listado de XBMC
    xbmctools.addnewfolder( CHANNELNAME , "listaVideosEpisodio" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapednote , totalItems=totalmatches)

  pDialog.update(100, texto1)
  FinalizaPlugin (pluginhandle,category)
  pDialog.close()

# FIN ListaDetalle
###########################################################################
def strm_detail (params,url,category):
  '''Reproduce el episodio seleccionado desde un fichero strm
  '''
  listaVideosEpisodio (params,url,category,strmfile=True)

def listaVideosEpisodio (params,url,category,strmfile=False):
  '''Extrae y muestra los v�deos disponibles para un episodio
  
  Inicialmente nos conformaremos s�lo con los de megavideo/megaupload
  Luego ir� a�adiendo el resto de los que me encuentre
  
  Tambien quiero considerar la opci�n de mostrar la lista de opciones o
  elegir una al azar o por alg�n mecanismo mejor. As� se ahorrar�a un paso
  aunque supongo que habr� riesgo de no elegir una buena opci�n.
  '''
  logger.info("[tvshack.py] ListaVideosEpisodios")


  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  title = urllib.unquote_plus( params.get("title") )
  thumbnail = urllib.unquote_plus( params.get("thumbnail") )

  # Descarga la p�gina
  data = scrapertools.cachePage(url)
  #Recortamos los datos al cuadro de enlaces alternativos
  match = re.search('<h3>Alternate links</h3>(.+?)</ul>',data,re.DOTALL)
  if not match:
    dlog ('[tvshack.py] listaVideosEpisodio - No hay secci�n de Alternate links')
    dlog (data)
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('No hay videos' , 'No hay videos v�lidos para este episodio.')
    return
  data = match.expand('\g<1>')
  
#Ej. Video por defecto:<li><a href="http://tvshack.cc/tv/Lost/season_4/episode_6/"><img src="http://road.../megavideo.gif" />megavideo.com</a> <small>(selected)</small></li>
#Ej. Alternat:<li><a href="http://tvshack.cc/tv/Lost/season_4/episode_6/a:723568/"><img src="http://road.../megavideo.gif" />megavideo.com</a></li>
  patronvideos = '''(?x)                                #      Activa opci�n VERBOSE.
    <li><a\ href="                                      #      Basura
    ([^"]+)">                                           # $0 = URL del episodio
    <img\ src="                                         #      Basura
    ([^"]+)"\ \/>                                       # $1 = URL de miniatura 
    ([^<]+)<\/a>                                        # $2 = Server
    (?:\ <small>\((selected)\)<\/small>)?               # $3 = Opcional: Video seleccionado
    <\/li>                                              #      Basura
  '''
  matches = re.findall(patronvideos, data)
  if len (matches) == 0:
    dlog ('[tvshack.py] listaVideosEpisodio - No hay enlaces en el cuadro alternate links.')
    dlog (data)
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('pelisalacarta - tvshack' , 'No hay videos v�lidos para este episodio.')
    return

  opciones = []
  servers = []
  for i,match in enumerate(matches):
    scrapedurl = match[0]
    scrapedthumbnail = match[1]
    if scrapedthumbnail.find('megavideo') > -1:
      scrapedthumbnail = IMAGEN_MEGAVIDEO
    scrapedserver = match[2].split ('.')[0].lower() #Convierte 'Megavideo.com' -> 'megavideo'
    servers.append (scrapedserver) 
    scrapedtitle = str(i) + '. [' + scrapedserver + ']'
    if match[3]=='selected':
      scrapedtitle = scrapedtitle + ' (Por defecto)'
    if scrapedserver not in SERVIDORES_PERMITIDOS:
      scrapedtitle = scrapedtitle + ' (NO SOPORTADO)'
      
    opciones.append(scrapedtitle)
  if config.getSetting("default_action")=="0" or config.getSetting("default_action")=="3":
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Elige un v�deo", opciones)
  else:
    #Si existe, preferimos megavideo.
    try:
      seleccion = servers.index('megavideo')
    except: #Si no hay megavideo buscamos cualquiera que sirva
      seleccion = 0
      while seleccion < len (opciones) and servers[seleccion] not in SERVIDORES_PERMITIDOS:
        seleccion = seleccion +1 
    if seleccion == len(opciones):
      dlog ('[tvshack.py] listaVideosEpisodio - No hay videos en los servidores soportados para este episodio.')
      advertencia = xbmcgui.Dialog()
      resultado = advertencia.ok('pelisalacarta - tvshack' , 'No hay videos v�lidos para este episodio.')
      return
  dlog( str(seleccion))
  if seleccion == -1:
    return
  else:
    params['title'] = title + ' [' + servers[seleccion] + ']'
    params['server'] = servers[seleccion]
    playVideo (params,matches[seleccion][0],category,strmfile)

# FIN listaVideosEpisodio
###########################################################################
def playVideo(params,url,category,strmfile=False):
  '''Reproduce el video seleccionado
  '''
  logger.info("[tvshack.py] playVideo")

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  if (params.has_key("category")):
    category = params.get("category")

  title = urllib.unquote_plus( params.get("title") )
  if params.has_key("thumbnail"):
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
  else:
    thumbnail = ''
    
  if params.has_key("plot"):
    plot = params.get("plot")
  else:
    plot = xbmc.getInfoLabel( "ListItem.Plot" )

  server = params["server"]

  if DEBUG:
    logger.info("[tvshack.py] url="+url)
    logger.info("[tvshack.py] title="+title)
    logger.info("[tvshack.py] plot="+plot)
    logger.info("[tvshack.py] thumbnail="+thumbnail)
    logger.info("[tvshack.py] server="+server)

  # Descarga la p�gina
  data = scrapertools.cachePage(url)

  #Averiguamos las partes del video (Puede tener m�s de una)
  partes = re.findall('<a href="javascript:changevid\(([0-9]+)\);"',data)

  # Y el path relativo de los v�deos  
#JUR CAMBIO EN WEB 01/04/2010
#  patronpath = '''(?x)                  #      Activa opci�n VERBOSE.
#    http://tvshack\.cc/report_video/   #      Basura
#    ([^/]+/[^/]+)                       # $0 = Path relativo Ej. 'tv/716063'
#    /","report"                         #      Basura
#  '''
  patronpath = '''(?x)                  #      Activa opci�n VERBOSE.
    http://tvshack\.cc/video_load/     #      Basura
    ([^/]+/[^/]+)                       # $0 = Path relativo Ej. 'tv/716063'
    /'\+part                            #      Basura
  '''
  paths=re.findall(patronpath,data)

  #JUR-PROV: De momento voy a considerar los v�deos de 1 s�la parte.
  # Para los v�deos con m�s partes habr� que crear una funci�n especial que
  # pregunte una sola vez y meta todos los v�deos juntos.
  if len(partes) > 1:
    logger.info ("[tvshack] playVideo - Video multiparte - pendiente:" + str(len(partes)))
    dialog = xbmcgui.Dialog()
    dialog.ok('pelisalacarta - tvshack','Este video tiene varias partes.','En esta versi�n de pelisalacarta no est�n soportados.','Eliga otro video con una s�la parte.')
#    for parte in partes:
  elif len(partes) == 1:
    url = 'http://tvshack.cc/video_load/'+paths[0] + '/' + partes[0]
    #Esta URL sigue sin ser un enlace megaupload u otro servidor v�lido por lo que seguimos scrapeando
    # para evitar excesivas selecciones por parte del usuario.

    # Descarga la p�gina
    data2 = scrapertools.cachePage(url)
    if server == 'megavideo':
      dlog ("[tvshack.py]playVideo: Server= megavideo")

      # 
      #Ej.<embed src="http://www.megavideo.com/v/5ZZHOM74...
      patronpath = '''(?x)                           #      Activa opci�n VERBOSE.
        <embed\ src="http://www\.megavideo\.com/v/   #      Basura
        (.{8})                                       # $0 = url megavideo Ej. '5ZZHOM74'
      '''
      mediaurl=re.findall(patronpath,data2)
      if len (mediaurl) == 0:
        dlog ("[tvshack.py]playVideo: No se encontr� la url de megavideo en:")
        dlog (data2)
        dialog = xbmcgui.Dialog()
        dialog.ok('pelisalacarta - tvshack','No se encontr� el video en megavideo.','Eliga otro video.')
        return
      elif len (mediaurl) > 1:
        dlog ("[tvshack.py]playVideo: Hay m�s de un enlace de megavideo (y no deber�a)")
        for url in mediaurl:
          dlog (url)
      mediaurl = mediaurl[0]
#      xbmctools.playvideo(CHANNELNAME,server,mediaurl,category,title,thumbnail,plot,Serie=Serie)
      dlog ("[tvshack.py]playVideo: Llamando al play. mediaurl= "+mediaurl)
      xbmctools.playvideo(CHANNELNAME,'Megavideo',mediaurl,category,title,'','',Serie=serie,strmfile=strmfile)
    else: # Video de otro servidor (no megavideo)
      #Probamos si es flash...
      flashmatch = re.search('flashvars="file=(.+?)&type=flv',data2)
      if flashmatch != None:
        dlog ('[tvshack.py]playVideo: Video flash - url = ' + flashmatch.group(1))
        xbmctools.playvideo(CHANNELNAME,'Directo',flashmatch.group(1),category,title,'','',Serie=serie,strmfile=strmfile)
        return
      #Si no, buscamos otras fuentes de video
      othersmatch = re.search('src="([^"]+)"',data2)
      if othersmatch != None and server in SERVIDORES_PERMITIDOS:
        url = othersmatch.group(1).replace('&amp;','&')
        xbmctools.playvideo(CHANNELNAME,server,url,category,title,'','',Serie=serie,strmfile=strmfile)
        return

      dlog ("[tvshack.py]playVideo: Servidor no soportado: "+server)
      dialog = xbmcgui.Dialog()
      dialog.ok('pelisalacarta - tvshack - '+server,'El video seleccionado es de '+server,'Ese servidor a�n no est� soportado en TVShack.')
      return

def FinalizaPlugin (pluginhandle,category):
  """Tareas comunes al final del plugin. Sin ordenaci�n
  """
  # Indicar metadatos del plugin para skis (Categor�a y contenido)
  xbmcplugin.setPluginCategory (pluginhandle , category)
  xbmcplugin.setContent (pluginhandle , category) #Estamos usando category como content.

  # Deshabilitar ordenaci�n
  xbmcplugin.addSortMethod (handle=pluginhandle , sortMethod=xbmcplugin.SORT_METHOD_NONE)

  # Finalizar Directorio del Plugin
  xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
  
def FinalizaPlugin_con_error (pluginhandle,category):
  """Tareas comunes al final del plugin. Sin ordenaci�n
  """
  # Indicar metadatos del plugin para skis (Categor�a y contenido)
  #xbmcplugin.setPluginCategory (pluginhandle , category)
  #xbmcplugin.setContent (pluginhandle , category) #Estamos usando category como content.

  # Deshabilitar ordenaci�n
  #xbmcplugin.addSortMethod (handle=pluginhandle , sortMethod=xbmcplugin.SORT_METHOD_NONE)

  # Finalizar Directorio del Plugin
  xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=False )
  
def LeeDatosSerie (tdata):
  """Obtiene una miniatura y la sinopsis de una serie
  
  tdata                 --> Datos de la p�gina de episodios de la serie
  miniatura,sinopsis  <-- Tupla con los datos requeridos
  """

  # PATRON PARA EXTRAER LOS POSTER DE LAS SERIES
  patronposter = '''(?x)                                #      Activa opci�n VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patr�n al ignorar los espacios.
                                                        #      Tambi�n permite comentarios como �ste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <img\ src="                                         #      Basura  
    ([^"]+)                                             # $0 = Poster Ej. http://roadrunner.tvshack.cc/tv-posters/16.jpg
    "\ alt="Poster"\ \/>                                #      Basura
  '''
  posterREO = re.compile(patronposter) # Objeto de Expresi�n Regular (REO)
  # Buscamos el Poster
  match = posterREO.search(tdata)
  if match:
    miniatura = match.group(1)
  else:
    miniatura = ""



  # PATRON PARA EXTRAER LA SINOPSIS DE LAS SERIES
  patronsinopsis = '''(?x)                              #      Activa opci�n VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patr�n al ignorar los espacios.
                                                        #      Tambi�n permite comentarios como �ste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <p>                                                 #      Basura  
    ([^<]+)                                             # $0 = Sinopsis
    <\/p>                                               #      Basura
  '''
  sinopsisREO = re.compile(patronsinopsis) # Objeto de Expresi�n Regular (REO)

  # Buscamos la sinopsis
  match = sinopsisREO.search(tdata)
  if match:
    sinopsis = match.group(1)
  else:
    sinopsis = ""

  return miniatura,sinopsis
  
# Estas son las expresiones XPATH para obtener el poster y la sinopsis.
# Averiguar si se pueden usar de alguna forma en python
#id('show-information-column2')/x:p
#id('show-information-column1')/x:div/x:img  

def dlog (text):
  if DEBUG:
    logger.info(text)

