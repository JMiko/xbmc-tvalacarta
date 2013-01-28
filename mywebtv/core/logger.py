# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Módulo de logging - xbmc dharma/eden
#------------------------------------------------------------

import xbmc
import urllib

def info(texto):
    try:
        xbmc.log(texto)
    except:
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~."
        stripped = ''.join(c for c in texto if c in validchars)
        xbmc.log("(stripped) "+stripped)

def debug(texto):
    try:
        xbmc.log(texto)
    except:
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~."
        stripped = ''.join(c for c in texto if c in validchars)
        xbmc.log("(stripped) "+stripped)

def error(texto):
    try:
        xbmc.log(texto)
    except:
        validchars = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'()-@[]^_`{}~."
        stripped = ''.join(c for c in texto if c in validchars)
        xbmc.log("(stripped) "+stripped)
