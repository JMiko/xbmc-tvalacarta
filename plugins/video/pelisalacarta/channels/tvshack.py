# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# tvshack.net - Películas, series, Anime, Documentales y Música en VO
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribución de jurrabi
#----------------------------------------------------------------------
import urllib,urllib2
import re
import sys
import xbmc
import xbmcplugin
import xbmcgui
import scrapertools
import servertools
import xbmctools
import os
import library
import random
import string

CHANNELNAME = "tvshack"

IMAGEN_MEGAVIDEO = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' , "megavideosite.png") )

SERVIDORES_PERMITIDOS = ['megavideo','veoh','tudou','movshare','stagevu','smotri']
#No soportados comprobados por el momento 56.com,zshare

BUSCADOR_THUMBNAIL = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters','buscador.png' ) )


FANART_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'fanart' ) )

# Esto permite su ejecución en modo emulado
try:
  pluginhandle = int( sys.argv[ 1 ] )
except:
  pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[tvshack.py] init")


#fanartfile = xbmc.translatePath( os.path.join( FANART_PATH, 'tvshack'+ str (random.randint(1,5))+'.png' ) )
fanartfile = xbmc.translatePath( os.path.join( FANART_PATH, 'tvshack.jpg' ) )
xbmc.output("[tvshac.py] init pluginhandle: "+str(pluginhandle))
xbmc.output("[tvshac.py] init fanart: "+fanartfile)
xbmcplugin.setPluginFanart(pluginhandle, fanartfile)

DEBUG = True

##############################################################################
def mainlist(params,url,category):
  """Lista las categorías principales del canal

  """
  xbmc.output("[tvshac.py] mainlist")


  # Lista de Categorías 
  xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Series" , "Series TV (VO)" , "http://tvshack.net/tv" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Cine" , "Películas (VO)" , "http://tvshack.net/movies" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Documentales" , "Documentales (VO)" , "http://tvshack.net/documentaries" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Anime" , "Anime (VO)" , "http://tvshack.net/anime" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Musica" , "Música " , "http://tvshack.net/music" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "Buscar" , "" , "Busqueda Global en TVShack" , "http://tvshack.net/search/" , thumbnail=BUSCADOR_THUMBNAIL , plot="" )

  # Opciones adicionales si modo canal único
  if xbmcplugin.getSetting ("singlechannel")=="true":
    xbmctools.addSingleChannelOptions (params , url , category)

  xbmc.output("[tvshac.py] mainlist finalizaplugin handle: "+str(pluginhandle))
  FinalizaPlugin (pluginhandle,category)

def Buscar (params,url,category):
  '''Busca en todo el canal y muestra lista de resultados
  '''
  xbmc.output("[tvshac.py] Buscar")

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
  
  # Descargamos la página
  data = scrapertools.cachePage(searchUrl)
  if len(data) == 0:
    dlog ("[tvshac.py] Buscar - No se encontraron resultados con :"+text)
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se produjeron resultados de búsqueda')
    return


# Ej. Serie:  <li><a href="http://tvshack.net/tv/The_Big_Bang_Theory/">Television - <strong>The Big Bang Theory</strong></a><a href="http://tvshack.net/tv/The_Big_Bang_Theory/"><span>57 episodes</span></a></li>
# Ej. Cine:   <li><a href="http://tvshack.net/movies/Bang_Bang_You_re_Dead__2002_/">Movies - <strong>Bang Bang You're Dead</strong></a><a href="http://tvshack.net/movies/Bang_Bang_You_re_Dead__2002_/"><span>2002</span></a></li>
# Ej. Musica: <li><a href="http://tvshack.net/music/Mr__Big/">Music - <strong>Mr. Big</strong></a><a href="http://tvshack.net/music/Mr__Big/"></a></li>
  patronvideos = '''(?x)                                #      Activa opción VERBOSE.
    <li><a\ href="                                      #      Basura
    (?P<url>[^"]+)">                                    # $0 = url del contenido
    ([^\ ]+)\ -\                                        # $1 = Tipo de contenido: Television, Movies o Music
    <strong>                                            #      Basura
    ([^<]+)                                             # $2 = Nombre del contenido
    </strong></a>                                       #      Basura
    (?:<a\ href=")                                      #      Basura
    (?P=url)">                                          # $0 = url del contenido (REPETICIÓN)
    (?:<span>)?                                         #      Basura
    ([0-9]+)?                                           # $3 = Nº Episodios o Año Producción
    (?:\ episodes)?                                     #      Basura
    (?:</span>)?</a></li>                               #      Basura
    ''' 
  matches = re.findall(patronvideos,data)
  totalmatches = len(matches)
  if totalmatches == 0:
    dlog ("[tvshac.py] Buscar - No se encontraron resulta2 con :"+text)
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se produjeron resultados de búsqueda')
    return

  for match in matches:
    if match[1]== 'Television':
      # Añade al listado de XBMC
      scrapedtitle = 'Serie - %s (%s episodios)' % (match[2],match[3])
      xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , "Series" , scrapedtitle , match[0] , "" , "" , Serie=match[2] , totalItems=totalmatches)
    elif match[1] == 'Movies':
      scrapedtitle = 'Cine - %s (%s)' % (match[2],match[3])
      xbmctools.addnewfolder( CHANNELNAME , "listaVideosEpisodio" , "Cine" , scrapedtitle , match[0] , "" , "" , totalItems=totalmatches)
    else: #Musica
      xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , "Musica" , "Música - "+match[2] , match[0] , "" , "" , totalItems=totalmatches)

  FinalizaPlugin (pluginhandle,category)


# FIN Buscar
###########################################################################
def ListaSeries(params,url,category):
  """Crea el listado de series,Anime o música y lo muestra para selección
  """
  xbmc.output("[tvshack.py] ListaSeries")

  # Iniciamos un cruadro de diálogo de espera.
  pDialog = xbmcgui.DialogProgress()
  text1 = 'Leyendo %s...' %(category,)
  ret = pDialog.create('pelisalacarta' , text1)
  pDialog.update(0, text1)

  # Descargamos la página
  data = scrapertools.cachePage(url)

  # Extraemos las series por medio de expresiones regulares (patrón)
  # Ej. Serie:  <li><a href="/tv/30_Rock/">30 Rock <font class="new-updated">Updated!</font><span style="margin-top:0px;">69 episodes</span></a></li> 
  # Ej. Anime:  <li><a href="http://tvshack.net/anime/Avatar__The_Abridged_Series/">Avatar: The Abridged Series<span style="margin-top:0px;">5 episodes</span></a></li>
  # Ej. Música: <li><a href="http://tvshack.net/music/Michael_Jackson/">Michael Jackson<span style="margin-top:0px;">27 songs</span></a></li>
  patronvideos = '''(?x)                                #      Activa opción VERBOSE.
    <li><a\ href="                                      #      Basura
    (?:http://tvshack\.net)?([^"]+)">                   # $0 = Path (relativo) de la serie Ej. "/tv/The_Wire/"
    ([^<]+)                                             # $1 = Nombre de la serie Ej. Wire, The
    (?:\ <font\ class="new-new">(New)!</font>)?         # $2 = 'New' si la serie es nueva.
    (?:\ <font\ class="new-updated">(Updated)!</font>)? # $3 = 'Updated' si la serie ha sido actualizada
    <span\ style="margin-top:0px;">                     #      Basura
    ([0-9]+)                                            # $4 = Número de episodios Ej. 59
    \ ((?:episodes)|(?:songs))                          # $5 = Indicador de episodios o canciones
                 ''' 
  matches = re.compile(patronvideos).findall(data) # Paso del DOTALL-no hace falta para nada.

  totalseries = len(matches)
  if totalseries == 0:
    pDialog.close()
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se encontró nada que listar')
    FinalizaPlugin_con_error(pluginhandle,category)
    return
  i = 0
  step = 100 / totalseries
  for match in matches:
    #Serie
    scrapedserie = match[1]  

    #Actualizados el diálogo de espera. Esto muestra el avance y por cual serie vamos
    i = i + step
    pDialog.update(i, text1+scrapedserie)

    #URL de la serie
    scrapedurl = "http://tvshack.net" + match[0]

    # En el título (que se mostrará en la siguiente pantalla) elaboramos 
    # un poquito más añadiendo información sobre:
    #   * El número de episodios almacenados.
    #   * Si la serie ha sido añadida recientemente.
    #   * Si se han añadido episodios recientemente.
    if match[5]=='episodes':
      tipo_singular = 'episodio'
      tipo_plural = 'episodios'
    else: #'songs'
      tipo_singular = 'canción'
      tipo_plural = 'canciones'
    if match[4]=='1': #Como soy puntilloso no me gusta cuando pone "1 episodios"
      scrapedtitle =  "%s (1 %s)" % (match[1],tipo_singular) # Ej. House (1 episodio)
    else:
      scrapedtitle = "%s (%s %s)" % (match[1], match[4], tipo_plural) # Ej. House (69 episodios)

    if match[2]: #Serie Nueva
      scrapedtitle = scrapedtitle + " (Nuevo)"
    if match[3]: #Nuevos episodios
      scrapedtitle = scrapedtitle + " (Nuevos contenidos)"
      
    # Ésta web no tiene información de cada serie en la lista de selección.
    #   Esa información está en la página del listado de episodios.
    #   Obtenerla en este momento seguramente sería muy costoso (en tiempo),
    #   sobretodo habiendo más de 1300 series. Quizá sea interesante para busquedas
    #   más limitadas... De todas formas lo programo para evaluar
#    scrapedthumbnail, scrapednote = LeeDatosSerie (scrapedurl)
    scrapedthumbnail = ""
    scrapednote = ""
    
    # Añade al listado de XBMC
    xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapednote , Serie=scrapedserie , totalItems=totalseries)

  pDialog.update(100, text1)
  FinalizaPlugin (pluginhandle,category)
  pDialog.close()

# FIN ListaSeries
###########################################################################
def ListaEpisodios(params,url,category):
  """Muestra los episodios de una serie
  """
  xbmc.output("[tvshack.py] ListaEpisodios")
  
  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  # Añade "Agregar todos a la librería"
  if category != 'Musica':
    xbmctools.addnewvideo( CHANNELNAME , "addlist2Library" , category , "", "AÑADIR TODOS LOS EPISODIOS A LA BIBLIOTECA" , url , "" , "" , serie)

  listaEp = devuelveListaEpisodios (params,url,category)

  for ep in listaEp:
    xbmctools.addnewvideo( CHANNELNAME , "listaVideosEpisodio" , category , "" , ep['title'] , ep['url'] , ep['thumbnail'] , ep['plot'] , Serie=serie)

  FinalizaPlugin (pluginhandle,category)

def addlist2Library(params,url,category,verbose=True):
  """Añade todos los episodios de una serie a la biblioteca
  """
  xbmc.output("[tvshack.py] addlist2Library")

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""
  
  if verbose:
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('pelisalacarta', 'Añadiendo episodios...')

  listaEp = devuelveListaEpisodios (params,url,category)
  episodios = 0
  errores = 0
  nuevos = 0
  for i,ep in enumerate(listaEp):
    if verbose:
      pDialog.update(i*100/len(listaEp), 'Añadiendo episodio...',ep['title'])
      if (pDialog.iscanceled()):
        return
    try:
      nuevos = nuevos + library.savelibrary(ep['title'],ep['url'],ep['thumbnail'],"",ep['plot'],canal=CHANNELNAME,category="Series",Serie=serie,verbose=False,accion="strm_detail",pedirnombre=False)
      episodios = episodios + 1
    except IOError:
      xbmc.output("Error al grabar el archivo "+ep['title'])
      errores = errores + 1

  if verbose:
    pDialog.close()
  if errores > 0:
    xbmc.output ("[tvshack.py - addlist2Library] No se pudo añadir "+str(errores)+" episodios") 

  if verbose:
    library.update(episodios,errores,nuevos)

  return nuevos
  
def devuelveListaEpisodios (params,url,category):
  """Scrapea la página de episodios y la devuelve como lista de diccionarios
  
  --> Los habituales en los canales de pelisalacarta.
  <-- [{Episodio}]  Lista de diccionarios con los datos de cada episodio
      Al añadir los episodios como diccionarios nos permite añadir o borrar claves a voluntad
      dejando abierto el diseño a poder añadir información en los canales que
      ésta exista.
      Las clave básicas en el momento de escribir este canal son:
      'title' : Título del episodio - Para la biblioteca peferiblemente en formato
                 NOMBRE_SERIE - TEMPORADAxEPISODIO TÍTULO_EPISODIO LOQUESEA
      'url'   : URL del episodio
      'plot'  : Resumen del episodio (o de la serie si éste no existe para este canal)
      'thumbnail' : Fotograma del episodio o carátula de la serie 
  """

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  # Descarga la página
  data = scrapertools.cachePage(url)

  # Primero debemos separar los datos por temporada
  patrontemporadas = '''(?x)                            #      Activa opción VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patrón al ignorar los espacios.
                                                        #      También permite comentarios como éste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <h2\ class="h-list-title">Season\                   #      Basura
    ([0-9]+)                                            # $0 = Temporada
    <\/h2>                                              #      Basura
    ''' 
  splitdata = re.split(patrontemporadas,data)
  
  #Ahora tenemos la página separada entre
  #  1. Secciones sin vídeos (La primera)
  #  2. Secciones de texto de temporada. De aquí sacamos el número de temporada
  #  3. Sección de videos de temporada.
  temporada = '0'
  # Extraemos los episodios por medio de expresiones regulares (patrón)
  # Ej. Serie:  <li><a href="/tv/Family_Guy/season_1/episode_1/">ep1. Death Has a Shadow</a><a href=""><span>31/1/1999</span></a></li>
  # Ej. Anime:  <li><a href="http://tvshack.net/anime/07_Ghost/season_1/episode_5/">ep5. Episode 5</a><a href=""><span>??/??/????</span></a></li> 
  # Ej. Musica: <li><a href="http://tvshack.net/music/Michael_Jackson/C85E8225E45E/">Black Or White<span>2,301 views</span></a></li><li><a 
  patronepisodios = '''(?x)                             #      Activa opción VERBOSE. Esto permite
    <li><a\ href="                                      #      Basura
    (?:http://tvshack\.net)?([^"]+)">                   #\g1 = Path (relativo) del episodio/video
    (?:ep([0-9]+)\.\ )?                                 #\g2 = Número de episodio
    ([^<]+)                                             #\g3 = Nombre del episodio
    (?:<\/a><a\ href="">)?<span>                        #      Basura
    ([0-9\?]+\/[0-9\?]+\/[0-9\?]+)?                     #\g4 = Fecha de emisión (sólo series)
    (?:([0-9,]+)\ views)?                               #\g5 = Veces visto (sólo música)
    <\/span><\/a><\/li>                                 #      Basura
  ''' 
  episodiosREO = re.compile(patronepisodios) ## Objeto de Expresión Regular (REO)

  listaEp = [] # Lista de Episodios
  Ep = {}      # Diccionario con la info de cada episodio

  # Como en éste canal no hay información por episodio, cogemos el argumento
  # y la carátula de la serie como datos para cada episodio 
  Ep['thumbnail'],Ep['plot'] = LeeDatosSerie (data)

  for parte in splitdata:
    if re.match("[0-9]+", parte): #texto de temporada
      temporada = parte
    else: # Busquemos episodios
      # Recorremos un iterador por los matches de episodiosREO 
      # (más elegante y breve en este caso aunque hay que conocer los 
      # Objetos de Expresión Regular (REO) y los matchobjects)
      for match in episodiosREO.finditer (parte):
        if category != 'Musica':
          Ep['title'] = match.expand (serie + ' - ' + temporada + 'x\g<2> - \g<3> (\g<4>)') #con expand los grupos referenciaos empiezan en 1
        else:
          Ep['title'] = match.expand ('\g<3> (visto \g<5> veces)') #con expand los grupos referenciaos empiezan en 1
        #URL del episodio
        Ep['url'] = "http://tvshack.net" + match.group(1)
        listaEp.append(Ep.copy()) #Se añade el episodio a la lista (hay que copiarlo)

  return listaEp
            
# FIN devuelveListaEpisodios
###########################################################################
def ListaDetallada(params,url,category):
  """Crea el listado de Espectáculos de las secciones de Cine y Docs.
  """
  xbmc.output("[tvshack.py] ListaDetallada")

  # Iniciamos un cruadro de diálogo de espera.
  pDialog = xbmcgui.DialogProgress()
  texto1 = 'Leyendo %s...' % (category,)
  ret = pDialog.create('pelisalacarta' , texto1)
  pDialog.update(0, texto1)

  # Descargamos la página
  data = scrapertools.cachePage(url)

  # Extraemos los videos por medio de expresiones regulares (patrón)
  # Ej. Cine: <li><a href="/movies/_Rec__2__2009_/">[Rec] 2<span style="margin-top:0px;">2009</span></a></li> 
  # Ej. Docu: <li><a href="/movies/Ancient_Aliens__2009_/">Ancient Aliens<span style="margin-top:0px;">2009</span></a></li>
  patronvideos = '''(?x)                                #      Activa opción VERBOSE.
    <li><a\ href="                                      #      Basura
    ([^"]+)">                                           # $0 = Path (relativo) del vídeo Ej. "/movies/Rec__2__2009_/"
    ([^<]+)                                             # $1 = Nombre del video Ej. [Rec] 2
    (?:\ <font\ class="new-new">(New)!</font>)?         # $2 = 'New' si el video es nuevo.
    (?:\ <font\ class="new-updated">(Updated)!</font>)? # $3 = 'Updated' Creo que no se usa. pero no hace daño
    <span\ style="margin-top:0px;">                     #      Basura
    ([0-9]+)</span>                                     # $4 = Año de la producción Ej. 2009
                 ''' 
  matches = re.compile(patronvideos).findall(data) # Paso del DOTALL-no hace falta para nada.

  totalmatches = len(matches)
  if totalmatches == 0:
    pDialog.close()
    error = xbmcgui.Dialog()
    error.ok('pelisalacarta - Canal TVShack','No se encontró nada que listar')
    FinalizaPlugin_con_error(pluginhandle,category)
    return

  i = 0
  step = 100 / totalmatches
  for match in matches:
    #Serie
    scrapedserie = match[1]  

    #Actualizados el diálogo de espera. Esto muestra el avance y por cual serie vamos
    i = i + step
    pDialog.update(i, texto1+scrapedserie)

    #URL del video
    scrapedurl = "http://tvshack.net" + match[0]

    # En el título (que se mostrará en la siguiente pantalla) elaboramos 
    # un poquito más añadiendo información sobre:
    #   * El año de producción.
    #   * Si el video ha sido añadido recientemente.
    scrapedtitle = '%s (%s)' % (match[1],match[4])
    if match[2]: #Contenido Nuevo
      scrapedtitle = scrapedtitle + " (Nuevo)"
      
    # Ésta web no tiene información de cada video en la lista de selección.
    #   Esa información está en la página del video.
    #   Obtenerla en este momento seguramente sería muy costoso (en tiempo),
    #   Quizá sea interesante para busquedas
    #   más limitadas... De todas formas lo programo para evaluar
#    scrapedthumbnail, scrapednote = LeeDatosSerie (scrapedurl)
    scrapedthumbnail = ""
    scrapednote = ""
    
    # Añade al listado de XBMC
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
  '''Extrae y muestra los vídeos disponibles para un episodio
  
  Inicialmente nos conformaremos sólo con los de megavideo/megaupload
  Luego iré añadiendo el resto de los que me encuentre
  
  Tambien quiero considerar la opción de mostrar la lista de opciones o
  elegir una al azar o por algún mecanismo mejor. Así se ahorraría un paso
  aunque supongo que habrá riesgo de no elegir una buena opción.
  '''
  xbmc.output("[tvshack.py] ListaVideosEpisodios")


  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  title = urllib.unquote_plus( params.get("title") )
  thumbnail = urllib.unquote_plus( params.get("thumbnail") )

  # Descarga la página
  data = scrapertools.cachePage(url)
  #Recortamos los datos al cuadro de enlaces alternativos
  match = re.search('<h3>Alternate links</h3>(.+?)</ul>',data,re.DOTALL)
  if not match:
    dlog ('[tvshack.py] listaVideosEpisodio - No hay sección de Alternate links')
    dlog (data)
    advertencia = xbmcgui.Dialog()
    resultado = advertencia.ok('No hay videos' , 'No hay videos válidos para este episodio.')
    return
  data = match.expand('\g<1>')
  
#Ej. Video por defecto:<li><a href="http://tvshack.net/tv/Lost/season_4/episode_6/"><img src="http://road.../megavideo.gif" />megavideo.com</a> <small>(selected)</small></li>
#Ej. Alternat:<li><a href="http://tvshack.net/tv/Lost/season_4/episode_6/a:723568/"><img src="http://road.../megavideo.gif" />megavideo.com</a></li>
  patronvideos = '''(?x)                                #      Activa opción VERBOSE.
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
    resultado = advertencia.ok('pelisalacarta - tvshack' , 'No hay videos válidos para este episodio.')
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
  if xbmcplugin.getSetting("default_action")=="0":
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Elige un vídeo", opciones)
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
      resultado = advertencia.ok('pelisalacarta - tvshack' , 'No hay videos válidos para este episodio.')
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
  xbmc.output("[tvshack.py] playVideo")

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
    xbmc.output("[tvshack.py] url="+url)
    xbmc.output("[tvshack.py] title="+title)
    xbmc.output("[tvshack.py] plot="+plot)
    xbmc.output("[tvshack.py] thumbnail="+thumbnail)
    xbmc.output("[tvshack.py] server="+server)

  # Descarga la página
  data = scrapertools.cachePage(url)

  #Averiguamos las partes del video (Puede tener más de una)
  partes = re.findall('<a href="javascript:changevid\(([0-9]+)\);"',data)

  # Y el path relativo de los vídeos  
  patronpath = '''(?x)                  #      Activa opción VERBOSE.
    http://tvshack\.net/report_video/   #      Basura
    ([^/]+/[^/]+)                       # $0 = Path relativo Ej. 'tv/716063'
    /","report"                         #      Basura
  '''
  paths=re.findall(patronpath,data)

  #JUR-PROV: De momento voy a considerar los vídeos de 1 sóla parte.
  # Para los vídeos con más partes habrá que crear una función especial que
  # pregunte una sola vez y meta todos los vídeos juntos.
  if len(partes) > 1:
    xbmc.output ("[tvshack] playVideo - Video multiparte - pendiente:" + str(len(partes)))
    dialog = xbmcgui.Dialog()
    dialog.ok('pelisalacarta - tvshack','Este video tiene varias partes.','En esta versión de pelisalacarta no están soportados.','Eliga otro video con una sóla parte.')
#    for parte in partes:
  elif len(partes) == 1:
    url = 'http://tvshack.net/video_load/'+paths[0] + '/' + partes[0]
    #Esta URL sigue sin ser un enlace megaupload u otro servidor válido por lo que seguimos scrapeando
    # para evitar excesivas selecciones por parte del usuario.

    # Descarga la página
    data2 = scrapertools.cachePage(url)
    if server == 'megavideo':
      dlog ("[tvshack.py]playVideo: Server= megavideo")

      # 
      #Ej.<embed src="http://www.megavideo.com/v/5ZZHOM74...
      patronpath = '''(?x)                           #      Activa opción VERBOSE.
        <embed\ src="http://www\.megavideo\.com/v/   #      Basura
        (.{8})                                       # $0 = url megavideo Ej. '5ZZHOM74'
      '''
      mediaurl=re.findall(patronpath,data2)
      if len (mediaurl) == 0:
        dlog ("[tvshack.py]playVideo: No se encontró la url de megavideo en:")
        dlog (data2)
        dialog = xbmcgui.Dialog()
        dialog.ok('pelisalacarta - tvshack','No se encontró el video en megavideo.','Eliga otro video.')
        return
      elif len (mediaurl) > 1:
        dlog ("[tvshack.py]playVideo: Hay más de un enlace de megavideo (y no debería)")
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
      dialog.ok('pelisalacarta - tvshack - '+server,'El video seleccionado es de '+server,'Ese servidor aún no está soportado en TVShack.')
      return

def FinalizaPlugin (pluginhandle,category):
  """Tareas comunes al final del plugin. Sin ordenación
  """
  # Indicar metadatos del plugin para skis (Categoría y contenido)
  xbmcplugin.setPluginCategory (pluginhandle , category)
  xbmcplugin.setContent (pluginhandle , category) #Estamos usando category como content.

  # Deshabilitar ordenación
  xbmcplugin.addSortMethod (handle=pluginhandle , sortMethod=xbmcplugin.SORT_METHOD_NONE)

  # Finalizar Directorio del Plugin
  xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
  
def FinalizaPlugin_con_error (pluginhandle,category):
  """Tareas comunes al final del plugin. Sin ordenación
  """
  # Indicar metadatos del plugin para skis (Categoría y contenido)
  #xbmcplugin.setPluginCategory (pluginhandle , category)
  #xbmcplugin.setContent (pluginhandle , category) #Estamos usando category como content.

  # Deshabilitar ordenación
  #xbmcplugin.addSortMethod (handle=pluginhandle , sortMethod=xbmcplugin.SORT_METHOD_NONE)

  # Finalizar Directorio del Plugin
  xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=False )
  
def LeeDatosSerie (tdata):
  """Obtiene una miniatura y la sinopsis de una serie
  
  tdata                 --> Datos de la página de episodios de la serie
  miniatura,sinopsis  <-- Tupla con los datos requeridos
  """

  # PATRON PARA EXTRAER LOS POSTER DE LAS SERIES
  patronposter = '''(?x)                                #      Activa opción VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patrón al ignorar los espacios.
                                                        #      También permite comentarios como éste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <img\ src="                                         #      Basura  
    ([^"]+)                                             # $0 = Poster Ej. http://roadrunner.tvshack.net/tv-posters/16.jpg
    "\ alt="Poster"\ \/>                                #      Basura
  '''
  posterREO = re.compile(patronposter) # Objeto de Expresión Regular (REO)
  # Buscamos el Poster
  match = posterREO.search(tdata)
  if match:
    miniatura = match.group(1)
  else:
    miniatura = ""



  # PATRON PARA EXTRAER LA SINOPSIS DE LAS SERIES
  patronsinopsis = '''(?x)                              #      Activa opción VERBOSE. Esto permite
                                                        #      un poco de libertad para ordenar
                                                        #      el patrón al ignorar los espacios.
                                                        #      También permite comentarios como éste.
                                                        # ---  COMIENZO DEL PATRON REAL  ---
    <p>                                                 #      Basura  
    ([^<]+)                                             # $0 = Sinopsis
    <\/p>                                               #      Basura
  '''
  sinopsisREO = re.compile(patronsinopsis) # Objeto de Expresión Regular (REO)

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
    xbmc.output(text)

