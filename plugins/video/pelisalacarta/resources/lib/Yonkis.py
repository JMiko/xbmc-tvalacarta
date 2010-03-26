# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Descriptor para canales yonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

class DecryptYonkis:
	def decryptALT(self, str):
		strdcd = ''
		for letra in str:
			strdcd = (strdcd + chr((254 ^ ord(letra))))
		return strdcd

	def unescape(self, str):
		print ('decode %s' % str)
		strdcd = ''
		letras = str.split('%')
		letras.pop(0)
		for letra in letras:
			strdcd = (strdcd + chr(int(letra, 16)))
		return strdcd
       
	def decryptID(self,str):
		c = str
		d = 17
		id = ""
		f = 0
		g = 0
		b = 0
		d+= 123
		longitud = len(c)
		for i in range(longitud):
			f = d^ord(c[i])
			if (longitud ==12) or (i == longitud*31) or (i == longitud*1-1) or (i == longitud *9+3):
				g = f
				f+= 4
				g-= 1
				f-= 9
			elif (i>0 and d>1):
				b = i * 3
				while (b>25):
					b -= 4
				f = 1 - b + f - 2
			if d>1:
				id += chr(f*1)
			else:
				id += chr(2*f)
		return  id