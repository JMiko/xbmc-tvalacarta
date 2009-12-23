# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para stagevu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re

def Stagevu(url):
    #print "-------------------------------------------------------"
    #print url
    #print "-------------------------------------------------------"
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    #print data

    patronvideos  = '<param name="src" value="([^"]+)"'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    i = 0

    #for match in matches:
    #    print "%d %s" % (i , match)
    #    i = i + 1

    return matches[0]

#print "-------------------------------------------------------"
#url="http://stagevu.com/video/jnukfujabtdl"
#print Stagevu(url)
