#ScriptName    : cachedhttp (formerly cachemanager)
Version         = '1.3'
# Author        : Van der Phunck aka Aslak Grinsted. as@phunck.cmo <- not cmo but com
# Desc          : cache manager
#
#

import sys, traceback, os.path, re 
ScriptPath = os.path.split(sys.modules['cachedhttp'].__file__)[0]+'\\' #this should always work! (note... os.getcwd() doesn't)

sys.path.insert(0, ScriptPath+'ClientCookie.zip')

import urllib2, re, time, string, random
import socket,md5,urlparse
import xbmc,xbmcgui
import mimetypes
import httplib
import ClientCookie
import base64
import urllib
import shutil

Debug=True
DefaultCacheTime=24*60.0 #minutes


try: Emulating = xbmcgui.Emulating #Thanks alot to alexpoet for the xbmc.py,xmbcgui.py emulator. Very useful!
except: Emulating = False


def fileExists(fname):
	return os.path.exists(fname)

def readCacheMeta(fname):
	if not fileExists(fname): return None
	try:
		fid=file(fname,'rb')
		info=httplib.HTTPMessage(fid)
		fid.close()
		return info
	except:
		return None
	
def isInFolder(fname,folder):
	fname=os.path.split(fname)
	fnamefolder=fname[0].lower()+'\\'
	if not (fnamefolder[-1]=='\\'): fnamefolder=fnamefolder+'\\'
	return (fnamefolder==folder.lower())

Rauth=re.compile('^(.*):(.*)@(.*)$',re.IGNORECASE)	
def parseAuthUrl(url):
	fields=urlparse.urlparse(url)
	fields=[fields[0],fields[1],fields[2],fields[3],fields[4],fields[5]]
	fauth=Rauth.findall(fields[1])
	if len(fauth)==0: return [url,'','']
	fields[1]=fauth[0][2] #host
	name=urllib.unquote(fauth[0][0]) #username
	pwd=urllib.unquote(fauth[0][1]) #password
	url=urlparse.urlunparse(fields)
	return [url,name,pwd]
	

Rwhitespace=re.compile('\s\s+',re.IGNORECASE)
Rillegalchars=re.compile('[^\.\_\w\d-]',re.IGNORECASE)
Rfilename=re.compile('[^\\/]*$',re.IGNORECASE)
Rdot2=re.compile('[\.\s]+',re.IGNORECASE)
def urltoxfilename(url):
	fields=urlparse.urlparse(url)
	fname=Rfilename.findall(fields[2])
	if len(fname)==0: fname=['']
	fname=fname[0]
	if len(fname)==0:
		fname=Rfilename.findall(fields[1])
		fname=fname[0]
		fname=fname.replace('.','-')
	fname=fname.replace(',',' ')
	fname=Rillegalchars.sub(' ',fname)
	fname=Rwhitespace.sub(' ',fname)
	fname=Rdot2.sub('.',fname)
	if len(fname)>40: #i think 42 is the limit?
		ext=os.path.splitext(fname)[1]
		fname=fname[0:40-max(len(ext),7)] #7 because a different extension might be added because of the mimetype...
		if fname[-1]=='.': fname=fname[0:-1]
		fname=fname+ext
	return fname


class CustomHandler(ClientCookie.HTTPCookieProcessor):
	def http_error_304(self, req, fp, code, message, headers):
		addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
		addinfourl.code = code
		return addinfourl


class CachedHTTP:
	def __init__(self):
		self.userAgent='OobaCacheMgr/'+Version
		self.urlContext=''
		self.socketTimeout=7.0
		self.cacheFolder='Z:\\~HttpCache\\'
		
		if Emulating: self.cacheFolder=ScriptPath+'Cache\\'
		try:
			os.makedirs(self.cacheFolder)
		except: pass
		
		self.cookiefile=self.cacheFolder+'~cookies.txt' 
		#the tilde is there to ensure that url2xfilename doesn't create a file that might overwrite this
		
		self.defaultCachetime=24*60.0 #minutes

		self.cookies=ClientCookie.LWPCookieJar()
		try:
			self.cookies.revert(self.cookiefile)
		except:
			print('Could not open cookie file: '+self.cookiefile)
			
		hh=CustomHandler(self.cookies)
		
		self.opener=ClientCookie.build_opener(hh)

	def saveCookies(self):
		self.cookies.save(self.cookiefile)
	
	def getCookieJar(self): return self.cookies
	
	def getUserAgent(self): return self.userAgent
	def setUserAgent(self,val): self.userAgent=val

	def getSocketTimeout(self): return self.socketTimeout
	def setSocketTimeout(self,val): self.socketTimeout=float(val)

	def getCacheFolder(self): return self.cacheFolder
#	def setCacheFolder(self,val): #you shouldn't call this really
#		self.cacheFolder=str(val)
#		if not (self.cacheFolder[-1]=='\\'): self.cacheFolder=self.cacheFolder+'\\'

	def getUrlContext(self): return self.urlContext
	def setUrlContext(self,val): self.urlContext=str(val)

	def getDefaultCachetime(self): return self.defaultCachetime
	def setDefaultCachetime(self,val): self.defaultCachetime=float(val)

	def getFullUrl(self,url): 
		if len(url)>0:
			if url[0]=='?': 
				f=urlparse.urlparse(self.urlContext)
				baseurl=urlparse.urlunparse([f[0],f[1],f[2],'','',''])
				return (baseurl+url).encode('iso-8859-1')
		return urlparse.urljoin(self.urlContext,url).encode('iso-8859-1')

	def onDataRetrieved(self, bytesRead, totalSize, url, localfile):
		return True
	def onDownloadFinished(self,success):
		pass
		
	def url2cachemetafile(self,url): #returns the filename of the meta file associated with url ... Note it does not necessarily exist 
		m = md5.new()
		m.update(url)
		digest=m.hexdigest()
		return self.cacheFolder+'~'+digest


	def cacheFilename(self,url):
		urlmetafile=self.url2cachemetafile(url)
		if fileExists(urlmetafile):
			info=readCacheMeta(urlmetafile)
			localfile=info['CM-Localfile']
			if fileExists(localfile): return localfile
		return ''

	def flushCache(self,url):
		urlmetafile=self.url2cachemetafile(url)
		if not fileExists(urlmetafile): return
		info=readCacheMeta(urlmetafile)
		os.remove(urlmetafile)
		if info is None: return #couldn't understand meta file...
		try:
			localfile=info['CM-localfile']
			if fileExists(localfile):
				if isInFolder(localfile,self.cacheFolder):
					os.remove(localfile)
		except: pass

	def getCacheMeta(self,urlmetafile,expiretime=None): #returns None if the file doesn't exist or if the data is too old.
		#expiretime is a way of overriding cachetime information in the metafile...
		if not fileExists(urlmetafile): return None
		info=readCacheMeta(urlmetafile)
		isMetaOK=not (info is None)
		try:
			if isMetaOK:
				localfile=info['CM-localfile']
				timestamp=float(info['CM-TimeStamp'])
				cachetime=float(info['CM-CacheTime'])
				if not expiretime is None: cachetime=expiretime
				if cachetime>=0: #(that is not permanent)
					isMetaOK=isMetaOK & (abs(time.time()-timestamp)<(cachetime*60))
				if fileExists(localfile):
					contentlength=int(info['Content-Length'])
					isMetaOK=isMetaOK & (os.path.getsize(localfile)==contentlength)
					if (not isMetaOK) and isInFolder(localfile,self.cacheFolder):
						os.remove(localfile)
				else:
					isMetaOK=False
		except:
			isMetaOK=False
		if not isMetaOK:
			os.remove(urlmetafile)
			return None
		return info
		
	
	def cleanCache(self,expiretime=None):
		files=os.listdir(self.cacheFolder)
		Rmetafile=re.compile('^\~[\dabcdef]{32}$',re.IGNORECASE)
		for filename in files:
			try:
				fname=filename.lower()
				if Rmetafile.match(fname):
					filename=self.cacheFolder+fname
					info=self.getCacheMeta(filename,expiretime)
			except:
				pass
				
	def urlretrieve(self,url,cachetime=None,localfile=None,ext=None,postdata=None):
		url=self.getFullUrl(url)
		urlmetafile=self.url2cachemetafile(url)
		if cachetime is None: cachetime=self.defaultCachetime
		metainfo = self.getCacheMeta(urlmetafile)
		furl=None
		fcache=None
		isDownloadCompleted=False
		try:
			self.onDataRetrieved(0, None, url, '')
			oldtimeout=socket.getdefaulttimeout()
			socket.setdefaulttimeout(self.socketTimeout)
			authurl=parseAuthUrl(url)
			if len(authurl[1])>0: #todo use HTTPBasicAuthHandler instead....
				url=authurl[0]
				base64string=base64.encodestring('%s:%s' % (authurl[1],authurl[2]))[:-1]
				authheader = "Basic %s" % base64string
			request = ClientCookie.Request(url)
			request.add_header('User-Agent',self.userAgent)
			if len(authurl[1])>0: request.add_header("Authorization", authheader)
			#if len(self.urlContext)>0: #TODO: not always
			#	request.add_header('Referer',self.urlContext)
			if not (metainfo is None):
				try:
					etag=metainfo['ETag']
					request.add_header('If-None-Match', etag)
				except:	pass
				try:
					lastmodified = metainfo['Last-Modified']
					request.add_header('If-Modified-Since', lastmodified)
				except: pass
			furl=self.opener.open(request,postdata)
			info=furl.info()
			if not (metainfo is None):
				if hasattr(furl, 'code') and furl.code == 304:
					self.urlContext=metainfo['CM-UrlContext']
					temp=os.path.split(metainfo['CM-Localfile'])
					print('using cache: '+temp[1])
					isDownloadCompleted=True
					if not (localfile is None):
						nameext=os.path.splitext(metainfo['CM-Localfile'])
						if not (localfile.lower()==nameext[0].lower()):
							localfile=localfile+nameext[1]
							shutil.copyfile(metainfo['CM-Localfile'],localfile)
							return localfile
					return metainfo['CM-Localfile']
				else:
					self.flushCache(url)
			try:
				totalSize=int(info['Content-Length'])
			except:
				totalSize=None
				
			#------------ construct local file name ---------
			xfname=os.path.splitext(urltoxfilename(url)) #tuple: suggested (filename,ext)
			xfname=[xfname[0],xfname[1]] #otherwise you cannot write to it
			try:
				mimetype=info['Content-Type'].split(';') # also understand "Content-Type: text/html; charset=utf-8"
				mimetype=mimetype[0].strip()
				mimeext=mimetypes.guess_extension(mimetype)
				if (not (mimeext is None)) and (len(mimeext)>0): 
					if mimeext=='.m1v': mimeext='.mpg'
					xfname[1]=mimeext #override the one based on url alone
			except:
				pass
			if not (ext is None): xfname[1]=ext #override with manual extension
			ext=xfname[1]
			xfname=xfname[0]
			if len(ext)>0:
				if not (ext[0]=='.'): ext='.'+ext
				ext=ext[0:7] #do not allow so long extensions... Just truncate
			if localfile is None: #then autogenerate a file name for the cache
				localfile=self.cacheFolder+xfname+ext
				i=1
				while fileExists(localfile):
					i=min(i*10,100000) #add a random number to minimize fileexist checks
					localfile=self.cacheFolder+xfname[0:30]+'['+str(random.randint(0,i-1))+']'+ext
			else:
				localfile=localfile+ext
			#------------------------------------------------
			fcache=file(localfile,'wb')
			iscanceled=not self.onDataRetrieved(0, totalSize, url, localfile)
			data='...'
			blockSize=8192
			pval=0
			while len(data)>0:
				if not totalSize is None:
					if pval>totalSize: totalSize=pval*2
				data = furl.read(blockSize)
				pval=pval+len(data)
				if len(data)>0: fcache.write(data)
				if len(data)<blockSize: break
				iscanceled=not self.onDataRetrieved(pval, totalSize, url, localfile)
				if iscanceled: break
			isDownloadCompleted=not iscanceled
			self.urlContext=furl.url
		finally:
			self.onDownloadFinished(isDownloadCompleted)
			try:
				if not fcache is None: fcache.close()
				if not furl is None: furl.close()
				socket.setdefaulttimeout(oldtimeout)
				if not isDownloadCompleted: os.remove(localfile)
			except:
				pass
		if not isDownloadCompleted:
			return None
		#------------- write url meta file ------------
		#TODO: maybe do something if info['cache-control']=private?
		info['Content-Length']=str(pval)
		info['CM-Localfile']=localfile
		info['CM-urlContext']=self.urlContext
		info['CM-CacheTime']=str(cachetime)
		info['CM-TimeStamp']=str(time.time())
		info['CM-url']=url
		fuc=file(urlmetafile,'wb')
		fuc.write(str(info))
		fuc.close()
		return localfile
		
	def urlopen(self,url,data=None):
		localfile=self.urlretrieve(url,postdata=data)
		f=file(localfile, 'rb')
		data = f.read()
		f.close()
		return data
		
	
				
class CachedHTTPWithProgress(CachedHTTP):
	def onDataRetrieved(self, bytesRead, totalSize, url, localfile):
		if (not hasattr(self,'progressbar')): self.progressbar=None
		if self.progressbar is None:
			nombrefichero =  urllib.unquote_plus( url.split("/")[-1] )
			self.progressbar=xbmcgui.DialogProgress()
			self.progressbar.create("Descargando...","",url,nombrefichero)
		if (not (bytesRead is None))&(not (totalSize is None)):
			pct=int((bytesRead % (totalSize+1))*100.0/totalSize)
			#self.progressbar.update(pct)
			self.progressbar.update(pct, "Descargados %.2fMB de %.2fMB (%d%%)" % ( float( float(bytesRead) / float(1024*1024) ) , float( float(totalSize) / float(1024*1024) ) , pct ))
		return not self.progressbar.iscanceled()
	
	def onDownloadFinished(self,success):
		try:
			self.progressbar.close()
		except: pass
		self.progressbar=None
