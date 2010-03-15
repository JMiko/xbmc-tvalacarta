# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# tvshack.net - Pel�culas, series, Anime, Documentales y M�sica en VO
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# contribuci�n de jurrabi
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

CHANNELNAME = "tvshack"

IMAGEN_MEGAVIDEO = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' , 'posters' , "megavideosite.png") )

SERVIDORES_PERMITIDOS = ['megavideo']


# Esto permite su ejecuci�n en modo emulado
try:
  pluginhandle = int( sys.argv[ 1 ] )
except:
  pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[tvshack.py] init")

DEBUG = True

##############################################################################
def mainlist(params,url,category):
  """Lista las categor�as principales del canal

  """
  xbmc.output("[tvshac.py] mainlist")

  # Lista de Categor�as 
  xbmctools.addnewfolder( CHANNELNAME , "ListaSeries" , "Series" , "Series TV (VO)" , "http://tvshack.net/tv" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Cine" , "Pel�culas (VO)" , "http://tvshack.net/movies" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Documentales" , "Documentales (VO)" , "http://tvshack.net/movies" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Anime" , "Anime (VO?)" , "http://tvshack.net/documentaries" , thumbnail="" , plot="" )
  xbmctools.addnewfolder( CHANNELNAME , "ListaDetallada" , "Musica" , "M�sica " , "http://tvshack.net/music" , thumbnail="" , plot="" )

  # Opciones adicionales si modo canal �nico
  if xbmcplugin.getSetting ("singlechannel")=="true":
    xbmctools.addSingleChannelOptions (params , url , category)

  FinalizaPlugin (pluginhandle,category)

def ListaSeries(params,url,category):
  """Crea el listado de series y lo muestra para selecci�n
  """
  xbmc.output("[tvshack.py] ListaSeries")

  # Iniciamos un cruadro de di�logo de espera.
  pDialog = xbmcgui.DialogProgress()
  ret = pDialog.create('pelisalacarta' , 'Leyendo series...')
  pDialog.update(0, 'Leyendo series...')

  # Descargamos la p�gina
  data = scrapertools.cachePage(url)

  # Extraemos las series por medio de expresiones regulares (patr�n)
  patronvideos = '''(?x)                                #      Activa opci�n VERBOSE.
    <li><a\ href="                                      #      Basura
    ([^"]+)">                                           # $0 = Path (relativo) de la serie Ej. "/tv/The_Wire/"
    ([^<]+)                                             # $1 = Nombre de la serie Ej. Wire, The
    (?:\ <font\ class="new-new">(New)!</font>)?         # $2 = 'New' si la serie es nueva.
    (?:\ <font\ class="new-updated">(Updated)!</font>)? # $3 = 'Updated' si la serie ha sido actualizada
    <span\ style="margin-top:0px;">                     #      Basura
    ([0-9]+)\ episodes                                  # $4 = N�mero de episodios Ej. 59
                 ''' 
  matches = re.compile(patronvideos).findall(data) # Paso del DOTALL-no hace falta para nada.

  totalseries = len(matches)
  i = 0
  step = 100 / totalseries
  for match in matches:
    #Serie
    scrapedserie = match[1]  

    #Actualizados el di�logo de espera. Esto muestra el avance y por cual serie vamos
    i = i + step
    pDialog.update(i, 'Leyendo series...'+scrapedserie)

    #URL de la serie
    scrapedurl = "http://tvshack.net" + match[0]

    # En el t�tulo (que se mostrar� en la siguiente pantalla) elaboramos 
    # un poquito m�s a�adiendo informaci�n sobre:
    #   * El n�mero de episodios almacenados.
    #   * Si la serie ha sido a�adida recientemente.
    #   * Si se han a�adido episodios recientemente.
    if match[4]=='1': #Como soy puntilloso no me gusta cuando pone "1 episodios"
      scrapedtitle = match[1] + " (1 episodio)"
    else:
      scrapedtitle = match[1] + " (" + match[4] + " episodios)"
    if match[2]: #Serie Nueva
      scrapedtitle = scrapedtitle + " (Serie Nueva)"
    if match[3]: #Nuevos episodios
      scrapedtitle = scrapedtitle + " (Nuevos episodios)"
      
    # �sta web no tiene informaci�n de cada serie en la lista de selecci�n.
    #   Esa informaci�n est� en la p�gina del listado de episodios.
    #   Obtenerla en este momento seguramente ser�a muy costoso (en tiempo),
    #   sobretodo habiendo m�s de 1300 series. Quiz� sea interesante para busquedas
    #   m�s limitadas... De todas formas lo programo para evaluar
#    scrapedthumbnail, scrapednote = LeeDatosSerie (scrapedurl)
    scrapedthumbnail = ""
    scrapednote = ""
    
    # A�ade al listado de XBMC
    xbmctools.addnewfolder( CHANNELNAME , "ListaEpisodios" , "Series" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapednote , Serie=scrapedserie , totalItems=totalseries)

  pDialog.update(totalseries, 'Leyendo series...')
  FinalizaPlugin (pluginhandle,category)
  pDialog.close()

# FIN ListaSeries
###########################################################################
def ListaEpisodios(params,url,category):
  """Muestra los episodios de una serie
  """
  xbmc.output("[tvshack.py] ListaEpisodios")
  
  procesaListaEpisodios (params,url,category,"creaLista")

def addlist2Library(params,url,category):
  """Muestra los episodios de una serie
  """
  xbmc.output("[tvshack.py] addlist2Library")
  
  procesaListaEpisodios (params,url,category,"a�adeBiblioteca")

def strm_detail (params,url,category):
  listaVideosEpisodio (params,url,category,strmfile=True)

def procesaListaEpisodios (params,url,category,proceso):
  """Scrapea la p�gina de episodios y realiza el proceso indicado
  
  proceso = "creaLista" - Crea la lista de episodios con xbmcplugin.addDirectoryItem
  proceso = "a�adeBiblioteca" - A�ade todos los episodios a la biblioteca
  """
  if proceso == "a�adeBiblioteca":
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('pelisalacarta', 'A�adiendo episodios...')

  if params.has_key("Serie"):
    serie = params.get("Serie")
  else:
    serie = ""

  # Descarga la p�gina
  data = scrapertools.cachePage(url)

  scrapedthumbnail,scrapednote = LeeDatosSerie (data)

  # A�ade "Agregar todos a la librer�a" si el proceso es creaLista
  if proceso == "creaLista":
    xbmctools.addnewvideo( CHANNELNAME , "addlist2Library" , category , "", "A�ADIR TODOS LOS EPISODIOS A LA BIBLIOTECA" , url , "" , scrapednote , serie)


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
  # Ej. <li><a href="/tv/Family_Guy/season_1/episode_1/">ep1. Death Has a Shadow</a><a href=""><span>31/1/1999</span></a></li>
  patronepisodios = '''(?x)                             #      Activa opci�n VERBOSE. Esto permite
    <li><a\ href="                                      #      Basura
    ([^"]+)">                                           #\g1 = Path (relativo) del episodio
    ep([0-9]+)\.\                                       #\g2 = N�mero de episodio
    ([^<]+)                                             #\g3 = Nombre del episodio
    <\/a><a\ href=""><span>                             #      Basura
    ([0-9\?]+\/[0-9\?]+\/[0-9\?]+)                      #\g4 = Fecha de emisi�n
    <\/span><\/a><\/li>                                 #      Basura
  ''' 
  episodiosREO = re.compile(patronepisodios) ## Objeto de Expresi�n Regular (REO)

  episodios = 0
  errores = 0
  for parte in splitdata:
    if re.match("[0-9]+", parte): #texto de temporada
      temporada = parte
    else: # Busquemos episodios
      # Recorremos un iterador por los matches de episodiosREO 
      # (m�s elegante y breve en este caso aunque hay que conocer los 
      # Objetos de Expresi�n Regular (REO) y los matchobjects)
      for match in episodiosREO.finditer (parte): 
        scrapedtitle = match.expand (serie + ' - ' + temporada + 'x\g<2> - \g<3> (\g<4>)') #con expand los grupos referenciaos empiezan en 1
        if proceso == "a�adeBiblioteca":
          pDialog.update(100, 'A�adiendo episodio...',scrapedtitle)
          if (pDialog.iscanceled()):
            return
        #URL del episodio
        scrapedurl = "http://tvshack.net" + match.group(1)

        if proceso == "creaLista": # A�ade al listado de XBMC si el proceso es creaLista
          xbmctools.addnewfolder( CHANNELNAME , "listaVideosEpisodio" , "Series" , scrapedtitle , scrapedurl , scrapedthumbnail , scrapednote , Serie=serie)
        elif proceso == "a�adeBiblioteca":
          try:
            library.savelibrary(scrapedtitle,scrapedurl,scrapedthumbnail,"",scrapednote,canal=CHANNELNAME,category="Series",Serie=serie,verbose=False,accion="strm_detail",pedirnombre=False)
            episodios = episodios + 1
          except IOError:
            xbmc.output("Error al grabar el archivo "+scrapedtitle)
            errores = errores + 1
          
  if proceso == "creaLista":
    FinalizaPlugin (pluginhandle,category)
  elif proceso == "a�adeBliblioteca":
    pDialog.close()
    if errores > 0:
      xbmc.output ("[tvshack.py - addlist2Library] No se pudo a�adir "+str(errores)+" episodios") 
    library.update(episodios,errores)
  
# FIN ListaEpisodios
###########################################################################
def listaVideosEpisodio (params,url,category,strmfile=False):
  '''Extrae y muestra los v�deos disponibles para un episodio
  
  Inicialmente nos conformaremos s�lo con los de megavideo/megaupload
  Luego ir� a�adiendo el resto de los que me encuentre
  
  Tambien quiero considerar la opci�n de mostrar la lista de opciones o
  elegir una al azar o por alg�n mecanismo mejor. As� se ahorrar�a un paso
  aunque supongo que habr� riesgo de no elegir una buena opci�n.
  '''
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
  
#Ej. Video por defecto:<li><a href="http://tvshack.net/tv/Lost/season_4/episode_6/"><img src="http://road.../megavideo.gif" />megavideo.com</a> <small>(selected)</small></li>
#Ej. Alternat:<li><a href="http://tvshack.net/tv/Lost/season_4/episode_6/a:723568/"><img src="http://road.../megavideo.gif" />megavideo.com</a></li>
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
#    scrapedtitle = title + ' [' + scrapedserver + ']'
    scrapedtitle = str(i) + '. [' + scrapedserver + ']'
    if match[3]=='selected':
      scrapedtitle = scrapedtitle + ' (Por defecto)'
    if scrapedserver not in SERVIDORES_PERMITIDOS:
      scrapedtitle = scrapedtitle + ' (NO SOPORTADO)'
    	
    opciones.append(scrapedtitle)
  if xbmcplugin.getSetting("default_action")=="0":
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Elige un v�deo", opciones)
  else:
    seleccion = 0
    while seleccion < len (opciones) and servers[seleccion] not in SERVIDORES_PERMITIDOS:
      seleccion = seleccion +1 
    if seleccion == len(opciones):
      dlog ('[tvshack.py] listaVideosEpisodio - No hay videos en los servidores permitidos para este episodio.')
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

#    xbmctools.addnewvideo( CHANNELNAME , "playVideo" , category , server , 
#      scrapedtitle , scrapedurl , scrapedthumbnail , '' , Serie=serie)

#  FinalizaPlugin (pluginhandle,category)



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
  thumbnail = urllib.unquote_plus( params.get("thumbnail") )

  if params.has_key("plot"):
    plot = params.get("plot")
  else:
    plot = xbmc.getInfoLabel( "ListItem.Plot" )

  server = params["server"]

  if DEBUG:
    xbmc.output("[tvshack.py] title="+title)
    xbmc.output("[tvshack.py] plot="+plot)
    xbmc.output("[tvshack.py] thumbnail="+thumbnail)
    xbmc.output("[tvshack.py] server="+server)

  # Descarga la p�gina
  data = scrapertools.cachePage(url)

  #Averiguamos las partes del video (Puede tener m�s de una)
  partes = re.findall('<a href="javascript:changevid\(([0-9]+)\);"',data)

  # Y el path relativo de los v�deos  
  patronpath = '''(?x)                  #      Activa opci�n VERBOSE.
    http://tvshack\.net/report_video/   #      Basura
    ([^/]+/[^/]+)                       # $0 = Path relativo Ej. 'tv/716063'
    /","report"                         #      Basura
  '''
  paths=re.findall(patronpath,data)

  #JUR-PROV: De momento voy a considerar los v�deos de 1 s�la parte.
  # Para los v�deos con m�s partes habr� que crear una funci�n especial que
  # pregunte una sola vez y meta todos los v�deos juntos.
  if len(partes) > 1:
    xbmc.output ("[tvshack] playVideo - Video multiparte - pendiente:" + str(len(partes)))
    dialog = xbmcgui.Dialog()
    dialog.ok('pelisalacarta - tvshack','Este video tiene varias partes.','En esta versi�n de pelisalacarta no est�n soportados.','Eliga otro video con una s�la parte.')
#    for parte in partes:
  elif len(partes) == 1:
    url = 'http://tvshack.net/video_load/'+paths[0] + '/' + partes[0]
    #Esta URL sigue sin ser un enlace megaupload por lo que seguimos scrapeando
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
    else: # Video de un servidor desconocido.
      dlog ("[tvshack.py]playVideo: Servidor desconocido: "+server)
      dialog = xbmcgui.Dialog()
      dialog.ok('pelisalacarta - tvshack - '+server,'El video seleccionado es de '+server,'Ese servidor a�n no est� soportado en TVShack.')
      return
          
#    # Ej. flashvars="file=http://tweetypie.tvshack.net/td/?id=ZjQ4NzljNmMzYjJlMWQyOGJiNmMwYTIyN2Y0NWE4ZmIuVTNKSFlUSTJNREJ3VmtRPQ==&type=flv
#    urlflv = re.findall ('flashvars="file=(.+?)&type=flv',data2) #URL al fichero flv (baja calidad)
#    if len(urlflv) == 1:
#      xbmctools.playvideo(CHANNELNAME,'flv',urlflv[0],category,title,thumbnail,plot,Serie = serie)

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
    ([^"]+)                                             # $0 = Poster Ej. http://roadrunner.tvshack.net/tv-posters/16.jpg
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
		xbmc.output(text)

