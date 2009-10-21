

# This example illustrates how to use cachedhttp.py functionality in your own scripts:

import cachedhttp
import xbmc, xbmcgui

def message(line1,line2='',line3=''):
	dialog = xbmcgui.Dialog()
	dialog.ok("Info", line1,line2,line3)


httpFetcher=cachedhttp.CachedHTTPWithProgress() #this class automatically puts up a cancelable progress bar while downloading

html=httpFetcher.urlopen('http://test:this@irisresearch.library.cornell.edu/control/authBasic/authTest/')


html=httpFetcher.urlopen("http://www.stfu.se")
html = httpFetcher.urlopen('http://www.stfu.se')
html = httpFetcher.urlopen('http://www.xboxmediaplayer.de/cgi-bin/forums/ikonboard.pl') #this should set some cookies!


# download to a file in the cache. returns the full path in the cache
# (downloading to a specific location is also possible) 
url = 'http://pictures.xbox-scene.com/hsdemonz/SmartXXSolderlesAdapter/AdapterFrontHI.jpg'
filename = httpFetcher.urlretrieve(url)
print filename

# download a file to a f:\videos\example.html
url = 'http://astrogeology.usgs.gov/assets/wallpaper/sun.jpg'
localfile='c:\\tester' #the extension will be autodetermined based on mimetype
httpFetcher.urlretrieve(url,None,localfile)
httpFetcher.urlretrieve(url,None,localfile) #use cache the second time.

httpFetcher.saveCookies()
del httpFetcher



#here is how you can write a custom progressbar:

class MyCachedHTTP(cachedhttp.CachedHTTP):
       def onDataRetrieved(self, bytesRead, totalSize, url, localfile):
               if (not (bytesRead is None))&(not (totalSize is None)):
                       pct=int(bytesRead*100.0/totalSize)
                       print(str(pct))
               return True # if you return false, then it means cancel the download
       
       def onDownloadFinished(self,success):
               pass

c=MyCachedHTTP()
data=c.urlopen('http://www.example.com')
