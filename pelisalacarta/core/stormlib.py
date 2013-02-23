# -*- coding: utf-8 -*-                                                                                                                                                        
#------------------------------------------------------------                                                                                                                     
# pelisalacarta - XBMC Plugin                                                                                                                                                     
# libreria para stormtv                                                                                                                                                         
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/                                                                                                                          
#------------------------------------------------------------                                                                                                                     
import urlparse,urllib2,urllib,re
import xml.dom.minidom as minidom                                                                                                                                                 
import urllib                                                                                                                                                                     
import os
from core import config
__server__ = "oc1.lopezepol.com"

def addfollow(tvs_id):
    print "[stormlib.py] addfollow "+config.get_data_path()
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    server= "https://"+__server__+"/stormtv/public/"
    path=config.get_data_path()+"stormtv/temp/"                                
    urllib.urlretrieve (server+"tvseries/addfollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, path+"temp.xml")
    print "[stormlib.py] addfollow"

def removefollow(tvs_id):
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    server= "https://"+__server__+"/stormtv/public/"
    path=config.get_data_path()+"stormtv/temp/"
    urllib.urlretrieve (server+"tvseries/removefollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, path+"temp.xml")
    print "[stormlib.py] Remove follow"

def iswatched(title,chap_dictionary):
    patronchap="([0-9](x|X)[0-9]*)"                                                                                                                                                 
    matcheschap= re.compile(patronchap,re.DOTALL).findall(title)                                                                                                              
    if (len(matcheschap)>0):
    	print matcheschap[0][0]                                                                                                                                                     
    	if (matcheschap[0][0].lower() in chap_dictionary):                                                                                                                                   
       		status=chap_dictionary[matcheschap[0][0].lower()].encode("utf-8")                                                                                                                    
       		#print status                                                                                                                                                      
       		title=title+" ["+status+"]"                                                                                                                                               
       		#print chap_dictionary[matcheschap[0]]+"#"
    return title, matcheschap[0][0].lower()

def getwatched(tvs_id):
    print "[stormlib.py] getwatched"+tvs_id
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    chap_dictionary = {}                                                                                                                                                          
    server= "https://"+__server__+"/stormtv/public/"                                                                                                                               
    path=config.get_data_path()+"stormtv/temp/"                                                                                            
    urllib.urlretrieve (server+"chapters/getstatus/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, path+"temp.xml")                                                              
    xml=path+"/"+"temp.xml"                                                                                                                                                       
    doc = minidom.parse(xml)                                                                                                                                                      
    node = doc.documentElement                                                                                                                                                    
    chapters = doc.getElementsByTagName("chapter")                                                                                                                                
    for chapter in chapters:                                                                                                                                                      
        number = chapter.getElementsByTagName("number")[0].childNodes[0].data                                                                                                 
        status = chapter.getElementsByTagName("status")[0].childNodes[0].data                                                                                                 
        chap_dictionary[number]=status                                                                                                                                        
        print number+chap_dictionary[number]+"#"
    return chap_dictionary

def setwatched (tvs_id,chap_number):
    print"[stormlib.py] setwatched"+tvs_id+" "+chap_number
    user_id=config.get_setting("stormtvuser")
    user_pass=config.get_setting("stormtvpassword")
    server= "https://"+__server__+"/stormtv/public/"                                                                                                                               
    path=config.get_data_path()+"stormtv/temp/"
    print"[stormlib.py] setwatched "+server+"chapters/add/tvs/"+tvs_id+"/user/"+user_id+"/pass/"+user_pass+"/chap/"+chap_number
    urllib.urlretrieve (server+"chapters/add/tvs/"+tvs_id+"/user/"+user_id+"/pass/"+user_pass+"/chap/"+chap_number, path+"temp.xml")                                          
    
    
def isfollow (tvs_id):
    print "[stormlib.py] isfollow"+ tvs_id
    user_id=config.get_setting("stormtvuser")                                                                                                   
    user_pass=config.get_setting("stormtvpassword")
    server= "https://"+__server__+"/stormtv/public/"
    # Create data_path if not exists
    path=config.get_data_path()+"stormtv/temp/"                                
    if not os.path.exists(path):                         
       print "Creating data_path "+path                                                             
       try:                                                        
           os.mkdir(path)                               
       except:                                            
           pass                                                                                                                                
    urllib.urlretrieve (server+"tvseries/isfollow/user/"+user_id+"/pass/"+user_pass+"/tvs/"+tvs_id, path+"temp.xml")
    xml=path+"/"+"temp.xml"                                                                                                                        
    doc = minidom.parse(xml)                                                                                                                       
    node = doc.documentElement                                                                                                                 
    follow = doc.getElementsByTagName("follow")
    status = follow[0].childNodes[0].data
    print status
    return status

