import os, platform, sys

class EnvController:
    def __init__(self):
        """
            Class to determine platform depended stuff
        """
        pass
    
    def GetEnvironment(self, displayOnly = False):
        """
            Get the environment type of the current Python
        """
        #print "os.environ"
        #print platform.architecture()
        env = os.environ.get( "OS", "win32" )
        #print env
        
        if env == "Linux":
            (bits, type) = platform.architecture()
            if bits.count("64") > 0:
                # first the bits of platform.architecture is checked
                return "Linux64"
            elif sys.maxint >> 33:
                # double check using the sys.maxint
                # and see if more than 32 bits are present
                return "Linux64"
            else:
                return "Linux"
        elif env == "OS X":
            return "OS X"
        else: 
            if displayOnly and not env == "win32":
                print "Setting XOT Environment to %s" % env
                return env
            else:
                print "Setting XOT Environment to Win32"
                return "win32"