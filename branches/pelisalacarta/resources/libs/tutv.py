# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urlparse,urllib2,urllib,re

def Tutv(url):
    #http://tu.tv/tutvweb.swf?kpt=aHR0cDovL3R1LnR2L3ZpZGVvc2NvZGkvYS92L2F2YXRhci1lcGlzb2RpbzEwLWpldC5mbHY=&xtp=110371
    #http://tu.tv/visualizacionExterna2.php?web=undefined&codVideo=110371
    #print "-------------------------------------------------------"
    #print url
    #print "-------------------------------------------------------"

    patronvideos  = '"http://tu.tv.*?\&xtp\=([^"]+)"'

    matches = re.compile(patronvideos,re.DOTALL).findall('"'+url+'"')
    i = 0

    if len(matches)==0:
        patronvideos  = '"http://www.tu.tv.*?\&xtp\=([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall('"'+url+'"')

    i = 0

    #for match in matches:
    #    print "%d %s" % (i , match)
    #    i = i + 1

    url = "http://tu.tv/visualizacionExterna2.php?web=undefined&codVideo="+matches[0]
    #print "-------------------------------------------------------"
    #print url
    #print "-------------------------------------------------------"

    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    #print data

    patronvideos  = 'urlVideo0=([^\&]+)\&'

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    i = 0

    #for match in matches:
    #    print "%d %s" % (i , match)
    #    i = i + 1

    return matches[0]

#print "-------------------------------------------------------"
#url="http://www.tu.tv/tutvweb.swf?kpt=aHR0cDovL3d3dy50dS50di92aWRlb3Njb2RpL24vYS9uYXppcy11bi1hdmlzby1kZS1sYS1oaXN0b3JpYS00LTYtZWwuZmx2&xtp=669973_VIDEO"
#print Tutv(url)
