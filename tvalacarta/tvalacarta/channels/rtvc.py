# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVC
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[rtvc.py] init")

DEBUG = False
CHANNELNAME = "rtvc"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtvc.py] mainlist")
    itemlist=[]

    # Empieza con el listado sólo de videos
    url="http://www.rtvc.es/television/emisiones/1.aspx"
    post="ctl00$content$ScriptManager1=ctl00$content$ScriptManager1|ctl00$content$imgVideos&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYGZg9kFgJmDw8WAh4HVmlzaWJsZWdkZAICD2QWBgIBDxYCHgVzdHlsZQUNZGlzcGxheTpub25lO2QCAw8WAh8BBQ9kaXNwbGF5OmlubGluZTtkAgUPFgIfAQUNZGlzcGxheTpub25lO2QCBA9kFg4CAw8PFgIeCEltYWdlVXJsBSIvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3RvZG8ucG5nZGQCBQ8PFgIfAgUrL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc192aWRlb19jaGVja2VkLnBuZ2RkAgcPDxYCHwIFIy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfYXVkaW8ucG5nZGQCCQ8PFgIfAgUjL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19mb3Rvcy5wbmdkZAILDw8WAh8CBSEvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3BkZi5wbmdkZAIND2QWAmYPZBYCAgEPEA8WBh4NRGF0YVRleHRGaWVsZAUFdmFsdWUeDkRhdGFWYWx1ZUZpZWxkBQNrZXkeC18hRGF0YUJvdW5kZ2QQFQ4VVG9kYXMgbGFzIGNhdGVnb3LDrWFzDEluZm9ybWF0aXZvcwRDaW5lCU1hZ2F6aW5lIAhEZXBvcnRlcwdNdXNpY2FsBUh1bW9yCEZvbGNsb3JlBlNlcmllcwpEb2N1bWVudGFsCEN1bHR1cmFsBU90cm9zCENhcm5hdmFsGUVzcGVjaWFsIETDrWEgZGUgQ2FuYXJpYXMVDgEwATEBMgE1ATYCMTECMjUCMjgENTAwNwQ1MDI1BDUwMjYENTA0NgQ1MDQ5BDUwNTEUKwMOZ2dnZ2dnZ2dnZ2dnZ2cWAWZkAg8PZBYCZg9kFgICAg88KwAJAQAPFgQeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AilkFlJmD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vMzAtbWludXRvcy05NDk0LmFzcHgKMzAgbWludXRvcwozMCBtaW51dG9zDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTQ5NC5hc3B4ZAIBD2QWAgIBDxUFMy90ZWxldmlzaW9uL2VtaXNpb24vYnVlbm9zLWTDrWFzLWNhbmFyaWFzLTExMjYuYXNweBZCdWVub3MgZMOtYXMsIENhbmFyaWFzGUJ1ZW5vcyBkw61hcywgQ2FuYXJpYXMuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMTI2LmFzcHhkAgIPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMS00Ni5hc3B4DlRlbGVub3RpY2lhcyAxEVRlbGVub3RpY2lhcyAxLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNDYuYXNweGQCAw9kFgICAQ8VBT0vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtZmluLWRlLXNlbWFuYS0xMDE1OC5hc3B4HkNhbmFyaWFzIEV4cHJlc3MgZmluIGRlIHNlbWFuYRNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNTguYXNweGQCBA9kFgICAQ8VBTkvdGVsZXZpc2lvbi9lbWlzaW9uL3RlbGVub3RpY2lhcy1maW4tZGUtc2VtYW5hLTEtMjg1LmFzcHgcVGVsZW5vdGljaWFzIEZpbiBkZSBzZW1hbmEgMRNUZWxlbm90aWNpYXMgRmluLi4uDEluZm9ybWF0aXZvcyEvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjg1LmFzcHhkAgUPZBYCAgEPFQU6L3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtZmluLWRlLXNlbWFuYS0yLTM3ODguYXNweBxUZWxlbm90aWNpYXMgRmluIGRlIHNlbWFuYSAyE1RlbGVub3RpY2lhcyBGaW4uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNzg4LmFzcHhkAgYPZBYCAgEPFQUsL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMi0xOTM3LmFzcHgOVGVsZW5vdGljaWFzIDIRVGVsZW5vdGljaWFzIDIuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xOTM3LmFzcHhkAgcPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMy05MC5hc3B4DlRlbGVub3RpY2lhcyAzEVRlbGVub3RpY2lhcyAzLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTAuYXNweGQCCA9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtMTAxNDguYXNweBBDYW5hcmlhcyBFeHByZXNzE0NhbmFyaWFzIEV4cHJlc3MuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE0OC5hc3B4ZAIJD2QWAgIBDxUFJy90ZWxldmlzaW9uL2VtaXNpb24vdG4tc29yZG9zLTkxMDIuYXNweAlUTiBzb3Jkb3MJVE4gc29yZG9zDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTEwMi5hc3B4ZAIKD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vZWwtZ3VzdG8tZXMtbcOtby04ODQyLmFzcHgQRWwgZ3VzdG8gZXMgbcOtbxNFbCBndXN0byBlcyBtw61vLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg0Mi5hc3B4ZAILD2QWAgIBDxUFLC90ZWxldmlzaW9uL2VtaXNpb24vZW4tY2xhdmUtZGUtamEtMzUwNi5hc3B4DkVuIGNsYXZlIGRlIEphEUVuIGNsYXZlIGRlIEphLi4uBUh1bW9yIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNTA2LmFzcHhkAgwPZBYCAgEPFQUuL3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlhcy1kaXJlY3RvLTExMDUuYXNweBBDYW5hcmlhcyBEaXJlY3RvE0NhbmFyaWFzIERpcmVjdG8uLi4JTWFnYXppbmUgIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMTA1LmFzcHhkAg0PZBYCAgEPFQUtL3RlbGV2aXNpb24vZW1pc2lvbi9sdWNoYS1jYW5hcmlhLXItODUxNS5hc3B4EUx1Y2hhIENhbmFyaWEgKFIpEEx1Y2hhIENhbmFyaWEuLi4IRGVwb3J0ZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg1MTUuYXNweGQCDg9kFgICAQ8VBScvdGVsZXZpc2lvbi9lbWlzaW9uL2VsLWVudml0ZS03ODAyLmFzcHgJRWwgZW52aXRlCUVsIGVudml0ZQxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzc4MDIuYXNweGQCDw9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL3BhcnJhbmRhLWNhbmFyaWEtMTAyOTcuYXNweBBQYXJyYW5kYSBjYW5hcmlhE1BhcnJhbmRhIGNhbmFyaWEuLi4HTXVzaWNhbCMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyOTcuYXNweGQCEA9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uL3RvZG8tZ29sZXMtMTEwNy5hc3B4ClRvZG8gR29sZXMKVG9kbyBHb2xlcwhEZXBvcnRlcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNy5hc3B4ZAIRD2QWAgIBDxUFMy90ZWxldmlzaW9uL2VtaXNpb24vcHJlbWlvcy1jYW5hcmlhcy0yMDEyLTkyNDcuYXNweBVQcmVtaW9zIENhbmFyaWFzIDIwMTITUHJlbWlvcyBDYW5hcmlhcy4uLghDdWx0dXJhbCIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTI0Ny5hc3B4ZAISD2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vbGEtcmV2b2x0b3NhLTk2MjguYXNweAxMYSBSZXZvbHRvc2EMTGEgUmV2b2x0b3NhBlNlcmllcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTYyOC5hc3B4ZAITD2QWAgIBDxUFMS90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZXhwcmVzcy0yLTEwMTQ5LmFzcHgSQ2FuYXJpYXMgRXhwcmVzcyAyE0NhbmFyaWFzIEV4cHJlc3MuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE0OS5hc3B4ZAIUD2QWAgIBDxUFRS90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlLWVzdGFkby1kZS1sYS1uYWNpb25hbGlkYWQtY2FuYXJpYS0xNTIuYXNweChEZWJhdGUgRXN0YWRvIGRlIGxhIE5hY2lvbmFsaWRhZCBDYW5hcmlhEERlYmF0ZSBFc3RhZG8uLi4MSW5mb3JtYXRpdm9zIS9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xNTIuYXNweGQCFQ9kFgICAQ8VBTkvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWF2YW5jZS1pbmZvcm1hdGl2by04NzczLmFzcHgbRXNwZWNpYWwgQXZhbmNlIGluZm9ybWF0aXZvEkVzcGVjaWFsIEF2YW5jZS4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg3NzMuYXNweGQCFg9kFgICAQ8VBSUvdGVsZXZpc2lvbi9lbWlzaW9uL2JvcmdpYS0xMDM2Ni5hc3B4BkJvcmdpYQZCb3JnaWEGU2VyaWVzIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM2Ni5hc3B4ZAIXD2QWAgIBDxUFPi90ZWxldmlzaW9uL2VtaXNpb24vY29uZmVyZW5jaWEtZGUtbcOzbmljYS10ZXJyaWJhcy0xMDM3Ny5hc3B4H0NvbmZlcmVuY2lhIGRlIE3Ds25pY2EgVGVycmliYXMRQ29uZmVyZW5jaWEgZGUuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM3Ny5hc3B4ZAIYD2QWAgIBDxUFLy90ZWxldmlzaW9uL2VtaXNpb24vYWdlbmRhLW3DoXMtY2luZS0xMDE5Ny5hc3B4EEFnZW5kYSBNw6FzIENpbmUTQWdlbmRhIE3DoXMgQ2luZS4uLgRDaW5lIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE5Ny5hc3B4ZAIZD2QWAgIBDxUFPC90ZWxldmlzaW9uL2VtaXNpb24vY2FiYWxnYXRhLWRlLXJleWVzLXNjLXRlbmVyaWZlLTM2MzMuYXNweB9DYWJhbGdhdGEgZGUgUmV5ZXMgUy9DIFRlbmVyaWZlFUNhYmFsZ2F0YSBkZSBSZXllcy4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMzYzMy5hc3B4ZAIaD2QWAgIBDxUFQC90ZWxldmlzaW9uL2VtaXNpb24vZXNwZWNpYWwtaW5mb3JtYXRpdm8tcmVzdW1lbi1hbnVhbC05Njg1LmFzcHgiRXNwZWNpYWwgaW5mb3JtYXRpdm8gcmVzdW1lbiBhbnVhbBdFc3BlY2lhbCBpbmZvcm1hdGl2by4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2ODUuYXNweGQCGw9kFgICAQ8VBU0vdGVsZXZpc2lvbi9lbWlzaW9uL21lbnNhamUtZGVsLXByZXNpZGVudGUtZGVsLWdvYmllcm5vLWRlLWNhbmFyaWFzLTg4NTIuYXNweC9NZW5zYWplIGRlbCBwcmVzaWRlbnRlIGRlbCBHb2JpZXJubyBkZSBDYW5hcmlhcxlNZW5zYWplIGRlbCBwcmVzaWRlbnRlLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg1Mi5hc3B4ZAIcD2QWAgIBDxUFJC90ZWxldmlzaW9uL2VtaXNpb24vcHJvbW9zLTg0MzYuYXNweAZQcm9tb3MGUHJvbW9zBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS84NDM2LmFzcHhkAh0PZBYCAgEPFQU9L3RlbGV2aXNpb24vZW1pc2lvbi9kZWJhdGVzLWNhbmRpZGF0b3MtYWwtY29uZ3Jlc28tMTAyMTUuYXNweB5EZWJhdGVzIGNhbmRpZGF0b3MgYWwgQ29uZ3Jlc28VRGViYXRlcyBjYW5kaWRhdG9zLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyMTUuYXNweGQCHg9kFgICAQ8VBT4vdGVsZXZpc2lvbi9lbWlzaW9uL29mcmVuZGEtcm9tZXLDrWEtdmlyZ2VuLWRlbC1waW5vLTI0NTguYXNweCBPZnJlbmRhIFJvbWVyw61hIFZpcmdlbiBkZWwgUGlubxNPZnJlbmRhIFJvbWVyw61hLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8yNDU4LmFzcHhkAh8PZBYCAgEPFQUrL3RlbGV2aXNpb24vZW1pc2lvbi8zMC1taW51dG9zLXItMTAxNTYuYXNweA4zMCBtaW51dG9zIChSKREzMCBtaW51dG9zIChSKS4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMTU2LmFzcHhkAiAPZBYCAgEPFQUoL3RlbGV2aXNpb24vZW1pc2lvbi9wYXJsYW1lbnRvLTc0MzEuYXNweApQYXJsYW1lbnRvClBhcmxhbWVudG8MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83NDMxLmFzcHhkAiEPZBYCAgEPFQVHL3RlbGV2aXNpb24vZW1pc2lvbi9kZWJhdGUtZXN0YWRvLWRlLWxhLW5hY2lvbmFsaWRhZC1jYW5hcmlhLTEwMzk5LmFzcHgoRGViYXRlIEVzdGFkbyBkZSBsYSBOYWNpb25hbGlkYWQgQ2FuYXJpYRBEZWJhdGUgRXN0YWRvLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAzOTkuYXNweGQCIg9kFgICAQ8VBTcvdGVsZXZpc2lvbi9lbWlzaW9uL2VudHJldmlzdGEtcGF1bGluby1yaXZlcm8tNjExMS5hc3B4GUVudHJldmlzdGEgUGF1bGlubyBSaXZlcm8VRW50cmV2aXN0YSBQYXVsaW5vLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNjExMS5hc3B4ZAIjD2QWAgIBDxUFQS90ZWxldmlzaW9uL2VtaXNpb24vZXNwZWNpYWwtaW5mb3JtYXRpdm8tcmVzdW1lbi1hbnVhbC0xMDI3MS5hc3B4IkVzcGVjaWFsIGluZm9ybWF0aXZvIHJlc3VtZW4gYW51YWwXRXNwZWNpYWwgaW5mb3JtYXRpdm8uLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDI3MS5hc3B4ZAIkD2QWAgIBDxUFMi90ZWxldmlzaW9uL2VtaXNpb24vcHJlbWllci1sYS1yZXZvbHRvc2EtOTY1My5hc3B4GFByZW1pZXIgJydMYSBSZXZvbHRvc2EnJxtQcmVtaWVyICcnTGEgUmV2b2x0b3NhJycuLi4FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2NTMuYXNweGQCJQ9kFgICAQ8VBTIvdGVsZXZpc2lvbi9lbWlzaW9uL3ByZW1pZXItbGEtcmV2b2x0b3NhLTk2NTYuYXNweBZQcmVtaWVyICdMYSBSZXZvbHRvc2EnGVByZW1pZXIgJ0xhIFJldm9sdG9zYScuLi4FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2NTYuYXNweGQCJg9kFgICAQ8VBTQvdGVsZXZpc2lvbi9lbWlzaW9uL2Fkw6FuLW1hcnTDrW4tZXNwZWNpYWwtOTQ0MC5hc3B4F0Fkw6FuIE1hcnTDrW4uIEVzcGVjaWFsGkFkw6FuIE1hcnTDrW4uIEVzcGVjaWFsLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTQ0MC5hc3B4ZAInD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vZG9uYWNjacOzbi04MTY0LmFzcHgKRG9uYWNjacOzbgpEb25hY2Npw7NuBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS84MTY0LmFzcHhkAigPZBYCAgEPFQUpL3RlbGV2aXNpb24vZW1pc2lvbi9kb25hY2Npw7NuLTEwNTI4LmFzcHgKRG9uYWNjacOzbgpEb25hY2Npw7NuBU90cm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDUyOC5hc3B4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBwUcY3RsMDAkbG9naW5idXR0b25zJGJ0bkVudmlhcgUeY3RsMDAkbG9naW5idXR0b25zJGNoYlJlY29yZGFyBRVjdGwwMCRjb250ZW50JGltZ1RvZG8FF2N0bDAwJGNvbnRlbnQkaW1nVmlkZW9zBRZjdGwwMCRjb250ZW50JGltZ0F1ZGlvBRZjdGwwMCRjb250ZW50JGltZ0ZvdG9zBRRjdGwwMCRjb250ZW50JGltZ1BERg%3D%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria=0&ctl00$content$typeselected=todo&ctl00$content$imgVideos.x=71&ctl00$content$imgVideos.y=20"
    
    # Descarga la página
    data = scrapertools.cache_page(url, post=post)
    #logger.info(data)

    # Extrae las categorías de vídeos
    '''
    <select name="ctl00$content$ddlEmisionesCategoria" onchange="javascript:setTimeout('__doPostBack(\'ctl00$content$ddlEmisionesCategoria\',\'\')', 0)" id="ctl00_content_ddlEmisionesCategoria" class="ddlEmisionesCategoria">
    <option selected="selected" value="0">Todas las categor&#237;as</option>
    <option value="1">Informativos</option>
    <option value="2">Cine</option>
    <option value="5">Magazine </option>
    <option value="6">Deportes</option>
    <option value="11">Musical</option>
    <option value="25">Humor</option>
    <option value="28">Folclore</option>
    <option value="5007">Series</option>
    <option value="5025">Documental</option>
    <option value="5026">Cultural</option>
    <option value="5046">Otros</option>
    <option value="5049">Carnaval</option>
    <option value="5051">Especial D&#237;a de Canarias</option>
        </select>
    '''
    print data    
    data = scrapertools.get_match( data , '<select name="ctl00\$content\$ddlEmisionesCategoria"[^>]+>(.*?)</select>' ).strip()
    #logger.info(data)
    patron  = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        # Atributos del vídeo
        scrapedtitle = match[1].strip()
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="programas" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show="" , category = scrapedtitle , folder=True) )

    return itemlist

def programas(item):
    logger.info("[rtvc.py] programlist")
    itemlist=[]

    # La url es el id del combo de categorías, lo pega dentro del DATA del POST
    post = "ctl00$content$ScriptManager1=ctl00$content$UpdatePanel1|ctl00$content$ddlEmisionesCategoria&__EVENTTARGET=ctl00%24content%24ddlEmisionesCategoria&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYGZg9kFgJmDw8WAh4HVmlzaWJsZWdkZAICD2QWBgIBDxYCHgVzdHlsZQUNZGlzcGxheTpub25lO2QCAw8WAh8BBQ9kaXNwbGF5OmlubGluZTtkAgUPFgIfAQUNZGlzcGxheTpub25lO2QCBA9kFg4CAw8PFgIeCEltYWdlVXJsBSIvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3RvZG8ucG5nZGQCBQ8PFgIfAgUrL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc192aWRlb19jaGVja2VkLnBuZ2RkAgcPDxYCHwIFIy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfYXVkaW8ucG5nZGQCCQ8PFgIfAgUjL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19mb3Rvcy5wbmdkZAILDw8WAh8CBSEvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3BkZi5wbmdkZAIND2QWAmYPZBYCAgEPEA8WBh4NRGF0YVRleHRGaWVsZAUFdmFsdWUeDkRhdGFWYWx1ZUZpZWxkBQNrZXkeC18hRGF0YUJvdW5kZ2QQFQoVVG9kYXMgbGFzIGNhdGVnb3LDrWFzBENpbmUIQ3VsdHVyYWwIRGVwb3J0ZXMFSHVtb3IMSW5mb3JtYXRpdm9zCU1hZ2F6aW5lIAdNdXNpY2FsBU90cm9zBlNlcmllcxUKATABMgQ1MDI2ATYCMjUBMQE1AjExBDUwNDYENTAwNxQrAwpnZ2dnZ2dnZ2dnFgFmZAIPD2QWAmYPZBYCAgIPPCsACQEADxYEHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudAIpZBZSZg9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uLzMwLW1pbnV0b3MtOTQ5NC5hc3B4CjMwIG1pbnV0b3MKMzAgbWludXRvcwxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk0OTQuYXNweGQCAQ9kFgICAQ8VBTMvdGVsZXZpc2lvbi9lbWlzaW9uL2J1ZW5vcy1kw61hcy1jYW5hcmlhcy0xMTI2LmFzcHgWQnVlbm9zIGTDrWFzLCBDYW5hcmlhcxlCdWVub3MgZMOtYXMsIENhbmFyaWFzLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEyNi5hc3B4ZAICD2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vdGVsZW5vdGljaWFzLTEtNDYuYXNweA5UZWxlbm90aWNpYXMgMRFUZWxlbm90aWNpYXMgMS4uLgxJbmZvcm1hdGl2b3MgL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzQ2LmFzcHhkAgMPZBYCAgEPFQU9L3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlhcy1leHByZXNzLWZpbi1kZS1zZW1hbmEtMTAxNTguYXNweB5DYW5hcmlhcyBFeHByZXNzIGZpbiBkZSBzZW1hbmETQ2FuYXJpYXMgRXhwcmVzcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMTU4LmFzcHhkAgQPZBYCAgEPFQU5L3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtZmluLWRlLXNlbWFuYS0xLTI4NS5hc3B4HFRlbGVub3RpY2lhcyBGaW4gZGUgc2VtYW5hIDETVGVsZW5vdGljaWFzIEZpbi4uLgxJbmZvcm1hdGl2b3MhL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzI4NS5hc3B4ZAIFD2QWAgIBDxUFOi90ZWxldmlzaW9uL2VtaXNpb24vdGVsZW5vdGljaWFzLWZpbi1kZS1zZW1hbmEtMi0zNzg4LmFzcHgcVGVsZW5vdGljaWFzIEZpbiBkZSBzZW1hbmEgMhNUZWxlbm90aWNpYXMgRmluLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMzc4OC5hc3B4ZAIGD2QWAgIBDxUFLC90ZWxldmlzaW9uL2VtaXNpb24vdGVsZW5vdGljaWFzLTItMTkzNy5hc3B4DlRlbGVub3RpY2lhcyAyEVRlbGVub3RpY2lhcyAyLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTkzNy5hc3B4ZAIHD2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vdGVsZW5vdGljaWFzLTMtOTAuYXNweA5UZWxlbm90aWNpYXMgMxFUZWxlbm90aWNpYXMgMy4uLgxJbmZvcm1hdGl2b3MgL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzkwLmFzcHhkAggPZBYCAgEPFQUvL3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlhcy1leHByZXNzLTEwMTQ4LmFzcHgQQ2FuYXJpYXMgRXhwcmVzcxNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNDguYXNweGQCCQ9kFgICAQ8VBScvdGVsZXZpc2lvbi9lbWlzaW9uL3RuLXNvcmRvcy05MTAyLmFzcHgJVE4gc29yZG9zCVROIHNvcmRvcwxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzkxMDIuYXNweGQCCg9kFgICAQ8VBS4vdGVsZXZpc2lvbi9lbWlzaW9uL2VsLWd1c3RvLWVzLW3DrW8tODg0Mi5hc3B4EEVsIGd1c3RvIGVzIG3DrW8TRWwgZ3VzdG8gZXMgbcOtby4uLglNYWdhemluZSAiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg4NDIuYXNweGQCCw9kFgICAQ8VBSwvdGVsZXZpc2lvbi9lbWlzaW9uL2VuLWNsYXZlLWRlLWphLTM1MDYuYXNweA5FbiBjbGF2ZSBkZSBKYRFFbiBjbGF2ZSBkZSBKYS4uLgVIdW1vciIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMzUwNi5hc3B4ZAIMD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZGlyZWN0by0xMTA1LmFzcHgQQ2FuYXJpYXMgRGlyZWN0bxNDYW5hcmlhcyBEaXJlY3RvLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNS5hc3B4ZAIND2QWAgIBDxUFLS90ZWxldmlzaW9uL2VtaXNpb24vbHVjaGEtY2FuYXJpYS1yLTg1MTUuYXNweBFMdWNoYSBDYW5hcmlhIChSKRBMdWNoYSBDYW5hcmlhLi4uCERlcG9ydGVzIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS84NTE1LmFzcHhkAg4PZBYCAgEPFQUnL3RlbGV2aXNpb24vZW1pc2lvbi9lbC1lbnZpdGUtNzgwMi5hc3B4CUVsIGVudml0ZQlFbCBlbnZpdGUMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83ODAyLmFzcHhkAg8PZBYCAgEPFQUvL3RlbGV2aXNpb24vZW1pc2lvbi9wYXJyYW5kYS1jYW5hcmlhLTEwMjk3LmFzcHgQUGFycmFuZGEgY2FuYXJpYRNQYXJyYW5kYSBjYW5hcmlhLi4uB011c2ljYWwjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjk3LmFzcHhkAhAPZBYCAgEPFQUoL3RlbGV2aXNpb24vZW1pc2lvbi90b2RvLWdvbGVzLTExMDcuYXNweApUb2RvIEdvbGVzClRvZG8gR29sZXMIRGVwb3J0ZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzExMDcuYXNweGQCEQ9kFgICAQ8VBTMvdGVsZXZpc2lvbi9lbWlzaW9uL3ByZW1pb3MtY2FuYXJpYXMtMjAxMi05MjQ3LmFzcHgVUHJlbWlvcyBDYW5hcmlhcyAyMDEyE1ByZW1pb3MgQ2FuYXJpYXMuLi4IQ3VsdHVyYWwiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzkyNDcuYXNweGQCEg9kFgICAQ8VBSovdGVsZXZpc2lvbi9lbWlzaW9uL2xhLXJldm9sdG9zYS05NjI4LmFzcHgMTGEgUmV2b2x0b3NhDExhIFJldm9sdG9zYQZTZXJpZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2MjguYXNweGQCEw9kFgICAQ8VBTEvdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtMi0xMDE0OS5hc3B4EkNhbmFyaWFzIEV4cHJlc3MgMhNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNDkuYXNweGQCFA9kFgICAQ8VBUUvdGVsZXZpc2lvbi9lbWlzaW9uL2RlYmF0ZS1lc3RhZG8tZGUtbGEtbmFjaW9uYWxpZGFkLWNhbmFyaWEtMTUyLmFzcHgoRGViYXRlIEVzdGFkbyBkZSBsYSBOYWNpb25hbGlkYWQgQ2FuYXJpYRBEZWJhdGUgRXN0YWRvLi4uDEluZm9ybWF0aXZvcyEvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTUyLmFzcHhkAhUPZBYCAgEPFQU5L3RlbGV2aXNpb24vZW1pc2lvbi9lc3BlY2lhbC1hdmFuY2UtaW5mb3JtYXRpdm8tODc3My5hc3B4G0VzcGVjaWFsIEF2YW5jZSBpbmZvcm1hdGl2bxJFc3BlY2lhbCBBdmFuY2UuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS84NzczLmFzcHhkAhYPZBYCAgEPFQUlL3RlbGV2aXNpb24vZW1pc2lvbi9ib3JnaWEtMTAzNjYuYXNweAZCb3JnaWEGQm9yZ2lhBlNlcmllcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAzNjYuYXNweGQCFw9kFgICAQ8VBT4vdGVsZXZpc2lvbi9lbWlzaW9uL2NvbmZlcmVuY2lhLWRlLW3Ds25pY2EtdGVycmliYXMtMTAzNzcuYXNweB9Db25mZXJlbmNpYSBkZSBNw7NuaWNhIFRlcnJpYmFzEUNvbmZlcmVuY2lhIGRlLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAzNzcuYXNweGQCGA9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2FnZW5kYS1tw6FzLWNpbmUtMTAxOTcuYXNweBBBZ2VuZGEgTcOhcyBDaW5lE0FnZW5kYSBNw6FzIENpbmUuLi4EQ2luZSMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxOTcuYXNweGQCGQ9kFgICAQ8VBTwvdGVsZXZpc2lvbi9lbWlzaW9uL2NhYmFsZ2F0YS1kZS1yZXllcy1zYy10ZW5lcmlmZS0zNjMzLmFzcHgfQ2FiYWxnYXRhIGRlIFJleWVzIFMvQyBUZW5lcmlmZRVDYWJhbGdhdGEgZGUgUmV5ZXMuLi4FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzM2MzMuYXNweGQCGg9kFgICAQ8VBUAvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtOTY4NS5hc3B4IkVzcGVjaWFsIGluZm9ybWF0aXZvIHJlc3VtZW4gYW51YWwXRXNwZWNpYWwgaW5mb3JtYXRpdm8uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85Njg1LmFzcHhkAhsPZBYCAgEPFQVNL3RlbGV2aXNpb24vZW1pc2lvbi9tZW5zYWplLWRlbC1wcmVzaWRlbnRlLWRlbC1nb2JpZXJuby1kZS1jYW5hcmlhcy04ODUyLmFzcHgvTWVuc2FqZSBkZWwgcHJlc2lkZW50ZSBkZWwgR29iaWVybm8gZGUgQ2FuYXJpYXMZTWVuc2FqZSBkZWwgcHJlc2lkZW50ZS4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg4NTIuYXNweGQCHA9kFgICAQ8VBSQvdGVsZXZpc2lvbi9lbWlzaW9uL3Byb21vcy04NDM2LmFzcHgGUHJvbW9zBlByb21vcwVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODQzNi5hc3B4ZAIdD2QWAgIBDxUFPS90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlcy1jYW5kaWRhdG9zLWFsLWNvbmdyZXNvLTEwMjE1LmFzcHgeRGViYXRlcyBjYW5kaWRhdG9zIGFsIENvbmdyZXNvFURlYmF0ZXMgY2FuZGlkYXRvcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjE1LmFzcHhkAh4PZBYCAgEPFQU%2BL3RlbGV2aXNpb24vZW1pc2lvbi9vZnJlbmRhLXJvbWVyw61hLXZpcmdlbi1kZWwtcGluby0yNDU4LmFzcHggT2ZyZW5kYSBSb21lcsOtYSBWaXJnZW4gZGVsIFBpbm8TT2ZyZW5kYSBSb21lcsOtYS4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjQ1OC5hc3B4ZAIfD2QWAgIBDxUFKy90ZWxldmlzaW9uL2VtaXNpb24vMzAtbWludXRvcy1yLTEwMTU2LmFzcHgOMzAgbWludXRvcyAoUikRMzAgbWludXRvcyAoUikuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE1Ni5hc3B4ZAIgD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vcGFybGFtZW50by03NDMxLmFzcHgKUGFybGFtZW50bwpQYXJsYW1lbnRvDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNzQzMS5hc3B4ZAIhD2QWAgIBDxUFRy90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlLWVzdGFkby1kZS1sYS1uYWNpb25hbGlkYWQtY2FuYXJpYS0xMDM5OS5hc3B4KERlYmF0ZSBFc3RhZG8gZGUgbGEgTmFjaW9uYWxpZGFkIENhbmFyaWEQRGViYXRlIEVzdGFkby4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMzk5LmFzcHhkAiIPZBYCAgEPFQU3L3RlbGV2aXNpb24vZW1pc2lvbi9lbnRyZXZpc3RhLXBhdWxpbm8tcml2ZXJvLTYxMTEuYXNweBlFbnRyZXZpc3RhIFBhdWxpbm8gUml2ZXJvFUVudHJldmlzdGEgUGF1bGluby4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzYxMTEuYXNweGQCIw9kFgICAQ8VBUEvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtMTAyNzEuYXNweCJFc3BlY2lhbCBpbmZvcm1hdGl2byByZXN1bWVuIGFudWFsF0VzcGVjaWFsIGluZm9ybWF0aXZvLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyNzEuYXNweGQCJA9kFgICAQ8VBTIvdGVsZXZpc2lvbi9lbWlzaW9uL3ByZW1pZXItbGEtcmV2b2x0b3NhLTk2NTMuYXNweBhQcmVtaWVyICcnTGEgUmV2b2x0b3NhJycbUHJlbWllciAnJ0xhIFJldm9sdG9zYScnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjUzLmFzcHhkAiUPZBYCAgEPFQUyL3RlbGV2aXNpb24vZW1pc2lvbi9wcmVtaWVyLWxhLXJldm9sdG9zYS05NjU2LmFzcHgWUHJlbWllciAnTGEgUmV2b2x0b3NhJxlQcmVtaWVyICdMYSBSZXZvbHRvc2EnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjU2LmFzcHhkAiYPZBYCAgEPFQU0L3RlbGV2aXNpb24vZW1pc2lvbi9hZMOhbi1tYXJ0w61uLWVzcGVjaWFsLTk0NDAuYXNweBdBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbBpBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbC4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk0NDAuYXNweGQCJw9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uL2RvbmFjY2nDs24tODE2NC5hc3B4CkRvbmFjY2nDs24KRG9uYWNjacOzbgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODE2NC5hc3B4ZAIoD2QWAgIBDxUFKS90ZWxldmlzaW9uL2VtaXNpb24vZG9uYWNjacOzbi0xMDUyOC5hc3B4CkRvbmFjY2nDs24KRG9uYWNjacOzbgVPdHJvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTA1MjguYXNweGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgcFHGN0bDAwJGxvZ2luYnV0dG9ucyRidG5FbnZpYXIFHmN0bDAwJGxvZ2luYnV0dG9ucyRjaGJSZWNvcmRhcgUVY3RsMDAkY29udGVudCRpbWdUb2RvBRdjdGwwMCRjb250ZW50JGltZ1ZpZGVvcwUWY3RsMDAkY29udGVudCRpbWdBdWRpbwUWY3RsMDAkY29udGVudCRpbWdGb3RvcwUUY3RsMDAkY29udGVudCRpbWdQREY%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria="+item.url+"&ctl00$content$typeselected=video&"
    url="http://www.rtvc.es/television/emisiones/1.aspx"
    
    # Descarga la página
    data = scrapertools.cache_page(url,post=post)
    logger.info(data)

    # Extrae los programas
    patron  = '<div class="emision">[^<]+'
    patron += '<div class="photo">[^<]+'
    patron += '<img id="[^"]+" src="/handlers/ThumbnailHandler.ashx\?width=90\&amp\;height=60\&amp\;fill=False\&amp\;src=([^"]+)"[^>]+>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="data">[^<]+'
    patron += '<a class="title" href="([^"]+)">[^<]+'
    patron += '<span id="title" title="([^"]+)">[^<]+</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        # Atributos del vídeo
        scrapedtitle = match[2].strip()
        scrapedurl = urlparse.urljoin(url,match[1])
        # /handlers/ThumbnailHandler.ashx?width=90&amp;height=60&amp;fill=False&amp;src=
        #scrapedthumbnail = urlparse.urljoin(url,match[0].replace("&amp;","&"))
        scrapedthumbnail = urlparse.urljoin(url,match[0].replace(" ","%20"))
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[rtvc.py] episodios")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae la tabla de los vídeos
    patron  = '<table id="emisiones"[^>]+>.*?<tbody>(.*?)</tbody>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        data = matches[0]
    
    '''
    <tr>
    <td>Capítulo 5 (Primera Temporada)</td>
    <td>Video</td>
    <td>05/01/2012</td>
    <td class="play"><a id="ctl00_content_repEmisiones_ctl09_lnkAction" href="javascript:PopupCenter('/television/diferido.aspx?id=9628&amp;fichero=kTJ6IrZOrIQ','Diferido','745','548')"><img src="/images/web/btn_emisiones_play.png" style="border-width:0px;" /></a></td>
    <td class="download"></td>
    </tr>
    '''

    patron  = '<tr>[^<]+'
    patron += '<td>([^<]+)</td>[^<]+'
    patron += '<td>Video</td>[^<]+'
    patron += '<td>([^<]+)</td>[^<]+'
    patron += '<td class="play"><a id="[^"]+" href="javascript\:PopupCenter\(\'([^\']+)\'[^"]+"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for title,fecha,url in matches:
        # Atributos del vídeo
        scrapedtitle = title.strip()
        logger.info("url="+url)
        scrapedthumbnail = ""
        scrapedplot = ""
        try:
            youtube_id = scrapertools.get_match(url,"fichero\=([0-9A-Za-z_-]{11})$")
            scrapedurl = "http://www.youtube.com/watch?v="+youtube_id
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = item.show+" "+scrapedtitle, action="play" , server="youtube" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=False) )
        except:
            scrapedurl = urlparse.urljoin(item.url,url)
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = item.show+" "+scrapedtitle, action="play" , server="directo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=False) )

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")


    return itemlist

def play(item):
    logger.info("[rtvc.py] play")
    itemlist = []

    if item.server=="youtube":
        itemlist.append(item)
    else:
        # Descarga la página
        url = item.url.replace("&amp;","&").replace(" ","%20")
        logger.info("[rtvc.py] url="+url)
        data = scrapertools.cache_page(url)
        patron  = '<input type="hidden" id="hidden_url" value=\'([^\']+)\''
        matches = re.compile(patron,re.DOTALL).findall(data)
        url = matches[0].replace(" ","%20")
        logger.info("[rtvc.py] url="+url)
    
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , show = item.show , category = item.category , folder=False) )

    return itemlist