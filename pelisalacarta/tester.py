# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# tester
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------


if __name__ == "__main__":
    from core import scrapertools

    from servers import bliptv
    
    print bliptv.get_url("http://blip.tv/file/4645870")