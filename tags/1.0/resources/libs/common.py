import os, re, string, sys, time
from string import *
import htmlentitydefs
import beautifulsoup

import xbmc

#===============================================================================
# Make global object available
#===============================================================================
import config, envcontroller
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler
#===============================================================================
class clistItem:
    def __init__(self, title, url, type="folder", parent=None):
        self.name =  ConvertHTMLEntities(title)
        self.url = url
        self.mediaurl = ""
        self.description = ""
        self.thumb = ""        # image of episode
        self.thumbUrl = ""
        self.icon = ""        # icon for list
        self.date = ""
        self.type = type     # video, folder, append, page
        self.parent = parent
        self.complete = False
        self.downloaded = False
        self.downloadable = False
        self.items = []
        self.rating = None
        # GUID used for identifcation of the object. Do not set from script
        self.guid = ("%s-%s" % (title,url)).replace(" ","") 
    
        self.channels = []    # only needed for Kanalenkiezer 
        
    
    def __eq__(self, item):
        return self.Equals(item)
    
    def __ne__(self, item):
        return not self.Equals(item)
        
    def Equals(self, item):
        return self.guid == item.guid
        
#===============================================================================
def HTMLEntityConverter(entity):
    #logFile.debug("1:%s, 2:%s", entity.group(1), entity.group(2))
    try:
        if entity.group(1)=='#':
            #logFile.debug("%s: %s", entity.group(2), chr(int(entity.group(2))))
            return chr(int(entity.group(2)))
        else:
            #logFile.debug("%s: %s", entity.group(2), htmlentitydefs.entitydefs[entity.group(2)])
            return htmlentitydefs.entitydefs[entity.group(2).lower()]
    except:
        logFile.error("error converting HTMLEntities", exc_info=True)
        return '&%s%s;' % (entity.group(1),entity.group(2))
    return entity

#============================================================================== 
def ConvertHTMLEntities(html):
    """
        Convert the entities in HTML using the HTMLEntityConverter
    """
    newHtml = re.sub("&(#?)(.+?);", HTMLEntityConverter, html)
    return newHtml

#============================================================================== 
def UrlEntityConverter(entity):
    """
       Substitutes an HTML/URL entity with the correct character
    """
    #logFile.debug("1:%s, 2:%s", entity.group(1), entity.group(2))
    try:
        tmpHex = '0x%s' % (entity.group(2))
        #logFile.debug(int(tmpHex, 16))
        return chr(int(tmpHex, 16))
    except:
        logFile.error("error converting URLEntities", exc_info=True)
        return '%s%s' % (entity.group(1),entity.group(2))

#============================================================================== 
def ConvertURLEntities(url):
    """
        Convert the entities in an URL using the UrlEntityConverter
    """
    newUrl = re.sub("(%)([1234567890ABCDEF]{2})", UrlEntityConverter, url)
    return newUrl
    
#===============================================================================
def StripAmp (data):
    return replace(data, "&amp;","&")

#===============================================================================
def DoRegexFindAll(regex, data):
    try:
        result = re.compile(regex, re.DOTALL + re.IGNORECASE)
        return result.findall(data)
    except:
        logFile.critical('error regexing', exc_info=True)
        return []

#============================================================================== 
def DoSoupFindAll(data, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs):
    try:
        soup = beautifulsoup.BeautifulSoup(data)
        return soup.findAll(name, attrs, recursive, text, limit, **kwargs)
    except:
        logFile.debug("Error parsing using soup", exc_info=True)
        return []

#===============================================================================
def GetSkinFolder():
    skinName = xbmc.getSkinDir()
    if (os.path.exists(os.path.join(config.rootDir,"resources","skins",skinName))):
        skinFolder = skinName
    else:
        skinFolder = "Default"
    logFile.info("Setting Skin to: " + skinFolder)
    return skinFolder

#===============================================================================
def DirectoryPrinter(dir):
    try:
        version = xbmc.getInfoLabel("system.buildversion")
        buildDate = xbmc.getInfoLabel("system.builddate")
        env = envcontroller.EnvController().GetEnvironment(True)
        logFile.debug("XBMC Information: \nVersion: XBMC %s\nEnvironment: %s\nBuildDate: %s)", version, env, buildDate)
        
        dirWalker = os.walk(dir)
        dirPrint = "Folder Structure of %s" % (config.appName)
        
        excludePattern = os.path.join('a','.').replace("a","")
        for dir, folders, files in dirWalker:
            if dir.count(excludePattern) == 0:
                for file in files:
                    if not file.startswith(".") and not file.endswith(".pyo"):
                        dirPrint = "%s\n%s" % (dirPrint, os.path.join(dir, file))
        logFile.debug("%s" % (dirPrint))
    except:
        logFile.critical("Error printing folder %s", dir, exc_info=True)        
        
#===============================================================================
def CacheCleanUp():
    try:
        deleteCount = 0
        fileCount = 0
        for item in os.listdir(config.cacheDir):
            fileName = os.path.join(config.cacheDir, item)
            if os.path.isfile(fileName):
                fileCount = fileCount + 1
                createTime = os.path.getctime(fileName)
                if createTime + config.cacheValidTime < time.time():
                    os.remove(fileName)
                    deleteCount = deleteCount + 1
        logFile.info("Removed %s of %s files from cache.", deleteCount, fileCount)
    except:
        logFile.critical("Error cleaning the cachefolder", exc_info=True)    