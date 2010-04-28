#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Tivion
## Copyright (C) 2009 Ángel Guzmán Maeso
## http://shakaran.net
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

CHANNEL_VERSION = '1269635428' # Total channels 692, 67 countries, lastest ID 698

import tivioncountries as co
import tivionconstants as cons

### List of channels 
# Do you have a new channel? Do you want to add? or some channel is broken?
# Send me an email to shakaran at gmail dot com and add/fix it with pleasure
CHANNEL = [ # Note: Channel 0 is reserved!
            ## Spain ## 58
            # [BROKEN-INVALID]['1', co.es_ES, cons.TV, 'La 1 - TVE - HD', 'FILMON23'],
            # http://79.125.47.119/rtve?auth=b814ab9dfca5a83ef9187a1aed60ba4d
            # [BROKEN-INVALID]['2', co.es_ES, cons.TV, 'La 1 - TVE LoSp', 'FILMON53'],
            # http://79.125.47.119/rtve_ls?auth=31b3e9148bfdd951671fb9e97a575dce
            # http://rtve.stream.flumotion.com/rtve/24h.flv.m3u BROKEN
            # http://195.10.10.103:80/rtve/24h.flv # BROKEN
            # http://194.224.110.205:80/rtve/24h.flv (Actual Server)
            ['1', co.es_ES, cons.TV, '24 horas', 'http://24h.rtve.stream.flumotion.com/rtve/24h.flv.m3u'],
            # Broken: http://nova.stream.flumotion.com/antena3/nova.asf.asx
            # Broken! ['4', co.es_ES, cons.TV, 'Nova', 'http://195.10.10.103:80/antena3/nova.asf'],
            ['2', co.es_ES, cons.TV, 'Intereconomía', 'mms://www.intereconomia.com/INTERECONOMIA-TV'],
            ['3', co.es_ES, cons.TV, 'Canal Sur', 'http://andaluciatelevision.rtva.stream.flumotion.com/rtva/andaluciatelevision.flv.m3u'],
            # http://195.10.10.209:80/rtva/andaluciatelevision.flv'],
            # http://195.10.10.215:80/rtva/andaluciatelevision.flv
            ['4', co.es_ES, cons.TV, 'Extremadura', 'http://195.10.10.214:80/extremaduratv/live1_600.flv'],
            # http://live1.extremaduratv.stream.flumotion.com/extremaduratv/live1_600.flv.m3u
            # Antena 3 - Have a variable IP - Needs a parser
            # BROKEN?: http://83.231.187.102:80/antena3/antena3.asf
            # Current?: http://83.231.187.101:80/antena3/antena3.asf
            # OR? http://195.10.10.103:80/antena3/antena3.asf
            ['5', co.es_ES, cons.TV, 'Antena 3', 'A3'],
            ['6', co.es_ES, cons.TV, 'A3 Noticias 24h (slow)', 'http://199.93.35.37/antena3wmlive-live/canal24h?MSWMExt=.asf'],
            # mms://antena3livewm.fplive.net/antena3wmlive-live/canal24h
            # http://199.93.35.37:80/antena3wmlive-live/canal24h?MSWMExt=.asf
            # http://199.93.35.37/antena3wmlive-live/canal24h?MSWMExt=.asf
            # http://antena3livewm.fplive.net/antena3wmlive-live/canal24h?MSWMExt=.asf
            # BROKEN: http://neox.stream.flumotion.com/antena3/neox.asf.asx
            # BROKEN! ['9', co.es_ES, cons.TV, 'Neox 8 (slow)', 'http://195.55.74.101:80/antena3/neox.asf'],
            # http://neox.stream.flumotion.com/antena3/neox.asf.asx
            ['7', co.es_ES, cons.TV, 'Canal Parlamento (slow)', 'mms://stream2.terra.es/wm2live1'],
            # http://10.20.38.13:80/wm2live1?MSWMExt=.asf 
            # http://stream2.terra.es/wm2live1?MSWMExt=.asf
            ['8', co.es_ES, cons.TV, 'A3 Internacional (slow)', 'http://206.33.32.19:80/antena3wmlive-live/canalinternacional?MSWMExt=.asf'],
            # mms://antena3livewm.fplive.net/antena3wmlive-live/canalinternacional
            # http://antena3livewm.fplive.net/antena3wmlive-live/canalinternacional?MSWMExt=.asf
            # http://a1808.l1571639807.c15716.e.lm.akamaistream.net/D/1808/15716/v0001/reflector:39807
            # BROKEN  09-01-10 ['12', co.es_ES, cons.TV, 'CNN+', 'http://90.84.49.102:80/D/1808/15716/v0001/reflector:39807?MSWMExt=.asf'],
            # mms://a1808.l1571639807.c15716.e.lm.akamaistream.net/D/1808/15716/v0001/reflector:39807
            # http://a1808.l1571639807.c15716.e.lm.akamaistream.net/D/1808/15716/v0001/reflector:39807?MSWMExt=.asf
            ['9', co.es_ES, cons.TV, 'ATEI (slow)', 'http://calixto.c.mad.interhost.com/radioatei'],
            # BROKEN ['14', co.es_ES, cons.TV, 'Almansa TV (slow)', 'http://89.29.128.6:7007/'],
            ['10', co.es_ES, cons.TV, 'Almansa TV (slow)', 'mms://89.29.128.10/tvalmansa'],
            # http://195.10.10.215:80/tvaragon/live.asf
            ['11', co.es_ES, cons.TV, 'Aragon TV', 'http://live.tvaragon.stream.flumotion.com/tvaragon/live.asf.asx', cons.ASX],
            ['12', co.es_ES, cons.TV, 'Ojos Solidarios TV', 'mms://wm.mad.interhost.com/OjosSolidariosTv'], # Canal 13 Digital (Las Palmas de Gran Canaria )
            ['13', co.es_ES, cons.TV, 'Duson TV (slow)', 'mms://antena.fundaciongoldenclover.com/live'], # Medicina Natural
            # BROKEN 09-01-10 ['18', co.es_ES, cons.TV, 'ETB Sat', 'mms://a217.l881320216.c8813.e.lm.akamaistream.net/D/217/8813/v0001/reflector:20216'],
            ['14', co.es_ES, cons.TV, 'Fuego TV', 'mms://rcri2.com/fuegotv'],
            ['15', co.es_ES, cons.TV, 'IB3 TV', 'mms://streamingtv01.ib3.es/ib3tv_en_directe'],
            ['16', co.es_ES, cons.TV, 'Localia-Huesca', 'mms://streaming.wdreams.com/localiatv'],
            ['17', co.es_ES, cons.TV, 'Madrid (DGT)', 'mms://stream2.terra.es/wm2live2'],
            ['18', co.es_ES, cons.TV, 'Radio Televisión Insular', 'mms://wagner.serveisweb.com/TI013'], #RTI o RTV Insular o RTI Gran Canaria
            ['19', co.es_ES, cons.TV, 'Teleasturias', 'mms://DWS28.dinaserver.com/directo'],
            ['20', co.es_ES, cons.TV, 'Telebahia - Cantabria', 'mms://stream.visualnetworks.es/str059'],
            ['21', co.es_ES, cons.TV, 'TV Ferrol', 'http://stream.visualnetworks.es:3840/tvf'],
            ['22', co.es_ES, cons.TV, 'Teletaxi', 'mms://88.87.218.43/teletaxitv'],
            ['23', co.es_ES, cons.TV, 'TV Canaria', 'mms://wm.gobiernodecanarias.org/tvctdt'],
            ['24', co.es_ES, cons.TV, 'TV Martí', 'mms://a165.1211035484.c2110.g.lm.akamaistream.net/D/165/2110/v0001/reflector:35484'],
            ['25', co.es_ES, cons.TV, 'TV Segovia', 'mms://video.ono.com/tvcyl_tvsg'],
            ['26', co.es_ES, cons.TV, 'Onda Almeria TV', 'mms://84.20.4.142/ondamartv'],
            ['27', co.es_ES, cons.TV, 'Videncia TV', 'mms://verdi.serveisweb.com/AT018'], # Mundo mágico TV
            ['28', co.es_ES, cons.TV, 'Cervantes TV', 'mms://193.146.5.220/Cervantes_tv'], 
            ['29', co.es_ES, cons.TV, 'TVCI HD', 'mms://i2catvserver.i2cat.net/TVC_inter'],
            ['30', co.es_ES, cons.TV, 'Canal Noticias Huelva', 'mms://video.ono.com/cnh'], #CNH
            ['31', co.es_ES, cons.TV, 'CRTVG Galicia', 'mms://85.91.64.23/Television'],
            ['32', co.es_ES, cons.TV, 'Ejido TV', 'mms://bach.serveisweb.com/EJ002'],
            ['33', co.es_ES, cons.TV, 'Estepona TV', 'mms://216.66.84.2/237461'],
            ['34', co.es_ES, cons.TV, 'Estrada TV', 'mms://82.223.149.58/estradatelevision'],
            ['35', co.es_ES, cons.TV, 'STV Rioja', 'mms://www.riojasintonia.com/stv'],
            ['36', co.es_ES, cons.TV, 'TeleTrébol', 'mms://streaming.alisys.net/rsa_tv?.wma'],
            ['37', co.es_ES, cons.TV, 'TVMas (Maspalomas)', 'mms://win.1.c3.audiovideoweb.com/1c3winlive6808'],
            ['38', co.es_ES, cons.TV, 'TVVi', 'mms://hechicera.cap.gva.es/tvvi?rtvv'],
            ['39', co.es_ES, cons.TV, 'Universidad Rey Juan Carlos', 'mms://marx.urjc.es/urjc'], #URJC
            ['40', co.es_ES, cons.TV, 'Universidad de Vigo', 'mms://193.146.209.50/directo'], 
            ['41', co.es_ES, cons.TV, 'Velevisa TV - Velez-Málaga', 'mms://212.163.215.206/Directo'], 
            ['42', co.es_ES, cons.TV, 'Cetelmon TV', 'mms://wagner.serveisweb.com/CE027'],
            ['43', co.es_ES, cons.TV, 'Canal 7', 'http://195.10.10.211/canal7tv/live.asf'],
            ['44', co.es_ES, cons.RADIO, 'Canal Sur Radio', 'http://canalsurradio.rtva.stream.flumotion.com/rtva/canalsurradio_master.mp3.m3u'], # --crop=16:9 --aspect-ratio=16:9
            ['45', co.es_ES, cons.RADIO, 'Radio Andalucía', 'http://radioandalucia.rtva.stream.flumotion.com/rtva/radioandalucia.mp3.m3u'], # --crop=16:9 --aspect-ratio=16:9
            ['46', co.es_ES, cons.RADIO, 'Canal Fiesta Radio', 'http://canalfiestaradio.rtva.stream.flumotion.com/rtva/canalfiestaradio_master.mp3.m3u'], # --crop=16:9 --aspect-ratio=16:9
            ['47', co.es_ES, cons.RADIO, 'Canal Flamenco', 'http://canalflamenco.rtva.stream.flumotion.com/rtva/canalflamenco.mp3.m3u'], # --crop=16:9 --aspect-ratio=16:9
            ['48', co.es_ES, cons.RADIO, 'Cadena SER Motril', 'http://217.125.82.196:4556'], # --crop=16:9 --aspect-ratio=16:9
            ['49', co.es_ES, cons.RADIO, 'RNE Radio 1', 'mms://a259.l773120483.c7731.e.lm.akamaistream.net/D/259/7731/v0001/reflector:20483'], # --crop=16:9 --aspect-ratio=16:9
            # http://www.rtve.es/rne/audio/r1live.asx
            ['50', co.es_ES, cons.RADIO, 'RTVE RNE Radio 1', 'mms://a729.l830022151.c8300.e.lm.akamaistream.net/D/729/8300/v0001/reflector:22151'], # --crop=16:9 --aspect-ratio=16:9
            ['51', co.es_ES, cons.RADIO, 'RTVE RNE Radio 1 (mirror)', 'mms://a1210.l830022154.c8300.e.lm.akamaistream.net/D/1210/8300/v0001/reflector:22154'], # --crop=16:9 --aspect-ratio=16:9
            # http://www.rtve.es/rne/audio/RNEclasica.asx
            ['52', co.es_ES, cons.RADIO, 'RNE Clásica', 'mms://a1247.l910622804.c9106.e.lm.akamaistream.net/D/1247/9106/v0001/reflector:22804'],
            # http://www.rtve.es/rne/audio/RNE3.asx
            ['53', co.es_ES, cons.RADIO, 'RNE 3', 'mms://a1830.l830120550.c8301.e.lm.akamaistream.net/D/1830/8301/v0001/reflector:20550'],
            ['54', co.es_ES, cons.RADIO, 'RNE 3 (mirror)', 'mms://a1830.l830120550.c8301.e.lm.akamaistream.net/D/1830/8301/v0001/reflector:20551'],
            # http://www.rtve.es/rne/audio/RNE4.asx
            ['55', co.es_ES, cons.RADIO, 'RNE 4', 'mms://a783.l1041530780.c10415.e.lm.akamaistream.net/D/783/10415/v0001/reflector:30780'],
            # http://www.rtve.es/rne/audio/RNE5.asx
            ['56', co.es_ES, cons.RADIO, 'RNE 5', 'mms://a1360.l910520572.c9105.e.lm.akamaistream.net/D/1360/9105/v0001/reflector:20572'],
            ['57', co.es_ES, cons.RADIO, 'RNE 5 (mirror)', 'mms://a1520.l910520573.c9105.e.lm.akamaistream.net/D/1520/9105/v0001/reflector:20573'],
            #[FIXME]IMG but no sound['30', en_GB, 'Radio Marca', 'mms://reflector.radiomarca.com:9004'], # --crop=16:10 --aspect-ratio=16:9
            ['58', co.es_ES, cons.RADIO, 'COPE', 'http://83.231.187.202:80/cope/copefm.asf'], # --crop=16:9 --aspect-ratio=16:9
            ['59', co.es_ES, cons.RADIO, 'OndaCero Madrid', 'mms://ondacerolivewm.fplive.net/ondacerowmlive-live/oc_convencional'], # --crop=16:9 --aspect-ratio=16:9
            ['60', co.es_ES, cons.RADIO, 'Europa FM', 'http://europafm.antena3.stream.flumotion.com/europafm/europafm.mp3.m3u'], # --crop=16:9 --aspect-ratio=16:9
            # [FIXME] Need a ASF parser http://cadena100.cope.stream.flumotion.com/cope/cadena100.asf.asx
            ['61', co.es_ES, cons.RADIO, 'Cadena 100', 'http://195.55.74.213:80/cope/cadena100.asf'],
            ['62', co.es_ES, cons.RADIO, 'Radio Surco', 'http://c05.webmanchaonline.com:9006/live'],
            ['63', co.es_ES, cons.RADIO, 'Punto Radio', 'http://www.puntoradio.com/streaming/puntoradio.pls'], # --crop=16:9 --aspect-ratio=16:9
            ['64', co.es_ES, cons.RADIO, 'RTV Amistad', 'mms://markoni.netpatio.com/rtvamistad/rtvamistad'],
            ['65', co.es_ES, cons.RADIO, 'Vaughan Radio - PLS', 'http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=pls'], # ovh.net
            #[FIXME] Stream not seekable! Totem works well.['56', co.es_ES, 'Vaughan Radio - PLS and RAM (Proxy)', 'http://server03.streaming-pro.com/CLUSTER/castcontrol/proxy.php?id=7'], # ovh.net
            # http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=pls&proxy=true
            #[FIXME] Stream not seekable!['57', co.es_ES, 'Vaughan Radio - ASX', 'http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=asx'], # ovh.net
            ['66', co.es_ES, cons.RADIO, 'Vaughan Radio - ASX (Proxy)', 'http://server03.streaming-pro.com/CLUSTER/castcontrol/proxy.php?wmp=true&id=7'], # ovh.net
            # http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=asx&proxy=true
            #[FIXME] Stream not seekable!['59', co.es_ES, 'Vaughan Radio - RAM', 'http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=ram'], # ovh.net
            #['60', co.es_ES, 'Vaughan Radio - RAM (Proxy)', 'http://server00.streaming-pro.com/castcontrol/castcontrol/playlist.php?id=4&type=ram&proxy=true'], # ovh.net
            #http://server03.streaming-pro.com/CLUSTER/castcontrol/proxy.php?id=7
            ['67', co.es_ES, cons.RADIO, 'Canal Extremadura', 'http://radio.extremaduratv.stream.flumotion.com/extremaduratv/canalextremaduraradio.mp3.m3u'],
            ['68', co.es_ES, cons.RADIO, 'TV-Canarias-SAT', 'mms://wm.gobiernodecanarias.org/tvc2'],
            ['69', co.es_ES, cons.RADIO, 'Telecorazón', 'mms://video.ono.com/telecorazon?WMBitrate=512000'],
            ['70', co.es_ES, cons.RADIO, 'Antorva - Canal 1 - Cantabria', 'mms://antorvara.no-ip.info:8089/*'],
            # http://www.ciberdomainc03.com/tunein.php/w000987/playlist.asx
            ['71', co.es_ES, cons.RADIO, 'Radio Marca (Barcelona) 89.1 FM', 'http://87.106.252.110:8109/live'],
            # http://www.rac105.org/audio_directe/rac105.pls
            # http://www.rac105.org/audio_directe/rac105cd.pls
            # http://www.rac105.org/audio_directe/rac105.wmx
            # http://www.rac105.org/audio_directe/rac105.ram
            # http://212.48.125.98:80/
            ['72', co.es_ES, cons.RADIO, 'Rac 105 (Cataluña)', 'http://rs9.radiostreamer.com:9280/listen.pls'],
            # http://www.radioasturias.com/online/40_Principales_Asturias.asx
            ['73', co.es_ES, cons.RADIO, '40 Principales (Asturias)', 'mms://66.90.103.45/yaspe02'],
            # http://www.radiomarcatenerife.com/html/RadioWeb/radiomarcatenerife.m3u
            ['74', co.es_ES, cons.RADIO, 'Radio Marca Tenerife', 'http://servidor4.todoexitos.com:7120'],
            ['75', co.es_ES, cons.RADIO, 'Interpop Novelda', 'mms://www.intereconomia.com/DIRECTOINTERPOP'],
            ['76', co.es_ES, cons.RADIO, 'Loca FM Lugo', 'http://94.23.207.98:23500/;stream.nsv'],
            # http://www.radioasturias.com/online/Radio_Asturias_SER_FM.asx
            ['77', co.es_ES, cons.RADIO, 'Cadena SER FM', 'mms://66.90.103.45/yaspe01'],
            ['78', co.es_ES, cons.TV, 'Kabbalah TV Spanish', 'mms://s53wm.castup.net/991910010-52.wmv?ct=ES'],
            ['79', co.es_ES, cons.TV, 'Televisió de Girona', 'mms://a1326.l1536459325.c15364.g.lm.akamaistream.net/D/1326/15364/v0001/reflector:59325'],
            ['80', co.es_ES, cons.TV, 'Gandia Televisió', 'mms://mmedia01.connectate.com/str061'],
            ['81', co.es_ES, cons.TV, 'Nuevo Tiempo', 'mms://strm01.novotempo.org.br/TVNuevoTiempo-Vivo'],
            #http://www.crtvg.es/asfroot/television.asx
            ['82', co.es_ES, cons.RADIO, 'Radio Galega', 'mmsh://videor.mundo-r.com/RadioGalega'],
            ['83', co.es_ES, cons.RADIO, 'Radio Galega Música', 'mmsh://videor.mundo-r.com/radiomusica'],
            ['84', co.es_ES, cons.RADIO, 'Son Galicia', 'mmsh://videor.mundo-r.com/songalicia'],
            ['85', co.es_ES, cons.TV, 'Galicia TV', 'http://videor.mundo-r.com/TVG/tvg.asx'],
            ['86', co.es_ES, cons.RADIO, 'QFM 94.3', 'http://s1.viastreaming.net:7420/listen.pls'],
            # [FIXME] Needs a parser. URL dont work: http://www.antena6.com/antena6_adsl.m3u 
            ['87', co.es_ES, cons.RADIO, 'Antena 6 89.4 FM', 'http://62.93.185.48:8015'],

            ## United States ## 53
            ['88', co.en_US, cons.TV, 'Asian small-clawed Otters Cam', 'mms://160.111.143.151/ao'],
            ['89', co.en_US, cons.TV, 'Barn Owl Cam [California]', 'mms://puffin.audubon.org/wmtencoder/starrranchhumming.wmv'],
            ['90', co.en_US, cons.TV, 'Cheetah Cam', 'mms://NZPWMserver1.si.edu/cheetah1'],
            ['91', co.en_US, cons.TV, 'City of Tampa Television', 'mms://cttv.tampagov.net/cttv'],
            ['92', co.en_US, cons.TV, 'Coral Gables Television', 'mms://216.242.214.8/cocgtvlive'],
            ['93', co.en_US, cons.TV, 'CTNi', 'mms://169.130.151.126/ctni'], # CHRISTIAN TELEVISION NETWORK
            ['94', co.en_US, cons.TV, 'CTVN', 'mms://quickstudy.wmlive.internapcdn.net/live_quickstudy_vitalstream_com_cornerstoneTv'],
            ['95', co.en_US, cons.TV, 'e-Gov-DBTv', 'mms://stream.codb.us/ch99'],
            ['96', co.en_US, cons.TV, 'Ferret Cam', 'mms://NZPWMserver1.si.edu/bff'],
            ['97', co.en_US, cons.TV, 'Florida Beach Cam', 'mms://24.214.233.60/beach'],
            ['98', co.en_US, cons.TV, 'Golden Lion Tamarin Cam', 'mms://NZPWMserver1.si.edu/glt'],
            ['99', co.en_US, cons.TV, 'Gorilla Cam', 'mms://nzpmedia1.si.edu/gorilla'],
            ['100', co.en_US, cons.TV, 'Hog\'s Breath Saloon Cam', 'mms://floridakeysmedia.com/hogsbarcam'],
            ['101', co.en_US, cons.TV, 'Home Shopping Network', 'mms://wm-live.z1.mii-streaming.net/live/hsn/hsnlive'],
            ['102', co.en_US, cons.TV, 'Home Shopping Network [HSN]', 'mms://live.hsn.com/live/hsn/hsnlive'],
            ['103', co.en_US, cons.TV, 'Kiwi Chick Cam', 'mms://NZPWMserver1.si.edu/ke0ed0bc8c'],
            ['104', co.en_US, cons.TV, 'Lion Cam', 'mms://160.111.143.151/lion'],
            ['105', co.en_US, cons.TV, 'MicroTheatre Cam', 'mms://NZPWMserver1.si.edu/mt'],
            ['106', co.en_US, cons.TV, 'Octopus Cam', 'mms://NZPWMserver1.si.edu/octopus'],
            ['107', co.en_US, cons.TV, 'Olelo Focus 49 [Hawaii]', 'mms://207.7.154.95/olelo_focus?wmcache=0'],
            ['108', co.en_US, cons.TV, 'Olelo O\'AHU52 [Hawaii]', 'mms://207.7.154.95/olelo_oahu52?wmcache=0'],
            ['109', co.en_US, cons.TV, 'Olelo NATV 53 [Hawaii]', 'mms://207.7.154.95/olelo_natv?wmcache=0'], # DWTV
            ['110', co.en_US, cons.TV, 'Olelo View 54 [Hawaii]', 'mms://207.7.154.95/olelo_views54?wmcache=0'],
            ['111', co.en_US, cons.TV, 'Orange County TV [Florida]', 'mms://otv.ocfl.net/live'],
            ['112', co.en_US, cons.TV, 'Orangutan Cam', 'mms://NZPWMserver1.si.edu/thinktank'],
            ['113', co.en_US, cons.TV, 'Panama City Pool Cam', 'mms://24.214.233.60/poolwest'],
            ['114', co.en_US, cons.TV, 'Panda Cam', 'mms://160.111.253.227/pandacam1'],
            ['115', co.en_US, cons.TV, 'Panda Cam 2', 'mms://160.111.253.227/pandacam2'],
            ['116', co.en_US, cons.TV, 'Pool Cam', 'mms://24.214.233.60/pooleast'],
            ['117', co.en_US, cons.TV, 'Report on Business TV', 'mms://pbs.wmod.llnwd.net/a1863/e1/general/windows/nbr/nbr_160.wmv'],
            ['118', co.en_US, cons.TV, 'Roswell\'s Government Access TV', 'mms://roswell.ecstreams.com/RoswellLive'],
            ['119', co.en_US, cons.TV, 'Rutherford County Television [TV19 Rutherford Cnty., TN]', 'mms://media1.rutherfordcountytn.gov:1031/live'],
            ['120', co.en_US, cons.TV, 'SGTV [TV199 Seminole Cnty, FL]', 'mms://streaming.seminolecountyfl.gov/live'],
            ['121', co.en_US, cons.TV, 'Sloth Bears Cam', 'mms://160.111.143.151/sb2'],
            ['122', co.en_US, cons.TV, 'Spokane City Cam', 'mms://media.spokanecity.org/100k'],
            ['123', co.en_US, cons.TV, 'Talk Radio Studio Cam [Tennessee]', 'mms://media.americainter.net/wgowenc2'],
            ['124', co.en_US, cons.TV, 'Tele Restauración', 'mms://live1.christianvideochannel.com/jemir'],
            ['125', co.en_US, cons.TV, 'The Aqualand Cam', 'mms://24.214.233.60/waterpark'],
            ['126', co.en_US, cons.TV, 'The Network 125 Internet TV and Video Guide Channel', 'mms://channel125.com/guide'],
            ['127', co.en_US, cons.TV, 'The Online Piano Bar', 'mms://wn71.reliablehosting.com/customer54'],
            ['128', co.en_US, cons.TV, 'Thriller Classics TV', 'mms://85.214.87.175/thriller-tv/rtsp:/85.214.87.175/thriller-tv/rtsp:/85.214.87.175/thriller-tv/rtsp:/85.214.87.175/thriller-tv/video'],
            ['129', co.en_US, cons.TV, 'Tiger Cam', 'mms://nzpmedia1.si.edu/tiger1'],
            ['130', co.en_US, cons.TV, 'TV Knob Movies', 'mms://streams.tvknob.com/tvloops/CH7/tvknob.wsx'],
            ['131', co.en_US, cons.TV, 'TV Marti', 'mms://a165.1211035484.c2110.g.lm.akamaistream.net/D/165/2110/v0001/reflector:35484'],
            ['132', co.en_US, cons.TV, 'Twelve TV', 'mms://a986.l2602438985.c26024.n.lm.akamaistream.net/D/986/26024/v0001/reflector:38985'],
            ['133', co.en_US, cons.TV, 'University of Virginia', 'mms://VIDEO1.itc.virginia.edu/RotundaCam'],
            ['134', co.en_US, cons.TV, 'Wilderness Waterpark', 'mms://66.135.44.65/Wilderness1'],
            ['135', co.en_US, cons.TV, 'WLOX [ABC13 Gulfport/Biloxi, MS]', 'mms://a501.l5671342500.c56713.n.lm.akamaistream.net/D/501/56713/v0001/reflector:42500'],
            ['136', co.en_US, cons.TV, 'Yellowstone Geyser Cam', 'mms://a293.l2717654292.c27176.g.lm.akamaistream.net/D/293/27176/v0001/reflector:54292'],
            ['137', co.en_US, cons.TV, 'Mobile NBC', 'mms://msnbc.wmod.llnwd.net/a275/e1/video/100/vh.asf'],
            # http://scfire-ntc-aa03.stream.aol.com:80/stream/1007
            ['138', co.en_US, cons.RADIO, 'DI FM - House (PLS)', 'http://www.di.fm/mp3/house.pls'],
            #[FIXME] http://www.di.fm/wma/house.asx # Needs a parser for variable stream!
            ['139', co.en_US, cons.RADIO, 'DI FM - House (WMA)', 'mms://wstream5e.di.fm/house'],
            ['140', co.en_US, cons.RADIO, 'DI FM - Deep House (PLS)', 'http://www.di.fm/mp3/deephouse.pls'],
            #[FIXME] http://www.di.fm/wma/deephouse.asx # Needs a parser for variable stream!
            ['141', co.en_US, cons.RADIO, 'DI FM - Deep House (WMA)', 'mms://wstream5e.di.fm/deephouse'],
            ['142', co.en_US, cons.RADIO, 'DI FM - Trance (PLS)', 'http://www.di.fm/mp3/trance.pls'],
            #[FIXME] http://www.di.fm/wma/trance.asx # Needs a parser for variable stream!
            ['143', co.en_US, cons.RADIO, 'DI FM - Trance (WMA)', 'mms://wstream5e.di.fm/trance'],
            ['144', co.en_US, cons.RADIO, 'DI FM - Chillout (PLS)', 'http://www.di.fm/mp3/chillout.pls'],
            #[FIXME] http://www.di.fm/wma/chillout.asx # Needs a parser for variable stream!
            ['145', co.en_US, cons.RADIO, 'DI FM - Chillout (WMA)', 'mms://wstream5e.di.fm/chillout'],
            ['146', co.en_US, cons.RADIO, 'Only house music radio (PLS)', 'http://87.117.250.3:9130/listen.pls'],
            ['147', co.en_US, cons.RADIO, 'Only house music radio (ASX)', 'http://87.117.250.3:9130'],
            #http://www.streamsolutions.co.uk/launch/?server=87.117.250.3&port=9130&type=Shoutcast&file=asx
            ['148', co.en_US, cons.RADIO, 'Ancient Faith RADIO', 'http://s2.viastreaming.net:7080/listen.pls', cons.PLS], 
            # http://208.53.158.48:8250
            ['149', co.en_US, cons.RADIO, '100 XR', 'http://100xr-play.redirectme.net/100xr.asx', cons.ASX],
            
            ## United Kingdom ## 55
            # [BROKEN-INVALID]['54', co.en_GB, cons.TV, 'BBC 1', 'FILMON14'], # --crop=16:10 --aspect-ratio=16:9
            #  http://79.125.47.119/bbc1?auth=65d976cc5ac7b78f5e9b098df927d5aa
            # [BROKEN-INVALID]['55', co.en_GB, cons.TV, 'BBC 1 LoSp', 'FILMON35'], # --crop=16:10 --aspect-ratio=16:9
            #  http://79.125.47.119/bbc1_ls?auth=7f9d5be762f9ae3951a169aeff2a627d
            # [BROKEN-INVALID]['56', co.en_GB, cons.TV, 'BBC 2', 'FILMON25'], # --crop=16:10 --aspect-ratio=16:9
            # 'http://79.125.47.119/bbc2_ls?auth=869b841670c28fe91747e5ba1af7ed13'
            # [BROKEN-INVALID]['41', co.en_GB, cons.TV, 'BBC 2 LoSp', 'FILMON55'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/bbc2_ls?auth=52367436cf413623dd9af0b6254014a4
            # [BROKEN-INVALID]['42', co.en_GB, cons.TV, 'ITV 1', 'FILMON11'], # --crop=16:10 --aspect-ratio=16:9
            #'http://79.125.47.119/itv1?auth=763fe6374a384237bf7041afbef79f47'
            # [BROKEN-INVALID]['43', co.en_GB, cons.TV, 'ITV 1 LoSp', 'FILMON42'], # --crop=16:10 --aspect-ratio=16:9
            #'http://79.125.47.119/itv1_ls?auth=12586d8556b09487ffd4a18e75467df9'
            # [BROKEN-INVALID]['44', co.en_GB, cons.TV, 'Channel 4', 'FILMON02'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/channel4?auth=884aaedf2e47829fc9d9e3cb97581280
            # [BROKEN-INVALID]['45', co.en_GB, cons.TV, 'Channel 4 LoSp', 'FILMON36'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/channel4_ls?auth=0169247e35e8343699e1b6909da0ee73
            # [BROKEN-INVALID]['46', co.en_GB, cons.TV, 'Channel 5', 'FILMON22'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/five?auth=ae578cb33b1e7881bc1f66f4cfcedc61
            # [BROKEN-INVALID]['47', co.en_GB, cons.TV, 'Channel 5 LoSp', 'FILMON52'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/five_ls?auth=2a9328f4a7f1deb11ce73083892bd7db
            # ['X', en_GB, 'ITV 2', 'mms://itvbrdbnd-itv2.wm.llnwd.net/itvbrdbnd_itv2?h=eb85fd5ceb888cfff1630b7b6d02dc06i'], # --crop=16:10 --aspect-ratio=16:9 Not available
            #['X', en_GB, 'ITV 3', 'mms://itvbrdbnd-itv3.wm.llnwd.net/itvbrdbnd_itv3?h=0b73cc338e26a65c89b769771e89525c'], # --crop=16:10 --aspect-ratio=16:9 Not available
            ['150', co.en_GB, cons.TV, 'ITV 4', 'mms://itvbrdbnd-itv4.wm.llnwd.net/itvbrdbnd_itv4?h=68c827f6e0551016d50c30c4b2ad01ae'], # --crop=16:10 --aspect-ratio=16:9
            # [BROKEN-INVALID]['49', co.en_GB, cons.TV, 'Film 4', 'FILMON13'], # --crop=16:10 --aspect-ratio=4:3
            # http://79.125.47.119/film4?auth=39f83649a5d4183d0781650be1cd3736
            # [BROKEN-INVALID]['50', co.en_GB, cons.TV, 'Film 4 LoSp', 'FILMON44'], # --crop=16:10 --aspect-ratio=4:3
            # http://79.125.47.119/film4_ls?auth=2a7c131dc3d1eabe87b6d0ba6df1a16a
            # [BROKEN-INVALID]['51', co.en_GB, cons.TV, 'Zone Horror', 'FILMON19'], # --crop=4:3 --aspect-ratio=4:3
            # http://79.125.47.119/zone_horror?auth=a79c3a89e7a8f6626f9ef1ba45b081a0
            # [BROKEN-INVALID]['52', co.en_GB, cons.TV, 'Zone Horror LoSp', 'FILMON49'], # --crop=4:3 --aspect-ratio=4:3
            # http://79.125.47.119/zone_horror_ls?auth=611d1e387ac48836032be6c01dc645fc
            # [BROKEN-INVALID]['53', co.en_GB, cons.TV, 'BBC XTRAS', 'FILMON26'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/sky-news?auth=73670c3416a48504246044bfaa5764d6
            # [BROKEN-INVALID]['54', co.en_GB, cons.TV, 'BBC XTRAS LoSp', 'FILMON56'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/sky-news_ls?auth=ca28e8bb47918a24f598072d7421907a
            # [BROKEN-INVALID]['55', co.en_GB, cons.TV, 'Eurosport 2', 'FILMON89'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/eurosport2?auth=bab68097441146e5a4f1fe33fdaa731f
            # [BROKEN-INVALID]['56', co.en_GB, cons.TV, 'Eurosport 2 LoSp', 'FILMON90'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/eurosport2_ls?auth=041048e5b94a42f61ba10eca4df96cda
            ##FIXME['30', en_GB, 'Eurosport News', 'http://player.eurosport.fr/playlist.aspx?mode=live&id=6'], # --crop=16:10 --aspect-ratio=16:9
            # [BROKEN-INVALID]['57', co.en_GB, cons.TV, 'Scuzz', 'FILMON59'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/scuzz?auth=7d6c9c00ef842d26b9d53b83950e71c5
            # [BROKEN-INVALID]['58', co.en_GB, cons.TV, 'Scuzz LoSp', 'FILMON61'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/scuzz_ls?auth=1bf0542b1cabd7339718050fbbc3936f
            # [BROKEN-INVALID]['59', co.en_GB, cons.TV, 'Flaunt', 'FILMON60'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/flaunt?auth=2ce5ca0be6ce68a363afed6716080846
            # [BROKEN-INVALID]['60', co.en_GB, cons.TV, 'Flaunt LoSp', 'FILMON58'], # --crop=16:10 --aspect-ratio=16:9
            # http://79.125.47.119/flaunt_ls?auth=6dea9bb7097578d0315e50128e1cfb91
            # [BROKEN-INVALID]['61', co.en_GB, cons.TV, 'Fashion TV', 'FILMON24'], # --crop=16:10 --aspect-ratio=4:3 
            # http://79.125.47.119/fashion_tv?auth=e0d5e3b048008a1012259b111a63df10
            # [BROKEN-INVALID]['62', co.en_GB, cons.TV, 'Fashion TV LoSp', 'FILMON54'], # --crop=16:10 --aspect-ratio=4:3 
            # http://79.125.47.119/fashion_tv_ls?auth=609c1025da6ea743b8709fdef0f8b022
            ['151', co.en_GB, cons.TV, 'BBC Click', 'mms://rmv8.bbc.net.uk/news/olmedia/n5ctrl/tvseq/od/bbc1/bb/wm/video/click_bb.wmv'],
            ['152', co.en_GB, cons.TV, 'BBC Daily Politics', 'mms://rmv8.bbc.net.uk/news/olmedia/n5ctrl/tvseq/od/bbc2/bb/wm/video/daily_pol_bb.wmv'],
            ['153', co.en_GB, cons.TV, 'BBC Panorama', 'mms://rmv8.bbc.net.uk/news/olmedia/n5ctrl/tvseq/od/bbc1/bb/wm/video/panorama_bb.wmv'],
            ['154', co.en_GB, cons.TV, 'BBC Question Time', 'mms://rmv8.bbc.net.uk/news/olmedia/n5ctrl/tvseq/od/bbc1/bb/wm/video/question_bb.wmv'],
            ['155', co.en_GB, cons.TV, 'BBC News 24H', 'http://www.bbc.co.uk/newsa/n5ctrl/tvseq/od/bbc2/nb/wm/video/newsnight_nb.asx'],
            ['156', co.en_GB, cons.TV, 'BBC Newsnight', 'mms://rmv8.bbc.net.uk/news/olmedia/n5ctrl/tvseq/od/bbc2/bb/wm/video/newsnight_bb.wmv'], # Maybe repeat
            ['157', co.en_GB, cons.TV, 'Invincible', 'mms://wm.Astream.net/urban'],
            ['158', co.en_GB, cons.TV, 'MTA 3 Al Arabiyah', 'mms://212.199.206.17/mta-high'],
            ['159', co.en_GB, cons.TV, 'MTA Muslim TV', 'mms://live300k1.wm.muslimtv.servecast.net/MuslimTV_wmlz_live300ken'],
            ['160', co.en_GB, cons.TV, 'QVC', 'mms://a1899.l3277436467.c32774.e.lm.akamaistream.net/D/1899/32774/v0001/reflector:36467'], # --crop=16:9 --aspect-ratio=16:9
            ['161', co.en_GB, cons.TV, 'Sky News', 'mms://live1.wm.skynews.servecast.net/skynews_wmlz_live300k'],
            ['162', co.en_GB, cons.TV, 'TFM Music', 'mms://85.119.217.29/TMFLive'],
            ['163', co.en_GB, cons.TV, 'Eurosport 1 HD', 'mms://195.90.118.25/eurosport1_1'],
            ['164', co.en_GB, cons.TV, 'Eurosport 2 HD', 'mms://195.90.118.25/eurosport2_1'],
            ['165', co.en_GB, cons.TV, 'e4', 'mms://195.90.118.25/e4_1'],
            ['166', co.en_GB, cons.TV, 'BBC 1 HD', 'mms://195.90.118.25/bbc1_1'],
            ['167', co.en_GB, cons.TV, 'Streetclip Tv', 'mms://streetclip.tv:1234/'],
            ['168', co.en_GB, cons.TV, 'Glasgow University Chapel Cam (UK)', 'mms://commsvs1.cent.gla.ac.uk/chapel'], 
            ['169', co.en_GB, cons.TV, 'Glasgow University Chapel Cam (UK)', 'mms://commsvs1.cent.gla.ac.uk/chapel'], 
            ['170', co.en_GB, cons.TV, 'Holiday TV (UK)', 'mms://server3.i2ic.com/iv?channel=16&bandwidth=4&token=fjuncfzJRxmP'], 
            ['171', co.en_GB, cons.TV, 'MTA 3 Int (UK)', 'mms://212.199.206.17/mta-high'], 
            ['172', co.en_GB, cons.TV, 'GAME NEWS TV', 'mms://a1191.v165449.c16544.g.vm.akamaistream.net/7/1191/16544/v001/roomediaco1.download.akamai.com/16544/wm.roomedia/902/902615_300.wmv?clipId=902615'], 
            ['173', co.en_GB, cons.TV, 'ACCESS SACRAMENTO', 'http://live.upstreamnetworks.com/15834-33555'], 
            ['174', co.en_GB, cons.TV, 'BOARDRIDERS TV', 'mms://quik4.impek.tv/brtv'], 
            ['175', co.en_GB, cons.TV, 'GEMS TV', 'mms://live.gemstv.co.uk/GemsTV'], 
            ['176', co.en_GB, cons.TV, 'SFGTV', 'mms://207.7.154.95/sanfrancisco_encoder2'], 
            ['177', co.en_GB, cons.TV, 'SUPREME MASTER', 'mms://smtv.godsdirectcontact.net/la_300k'], 
            ['178', co.en_GB, cons.RADIO, 'MATCHBOX RADIO 24 (slow)', 'http://www.live365.com/cgi-bin/play.pls?stationid=293185'], 
            ['179', co.en_GB, cons.RADIO, 'SIREN FM (slow)', 'http://www.live365.com/cgi-bin/play.pls?stationid=288238'], 
            ['180', co.en_GB, cons.RADIO, 'THE HUB', 'rtsp://real.uwe.ac.uk/live/thehub'], 
            ['181', co.en_GB, cons.RADIO, 'So you!', 'http://so-you.eu:8000/listen.pls'], 
            ['182', co.en_GB, cons.TV, 'freetalk', 'mms://209.90.224.6/SCANLive'], 
            ['183', co.en_GB, cons.TV, 'SCCTV BROADBAND', 'mms://media.scctv.net/SCCtv%20Broadband'], 

            ## France ## 32
            ['184', co.fr_FR, cons.TV, 'Tele night', 'mms://195.95.225.110/telenight'],
            ['185', co.fr_FR, cons.TV, 'nrj Paris', 'mms://vipnrj.yacast.net/nrj_tvparis'],
            ['186', co.fr_FR, cons.TV, 'CityZen TV', 'http://movix.sdv.fr:8086/cityzen.asf'],
            ['187', co.fr_FR, cons.TV, 'France 24 French', 'mms://stream1.france24.yacast.net/f24_livefr'],
            ['188', co.fr_FR, cons.TV, 'France 24 English', 'mms://stream1.france24.yacast.net/f24_liveen'],
            ['189', co.fr_FR, cons.TV, 'France 24 Arabic', 'mms://stream1.france24.yacast.net/f24_livefrda'],
            ['190', co.fr_FR, cons.TV, 'France 2 - La Météo', 'mms://a988.v101995.c10199.e.vm.akamaistream.net/7/988/10199/3f97c7e6/ftvigrp.download.akamai.com/10199/horsgv/regions/siege/france2/meteo/meteo_GT.wmv'],
            ['191', co.fr_FR, cons.TV, 'IDF1', 'mms://live240.impek.com/idf1'],
            ['192', co.fr_FR, cons.TV, 'LaLocale TV', 'mms://stream.lalocale.com/lalocale'],
            ['193', co.fr_FR, cons.TV, 'LCP - Assemblée nationale', 'mms://vipmms9.yacast.net/rcs_lcplive?WMThinning=0'],
            ['194', co.fr_FR, cons.TV, 'MBOA TV', 'mms://88.191.23.167/mboatv'],
            ['195', co.fr_FR, cons.TV, 'Netgaming TV', 'mms://88.191.89.94/netgamingtv'],
            ['196', co.fr_FR, cons.TV, 'Orange Sport', 'mms://livewm.orange.fr/live-multicanaux'],
            ['197', co.fr_FR, cons.TV, 'TLM', 'mms://91.121.38.105/tlm'],
            ['198', co.fr_FR, cons.TV, 'TSF Network', 'mms://stream.tvsf.fr/live'],
            ['199', co.fr_FR, cons.TV, 'TV Grenoble', 'http://movix.sdv.fr:8084/teleg1.asf'],
            ['200', co.fr_FR, cons.TV, 'TV8 Moselle-Est', 'mms://live.tv8.fr/tv'],
            ['201', co.fr_FR, cons.TV, 'WEO TV', 'mms://91.121.188.214/weopub'],
            ['202', co.fr_FR, cons.TV, 'FR BFM TV EN DIRECT', 'mms://vipmms9.yacast.net/bfm_bfmtv'],
            ['203', co.fr_FR, cons.TV, 'CALAIS TV', 'mms://91.121.2.60/calaistv'],
            ['204', co.fr_FR, cons.TV, 'CANAL SAVOIR', 'mms://stream2.canal.qc.ca/enOndes_bas_debit'],
            ['205', co.fr_FR, cons.TV, 'CAP 24', 'mms://wm.live.tv-radio.com/cap24_360k'],
            ['206', co.fr_FR, cons.TV, 'CT2E', 'http://www.ct2e.com/live.wmv'],
            ['207', co.fr_FR, cons.TV, 'IRANCI', 'mms://live210.impek.com/inraci'],
            ['208', co.fr_FR, cons.TV, 'LABELLE TV', 'mms://www.labelletv.net/labelleTV'],
            ['209', co.fr_FR, cons.TV, 'MULIVAN TV', 'mms://mulivan.diffusepro.com/mulivantv'],
            ['210', co.fr_FR, cons.TV, 'NRJ HITS (slow)', 'mms://vipnrj.yacast.net/nrj_tvhit'],
            ['211', co.fr_FR, cons.TV, 'NRJ DANCE', 'mms://vipnrj.yacast.net/nrj_webtv02'],
            ['212', co.fr_FR, cons.TV, 'TELE 102', 'mms://www.tele102.net/tele102'],
            ['213', co.fr_FR, cons.RADIO, 'RADIO SING SING (slow)', 'http://www.sing-sing.org/confort2.pls'],
            ['214', co.fr_FR, cons.TV, 'Kabbalah TV Francais', 'mms://vod.kab.tv/fre'],
            ['215', co.fr_FR, cons.TV, 'CLAP TV', 'mms://rr93.diffusepro.com/rr93'],
            ['216', co.fr_FR, cons.RADIO, 'Alouette 92.8 FM', 'http://ns57.ovh.net:80/listen.pls', cons.PLS],
            ['698', co.fr_FR, cons.RADIO, 'Z-103.5', 'http://38.100.101.69/CIDCFMAAC'],
            
            ## Italy ## 74
            #mms://151.1.245.36/rtl102.5vs
            ['217', co.it_IT, cons.TV, 'RTL', 'mms://windowsmedia.rtl.it/rtl102.5vs/'],
            ['218', co.it_IT, cons.TV, 'Canale 7', 'mms://151.1.245.65/CANALE7'],
            ['219', co.it_IT, cons.TV, 'CBL Film', 'mms://151.1.245.71/cblfilm-live'],
            ['220', co.it_IT, cons.TV, 'Cinquestelle TV', 'mms://iptv.telecard.it/Cinquestelle'],
            ['221', co.it_IT, cons.TV, 'ETV (Bologna)', 'mms://streaming.e-tv.it/etvsatellite'],
            ['222', co.it_IT, cons.TV, 'Idea TV', 'mms://streaming1.bsnewline.com/ideatv'],
            ['223', co.it_IT, cons.TV, 'LA8 Romagna', 'mms://iptv.telecard.it/LA8ER_LQ'],
            ['224', co.it_IT, cons.TV, 'Piu Blu', 'mms://151.1.245.65/unitedcom-v'], # Lombardia
            ['225', co.it_IT, cons.TV, 'Primocanale', 'mms://iptv.primocanale.it/diretta'],
            ['226', co.it_IT, cons.TV, 'Rai 3', 'mms://a1509.l6934735508.c69347.e.lm.akamaistream.net/D/1509/69347/v0001/reflector:45832'],
            ['227', co.it_IT, cons.TV, 'TV Oggi', 'http://85.18.170.70:8080'],
            ['228', co.it_IT, cons.TV, 'TRG', 'mms://212.104.10.35/TRG'],
            ['229', co.it_IT, cons.TV, 'Telesud TV', 'http://www.palermoweb.net/videostream/tvnews/tvnews.wmv'],
            ['230', co.it_IT, cons.TV, 'Teleradioerre', 'mms://www.teleradioerre.com/Teleradioerre'],
            ['231', co.it_IT, cons.TV, 'Sport Italia (slow)', 'mms://mms.cdn-tiscali.com/sportitalia'],
            ['232', co.it_IT, cons.TV, 'Sat2000 (Vatican)', 'mms://62.101.89.122/Sat2000'],
            ['233', co.it_IT, cons.TV, 'RTV 38', 'mms://streaming.intoscana.it/wmtencoder/rtv38.wmv'],
            ['234', co.it_IT, cons.TV, 'Retesole Perugia', 'mms://212.48.126.114/retesoleperugia'],
            ['235', co.it_IT, cons.TV, '3 channel', 'mms://84.233.254.2/3Channel'],
            ['236', co.it_IT, cons.TV, 'Antenna 6', 'mms://81.25.97.50/antenna6'],
            ['237', co.it_IT, cons.TV, 'Carpe Diem', 'mms://iptv.telecard.it/carpediem'],
            ['238', co.it_IT, cons.TV, 'Florence TV', 'http://www.florence.tv/playlist.aspx?v=135'],
            ['239', co.it_IT, cons.TV, 'In cucina TV', 'http://media.mi.interact.it/INTV_Incucina_Hi'],
            ['240', co.it_IT, cons.TV, 'LA8', 'mms://iptv.telecard.it/LA8VE_LQ'],
            ['241', co.it_IT, cons.TV, 'Meteo.it', 'http://media.meteo.it/TGItaBL.wmv'],
            ['242', co.it_IT, cons.TV, 'Repubblica TV', 'http://live.mediaserver.kataweb.it/repubblicaradiotv'],
            ['243', co.it_IT, cons.TV, 'Studio 100 SAT', 'mms://iptv.telecard.it/Studio100'],
            ['244', co.it_IT, cons.TV, 'Tele Molise', 'mms://wmlive.telemolise.com/multicast_stream2'],
            ['245', co.it_IT, cons.TV, 'Teletruria', 'mms://83.147.65.2/TeletruriaLive'],
            ['246', co.it_IT, cons.TV, 'Retequattro', 'mms://live.mediashopping.it/enc1-c3'],
            ['247', co.it_IT, cons.TV, 'Italia 1', 'mms://live.mediashopping.it/enc1-c2'],
            ['248', co.it_IT, cons.TV, 'Canale 5', 'mms://live.mediashopping.it/enc1-c1'],
            ['249', co.it_IT, cons.TV, 'Vive TV', 'mms://streaming3.arcoiris.tv/vive-adsl'],
            ['250', co.it_IT, cons.TV, 'Videolina', 'mms://91.121.222.160/videolina'],
            ['251', co.it_IT, cons.TV, 'Rock Television', 'mms://194.116.83.15/New'],
            # Maybe this channels works with a proxy o similar trick for outside of Italy
            ['252', co.it_IT, cons.RADIO, 'Raiuno (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=983', cons.ASX],
            ['253', co.it_IT, cons.RADIO, 'Raidue (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=984', cons.ASX],
            ['254', co.it_IT, cons.RADIO, 'Raitre (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=986', cons.ASX],
            ['255', co.it_IT, cons.RADIO, 'Raiquattro (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=75708', cons.ASX],
            ['256', co.it_IT, cons.RADIO, 'Rainews24 (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=1', cons.ASX],
            ['257', co.it_IT, cons.RADIO, 'Raisport (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=4145', cons.ASX],
            ['258', co.it_IT, cons.RADIO, 'Raistoria (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=24269', cons.ASX],
            ['259', co.it_IT, cons.RADIO, 'Raiedu (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=24268', cons.ASX],
            ['260', co.it_IT, cons.RADIO, 'Rai sat cinema (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72381', cons.ASX],
            ['261', co.it_IT, cons.RADIO, 'Rai sat extra (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72382', cons.ASX],
            ['262', co.it_IT, cons.RADIO, 'Rai sat premium (Italy only)', 'http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72916', cons.ASX],
            ['263', co.it_IT, cons.RADIO, 'Radio Blu', 'http://live2.streamingmedia.it/blu'],
            ['264', co.it_IT, cons.RADIO, 'RTL 102.5 Hit Channel', 'mms://151.1.245.36/rtl102.5vs/'],
            ['265', co.it_IT, cons.RADIO, 'GNUfunk Radio', 'http://gnufunk.org/radio/playlist.pls'],
            ['266', co.it_IT, cons.RADIO, 'Controradio', 'http://streaming.controradio.emmi.it:8190/'],
            ['267', co.it_IT, cons.RADIO, 'Radio 105', 'mms://151.1.245.6/1'],
            ['268', co.it_IT, cons.RADIO, 'Radio Uno (slow)', 'rtsp://live.media.rai.it/broadcast/radiouno.rm'],
            ['269', co.it_IT, cons.RADIO, 'Radio due (slow)', 'rtsp://live.media.rai.it/broadcast/radiodue.rm'],
            ['270', co.it_IT, cons.RADIO, 'Radio Tre (slow)', 'rtsp://live.media.rai.it/broadcast/radiotre.rm'],
            ['271', co.it_IT, cons.RADIO, 'Radio Deejay', 'mms://live.mediaserver.kataweb.it/radiodeejay?MSWMext=.asf'],
            ['272', co.it_IT, cons.RADIO, 'RTL 102.5', 'mms://151.1.245.36/rtl102.5lq/'],
            ['273', co.it_IT, cons.RADIO, 'RDS live streamingG', 'mms://fastreal.fastweb.it/RDS'],
            ['274', co.it_IT, cons.RADIO, 'Radio Gamma', 'http://live.wm.p1.str3.com/000999_bc_a365_radiogamma_mi'],
            ['275', co.it_IT, cons.RADIO, 'Nostalgia', 'mms://www.nostalgia.it/nostalgia'],
            ['276', co.it_IT, cons.RADIO, 'Radio Onda Rossa', 'http://radio.dyne.org:8000/ondarossa.mp3'],
            ['277', co.it_IT, cons.RADIO, 'Radio Blackout', 'http://stream.teknusi.org:8000/blackout.mp3'],
            ['278', co.it_IT, cons.RADIO, 'Radio Sherwood', 'http://62.101.68.185:8000/sherwood.ogg'],
            ['279', co.it_IT, cons.RADIO, 'Virgin radio', 'mmsh://151.1.245.1/20?MSWMExt=.asf'],
            ['280', co.it_IT, cons.RADIO, 'Virgin rock classico', 'mms://151.1.245.1/24'],
            ['281', co.it_IT, cons.RADIO, 'Virgin rock extreme', 'mms://151.1.245.1/25'],
            ['282', co.it_IT, cons.RADIO, 'Virgin rock alternative', 'mms://151.1.245.1/36'],
            ['283', co.it_IT, cons.RADIO, 'Virgin revolver', 'mms://151.1.245.1/34'],
            ['284', co.it_IT, cons.RADIO, 'Radio Capital', 'mms://live.mediaserver.kataweb.it/capital?MSWMExt=.asf'],
            ['285', co.it_IT, cons.RADIO, 'Radio Catania', 'mmsh://ams01.egihosting.com/584936/?MSWMExt=.asf'],
            ['286', co.it_IT, cons.RADIO, 'Radio Ciccio Riccio', 'mms://ciccioriccio.e20live.com/ciccioriccio'],
            ['287', co.it_IT, cons.RADIO, 'Radio Fiesole', 'http://83.103.40.204:8000/fiesole100.ogg'],
            ['288', co.it_IT, cons.RADIO, 'Radio Monte Carlo 1', 'mms://151.1.245.1/2'],
            ['289', co.it_IT, cons.RADIO, 'Radio Monte Carlo Film', 'mms://151.1.245.1/12'],
            ['290', co.it_IT, cons.RADIO, 'Radio Monte Carlo Great Artist', 'mms://151.1.245.1/6'],
            ['291', co.it_IT, cons.RADIO, 'Radio Monte Carlo Italia', 'mms://151.1.245.1/18'],
            ['292', co.it_IT, cons.RADIO, 'Radio Monte Carlo Marine', 'mms://151.1.245.1/26'],
            ['293', co.it_IT, cons.RADIO, 'Radio Monte Carlo The best', 'mms://151.1.245.1/15'],
            ['294', co.it_IT, cons.RADIO, 'Radio Napoli Doc', 'http://str30.creacast.com:80/radio_napolidoc'],
            ['295', co.it_IT, cons.RADIO, 'Radio Norba', 'http://onair1.xdevel.com/RadioNorba_32'],
            ['296', co.it_IT, cons.RADIO, 'Radio Radicale', 'http://livemp3.radioradicale.it/live.mp3'],
            ['297', co.it_IT, cons.RADIO, 'Rai Filodiffusione 4 (slow)', 'rtsp://live.media.rai.it/broadcast/fd4.rm'],
            ['298', co.it_IT, cons.RADIO, 'Rai Filodiffusione 5 (slow)', 'rtsp://live.media.rai.it/broadcast/fd5.rm'],
            ['299', co.it_IT, cons.RADIO, 'Rai GR parlamento (slow)', 'rtsp://live.media.rai.it/broadcast/grparlamento.rm'],
            ['300', co.it_IT, cons.RADIO, 'Rai Iso  (slow)', 'rtsp://live.media.rai.it/broadcast/isoradio.rm'],
            ['301', co.it_IT, cons.RADIO, 'Rai Satel (slow)', 'rtsp://live.media.rai.it/broadcast/italica.rm'],  
            ['302', co.it_IT, cons.RADIO, 'Radio Rock FM', 'http://str30.creacast.com/r101_thema5'],
            ['303', co.it_IT, cons.RADIO, 'Radio Siena', 'mmsh://energy10.egihosting.com/776344?MSWMExt=.asf'],
            ['304', co.it_IT, cons.RADIO, 'Radio Sorriso', 'http://212.103.197.217:8000/sorrriso_live'],
            ['305', co.it_IT, cons.RADIO, 'Radio Sound 95', 'mmsh://rs2.radiostreamer.com/RadioSound95.it?MSWMExt=.asf'],
            ['306', co.it_IT, cons.RADIO, 'Radio Umbria Radio', 'mms://212.48.126.114/umbria_radio'],
            ['307', co.it_IT, cons.RADIO, 'Radio Vaticana Rete 2', 'mms://212.77.1.198/rete2'],
            ['308', co.it_IT, cons.RADIO, 'Radio Maria', 'mms://streaming1.eu.radiomaria.org/Italy'],
            ['309', co.it_IT, cons.TV, 'Kabbalah TV Italian', 'mms://vod.kab.tv/ita'],
            
            ## Argentina ## 18
            ['310', co.ar_AR, cons.TV, 'Canal 7', 'mms://canal7envivo.telecomdatacenter.com.ar/canal7envivo'],
            # http://www.tn.com.ar/vivo/metafile.asx
            ['311', co.ar_AR, cons.TV, 'Canal 10 SRT - TN Television', 'mms://streamtn.uigc.net/TN'], # Todo Noticias
            ['312', co.ar_AR, cons.TV, 'Canal 11 - Paraná', 'mms://stream01.siglocero.net/canal11parana'],
            ['313', co.ar_AR, cons.TV, 'Canal 26', 'mms://200.115.194.1/Canal26?MSWMExt=.asf'],
            # http://200.115.194.1:8080/Canal26 
            ['314', co.ar_AR, cons.TV, 'Canal 13 - Vivo', 'mms://canal13.uigc.net/canal13vivo'],
            ['315', co.ar_AR, cons.TV, 'Canal 13 - Buenos Aires', 'http://www.telediariodigital.com.ar/video_/td.wmv'],
            # http://200.69.143.214/video_/td.wmv
            ['316', co.ar_AR, cons.TV, 'Canal Luz Satelite', 'mms://canalluz.telecomdatacenter.com.ar/canalluz/'],
            ['317', co.ar_AR, cons.TV, 'Plan Dj - Nueva imagen', 'mms://74.208.78.187/nuevaimagen'],
            ['318', co.ar_AR, cons.TV, 'La Red', 'mms://stream1.interrogacaodigital.net/tucumantv2'],
            ['319', co.ar_AR, cons.TV, 'Canal 5 Tucuman', 'mms://lared.wms.sinectis.com.ar/laredam910'],
            ['320', co.ar_AR, cons.TV, 'EduHard','mms://200.123.147.39:1029'],
            # http://www.alsolnet.com/stream/zona31/vivo.asx
            ['321', co.ar_AR, cons.TV, 'Zona 31','mms://streamair.alsolnet.com/zona31'],
            # http://www.alsolnet.com/stream/puerto2607/vivo.asx
            ['322', co.ar_AR, cons.TV, 'Argentinisima satelital', 'mms://streamair.alsolnet.com/puerto2607'],
            ['323', co.ar_AR, cons.RADIO, '89.1 Radio Mix', 'http://wmserver2.aginet.com.ar/FMPALERMO3'],
            ['324', co.ar_AR, cons.RADIO, 'Activa 91.9 FM', 'http://63.247.80.34:18020/listen.pls', cons.PLS],
            ['325', co.ar_AR, cons.RADIO, '97.5 Vale', 'http://200.43.193.143/vale/.wma'],
            ['326', co.ar_AR, cons.RADIO, '98.3 La Mega', 'http://mega.telecomdatacenter.com.ar/mega/.wma'],
            ['327', co.ar_AR, cons.RADIO, '99.5 Radio Palermo', 'http://wmserver3.aginet.com.ar/FMPALERMO1/.wma'],
            ['328', co.ar_AR, cons.RADIO, '101.5 Pop', 'http://pop.telecomdatacenter.com.ar/pop/.wma'],
            ['329', co.ar_AR, cons.RADIO, '103.7 Amadeus', 'http://amadeus.telecomdatacenter.com.ar/amadeus/.wma'],
            ['330', co.ar_AR, cons.RADIO, '105.5 FM Hit', 'http://66.175.96.10/ARLOS40P/.wma'],
            
            ## Hungary ## 13
            ['331', co.hu_HU, cons.TV, 'Budapest 13', 'mms://media.bp13.hu/TV13'],
            ['332', co.hu_HU, cons.TV, 'Digi TV', 'http://193.110.59.95:8080'],
            ['333', co.hu_HU, cons.TV, 'Supra TV', 'mms://stream01.gtk.hu/Supra_boglar_tv'],
            ['334', co.hu_HU, cons.TV, 'TV 8', 'mms://adas.pixeltv.hu/tv8'],
            ['335', co.hu_HU, cons.TV, 'T1 TV (slow)', 'mms://stream02.gtk.hu/torokszentmiklos_tv'],
            ['336', co.hu_HU, cons.TV, 'SzuperNet Feher', 'mms://live2.szupernet.tv/feher90'],
            ['337', co.hu_HU, cons.TV, 'SIO TV slow)', 'mms://stream02.gtk.hu/sio_tv'],
            ['338', co.hu_HU, cons.TV, 'REVITA TELEVIZIO', 'mms://stream01.gtk.hu/revita_tv'],
            ['339', co.hu_HU, cons.TV, 'MELITTA TV', 'mms://stream01.gtk.hu/gil'],
            ['340', co.hu_HU, cons.TV, 'Magyar ATV TV', 'mms://broadcast.line.hu/ATVlive/audio'], # ATV LIVE 
            ['341', co.hu_HU, cons.TV, 'Feherevar TV', 'mms://stream01.gtk.hu/fehervar_tv'],
            ['342', co.hu_HU, cons.TV, 'DANCE TV (slow)', 'mms://stream02.gtk.hu/dance_tvd'],
            ['343', co.hu_HU, cons.TV, 'ZTV (slow)', 'mms://stream02.gtk.hu/zeg_tv'],
            ['344', co.hu_HU, cons.TV, 'TV 8', 'mms://adas.pixeltv.hu/tv8'],
   
            ## Turkey ## 107
            ['345', co.tr_TR, cons.TV, 'Çay', 'mms://84.16.227.87/CayTv'],
            ['346', co.tr_TR, cons.TV, 'Expo channel', 'mms://yayin.canlitv.com/expochannel'],
            ['347', co.tr_TR, cons.TV, 'Guney TV', 'mms://yayin.canlitv.com/guneytv/guneytv.asf'],
            ['348', co.tr_TR, cons.TV, 'Kanal 15', 'mms://193.200.241.14/HResid'],
            ['349', co.tr_TR, cons.TV, 'Kanal 48', 'mms://yayin.canlitv.com/kanal48'],
            ['350', co.tr_TR, cons.TV, 'Kirsehir TV', 'mms://94.75.240.129/kirsehirtv'],
            ['351', co.tr_TR, cons.TV, 'M44 TV Malatya', 'mms://70.86.151.230/MalatyaInternetTv'],
            ['352', co.tr_TR, cons.TV, 'Olay TV', 'mms://yayin.canlitv.com/olaytv'],
            ['353', co.tr_TR, cons.TV, 'Oncu RTV', 'mms://yayin.canlitv.com/oncurtv'],
            ['354', co.tr_TR, cons.TV, 'TRT1', 'mms://212.156.63.102/TV1'],
            ['355', co.tr_TR, cons.TV, 'TV41', 'mms://yayin.canlitv.com/tv41'],
            ['356', co.tr_TR, cons.TV, 'YOL', 'mms://85.214.55.224/yol'],
            ['357', co.tr_TR, cons.TV, 'TRTTURK', 'mms://212.156.63.226/TRTTURK'],
            ['358', co.tr_TR, cons.TV, 'TRT2', 'mms://212.156.63.102/TV2'],
            ['359', co.tr_TR, cons.TV, 'TRT3', 'mms://212.156.63.226/TV3'],
            ['370', co.tr_TR, cons.TV, 'TRT5 ANADOLU', 'mms://212.156.63.102/TV5'],
            ['371', co.tr_TR, cons.TV, 'TRT6', 'mms://212.156.63.226/TV6'],
            ['372', co.tr_TR, cons.TV, 'TRT4 ÇOCUK', 'mms://212.156.63.226/TV4'],
            ['373', co.tr_TR, cons.TV, 'STV HABER', 'mms://canli.samanyoluhaber.tv/shaber'],
            ['374', co.tr_TR, cons.TV, 'YUMURCAK TV', 'mms://canli.yumurcak.tv/yumurcak'],
            ['375', co.tr_TR, cons.TV, 'KANAL67', 'mms://94.75.240.130/emrah'],
            ['376', co.tr_TR, cons.TV, 'BRT TV', 'mms://bms.brtk.net/brttv'],
            ['377', co.tr_TR, cons.TV, 'BRT2 TV', 'mms://bms.brtk.net/brt2'],
            ['378', co.tr_TR, cons.TV, 'DRTTV', 'mms://euro3.bizidinle.com/yayin-bd-drttv'],
            ['379', co.tr_TR, cons.TV, 'KIBRISGENÇTV', 'mms://euro3.bizidinle.com/yayin-bd-kibrisgenctv'],
            ['380', co.tr_TR, cons.TV, 'TV5', 'mms://94.75.240.130/tv5'],
            ['381', co.tr_TR, cons.TV, 'TRT belgesel', 'mms://212.156.63.102/TRTBELGESEL'],
            ['382', co.tr_TR, cons.TV, 'TV41KOCAELİ', 'mms://yayin.canlitv.com/tv41'],
            ['383', co.tr_TR, cons.TV, 'SAMANYOLUTV', 'mms://canli.samanyolu.tv/stv'],
            ['384', co.tr_TR, cons.TV, 'AMASYA ARTTV', 'mms://euro3.bizidinle.com/yayin-bd-arttv'],
            ['385', co.tr_TR, cons.TV, 'GÜNAZTV', 'mms://v1.webcasting.com/webcasting_gunaz'],
            ['386', co.tr_TR, cons.TV, 'HİLAL TV', 'mms://94.75.240.130/hilaltv'],
            ['387', co.tr_TR, cons.TV, 'HİZMET TV(slow)', 'mms://euro3.bizidinle.com/yayin-bd-hizmettv'],
            ['388', co.tr_TR, cons.TV, 'İÇTİMAİ TV', 'mms://85.132.81.6:1044/'],
            ['389', co.tr_TR, cons.TV, 'KAÇKAR TV', 'mms://94.75.240.130/kackartv'],
            ['390', co.tr_TR, cons.TV, 'NTV', 'mms://144.122.56.15/odtutv'],
            ['391', co.tr_TR, cons.TV, 'CİNE 5 (slow)', 'mms://yayin.cine5.com.tr/cine5'],
            ['392', co.tr_TR, cons.TV, 'KANAL48', 'mms://yayin.canlitv.com/kanal48'],
            ['393', co.tr_TR, cons.TV, 'KANAL51', 'mms://94.75.240.158/kanal51'],
            ['394', co.tr_TR, cons.TV, 'KANAL ALANYA', 'mms://kanalalanya.com/kanalalanya'],
            ['395', co.tr_TR, cons.TV, 'KANALVİP VTV', 'mms://88.225.223.212/'],
            ['396', co.tr_TR, cons.TV, 'MEHTAP TV', 'mms://canli.mehtap.tv/mehtap'],
            ['397', co.tr_TR, cons.TV, 'ÜN TV (slow)', 'mms://193.255.244.60:8080'],
            ['398', co.tr_TR, cons.TV, 'TRT MÜZİK', 'mms://212.156.63.102/TRTMUZIK'],
            ['399', co.tr_TR, cons.TV, 'TRT AVAZ', 'mms://212.156.63.226/TRTAVAZ'],
            ['400', co.tr_TR, cons.TV, 'ADATV', 'mms://212.175.149.82:8080'],
            ['401', co.tr_TR, cons.TV, 'KANAL3 TV', 'mms://91.191.163.159/Kanal3tv'],
            ['402', co.tr_TR, cons.RADIO, 'RADYO 1', 'mms://212.156.63.102/RADYO1'],
            ['403', co.tr_TR, cons.RADIO, 'RADYO 3', 'mms://212.156.63.102/RADYO3'],
            ['404', co.tr_TR, cons.RADIO, 'RADYO 4', 'mms://212.156.63.102/RADYO4'],
            ['405', co.tr_TR, cons.RADIO, 'TRT FM', 'mms://212.156.63.102/RADYOFM'],
            ['406', co.tr_TR, cons.RADIO, 'TRT TÜRKÜ', 'mms://212.156.63.102/TURKU'],
            ['407', co.tr_TR, cons.RADIO, 'TRT TSR', 'mms://212.156.63.102/RDTSR'],
            ['408', co.tr_TR, cons.RADIO, 'TRT VOT EAST', 'mms://212.156.63.102/RDVOT2'],
            ['409', co.tr_TR, cons.RADIO, 'TRT VOT WORLD', 'mms://212.156.63.102/RDVOT'],
            ['410', co.tr_TR, cons.RADIO, 'TRT VOT WEST', 'mms://212.156.63.102/RDTSR2'],
            ['411', co.tr_TR, cons.RADIO, 'TRT RADYO 6', 'mms://212.156.63.102/RADWORLD2'],
            ['412', co.tr_TR, cons.RADIO, 'TRT NAĞME', 'mms://212.156.63.102/TSM'],
            ['413', co.tr_TR, cons.RADIO, 'TRT ANKARA', 'mms://212.156.63.102/KENT'],
            ['414', co.tr_TR, cons.RADIO, 'TRT AVRUPA', 'mms://212.156.63.102/AVRUPA'],
            ['415', co.tr_TR, cons.RADIO, 'TRT ANTALYA', 'mms://212.156.63.102/ANTALYA'],
            ['416', co.tr_TR, cons.RADIO, 'TRT GAP', 'mms://212.156.63.102/TRTGAP'],
            ['417', co.tr_TR, cons.RADIO, 'TRT ERZURUM', 'mms://212.156.63.102/ERZURUM'],
            ['418', co.tr_TR, cons.RADIO, 'TRT ÇUKUROVA', 'mms://212.156.63.102/CUKUROVA'],
            ['419', co.tr_TR, cons.RADIO, 'TRT TRABZON', 'mms://212.156.63.102/TRABZON'],
            ['420', co.tr_TR, cons.RADIO, 'POLİS RADYOSU', 'mms://212.175.37.110/pr3'],
            ['421', co.tr_TR, cons.RADIO, 'RADYO D (slow)', 'mms://84.16.230.44/Radyod'],
            ['422', co.tr_TR, cons.RADIO, 'BAYRAK RADYOSU', 'mms://bms.brtk.net/bayrakradio'],
            ['423', co.tr_TR, cons.RADIO, 'BAYRAK INTERNATIONAL', 'mms://bms.brtk.net/bayrak-int'],
            ['424', co.tr_TR, cons.RADIO, 'BAYRAK FM', 'mms://bms.brtk.net/bayrakfm'],
            ['425', co.tr_TR, cons.RADIO, 'BAYRAK KLASİK', 'mms://bms.brtk.net/bayrak-classic'],
            ['426', co.tr_TR, cons.RADIO, 'BAYRAK RADYO 5', 'mms://bms.brtk.net/bayrak-radyo5'],
            ['427', co.tr_TR, cons.RADIO, 'METRO FM', 'http://metrofm.radyolarburada.com:9720'],
            ['428', co.tr_TR, cons.RADIO, 'BURSA 1001 FM', 'http://1001fm.radyoyayini.com:9170'],
            ['429', co.tr_TR, cons.RADIO, 'ADANA FM', 'http://yayin1.yayindakiler.com:3182'],
            ['430', co.tr_TR, cons.RADIO, 'AFŞİN RADYO', 'http://sunucu2.radyolarburada.com:7546'],
            ['431', co.tr_TR, cons.RADIO, 'RADYO AKDENİZ', 'mms://ns9.adabilisim.net/radyoakdeniz'],
            ['432', co.tr_TR, cons.RADIO, 'ARMONİ FM', 'http://canli.radyoyayini.com:7072'],
            ['433', co.tr_TR, cons.RADIO, 'AŞK FM', 'http://95.168.183.113:8020'],
            ['434', co.tr_TR, cons.RADIO, 'AVRASYA TÜRK', 'http://radyoavrasya.radyolarburada.com:1071'],
            ['435', co.tr_TR, cons.RADIO, 'ANTALYA BİZİM FM', 'http://www.onlinedinle.com:707'],
            ['436', co.tr_TR, cons.RADIO, 'DELTA FM', 'http://deltafm.radyolarburada.com:2030'],
            ['437', co.tr_TR, cons.RADIO, 'DÖNENCE FM', 'http://78.159.117.225:9290'],
            ['438', co.tr_TR, cons.RADIO, 'GEBZE FM', 'http://canli.radyoyayini.com:7199'],
            ['439', co.tr_TR, cons.RADIO, 'GÖZYAŞI FM', 'mms://94.75.240.129/gozyasi1'],
            ['440', co.tr_TR, cons.RADIO, 'SAKARYA HÜR FM', 'http://sunucu2.radyolarburada.com:8165'],
            ['441', co.tr_TR, cons.RADIO, 'KAPADOKYA FM', 'http://live.radyoyayini.com:3980'],
            ['442', co.tr_TR, cons.RADIO, 'MAX FM', 'http://maxfm.radyolarburada.com:3300'],
            ['443', co.tr_TR, cons.RADIO, 'METROPOL FM', 'http://live2.radyotvonline.com:7300'],
            ['444', co.tr_TR, cons.RADIO, 'PAŞA FM', 'http://pasafm.radyoyayini.com:9012'],
            ['445', co.tr_TR, cons.RADIO, 'RADYO 06', 'http://live.radyotvonline.com:8170'],
            ['446', co.tr_TR, cons.RADIO, 'BURÇ FM', 'http://live0.stv.com.tr/burcfm'],
            ['447', co.tr_TR, cons.RADIO, 'S HABER RADYO', 'http://live0.stv.com.tr/shaberradyo'],
            ['448', co.tr_TR, cons.RADIO, 'DÜNYA RADYO', 'http://live0.stv.com.tr/dunya'],
            ['449', co.tr_TR, cons.RADIO, 'AKRA RADYO', 'mms://74.53.35.226/akracanli'],
            ['450', co.tr_TR, cons.RADIO, 'MORAL FM', 'mms://94.75.240.130/moralfm'],
            ['451', co.tr_TR, cons.RADIO, 'AKSARAY FM', 'http://kalite.radyoyayini.com:9270'],
            ['452', co.tr_TR, cons.RADIO, 'BANAZDOST FM', 'http://banazdostfm.radyoyayini.com:5567'],
            ['453', co.tr_TR, cons.RADIO, 'ÇANAKKALE ÇAN FM', 'http://canfm1005.radyoyayini.com:7080'],
            ['454', co.tr_TR, cons.RADIO, 'MALKARA DOST FM', 'http://www.malkaradost.com:21002'],
            ['455', co.tr_TR, cons.RADIO, 'KALP FM', 'http://kalpfm.radyolarburada.com:8880'],
            ['456', co.tr_TR, cons.RADIO, 'KRAL TÜRK FM', 'http://sunucu2.radyolarburada.com:6565'],
            ['457', co.tr_TR, cons.RADIO, 'MAVİ RADYO', 'http://sunucu2.radyolarburada.com:7535'],
            ['458', co.tr_TR, cons.RADIO, 'RADYO MEGA', 'http://sunucu4.radyolarburada.com:1054'],
            ['459', co.tr_TR, cons.RADIO, 'ROMANTİK TÜRK', 'http://sunucu2.radyolarburada.com:8845'],
            ['460', co.tr_TR, cons.RADIO, 'İZMİR SAHİL FM', 'mms://89.19.26.210/radyosahil'],
            ['461', co.tr_TR, cons.RADIO, 'İSTANBUL YÖN RADYO', 'http://yonradyo.radyolarburada.com:8020'],

            ## China ## 11
            ['462', co.cn_CN, cons.TV, 'CCTV 9', 'mms://72.166.136.132/cctv9-300'], # Central China TV
            ['463', co.cn_CN, cons.TV, 'CSPN Sports', 'mms://58.48.156.93/hubeitiyu'],
            ['464', co.cn_CN, cons.TV, 'LSTV 1', 'mms://202.96.114.251/lstv'],
            ['465', co.cn_CN, cons.TV, 'NC News', 'mms://live2.ncnews.com.cn/sjb?userid=guest&token=7b4821c3f9ae818c3964a687a62773a2'],
            ['466', co.cn_CN, cons.TV, 'Shanghai PanCam', 'mms://www.onedir.com/cam3'],
            ['467', co.cn_CN, cons.TV, 'Shanghai Huang Pu River Cam', 'mms://www.onedir.com/cam1'],
            ['468', co.cn_CN, cons.TV, 'SUN TV', 'mms://211.157.10.21/suntvlive'],
            ['469', co.cn_CN, cons.TV, 'Weather China', 'mms://hainan.weathercn.com/qx'],
            ['470', co.cn_CN, cons.TV, 'XZTV 1)', 'mms://218.3.205.21/xwzhpd'],
            ['471', co.cn_CN, cons.TV, 'XZTV 2', 'mms://218.3.205.21/jjshpd'],
            ['472', co.cn_CN, cons.TV, 'XZTV 3', 'mms://218.3.205.21/shzfpd'],
            ['473', co.cn_CN, cons.TV, 'webshss', 'mms://webshss.bbtv.cn/webshss'],
            ['474', co.cn_CN, cons.TV, 'webcbn', 'mms://webcbn.bbtv.cn/webcbn'],
            ['475', co.cn_CN, cons.TV, 'webdsj', 'mms://webdsj.bbtv.cn/webdsj'],
            ['476', co.cn_CN, cons.TV, 'web dfdy', 'mms://webdfdy.bbtv.cn/webdfdy'],
            ['477', co.cn_CN, cons.TV, 'cctv2', 'mms://61.175.162.94/cctv2'],
                        
            ## Brazil ## 10
            ['478', co.pl_PL, cons.TV, 'ALLTV', 'mms://media.brturbo.com.br/turbotv.wmv'],
            ['479', co.pl_PL, cons.TV, 'CRISTO VIVE', 'mms://overserver1000.com/tvcristovive3'],
            ['480', co.pl_PL, cons.TV, 'HI-LIFE TV', 'mms://espalhabrasas.sapo.pt/hilifetv'],
            ['481', co.pl_PL, cons.TV, 'JUST TV', 'mms://208.109.239.158/Fazoko'],
            ['482', co.pl_PL, cons.TV, 'REDE FAMILIA', 'mms://srv3.ntelecom.com.br/redefamilia'],
            ['483', co.pl_PL, cons.TV, 'RTPN TV', 'mms://195.245.168.21/rtp'],
            ['484', co.pl_PL, cons.TV, 'TV CAMBURY', 'mms://stream1.interrogacaodigital.net/cambury'],
            ['485', co.pl_PL, cons.TV, 'CACAO NOVA', 'mms://200.98.195.4/tvcn'],
            ['486', co.pl_PL, cons.TV, 'TV CLENCIA', 'http://video-wm.tvciencia.pt/video/tvcnews_256.wmv'],
            ['487', co.pl_PL, cons.TV, 'YOURVIDA', 'mms://media.stream-music.net/stream2'],
            ['488', co.pl_PL, cons.TV, 'Sao Paulo (slow)', 'mms://wms.localmidia.com.br/canalsp'],
            ['490', co.pl_PL, cons.TV, 'FAAP TV (slow)', 'mms://video.faap.br/tvfaap'],
            
            ## Germany ## 10
            ['491', co.de_DE, cons.TV, 'VFO', 'http://members.inext.at/vof-tv/vof-tv/tv.wmv'],
            ['492', co.de_DE, cons.TV, 'Stuttgart Cam', 'mms://81.169.180.142/Stream-Stuttgart-9F4gS329'],
            ['493', co.de_DE, cons.TV, 'Rheinmain TV', 'mms://rheinmaintv-livestream.de/rmtv-livestream'],
            ['494', co.de_DE, cons.TV, 'WORM TV', 'mms://wms.global-streaming.net/04988'],
            ['495', co.de_DE, cons.TV, 'ANTENNEWEST', 'http://stream.christo.net/Antennewest'],
            ['496', co.de_DE, cons.TV, 'ASTRO TV', 'mms://atkon-webcast1-700k.wm.llnwd.net/atkon_webcast1_700K'],
            ['497', co.de_DE, cons.TV, 'CAMORAKEL TV', 'mms://85.214.87.175/camorakel/'],
            ['498', co.de_DE, cons.TV, 'DONAU TV', 'mms://d8019013966.w.glx.core006.cdn.streamfarm.net/11008bmt/live/3338s04donautv/300.wmv?cid=60535'],
            ['499', co.de_DE, cons.TV, 'TRP 1', 'mms://d8019013966.w.glx.core006.cdn.streamfarm.net/11008bmt/live/3338s12trp1/300.wmv?cid=60996'],
            ['500', co.de_DE, cons.TV, 'NDR HAMBURG', 'http://ndr-fs-nds-hi-wmv.wm.llnwd.net/ndr_fs_nds_hi_wmv'],
            ['501', co.de_DE, cons.TV, 'Kabbalah TV Deutsch', 'mms://vod.kab.tv/ger'],
            # http://wstreaming.zdf.de/encoder/3sat_vh.asx
            ['502', co.de_DE, cons.TV, '3SAT', 'mms://live.msmedia.zdf.newmedia.nacamar.net/zdf/3sat_vh_16zu9.wmv'],
            
            ## Austria ## 9
            ['503', co.at_AT, cons.TV, 'Burgenland TV', 'mms://83.142.83.22/bgld'],
            ['504', co.at_AT, cons.TV, 'Mittelburgenland TV', 'mms://83.142.83.22/bgld_m'],
            ['505', co.at_AT, cons.TV, 'Nordburgenland TV', 'mms://83.142.83.22/bgld_n'],
            ['506', co.at_AT, cons.TV, 'Paznaun skicenter Cam', 'mms://streamnt02.highway.telekom.at/panorama_see_adsl'],
            ['507', co.at_AT, cons.TV, 'Radio Noe Cam', 'mms://radio-noe.streaming.kabsi.at/radio_noe_cam'],
            ['508', co.at_AT, cons.TV, 'HT1 LIVE (slow)', 'mms://mediastream.mghmedien.at/mgh-tv'],
            ['509', co.at_AT, cons.TV, 'MF1', 'mms://gcs.redir.pkfdom.ris.at/mf1plus'],
            ['510', co.at_AT, cons.TV, 'REISE TV', 'mms://213.155.73.167/treffpunkt-austria-tv_standard_15'],
            ['511', co.at_AT, cons.TV, 'Suedburgenland TV', 'mms://globalserver.speednet.at/sbgldtv_live01'],    
                
            ## Thailand ## 9
            ['512', co.th_TH, cons.TV, 'Thai Tv', 'mms://broadcast.manager.co.th/11news1'],
            # mms://broadcast.manager.co.th/11news1?wmcontentbitrate=120000
            ['513', co.th_TH, cons.TV, 'X??', 'mms://video.tv5.co.th/live'],
            ['514', co.th_TH, cons.TV, 'X2??', 'mms://202.142.200.130/tv9?WMcontentBitrate=256000'],
            ['515', co.th_TH, cons.TV, 'ASTV2 - Toc', 'mms://broadcast.manager.co.th/toc'],
            ['516', co.th_TH, cons.TV, 'Kimeng', 'mms://202.57.163.14/kimeng1'],
            ['517', co.th_TH, cons.TV, 'Faikham TV', 'mms://media.ru.ac.th/Faikham_TV'],
            ['518', co.th_TH, cons.TV, 'Koh Samui Cam', 'mms://wms.th66.com/Livecam218'],
            ['519', co.th_TH, cons.TV, 'MVTV My', 'mms://61.19.248.196/mvtv_8?WMContentBitrate=256000'],
            ['520', co.th_TH, cons.TV, 'Siam Sport', 'mms://58.147.79.136/siamsport'],

            ## Poland ## 7
            ['521', co.pl_PL, cons.TV, 'TVFLY RAP', 'mms://tvfly.server-tv.com/TVFLY/?MSWMExt=.asf'],
            ['522', co.pl_PL, cons.TV, 'iTV', 'mms://stream.mni.pl/ITV'],
            ['523', co.pl_PL, cons.TV, 'Toya TV', 'mms://217.113.224.22/TVToya'],
            ['524', co.pl_PL, cons.TV, 'TV Trwam', 'mms://195.94.205.211/Trwam'],
            ['525', co.pl_PL, cons.TV, 'TVFLY', 'mms://tvfly.server-tv.com/TVFLY'],
            ['526', co.pl_PL, cons.TV, 'Wapster TV', 'mms://nadajnik.wapster.pl/wapstertv'],
            ['527', co.pl_PL, cons.TV, 'Kiss TV', 'mms://ml2.gazeta.pl/kiss_tv'],
            
            ## Russia ## 6
            ['528', co.ru_RU, cons.TV, 'РБК tv', 'mms://tv.gldn.net/rbc'],
            ['529', co.ru_RU, cons.TV, 'Eurosport News', 'mms://stream02.rambler.ru/eurosport'],
            ['530', co.ru_RU, cons.TV, 'City FM', 'mms://87.242.72.62/cityvideo'],
            ['531', co.ru_RU, cons.TV, 'CNL [Siberia]', 'mms://live.cnl.tv/cnl-sib'],
            ['532', co.ru_RU, cons.TV, 'MIR TV (128kb)', 'mms://213.232.226.11/MIRTV_128'],
            ['533', co.ru_RU, cons.TV, 'MIR TV (300kb)', 'mms://213.232.226.11/MIRTV_300'],
            ['534', co.ru_RU, cons.TV, 'TBN', 'mms://mms.rrsat-internet.tv/tbn'],
            # mms://mms.amtv.ru/BizOne
            ['535', co.ru_RU, cons.TV, 'AMTV SME', 'http://tvsme.ru/channels/high_r_1.asx', cons.ASX],
            ['536', co.ru_RU, cons.TV, 'Kultura TV', 'http://www.kulturatv.kiev.ua/Kultura-EU.asx', cons.ASX],
            ['537', co.ru_RU, cons.RADIO, '101 Cinema Music', 'mms://mms.online.ru/c2_2_128'],
            ['538', co.ru_RU, cons.RADIO, '101 Classic', 'mms://mms.online.ru/c7_1_128'],
            ['539', co.ru_RU, cons.RADIO, '101 Dance', 'mms://mms.online.ru/c4_2_128'],
            ['540', co.ru_RU, cons.RADIO, '101 Disco 80', 'mms://mms.online.ru/c7_3_128'],
            ['541', co.ru_RU, cons.RADIO, '101 Drum&amp;Bass', 'mms://mms.online.ru/c12_3_128'],
            ['542', co.ru_RU, cons.RADIO, '101 Easy Listening', 'mms://mms.online.ru/c11_2_128'],
            ['543', co.ru_RU, cons.RADIO, '101 Electro', 'mms://mms.online.ru/c6_3_128'],
            ['542', co.ru_RU, cons.RADIO, '101 Funk &amp; Soul', 'mms://mms.online.ru/c9_4_128'],
            ['544', co.ru_RU, cons.RADIO, '101 House', 'mms://mms.online.ru/c6_5_128'],
            ['545', co.ru_RU, cons.RADIO, '101 Instrumental', 'mms://mms.online.ru/c11_4_128'],
            ['546', co.ru_RU, cons.RADIO, '101 Love Songs', 'mms://mms.online.ru/c9_1_128'],
            ['547', co.ru_RU, cons.RADIO, '101 Office Lounge', 'mms://mms.online.ru/c2_1_128'],
            ['548', co.ru_RU, cons.RADIO, '101 Pink Floyd', 'mms://mms.online.ru/c8_2_128'],
            ['549', co.ru_RU, cons.RADIO, '101 progressive', 'mms://mms.online.ru/c8_4_128'],
            ['550', co.ru_RU, cons.RADIO, '101 Queen &amp; Freddie Mercury', 'mms://mms.online.ru/c13_1_128'],
            ['551', co.ru_RU, cons.RADIO, '101 Reggae', 'mms://mms.online.ru/c5_5_128'],
            ['552', co.ru_RU, cons.RADIO, '101 R\'n\'B', 'mms://mms.online.ru/c4_3_128'],
            ['553', co.ru_RU, cons.RADIO, '101 Rock RADIO', 'mms://mms.online.ru/c1_4_128'],
            ['554', co.ru_RU, cons.RADIO, '101 Smooth Jazz', 'mms://mms.online.ru/c2_3_128'],
            ['555', co.ru_RU, cons.RADIO, '101 The Beatles', 'mms://mms.online.ru/c10_3_128'],
            ['556', co.ru_RU, cons.RADIO, '101 Top 30', 'mms://mms.online.ru/c4_4_128'],
            ['557', co.ru_RU, cons.RADIO, 'Business FM 87.5 FM', 'http://stream03.rambler.ru/bizz'],
            ['556', co.ru_RU, cons.RADIO, 'Corbina Radio', 'http://radio.corbina.ru:8035/listen.pls', cons.PLS],
            ['557', co.ru_RU, cons.RADIO, 'Echo of Moscow 69.44 FM(MP3)', 'http://w02-sw01.akadostream.ru:8000/moscowecho128.mp3', cons.MP3],
            ['558', co.ru_RU, cons.RADIO, 'Echo of Rostov 69.44 FM(PLS)', 'http://echorostova.ru:8000/listen.pls', cons.PLS],
            ['559', co.ru_RU, cons.RADIO, 'Free Chechnya Radio 594 AM', 'http://212.69.114.20:8000/listen.pls', cons.PLS],
            # mms://195.161.23.194:8080/
            ['560', co.ru_RU, cons.RADIO, 'GTRK - St. Petersburg', 'http://www.vtuner.com/vtunerweb/mms/mms15802.asx', cons.ASX],
            # http://www.loveradio.ru/love-radio-96k.m3u
            ['561', co.ru_RU, cons.TV, 'Love Radio 105.3 FM', 'http://stream.loveradio.ru:8000/Loveradio_96_stereo.mp3'],
            
            ## South Korea ## 5
            ['562', co.kr_KR, cons.TV, 'CGN TV', 'mms://cdn7.cgntv.net/live200'], 
            ['563', co.kr_KR, cons.TV, 'C3TV', 'mms://211.63.212.50/live'],
            ['564', co.kr_KR, cons.TV, 'CBS', 'mms://vod2.cbs.co.kr/cbs_tv_live34'],
            ['565', co.kr_KR, cons.TV, 'CTS', 'mms://222.122.78.81/LIVE'],
            ['566', co.kr_KR, cons.TV, 'MBN Dream', 'mms://mbnlive.hanafoslive.com/mkimbn200'],
   
            ## Mexico ## 3
            ['567', co.mx_MX, cons.TV, 'Canal 53 UNAL', 'mms://148.234.13.58/canal53bandaancha'],
            ['568', co.mx_MX, cons.TV, 'Grupo FM TV', 'mms://70.85.59.52/grupofm'],
            ['569', co.mx_MX, cons.TV, '95.1 LATINO VIBE (REGGAETON)', 'http://95latinovibe.clients.brians.com:8000/951latinovibe.mp3'],

            ## Venezuela ## 2
            ['570', co.ve_VE, cons.TV, 'Promar TV', 'mms://corpoweb.interrogacaodigital.net/corpoweb'],

            ## Greece ## 3
            ['571', co.gr_GR, cons.TV, 'Achaia News', 'mms://174.36.42.85/achaiatv1'],
            ['572', co.gr_GR, cons.TV, 'Sport TV', 'mms://broadcast.hol.gr/tvmagic'],
            ['572', co.gr_GR, cons.TV, 'West Channel', 'mms://216.66.84.2/584932'],

            ## Portugal ## 3
            ['573', co.pt_PT, cons.TV, 'Guimaraes TV', 'mms://espalhabrasas.sapo.pt/guimaraestv'],
            ['574', co.pt_PT, cons.TV, 'Minho Actual TV', 'mms://espalhabrasas.sapo.pt/minhoactualtv'],
            ['575', co.pt_PT, cons.TV, 'TV Net', 'mms://espalhabrasas.sapo.pt/tvnet'],
            ['576', co.pt_PT, cons.RADIO, 'Antena 1', 'mms://rdp.oninet.pt/antena1'],
            
            ## Iraq ## 3
            ['577', co.iq_IQ, cons.TV, 'Turkmeneli TV', 'mms://94.75.240.129/turkmenelitv'],
            ['578', co.iq_IQ, cons.TV, 'Zagros TV', 'mms://live.zagrostv.com/zag'], # Kurdistan/Iraq
            ['579', co.iq_IQ, cons.TV, 'Kurdistan TV', 'mms://81.26.218.82/kurdistantv?wmbitrate=291000'], # Kurdistan
            
            ## Vietnam ## 2
            ['580', co.vn_VN, cons.TV, 'THVL', 'mms://123.30.108.77/THVL1'],
            ['581', co.vn_VN, cons.TV, 'Vietnamnet TV', 'mms://tv.vietnamnet.vn/live'],
            ['582', co.vn_VN, cons.TV, 'Giai Tri nuoc ngoai', 'http://63.218.83.51/MaksTv'],
            
            ## Congo ## 2
            ['583', co.cg_CG, cons.TV, 'BRN TV', 'mms://almadina.tv.ly/live'],
            ['584', co.cg_CG, cons.TV, 'Congo Planet', 'mms://congoplanet.com/Congo_Planet_TV'],
            ['585', co.cg_CG, cons.RADIO, 'Radio Okapi', 'http://rs1.radiostreamer.com:9080/listen.pls'],
            ['586', co.cg_CG, cons.RADIO, 'Mangembo 99.7 FM', 'http://87.98.222.14:7460'],
            
            ## Cuba ## 2
            ['587', co.cu_CU, cons.TV, 'TV Martí', 'mms://a165.1211035484.c2110.g.lm.akamaistream.net/D/165/2110/v0001/reflector:35484'],
            ['588', co.cu_CU, cons.TV, 'Cubavision', 'mms://200.55.129.7:80/Tvcubana/Tvcubana.asx'],

            ## Bosnia and Herzegovina ## 2
            ['589', co.ba_BA, cons.TV, 'TV Slon', 'mms://media.bih.net.ba/radioslon1'],
            ['590', co.ba_BA, cons.TV, 'Valentino BH OTV', 'mms://77.74.231.12/web2'],
            
            ## Romania ## 2
            ['591', co.ro_RO, cons.TV, 'Alfa Omega Movies', 'mms://ns.alfanet.ro/live'],
            ['592', co.ro_RO, cons.TV, 'Crestin TV', 'mms://ns.alfanet.ro/CrestinTv'],
            
            ## Albania ## 2
            ['593', co.al_AL, cons.TV, 'Vizion Plus', 'http://www.vizionplus.tv/foto/lajme.wmv'],
            ['594', co.al_AL, cons.TV, 'Albanian TV of Michigan', 'mms://live.upstreamnetworks.com/19514-47599'],
            # http://www.atdheu.de/RadioAtdheu.m3u
            ['595', co.al_AL, cons.RADIO, 'Atdheu', 'http://www.atdheu.de:8000'],
            # http://www.radiodardania.com/radio.m3u
            ['596', co.al_AL, cons.RADIO, 'Dardania', 'http://radio.radiodardania.com:4000'],
            
            ## Switzerland ## 2
            ['597', co.ch_CH, cons.TV, 'Tele M1', 'mms://wms01.agglo.ch/m1-live'],
            ['598', co.ch_CH, cons.TV, 'Tele Tell', 'mms://wms01.agglo.ch/tell-live'],
            
            ## Chile ## 2
            ['599', co.cl_CL, cons.TV, 'Canal 13', 'http://streaming.entelchile.net/canal13'],
            ['600', co.cl_CL, cons.TV, 'Canal 54', 'http://streaming.entelchile.net/canal54'],
            ['601', co.cl_CL, cons.RADIO, 'Maxima FM - Antofagasta', 'http://cast.chilestreaming.com:8210'],
            ['602', co.cl_CL, cons.RADIO, 'Clann NiNja', 'http://cast.chilestreaming.com:9468'],
            ['603', co.cl_CL, cons.RADIO, 'La voz de Yungay', 'http://cast.chilestreaming.com:8034'],
            # http://www.radioaconcagua.cl/aconcagua.asx
            ['604', co.cl_CL, cons.RADIO, 'Aconcagua (San Felipe)', 'http://atanua.broadcastchile.cl:4080'],
            ['605', co.cl_CL, cons.RADIO, 'Alfaomega (Curicó)', 'http://sc4.spacialnet.com:13826'],
            # http://radioanglolatina.cl/play.asx
            ['606', co.cl_CL, cons.RADIO, 'AngloLatina (Antofagasta)', 'http://streaming.radioservicios.cl:8098'],
            ['607', co.cl_CL, cons.RADIO, 'Radio Beethoven', 'http://sc.grupodial.net:8086'],
            ['608', co.cl_CL, cons.RADIO, 'Carolina', 'http://sc.grupodial.net:8080'],
            ['610', co.cl_CL, cons.RADIO, 'Club FM', 'http://online.3radio.cl/clubonline'],
            ['611', co.cl_CL, cons.RADIO, 'FM Plus (Antofagasta)', 'http://cast.chilestreaming.com:9466'],
            ['612', co.cl_CL, cons.RADIO, 'FM Tiempo', 'mms://200.27.214.28/fmtiempo'],
            # http://audio2.grupolatinoderadio.com/envivo.ASX?EMI=CLFUTURO
            ['613', co.cl_CL, cons.RADIO, 'Radio Futuro', 'http://streaming.iberoamerican.cl/clfuturo'],
            # http://audio2.grupolatinoderadio.com/envivo.ASX?EMI=CLROCKPOP
            ['614', co.cl_CL, cons.RADIO, 'Rock and Pop', 'http://streaming.iberoamerican.cl/clrockpop'],
            # http://online.laradio.cl:8000/32K.m3u
            ['615', co.cl_CL, cons.RADIO, 'Radio Biobio', 'http://online.laradio.cl:8000/32K'],
            # http://www.canal80.com/128k.asx
            ['616', co.cl_CL, cons.RADIO, 'Canal 80 (Valdivia)', 'http://main.cl.mu:8000'],
            # http://www.radiocamila.cl/player/radiocamila.asx
            ['617', co.cl_CL, cons.RADIO, 'Camila (Los Angeles)', 'http://200.71.207.92:8020'],
            # http://www.vtuner.com/vtunerweb/mms/mms17337.asx (this channel dont have ASX format)
            ['618', co.cl_CL, cons.RADIO, 'Caribe 104.9 FM', 'mms://68.178.148.43/caribefm'],
            ['619', co.cl_CL, cons.RADIO, 'Duna 89.7 FM', 'http://sc.grupodial.net:8088/listen.pls', cons.PLS],
            ['620', co.cl_CL, cons.RADIO, 'Festival 1270 AM', 'http://www.festival.cl/eng/festival.pls', cons.PLS],
            ['621', co.cl_CL, cons.RADIO, 'Buenan Nueva de Chanco 106.3', 'http://sc.digitalproserver.com:9418/listen.pls'],
            ['622', co.cl_CL, cons.RADIO, 'Alfaomega 106.5 FM', 'http://sc4.spacialnet.com:13826'],
            # http://www.vtuner.com/vtunerweb/mms/mms14257.asx
            ['623', co.cl_CL, cons.RADIO, 'Señal internet', 'mms://RUTASFM.mercurio.cl/lowstreaminternet2004'],
            ['624', co.cl_CL, cons.RADIO, 'El Faro 95.7 FM', 'http://radioelfaro.no-ip.com:8000/listen.pls'],
            # This channel have a invalid XML file for ASX, but emit with: http://santiagoradio.cl/64.asx
            ['625', co.cl_CL, cons.RADIO, 'Santiago', 'http://208.85.242.184:8002'], #, cons.ASX
            ['626', co.cl_CL, cons.TV, 'Telecanal', 'http://wmedia3.ifxnw.cl/telecanal'],
            ['627', co.cl_CL, cons.TV, 'MasCanal 22 (slow)', 'http://www.mas22.cl/canalmas22.asx', cons.ASX],
            ['628', co.cl_CL, cons.TV, 'Uniacc', 'mms://media.uniacc.cl/canal34tv'],
            ['629', co.cl_CL, cons.RADIO, 'Hit40 (slow)', 'http://audio2.grupolatinoderadio.com/envivo.ASX?EMI=CLHIT40', cons.ASX],
            ['630', co.cl_CL, cons.TV, 'Canal 33 (slow)', 'http://190.8.65.106:1047'],
            
            ## Sweden ## 2
            ['631', co.se_SE, cons.TV, 'DKNET', 'mms://wm-live.crossnet.net/dknettv'],
            ['632', co.se_SE, cons.TV, 'Kanal 10', 'mms://wm-live.crossnet.net/kanal10'],
            
            ## Dominican Republic ## 2
            ['633', co.do_DO, cons.TV, 'Digital 15', 'mms://66.128.53.146/DIGITAL15'],
            ['634', co.do_DO, cons.TV, 'TeleMicro', 'mms://66.128.53.146/TELEMICRO'],
            
            ## Belgium ## 2
            ['635', co.be_BE, cons.TV, 'RTC Tele Liege', 'http://video.rtc.be/jt_du_jour.wmv'],
            ['636', co.be_BE, cons.TV, 'RTV', 'http://www.rtv-media.be/nieuws/nieuwskempen.wmv'],

            ## Netherlands ## 3
            ['637', co.nl_NL, cons.TV, 'Graafschap TV', 'mms://graafschaptv.streamonline.nl/graafschaptv'],
            ['638', co.nl_NL, cons.TV, 'NOS Journaal 24', 'mms://livemedia2.omroep.nl/nos_journaal24-bb'],
            ['639', co.nl_NL, cons.RADIO, '78-toeren.be', 'http://radiobel.dahstream.nl:8016/listen.pls', cons.PLS],
            
            ## Japan ## 2
            ['640', co.jp_JP, cons.TV, 'POD TV', 'mms://dca.live.pod.tv/tandm56-2'],
            ['641', co.jp_JP, cons.TV, 'Fuji News Network', 'http://www.fnn-news.com/en/news/playlist/video/wmv/news_300_en.asx'],
            # [FIXME] => Make a parser =>  http://www.yomiuri.co.jp/stream/vnews/vnews-w.asx (Some weird ¬¬)
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Geino 1)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/geino/geino1.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Geino 2)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/geino/geino2.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Geino 3)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/geino/geino3.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Geino 4)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/geino/geino4.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Sports 1)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/sports/sports1.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Sports 2)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/sports/sports2.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Sports 3)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/sports/sports3.wmv'],
            #['80', co.jp_JP, cons.TV, 'Yomiuri News (Sports 4)', 'mms://pluto.primestage.net/impresstv/pj2/yomiuri/sports/sports4.wmv'],
            ['642', co.jp_JP, cons.TV, 'QVC (Slow)', 'mms://ecst.qvc.jp/LiveHigh'],
            # http://www.odoroku.tv/cgi-bin/mov/live.cgi?no=1&bps=56
            # mms://end.live.pod.tv/tandm56-2
            ['643', co.jp_JP, cons.TV, 'Odoroku 56kb', 'mms://dca.live.pod.tv/tandm56-2'],
            # http://www.odoroku.tv/cgi-bin/mov/live.cgi?no=1&bps=512
            # mms://end.live.pod.tv/tandm500
            ['644', co.jp_JP, cons.TV, 'Odoroku 512kb', 'mms://dca.live.pod.tv/tandm500'],
            #[FIXME] => Make a parser => http://www.channelj.co.jp/meta/toppage.asx (Some weird ¬¬)
            #['80', co.jp_JP, cons.TV, 'Channel J (irmess_asahi2)', 'mms://channelj.bmcdn.jp/channelj/chj/irmess_asahi2_j_071505s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (kanshi_kokaku)', 'mms://channelj.bmcdn.jp/channelj/chj/kanshi_kokaku_j_071505s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (shisei_hikari)', 'mms://channelj.bmcdn.jp/channelj/chj/shisei_hikari_j_071505s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (allnip_ec2005)', 'mms://channelj.bmcdn.jp/channelj/chj/allnip_ec2005_j_071205s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (expo71_hikita)', 'mms://channelj.bmcdn.jp/channelj/chj/expo71_hikita_j_070805s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (denkan_burger)', 'mms://channelj.bmcdn.jp/channelj/chj/denkan_burger_j_062805s.asf'],
            #['80', co.jp_JP, cons.TV, 'Channel J (ifacon_nikkoh)', 'mms://channelj.bmcdn.jp/channelj/chj/ifacon_nikkoh_j_062205s.asf'],
            # [FIXME] => Make a parser => FUJI NEWS NETWORK http://www.fnn-news.com/en/news/playlist/video/wmv/news_300_en.asx
            # [FIXME] => Make a parser => FNN NEWS http://www.fnn-news.com/en/news/playlist/video/wmv/news_300_en.asx
            ['645', co.jp_JP, cons.TV, 'Anime Academy Radio Network', 'http://www.animeacademyradio.net/listen.m3u', cons.M3U],
            
            ## Canada ## 1
            ['646', co.ca_CA, cons.TV, 'The Shopping Channel', 'mms://38.99.151.49/shop2/tsc.asx'],

            ## Slovenia ## 1
            ['647', co.si_SI, cons.TV, 'Paprika TV', 'mms://wmedia.siol.net/paprika/live'],
            
            ## Egypt ## 1
            ['648', co.eg_EG, cons.TV, 'Sat 7 Kids', 'mms://energy10.egihosting.com/859238'], 
            
            ## Norway ## 1
            ['649', co.no_NO, cons.TV, 'NRK 2 TV', 'mms://mms-icanal-live.online.no/nrk_tv_webvid04_h'],
            ['650', co.no_NO, cons.RADIO, '1FM', 'http://stream.1fm.no:2012/listen.pls', cons.PLS],
            
            ## Libya ## 1
            ['651', co.li_LY, cons.TV, 'Al Madina', 'mms://almadina.tv.ly/live'],
            
            ## South Africa ## 1
            ['652', co.za_ZA, cons.TV, 'Divine Truth', 'mms://78.129.146.199/divinetruth'], 
            
            ## India ## 1
            ['653', co.in_IN, cons.TV, 'IBN Lokmat', 'mms://a990.l4028444989.c40284.a.lm.akamaistream.net/D/990/40284/v0001/reflector:44989'],

            ## Iran ## 1
            ['654', co.ir_IR, cons.TV, 'Press TV English', 'mms://wms.edgecastcdn.net/200216/ipresstv'],
           
            ## Antigua and Barbuda ## 1
            ['655', co.ag_AG, cons.TV, 'ABS', 'mms://winmedia.act2000.net/abstv'],
            
            ## Andorra ## 1
            ['656', co.ad_AD, cons.TV, 'ATV', 'mms://194.158.91.91/Atv'], #Andorra TV

            ## Belize ## 1
            ['657', co.bz_BZ, cons.TV, '7 News', 'mms://200.32.198.90/7news'],
            
            ## El salvador ## 1
            ['658', co.sv_SV, cons.TV, 'Canal 21', 'mms://livetv2.siscompnetwork.com/canal21'],
             
            ## Bolivia ## 1
            ['659', co.bo_BO, cons.TV, 'Redadvenir', 'mms://eleden.com/redadvenir'],
            ['660', co.bo_BO, cons.RADIO, '96.9 FM La Paz', 'http://realserver2.megalink.com:8110/listen.pls', cons.PLS],
            
            ## Colombia ## 1
            ['661', co.co_CO, cons.TV, 'Teleantioquia', 'mms://200.12.176.10/comunicacionpolitica/cienciaspoliticas21abr2009.wmv'],
            
            ## Luxemburgo ## 1
            ['662', co.lu_LU, cons.TV, 'RTL', 'mms://streaming.newmedia.lu/telehighres'],
            
            ## Malta ## 1
            ['663', co.mt_MT, cons.TV, 'Smash Tv', 'mms://stream01.nextweb.net.mt/SmashTV'],
           
            ## Kuwait ## 1
            ['662', co.kw_KW, cons.TV, 'Al Watan Plus', 'mms://stream8.netro.ca/watantv/watanplus'],
           
            ## Qatar ## 1
            ['663', co.qa_QA, cons.TV, 'Al-Hekmah', 'mms://alhekmah.tv/live'],
           
            ## Lebanon ## 1
            ['664', co.lb_LB, cons.TV, 'Al-Manar TV', 'mms://209.172.60.145/live'],
            ['665', co.lb_LB, cons.RADIO, 'Al Manar', 'http://208.80.52.60:443/WKRKFMDIALUPCMP3'],
            
            ## Pakistan ## 1
            ['666', co.pk_PK, cons.TV, 'Express News', 'mms://ams01.egihosting.com/ExpressEnglish'],
            
            ## Jordan ## 1
            ['667', co.jo_JO, cons.TV, 'Jordan TV', 'mms://stream.jrtv.jo/jrtv'],
            
            ## Israel ## 1
            ['668', co.il_IL, cons.TV, 'Radios 100 Cam', 'mms://213.8.193.29/100fmcam'],

            ## Armenia ## 1
            ['669', co.am_AM, cons.TV, 'Amga TV', 'mms://74.208.15.132/Amga'],
            
            ## Kazakhstan ## 1
            ['670', co.kz_KZ, cons.TV, 'CNL Siberia', 'mms://live.cnl.tv/cnl-sib'],
            
            ## Czech Republic ## 1
            ['671', co.cz_CZ, cons.TV, 'HDTV1', 'mms://server3.streaming.cesnet.cz/hdtv1?WMThinning=0&MSWMExt=.asf'],
            
            ## Bulgaria ## 1
            ['672', co.bg_BG, cons.TV, 'Hip Hop TV', 'mms://84.22.1.210/hiphoptv'],
            
            ## Azerbaijan ## 1
            ['673', co.az_AZ, cons.TV, 'Lider TV', 'mms://85.132.50.243/Lider_Online'],
            
            ## Latvia ## 1
            ['674', co.lv_LV, cons.TV, 'LZK News', 'mms://stream.grafton.lv/live_lzk_lo'], # lativa?

            ## Estonia ## 1
            ['675', co.ee_EE, cons.TV, 'Ring FM Cam', 'mms://wms5.neti.tv/ringfm'],
             
            ## Denmark ## 1
            ['676', co.dk_DK, cons.TV, 'National Georaphic Wild', 'mms://80.167.239.220/Encoder16'],
            
            ## Australia ## 1
            ['677', co.au_AU, cons.TV, 'ABC Kids', 'mms://media4.abc.net.au/broadbandkids/20070521_1500/story1hi.wmv'],
            
            # Croatia ## 3
            ['678', co.hr_HR, cons.RADIO, 'Radio Koprivnica 91.7 FM (256kb)', 'http://85.25.151.118:23613/listen.pls'],
            ['679', co.hr_HR, cons.RADIO, 'Radio Koprivnica 91.7 FM (128kb)', 'http://85.25.151.118:23615/listen.pls'],
            ['680', co.hr_HR, cons.RADIO, 'Radio Koprivnica 91.7 FM (64kb)', 'http://85.25.151.118:23655/listen.pls'],
            ['681', co.hr_HR, cons.RADIO, 'Narodni', 'http://tv.stream-music.net:9374/listen.pls'],
            ['682', co.hr_HR, cons.RADIO, 'Narodni Radio', 'mmsh://media.t-com.hr/www.narodni.hr'],
            ['683', co.hr_HR, cons.RADIO, 'Radio Lijepa Nasa', 'http://www.radiolijepanasa.eu/listen.pls'],
            ['684', co.hr_HR, cons.RADIO, 'Gradski Radio - 99.1 FM', 'mms://wms.iskon.hr/Gradski%20radio%20Osijek'],
            # mms://wms.iskon.hr/Slavonski radio Osijek
            ['685', co.hr_HR, cons.RADIO, 'Slavonski Radio Osijek', 'http://wms.iskon.hr/Slavonski%20radio%20Osijek?MSWMExt=.asf'],
            #mms://wms.iskon.hr/Hrvatski radio Vukovar
            # http://wms.iskon.hr/Hrvatski?MSWMExt=.asf
            # http://www.vtuner.com/vtunerweb/mms/mms9988.asx
            ['686', co.hr_HR, cons.RADIO, 'Hrvatski Radio Vukovar', '"mms://wms.iskon.hr/Hrvatski radio Vukovar"'],
            # rtsp://213.5.57.148:554/encoder/htv1.rm
            # http://www.hrt.hr/streams/htv1.ram
            ['687', co.hr_HR, cons.TV, 'Hrvatski TV - Glas Hrvatske', 'rtsp://213.5.57.152:554/broadcast/htv1.rm'],
            ['688', co.hr_HR, cons.RADIO, 'Radio Sibenik 88.6 FM', 'http://38.96.148.19:9510/listen.pls'],
            ['689', co.hr_HR, cons.RADIO, 'Radio Martin 101.8 FM', 'http://glazba.posluh.hr:8000/listen.pls'],
            ['690', co.hr_HR, cons.RADIO, 'Radio America 780 AM', 'http://www.webitp.com:8000/listen.pls', cons.PLS],
            
            # American Samoa
            ['691', co.as_AS, cons.RADIO, '93 KHJ', 'http://khjradio.dyndns.org:8200/listen.pls', cons.PLS],

            # Lithuania
            ['692', co.lt_LT, cons.TV, '1 Music', 'mms://195.244.137.207:81/'],

            # SOPCAST CHANNELS
            ['693', co.es_ES, cons.SOPCAST, 'Roja Directa 1', 'sop://sop.rojadirecta.com:3912/6001'],
            ['694', co.es_ES, cons.SOPCAST, 'Roja Directa 2', 'sop://sop.rojadirecta.com:3912/6002'],
            ['695', co.es_ES, cons.SOPCAST, 'Roja Directa 99', 'sop://sop.rojadirecta.com:3912/6099'],
            ['696', co.en_US, cons.SOPCAST, 'Miami Heat - New York Knicks', 'sop://60.191.221.56:3912/18132'],
            ['697', co.cn_CN, cons.SOPCAST, 'Shanghai GSports [上海体育频道]', 'sop://60.191.221.56:3912/6001'],

            # ADD YOUR OWN CHANNELS HERE! (FOR NOW)
          ]
