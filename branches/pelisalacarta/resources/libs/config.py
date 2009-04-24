import os, logging

rootDir = os.getcwd().replace(";","")
rootDir = os.path.join(rootDir, '')

cacheDir = os.path.join(rootDir,'cache','')

cacheValidTime = 7*24*3600
webTimeOut = 30

appName = "pelisalacarta"
appSkin = "progwindow.xml"
contextMenuSkin = "uzg-contextmenu.xml"
updaterSkin = "xot-updater.xml"

logLevel = logging.DEBUG
logDual = True
logFileName = "pelisalacarta.log"
logFileNamePlugin = "pelisalacartaPlugin.log"

xotDbFile = os.path.join(rootDir,"pelisalacarta.db")

version = "3.2.0b2"
updateUrl = ""

skinFolder = "" #get's set from default.py

checkforupdates = True