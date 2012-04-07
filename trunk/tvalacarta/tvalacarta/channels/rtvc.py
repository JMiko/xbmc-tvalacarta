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
    post="ctl00$content$ScriptManager1=ctl00$content$ScriptManager1|ctl00$content$imgVideos&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYEZg9kFgYCAQ8WAh4Fc3R5bGUFDWRpc3BsYXk6bm9uZTtkAgMPFgIfAAUPZGlzcGxheTppbmxpbmU7ZAIFDxYCHwAFDWRpc3BsYXk6bm9uZTtkAgIPZBYOAgMPDxYCHghJbWFnZVVybAUiL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc190b2RvLnBuZ2RkAgUPDxYCHwEFKy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfdmlkZW9fY2hlY2tlZC5wbmdkZAIHDw8WAh8BBSMvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX2F1ZGlvLnBuZ2RkAgkPDxYCHwEFIy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfZm90b3MucG5nZGQCCw8PFgIfAQUhL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19wZGYucG5nZGQCDQ9kFgJmD2QWAgIBDxAPFgYeDURhdGFUZXh0RmllbGQFBXZhbHVlHg5EYXRhVmFsdWVGaWVsZAUDa2V5HgtfIURhdGFCb3VuZGdkEBUJFVRvZGFzIGxhcyBjYXRlZ29yw61hcwRDaW5lCERlcG9ydGVzBUh1bW9yDEluZm9ybWF0aXZvcwlNYWdhemluZSAHTXVzaWNhbAVPdHJvcwZTZXJpZXMVCQEwATIBNgIyNQExATUCMTEENTA0NgQ1MDA3FCsDCWdnZ2dnZ2dnZxYBZmQCDw9kFgJmD2QWAgICDzwrAAkBAA8WBB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQCKWQWUmYPZBYCAgEPFQUoL3RlbGV2aXNpb24vZW1pc2lvbi8zMC1taW51dG9zLTk0OTQuYXNweAozMCBtaW51dG9zCjMwIG1pbnV0b3MMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NDk0LmFzcHhkAgEPZBYCAgEPFQUzL3RlbGV2aXNpb24vZW1pc2lvbi9idWVub3MtZMOtYXMtY2FuYXJpYXMtMTEyNi5hc3B4FkJ1ZW5vcyBkw61hcywgQ2FuYXJpYXMZQnVlbm9zIGTDrWFzLCBDYW5hcmlhcy4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzExMjYuYXNweGQCAg9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtMTAxNDguYXNweBBDYW5hcmlhcyBFeHByZXNzE0NhbmFyaWFzIEV4cHJlc3MuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE0OC5hc3B4ZAIDD2QWAgIBDxUFKi90ZWxldmlzaW9uL2VtaXNpb24vdGVsZW5vdGljaWFzLTEtNDYuYXNweA5UZWxlbm90aWNpYXMgMRFUZWxlbm90aWNpYXMgMS4uLgxJbmZvcm1hdGl2b3MgL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzQ2LmFzcHhkAgQPZBYCAgEPFQUsL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMi0xOTM3LmFzcHgOVGVsZW5vdGljaWFzIDIRVGVsZW5vdGljaWFzIDIuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xOTM3LmFzcHhkAgUPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMy05MC5hc3B4DlRlbGVub3RpY2lhcyAzEVRlbGVub3RpY2lhcyAzLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTAuYXNweGQCBg9kFgICAQ8VBT0vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtZmluLWRlLXNlbWFuYS0xMDE1OC5hc3B4HkNhbmFyaWFzIEV4cHJlc3MgZmluIGRlIHNlbWFuYRNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNTguYXNweGQCBw9kFgICAQ8VBTkvdGVsZXZpc2lvbi9lbWlzaW9uL3RlbGVub3RpY2lhcy1maW4tZGUtc2VtYW5hLTEtMjg1LmFzcHgcVGVsZW5vdGljaWFzIEZpbiBkZSBzZW1hbmEgMRNUZWxlbm90aWNpYXMgRmluLi4uDEluZm9ybWF0aXZvcyEvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjg1LmFzcHhkAggPZBYCAgEPFQU6L3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtZmluLWRlLXNlbWFuYS0yLTM3ODguYXNweBxUZWxlbm90aWNpYXMgRmluIGRlIHNlbWFuYSAyE1RlbGVub3RpY2lhcyBGaW4uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNzg4LmFzcHhkAgkPZBYCAgEPFQUvL3RlbGV2aXNpb24vZW1pc2lvbi9wYXJyYW5kYS1jYW5hcmlhLTEwMjk3LmFzcHgQUGFycmFuZGEgY2FuYXJpYRNQYXJyYW5kYSBjYW5hcmlhLi4uB011c2ljYWwjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjk3LmFzcHhkAgoPZBYCAgEPFQUnL3RlbGV2aXNpb24vZW1pc2lvbi90bi1zb3Jkb3MtOTEwMi5hc3B4CVROIHNvcmRvcwlUTiBzb3Jkb3MMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85MTAyLmFzcHhkAgsPZBYCAgEPFQUxL3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlhcy1leHByZXNzLTItMTAxNDkuYXNweBJDYW5hcmlhcyBFeHByZXNzIDITQ2FuYXJpYXMgRXhwcmVzcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMTQ5LmFzcHhkAgwPZBYCAgEPFQUnL3RlbGV2aXNpb24vZW1pc2lvbi9lbC1lbnZpdGUtNzgwMi5hc3B4CUVsIGVudml0ZQlFbCBlbnZpdGUMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83ODAyLmFzcHhkAg0PZBYCAgEPFQUkL3RlbGV2aXNpb24vZW1pc2lvbi9yZXBvcjctNzY4Ni5hc3B4BlJlcG9yNwZSZXBvcjcMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83Njg2LmFzcHhkAg4PZBYCAgEPFQVFL3RlbGV2aXNpb24vZW1pc2lvbi9kZWJhdGUtZXN0YWRvLWRlLWxhLW5hY2lvbmFsaWRhZC1jYW5hcmlhLTE1Mi5hc3B4KERlYmF0ZSBFc3RhZG8gZGUgbGEgTmFjaW9uYWxpZGFkIENhbmFyaWEQRGViYXRlIEVzdGFkby4uLgxJbmZvcm1hdGl2b3MhL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzE1Mi5hc3B4ZAIPD2QWAgIBDxUFOS90ZWxldmlzaW9uL2VtaXNpb24vZXNwZWNpYWwtYXZhbmNlLWluZm9ybWF0aXZvLTg3NzMuYXNweBtFc3BlY2lhbCBBdmFuY2UgaW5mb3JtYXRpdm8SRXNwZWNpYWwgQXZhbmNlLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODc3My5hc3B4ZAIQD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vZWwtZ3VzdG8tZXMtbcOtby04ODQyLmFzcHgQRWwgZ3VzdG8gZXMgbcOtbxNFbCBndXN0byBlcyBtw61vLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg0Mi5hc3B4ZAIRD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vdG9kby1nb2xlcy0xMTA3LmFzcHgKVG9kbyBHb2xlcwpUb2RvIEdvbGVzCERlcG9ydGVzIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMTA3LmFzcHhkAhIPZBYCAgEPFQU6L3RlbGV2aXNpb24vZW1pc2lvbi9lc3BlY2lhbC1hdmFuY2UtaW5mb3JtYXRpdm8tMTAzODguYXNweBtFc3BlY2lhbCBhdmFuY2UgaW5mb3JtYXRpdm8SRXNwZWNpYWwgYXZhbmNlLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAzODguYXNweGQCEw9kFgICAQ8VBSUvdGVsZXZpc2lvbi9lbWlzaW9uL2JvcmdpYS0xMDM2Ni5hc3B4BkJvcmdpYQZCb3JnaWEGU2VyaWVzIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM2Ni5hc3B4ZAIUD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZGlyZWN0by0xMTA1LmFzcHgQQ2FuYXJpYXMgRGlyZWN0bxNDYW5hcmlhcyBEaXJlY3RvLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNS5hc3B4ZAIVD2QWAgIBDxUFPi90ZWxldmlzaW9uL2VtaXNpb24vY29uZmVyZW5jaWEtZGUtbcOzbmljYS10ZXJyaWJhcy0xMDM3Ny5hc3B4H0NvbmZlcmVuY2lhIGRlIE3Ds25pY2EgVGVycmliYXMRQ29uZmVyZW5jaWEgZGUuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM3Ny5hc3B4ZAIWD2QWAgIBDxUFLC90ZWxldmlzaW9uL2VtaXNpb24vZW4tY2xhdmUtZGUtamEtMzUwNi5hc3B4DkVuIGNsYXZlIGRlIEphEUVuIGNsYXZlIGRlIEphLi4uBUh1bW9yIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNTA2LmFzcHhkAhcPZBYCAgEPFQUtL3RlbGV2aXNpb24vZW1pc2lvbi9sdWNoYS1jYW5hcmlhLXItODUxNS5hc3B4EUx1Y2hhIENhbmFyaWEgKFIpEEx1Y2hhIENhbmFyaWEuLi4IRGVwb3J0ZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg1MTUuYXNweGQCGA9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2FnZW5kYS1tw6FzLWNpbmUtMTAxOTcuYXNweBBBZ2VuZGEgTcOhcyBDaW5lE0FnZW5kYSBNw6FzIENpbmUuLi4EQ2luZSMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxOTcuYXNweGQCGQ9kFgICAQ8VBSovdGVsZXZpc2lvbi9lbWlzaW9uL2xhLXJldm9sdG9zYS05NjI4LmFzcHgMTGEgUmV2b2x0b3NhDExhIFJldm9sdG9zYQZTZXJpZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2MjguYXNweGQCGg9kFgICAQ8VBTwvdGVsZXZpc2lvbi9lbWlzaW9uL2NhYmFsZ2F0YS1kZS1yZXllcy1zYy10ZW5lcmlmZS0zNjMzLmFzcHgfQ2FiYWxnYXRhIGRlIFJleWVzIFMvQyBUZW5lcmlmZRVDYWJhbGdhdGEgZGUgUmV5ZXMuLi4FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzM2MzMuYXNweGQCGw9kFgICAQ8VBUAvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtOTY4NS5hc3B4IkVzcGVjaWFsIGluZm9ybWF0aXZvIHJlc3VtZW4gYW51YWwXRXNwZWNpYWwgaW5mb3JtYXRpdm8uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85Njg1LmFzcHhkAhwPZBYCAgEPFQVNL3RlbGV2aXNpb24vZW1pc2lvbi9tZW5zYWplLWRlbC1wcmVzaWRlbnRlLWRlbC1nb2JpZXJuby1kZS1jYW5hcmlhcy04ODUyLmFzcHgvTWVuc2FqZSBkZWwgcHJlc2lkZW50ZSBkZWwgR29iaWVybm8gZGUgQ2FuYXJpYXMZTWVuc2FqZSBkZWwgcHJlc2lkZW50ZS4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg4NTIuYXNweGQCHQ9kFgICAQ8VBSQvdGVsZXZpc2lvbi9lbWlzaW9uL3Byb21vcy04NDM2LmFzcHgGUHJvbW9zBlByb21vcwVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODQzNi5hc3B4ZAIeD2QWAgIBDxUFPS90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlcy1jYW5kaWRhdG9zLWFsLWNvbmdyZXNvLTEwMjE1LmFzcHgeRGViYXRlcyBjYW5kaWRhdG9zIGFsIENvbmdyZXNvFURlYmF0ZXMgY2FuZGlkYXRvcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjE1LmFzcHhkAh8PZBYCAgEPFQU%2BL3RlbGV2aXNpb24vZW1pc2lvbi9vZnJlbmRhLXJvbWVyw61hLXZpcmdlbi1kZWwtcGluby0yNDU4LmFzcHggT2ZyZW5kYSBSb21lcsOtYSBWaXJnZW4gZGVsIFBpbm8TT2ZyZW5kYSBSb21lcsOtYS4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjQ1OC5hc3B4ZAIgD2QWAgIBDxUFKy90ZWxldmlzaW9uL2VtaXNpb24vMzAtbWludXRvcy1yLTEwMTU2LmFzcHgOMzAgbWludXRvcyAoUikRMzAgbWludXRvcyAoUikuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE1Ni5hc3B4ZAIhD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vcGFybGFtZW50by03NDMxLmFzcHgKUGFybGFtZW50bwpQYXJsYW1lbnRvDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNzQzMS5hc3B4ZAIiD2QWAgIBDxUFRy90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlLWVzdGFkby1kZS1sYS1uYWNpb25hbGlkYWQtY2FuYXJpYS0xMDM5OS5hc3B4KERlYmF0ZSBFc3RhZG8gZGUgbGEgTmFjaW9uYWxpZGFkIENhbmFyaWEQRGViYXRlIEVzdGFkby4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMzk5LmFzcHhkAiMPZBYCAgEPFQU3L3RlbGV2aXNpb24vZW1pc2lvbi9lbnRyZXZpc3RhLXBhdWxpbm8tcml2ZXJvLTYxMTEuYXNweBlFbnRyZXZpc3RhIFBhdWxpbm8gUml2ZXJvFUVudHJldmlzdGEgUGF1bGluby4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzYxMTEuYXNweGQCJA9kFgICAQ8VBUEvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtMTAyNzEuYXNweCJFc3BlY2lhbCBpbmZvcm1hdGl2byByZXN1bWVuIGFudWFsF0VzcGVjaWFsIGluZm9ybWF0aXZvLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyNzEuYXNweGQCJQ9kFgICAQ8VBTIvdGVsZXZpc2lvbi9lbWlzaW9uL3ByZW1pZXItbGEtcmV2b2x0b3NhLTk2NTMuYXNweBhQcmVtaWVyICcnTGEgUmV2b2x0b3NhJycbUHJlbWllciAnJ0xhIFJldm9sdG9zYScnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjUzLmFzcHhkAiYPZBYCAgEPFQUyL3RlbGV2aXNpb24vZW1pc2lvbi9wcmVtaWVyLWxhLXJldm9sdG9zYS05NjU2LmFzcHgWUHJlbWllciAnTGEgUmV2b2x0b3NhJxlQcmVtaWVyICdMYSBSZXZvbHRvc2EnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjU2LmFzcHhkAicPZBYCAgEPFQU0L3RlbGV2aXNpb24vZW1pc2lvbi9hZMOhbi1tYXJ0w61uLWVzcGVjaWFsLTk0NDAuYXNweBdBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbBpBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbC4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk0NDAuYXNweGQCKA9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uL2RvbmFjY2nDs24tODE2NC5hc3B4CkRvbmFjY2nDs24KRG9uYWNjacOzbgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODE2NC5hc3B4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBwUcY3RsMDAkbG9naW5idXR0b25zJGJ0bkVudmlhcgUeY3RsMDAkbG9naW5idXR0b25zJGNoYlJlY29yZGFyBRVjdGwwMCRjb250ZW50JGltZ1RvZG8FF2N0bDAwJGNvbnRlbnQkaW1nVmlkZW9zBRZjdGwwMCRjb250ZW50JGltZ0F1ZGlvBRZjdGwwMCRjb250ZW50JGltZ0ZvdG9zBRRjdGwwMCRjb250ZW50JGltZ1BERg%3D%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria=0&ctl00$content$typeselected=video&ctl00$content$imgVideos.x=38&ctl00$content$imgVideos.y=14"
    
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
    post = "ctl00$content$ScriptManager1=ctl00$content$UpdatePanel1|ctl00$content$ddlEmisionesCategoria&__EVENTTARGET=ctl00%24content%24ddlEmisionesCategoria&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwULLTEzNjQ1NDg2NTgPZBYCZg9kFgICAxBkZBYEZg9kFgYCAQ8WAh4Fc3R5bGUFDWRpc3BsYXk6bm9uZTtkAgMPFgIfAAUPZGlzcGxheTppbmxpbmU7ZAIFDxYCHwAFDWRpc3BsYXk6bm9uZTtkAgIPZBYOAgMPDxYCHghJbWFnZVVybAUiL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc190b2RvLnBuZ2RkAgUPDxYCHwEFKy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfdmlkZW9fY2hlY2tlZC5wbmdkZAIHDw8WAh8BBSMvaW1hZ2VzL3dlYi9idG5fZW1pc2lvbmVzX2F1ZGlvLnBuZ2RkAgkPDxYCHwEFIy9pbWFnZXMvd2ViL2J0bl9lbWlzaW9uZXNfZm90b3MucG5nZGQCCw8PFgIfAQUhL2ltYWdlcy93ZWIvYnRuX2VtaXNpb25lc19wZGYucG5nZGQCDQ9kFgJmD2QWAgIBDxAPFgYeDURhdGFUZXh0RmllbGQFBXZhbHVlHg5EYXRhVmFsdWVGaWVsZAUDa2V5HgtfIURhdGFCb3VuZGdkEBUJFVRvZGFzIGxhcyBjYXRlZ29yw61hcwRDaW5lCERlcG9ydGVzBUh1bW9yDEluZm9ybWF0aXZvcwlNYWdhemluZSAHTXVzaWNhbAVPdHJvcwZTZXJpZXMVCQEwATIBNgIyNQExATUCMTEENTA0NgQ1MDA3FCsDCWdnZ2dnZ2dnZxYBZmQCDw9kFgJmD2QWAgICDzwrAAkBAA8WBB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQCKWQWUmYPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMS00Ni5hc3B4DlRlbGVub3RpY2lhcyAxEVRlbGVub3RpY2lhcyAxLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNDYuYXNweGQCAQ9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uLzMwLW1pbnV0b3MtOTQ5NC5hc3B4CjMwIG1pbnV0b3MKMzAgbWludXRvcwxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk0OTQuYXNweGQCAg9kFgICAQ8VBTMvdGVsZXZpc2lvbi9lbWlzaW9uL2J1ZW5vcy1kw61hcy1jYW5hcmlhcy0xMTI2LmFzcHgWQnVlbm9zIGTDrWFzLCBDYW5hcmlhcxlCdWVub3MgZMOtYXMsIENhbmFyaWFzLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEyNi5hc3B4ZAIDD2QWAgIBDxUFLy90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZXhwcmVzcy0xMDE0OC5hc3B4EENhbmFyaWFzIEV4cHJlc3MTQ2FuYXJpYXMgRXhwcmVzcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMTQ4LmFzcHhkAgQPZBYCAgEPFQUsL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMi0xOTM3LmFzcHgOVGVsZW5vdGljaWFzIDIRVGVsZW5vdGljaWFzIDIuLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xOTM3LmFzcHhkAgUPZBYCAgEPFQUqL3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtMy05MC5hc3B4DlRlbGVub3RpY2lhcyAzEVRlbGVub3RpY2lhcyAzLi4uDEluZm9ybWF0aXZvcyAvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvOTAuYXNweGQCBg9kFgICAQ8VBT0vdGVsZXZpc2lvbi9lbWlzaW9uL2NhbmFyaWFzLWV4cHJlc3MtZmluLWRlLXNlbWFuYS0xMDE1OC5hc3B4HkNhbmFyaWFzIEV4cHJlc3MgZmluIGRlIHNlbWFuYRNDYW5hcmlhcyBFeHByZXNzLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxNTguYXNweGQCBw9kFgICAQ8VBTkvdGVsZXZpc2lvbi9lbWlzaW9uL3RlbGVub3RpY2lhcy1maW4tZGUtc2VtYW5hLTEtMjg1LmFzcHgcVGVsZW5vdGljaWFzIEZpbiBkZSBzZW1hbmEgMRNUZWxlbm90aWNpYXMgRmluLi4uDEluZm9ybWF0aXZvcyEvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjg1LmFzcHhkAggPZBYCAgEPFQU6L3RlbGV2aXNpb24vZW1pc2lvbi90ZWxlbm90aWNpYXMtZmluLWRlLXNlbWFuYS0yLTM3ODguYXNweBxUZWxlbm90aWNpYXMgRmluIGRlIHNlbWFuYSAyE1RlbGVub3RpY2lhcyBGaW4uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNzg4LmFzcHhkAgkPZBYCAgEPFQUvL3RlbGV2aXNpb24vZW1pc2lvbi9wYXJyYW5kYS1jYW5hcmlhLTEwMjk3LmFzcHgQUGFycmFuZGEgY2FuYXJpYRNQYXJyYW5kYSBjYW5hcmlhLi4uB011c2ljYWwjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjk3LmFzcHhkAgoPZBYCAgEPFQUnL3RlbGV2aXNpb24vZW1pc2lvbi90bi1zb3Jkb3MtOTEwMi5hc3B4CVROIHNvcmRvcwlUTiBzb3Jkb3MMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85MTAyLmFzcHhkAgsPZBYCAgEPFQUxL3RlbGV2aXNpb24vZW1pc2lvbi9jYW5hcmlhcy1leHByZXNzLTItMTAxNDkuYXNweBJDYW5hcmlhcyBFeHByZXNzIDITQ2FuYXJpYXMgRXhwcmVzcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMTQ5LmFzcHhkAgwPZBYCAgEPFQUnL3RlbGV2aXNpb24vZW1pc2lvbi9lbC1lbnZpdGUtNzgwMi5hc3B4CUVsIGVudml0ZQlFbCBlbnZpdGUMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83ODAyLmFzcHhkAg0PZBYCAgEPFQUkL3RlbGV2aXNpb24vZW1pc2lvbi9yZXBvcjctNzY4Ni5hc3B4BlJlcG9yNwZSZXBvcjcMSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS83Njg2LmFzcHhkAg4PZBYCAgEPFQVFL3RlbGV2aXNpb24vZW1pc2lvbi9kZWJhdGUtZXN0YWRvLWRlLWxhLW5hY2lvbmFsaWRhZC1jYW5hcmlhLTE1Mi5hc3B4KERlYmF0ZSBFc3RhZG8gZGUgbGEgTmFjaW9uYWxpZGFkIENhbmFyaWEQRGViYXRlIEVzdGFkby4uLgxJbmZvcm1hdGl2b3MhL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzE1Mi5hc3B4ZAIPD2QWAgIBDxUFOS90ZWxldmlzaW9uL2VtaXNpb24vZXNwZWNpYWwtYXZhbmNlLWluZm9ybWF0aXZvLTg3NzMuYXNweBtFc3BlY2lhbCBBdmFuY2UgaW5mb3JtYXRpdm8SRXNwZWNpYWwgQXZhbmNlLi4uDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODc3My5hc3B4ZAIQD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vZWwtZ3VzdG8tZXMtbcOtby04ODQyLmFzcHgQRWwgZ3VzdG8gZXMgbcOtbxNFbCBndXN0byBlcyBtw61vLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODg0Mi5hc3B4ZAIRD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vdG9kby1nb2xlcy0xMTA3LmFzcHgKVG9kbyBHb2xlcwpUb2RvIEdvbGVzCERlcG9ydGVzIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMTA3LmFzcHhkAhIPZBYCAgEPFQU6L3RlbGV2aXNpb24vZW1pc2lvbi9lc3BlY2lhbC1hdmFuY2UtaW5mb3JtYXRpdm8tMTAzODguYXNweBtFc3BlY2lhbCBhdmFuY2UgaW5mb3JtYXRpdm8SRXNwZWNpYWwgYXZhbmNlLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAzODguYXNweGQCEw9kFgICAQ8VBSUvdGVsZXZpc2lvbi9lbWlzaW9uL2JvcmdpYS0xMDM2Ni5hc3B4BkJvcmdpYQZCb3JnaWEGU2VyaWVzIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM2Ni5hc3B4ZAIUD2QWAgIBDxUFLi90ZWxldmlzaW9uL2VtaXNpb24vY2FuYXJpYXMtZGlyZWN0by0xMTA1LmFzcHgQQ2FuYXJpYXMgRGlyZWN0bxNDYW5hcmlhcyBEaXJlY3RvLi4uCU1hZ2F6aW5lICIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTEwNS5hc3B4ZAIVD2QWAgIBDxUFPi90ZWxldmlzaW9uL2VtaXNpb24vY29uZmVyZW5jaWEtZGUtbcOzbmljYS10ZXJyaWJhcy0xMDM3Ny5hc3B4H0NvbmZlcmVuY2lhIGRlIE3Ds25pY2EgVGVycmliYXMRQ29uZmVyZW5jaWEgZGUuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDM3Ny5hc3B4ZAIWD2QWAgIBDxUFLC90ZWxldmlzaW9uL2VtaXNpb24vZW4tY2xhdmUtZGUtamEtMzUwNi5hc3B4DkVuIGNsYXZlIGRlIEphEUVuIGNsYXZlIGRlIEphLi4uBUh1bW9yIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8zNTA2LmFzcHhkAhcPZBYCAgEPFQUtL3RlbGV2aXNpb24vZW1pc2lvbi9sdWNoYS1jYW5hcmlhLXItODUxNS5hc3B4EUx1Y2hhIENhbmFyaWEgKFIpEEx1Y2hhIENhbmFyaWEuLi4IRGVwb3J0ZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg1MTUuYXNweGQCGA9kFgICAQ8VBS8vdGVsZXZpc2lvbi9lbWlzaW9uL2FnZW5kYS1tw6FzLWNpbmUtMTAxOTcuYXNweBBBZ2VuZGEgTcOhcyBDaW5lE0FnZW5kYSBNw6FzIENpbmUuLi4EQ2luZSMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAxOTcuYXNweGQCGQ9kFgICAQ8VBSovdGVsZXZpc2lvbi9lbWlzaW9uL2xhLXJldm9sdG9zYS05NjI4LmFzcHgMTGEgUmV2b2x0b3NhDExhIFJldm9sdG9zYQZTZXJpZXMiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk2MjguYXNweGQCGg9kFgICAQ8VBTwvdGVsZXZpc2lvbi9lbWlzaW9uL2NhYmFsZ2F0YS1kZS1yZXllcy1zYy10ZW5lcmlmZS0zNjMzLmFzcHgfQ2FiYWxnYXRhIGRlIFJleWVzIFMvQyBUZW5lcmlmZRVDYWJhbGdhdGEgZGUgUmV5ZXMuLi4FT3Ryb3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzM2MzMuYXNweGQCGw9kFgICAQ8VBUAvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtOTY4NS5hc3B4IkVzcGVjaWFsIGluZm9ybWF0aXZvIHJlc3VtZW4gYW51YWwXRXNwZWNpYWwgaW5mb3JtYXRpdm8uLi4MSW5mb3JtYXRpdm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85Njg1LmFzcHhkAhwPZBYCAgEPFQVNL3RlbGV2aXNpb24vZW1pc2lvbi9tZW5zYWplLWRlbC1wcmVzaWRlbnRlLWRlbC1nb2JpZXJuby1kZS1jYW5hcmlhcy04ODUyLmFzcHgvTWVuc2FqZSBkZWwgcHJlc2lkZW50ZSBkZWwgR29iaWVybm8gZGUgQ2FuYXJpYXMZTWVuc2FqZSBkZWwgcHJlc2lkZW50ZS4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzg4NTIuYXNweGQCHQ9kFgICAQ8VBSQvdGVsZXZpc2lvbi9lbWlzaW9uL3Byb21vcy04NDM2LmFzcHgGUHJvbW9zBlByb21vcwVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODQzNi5hc3B4ZAIeD2QWAgIBDxUFPS90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlcy1jYW5kaWRhdG9zLWFsLWNvbmdyZXNvLTEwMjE1LmFzcHgeRGViYXRlcyBjYW5kaWRhdG9zIGFsIENvbmdyZXNvFURlYmF0ZXMgY2FuZGlkYXRvcy4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMjE1LmFzcHhkAh8PZBYCAgEPFQU%2BL3RlbGV2aXNpb24vZW1pc2lvbi9vZnJlbmRhLXJvbWVyw61hLXZpcmdlbi1kZWwtcGluby0yNDU4LmFzcHggT2ZyZW5kYSBSb21lcsOtYSBWaXJnZW4gZGVsIFBpbm8TT2ZyZW5kYSBSb21lcsOtYS4uLgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMjQ1OC5hc3B4ZAIgD2QWAgIBDxUFKy90ZWxldmlzaW9uL2VtaXNpb24vMzAtbWludXRvcy1yLTEwMTU2LmFzcHgOMzAgbWludXRvcyAoUikRMzAgbWludXRvcyAoUikuLi4MSW5mb3JtYXRpdm9zIy9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS8xMDE1Ni5hc3B4ZAIhD2QWAgIBDxUFKC90ZWxldmlzaW9uL2VtaXNpb24vcGFybGFtZW50by03NDMxLmFzcHgKUGFybGFtZW50bwpQYXJsYW1lbnRvDEluZm9ybWF0aXZvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvNzQzMS5hc3B4ZAIiD2QWAgIBDxUFRy90ZWxldmlzaW9uL2VtaXNpb24vZGViYXRlLWVzdGFkby1kZS1sYS1uYWNpb25hbGlkYWQtY2FuYXJpYS0xMDM5OS5hc3B4KERlYmF0ZSBFc3RhZG8gZGUgbGEgTmFjaW9uYWxpZGFkIENhbmFyaWEQRGViYXRlIEVzdGFkby4uLgxJbmZvcm1hdGl2b3MjL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzEwMzk5LmFzcHhkAiMPZBYCAgEPFQU3L3RlbGV2aXNpb24vZW1pc2lvbi9lbnRyZXZpc3RhLXBhdWxpbm8tcml2ZXJvLTYxMTEuYXNweBlFbnRyZXZpc3RhIFBhdWxpbm8gUml2ZXJvFUVudHJldmlzdGEgUGF1bGluby4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzYxMTEuYXNweGQCJA9kFgICAQ8VBUEvdGVsZXZpc2lvbi9lbWlzaW9uL2VzcGVjaWFsLWluZm9ybWF0aXZvLXJlc3VtZW4tYW51YWwtMTAyNzEuYXNweCJFc3BlY2lhbCBpbmZvcm1hdGl2byByZXN1bWVuIGFudWFsF0VzcGVjaWFsIGluZm9ybWF0aXZvLi4uDEluZm9ybWF0aXZvcyMvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvMTAyNzEuYXNweGQCJQ9kFgICAQ8VBTIvdGVsZXZpc2lvbi9lbWlzaW9uL3ByZW1pZXItbGEtcmV2b2x0b3NhLTk2NTMuYXNweBhQcmVtaWVyICcnTGEgUmV2b2x0b3NhJycbUHJlbWllciAnJ0xhIFJldm9sdG9zYScnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjUzLmFzcHhkAiYPZBYCAgEPFQUyL3RlbGV2aXNpb24vZW1pc2lvbi9wcmVtaWVyLWxhLXJldm9sdG9zYS05NjU2LmFzcHgWUHJlbWllciAnTGEgUmV2b2x0b3NhJxlQcmVtaWVyICdMYSBSZXZvbHRvc2EnLi4uBU90cm9zIi9yc3MvdGVsZXZpc2lvbi9wcm9ncmFtYS85NjU2LmFzcHhkAicPZBYCAgEPFQU0L3RlbGV2aXNpb24vZW1pc2lvbi9hZMOhbi1tYXJ0w61uLWVzcGVjaWFsLTk0NDAuYXNweBdBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbBpBZMOhbiBNYXJ0w61uLiBFc3BlY2lhbC4uLgxJbmZvcm1hdGl2b3MiL3Jzcy90ZWxldmlzaW9uL3Byb2dyYW1hLzk0NDAuYXNweGQCKA9kFgICAQ8VBSgvdGVsZXZpc2lvbi9lbWlzaW9uL2RvbmFjY2nDs24tODE2NC5hc3B4CkRvbmFjY2nDs24KRG9uYWNjacOzbgVPdHJvcyIvcnNzL3RlbGV2aXNpb24vcHJvZ3JhbWEvODE2NC5hc3B4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBwUcY3RsMDAkbG9naW5idXR0b25zJGJ0bkVudmlhcgUeY3RsMDAkbG9naW5idXR0b25zJGNoYlJlY29yZGFyBRVjdGwwMCRjb250ZW50JGltZ1RvZG8FF2N0bDAwJGNvbnRlbnQkaW1nVmlkZW9zBRZjdGwwMCRjb250ZW50JGltZ0F1ZGlvBRZjdGwwMCRjb250ZW50JGltZ0ZvdG9zBRRjdGwwMCRjb250ZW50JGltZ1BERg%3D%3D&ctl00$loginbuttons$txtUsuario=&ctl00$loginbuttons$txtPassword=&ctl00$content$ddlEmisionesCategoria="+item.url+"&ctl00$content$typeselected=video&"
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