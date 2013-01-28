#!/usr/bin/env bash

###############################################
#              www.TVenLinux.com              #
#           Actualizado: 20/01/2013           #
#   Autor: Busindre (busilezas[@]gmail.com)   #
#  Programación TV: www.programacion-tdt.com  #
###############################################

# http://xmltvepg.wanwizard.eu/rytecxmltvdplus.gz --> Programacion más completa en xml (http://www.rytec.be/)

############################### Configuración. (Mirar en la web www.tvenlinux.com alguna otra posibilidad no documentada aquí.).

# Segundos que estará descargando el streaming de TV antes de empezar a reproducirlo, aumentar los segundos para conexiones lentas.
CACHE_STREAMING=12 

# Número de Kbytes que usará Mplayer para poder retroceder en la visualización del streaming de TV.
CACHE_MPLAYER=10000 

# Cambiando el valor a 1 no preguntará si queremos guardar lo visualizado. Útil si no te interesa guardar y se quiere evitar la pregunta.
SAVE=0 

# Usar una pila fifo en vez de guardar un fichero temporal. Valor por defecto 1 (No usa fifo.)
# Poner a 0 para usar una pila en vez de guardar un temporal
# Poner a 2 para usar la pila apoyándose en "cat" (Probar si con la opción 0 no se consigue mejora)
# NOTA: Con determinados canales el uso de la pila puede colgar TVenLinux, usar cntrl+c en consola. 
fifo=1 

# Cambiar el valor a 1 para no mostrar la ventana de "Teclas útiles de Mplayer".
MPLAYER_HELP=0 

# Cambiar el reproductor ( vlc, cvlc y ffplay ). Si prefieres que mplayer termine en vez de esperar más datos introduce: "mplayer_old".
REPRODUCTOR="mplayer"

ID=`date '+%s'` 
V_script="20/01/2013";

#touch /tmp/versiontv # Descomentar esta linea (Quitar la primera almohadilla) si se quiere que TVenLinux NO busque actualizaciones de forma automática.

############################### Función para obtener la Versión y mostrar un aviso.
function version {

randomversion=$[($ID % 3)]
ls /tmp/versiontv > /dev/null 2>&1
ver=$?
if [ $ver -eq 2 -a $randomversion -eq 1 ]; then # Si no existe el fichero, y el random no da 0 comprobamos, el random se utiliza para no mostrar siempre el aviso.
	echo -e " \e[00;36mBuscando si hay nuevas versiones de TVenLinux.sh\e[00m\n"
	V_actual=`curl  -r 2480-2497 -A "Mozilla 5.0" -s http://www.tvenlinux.com/ | grep -i -e "<h5>(" -e ")</h5>" | sed  -e "s/<h5>(//" -e "s/)<\/h5>//" -e "s/^[ \t]*//"`
	touch "/tmp/versiontv" ; # Para que solo muestre el aviso una vez por cada ejecución.
	
	if [ "$V_actual" != "$V_script" -a "$V_actual" != "" ]; then # Si se ha podido verificar la versión y hay actualización disponible.
	
		if [ $KDE -eq 1 ]; then
			zenity --title "Nueva versión disponible" --no-wrap --info --text="Hay una nueva versión actualizada a fecha de $V_actual.\n\nPuede descargarla de www.tvenlinux.com" ;
		else
			kdialog --msgbox  "Hay una nueva versión actualizada a fecha de $V_actual.\n\nPuede descargarla de www.tvenlinux.com" ;
		fi
	fi
	
fi

}

############################### Función para mostrar la ayuda de Mplayer (Teclas útiles).

function mplayer_keys {

ls /tmp/tvhelp > /dev/null 2>&1
tvhelp=$?

if [ $MPLAYER_HELP -eq 0 -a $KDE -eq 1 -a $tvhelp -eq 2 -a "$REPRODUCTOR" = "mplayer" ]; then

	touch /tmp/tvhelp;
	zenity --no-wrap --title "Teclas útiles" --info --text="0: Sube el volumen\n9: Baja el volumen\n( ) Balance de sonido  izda / dcha\nm: Silencio (Mute)\n\nIzquierda: Retrocede 10 segundos.\nDerecha: Avanza 10 segundos.\n\nArriba: Avanza 1 minuto.\nAbajo: Retrocede 1 minuto.\n\nAv. Pág: Retrocede 10 minutos.\nRe Pág: Avanza 10 minutos.\n\np, Espacio: Pausa / Reproducir.\n\nF: Pantalla completa.\n\nMays + t: Siempre encima.\n\nq, Esc: Cierra mplayer." ;

elif [ $MPLAYER_HELP -eq 0 -a $KDE -eq 0 -a $tvhelp -eq 2 -a "$REPRODUCTOR" = "mplayer" ]; then
	
	touch /tmp/tvhelp;
	kdialog --msgbox  "0: Sube el volumen\n9: Baja el volumen\n( ) Balance de sonido  izda / dcha\nm: Silencio (Mute)\n\nIzquierda: Retrocede 10 segundos.\nDerecha: Avanza 10 segundos.\n\nArriba: Avanza 1 minuto.\nAbajo: Retrocede 1 minuto.\n\nAv. Pág: Retrocede 10 minutos.\nRe Pág: Avanza 10 minutos.\n\np, Espacio: Pausa / Reproducir.\n\nF: Pantalla completa.\n\nMays + t: Siempre encima.\n\nq, Esc: Cierra mplayer." ;


fi
}

############################### Función para forzar configuración antigua para streamings descargados con mplayer, ya que no aceptan las opciones de reproducción por defecto.

function mplayer_conf_change {

if [ "$REPRODUCTOR" = "mplayer" ]; then 
	REPRODUCTOR="mplayer_old"
fi

}

############################### Función para cambiar el reproductor y comprueba si el mismo está o no instalado, de no estarlo, corta el streaming y sale.

function reproductor {

if  [ "$REPRODUCTOR" = "vlc" ]; then
	
	whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b vlc | grep -i "/vlc" > /dev/null 2>&1
	repro_instalado=$?
	if [ $repro_instalado -eq 1 ]; then
		echo -e " \e[00;31mERROR: No se ha encontrado el programa $REPRODUCTOR instalado en su sistema.\e[00m\n"
		kill -1 $LASTPID > /dev/null 2>&1
		exit
	else
	
		echo -e " \e[00;36mEjecutando Vlc\e[00m\n"
		vlc /tmp/$CANAL."$ID" > /dev/null 2>&1 ;
	fi

elif  [ "$REPRODUCTOR" = "cvlc" ]; then

	whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b cvlc | grep -i "/cvlc" > /dev/null 2>&1
	repro_instalado=$?
	if [ $repro_instalado -eq 1 ]; then
		echo -e " \e[00;31mERROR: No se ha encontrado el programa $REPRODUCTOR instalado en su sistema.\e[00m\n"
		kill -1 $LASTPID > /dev/null 2>&1
		exit
	else
	
		echo -e " \e[00;36mEjecutando Cvlc\e[00m\n"
		cvlc /tmp/$CANAL."$ID" > /dev/null 2>&1 ;

	fi

elif [ "$REPRODUCTOR" = "ffplay" ]; then

	whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b ffplay | grep -i "/ffplay" > /dev/null 2>&1
	repro_instalado=$?
	if [ $repro_instalado -eq 1 ]; then
		echo -e " \e[00;31mERROR: No se ha encontrado el programa $REPRODUCTOR instalado en su sistema.\e[00m\n"
		kill -1 $LASTPID > /dev/null 2>&1
		exit
	else

		echo -e " \e[00;36mEjecutando ffplay\e[00m\n"
		ffplay /tmp/$CANAL."$ID" > /dev/null 2>&1 ;

	fi

elif [ "$REPRODUCTOR" = "mplayer_old" ]; then

	echo -e " \e[00;36mEjecutando Mplayer (Configuración alternativa)\e[00m\n"
	mplayer -vo vdpau,va,xv,gl2 -lavdopts threads=1 -really-quiet -mc 10 -autosync 30 -cache $CACHE_MPLAYER /tmp/$CANAL."$ID" > /dev/null 2>&1 ;

elif [ "$REPRODUCTOR" = "mplayer_fifo" -a $fifo -eq 0 ]; then

	echo -e " \e[00;36mEjecutando Mplayer (Configuración fifo)\e[00m\n"
 	mplayer -really-quiet /tmp/$CANAL."$ID" > /dev/null 2>&1 ;

elif [ "$REPRODUCTOR" = "mplayer_fifo" -a $fifo -eq 2 ]; then

	echo -e " \e[00;36mEjecutando Mplayer (Configuración fifo 2)\e[00m\n"
	cat /tmp/$CANAL."$ID" | mplayer -really-quiet - > /dev/null 2>&1 ;

elif [ "$REPRODUCTOR" = "mplayer" ]; then

	echo -e " \e[00;36mEjecutando Mplayer\e[00m\n"
	echo 'pause' > /tmp/backtv
	echo 'seek -100' >> /tmp/backtv
	mplayer -input file=/tmp/backtv -loop 0 -fixed-vo -ss 10000 -vo vdpau,va,xv,gl2 -lavdopts threads=1 -really-quiet -mc 10 -autosync 30 /tmp/$CANAL."$ID" > /dev/null 2>&1 ;

else
	echo -e " \e[00;31mERROR: Seleccione un reproductor válido.\e[00m\n"
	kill -1 $LASTPID > /dev/null 2>&1
	exit

fi

}
############################### Escritorio KDE.

if [ "$DESKTOP_SESSION" = "KDE" -o "$KDE_FULL_SESSION" = "true" ]; then 
	KDE=0;
else
	KDE=1;
fi

# Si no usamos KDE como escritorio pero está instalado y no queremos usar zenity, descometar esta linea.
#KDE=0

############################### Dependencias (Zenity | Kdialog, mplayer y rtmpdump).

if [ $KDE -eq 1 ]; then
	whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b zenity | grep -i "/zenity" > /dev/null 2>&1
	zenity=$?
	if [ $zenity -eq 1 ]; then
		xterm -fa default -fs 12 -bg white -fg black  -geometry 75x2 -T "Error" -e "echo 'No se ha podido encontrar el programa "zenity" instalado en su equipo' && sleep 5" ;
		exit
	fi

else
	whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b kdialog | grep -i "/kdialog" > /dev/null 2>&1
	kdialog=$?
	if [ $kdialog -eq 1 ]; then
		xterm -fa default -fs 12 -bg white -fg black  -geometry 75x2 -T "Error" -e "echo 'No se ha podido encontrar el programa "kdialog" instalado en su equipo' && sleep 5" ;
		exit
	fi
fi



whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b mplayer | grep -i "/mplayer" > /dev/null 2>&1
mplayer=$?
if [ $mplayer -eq 1 -a $KDE -eq 1 -a "$REPRODUCTOR" = "mplayer" ]; then
	zenity --no-wrap --error --text='No se ha podido encontrar el programa "mplayer" instalado en su equipo' ;
	exit
elif [ $mplayer -eq 1 -a $KDE -eq 0 -a "$REPRODUCTOR" = "mplayer" ]; then
	kdialog --title 'Dependencia no encontrada' --error 'No se ha podido encontrar el programa "mplayer" instalado en su equipo' ;
	exit
fi



whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b rtmpdump | grep -i "/rtmpdump" > /dev/null 2>&1
rtmpdump=$?
if [ $rtmpdump -eq 1  -a $KDE -eq 1 ]; then
	zenity --no-wrap --error --text='No se ha podido encontrar el programa "rtmpdump" instalado en su equipo' ;
	exit
elif [ $rtmpdump -eq 1  -a $KDE -eq 0 ]; then
	kdialog --title 'Dependencia no encontrada' --error 'No se ha podido encontrar el programa "rtmpdump" instalado en su equipo' ;
	exit
fi


################################ Curl como dependencia / Programación de cada canal. 

whereis -B "/usr/sbin" "/usr/local/sbin" "/sbin" "/usr/bin" "/usr/local/bin" "/bin" -b curl | grep -i "/curl" > /dev/null 2>&1
curl=$?
if [ $curl -eq 1 -a $KDE -eq 1 ]; then
	zenity --no-wrap --warning --timeout=2 --text='No se ha podido encontrar el programa "curl" instalado en su equipo, no podrá visualizar el nombre de los programas en activo' ;
	curl=1;

elif [ $curl -eq 1 -a $KDE -eq 0 ]; then

	kdialog --warningcontinuecancel 'No se ha podido encontrar el programa "curl" instalado en su equipo, no podrá visualizar el nombre de los programas en activo' ;
	curl=1;

else
	version # Comprobamos la versión del script llamando a la función para avisar al usuario.
	curl -s http://www.programacion-tdt.com/ahora.php | iconv -t utf-8 -f iso-8859-1 | grep -A 1 -i "<td" |  sed -e 's/<td width="250" valign="top">/Canal: /' -e 's/<\/td>/ /' -e 's/<\/tr>/ /' -e 's/<td width="70%"><span class="ind">/Programa: /' -e 's/<\/span> comenzó/ [/' -e 's/minutos/minutos ]/'  -e 's/segundos/segundos ]/' -e 's/     //' > /tmp/programacion
	curl=0;
fi



grep "Paramount Channel" /tmp/programacion > /dev/null 2>&1
programacion=$?
if [ $programacion -eq 1 -a $curl -eq 0 -a $KDE -eq 1 ]; then # Si no se encontraron los canales en el fichero pero sí está instalado curl (Fallo al conectar).
	zenity --no-wrap --warning --timeout=2 --text='No se ha podido descargar la programación de cada canal' ;
	curl=1;

elif [ $programacion -eq 1 -a $curl -eq 0 -a $KDE -eq 0 ]; then
	kdialog --warningcontinuecancel 'No se ha podido descargar la programación de cada canal' ;
	curl=1;


elif [ $curl -eq 0 ]; then  # Si curl está instalado y se ha podido descargar la lista de canales.

	AHORA=`date`;

	rtve1=`grep -A 1 "TVE1 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	rtve2=`grep -A 1 "La 2 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	rtve24=`grep -A 1 "Canal 24h $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	tdp=`grep -A 1 "Teledeporte $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Antena_3=`grep -A 1 "Antena 3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	La_Sexta=`grep -A 1 "La Sexta $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Cuatro=`grep -A 1 "Cuatro $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Tele5=`grep -A 1 "Telecinco $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Xplora=`grep -A 1 "xplora $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Nitro=`grep -A 1 "Nitro $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Neox=`grep -A 1 "A3 Neox $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	La_Sexta_3=`grep -A 1 "La Sexta 3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Paramount=`grep -A 1 "Paramount Channel $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Intereconomia=`grep -A 1 "Intereconomia TV $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Energy=`grep -A 1 "Energy $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	FDF=`grep -A 1 "FDF $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	Divinity=`grep -A 1 "Divinity $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'` 
	trecetv=`grep -A 1 "13 TV $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Cyl7=`grep -A 1 "cyl7 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	BarcelonaTV=`grep -A 1 "Barcelona TV $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Aragon_TV=`grep -A 1 "Aragon Television $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Galicia_TV_AM=`grep -A 1 "Galicia TV America $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	TPA_a7=`grep -A 1 "TPA a7 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Andalucia=`grep -A 1 "Canal Sur $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Canal9_24=`grep -A 1 "Noudos $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	IB3=`grep -A 1 "IB3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	TV3=`grep -A 1 "TV3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Esport3=`grep -A 1 "Esport3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	TV3_24=`grep -A 1 "3 24 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Super3=`grep -A 1 "Canal Super3 $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Canal_8=`grep -A 1 "8tv $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`
	Telemadrid_Otra=`grep -A 1 "La Otra $" /tmp/programacion | grep -i Programa | sed -e 's/Programa://'`	

	TV3CAT=" - "
	StvRioja=" - "
	TVRioja=" - "
	BusinessTV=" - ";
	Canarias_NET=" - ";
	Canarias=" - ";
	Lancelot=" - "
	Eldia_TV=" - "
	Onda_Azul=" - ";
	Ribera_TV=" - "
	Telemadrid_SAT=" - ";
	Etb_SAT=" - ";
	Discovery_Channel=" - ";
	TNT=" - ";
	Xtrm=" - ";
	SyFy=" - ";
	Cosmo=" - ";
	Galicia_TV_EU=" - "
	Teleminho=" - "
	Canal_33=" - "
	Abteve=" - "
	KissTV=" - "
	UnaCadiz=" - "
	EuroNews_ES=" - "
	France24=" - "
	PressTV=" - "
	TeleBilbao=" - "
	UnaCordoba=" - "
	Telebahia=" - "
	ImasTV=" - "
	ZaragozaTV=" - "
	TeleToledo=" - "
	Huelva_CNH=" - "
	LevanteTV=" - "
	InformacionTV=" - "
	PTV_Malaga=" - "
	CostadelSol_TV=" - "
	M95TV=" - "
	Humorbox=" - "
	MusicBox=" - "
	ShansonTV=" - "
	Russian_Today=" - "
	TeleSur=" - "
	AtelTV=" - "
	DatTV=" - "
	VTV=" - "
	IslaTV=" - "
	PromarTV=" - "
	DeluxeMusic=" - "
	GoticaTV=" - "
	LobasTV=" - "
	PartyTV=" - "
	Unlove=" - "
	Eska=" - "
	TV105=" - "
	RMC_TV=" - "
	LaBelleTV=" - "
	SoleilTV=" - "
	Funtv=" - "
	RblTV=" - "
	StreetclipTV=" - "
	Canal_Extremadura=" - "
	Aljazeera_Eng=" - "
	Esne_TV=" - "
	Huelva_TV=" - "
	LUX_Mallorca=" - "
	Huesca_TV=" - "
	TeleB=" - "
	TV_Girona=" - "
	RtvCE=" - "
	TVMelilla=" - "
	TVCS=" - "
	Astrocanalshop=" - "
	Ondamex=" - "
	CubaVision=" - "
	Panamericana=" - "
	Global_TV=" - "
	ATV_Sur=" - "
	AricaTV=" - "
	Cetelmon_TV=" - "
	SolidariaTV=" - "
	Hispan_TV=" - "
	VoTV=" - "
	RedBull=" - "
	TileSport=" - "
	Al_Iraqiya_Sports=" - "
	SportItalia=" - "
	SkyPoker=" - "
	Canal2=" - "
	Canal9=" - "
	Digital_Channel=" - "
	Enlace=" - "
	Canal33=" - "
	TVinet=" - "
	Itv=" - "
	RedTV=" - "
	MegaTV=" - "
	MetroTV=" - "
	TVnuevotiempo=" - "
	RTC=" - "
	TVu=" - "
	TVlota=" - "
	SenadoTV=" - "
	UATV=" - "
	UNIACCTV=" - "
	UMAGTV=" - "
	Horas24=" - "
	VaughanTV=" - "
	TamTV=" - "
	TVes=" - "
	TicTV=" - "
	TrpTV=" - "
	ArgentinisimaTV=" - "
	Canal10=" - "
	CBA24=" - "
	Canal21=" - "
	Canal3=" - "
	Canal5=" - "
	Canal7=" - "
	Canal9=" - "
	Canal_Provincial=" - "
	El_Rural=" - "
	El_trece=" - "
	Construir_TV=" - "
	PakaPaka=" - "
	QMusica=" - "
	Canal26=" - "
	TN=" - "
	Zona31=" - "
	N9=" - "
	Canal13=" - "
	Canal10_Tucuman=" - "
	LapachoTV=" - "
	TVO=" - "
	FacetasDeportivas=" - "
	Cable_Noticias=" - "
	Canal_Tiempo=" - "
	Tu_Kanal=" - "
	PyC=" - "
	Canal_Capital=" - "
	CMB=" - "
	CristoVision=" - "
	TeleVida=" - "
	RTVC=" - "
	RTVC2=" - "
	TeleCaribe=" - "
	TelePacifico=" - "
	RPC=" - "
	Paravision=" - "
	TeleFuturo=" - "
	TelevisaHD=" - "
	Milenio=" - "
	OnceTV=" - "
	Canal66=" - "
	Canal44=" - "
	Congreso=" - "
	Canal_Justicia=" - "
	Cortes_Diputados=" - "
	Kanal_D=" - "
	Sat7_Kids=" - "
	SmileofaChildTV=" - "
	NASA=" - "
	Barbaraki_TV=" - "
	Minika_GO=" - "
	Minika_Cocuk=" - "
	Yumurcak=" - "
	Gang_Cartoon_Channel=" - "
	RTS=" - "
	Canal1=" - "
	Ecuadortv=" - "
	Oromar=" - "

fi

############################## Temáticas de cada canal (Solo zenity).

	rtve1_tm=" Público generalista"
	rtve2_tm=" Público cultural"
	rtve24_tm=" Noticias 24/7 (ESP)"
	tdp_tm=" Público deportes"
	Antena_3_tm=" Generalista"
	La_Sexta_tm=" Generalista"
	Cuatro_tm=" Generalista"
	Tele5_tm=" Generalista/Amarillista"
	Xplora_tm=" Documentales/Masculino"
	Nitro_tm=" Series/Cine/Masculino"
	Neox_tm=" Series/Jóvenes"
	La_Sexta_3_tm=" Cine"
	Paramount_tm=" Cine"
	Intereconomia_tm=" Política/Religión"
	Energy_tm=" Documentales/Masculino"
	FDF_tm=" Series Tele5"
	Divinity_tm=" Series/Docu/Femenino"
	trecetv_tm=" Cine/Religión"
	Cyl7_tm=" Local Castilla León"
	BarcelonaTV_tm=" Local ciudad BCN"
	Aragon_TV_tm=" Local Aragón"
	Galicia_TV_AM_tm=" Local Galicia"
	TVRioja_tm=" Local La Rioja"
	TPA_a7_tm=" Local Asturias"
	Andalucia_tm=" Local Andalucía"
	Canal9_24_tm=" Local Valencia"
	IB3_tm=" Local Baleares"
	TV3_tm=" Local Cataluña"
	Esport3_tm=" Deportes Cataluña"
	TV3_24_tm=" Noticias 24/7 (CAT)"
	Super3_tm=" Infantil Cataluña"
	Canal_8_tm=" Local Cataluña"
	TV3CAT_tm=" Local Cataluña"
	StvRioja_tm=" Local La Rioja"
	BusinessTV_tm=" Política/Economía";
	Canarias_NET_tm=" Local Canarias";
	Canarias_tm=" Local Canarias";
	Lancelot_tm=" Local Lanzarote"
	Eldia_TV_tm=" Local Tenerife"
	Onda_Azul_tm=" Local Málaga";
	Ribera_TV_tm=" Local La Ribera"
	Telemadrid_SAT_tm=" Local Madrid";
	Telemadrid_Otra_tm=" Local Madrid";
	Etb_SAT_tm=" Local Vasco";
	Discovery_Channel_tm=" Documentales";
	TNT_tm=" Series/Cine"
	Xtrm_tm=" Cine/Acción";
	SyFy_tm=" Ciencia ficción";
	Cosmo_tm=" Canal femenino" 
	Galicia_TV_EU_tm=" Local Galicia"
	Teleminho_tm=" Local Ourense"
	Canal_33_tm=" Cultural Cataluña"
	Abteve_tm=" Local Albacete"
	KissTV_tm=" Música 24/7"
	UnaCadiz_tm=" Local Cádiz"
	EuroNews_ES_tm=" Noticias 24/7 (ESP)"
	France24_tm=" Noticias 24/7 (ENG)"
	PressTV_tm=" Noticias 24/7 (ENG)"
	NASA_tm=" Didáctico ciencia (ENG)"
	TeleBilbao_tm=" Local Bilbao"
	UnaCordoba_tm=" Local Córdoba"
	Telebahia_tm=" Local Santander"
	ImasTV_tm=" Local Ciudad Real"
	ZaragozaTV_tm=" Local Zaragoza"
	TeleToledo_tm=" Local Toledo"
	Huelva_CNH_tm=" Local Huelva"
	LevanteTV_tm=" Local Levante"
	InformacionTV_tm=" Local Alicante"
	PTV_Malaga_tm=" Local Málaga"
	CostadelSol_TV_tm=" Local Costa del Sol"
	M95TV_tm=" Local Marbella"
	Humorbox_tm=" Música 24/7 (RUS)"
	MusicBox_tm=" Música 24/7 (RUS)"
	ShansonTV_tm=" Música 24/7 (RUS/Global)"
	Russian_Today_tm=" Noticias 24/7 (ESP)"
	TeleSur_tm=" Generalista Venezuela"
	AtelTV_tm=" Generalista Venezuela"
	DatTV_tm=" Generalista Venezuela"
	VTV_tm=" Generalista Venezuela"
	IslaTV_tm=" Generalista Venezuela"
	PromarTV_tm=" Generalista Venezuela"
	TamTV_tm=" Noticias / Cultura Mérida"
	TVes_tm=" Generalista Venezuela"
	TicTV_tm=" Generalista Venezuela"
	TrpTV_tm=" Generalista Venezuela"
	TVO_tm=" Generalista Venezuela"
	DeluxeMusic_tm=" Música 24/7"
	GoticaTV_tm=" Música 24/7 Gótica"
	LobasTV_tm=" Música 24/7 Divas"
	PartyTV_tm=" Música 24/7"
	Unlove_tm=" Música 24/7"
	Eska_tm=" Música 24/7 (POL/Global)"
	TV105_tm=" Música 24/7"
	RMC_TV_tm=" Música 24/7 (FR/ITA)"
	LaBelleTV_tm=" Música 24/7 (FR)"
	SoleilTV_tm=" Música 24/7 (FR)"
	Funtv_tm=" Música 24/7 (RUS/Global)"
	RblTV_tm=" Música 24/7 (RUS/Global)"
	StreetclipTV_tm=" Música 24/7 Rock Metal"
	Canal_Extremadura_tm=" Local Extremadura"
	Aljazeera_Eng_tm=" Noticias 24/7 (ENG)"
	Esne_TV_tm=" Religión Arizona (ESP)"
	Huelva_TV_tm=" Local Huelva"
	LUX_Mallorca_tm=" Local Mallorca"
	Huesca_TV_tm=" Local Huesca"
	TeleB_tm=" Local Badalona"
	TV_Girona_tm=" Local Girona"
	RtvCE_tm=" Local Ceuta"
	TVMelilla_tm=" Local Melilla"
	TVCS_tm=" Local Castellón"
	Astrocanalshop_tm=" Teletienda"
	Ondamex_tm=" Tarot/Contactos"
	CubaVision_tm=" Generalista Cuba"
	Panamericana_tm=" Generalista Perú"
	Global_TV_tm=" Generalista Perú"
	ATV_Sur_tm=" Generalista Perú"
	AricaTV_tm=" Generalista Chile"
	Canal2_tm=" Generalista Chile"
	Canal9_tm=" Generalista Chile"
	Digital_Channel_tm=" Generalista Chile"
	Enlace_tm=" Generalista Chile"
	Canal33_tm=" Generalista Chile"
	TVinet_tm=" Generalista Chile"
	Itv_tm=" Generalista Chile"
	RedTV_tm=" Generalista Chile"
	MegaTV_tm=" Generalista Chile"
	MetroTV_tm=" TV Metro de Santiago"
	TVnuevotiempo_tm=" Religión Chile"
	RTC_tm=" Generalista Chile"
	TVlota_tm=" Generalista Chile"
	SenadoTV_tm=" TV Senado Chile"
	TVu_tm=" Universidad Concepción"
	UNIACCTV_tm=" Universidad ACC"
	UATV_tm=" Universidad Autónoma"
	UMAGTV_tm=" Universidad Magallanes"
	Horas24_tm=" Generalista Chile"
	Cetelmon_TV_tm=" Religión Alicante"
	SolidariaTV_tm=" Religión Vitoria"
	Hispan_TV_tm=" Noticias 24/7 Irán (ESP)"
	VoTV_tm=" Local Cataluña"
	RedBull_tm=" Deportes/Música (ENG)"
	TileSport_tm=" Deportes 24/7 (GRE)"
	Al_Iraqiya_Sports_tm=" Deportes 24/7 (IRQ)"
	SportItalia_tm=" Deportes 24/7 (ITA)"
	SkyPoker_tm=" Poker 24/7 (ENG)"
	VaughanTV_tm=" Aprender Inglés (ENG/ESP)"
	Canal10_tm=" Local Córdoba"
	CBA24_tm=" Local Córdoba"
	ArgentinisimaTV_tm=" Generalista Argentina"
	Canal3_tm=" Generalista Argentina"
	Canal7_tm=" Generalista Argentina"
	Canal9_tm=" Generalista Argentina"
	Canal_Provincial_tm=" Generalista Argentina"
	Zona31_tm=" Generalista Argentina"
	El_trece_tm=" Generalista Argentina"
	Canal13_tm=" Generalista Argentina"
	Canal10_Tucuman_tm=" Local Tucumán"
	LapachoTV_tm=" Generalista Argentina"
	N9_tm=" Generalista/Noticias"
	Canal21_tm=" Religión Buenos Aires"
	Construir_TV_tm=" Tema construcción"
	El_Rural_tm=" Mundo rural"
	PakaPaka_tm=" Infantil/Educativo"
	QMusica_tm=" Música 24/7 (ESP)"
	Canal5_tm=" Noticias 24/7"
	Canal26_tm=" Noticias 24/7"
	TN_tm=" Noticias 24/7"
	FacetasDeportivas_tm=" Deportes 24/7"
	Cable_Noticias_tm=" Noticias 24/7"
	Canal_Tiempo_tm=" Meteorología/Noticias"
	Tu_Kanal_tm=" Generalista Colombia"
	PyC_tm=" Generalista Colombia"
	Canal_Capital_tm=" Generalista Colombia"
	CMB_tm=" Religión Colombia"
	CristoVision_tm=" Religión Colombia"
	TeleVida_tm=" Religión Colombia"
	RTVC_tm=" Generalista Colombia"
	RTVC2_tm=" Generalista Colombia"
	TeleCaribe_tm=" Generalista Colombia"
	TelePacifico_tm=" Generalista Colombia"
######

	RPC_tm=" Generalista Paraguay"
	Paravision_tm=" Generalista Paraguay"
	TeleFuturo_tm=" Generalista Paraguay"
	TelevisaHD_tm=" Generalista Mexico"
	Milenio_tm=" Noticias/Política" 
	OnceTV_tm=" Generalista Mexico"
	Canal66_tm=" Noticias/Reportajes"
	Canal44_tm=" Noticias/Reportajes"
	Congreso_tm=" Canal del congreso"
	Canal_Justicia_tm=" Ministerio Justicia"
	Cortes_Diputados_tm=" Cortes Dicupatos"
	Kanal_D_tm=" Infantil/Educativo (SR)"
	Sat7_Kids_tm=" Infantil/Educativo (EN)"
	SmileofaChildTV_tm=" Infantil/Educativo (EN)"
	Barbaraki_TV_tm=" Infantil/Educativo (RUS)"
	Minika_GO_tm=" Infantil/Educativo (TUR)"
	Minika_Cocuk_tm=" Infantil/Educativo (TUR)"
	Yumurcak_tm=" Infantil/Educativo (TUR)"
	Gang_Cartoon_Channel_tm=" Infantil/Anime (THA)"
	RTS_tm=" Generalista Ecuador"
	Canal1_tm=" Generalista Ecuador"
	Ecuadortv_tm=" Generalista Ecuador"
	Oromar_tm=" Generalista Ecuador"

############################## Canales.

if [ $curl -eq 0  -a $KDE -eq 1 ]; then
	CANAL=`zenity --window-icon="/usr/share/icons/hicolor/48x48/devices/totem-tv.png" --list --title="TVenLinux ($V_script)" --text="Seleccione un canal" --height=450 --width=750 --column="Canales" --column="Temática" --column="Emisión $AHORA " "rtve1" "$rtve1_tm" "$rtve1" "rtve2" "$rtve2_tm" "$rtve2" "rtve24" "$rtve24_tm" "$rtve24" "Antena_3" "$Antena_3_tm" "$Antena_3" "Cuatro" "$Cuatro_tm" "$Cuatro" "Tele5" "$Tele5_tm" "$Tele5" "La_Sexta" "$La_Sexta_tm" "$La_Sexta" "Xplora" "$Xplora_tm" "$Xplora" "Discovery_Channel" "$Discovery_Channel_tm" "$Discovery_Channel" "Energy" "$Energy_tm" "$Energy" "Nitro" "$Nitro_tm" "$Nitro" "Neox" "$Neox_tm" "$Neox" "Divinity" "$Divinity_tm" "$Divinity" "SyFy" "$SyFy_tm" "$SyFy" "Xtrm" "$Xtrm_tm" "$Xtrm" "TNT" "$TNT_tm" "$TNT" "FDF" "$FDF_tm" "$FDF" "Cosmo" "$Cosmo_tm" "$Cosmo" "13TV" "$trecetv_tm" "$trecetv" "Intereconomia" "$Intereconomia_tm" "$Intereconomia" "BusinessTV" "$BusinessTV_tm" "$BusinessTV" "La_Sexta_3" "$La_Sexta_3_tm" "$La_Sexta_3" "Paramount" "$Paramount_tm" "$Paramount" "VaughanTV" "$VaughanTV_tm" "$VaughanTV"  "Kanal_D" "$Kanal_D_tm" "$Kanal_D" "Sat7_Kids" "$Sat7_Kids_tm" "$Sat7_Kids" "SmileofaChildTV" "$SmileofaChildTV_tm" "$SmileofaChildTV" "Barbaraki_TV" "$Barbaraki_TV_tm" "$Barbaraki_TV" "Minika_GO" "$Minika_GO_tm" "$Minika_GO" "Minika_Cocuk" "$Minika_Cocuk_tm" "$Minika_Cocuk" "Yumurcak" "$Yumurcak_tm" "$Yumurcak" "Gang_Cartoon_Channel" "$Gang_Cartoon_Channel_tm" "$Gang_Cartoon_Channel" "Aljazeera_Eng" "$Aljazeera_Eng_tm" "$Aljazeera_Eng"  "EuroNews_ES" "$EuroNews_ES_tm" "$EuroNews_ES" "France24" "$France24_tm" "$France24" "PressTV" "$PressTV_tm" "$PressTV" "NASA" "$NASA_tm" "$NASA" "Russian_Today" "$Russian_Today_tm" "$Russian_Today" "Cetelmon_TV" "$Cetelmon_TV_tm" "$Cetelmon_TV" "Ondamex" "$Ondamex_tm" "$Ondamex" "KissTV" "$KissTV_tm" "$KissTV" "DeluxeMusic" "$DeluxeMusic_tm" "$DeluxeMusic" "Eska" "$Eska_tm" "$Eska" "GoticaTV" "$GoticaTV_tm" "$GoticaTV" "Humorbox" "$Humorbox_tm" "$Humorbox" "Funtv" "$Funtv_tm" "$Funtv" "RblTV" "$RblTV_tm" "$RblTV" "LobasTV" "$LobasTV_tm" "$LobasTV" "MusicBox" "$MusicBox_tm" "$MusicBox" "PartyTV" "$PartyTV_tm" "$PartyTV" "RMC_TV" "$RMC_TV_tm" "$RMC_TV" "ShansonTV" "$ShansonTV_tm" "$ShansonTV" "TV105" "$TV105_tm" "$TV105" "Unlove" "$Unlove_tm" "$Unlove" "StreetclipTV" "$StreetclipTV_tm" "$StreetclipTV" "SoleilTV" "$SoleilTV_tm" "$SoleilTV" "LaBelleTV" "$LaBelleTV_tm" "$LaBelleTV" "Esport3" "$Esport3_tm" "$Esport3" "Al_Iraqiya_Sports" "$Al_Iraqiya_Sports_tm" "$Al_Iraqiya_Sports" "SkyPoker" "$SkyPoker_tm" "$SkyPoker" "SportItalia" "$SportItalia_tm" "$SportItalia" "tdp" "$tdp_tm" "$tdp" "TileSport" "$TileSport_tm" "$TileSport" "RedBull" "$RedBull_tm" "$RedBull" "Abteve" "$Abteve_tm" "$Abteve" "Andalucia" "$Andalucia_tm" "$Andalucia" "Aragon_TV" "$Aragon_TV_tm" "$Aragon_TV" "BarcelonaTV" "$BarcelonaTV_tm" "$BarcelonaTV" "Canal_33" "$Canal_33_tm" "$Canal_33" "Canal_8" "$Canal_8_tm" "$Canal_8" "Canal_Extremadura" "$Canal_Extremadura_tm" "$Canal_Extremadura" "Canal9_24" "$Canal9_24_tm" "$Canal9_24" "Canarias" "$Canarias_tm" "$Canarias" "Canarias_NET" "$Canarias_NET_tm" "$Canarias_NET" "Lancelot" "$Lancelot_tm" "$Lancelot" "CostadelSol_TV" "$CostadelSol_TV_tm" "$CostadelSol_TV" "Cyl7" "$Cyl7_tm" "$Cyl7" "Eldia_TV" "$Eldia_TV_tm" "$Eldia_TV" "Etb_SAT" "$Etb_SAT_tm" "$Etb_SAT" "Galicia_TV_AM" "$Galicia_TV_AM_tm" "$Galicia_TV_AM" "Galicia_TV_EU" "$Galicia_TV_EU_tm" "$Galicia_TV_EU" "Teleminho" "$Teleminho_tm" "$Teleminho" "Hispan_TV" "$Hispan_TV_tm" "$Hispan_TV" "Huelva_CNH" "$Huelva_CNH_tm" "$Huelva_CNH" "Huelva_TV" "$Huelva_TV_tm" "$Huelva_TV" "Huesca_TV" "$Huesca_TV_tm" "$Huesca_TV" "IB3" "$IB3_tm" "$IB3" "ImasTV" "$ImasTV_tm" "$ImasTV" "InformacionTV" "$InformacionTV_tm" "$InformacionTV" "LevanteTV" "$LevanteTV_tm" "$LevanteTV" "LUX_Mallorca" "$LUX_Mallorca_tm" "$LUX_Mallorca" "M95TV" "$M95TV_tm" "$M95TV" "Onda_Azul" "$Onda_Azul_tm" "$Onda_Azul" "PTV_Malaga" "$PTV_Malaga_tm" "$PTV_Malaga" "Ribera_TV" "$Ribera_TV_tm" "$Ribera_TV" "RtvCE" "$RtvCE_tm" "$RtvCE" "Super3" "$Super3_tm" "$Super3" "StvRioja" "$StvRioja_tm" "$StvRioja" "TeleB" "$TeleB_tm" "$TeleB" "Telebahia" "$Telebahia_tm" "$Telebahia" "TeleBilbao" "$TeleBilbao_tm" "$TeleBilbao" "Telemadrid_SAT" "$Telemadrid_SAT_tm" "$Telemadrid_SAT" "Telemadrid_Otra" "$Telemadrid_Otra_tm" "$Telemadrid_Otra" "TeleToledo" "$TeleToledo_tm" "$TeleToledo" "TPA_a7" "$TPA_a7_tm" "$TPA_a7" "TV_Girona" "$TV_Girona_tm" "$TV_Girona" "TV3" "$TV3_tm" "$TV3" "TV3CAT" "$TV3CAT_tm" "$TV3CAT" "TV3_24" "$TV3_24_tm" "$TV3_24" "TVCS" "$TVCS_tm" "$TVCS" "TVMelilla" "$TVMelilla_tm" "$TVMelilla" "TVRioja" "$TVRioja_tm" "$TVRioja" "UnaCadiz" "$UnaCadiz_tm" "$UnaCadiz" "UnaCordoba" "$UnaCordoba_tm" "$UnaCordoba" "VoTV" "$VoTV_tm" "$VoTV" "ZaragozaTV" "$ZaragozaTV_tm" "$ZaragozaTV" "Esne_TV" "$Esne_TV_tm" "$Esne_TV" "Astrocanalshop" "$Astrocanalshop_tm" "$Astrocanalshop" "SolidariaTV" "$SolidariaTV_tm" "$SolidariaTV" "" "" "" "Global_TV" "$Global_TV_tm" "$Global_TV" "ATV_Sur" "$ATV_Sur_tm" "$ATV_Sur" "Panamericana" "$Panamericana_tm" "$Panamericana" "" "" "" "CubaVision" "$CubaVision_tm" "$CubaVision" "" "" "" "AricaTV" "$AricaTV_tm" "$AricaTV" "Canal2" "$Canal2_tm" "$Canal2" "Canal9" "$Canal9_tm" "$Canal9" "Digital_Channel" "$Digital_Channel_tm" "$Digital_Channel" "Enlace" "$Enlace_tm" "$Enlace" "Canal33" "$Canal33_tm" "$Canal33" "TVinet" "$TVinet_tm" "$TVinet" "Itv" "$Itv_tm" "$Itv" "RedTV" "$RedTV_tm" "$RedTV" "MegaTV" "$MegaTV_tm" "$MegaTV" "MetroTV" "$MetroTV_tm" "$MetroTV" "TVnuevotiempo" "$TVnuevotiempo_tm" "$TVnuevotiempo" "RTC" "$RTC_tm" "$RTC" "TVu" "$TVu_tm" "$TVu" "TVlota" "$TVlota_tm" "$TVlota" "SenadoTV" "$SenadoTV_tm" "$SenadoTV" "UNIACCTV" "$UNIACCTV_tm" "$UNIACCTV" "UATV" "$UATV_tm" "$UATV" "UMAGTV" "$UMAGTV_tm" "$UMAGTV" "Horas24" "$Horas24_tm" "$Horas24" "" "" "" "TeleSur" "$TeleSur_tm" "$TeleSur" "AtelTV" "$AtelTV_tm" "$AtelTV" "DatTV" "$DatTV_tm" "$DatTV" "VTV" "$VTV_tm" "$VTV" "IslaTV" "$IslaTV_tm" "$IslaTV" "PromarTV" "$PromarTV_tm" "$PromarTV" "TamTV" "$TamTV_tm" "$TamTV" "TVes" "$TVes_tm" "$TVes" "TicTV" "$TicTV_tm" "$TicTV" "TrpTV" "$TrpTV_tm" "$TrpTV" "TVO" "$TVO_tm" "$TVO" "" "" "" "Canal10" "$Canal10_tm" "$Canal10" "CBA24" "$CBA24_tm" "$CBA24" "ArgentinisimaTV" "$ArgentinisimaTV_tm" "$ArgentinisimaTV" "Canal3" "$Canal3_tm" "$Canal3" "Canal7" "$Canal7_tm" "$Canal7" "Canal9" "$Canal9_tm" "$Canal9" "Canal_Provincial" "$Canal_Provincial_tm" "$Canal_Provincial" "Zona31" "$Zona31_tm" "$Zona31" "El_trece" "$El_trece_tm" "$El_trece" "Canal21" "$Canal21_tm" "$Canal21" "Construir_TV" "$Construir_TV_tm" "$Construir_TV" "El_Rural" "$El_Rural_tm" "$El_Rural" "PakaPaka" "$PakaPaka_tm" "$PakaPaka" "QMusica" "$QMusica_tm" "$QMusica" "Canal5" "$Canal5_tm" "$Canal5" "Canal26" "$Canal26_tm" "$Canal26" "N9" "$N9_tm" "$N9" "TN" "$TN_tm" "$TN" "Canal13" "$Canal13_tm" "$Canal13" "Canal10_Tucuman" "$Canal10_Tucuman_tm" "$Canal10_Tucuman" "LapachoTV" "$LapachoTV_tm" "$LapachoTV" "" "" "" "FacetasDeportivas" "$FacetasDeportivas_tm" "$FacetasDeportivas" "" "" "" "Cable_Noticias" "$Cable_Noticias_tm" "$Cable_Noticias" "Canal_Tiempo" "$Canal_Tiempo_tm" "$Canal_Tiempo" "Tu_Kanal" "$Tu_Kanal_tm" "$Tu_Kanal" "PyC" "$PyC_tm" "$PyC" "Canal_Capital" "$Canal_Capital_tm" "$Canal_Capital" "CMB" "$CMB_tm" "$CMB" "CristoVision" "$CristoVision_tm" "$CristoVision" "TeleVida" "$TeleVida_tm" "$TeleVida" "RTVC" "$RTVC_tm" "$RTVC" "RTVC2" "$RTVC2_tm" "$RTVC2" "TeleCaribe" "$TeleCaribe_tm" "$TeleCaribe" "TelePacifico" "$TelePacifico_tm" "$TelePacifico" "" "" "" "RPC" "$RPC_tm" "$RPC" "Paravision" "$Paravision_tm" "$Paravision" "TeleFuturo" "$TeleFuturo_tm" "$TeleFuturo" "" "" "" "TelevisaHD" "$TelevisaHD_tm" "$TelevisaHD" "Milenio" "$Milenio_tm" "$Milenio" "OnceTV" "$OnceTV_tm" "$OnceTV" "Canal66" "$Canal66_tm" "$Canal66" "Canal44" "$Canal44_tm" "$Canal44" "Congreso" "$Congreso_tm" "$Congreso" "Canal_Justicia" "$Canal_Justicia_tm" "$Canal_Justicia" "Cortes_Diputados" "$Cortes_Diputados_tm" "$Cortes_Diputados" "" "" "" "RTS" "$RTS_tm" "$RTS" "Canal1" "$Canal1_tm" "$Canal1" "Ecuadortv" "$Ecuadortv_tm" "$Ecuadortv" "Oromar" "$Oromar_tm" "$Oromar"`

elif [ $curl -eq 0  -a $KDE -eq 0 ]; then
	CANAL=`kdialog  --title "TVenLinux ($V_script)" --geometry 650x600 --menu "Seleccione un canal  [ $AHORA ]" "rtve1" "rtve1     ---   $rtve1" "rtve2" "rtve2     ---   $rtve2" "rtve24" "rtve24     ---   $rtve24" "Antena_3" "Antena_3     ---   $Antena_3" "Cuatro" "Cuatro     ---   $Cuatro" "Tele5" "Tele5     ---   $Tele5" "La_Sexta" "La_Sexta     ---   $La_Sexta" "Xplora" "Xplora     ---   $Xplora" "Discovery_Channel" "Discovery_Channel     ---   $Discovery_Channel_tm" "Energy" "Energy     ---   $Energy" "Nitro" "Nitro     ---   $Nitro" "Neox" "Neox     ---   $Neox" "Divinity" "Divinity     ---   $Divinity" "SyFy" "SyFy     ---   $SyFy_tm" "Xtrm" "Xtrm     ---   $Xtrm_tm" "TNT" "TNT     ---   $TNT_tm" "FDF" "FDF     ---   $FDF" "Cosmo" "Cosmo     ---   $Cosmo_tm" "13TV" "13TV     ---   $trecetv" "Intereconomia" "Intereconomia     ---   $Intereconomia" "BusinessTV" "BusinessTV     ---   $BusinessTV_tm" "La_Sexta_3" "La_Sexta_3     ---   $La_Sexta_3" "Paramount" "Paramount     ---   $Paramount" "VaughanTV" "VaughanTV     ---   $VaughanTV_tm" "Kanal_D" "Kanal_D     ---   $Kanal_D_tm" "Sat7_Kids" "Sat7_Kids     ---   $Sat7_Kids_tm" "SmileofaChildTV" "SmileofaChildTV     ---   $SmileofaChildTV_tm" "Barbaraki_TV" "Barbaraki_TV     ---   $Barbaraki_TV_tm" "Minika_GO" "Minika_GO     ---   $Minika_GO_tm" "Minika_Cocuk" "Minika_Cocuk     ---   $Minika_Cocuk_tm" "Yumurcak" "Yumurcak     ---   $Yumurcak_tm" "Gang_Cartoon_Channel" "Gang_Cartoon_Channel     ---   $Gang_Cartoon_Channel_tm" "Aljazeera_Eng" "Aljazeera_Eng     ---   $Aljazeera_Eng_tm" "EuroNews_ES" "EuroNews_ES     ---   $EuroNews_ES_tm" "France24" "France24     ---   $France24_tm" "PressTV" "PressTV     ---   $PressTV_tm" "Russian_Today" "Russian_Today     ---   $Russian_Today_tm" "NASA" "NASA     ---   $NASA_tm" "Cetelmon_TV" "Cetelmon_TV     ---   $Cetelmon_TV_tm" "Ondamex" "Ondamex     ---   $Ondamex_tm" "KissTV" "KissTV     ---   $KissTV_tm" "DeluxeMusic" "DeluxeMusic     ---   $DeluxeMusic_tm" "Eska" "Eska     ---   $Eska_tm" "GoticaTV" "GoticaTV     ---   $GoticaTV_tm" "Humorbox" "Humorbox     ---   $Humorbox_tm" "Funtv" "Funtv     ---   $Funtv_tm" "RblTV" "RblTV     ---   $RblTV_tm" "LobasTV" "LobasTV     ---   $LobasTV_tm" "MusicBox" "MusicBox     ---   $MusicBox_tm" "PartyTV" "PartyTV     ---   $PartyTV_tm" "RMC_TV" "RMC_TV     ---   $RMC_TV_tm" "ShansonTV" "ShansonTV     ---   $ShansonTV_tm" "TV105" "TV105     ---   $TV105_tm" "Unlove" "Unlove     ---   $Unlove_tm" "StreetclipTV" "StreetclipTV     ---   $StreetclipTV_tm" "SoleilTV" "SoleilTV     ---   $SoleilTV_tm" "LaBelleTV" "LaBelleTV     ---   $LaBelleTV_tm" "Esport3" "Esport3     ---   $Esport3" "Al_Iraqiya_Sports" "Al_Iraqiya_Sports     ---   $Al_Iraqiya_Sports_tm" "SkyPoker" "SkyPoker     ---   $SkyPoker_tm" "SportItalia" "SportItalia     ---   $SportItalia_tm" "tdp" "tdp     ---   $tdp" "TileSport" "TileSport     ---   $TileSport_tm" "RedBull" "RedBull     ---   $RedBull_tm" "Abteve" "Abteve     ---   $Abteve_tm" "Andalucia" "Andalucia     ---   $Andalucia" "Aragon_TV" "Aragon_TV     ---   $Aragon_TV_tm" "BarcelonaTV" "BarcelonaTV     ---   $BarcelonaTV" "Canal_33" "Canal_33     ---   $Canal_33_tm" "Canal_8" "Canal_8     ---   $Canal_8" "Canal_Extremadura" "Canal_Extremadura     ---   $Canal_Extremadura_tm" "Canal9_24" "Canal9_24     ---   $Canal9_24" "Canarias" "Canarias     ---   $Canarias_tm" "Canarias_NET" "Canarias_NET     ---   $Canarias_NET_tm" "Lancelot" "Lancelot     ---   $Lancelot_tm" "CostadelSol_TV" "CostadelSol_TV     ---   $CostadelSol_TV_tm" "Cyl7" "Cyl7     ---   $Cyl7" "Eldia_TV" "Eldia_TV     ---   $Eldia_TV_tm" "Etb_SAT" "Etb_SAT     ---   $Etb_SAT_tm" "Galicia_TV_AM" "Galicia_TV_AM     ---   $Galicia_TV_AM" "Galicia_TV_EU" "Galicia_TV_EU     ---   $Galicia_TV_EU_tm" "Teleminho" "Teleminho     ---   $Teleminho_tm" "Hispan_TV" "Hispan_TV     ---   $Hispan_TV_tm" "Huelva_CNH" "Huelva_CNH     ---   $Huelva_CNH_tm" "Huelva_TV" "Huelva_TV     ---   $Huelva_TV_tm" "Huesca_TV" "Huesca_TV     ---   $Huesca_TV_tm" "IB3" "IB3     ---   $IB3" "ImasTV" "ImasTV     ---   $ImasTV_tm" "InformacionTV" "InformacionTV     ---   $InformacionTV_tm" "LevanteTV" "LevanteTV     ---   $LevanteTV_tm" "LUX_Mallorca" "LUX_Mallorca     ---   $LUX_Mallorca_tm" "M95TV" "M95TV     ---   $M95TV_tm" "Onda_Azul" "Onda_Azul     ---   $Onda_Azul_tm" "PTV_Malaga" "PTV_Malaga     ---   $PTV_Malaga_tm" "Ribera_TV" "Ribera_TV     ---   $Ribera_TV_tm" "RtvCE" "RtvCE     ---   $RtvCE_tm" "Super3" "Super3     ---   $Super3" "StvRioja" "StvRioja     ---   $StvRioja_tm" "TeleB" "TeleB     ---   $TeleB_tm" "Telebahia" "Telebahia     ---   $Telebahia_tm" "TeleBilbao" "TeleBilbao     ---   $TeleBilbao_tm" "Telemadrid_SAT" "Telemadrid_SAT     ---   $Telemadrid_SAT_tm" "Telemadrid_Otra" "Telemadrid_Otra     ---   $Telemadrid_Otra_tm" "TeleToledo" "TeleToledo     ---   $TeleToledo_tm" "TPA_a7" "TPA_a7     ---   $TPA_a7" "TV_Girona" "TV_Girona     ---   $TV_Girona_tm" "TV3" "TV3     ---   $TV3" "TV3CAT" "TV3CAT     ---   $TV3CAT_tm" "TV3_24" "TV3_24     ---   $TV3_24" "TVCS" "TVCS     ---   $TVCS_tm" "TVMelilla" "TVMelilla     ---   $TVMelilla_tm" "TVRioja" "TVRioja     ---   $TVRioja_tm" "UnaCadiz" "UnaCadiz     ---   $UnaCadiz_tm" "UnaCordoba" "UnaCordoba     ---   $UnaCordoba_tm" "VoTV" "VoTV     ---   $VoTV_tm" "ZaragozaTV" "ZaragozaTV     ---   $ZaragozaTV_tm" "Esne_TV" "Esne_TV     ---   $Esne_TV_tm" "Astrocanalshop" "Astrocanalshop     ---   $Astrocanalshop_tm" "SolidariaTV" "SolidariaTV     ---   $SolidariaTV_tm" "" "" "Global_TV" "Global_TV     ---   $Global_TV_tm" "ATV_Sur" "ATV_Sur     ---   $ATV_Sur_tm" "Panamericana" "Panamericana     ---   $Panamericana_tm" "" "" "CubaVision" "CubaVision     ---   $CubaVision_tm" "" "" "AricaTV" "AricaTV     ---   $AricaTV_tm" "Canal2" "Canal2     ---   $Canal2_tm" "Canal9" "Canal9     ---   $Canal9_tm" "Digital_Channel" "Digital_Channel     ---   $Digital_Channel_tm" "Enlace" "Enlace     ---   $Enlace_tm" "Canal33" "Canal33     ---   $Canal33_tm" "TVinet" "TVinet     ---   $TVinet_tm" "Itv" "Itv     ---   $Itv_tm" "RedTV" "RedTV     ---   $RedTV_tm" "MegaTV" "MegaTV     ---   $MegaTV_tm" "MetroTV" "MetroTV     ---   $MetroTV_tm" "TVnuevotiempo" "TVnuevotiempo     ---   $TVnuevotiempo_tm" "RTC" "RTC     ---   $RTC_tm" "TVu" "TVu     ---   $TVu_tm" "TVlota" "TVlota     ---   $TVlota_tm" "SenadoTV" "SenadoTV     ---   $SenadoTV_tm" "UNIACCTV" "UNIACCTV     ---   $UNIACCTV_tm" "UATV" "UATV     ---   $UATV_tm" "UMAGTV" "UMAGTV     ---   $UMAGTV_tm" "Horas24" "Horas24     ---   $Horas24_tm" "" "" "TeleSur" "TeleSur     ---   $TeleSur_tm" "AtelTV" "AtelTV     ---   $AtelTV_tm" "DatTV" "DatTV     ---   $DatTV_tm" "VTV" "VTV     ---   $VTV_tm" "IslaTV" "IslaTV     ---   $IslaTV_tm" "PromarTV" "PromarTV     ---   $PromarTV_tm" "TamTV" "TamTV     ---   $TamTV_tm" "TVes" "TVes     ---   $TVes_tm" "TicTV" "TicTV     ---   $TicTV_tm" "TrpTV" "TrpTV     ---   $TrpTV_tm" "TVO" "TVO     ---   $TVO_tm" "" "" "Canal10" "Canal10     ---   $Canal10_tm" "CBA24" "CBA24     ---   $CBA24_tm" "ArgentinisimaTV" "ArgentinisimaTV     ---   $ArgentinisimaTV_tm" "Canal3" "Canal3     ---   $Canal3_tm" "Canal7" "Canal7     ---   $Canal7_tm" "Canal9" "Canal9     ---   $Canal9_tm" "Canal_Provincial" "Canal_Provincial     ---   $Canal_Provincial_tm" "Zona31" "Zona31     ---   $Zona31_tm" "El_trece" "El_trece     ---   $El_trece_tm" "Canal21" "Canal21     ---   $Canal21_tm" "Construir_TV" "Construir_TV     ---   $Construir_TV_tm" "El_Rural" "El_Rural     ---   $El_Rural_tm" "PakaPaka" "PakaPaka     ---   $PakaPaka_tm" "QMusica" "QMusica     ---   $QMusica_tm" "Canal5" "Canal5     ---   $Canal5_tm" "Canal26" "Canal26     ---   $Canal26_tm" "TN" "TN     ---   $TN_tm" "N9" "N9     ---   $N9_tm" "Canal13" "Canal13     ---   $Canal13_tm" "Canal10_Tucuman" "Canal10_Tucuman     ---   $Canal10_Tucuman_tm" "LapachoTV" "LapachoTV     ---   $LapachoTV_tm" "" "" "FacetasDeportivas" "FacetasDeportivas     ---   $FacetasDeportivas_tm" "" "" "Cable_Noticias" "Cable_Noticias     ---   $Cable_Noticias_tm" "Canal_Tiempo" "Canal_Tiempo     ---   $Canal_Tiempo_tm" "Tu_Kanal" "Tu_Kanal     ---   $Tu_Kanal_tm" "PyC" "PyC     ---   $PyC_tm" "Canal_Capital" "Canal_Capital     ---   $Canal_Capital_tm" "CMB" "CMB     ---   $CMB_tm" "CristoVision" "CristoVision     ---   $CristoVision_tm" "TeleVida" "TeleVida     ---   $TeleVida_tm" "RTVC" "RTVC     ---   $RTVC_tm" "RTVC2" "RTVC2     ---   $RTVC2_tm" "TeleCaribe" "TeleCaribe     ---   $TeleCaribe_tm" "TelePacifico" "TelePacifico     ---   $TelePacifico_tm" "" "" "RPC" "RPC     ---   $RPC_tm" "Paravision" "Paravision     ---   $Paravision_tm" "TeleFuturo" "TeleFuturo     ---   $TeleFuturo_tm" "" "" "TelevisaHD" "TelevisaHD     ---   $TelevisaHD_tm" "Milenio" "Milenio     ---   $Milenio_tm" "OnceTV" "OnceTV     ---   $OnceTV_tm" "Canal66" "Canal66     ---   $Canal66_tm" "Canal44" "Canal44     ---   $Canal44_tm" "Congreso" "Congreso     ---   $Congreso_tm" "Canal_Justicia" "Canal_Justicia     ---   $Canal_Justicia_tm" "Cortes_Diputados" "Cortes_Diputados     ---   $Cortes_Diputados_tm" "" "" "RTS" "RTS     ---   $RTS_tm" "Canal1" "Canal1     ---   $Canal1_tm" "Ecuadortv" "Ecuadortv     ---   $Ecuadortv_tm" "Oromar" "Oromar     ---   $Oromar_tm"`




elif [ $curl -eq 1  -a $KDE -eq 1 ]; then
	
	# Si no se pudo conectar a la programación mostramos este dialogo sin la programación.
	CANAL=`zenity --window-icon="/usr/share/icons/hicolor/48x48/devices/totem-tv.png" --list --title="TVenLinux ($V_script)" --text="Seleccione un canal" --height=450 --width=370 --column="Canales" --column="Temática" "rtve1" "$rtve1_tm" "rtve2" "$rtve2_tm" "rtve24" "$rtve24_tm" "Antena_3" "$Antena_3_tm" "Cuatro" "$Cuatro_tm" "Tele5" "$Tele5_tm" "La_Sexta" "$La_Sexta_tm" "Xplora" "$Xplora_tm" "Discovery_Channel" "$Discovery_Channel_tm" "Energy" "$Energy_tm" "Nitro" "$Nitro_tm" "Neox" "$Neox_tm" "Divinity" "$Divinity_tm" "SyFy" "$SyFy_tm" "Xtrm" "$Xtrm_tm" "TNT" "$TNT_tm" "FDF" "$FDF_tm" "Cosmo" "$Cosmo_tm" "13TV" "$trecetv_tm" "Intereconomia" "$Intereconomia_tm" "BusinessTV" "$BusinessTV_tm" "La_Sexta_3" "$La_Sexta_3_tm" "Paramount" "$Paramount_tm" "VaughanTV" "$VaughanTV_tm" "Kanal_D" "$Kanal_D_tm" "Sat7_Kids" "$Sat7_Kids_tm" "SmileofaChildTV" "$SmileofaChildTV_tm" "Barbaraki_TV" "$Barbaraki_TV_tm" "Minika_GO" "$Minika_GO_tm" "Minika_Cocuk" "$Minika_Cocuk_tm" "Yumurcak" "$Yumurcak_tm" "Gang_Cartoon_Channel" "$Gang_Cartoon_Channel_tm" "Aljazeera_Eng" "$Aljazeera_Eng_tm" "EuroNews_ES" "$EuroNews_ES_tm" "France24" "$France24_tm" "PressTV" "$PressTV_tm" "Russian_Today" "$Russian_Today_tm" "NASA" "$NASA_tm" "Cetelmon_TV" "$Cetelmon_TV_tm" "Ondamex" "$Ondamex_tm" "KissTV" "$KissTV_tm" "DeluxeMusic" "$DeluxeMusic_tm" "Eska" "$Eska_tm" "GoticaTV" "$GoticaTV_tm" "Humorbox" "$Humorbox_tm" "Funtv" "$Funtv_tm" "RblTV" "$RblTV_tm" "LobasTV" "$LobasTV_tm" "MusicBox" "$MusicBox_tm" "PartyTV" "$PartyTV_tm" "RMC_TV" "$RMC_TV_tm" "ShansonTV" "$ShansonTV_tm" "TV105" "$TV105_tm" "Unlove" "$Unlove_tm" "StreetclipTV" "$StreetclipTV_tm" "SoleilTV" "$SoleilTV_tm" "LaBelleTV" "$LaBelleTV_tm" "Esport3" "$Esport3_tm" "Al_Iraqiya_Sports" "$Al_Iraqiya_Sports_tm" "SkyPoker" "$SkyPoker_tm" "SportItalia" "$SportItalia_tm" "tdp" "$tdp_tm" "TileSport" "$TileSport_tm" "RedBull" "$RedBull_tm" "Abteve" "$Abteve_tm" "Andalucia" "$Andalucia_tm" "Aragon_TV" "$Aragon_TV_tm" "BarcelonaTV" "$BarcelonaTV_tm" "Canal_33" "$Canal_33_tm" "Canal_8" "$Canal_8_tm" "Canal_Extremadura" "$Canal_Extremadura_tm" "Canal9_24" "$Canal9_24_tm" "Canarias" "$Canarias_tm" "Canarias_NET" "$Canarias_NET_tm" "Lancelot" "$Lancelot_tm" "CostadelSol_TV" "$CostadelSol_TV_tm" "Cyl7" "$Cyl7_tm" "Eldia_TV" "$Eldia_TV_tm" "Etb_SAT" "$Etb_SAT_tm" "Galicia_TV_AM" "$Galicia_TV_AM_tm" "Galicia_TV_EU" "$Galicia_TV_EU_tm" "Teleminho" "$Teleminho_tm" "Hispan_TV" "$Hispan_TV_tm" "Huelva_CNH" "$Huelva_CNH_tm" "Huelva_TV" "$Huelva_TV_tm" "Huesca_TV" "$Huesca_TV_tm" "IB3" "$IB3_tm" "ImasTV" "$ImasTV_tm" "InformacionTV" "$InformacionTV_tm" "LevanteTV" "$LevanteTV_tm" "LUX_Mallorca" "$LUX_Mallorca_tm" "M95TV" "$M95TV_tm" "Onda_Azul" "$Onda_Azul_tm" "PTV_Malaga" "$PTV_Malaga_tm" "Ribera_TV" "$Ribera_TV_tm" "RtvCE" "$RtvCE_tm" "Super3" "$Super3_tm" "StvRioja" "$StvRioja_tm" "TeleB" "$TeleB_tm" "Telebahia" "$Telebahia_tm" "TeleBilbao" "$TeleBilbao_tm" "Telemadrid_SAT" "$Telemadrid_SAT_tm" "Telemadrid_Otra" "$Telemadrid_Otra_tm" "TeleToledo" "$TeleToledo_tm" "TPA_a7" "$TPA_a7_tm" "TV_Girona" "$TV_Girona_tm" "TV3" "$TV3_tm" "TV3CAT" "$TV3CAT_tm" "TV3_24" "$TV3_24_tm" "TVCS" "$TVCS_tm" "TVMelilla" "$TVMelilla_tm" "TVRioja" "$TVRioja_tm" "UnaCadiz" "$UnaCadiz_tm" "UnaCordoba" "$UnaCordoba_tm" "VoTV" "$VoTV_tm" "ZaragozaTV" "$ZaragozaTV_tm" "Esne_TV" "$Esne_TV_tm" "Astrocanalshop" "$Astrocanalshop_tm" "SolidariaTV" "$SolidariaTV_tm" "" "" "Global_TV" "$Global_TV_tm" "ATV_Sur" "$ATV_Sur_tm" "Panamericana" "$Panamericana_tm" "" "" "CubaVision" "$CubaVision_tm" "" "" "AricaTV" "$AricaTV_tm" "Canal2" "$Canal2_tm" "Canal9" "$Canal9_tm" "Digital_Channel" "$Digital_Channel_tm" "Enlace" "$Enlace_tm" "Canal33" "$Canal33_tm" "TVinet" "$TVinet_tm" "Itv" "$Itv_tm" "RedTV" "$RedTV_tm" "MegaTV" "$MegaTV_tm" "MetroTV" "$MetroTV_tm" "TVnuevotiempo" "$TVnuevotiempo_tm" "RTC" "$RTC_tm" "TVu" "$TVu_tm" "TVlota" "$TVlota_tm" "SenadoTV" "$SenadoTV_tm" "UNIACCTV" "$UNIACCTV_tm" "UATV" "$UATV_tm" "UMAGTV" "$UMAGTV_tm" "Horas24" "$Horas24_tm" "" "" "TeleSur" "$TeleSur_tm" "AtelTV" "$AtelTV_tm" "DatTV" "$DatTV_tm" "VTV" "$VTV_tm" "IslaTV" "$IslaTV_tm" "PromarTV" "$PromarTV_tm" "TamTV" "$TamTV_tm" "TVes" "$TVes_tm" "TicTV" "$TicTV_tm" "TrpTV" "$TrpTV_tm" "TVO" "$TVO_tm" "" "" "Canal10" "$Canal10_tm" "CBA24" "$CBA24_tm" "ArgentinisimaTV" "$ArgentinisimaTV_tm" "Canal3" "$Canal3_tm" "Canal7" "$Canal7_tm" "Canal9" "$Canal9_tm" "Canal_Provincial" "$Canal_Provincial_tm" "Zona31" "$Zona31_tm" "El_trece" "$El_trece_tm" "Canal21" "$Canal21_tm" "Construir_TV" "$Construir_TV_tm" "El_Rural" "$El_Rural_tm" "PakaPaka" "$PakaPaka_tm" "QMusica" "$QMusica_tm" "Canal5" "$Canal5_tm" "Canal26" "$Canal26_tm" "TN" "$TN_tm" "N9" "$N9_tm" "Canal13" "$Canal13_tm" "Canal10_Tucuman" "$Canal10_Tucuman_tm" "LapachoTV" "$LapachoTV_tm" "" "" "FacetasDeportivas" "$FacetasDeportivas_tm" "" "" "Cable_Noticias" "$Cable_Noticias_tm" "Canal_Tiempo" "$Canal_Tiempo_tm" "Tu_Kanal" "$Tu_Kanal_tm" "PyC" "$PyC_tm" "Canal_Capital" "$Canal_Capital_tm" "CMB" "$CMB_tm" "CristoVision" "$CristoVision_tm" "TeleVida" "$TeleVida_tm" "RTVC" "$RTVC_tm" "RTVC2" "$RTVC2_tm" "TeleCaribe" "$TeleCaribe_tm" "TelePacifico" "$TelePacifico_tm" "" "" "RPC" "$RPC_tm" "Paravision" "$Paravision_tm" "TeleFuturo" "$TeleFuturo_tm" "" "" "TelevisaHD" "$TelevisaHD_tm" "Milenio" "$Milenio_tm" "OnceTV" "$OnceTV_tm" "Canal66" "$Canal66_tm" "Canal44" "$Canal44_tm" "Congreso" "$Congreso_tm" "Canal_Justicia" "$Canal_Justicia_tm" "Cortes_Diputados" "$Cortes_Diputados_tm" "" "" "RTS" "$RTS_tm" "Canal1" "$Canal1_tm" "Ecuadortv" "$Ecuadortv_tm" "Oromar" "$Oromar_tm"`


elif [ $curl -eq 1  -a $KDE -eq 0 ]; then
	
	CANAL=`kdialog  --title "TVenLinux ($V_script)" --geometry 100x600 --menu "Seleccione un Canal" "rtve1" "rtve1" "rtve2" "rtve2" "rtve24" "rtve24" "Antena_3" "Antena_3" "Cuatro" "Cuatro" "Tele5" "Tele5" "La_Sexta" "La_Sexta" "Xplora" "Xplora" "Discovery_Channel" "Discovery_Channel" "Energy" "Energy" "Nitro" "Nitro" "Neox" "Neox" "Divinity" "Divinity" "SyFy" "SyFy" "Xtrm" "Xtrm" "TNT" "TNT" "FDF" "FDF" "Cosmo" "Cosmo" "13TV" "13TV" "Intereconomia" "Intereconomia" "BusinessTV" "BusinessTV" "La_Sexta_3" "La_Sexta_3" "Paramount" "Paramount" "VaughanTV" "VaughanTV" "Kanal_D" "Kanal_D" "Sat7_Kids" "Sat7_Kids" "SmileofaChildTV" "SmileofaChildTV" "Barbaraki_TV" "Barbaraki_TV" "Minika_GO" "Minika_GO" "Minika_Cocuk" "Minika_Cocuk" "Yumurcak" "Yumurcak" "Gang_Cartoon_Channel" "Gang_Cartoon_Channel" "Aljazeera_Eng" "Aljazeera_Eng" "EuroNews_ES" "EuroNews_ES" "France24" "France24" "PressTV" "PressTV" "Russian_Today" "Russian_Today" "NASA" "NASA" "Cetelmon_TV" "Cetelmon_TV" "Ondamex" "Ondamex" "KissTV" "KissTV" "DeluxeMusic" "DeluxeMusic" "Eska" "Eska" "GoticaTV" "GoticaTV" "Humorbox" "Humorbox" "Funtv" "Funtv" "RblTV" "RblTV" "LobasTV" "LobasTV" "MusicBox" "MusicBox" "PartyTV" "PartyTV" "RMC_TV" "RMC_TV" "ShansonTV" "ShansonTV" "TV105" "TV105" "Unlove" "Unlove" "StreetclipTV" "StreetclipTV" "SoleilTV" "SoleilTV" "LaBelleTV" "LaBelleTV" "Esport3" "Esport3" "Al_Iraqiya_Sports" "Al_Iraqiya_Sports" "SkyPoker" "SkyPoker" "SportItalia" "SportItalia" "tdp" "tdp" "TileSport" "TileSport" "RedBull" "RedBull" "Abteve" "Abteve" "Andalucia" "Andalucia" "Aragon_TV" "Aragon_TV" "BarcelonaTV" "BarcelonaTV" "Canal_33" "Canal_33" "Canal_8" "Canal_8" "Canal_Extremadura" "Canal_Extremadura" "Canal9_24" "Canal9_24" "Canarias" "Canarias" "Canarias_NET" "Canarias_NET" "Lancelot" "Lancelot" "CostadelSol_TV" "CostadelSol_TV" "Cyl7" "Cyl7" "Eldia_TV" "Eldia_TV" "Etb_SAT" "Etb_SAT" "Galicia_TV_AM" "Galicia_TV_AM" "Galicia_TV_EU" "Galicia_TV_EU" "Teleminho" "Teleminho" "Hispan_TV" "Hispan_TV" "Huelva_CNH" "Huelva_CNH" "Huelva_TV" "Huelva_TV" "Huesca_TV" "Huesca_TV" "IB3" "IB3" "ImasTV" "ImasTV" "InformacionTV" "InformacionTV" "LevanteTV" "LevanteTV" "LUX_Mallorca" "LUX_Mallorca" "M95TV" "M95TV" "Onda_Azul" "Onda_Azul" "PTV_Malaga" "PTV_Malaga" "Ribera_TV" "Ribera_TV" "RtvCE" "RtvCE" "Super3" "Super3" "StvRioja" "StvRioja" "TeleB" "TeleB" "Telebahia" "Telebahia" "TeleBilbao" "TeleBilbao" "Telemadrid_SAT" "Telemadrid_SAT" "Telemadrid_Otra" "Telemadrid_Otra" "TeleToledo" "TeleToledo" "TPA_a7" "TPA_a7" "TV_Girona" "TV_Girona" "TV3" "TV3" "TV3CAT" "TV3CAT" "TV3_24" "TV3_24" "TVCS" "TVCS" "TVMelilla" "TVMelilla" "TVRioja" "TVRioja" "UnaCadiz" "UnaCadiz" "UnaCordoba" "UnaCordoba" "VoTV" "VoTV" "ZaragozaTV" "ZaragozaTV" "Esne_TV" "Esne_TV" "Astrocanalshop" "Astrocanalshop" "SolidariaTV" "SolidariaTV" "" "" "Global_TV" "Global_TV" "ATV_Sur" "ATV_Sur" "Panamericana" "Panamericana" "" "" "CubaVision" "CubaVision"  "" "" "AricaTV" "AricaTV" "Canal2" "Canal2" "Canal9" "Canal9" "Digital_Channel" "Digital_Channel" "Enlace" "Enlace" "Canal33" "Canal33" "TVinet" "TVinet" "Itv" "Itv" "RedTV" "RedTV" "MegaTV" "MegaTV" "MetroTV" "MetroTV" "TVnuevotiempo" "TVnuevotiempo" "RTC" "RTC" "TVu" "TVu" "TVlota" "TVlota" "SenadoTV" "SenadoTV" "UNIACCTV" "UNIACCTV" "UATV" "UATV" "UMAGTV" "UMAGTV" "Horas24" "Horas24" "" "" "TeleSur" "TeleSur" "AtelTV" "AtelTV" "DatTV" "DatTV" "VTV" "VTV" "IslaTV" "IslaTV" "PromarTV" "PromarTV" "TamTV" "TamTV" "TVes" "TVes" "TicTV" "TicTV" "TrpTV" "TrpTV" "TVO" "TVO" "" "" "Canal10" "Canal10" "CBA24" "CBA24" "ArgentinisimaTV" "ArgentinisimaTV" "Canal3" "Canal3" "Canal7" "Canal7" "Canal9" "Canal9" "Canal_Provincial" "Canal_Provincial" "Zona31" "Zona31" "El_trece" "El_trece" "Canal21" "Canal21" "Construir_TV" "Construir_TV" "El_Rural" "El_Rural" "PakaPaka" "PakaPaka" "QMusica" "QMusica" "Canal5" "Canal5" "Canal26" "Canal26" "TN" "TN" "N9" "N9" "Canal13" "Canal13" "Canal10_Tucuman" "Canal10_Tucuman" "LapachoTV" "LapachoTV" "" "" "FacetasDeportivas" "FacetasDeportivas" "" "" "Cable_Noticias" "Cable_Noticias" "Canal_Tiempo" "Canal_Tiempo" "Tu_Kanal" "Tu_Kanal" "PyC" "PyC" "Canal_Capital" "Canal_Capital" "CMB" "CMB" "CristoVision" "CristoVision" "TeleVida" "TeleVida" "RTVC" "RTVC" "RTVC2" "RTVC2" "TeleCaribe" "TeleCaribe" "TelePacifico" "TelePacifico" "" "" "RPC" "RPC" "Paravision" "Paravision" "TeleFuturo" "TeleFuturo" "" "" "TelevisaHD" "TelevisaHD" "Milenio" "Milenio" "OnceTV" "OnceTV" "Canal66" "Canal66" "Canal44" "Canal44" "Congreso" "Congreso" "Canal_Justicia" "Canal_Justicia" "Cortes_Diputados" "Cortes_Diputados" "" "" "RTS" "RTS" "Canal1" "Canal1" "Ecuadortv" "Ecuadortv" "Oromar" "Oromar"`


fi

if [ $fifo -eq 0 -o $fifo -eq 2 ]; then # Se crea la fifo y forzamos usar mplayer sin opciones con la pila
	mkfifo /tmp/$CANAL."$ID"
	SAVE=0
	
	if [ "$REPRODUCTOR" = "mplayer" -o  "$REPRODUCTOR" = "vlc" ]; then # Fuerza el uso de Mplayer si usa vlc y da libertad a usar ffplay
		REPRODUCTOR="mplayer_fifo"
	fi
fi

case $CANAL in

	rtve1) rtmpdump -m 200 -r "rtmp://cp68975.live.edgefcs.net:1935/live" -y "LA1_AKA_WEB_NOG@58877" -W "http://www.rtve.es/swf/4.1.11/RTVEPlayerVideo.swf" -p "http://www.rtve.es/noticias/directo-la-1" -t "rtmp://cp68975.live.edgefcs.net:1935/live" -v -q > /tmp/$CANAL."$ID" & ;;

	rtve2) rtmpdump -m 200 -r "rtmp://cp68975.live.edgefcs.net:1935/live" -y "LA2_AKA_WEB_NOG@60554" -W "http://www.rtve.es/swf/4.1.11/RTVEPlayerVideo.swf" -p "http://www.rtve.es/television/la-2-directo" -t "rtmp://cp68975.live.edgefcs.net:1935/live" -q -v > /tmp/$CANAL."$ID" & ;;

	rtve24) rtmpdump -r "rtmp://rtvefs.fplive.net:1935/rtve-live-live?ovpfv=2.1.2/RTVE_24H_LV3_WEB_NOG" -W "http://www.rtve.es/swf/4.1.18/RTVEPlayerVideo.swf" -q -v > /tmp/$CANAL."$ID" & ;;

	tdp) rtmpdump -m 200 -r "rtmp://cp48772.live.edgefcs.net:1935/live" -y "TDP_AKA_WEB_GEO@58884" -W "http://www.rtve.es/swf/4.0.37/RTVEPlayerVideo.swf" -p "http://www.rtve.es/deportes/directo/teledeporte" -q -v > /tmp/$CANAL."$ID" & ;;

	Antena_3) rtmpdump -m 200 -r "rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live" -y "stream-antena3" -W "http://www.antena3.com/static/swf/A3Player.swf?nocache=200" -p "http://www.antena3.com/directo/" -q -v > /tmp/$CANAL."$ID" & ;;

	La_Sexta) rtmpdump -m 200 -r "rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-lasexta" -W "http://www.antena3.com/static/swf/A3Player.swf" -p "http://www.lasexta.com/directo" -q -v > /tmp/$CANAL."$ID" & ;;

	Cuatro) rtmpdump -m 200 -r "rtmp://174.37.222.57/live" -y "cuatrolacajatv?id=14756" -W "http://www.ucaster.eu/static/scripts/eplayer.swf" -p "http://www.ucaster.eu/embedded/cuatrolacajatv/1/670/400" -q -v > /tmp/$CANAL."$ID" & ;;

	Tele5) rtmpdump -m 200 -r "rtmp://68.68.31.229/live" -y "t5hdlacajatv2" -W "http://www.udemy.com/static/flash/player5.9.swf" -p "http://www.castamp.com/embed.php?c=t5hdlacajatv2&vwidth=670&vheight=400" -q > /tmp/$CANAL."$ID" & ;;


	Xplora) rtmpdump -m 200 -r "rtmp://antena3fms35geobloqueolivefs.fplive.net:1935/antena3fms35geobloqueolive-live/stream-xplora" -W "http://www.antena3.com/static/swf/A3Player.swf" -p "http://www.lasexta.com/xplora/directo" -q -v > /tmp/$CANAL."$ID" & ;;

	Nitro) rtmpdump -m 200 -a "live" -r "rtmp://173.193.205.81/live" -y "nitrolacajatv?id=126587" -W "http://mips.tv/content/scripts/eplayer.swf" -p "http://mips.tv/embedplayer/nitrolacajatv/1/670/400"  -q -v > /tmp/$CANAL."$ID" & ;;

	Neox) rtmpdump -m 200 -r "rtmp://live.zcast.us:1935/liveorigin/_definst_" -y "neoxlacaja-lI7mjw6RDa" -W "http://player.zcast.us/player58.swf" -p "http://zcast.us/gen.php?ch=neoxlacaja-lI7mjw6RDa&width=670&height=400" -q -v > /tmp/$CANAL."$ID" & ;;

	La_Sexta_3) rtmpdump -m 200 -r "rtmp://174.36.251.140/live/lasexta3lacaja?id=15912" -W "http://www.ucaster.eu/static/scripts/eplayer.swf" -p "http:schuster92.com" -q > /tmp/$CANAL."$ID" & ;;
	Paramount) rtmpdump -m 200 -r "rtmp://173.193.46.109/live" -y "179582" -W "http://static.castalba.tv/player.swf" -p "http://castalba.tv/embed.php?cid=9947&wh=680&ht=400&r=lacajatv.es" -q -v > /tmp/$CANAL."$ID" & ;;

	Intereconomia) rtmpdump -m 200 -r "rtmp://media.intereconomia.com/live/intereconomiatv1" -q -v > /tmp/$CANAL."$ID" & ;;

	BusinessTV) rtmpdump -m 200 -r "rtmp://media.intereconomia.com/live" -y "business1" -W "ttp://www.intereconomia.com/flowplayer-3.2.5.swf?0.19446.067378316934" -p "http://www.intereconomia.com/ver-intereconomia-business-tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	13TV) rtmpdump -m 200 -r "rtmp://xiiitvlivefs.fplive.net/xiiitvlive-live" -y "stream13tv" -W "http://static.hollybyte.com/public/players/flowplayer/swf/flowplayer.commercial.swf" -p "http://live.13tv.hollybyte.tv/embed/4f33a91894a05f5f49020000" -q -v > /tmp/$CANAL."$ID" & ;;

	Energy) rtmpdump -m 200 -r "rtmp://50.7.28.130/live" -y "lacajatvenergy" -W "http://www.udemy.com/static/flash/player5.9.swf" -p "http://www.castamp.com/embed.php?c=lacajatvenergy&vwidth=670&vheight=400" -q -v > /tmp/$CANAL."$ID" & ;;

	FDF) rtmpdump -m 200 -a "live" -r "rtmp://46.23.67.114/live" -y "fffdf?id=29750" -W "http://www.ucaster.eu/static/scripts/eplayer.swf" -p "http://www.ucaster.eu/embedded/fffdf/1/650/400"  -q -v > /tmp/$CANAL."$ID" & ;;

	Aragon_TV) rtmpdump -m 200 -r "rtmp://aragontvlivefs.fplive.net/aragontvlive-live" -y "stream_normal_abt" -W "http://alacarta.aragontelevision.es/streaming/flowplayer.commercial-3.2.7.swf" -p "http://alacarta.aragontelevision.es/streaming/streaming.html" -q -v > /tmp/$CANAL."$ID" & ;;

	Huesca_TV) rtmpdump -m 200 -r "rtmp://streaming2.radiohuesca.com/live/" -W "http://player.longtailvideo.com/player5.3.swf" -y "huescatv" -p "http://www.intertelevision.com/spain/localiatv.php" -v > /tmp/$CANAL."$ID" & ;;

	Galicia_TV_EU) rtmpdump -m 200 -r "rtmp://media3.crtvg.es:80/live" -y "tvge_2" -W "http://www.crtvg.es/flowplayer3/flowplayer.commercial-3.2.7.swf" -p "http://www.crtvg.es/tvg/tvg-en-directo" -q -v > /tmp/$CANAL."$ID" & ;;

	Galicia_TV_AM) rtmpdump -m 200 -r "rtmp://media3.crtvg.es:80/live" -y "tvga_2" -W "http://www.crtvg.es/flowplayer3/flowplayer.commercial-3.2.7.swf" -p "http://www.crtvg.es/tvg/tvg-en-directo/canle/galicia-tv-america" -q -v > /tmp/$CANAL."$ID"  & ;;

	Teleminho) rtmpdump -m 200 -a "teleminho" -r "rtmp://fcs.grupo5.com/teleminho/" -y "telemiño" -W "http://www.grupo5.com/fcs/teleminho/teleminho.swf" -p "http://www.teleminho.com/" -q -v > /tmp/$CANAL."$ID"  & ;;

	Canarias) rtmpdump -m 200 -r "rtmp://streamrtvc.mad.idec.net/rtvc1" -y "rtvc_1.sdp" -W "http://www.rtvc.es/swf/flowplayer.commercial-3.1.5.swf" -p "http://www.rtvc.es/television/enDirecto.aspx?canal=tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Canarias_NET) rtmpdump -m 200 -r "rtmp://streamrtvc.mad.idec.net:1935/rtvcnet/" -y "rtvc_net.sdp" -W "http://www.rtvc.es/swf/flowplayer.commercial-3.1.5.swf" -p "http://www.rtvc.es/television/enDirecto.aspx?canal=tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Lancelot) rtmpdump -m 200 -a "directo" -r "rtmp://5.135.177.210/directo" -y "lancelot" -W "http://www.lancelot.tv/directo/player.swf" -p "http://www.lancelot.tv/directo/" -q -v > /tmp/$CANAL."$ID" & ;;

	Eldia_TV) rtmpdump -m 200 -r "rtmp://teledifusion.tv/dia" -y "dia" -W "http://www.eldia.tv/player.swf" -p "http://www.eldia.tv/" -q -v > /tmp/$CANAL."$ID" & ;;

	TVRioja) rtmpdump -m 200 -r "rtmp://teledifusion.tv/rioja" -y "rioja" -W "http://www.tvr.es/html5/player.swf" -p "http://www.tvr.es/directo.php" -q -v > /tmp/$CANAL."$ID" & ;;

	StvRioja) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://www.riojasintonia.com/stv > /dev/null 2>&1 & mplayer_conf_change ;;

	TPA_a7) rtmpdump -m 200 -r "rtmp://teledifusion.tv:1935/asturiastv" -y "asturiastvlive" -W "http://www.rtpa.es/jwplayer/player.swf" -p "http://www.rtpa.es/television" -q -v > /tmp/$CANAL."$ID" & ;;

	Andalucia)  mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" http://195.10.10.220/rtva/andaluciatelevisionh264.flv > /dev/null 2>&1 & mplayer_conf_change ;;

	Huelva_TV) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/huelvatv" -W "http://www.huelvatv.com/plugins/content/jw_allvideos/includes/js/mediaplayer/player.swf" -y "livestream" -p "http://huelvatv.com/index.php/en-directo" -q -v > /tmp/$CANAL."$ID" & ;;

	Abteve) rtmpdump -m 200 -r "rtmp://live.cycnet.eu/flvplayback" -y "ts_2_68_69" -W "http://www.abteve.com/live/flowplayer/flowplayer-3.2.11.swf" -p "http://www.abteve.com/abteve-on-line.htm" -q -v > /tmp/$CANAL."$ID" & ;;

	BarcelonaTV)  mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" http://195.10.10.207/barcelonatv/barcelonatv-high.flv  > /dev/null 2>&1 & mplayer_conf_change ;;
	
	IB3) rtmpdump -m 200 -r "rtmp://ib3tvlivefs.fplive.net/ib3tvlive-live" -y "streamib3" -W "http://ib3cdn.s3.amazonaws.com/player/player.swf" -p "http://ib3tv.com/ib3/player/ib3sat.php" -q -v > /tmp/$CANAL."$ID"  & ;;

	Canal9_24)  mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" http://195.10.10.213/rtvv/canal9.flv > /dev/null 2>&1 & mplayer_conf_change ;; 

	Onda_Azul) rtmpdump -m 200 -r "rtmp://ondaazullivefs.fplive.net:1935/ondaazullive-live/" -y "ondaazullive-stream1" -W "http://www.freeetv.com/script/mediaplayer/player.swf" -p "http://www.waaatch.com/modules.php?name=Video_Stream&page=watch&id=4690" -q -v > /tmp/$CANAL."$ID" & ;;

	TV3CAT) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_TV3CAT_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/directes/" -q -v > /tmp/$CANAL."$ID" & ;;

	TV3) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_TV3_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/directes/" -q -v > /tmp/$CANAL."$ID" & ;;

	TV3_24) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_324_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/directes/" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal_33) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_33D_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/directes/" -q -v > /tmp/$CANAL."$ID" & ;;

	Esport3) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_ES3_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/directes/" -q -v > /tmp/$CANAL."$ID" & ;;

	Super3) rtmpdump -m 200 -r "rtmp://tv-nogeo-flashlivefs.fplive.net/tv-nogeo-flashlive-live" -y "stream_33D_FLV" -W "http://www.tv3.cat/ria/players/3ac/evp/Main.swf" -p "http://www.tv3.cat/3alacarta/#/directes/SUPER3" -q -v > /tmp/$CANAL."$ID" & ;;

	TeleB) rtmpdump -m 200 -r "rtmp://directe.tvbadalona.cat/live" -y "myStream.sdp" -W "http://www.teleb.cat/directe/flowplayer-3.2.5.swf" -p "http://www.teleb.cat/directe/" -q -v > /tmp/$CANAL."$ID" & ;;

	TV_Girona) rtmpdump -m 200 -r "rtmp://81.95.0.67:19935/tvgirona" -y "directe" -W "http://www.ixac.tv/rtmp/flowplayer.commercial-3.2.5.swf" -p "http://www.ixac.tv/rtmp/tvgirona_Vidal_player_independent_E.html" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal_8) rtmpdump -m 200 -r "rtmp://94.23.54.177/8TV" -y "8aldia-directe" -W "http://css01.mundodeportivo.com/imagenes/players/player.swf" -p "http://narrowcast.lavanguardia.com" -q -v > /tmp/$CANAL."$ID" & ;;

	VoTV) rtmpdump -m 200 -r "rtmp://xiptv-streaming.gnuine.com/ocasional5" -y "directe" -W "http://votv.xiptv.cat/flash/flowplayer.commercial-3.2.11.swf" -p "http://votv.xiptv.cat" -q -v > /tmp/$CANAL."$ID" & ;;

	TVCS) rtmpdump -m 200 -r "rtmp://188.165.230.206/directo" -y "livestream" -W "http://www.tvcs.tv/skins2.3.5/awes/player.swf" -p "http://www.tvcs.tv/endirecto/" -q -v > /tmp/$CANAL."$ID" & ;;

	Ribera_TV) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/ribera" -y "livestream" -W "http://www.todostreaming.es/player_new.swf" -p "http://www.riberatelevisio.com" -q -v > /tmp/$CANAL."$ID" & ;;

	Telemadrid_SAT) rtmpdump -m 200 -r "rtmp://cp118140.live.edgefcs.net:1935/live" -y "TSAtelemadridsat@47720" -q -v > /tmp/$CANAL."$ID" & ;;

	Telemadrid_Otra) rtmpdump -m 200 -r "rtmp://cp96225.live.edgefcs.net:1935/live?videoId=292161053001&lineUpId=&pubId=104403117001&playerId=111868723001&.affiliateId=" -W "http://admin.brightcove.com/viewer/us20130118.1025/federatedVideoUI/BrightcovePlayer.swf" -y "Laotra@30799" -p "http://www.telemadrid.es/?q=emision_en_directo_laotra" -q -v > /tmp/$CANAL."$ID" & ;;

	Cyl7) rtmpdump -m 200 -r "rtmp://live2.nice264.com:1935/niceStreamingServer/_definst_/cyl_cyltv_live|rtmp://live1.nice264.com:1935/niceStreamingServer/_definst_/cyl_cyltv_live" -a "niceLiveServer"  -W "http://mgmt.nice264.com/swf/jwplayer.swf" -p "http://www.rtvcyl.es/Directo.aspx" -q -v > /tmp/$CANAL."$ID" & ;;

	Etb_SAT) rtmpdump -m 200 -r "rtmp://cp70268.live.edgefcs.net/live" -y "eitb-ETBSat@5219" -W "http://www.eitb.com/resources/flash/video_playerberria3.swf" -p "http://www.eitb.com/es/television/etb-sat/" -q -v > /tmp/$CANAL."$ID" & ;;

	TeleBilbao) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "telebilbao.stream" -W "http://www.lasteles.com/js/mediaplayer-5.8/player.swf" -p "http://www.lasteles.com/es/player.php?auto=0&id=14884" -q -v > /tmp/$CANAL."$ID" & ;;

	Divinity) rtmpdump -m 200 -r "rtmp://68.68.17.102/live" -y "discomaxlacajatv" -W "http://www.udemy.com/static/flash/player5.9.swf" -p "http://www.castamp.com/embed.php?c=discomaxlacajatv&tk=5mD8Tatf&vwidth=650&vheight=400" -q -v > /tmp/$CANAL."$ID" & ;;

	Discovery_Channel) rtmpdump -m 200 -r "rtmp://184.173.181.44/live" -y "discoverylacajatv?id=14680" -W "http://www.ucaster.eu/static/scripts/eplayer.swf" -p "http://www.ucaster.eu/embedded/discoverylacajatv/1/650/400" -q > /tmp/$CANAL."$ID" & ;;

	TNT) rtmpdump -r "rtmp://212.7.206.71/live" -y "tntnnn?id=29722" -W "http://www.ucaster.eu/static/scripts/eplayer.swf" -p "http://www.ucaster.eu/embedded/tntnnn/1/650/400" -q -v > /tmp/$CANAL."$ID" & ;;

	Xtrm) rtmpdump -m 200 -r "rtmp://93.174.93.58/freelivestreamHD" -y "xtrmlacajatv" -W "http://freelivestream.tv/swfs/player.swf" -p "http://freelivestream.tv/embedPlayer.php?file=xtrmlacajatv&width=670&height=400&ckattempt=1" -q -v > /tmp/$CANAL."$ID" & ;;

	SyFy) rtmpdump -m 200 -r "rtmp://romania.zcast.us/liveedge" -y "syfy-p2X1XuGkY" -W "http://player.zcast.us/player58.swf" -p "http://zcast.us" -q -v > /tmp/$CANAL."$ID" & ;;

	Cosmo) rtmpdump -m 200  -r "rtmp://93.174.93.58/freelivestreamHD" -y "cosmolacajatv" -W "http://freelivestream.tv/swfs/player.swf" -p "http://freelivestream.tv/embedPlayer.php"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal_Extremadura) rtmpdump -m 200 -r "rtmp://canalextremaduralive.cdn.canalextremadura.es/canalextremaduralive-live/" -y "stream001" -W "http://www.canalextremadura.es/sites/all/modules/custom/slx_reproductor/js/mediaplayer-5.7/player.swf" -p "http://www.canalextremadura.es/alacarta/tv/directo" -q -v > /tmp/$CANAL."$ID" & ;;

	KissTV) rtmpdump -m 200 -r "rtmp://kisstelevision.es.flash3.glb.ipercast.net/kisstelevision.es-live" -y "live" -W "http://kisstelevision.en-directo.com/kisstelevision_avw.swf" -p "http://www.kisstelevision.es" -q -v > /tmp/$CANAL."$ID" & ;;

	UnaCadiz) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/unatv" -y "live" -W "http://www.todostreaming.es/player_new.swf" -p "http://www.unacadiz.tv/directo/" -q -v > /tmp/$CANAL."$ID" & ;;

	UnaCordoba) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "unacordoba.stream" -W "http://www.lasteles.com/js/mediaplayer-5.8/player.swf" -q -v > /tmp/$CANAL."$ID" & ;;

	LUX_Mallorca) rtmpdump -m 200 -r "rtmp://fl1.viastreaming.net/canal37" -W "http://fl1.viastreaming.net:8000/player/player.swf" -y "livestream" -p "http://luxmallorca.tv/" -q -v > /tmp/$CANAL."$ID" & ;;

	RtvCE) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/rtvceuta" -y "livestream" -W "http://www.todostreaming.es/player.swf" -p "http://www.rtvce.es/" -q -v > /tmp/$CANAL."$ID" & ;;

	TVMelilla) rtmpdump -m 200 -r "rtmp://stream.tvmelilla.es:1935/tvmelilla" -y "live" -W "http://www.tvmelilla.es/jwplayer/player.swf" -p "http://www.tvmelilla.es/directo.html" -q -v > /tmp/$CANAL."$ID" & ;;

	EuroNews_ES) rtmpdump -m 200 -r "rtmp://fr-par-1.stream-relay.hexaglobe.net:1935/rtpeuronewslive" -y "es_video350_flash_all.sdp" -W "http://es.euronews.com/media/player_live_1_14.swf" -p "http://es.euronews.com/noticias/en-directo/" -q -v > /tmp/$CANAL."$ID" & ;;
	
	France24) rtmpdump -m 200 -r "rtmp://vipwowza.yacast.net/france24_live_en" -y "f24_liveen.stream" -W "http://www.france24.com/en/sites/all/modules/maison/aef_player/flash/player_new.swf" -p "http://www.france24.com" -q -v > /tmp/$CANAL."$ID"  & ;;

	PressTV) rtmpdump -m 200 -r "rtmp://cp140005.live.edgefcs.net:80/live" -y "PressTV_RTMP_4@87306" -p "http://www.presstv.ir" -q -v > /tmp/$CANAL."$ID" & ;;

	VaughanTV) rtmpdump -m 200 -a "vaughantvlive-live/" -r "rtmp://vaughantvlivefs.fplive.net/vaughantvlive-live/" -y "vaughantv_1" -W "http://vaughantv.cdn.customers.overon.es/player/player.swf" -p "http://www.vaughanradio.com" -q -v > /tmp/$CANAL."$ID" & ;;

	Russian_Today) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "russiantoday.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	TeleSur) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "telesur.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	AtelTV) rtmpdump -m 200 -r "rtmp://edge.wms28.lorini.net/ateltv/" -y "ateltv" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.lorini.net" -q -v > /tmp/$CANAL."$ID" & ;;

	DatTV) rtmpdump -m 200 -a "ustream2live-live/" -r "rtmp://ustreamlivefs.fplive.net:1935/ustream2live-live/" -y "stream_live_1_1_4172359" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.ustream.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	VTV) rtmpdump -m 200 -a "vtvdsl" -r "rtmp://edg.ord.movipbox2.streamguys.net/vtvdsl" -y "vtvdsl.sdp" -W "http://www.vtv.gob.ve/player.swf" -p "http://www.vtv.gob.ve"  -q -v > /tmp/$CANAL."$ID" & ;;

	IslaTV) rtmpdump -m 200 -r "rtmp://edge.wms28.lorini.net/islatv/" -y "islatv" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.islatv.com.ve" -q -v > /tmp/$CANAL."$ID" & ;;

	PromarTV) rtmpdump -m 200 -r "rtmp://edge.wms28.lorini.net/promartv/" -y "promartv" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.lorini.net"  -q -v > /tmp/$CANAL."$ID" & ;;

	Telebahia) rtmpdump -m 200 -r "rtmp://62.42.17.93:1935/live" -y "Live" -W "http://www.telebahia.tv/player/player.swf" -q -v > /tmp/$CANAL."$ID" & ;;

	ImasTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "imastv.stream" -q -v > /tmp/$CANAL."$ID" & ;; 
	
	ZaragozaTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "ztv.stream" -q -v > /tmp/$CANAL."$ID" & ;;
	
	TeleToledo) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "teletoledo.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	Huelva_CNH) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "cnh.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	LevanteTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "levantetv.stream" -q -v > /tmp/$CANAL."$ID" & ;;	

	InformacionTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "informaciontv.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	PTV_Malaga) rtmpdump -m 200 -r "rtmp://149.11.34.6/rtplive" -y "ptvmalaga.stream" -q -v > /tmp/$CANAL."$ID" & ;;
	
	CostadelSol_TV) rtmpdump -m 200 -r "rtmp://fl0.c80177.cdn.qbrick.com:1935/80177/_definst_" -y "20242994"  -p "http://www.costadelsoltv.com" -q -v > /tmp/$CANAL."$ID"  & ;;

	M95TV) rtmpdump -m 200 -r "rtmp://movipbox.streamguys.net:1935/m95tv/" -y "m95tv.sdp" -W "http://www.m95tv.es/modules/mod_playerjr/player-licensed5.swf" -p "http://www.m95tv.es" -q -v > /tmp/$CANAL."$ID" & ;;

	Humorbox) rtmpdump -m 200 -r "rtmp://musicbox.cdnvideo.ru/musicbox-live" -y "humorbox.sdp" -W "http://www.musicboxtv.ru/_front/flowplayer-3.2.7.swf" -p "http://www.musicboxtv.ru" -q -v > /tmp/$CANAL."$ID" & ;;
	
	MusicBox) rtmpdump -m 200 -r "rtmp://musicbox.cdnvideo.ru/musicbox-live" -y "musicbox.sdp" -W "http://www.musicboxtv.ru/_front/flowplayer-3.2.7.swf" -p "http://www.musicboxtv.ru" -q -v > /tmp/$CANAL."$ID" & ;;

	ShansonTV) rtmpdump -m 200 -r "rtmp://chanson.cdnvideo.ru/chanson-live/" -y "shansontv.sdp" -W "http://www.shanson.tv/jw/jwplayer.flash.swf" -p "http://www.shanson.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	DeluxeMusic) rtmpdump -m 200 -r "rtmp://flash.cdn.deluxemusic.tv/deluxemusic.tv-live/" -y "web_850.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	GoticaTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "gotica.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	LobasTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "lobas.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	PartyTV) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "partytv.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	Unlove) rtmpdump -m 200 -r "rtmp://149.11.34.6/live" -y "unlovechannel.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	Eska) rtmpdump -m 200 -r "rtmp://46.105.112.212:1935/live" -y "mpegts.stream" -q -v > /tmp/$CANAL."$ID" & ;;

	TV105) rtmpdump -m 200 -r "rtmp://fms.105.net:1935/live" -y "105Test1" -W "http://www.105.net/com/universalmind/swf/video_player_102.swf?xmlPath=/com/universalmind/tv/105/videoXML.xml&advXML=/com/universalmind/adsWizzConfig/0.xml" -p "http://www.105.net" -q -v > /tmp/$CANAL."$ID" & ;;

	RMC_TV) rtmpdump -m 200 -r "rtmp://fms.105.net:1935/live" -y "rmc1" -W "http://video.radiomontecarlo.net/com/universalmind/swf/videoPlayerAdsWizz01.swf?xmlPath=/com/universalmind/tv/rmc/videoXML.xml&advXML=/com/universalmind/adsWizzConfig/1.xml" -p "http://video.radiomontecarlo.net" -q -v > /tmp/$CANAL."$ID" & ;;

	LaBelleTV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://www.labelletv.net/labelleTV  > /dev/null 2>&1 & mplayer_conf_change ;;
	
	SoleilTV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://live240.impek.com/soleiltv  > /dev/null 2>&1 & mplayer_conf_change ;;

	Funtv) rtmpdump -m 200 -r "rtmp://creyden.popler.tv:80/publishlive?play=123452" -y "4funtv" -W "http://www.popler.tv/player/flowplayer.commercial.swf" -p "http://www.4fun.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	RblTV) rtmpdump -m 200 -r "rtmp://poviss.popler.tv:1935/publishlive?play=123452" -y "rebeltv" -W "http://www.popler.tv/player/flowplayer.commercial.swf" -p "http://www.rbl.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	StreetclipTV) rtmpdump -m 200 -r "rtmp://stream.streetclip.tv:1935/live" -y "low-stream" -W "http://www.streetclip.tv/fileadmin/Templates/Streetclip20.11/libs/flowplayer/flowplayer.commercial-3.2.10.swf" -p "http://www.streetclip.tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	Hispan_TV) rtmpdump -m 200 -r "rtmp://mtv.fms-01.visionip.tv/live" -y "mtv-m_tv-live-25f-4x3-SDh" -W "http://embeddedplayer.visionip.tv/data/swf/8f44869de82046.059e9bf6e623ee1d54965/player.swf" -p "http://www.hispantv.com" -q -v > /tmp/$CANAL."$ID" & ;;

	Aljazeera_Eng) rtmpdump -m 200 -r "rtmp://aljazeeraflashlivefs.fplive.net:1935/aljazeeraflashlive-live" -y "aljazeera_eng_high" -W "http://admin.brightcove.com/viewer/us20121113.1511/federatedVideoUI/BrightcovePlayer.swf" -p "http://www.aljazeera.com/watch_now/" -q -v > /tmp/$CANAL."$ID" & ;;

	NASA) rtmpdump -a "ustreamCdn/flash94/6540154" -r "rtmp://flash59.gblx.tcdn.ustream.tv:1935/ustreamCdn/flash94/6540154" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:360.swf" -p "http://www.ustream.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Esne_TV) rtmpdump -m 200 -r "rtmp://69.60.121.166/live" -y "esne2" -W "http://elsembradorministries.com/esne/ESNE-TV/files/player.swf" -p "http://elsembradorministries.com/esne/ESNE-TV/esnetvenvivo.html" -q -v > /tmp/$CANAL."$ID" & ;;

	Astrocanalshop) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/telelinea1" -W "http://www.todostreaming.es/player_new.swf" -y "mystream" -p "http://www.astrocanalshop.com/streaming.htm" -q -v > /tmp/$CANAL."$ID" & ;;

	Ondamex) rtmpdump -m 200 -r "rtmp://stream.visualnetworks.es:1935/str063" -y "live" -W "http://ondamex.com/ondamex.swf" -p "http://ondamex.com" -q -v > /tmp/$CANAL."$ID" & ;;

	CubaVision) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID"  mms://cubavision.cubasi.cu/Tvcubana > /dev/null 2>&1 & mplayer_conf_change ;;

	Panamericana) rtmpdump -m 200 -r "rtmp://demo5.iblups.com/demo" -y "nm5esQgmkT"  -W "http://iblups.com/playertvlive123456789panamericanatv.swf" -p "http://iblups.com/e_panamericanatv-490-320" -q -v > /tmp/$CANAL."$ID" & ;;

	Global_TV) rtmpdump -m 200 -r "rtmp://demo13.iblups.com/demo" -y "hTWNttHSsq" -W "http://iblups.com/playertvlive123456789globaltv.swf" -p "http://iblups.com/e_globaltv-490-33" -q -v > /tmp/$CANAL."$ID" & ;;

	ATV_Sur) rtmpdump -m 200 -r "rtmp://demo.iblups.com/demo" -y "yVUQhp8tNL" -W "http://iblups.com/playertvlive123456789.swf" -p "http://iblups.com/e_atvsur-400-330" -q -v > /tmp/$CANAL."$ID" & ;;

	AricaTV) rtmpdump -m 200 -a "aricatv/aricatvvivo" -r "rtmp://stream210.digitalproserver.com:443/aricatv/aricatvvivo" -y "livestream" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.aricatv.com/" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal2) rtmpdump -r "rtmp://v1.streamcontrolpanel.com:1935/canal2" -y "canal2" -W "http://player.pepago.com/detectorvd/StrobeMediaPlayback.swf" -p "http://player.pepago.com" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal9) rtmpdump -m 200 -r "rtmp://stream210.digitalproserver.com:1935/c9/c9vivo/livestream1" -y "livestream1" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.biobiotv.cl" -q -v > /tmp/$CANAL."$ID" & ;;

	Digital_Channel) rtmpdump -m 200 -r "rtmp://stream210.digitalproserver.com:443/dch/dchvivo" -y "livestream" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.dch.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Enlace) rtmpdump -m 200 -r "rtmp://cdne.unored.com/enlace" -y "str.sdp" -W "http://tvportal2.unored.com/enlace/player5/player.swf" -p "http://tvportal2.unored.com"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal33) rtmpdump -m 200 -r "rtmp://crearchile.com/live" -y "mp4:canal33.mp4" -W "http://crearchile.com/player/player.swf" -p "http://www.canal33.cl/senal.php" -q -v > /tmp/$CANAL."$ID" & ;;

	TVinet) rtmpdump -m 200 -r "rtmp://tv01.pueblohost.com/tvinet" -y "tvinet" -W "http://tv01.pueblohost.com/system/misc/jwplayer/player.swf" -p "http://www.tvinet.cl/emergente.php" -q -v > /tmp/$CANAL."$ID" & ;;

	Itv) rtmpdump -m 200 -r "rtmp://184.82.37.10:1935/live" -y "itvp" -W "http://fpdownload.adobe.com/strobe/FlashMediaPlayback.swf" -p "http://www.itvpatagonia.cl/online.html" -q -v > /tmp/$CANAL."$ID" & ;;

	RedTV) rtmpdump -m 200 -a "redtv/redtvvivo" -r "rtmp://66.231.177.36/redtv/redtvvivo" -y "livestream1" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.lared.cl/online/" -q -v > /tmp/$CANAL."$ID" & ;;

	MegaTV) rtmpdump -m 200 -r "rtmp://mega.lb.ztreaming.com:80/mega/" -y "megaJaeRa1xing.sdp" -W "http://www.mega.cl/website/js/flowplayer/3.2.2/swf/rtmp.swf" -p "http://www.mega.cl/senal-en-vivo/" -q -v > /tmp/$CANAL."$ID" & ;;

	MetroTV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" http://190.196.9.186:8080/subtv > /dev/null 2>&1 & mplayer_conf_change ;;

	TVnuevotiempo) rtmpdump -m 200 -r "rtmp://play2go.tv:1935/live" -y "TVnuevotiempo" -W "http://play2go.tv/flowplayer/flowplayer.commercial-3.2.14.swf" -p "http://play2go.tv/live/flowplayer.html?stream=TVnuevotiempo" -q -v > /tmp/$CANAL."$ID" & ;;

	RTC) rtmpdump -m 200 -a "ustreamVideo/12775842" -r "rtmp://flash79.ustream.tv:1935/ustreamVideo/12775842" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://cormudesi.cl/RTC_TV.html" -q -v > /tmp/$CANAL."$ID" & ;;
	
	TVu) rtmpdump -m 200 -a "tvu/tvuvivo" -r "rtmp://190.196.10.194/tvu/tvuvivo" -y "livestream1" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.tvu.cl/images/stories/online.php"  -q -v > /tmp/$CANAL."$ID" & ;;

	TVlota) rtmpdump -m 200 -a "tvlota/tvlotavivo" -r "rtmp://stream210.digitalproserver.com:443/tvlota/tvlotavivo" -y "livestream" -W "http://media.digitalproserver.com/dps_player.swf" -p "http://www.tvlota.cl/index.php?option=com_content&view=article&id=2&Itemid=6"  -q -v > /tmp/$CANAL."$ID" & ;;

	SenadoTV) rtmpdump -m 200  -r "rtmp://senadortmpr.janus.cl:80/senadotv" -y "senado600" -W "http://www.senado.cl/prontus_senado/js-local/jwplayer/player.swf" -p "http://www.senado.cl/prontus_senado/site/edic/base/port/tv_senado.html"  -q -v > /tmp/$CANAL."$ID" & ;;

	UNIACCTV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://media.uniacc.cl/canal34tv > /dev/null 2>&1 & mplayer_conf_change ;;

	UATV) rtmpdump -m 200  -a "live/uautonoma" -r "rtmp://190.196.29.26:1935/live/uautonoma" -y "uautonoma" -W "http://www.eltelontv.com/clientes/uautonoma/bolt.swf" -p "http://www.eltelontv.com/clientes/uautonoma/"  -q -v > /tmp/$CANAL."$ID" & ;;

	UMAGTV) rtmpdump -m 200  -a "grupozlive-live/" -r "rtmp://grupozlivefs.fplive.net/grupozlive-live/" -y "streamumagtv" -W "http://umagtv.ztreaming.cl/swf/player.swf" -p "http://umagtv.ztreaming.cl/"  -q -v > /tmp/$CANAL."$ID" & ;;

	Horas24) rtmpdump -m 200 -a "envivo_edge/" -r "rtmp://wow1.tvn.cl/envivo_edge/" -y "imagen3" -W "http://www.24horas.cl/skins/24horas/swf/flowplayer.cluster-3.2.3.swf" -p "http://www.24horas.cl/envivo/"  -q -v > /tmp/$CANAL."$ID" & ;;

	TamTV) rtmpdump -m 200  -a "tamtv/" -r "rtmp://edge.wms28.lorini.net/tamtv/" -y "tamtv" -W "http://tamtv.com.ve/tv/player.swf" -p "http://tamtv.com.ve"  -q -v > /tmp/$CANAL."$ID" & ;;

	TVes) rtmpdump -m 200  -a "tves" -r "rtmp://movipbox.streamguys.net:1935/tves" -y "tves.sdp" -W "http://flash.telepuertovirtual.tv/tves-flash/player.swf" -p "http://www.tves.gob.ve" -q -v > /tmp/$CANAL."$ID" & ;;

	TicTV) rtmpdump -m 200  -a "tictv/" -r "rtmp://edge.wms28.lorini.net/tictv/" -y "tictv" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.tictv.com.ve" -q -v > /tmp/$CANAL."$ID" & ;;

	TrpTV) rtmpdump -m 200  -a "trptv/" -r "rtmp://edge.wms28.lorini.net/trptv/" -y "trptv" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.lorini.net"  -q -v > /tmp/$CANAL."$ID" & ;;

	TVO) rtmpdump -m 200 -a "tvo/" -r "rtmp://edge.wms28.lorini.net/tvo/" -y "tvo" -W "http://www.lorini.net/playerv/player.swf" -p "http://www.lorini.net/streaming/clientes/tvo.htm" -q -v > /tmp/$CANAL."$ID" & ;;

	Cetelmon_TV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID"  http://tense.dyndns.org:8207 > /dev/null 2>&1 & mplayer_conf_change ;;  

	SolidariaTV) rtmpdump -m 200 -r "rtmp://flash3.todostreaming.es/solidariatv" -y "mystream" -W "http://www.todostreaming.es/player_new.swf" -p "http://www.solidariatv.com" -q -v > /tmp/$CANAL."$ID" & ;;

	RedBull) rtmpdump -m 200 -r "rtmp://cp93704.live.edgefcs.net/live/" -y "redbull1@21839" -W "http://www.chanfeed.com/streams/mediaplayer.swf" -p "http://chanfeed.com/red-bull-sport" -q -v > /tmp/$CANAL."$ID" & ;;

	TileSport) rtmpdump -m 200 -r "rtmp://tv1.streampulse.eu/tilesport" -y "movie1" -W "http://www.tilesport.tv/jwplayer/player.swf" -p "http://www.tilesport.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Al_Iraqiya_Sports) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://212.7.196.74/sport > /dev/null 2>&1 & mplayer_conf_change ;;
	
	SportItalia) rtmpdump -m 200 -r "rtmp://94.32.97.9/streamit" -y "solocalciolive" -W "http://sportitalia24.twww.tv/embed.swf"  -q -v > /tmp/$CANAL."$ID" & ;;

	SkyPoker) rtmpdump -m 200 -r "rtmp://92.122.49.165:1935/live?_fcs_vhost=cp67698.live.edgefcs.net&akmfv=1.8" -y "SkyPoker_500k@9124" -W "http://www.skypoker.com/img/cms/live_tv_player.swf" -p "http://www.skypoker.com" -q -v > /tmp/$CANAL."$ID" & ;;

	ArgentinisimaTV) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID"  http://tense.dyndns.org:8207 > /dev/null 2>&1 & mplayer_conf_change ;;

	Canal10) rtmpdump -m 200 -a "ustreamVideo/11028856" -r "rtmp://flash74.ustream.tv:1935/ustreamVideo/11028856" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.cba24n.com.ar"  -q -v > /tmp/$CANAL."$ID" & ;;

	CBA24) rtmpdump -m 200 -a "ustreamVideo/11678041" -r "rtmp://flash83.ustream.tv:1935/ustreamVideo/11678041" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.cba24n.com.ar"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal21) rtmpdump -m 200 -a "canal21" -r "rtmp://184.173.6.168:1935/canal21" -y "h264live.f4v" -W "http://fpdownload.adobe.com/strobe/FlashMediaPlayback_101.swf" -p "http://arzbaires.c21tv.com.ar" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal3)  mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://201.251.124.171:1021 > /dev/null 2>&1 & mplayer_conf_change ;;

	Canal5) rtmpdump -m 200 -a "ustreamCdn/flash68/199131" -r "rtmp://flash98.xo.tcdn.ustream.tv:1935/ustreamCdn/flash68/199131" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.ustream.tv" -q -v > /tmp/$CANAL."$ID" & ;;  

	Canal7) rtmpdump -m 200 -a "live/c7" -r "rtmp://cms.tvsiete.tv/live/c7" -y "mp4:canal" -W "http://cms.tvsiete.tv/tools/mediaplayer/pla.swf" -p "http://www.tvsiete.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal9) rtmpdump -m 200 -a "live/c9" -r "rtmp://www.canal9comodoro.com/live/c9" -y "mp4:canal" -W "http://www.canal9comodoro.com/mediaplayer/pla.swf" -p "http://www.canal9comodoro.com" -q -v > /tmp/$CANAL."$ID" & ;;  

	Canal_Provincial) rtmpdump -m 200 -a "live" -r "rtmp://190.2.58.90/live" -y "telered" -W "http://190.105.0.71/stream/jwplayer/player.swf" -p "http://www.canalprovincial.com.ar"  -q -v > /tmp/$CANAL."$ID" & ;;

	El_Rural)  rtmpdump -m 200 -a "live/crural" -r "rtmp://streamrural.cmd.com.ar/live/crural" -y "rural1" -W "http://www.elrural.com/sites/default/files/jwplayermodule/player/player.swf" -p "http://www.elrural.com"  -q -v > /tmp/$CANAL."$ID" & ;;

	El_trece) rtmpdump -m 200 -a "live13/13tv" -r "rtmp://stream.eltrecetv.com.ar/live13/13tv" -y "13tv1" -p "http://www.eltrecetv.com.ar" -q -v > /tmp/$CANAL."$ID" & ;;

	Construir_TV) rtmpdump -m 200 -a "ustreamVideo/9143107" -r "rtmp://flash80.ustream.tv:1935/ustreamVideo/9143107" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.construirtv.com"  -q -v > /tmp/$CANAL."$ID" & ;;

	PakaPaka) rtmpdump -m 200  -r "rtmp://92.122.49.116:1935/live?_fcs_vhost=cp54218.live.edgefcs.net&uu.id=fj5159u7" -y "Canal_Encuentro_3@68921" -W "http://player.multicastmedia.com/templates/livefull2.swf" -p "http://player.multicastmedia.com" -q -v > /tmp/$CANAL."$ID" & ;;

	QMusica) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" mms://streamqm.uigc.net/qmusica > /dev/null 2>&1 & mplayer_conf_change ;;

	Canal26) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" http://200.115.194.1:8080/Canal26 > /dev/null 2>&1 & mplayer_conf_change ;;

	N9) rtmpdump -m 200 -a "ustreamVideo/4009255" -r "rtmp://flash58.ustream.tv:1935/ustreamVideo/4009255" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.noticiero9.com.ar/"  -q -v > /tmp/$CANAL."$ID" & ;;

	TN) rtmpdump -m 200  -a "live" -r "rtmp://stream.tn.com.ar/live" -y "tnmovil2" -W "http://tn.com.ar/sites/all/themes/dientuki/swf/dplayer/player.swf" -p "http://tn.com.ar"  -q -v > /tmp/$CANAL."$ID" & ;; 

	Zona31) rtmpdump -m 200  -a "zona31" -r "rtmp://84.246.231.153/zona31" -y "zona31" -W "http://www.zona31.tv/player.swf" -p "http://www.zona31.tv" -q -v > /tmp/$CANAL."$ID" & ;;
	
	Canal13) rtmpdump -m 200 -a "ustreamCdn/flash72/1358413" -r "rtmp://flash89.xo.tcdn.ustream.tv:1935/ustreamCdn/flash72/1358413" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.ustream.tv/channel-popup/canal13riocuar.to" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal10_Tucuman) rtmpdump -m 200 -a "live/8" -r "rtmp://200.85.152.45:1935/live/8" -y "stream" -W "http://www.g-video.org/embed.swf" -p "http://www.g-video.org/embed/8/425/351/FALSE/false" -q -v > /tmp/$CANAL."$ID" & ;;

	LapachoTV) rtmpdump -m 200 -r "rtmp://84.246.231.153/lapacho" -y "lapacho" -W "http://www.lapachotv.com.ar/jwplayer/player.swf" -p "http://www.lapachotv.com.ar/vivo/" -q -v > /tmp/$CANAL."$ID" & ;;

	FacetasDeportivas) rtmpdump -m 200 -a "live/_definst_" -r "rtmp://68.68.30.139/live/_definst_" -y "facetas1" -W "http://www.veemi.com/player/player-licensed.swf" -p "http://www.veemi.com/embed.php"  -q -v > /tmp/$CANAL."$ID" & ;;

	Cable_Noticias) rtmpdump -m 200 -a "live/" -r "rtmp://50.23.172.98:1935/live/" -y "cablenoticias" -W "http://www.cablenoticias.tv/player.swf" -p "http://www.cablenoticias.tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal_Tiempo) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "http://208.80.54.128/CANALELTIEMPO?streamtheworld_user=1&nobuf=1355954794813" > /dev/null 2>&1 & mplayer_conf_change ;;

	Tu_Kanal) rtmpdump -m 200 -a "ustreamVideo/10317018" -r "rtmp://flash81.ustream.tv:1935/ustreamVideo/10317018" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -y "streams/live_1" -p "http://www.ustream.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	PyC) rtmpdump -m 200 -a "ustreamVideo/10554562" -r "rtmp://flash93.ustream.tv:1935/ustreamVideo/10554562" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.proyectosycomunicaciones.com"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal_Capital) rtmpdump -m 200 -a "ustream4live-live/" -r "rtmp://ustreamlivefs.fplive.net:1935/ustream4live-live/" -y "stream_live_1_1_9968011" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:353.swf" -p "http://www.ustream.tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	CMB) rtmpdump -m 200 -a "cmbtv" -r "rtmp://4.30.20.151/cmbtv" -y "cmbtv1" -W "http://cpanel.netpatio.com/swfs/jwplayer/player.swf" -p "http://www.cmbcolombia.tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	CristoVision) rtmpdump -m 200 -a "8008" -r "rtmp://wowzatv.paradigmaweb.com/8008" -y "8008" -W "http://www.cristovision.tv/player/playertv.swf" -p "http://www.cristovision.tv"  -q -v > /tmp/$CANAL."$ID" & ;;

	TeleVida) rtmpdump -m 200 -a "live" -r "rtmp://streaming3.vcb.com.co/live" -y "myStream" -W "http://eventos.vcb.com.co/mobile/player.swf" -p "http://eventos.vcb.com.co"  -q -v > /tmp/$CANAL."$ID" & ;;

	RTVC) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://cdns724ste1010.multistream.net:80/rtvclive/live-200" > /dev/null 2>&1 & mplayer_conf_change ;;
	
	RTVC2) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://cdns724ste1010.multistream.net:80/rtvc2live/live-200" > /dev/null 2>&1 & mplayer_conf_change ;;

	TeleCaribe) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://cdns724ste1010.multistream.net:80/telecaribelive/live-200" > /dev/null 2>&1 & mplayer_conf_change ;;

	TelePacifico) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://cdns724ste1010.multistream.net:80/telepacificolive/live-200" > /dev/null 2>&1 & mplayer_conf_change ;;

	######

	RPC) rtmpdump -m 200 -a "live" -r "rtmp://74.222.1.108:1935/live" -y "canal13_hq.stream" -W "http://www.rpc.com.py/swf/player_web03.swf" -p "http://www.rpc.com.py"  -q -v > /tmp/$CANAL."$ID" & ;;

	Paravision) rtmpdump -m 200 -a "TV" -r "rtmp://83.170.79.14/TV" -y "paravisionext" -p "http://www.desdeparaguay.com" -q -v > /tmp/$CANAL."$ID" & ;;

	TeleFuturo) rtmpdump -m 200 -a "live" -r "rtmp://190.52.182.109:1935/live" -W "http://fpdownload.adobe.com/strobe/FlashMediaPlayback.swf" -y "myStream" -p "http://www.telefuturo.com.py" -q -v > /tmp/$CANAL."$ID" & ;;

	#####

	TelevisaHD) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "http://televisahdlive-f.akamaihd.net/gball01_1_475@56607"  > /dev/null 2>&1 & mplayer_conf_change ;;

	Milenio) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "http://brightcove03-f.akamaihd.net/milenio_centro_512k@51752"  > /dev/null 2>&1 & mplayer_conf_change ;;

	OnceTV) rtmpdump -m 200 -r "rtmp://www.oncetvmexicolive.tv:1935/livepkgr2" -y "int3" -W "http://www.oncetvmexicolive.tv/StrobeMediaPlayback.swf" -p "http://www.oncetvmexicolive.tv/internacional/" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal66) rtmpdump -m 200 -a "canal66" -r "rtmp://unirtmp.tulix.tv:1935/canal66" -y "myStream.sdp" -W "http://www.streamwebtown.com/mediaplayer/player.swf" -p "http://giliboi.com/canal66/web/" -q -v > /tmp/$CANAL."$ID" & ;;

	Canal44) rtmpdump -m 200 -a "canal44" -r "rtmp://unirtmp.tulix.tv:1935/canal44" -y "myStream.sdp" -W "http://www.streamwebtown.com/mediaplayer/player.swf" -p "http://www.canal44.com/envivo.php" -q -v > /tmp/$CANAL."$ID" & ;;

	Congreso) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://apreal03.triara.com/broadcast/canalcongreso.rm"  > /dev/null 2>&1 & mplayer_conf_change ;;

	Canal_Justicia) rtmpdump -m 200 -a "rtmplive" -r "rtmp://72.233.123.138:1936/rtmplive/" -y "/broadcast/scjnA1.mp4" -W "http://www.scjn.gob.mx/player/player.swf" -p "http://www.scjn.gob.mx/Paginas/transmision_vivo.aspx" -q -v > /tmp/$CANAL."$ID" & ;;

	Cortes_Diputados) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "rtsp://201.147.98.13:554/broadcast/sesion.rm"  > /dev/null 2>&1 & mplayer_conf_change ;; 

	Kanal_D) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "mms://beotelmedia.beotel.net/kanald"  > /dev/null 2>&1 & mplayer_conf_change ;;

	Sat7_Kids) mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "mms://wm1.sz.xlcdn.com/sz=SAT7=CYSAT7KIDS"  > /dev/null 2>&1 & mplayer_conf_change ;; 

	SmileofaChildTV) rtmpdump -m 200 -a "live" -r "rtmp://cp114426.live.edgefcs.net:1935/live?ovpfv=2.1.5" -y "smile_mbr_high_3@59409" -W "http://www.tbn.org/flash/hd_player_4x3.swf" -p "http://www.tbn.org"  -q -v > /tmp/$CANAL."$ID" & ;;

	Barbaraki_TV) rtmpdump -m 200  -r "rtmp://80.93.53.88:1935/live" -y "channel_6" -W "http://www.planeta-online.tv/planeta_player.swf" -p "http://www.planeta-online.tv" -q -v > /tmp/$CANAL."$ID" & ;;
	
	Minika_GO) rtmpdump -m 200 -r "rtmp://5.63.145.228:443/minika" -y "minika3" -W "http://i.tmgrup.com.tr/mnka/player/TMDMedia/TMDPlayer327.swf" -p "http://www.minika.com.tr" -q -v > /tmp/$CANAL."$ID" & ;;

	Minika_Cocuk )rtmpdump -m 200 -r "rtmp://198.105.211.4:443/minikacocuk" -y "minikacocuk3" -W "http://i.tmgrup.com.tr/mnka/player/TMDMedia/TMDPlayer327.swf" -p "http://www.minika.com.tr"  -q -v > /tmp/$CANAL."$ID" & ;;

	Yumurcak)  rtmpdump -m 200  -r "rtmp://eu01.kure.tv:80/liveedge" -y "yumurcak3" -W "http://web1.kure.tv/P/player_files/flowplayer.commercial-3.2.7.swf" -p "http://www.kure.tv" -q -v > /tmp/$CANAL."$ID" & ;;

	Gang_Cartoon_Channel)  mplayer -really-quiet -dumpstream -dumpfile /tmp/$CANAL."$ID" "mmsh://202.43.34.236/gan?server_time=1/17/2013%2010:22:04%20PM&hash_value=NUUej8agT0qDgDXQbJeIkw==&validminutes=480&MSWMExt=.asf"  > /dev/null 2>&1 & mplayer_conf_change ;;  

	RTS) rtmpdump -m 200 -a "vl/_definst_" -r "rtmp://96.44.149.50/vl/_definst_" -y "rtsonline88" -W "http://www.veemi.com/player/player-licensed.swf" -p "http://www.veemi.com/embed.php"  -q -v > /tmp/$CANAL."$ID" & ;;

	Canal1) rtmpdump -m 200 -a "vsharepulllive-live" -r "rtmp://vsharepulllivefs.vod.swiftcdn1.com:443/vsharepulllive-live" -y "18d0u2b661j" -W "http://vshare.tv/flash/player_209.swf" -p "http://www.canal1tv.com/" -q -v > /tmp/$CANAL."$ID" & ;;


	Ecuadortv) rtmpdump -m 200 -a "live" -r "rtmp://38.96.148.216:1935/live" -y "ecuadortvn" -W "http://www.ecuadortv.ec/mod_video/player.swf" -p "http://www.ecuadortv.ec/ecu.php?c=43" -q -v > /tmp/$CANAL."$ID" & ;;

	Oromar) rtmpdump -m 200 -a "ustreamVideo/10684956" -r "rtmp://flash82.ustream.tv:1935/ustreamVideo/10684956" -y "streams/live_1" -W "http://static-cdn1.ustream.tv/swf/live/viewer.rsl:360.swf" -p "http://www.ustream.tv/embed/10684956"  -q -v > /tmp/$CANAL."$ID" & ;;

	*) echo -e "\n \e[00;36mBorrando ficheros temporales y saliendo,... \e[00m\n" && rm /tmp/versiontv /tmp/tvhelp > /dev/null 2>&1 ; exit ;;

esac



############################## Reproducir el streaming.

LASTPID=$(echo $!)
echo -e "\n * \e[00;36mConectando a $CANAL\e[00m\n"
sleep $CACHE_STREAMING

if [ -e /tmp/$CANAL."$ID" ]; then # Si existe, miramos el tamaño. Con mplayer, cuando no puede descargar el streaming, no crea el fichero.
	size=`du /tmp/$CANAL."$ID" | cut -f1`
else
	size=0
fi

if [ $KDE -eq 1 ]; then # Si KDE no está arrancado.

	if [ $size -lt 90 -a $fifo -eq 1 ]; then
		 echo -e " \e[00;31mError al conectar a $CANAL\e[00m\n"
		 zenity --no-wrap --error --text="No se ha podido establecer comunicación con el servidor de streaming de $CANAL" ;
		 rm /tmp/$CANAL."$ID" > /dev/null 2>&1 ;
		
	 else

		mplayer_keys &
		reproductor;
		
		if [ $SAVE -eq 0 -a $fifo -eq 1 ]; then
			zenity --question --text "¿Desea guardar el streaming de video en disco?" ;
	
			case $? in
   				0) mv /tmp/$CANAL."$ID" `zenity --file-selection --save` > /dev/null 2>&1 ;;
   			esac
		fi
	fi


elif [ $KDE -eq 0 ]; then # Si KDE está arrancado.


	if [ $size -lt 90 -a $fifo -eq 1 ]; then
		echo -e " \e[00;31mError al conectar a $CANAL\e[00m\n"
		kdialog --title 'Fallo al conectar' --error "No se ha podido establecer comunicación con el servidor de streaming de $CANAL" ;
		rm /tmp/$CANAL."$ID" > /dev/null 2>&1 ;
	else
		mplayer_keys &
		reproductor;
	
		if [ $SAVE -eq 0 ]; then	
			kdialog --yesno "¿Desea guardar el streaming de video en disco?" ;
	
			case $? in
   				0) mv /tmp/$CANAL."$ID" `kdialog --getsavefilename $HOME` > /dev/null 2>&1 ;;
   			esac
		fi
	fi



fi

############################## Desconectamos del canal y arancamos de nuevo el script.

echo -e " \e[00;36mBorrando temporales\e[00m\n" && rm /tmp/$CANAL."$ID" > /dev/null 2>&1
kill -1 $LASTPID > /dev/null 2>&1
echo -e " \e[00;35m---\e[00m\n"
bash $0 # Comentar esta linea si no queremos que se ejecute de nuevo una vez terminada la emisión.
