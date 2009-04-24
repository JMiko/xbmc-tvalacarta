import os
import config

def getConfigValue(name, defaultValue):

	valor = defaultValue

	# Lee el fichero de configuracion
	configfilepath = os.path.join(config.rootDir,'parameters.ini')
	#logFile.info("configfilepath="+configfilepath)
	configfile = open(configfilepath)
	lines = configfile.readlines()
	configfile.close();

	for line in lines:
		#print "line=" , line
		if line.startswith(name):
			valor = line.split("=")[1]
			if valor.endswith("\n"):
				valor = valor[:-1]
			if valor.endswith("\r"):
				valor = valor[:-1]

	return valor

def setConfigValue(name, newvalue):

	# Lee el fichero de configuracion
	configfilepath = os.path.join(config.rootDir,'parameters.ini')
	#logFile.info("configfilepath="+configfilepath)
	configfile = open(configfilepath)
	lines = configfile.readlines()
	configfile.close();

	outfile = open(configfilepath,"w")

	for line in lines:
		#print "line=" , line
		if line.startswith(name):
			#logFile.info(name+"="+newvalue)
			outfile.write(name+"="+newvalue)
		else:
			#logFile.info(line)
			outfile.write(line)
	
	outfile.flush()
	outfile.close()

'''
print getConfigValue("all.use.long.filenames","True")=="True"
print getConfigValue("all.use.long.filenames","True")!="True"
print getConfigValue("all.use.long.filenames","True")

destFolder = getConfigValue("rtve.download.path","test.dir")
print destFolder
setConfigValue("rtve.download.path",destFolder + "modificado")

print getConfigValue("rtve.download.path","test.dir")
'''
