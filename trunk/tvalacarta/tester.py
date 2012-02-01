# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# tester
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------


if __name__ == "__main__":
    '''
    from servers import telefe
    
    #video_urls = telefe.get_video_url("http://www.telefe.com/2010/10/09/lo-que-el-tiempo-nos-dejo-un-mundo-mejor/")
    video_urls = telefe.get_video_url("http://elelegido.telefe.com/2011/10/26/capitulo-152-26-10-11/")
    
    for video_url in video_urls:
        print './rtmpdump-2.4 -r "'+video_url[1]+'" -s "http://www.telefe.com/wp-content/plugins/fc-velocix-video/flowplayer/flowplayer.rtmp-3.1.3.swf" -o out.mp4'
    '''
    
    from servers import tvg    
    video_urls = tvg.get_video_url("http://www.crtvg.es/tvg/a-carta/cap-35")
