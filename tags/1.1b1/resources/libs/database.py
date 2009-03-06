import os, sys
#sys.path.append(os.path.join(os.getcwd().replace(";",""),'libs'))
from pysqlite2 import dbapi2 as sqlite
import config
import common

logFile = sys.modules['__main__'].globalLogFile

#===============================================================================
# Database Handler class
#===============================================================================
class DatabaseHandler:
    def __init__(self):
        """
            initialize the DB connection
        """
        self.xotDatabase = sqlite.connect(config.xotDbFile)
        self.CheckDatabaseExistence()
        pass
    
    #============================================================================== 
    # Database creation 
    #============================================================================== 
    def CheckDatabaseExistence(self):
        """
            Checks if the database exists, if not, it will be created.
        """
        sql = "PRAGMA table_info('favorites')"
        results = self.ExecuteQuery(sql)
        
        # check if DB exists
        if len(results) < 1:
            self.CreateDatabase()
            # reload the query
            results = self.ExecuteQuery(sql)
        
        # Check for GUID column
        columnGuidExists = False
        for result in results:
            if result[1] == "guid":
                logFile.debug("Database: Guid column already present in favorites table.")
                columnGuidExists = True
                break
        if not (columnGuidExists):            
            logFile.debug("Database: Creating column guid")
            sql = "ALTER TABLE favorites ADD COLUMN guid"
            self.ExecuteNonQuery(sql, commit=True)
        
    #============================================================================== 
    def CreateDatabase(self):
        """
            Creates a functional database
        """
        logFile.info("Creating Database")
        sql = 'PRAGMA encoding = "UTF-16"'
        self.ExecuteNonQuery(sql, True)
        sql = "CREATE TABLE favorites (channel string, name string, url string)"
        self.ExecuteNonQuery(sql)
        sql = "CREATE TABLE settings (setting string, value string)"
        self.ExecuteNonQuery(sql)
    
    #==============================================================================
    def UpgradeFrom310(self, channel):
        sql = "UPDATE favorites SET guid='%s' where channel='%s'" % (channel.guid, channel.channelName)
        self.ExecuteNonQuery(sql, commit=True)
            
    
    #===============================================================================
    #    Favorites Methodes
    #===============================================================================
    def AddFavorite(self, name, url, channel):
        logFile.debug("Adding favorite '%s' for channel '%s' with guid '%s' and url '%s'", name, channel.channelName, channel.guid, url)
        sql = u"INSERT INTO favorites (name, url, guid) VALUES(?, ?, ?)"
        params = (name, url, channel.guid)
        logFile.debug(params)
        self.ExecuteNonQuery(sql, params=params)
    
    #==============================================================================
    def LoadFavorites(self, channel):
        logFile.debug("Loading favorites")
        items = []
        
        self.UpgradeFrom310(channel)
        
        sql = "SELECT name, url FROM favorites WHERE guid='%s'" % (channel.guid)
        rows = self.ExecuteQuery(sql)
        
        for row in rows:            
            item = common.clistItem(row[0], row[1])
            items.append(item)
        
        return items
    
    #============================================================================== 
    def DeleteFavorites(self, name, url, channel):
        logFile.debug("Deleting favorite %s (%s)", name, url)
        query = "DELETE FROM favorites WHERE name=? AND url=? AND guid=?"
        self.ExecuteNonQuery(query, commit=True, params=(name, url, channel.guid))
        return
    
    #===============================================================================
    # Query Methods 
    #===============================================================================
    def ExecuteNonQuery(self, query, commit=True, params = []):
        """
            Executes and commits (if true) a sql statement to the database.
            Returns nothing, as it does not expect any results
        """
        
        # decode to unicode
        uParams = []
        for param in params:
            uParams.append(param.decode('iso-8859-1'))
        
        cursor = self.xotDatabase.cursor()
        if len(params) > 0:
            cursor.execute(query, uParams)
        else:
            cursor.execute(query)
        
        if commit:
            self.xotDatabase.commit()
    
    def ExecuteQuery(self, query, commit=False, params = []):
        """
            Executs and commits (if true) a sql statement to the database.
            Returns a row-set
        """
        
        # decode to unicode
        uParams = []
        for param in params:
            uParams.append(param.decode('iso-8859-1'))
        
        cursor = self.xotDatabase.cursor()
        if len(params) > 0:
            cursor.execute(query, uParams)
        else:
            cursor.execute(query)        
        
        if commit:
            self.xotDatabase.commit()
        
        return cursor.fetchall()