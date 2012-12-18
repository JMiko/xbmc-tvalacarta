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
    url="http://rtvc.es/television/emisiones/1.aspx"
    post="ctl00$content$ScriptManager1=ctl00$content$ScriptManager1|ctl00$content$imgVideos&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYEAgMPZBYGAgEPFgIeBXN0eWxlBQ1kaXNwbGF5Om5vbmU7ZAIDDxYCHwAFD2Rpc3BsYXk6aW5saW5lO2QCBQ8WAh8ABQ1kaXNwbGF5Om5vbmU7ZAIFD2QWDgIDDw8WAh4ISW1hZ2VVcmwFIi9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfdG9kby5wbmdkZAIFDw8WAh8BBSsvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3ZpZGVvX2NoZWNrZWQucG5nZGQCBw8PFgIfAQUjL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19hdWRpby5wbmdkZAIJDw8WAh8BBSMvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX2ZvdG9zLnBuZ2RkAgsPDxYCHwEFIS9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfcGRmLnBuZ2RkAg0PZBYCZg9kFgICAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQV2YWx1ZR4ORGF0YVZhbHVlRmllbGQFA2tleR4LXyFEYXRhQm91bmRnZBAVDhVUb2RhcyBsYXMgY2F0ZWdvcsOtYXMMSW5mb3JtYXRpdm9zBENpbmUJTWFnYXppbmUgCERlcG9ydGVzB011c2ljYWwFSHVtb3IIRm9sY2xvcmUGU2VyaWVzCkRvY3VtZW50YWwIQ3VsdHVyYWwFT3Ryb3MIQ2FybmF2YWwZRXNwZWNpYWwgRMOtYSBkZSBDYW5hcmlhcxUOATABMQEyATUBNgIxMQIyNQIyOAQ1MDA3BDUwMjUENTAyNgQ1MDQ2BDUwNDkENTA1MRQrAw5nZ2dnZ2dnZ2dnZ2dnZxYBZmQCDw9kFgJmD2QWAgICDzwrAAkBAA8WBB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQCKWQWUmYPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMS00Ni5hc3B4DlRlbGVub3RpY2lhcyAxEVRlbGVub3RpY2lhcyAxLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNDYuYXNweGQCAQ9kFgICAQ8VBSwvdGVsZXZpc2lvbi9lbWlzaW9uL3RlbGVub3RpY2lhcy0yLTE5MzcuYXNweA5UZWxlbm90aWNpYXMgMhFUZWxlbm90aWNpYXMgMi4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzE5MzcuYXNweGQCAg9kFgICAQ8VBSkvdGVsZXZpc2lvbi9lbWlzaW9uL3RuLTctaXNsYXMtMTA2MDIuYXNweApUbiA3IElzbGFzClRuIDcgSXNsYXMMSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDYwMi5hc3B4ZAIDD2QWAgIBDxUFJy90ZWxldmlzaW9uL2VtaXNpb24vZWwtZW52aXRlLTc4MDIuYXNweAlFbCBlbnZpdGUJRWwgZW52aXRlDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNzgwMi5hc3B4ZAIED2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vZWwtZW52aXRlLXItMTA3MDIuYXNweA1FbCBlbnZpdGUgKFIpDUVsIGVudml0ZSAoUikMSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDcwMi5hc3B4ZAIFD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZGlyZWN0by0xMTA1LmFzcHgQQ2FuYXJpYXMgRGlyZWN0bxNDYW5hcmlhcyBEaXJlY3RvLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNS5hc3B4ZAIGD2QWAgIBDxUFMC90ZWxldmlzaW9uL2VtaXNpb24vY29tZXItZW4tY2FuYXJpYXMtMTA1MjkuYXNweBFDb21lciBlbiBDYW5hcmlhcxRDb21lciBlbiBDYW5hcmlhcy4uLglNYWdhemluZSAjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwNTI5LmFzcHhkAgcPZBYCAgEPFQUpL3RlbGV2aXNpb24vZW1pc2lvbi96b25hLW1vdG9yLTEwNTIwLmFzcHgKWm9uYSBNb3Rvcgpab25hIE1vdG9yCERlcG9ydGVzIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDUyMC5hc3B4ZAIID2QWAgIBDxUFKy90ZWxldmlzaW9uL2VtaXNpb24vbnVlc3RyYS1tZXNhLTEwNjA3LmFzcHgMTnVlc3RyYSBtZXNhDE51ZXN0cmEgbWVzYQlNYWdhemluZSAjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwNjA3LmFzcHhkAgkPZBYCAgEPFQUwL3RlbGV2aXNpb24vZW1pc2lvbi92aXZpci1lbi1jYW5hcmlhcy0xMDUyMi5hc3B4EVZpdmlyIGVuIENhbmFyaWFzFFZpdmlyIGVuIENhbmFyaWFzLi4uCU1hZ2F6aW5lICMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTA1MjIuYXNweGQCCg9kFgICAQ8VBSkvdGVsZXZpc2lvbi9lbWlzaW9uL2RvbmFjY2nDs24tMTA1MjguYXNweApEb25hY2Npw7NuCkRvbmFjY2nDs24FT3Ryb3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwNTI4LmFzcHhkAgsPZBYCAgEPFQUzL3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlvcy01LWVzdHJlbGxhcy0xMDYwNi5hc3B4FENhbmFyaW9zIDUgZXN0cmVsbGFzF0NhbmFyaW9zIDUgZXN0cmVsbGFzLi4uCU1hZ2F6aW5lICMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTA2MDYuYXNweGQCDA9kFgICAQ8VBT0vdGVsZXZpc2lvbi9lbWlzaW9uL3J1ZWRhLWRlLXByZW5zYS1wYXVsaW5vLXJpdmVyby0xMDYzNi5hc3B4HlJ1ZWRhIGRlIHByZW5zYSBQYXVsaW5vIFJpdmVybxJSdWVkYSBkZSBwcmVuc2EuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDYzNi5hc3B4ZAIND2QWAgIBDxUFKy90ZWxldmlzaW9uL2VtaXNpb24vbcOhcy10dXJpc21vLTEwNjEwLmFzcHgMTcOhcyB0dXJpc21vDE3DoXMgdHVyaXNtbwlNYWdhemluZSAjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwNjEwLmFzcHhkAg4PZBYCAgEPFQUpL3RlbGV2aXNpb24vZW1pc2lvbi91bi1kw61hLWVuLTEwNjEzLmFzcHgNVW4gZMOtYSBlbi4uLg1VbiBkw61hIGVuLi4uCU1hZ2F6aW5lICMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTA2MTMuYXNweGQCDw9kFgICAQ8VBT0vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtZmluLWRlLXNlbWFuYS0xMDE1OC5hc3B4HkNhbmFyaWFzIEV4cHJlc3MgZmluIGRlIHNlbWFuYRNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNTguYXNweGQCEA9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtMTAxNDguYXNweBBDYW5hcmlhcyBFeHByZXNzE0NhbmFyaWFzIEV4cHJlc3MuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE0OC5hc3B4ZAIRD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vZWwtZ3VzdG8tZXMtbcOtby04ODQyLmFzcHgQRWwgZ3VzdG8gZXMgbcOtbxNFbCBndXN0byBlcyBtw61vLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg0Mi5hc3B4ZAISD2QWAgIBDxUFLC90ZWxldmlzaW9uL2VtaXNpb24vZW4tY2xhdmUtZGUtamEtMzUwNi5hc3B4DkVuIGNsYXZlIGRlIEphEUVuIGNsYXZlIGRlIEphLi4uBUh1bW9yIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNTA2LmFzcHhkAhMPZBYCAgEPFQUtL3RlbGV2aXNpb24vZW1pc2lvbi9sdWNoYS1jYW5hcmlhLXItODUxNS5hc3B4EUx1Y2hhIENhbmFyaWEgKFIpEEx1Y2hhIENhbmFyaWEuLi4IRGVwb3J0ZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg1MTUuYXNweGQCFA9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uL3RvZG8tZ29sZXMtMTEwNy5hc3B4ClRvZG8gR29sZXMKVG9kbyBHb2xlcwhEZXBvcnRlcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNy5hc3B4ZAIVD2QWAgIBDxUFMy90ZWxldmlzaW9uL2VtaXNpb24vcHJlbWlvcy1jYW5hcmlhcy0yMDEyLTkyNDcuYXNweBVQcmVtaW9zIENhbmFyaWFzIDIwMTITUHJlbWlvcyBDYW5hcmlhcy4uLghDdWx0dXJhbCIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTI0Ny5hc3B4ZAIWD2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vbGEtcmV2b2x0b3NhLTk2MjguYXNweAxMYSBSZXZvbHRvc2EMTGEgUmV2b2x0b3NhBlNlcmllcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTYyOC5hc3B4ZAIXD2QWAgIBDxUFMS90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZXhwcmVzcy0yLTEwMTQ5LmFzcHgSQ2FuYXJpYXMgRXhwcmVzcyAyE0NhbmFyaWFzIEV4cHJlc3MuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE0OS5hc3B4ZAIYD2QWAgIBDxUFRS90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlLWVzdGFkby1kZS1sYS1uYWNpb25hbGlkYWQtY2FuYXJpYS0xNTIuYXNweChEZWJhdGUgRXN0YWRvIGRlIGxhIE5hY2lvbmFsaWRhZCBDYW5hcmlhEERlYmF0ZSBFc3RhZG8uLi4MSW5mb3JtYXRpdm9zIS9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xNTIuYXNweGQCGQ9kFgICAQ8VBTkvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWF2YW5jZS1pbmZvcm1hdGl2by04NzczLmFzcHgbRXNwZWNpYWwgQXZhbmNlIGluZm9ybWF0aXZvEkVzcGVjaWFsIEF2YW5jZS4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg3NzMuYXNweGQCGg9kFgICAQ8VBSUvdGVsZXZpc2lvbi9lbWlzaW9uL2JvcmdpYS0xMDM2Ni5hc3B4BkJvcmdpYQZCb3JnaWEGU2VyaWVzIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM2Ni5hc3B4ZAIbD2QWAgIBDxUFPi90ZWxldmlzaW9uL2VtaXNpb24vY29uZmVyZW5jaWEtZGUtbcOzbmljYS10ZXJyaWJhcy0xMDM3Ny5hc3B4H0NvbmZlcmVuY2lhIGRlIE3Ds25pY2EgVGVycmliYXMRQ29uZmVyZW5jaWEgZGUuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM3Ny5hc3B4ZAIcD2QWAgIBDxUFLy90ZWxldmlzaW9uL2VtaXNpb24vYWdlbmRhLW3DoXMtY2luZS0xMDE5Ny5hc3B4EEFnZW5kYSBNw6FzIENpbmUTQWdlbmRhIE3DoXMgQ2luZS4uLgRDaW5lIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE5Ny5hc3B4ZAIdD2QWAgIBDxUFPC90ZWxldmlzaW9uL2VtaXNpb24vY2FiYWxnYXRhLWRlLXJleWVzLXNjLXRlbmVyaWZlLTM2MzMuYXNweB9DYWJhbGdhdGEgZGUgUmV5ZXMgUy9DIFRlbmVyaWZlFUNhYmFsZ2F0YSBkZSBSZXllcy4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMzYzMy5hc3B4ZAIeD2QWAgIBDxUFQC90ZWxldmlzaW9uL2VtaXNpb24vZXNwZWNpYWwtaW5mb3JtYXRpdm8tcmVzdW1lbi1hbnVhbC05Njg1LmFzcHgiRXNwZWNpYWwgaW5mb3JtYXRpdm8gcmVzdW1lbiBhbnVhbBdFc3BlY2lhbCBpbmZvcm1hdGl2by4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2ODUuYXNweGQCHw9kFgICAQ8VBU0vdGVsZXZpc2lvbi9lbWlzaW9uL21lbnNhamUtZGVsLXByZXNpZGVudGUtZGVsLWdvYmllcm5vLWRlLWNhbmFyaWFzLTg4NTIuYXNweC9NZW5zYWplIGRlbCBwcmVzaWRlbnRlIGRlbCBHb2JpZXJubyBkZSBDYW5hcmlhcxlNZW5zYWplIGRlbCBwcmVzaWRlbnRlLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg1Mi5hc3B4ZAIgD2QWAgIBDxUFJC90ZWxldmlzaW9uL2VtaXNpb24vcHJvbW9zLTg0MzYuYXNweAZQcm9tb3MGUHJvbW9zBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS84NDM2LmFzcHhkAiEPZBYCAgEPFQU9L3RlbGV2aXNpb24vZW1pc2lvbi9kZWJhdGVzLWNhbmRpZGF0b3MtYWwtY29uZ3Jlc28tMTAyMTUuYXNweB5EZWJhdGVzIGNhbmRpZGF0b3MgYWwgQ29uZ3Jlc28VRGViYXRlcyBjYW5kaWRhdG9zLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyMTUuYXNweGQCIg9kFgICAQ8VBUcvdGVsZXZpc2lvbi9lbWlzaW9uL2RlYmF0ZS1lc3RhZG8tZGUtbGEtbmFjaW9uYWxpZGFkLWNhbmFyaWEtMTAzOTkuYXNweChEZWJhdGUgRXN0YWRvIGRlIGxhIE5hY2lvbmFsaWRhZCBDYW5hcmlhEERlYmF0ZSBFc3RhZG8uLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM5OS5hc3B4ZAIjD2QWAgIBDxUFNy90ZWxldmlzaW9uL2VtaXNpb24vZW50cmV2aXN0YS1wYXVsaW5vLXJpdmVyby02MTExLmFzcHgZRW50cmV2aXN0YSBQYXVsaW5vIFJpdmVybxVFbnRyZXZpc3RhIFBhdWxpbm8uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS82MTExLmFzcHhkAiQPZBYCAgEPFQVBL3RlbGV2aXNpb24vZW1pc2lvbi9lc3BlY2lhbC1pbmZvcm1hdGl2by1yZXN1bWVuLWFudWFsLTEwMjcxLmFzcHgiRXNwZWNpYWwgaW5mb3JtYXRpdm8gcmVzdW1lbiBhbnVhbBdFc3BlY2lhbCBpbmZvcm1hdGl2by4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjcxLmFzcHhkAiUPZBYCAgEPFQUyL3RlbGV2aXNpb24vZW1pc2lvbi9wcmVtaWVyLWxhLXJldm9sdG9zYS05NjUzLmFzcHgYUHJlbWllciAnJ0xhIFJldm9sdG9zYScnG1ByZW1pZXIgJydMYSBSZXZvbHRvc2EnJy4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTY1My5hc3B4ZAImD2QWAgIBDxUFMi90ZWxldmlzaW9uL2VtaXNpb24vcHJlbWllci1sYS1yZXZvbHRvc2EtOTY1Ni5hc3B4FlByZW1pZXIgJ0xhIFJldm9sdG9zYScZUHJlbWllciAnTGEgUmV2b2x0b3NhJy4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTY1Ni5hc3B4ZAInD2QWAgIBDxUFNC90ZWxldmlzaW9uL2VtaXNpb24vYWTDoW4tbWFydMOtbi1lc3BlY2lhbC05NDQwLmFzcHgXQWTDoW4gTWFydMOtbi4gRXNwZWNpYWwaQWTDoW4gTWFydMOtbi4gRXNwZWNpYWwuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NDQwLmFzcHhkAigPZBYCAgEPFQUoL3RlbGV2aXNpb24vZW1pc2lvbi9kb25hY2Npw7NuLTgxNjQuYXNweApEb25hY2Npw7NuCkRvbmFjY2nDs24FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzgxNjQuYXNweGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgcFHGN0bDAwJGxvZ2luYnV0dG9ucyRidG5FbnZpYXIFHmN0bDAwJGxvZ2luYnV0dG9ucyRjaGJSZWNvcmRhcgUVY3RsMDAkY29udGVudCRpbWdUb2RvBRdjdGwwMCRjb250ZW50JGltZ1ZpZGVvcwUWY3RsMDAkY29udGVudCRpbWdBdWRpbwUWY3RsMDAkY29udGVudCRpbWdGb3RvcwUUY3RsMDAkY29udGVudCRpbWdQREY%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria=0&ctl00$content$typeselected=todo&ctl00$content$imgVideos.x=49&ctl00$content$imgVideos.y=10"
    
    # Descarga la página
    logger.info("-------------------------------------------------------------------------------------------")
    data = scrapertools.cache_page(url, post=post)
    logger.info(data)

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
    logger.info("-------------------------------------------------------------------------------------------")
    data = scrapertools.get_match( data , '<select name="ctl00\$content\$ddlEmisionesCategoria"[^>]+>(.*?)</select>' ).strip()
    logger.info(data)
    patron  = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("matches="+str(matches))
    logger.info("-------------------------------------------------------------------------------------------")

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
    post = "ctl00$content$ScriptManager1=ctl00$content$UpdatePanel1|ctl00$content$ddlEmisionesCategoria&__EVENTTARGET=ctl00%24content%24ddlEmisionesCategoria&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYEAgMPZBYGAgEPFgIeBXN0eWxlBQ1kaXNwbGF5Om5vbmU7ZAIDDxYCHwAFD2Rpc3BsYXk6aW5saW5lO2QCBQ8WAh8ABQ1kaXNwbGF5Om5vbmU7ZAIFD2QWDgIDDw8WAh4ISW1hZ2VVcmwFIi9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfdG9kby5wbmdkZAIFDw8WAh8BBSsvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX3ZpZGVvX2NoZWNrZWQucG5nZGQCBw8PFgIfAQUjL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19hdWRpby5wbmdkZAIJDw8WAh8BBSMvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX2ZvdG9zLnBuZ2RkAgsPDxYCHwEFIS9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfcGRmLnBuZ2RkAg0PZBYCZg9kFgICAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQV2YWx1ZR4ORGF0YVZhbHVlRmllbGQFA2tleR4LXyFEYXRhQm91bmRnZBAVCRVUb2RhcyBsYXMgY2F0ZWdvcsOtYXMEQ2luZQhDdWx0dXJhbAhEZXBvcnRlcwVIdW1vcgxJbmZvcm1hdGl2b3MJTWFnYXppbmUgBU90cm9zBlNlcmllcxUJATABMgQ1MDI2ATYCMjUBMQE1BDUwNDYENTAwNxQrAwlnZ2dnZ2dnZ2cWAQIBZAIPD2QWAmYPZBYCAgIPPCsACQEADxYEHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudAIBZBYCZg9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2FnZW5kYS1tw6FzLWNpbmUtMTAxOTcuYXNweBBBZ2VuZGEgTcOhcyBDaW5lE0FnZW5kYSBNw6FzIENpbmUuLi4EQ2luZSMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxOTcuYXNweGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgcFHGN0bDAwJGxvZ2luYnV0dG9ucyRidG5FbnZpYXIFHmN0bDAwJGxvZ2luYnV0dG9ucyRjaGJSZWNvcmRhcgUVY3RsMDAkY29udGVudCRpbWdUb2RvBRdjdGwwMCRjb250ZW50JGltZ1ZpZGVvcwUWY3RsMDAkY29udGVudCRpbWdBdWRpbwUWY3RsMDAkY29udGVudCRpbWdGb3RvcwUUY3RsMDAkY29udGVudCRpbWdQREY%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria="+item.url+"&ctl00$content$typeselected=video&"
    url="http://rtvc.es/television/emisiones/1.aspx"
    
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