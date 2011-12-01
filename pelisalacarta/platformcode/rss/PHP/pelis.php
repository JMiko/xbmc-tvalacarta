#!/tmp/www/cgi-bin/php
﻿<?php 
//header("Content-Type: plain/xml");

   $MI_IP = "192.168.1.20";
   $INICIAR_PELISALACARTA = "cd /opt/pelisalacarta; /opt/bin/python /opt/pelisalacarta/pelisalacarta.py  > /dev/null 2> /dev/null &";
   $INICIAR_PYLOAD = "cd /opt/pyload; /opt/bin/python pyLoadCore.py --configdir=/opt/pyload/.pyload  > /dev/null 2> /dev/null &";
    
   $uri = $_SERVER["PHP_SELF"];
   $ip_remota = $_SERVER["REMOTE_ADDR"];

   if ($ip_remota == "127.0.0.1") $ip_local = "127.0.0.1";
   else                           $ip_local = $MI_IP;
   $mi_url = "http://".$ip_local.$uri."?url=";

   $url = substr($_ENV["QUERY_STRING"],4);
   if ($url == "") $url = "http://127.0.0.1:9000/rss/";

   $ruta = explode("/", $url); # http:, '', host, rss, canal, accion, url, server, categoria, fulltitle
   $host = $ruta[2];
   $canal = $ruta[4];
   $accion = $ruta[5];
   //echo "url = ".$url."<BR>\nhost = ".$host."<BR>\ncanal = ".$canal."<BR>\naccion = ".$accion."<BR>\n";
   $translate = NULL;
   
   inicia_pelisalacarta();
   if ($canal == "pyload") inicia_pyload();
   $xml = file_get_contents($url);
   $tipo_contenido = tipo_contenido();
   pinta_cabecera();
  
   // Pinta titulo del canal
   if (preg_match( "/\<title\>(.*?)\<\/title\>/s", $xml, $match )) $titulo_canal = $match[1];
   echo "<channel>\n";
   echo "<title>$titulo_canal</title>\n";
   echo "<link>$url</link>\n\n";
  

   preg_match_all( "/\<item\>(.*?)\<\/item\>/s", $xml, $items );
   foreach( $items[1] as $item ) // Trata cada item
   {
       // Busca todos los elementos posibles del item en curso
       preg_match_all( '/\<title\>(.*?)\<\/title\>/', $item, $titulo );
       preg_match_all( "/\<fulltitle\>(.*?)\<\/fulltitle\>/", $item, $fulltitle );
       preg_match_all( "/\<image\>(.*?)\<\/image\>/", $item, $imagen );
       preg_match_all( "/\<link\>(.*?)\<\/link\>/", $item, $link );
       preg_match_all( "/\<description\>(.*?)\<\/description\>/", $item, $descr );
       preg_match_all( '#\<search url\="(.*?)" />#U', $item, $search );
       if (count($link[1]) == 0) preg_match_all( '#\<enclosure url\="(.*?)" type\="(.*?)"#U', $item, $link );
  
       echo "<item>\n";
       if ($tipo_contenido == "videos_translate") {
           echo ("<title>".$titulo[1][0]."</title>\n");
           echo ("<fulltitle>".$fulltitle[1][0]."</fulltitle>\n");
           echo ("<image>".$imagen[1][0]."</image>\n");
           echo ("<description>".$descr[1][0]."</description>\n");
           echo ("<stream_url>".str_replace("&","&amp;",$link[1][0])."</stream_url>\n"); 
           echo ("<stream_class>video</stream_class>\n");
           echo ("<stream_protocol>http</stream_protocol>\n");
           echo ("<mediaDisplay name=\"photoView\"/>");
           //echo ("<protocol>http</protocol>\n");
           //echo ("<location>".$link[1][0]."</location>\n");
           //echo ("<stream_url><script>translate_base_url+\"stream,,".$link[1][0]."\";</script></stream_url>\n");
           //echo ("<stream_type>video/x-flv</stream_type>\n");
       }
       elseif ($tipo_contenido == "videos_enclosure") {
           echo ("<title>".$titulo[1][0]."</title>\n");
           echo ("<fulltitle>".$fulltitle[1][0]."</fulltitle>\n");
           echo ("<image>".$imagen[1][0]."</image>\n");
           echo ("<description>".$descr[1][0]."</description>\n");
           echo ("<media:content url=\"".str_replace("&","&amp;",$link[1][0])."\" />\n"); 
           echo ("<mediaDisplay name=\"photoView\"/>");
           //echo ("<enclosure url=\"".$link[1][0]."\" type=\"".$link[1][1]."\" />\n");
       }
       else {
           echo ("<title>".html_entity_decode($titulo[1][0])."</title>\n");
           if ($fulltitle[1][0]) echo ("<fulltitle>".$fulltitle[1][0]."</fulltitle>\n");
           echo ("<image>".$imagen[1][0]."</image>\n");
           if ($descr[1][0]) echo ("<description>".$descr[1][0]."</description>\n");
           if ($link[1][0] == "rss_command://search") {
                echo ("<link>rss_command://search</link>\n");
                echo ("<search url=\"".$mi_url.$search[1][0]."\" />\n");
           }
           else echo ("<link>".$mi_url.$link[1][0]."</link>\n");
       }
       echo "</item>\n";
   }
  
   echo "</channel>\n</rss>\n";

function tipo_contenido() {
   global $canal, $translate, $xml;
   $tipo = "menu";
  
   preg_match_all( '#\<enclosure url\="(.+?)" type\="(.*?)"#U', $xml, $result );
   $con_videos = (count($result[1])  > 0);
   preg_match_all( "/\<description\>(.+?)\<\/description\>/", $xml, $result );
   $con_plot = (count($result[1])  > 0);
   preg_match_all( "/\<image\>(.+?)\<\/image\>/", $xml, $result );
   $con_imagen = (count($result[1])  > 0);
   if ($con_imagen) {
       $menu = true;
       $primera_imagen = $result[1][0];
       foreach( $result[1] as $img )
          if ($img != $primera_imagen) $menu = false;
   }
   if ($con_videos) { 
       if ($translate === NULL) $translate = get_modo_play(); 
       if ($translate) $tipo = "videos_translate";
       else            $tipo = "videos_enclosure";
   }
   else {
       if (in_array($canal,array("","channelselector"))) $tipo = "iconos";
       elseif ($menu) {
           if ($con_plot) $tipo = "menu_video";
           else $tipo = "caratulas";
       }
       elseif ($con_imagen) $tipo = "caratulas";
   }
   return $tipo;
}
  
function pinta_cabecera() { 
  global $tipo_contenido;
  
  $ruta_real = dirname(realpath($_SERVER['SCRIPT_FILENAME']));
  
  if ($tipo_contenido == "menu") $cab = "cabecera_menu";
  if ($tipo_contenido == "iconos") $cab = "cabecera_iconos";
  if ($tipo_contenido == "menu_video") $cab = "cabecera_mirror";
  if ($tipo_contenido == "caratulas") $cab = "cabecera_caratulas";
  if ($tipo_contenido == "videos_translate") $cab = "cabecera_fuentes_translate";
  if ($tipo_contenido == "videos_enclosure") $cab = "cabecera_fuentes_enclosure";
   
  $fichcab = fopen("$ruta_real/$cab.rss","r"); 
  while( $data = fgets( $fichcab, 4096 ) ) { echo($data); }
  fclose($fichcab);

}

function get_modo_play() { 
    global $host;
    $trans = FALSE;
    
    $url_conf = "http://$host/rss/configuracion/mainlist/none/none/none/none/none/playlist.rss";
    $conf = file_get_contents($url_conf);
    if (preg_match( '#Media translate activado: (true)#', $conf, $hallado )) $trans = TRUE;
    return $trans;
    /*
    $translate = false;
    $CONF_PELISALACARTA = "/opt/pelisalacarta/.pelisalacarta/pelisalacarta.conf";
    $conf = file_get_contents($CONF_PELISALACARTA);
    if (preg_match( '#enablemedia-translate[ ]*\=[ ]*([a-z]+)#', $conf, $hallado ) && $hallado[1] == "true") 
        $translate = true;
    return $translate;
    */
}

function inicia_pelisalacarta() {
   global $host, $MI_IP, $INICIAR_PELISALACARTA;
   // Si es una peticion a pelisalacarta local y está parado, lo inicia
   $paso = explode(":",$host);
   if ($paso[0] == "127.0.0.1" || $paso[0] == $MI_IP) {
      $py_parado = true;
      exec("ps -aux | grep pelisalacarta | grep -v grep", $pslist); 
      if (count($pslist) == 0) {
         shell_exec($INICIAR_PELISALACARTA);
         sleep(15);
      }
   }
}

function inicia_pyload() {
   global $host, $MI_IP, $INICIAR_PYLOAD;
   // Si es una peticion a pelisalacarta local y está parado, lo inicia
   $paso = explode(":",$host);
   if ($paso[0] == "127.0.0.1" || $paso[0] == $MI_IP) {
      $py_parado = true;
      exec("ps -aux | grep pyLoad | grep -v grep", $pslist); 
      if (count($pslist) == 0) {
         shell_exec($INICIAR_PYLOAD);
         sleep(15);
      }
   }
}

  

