#! /usr/bin/env python

## python imgur uploader script (got sick of imageshack)
## by gnomeye

## mods

import sys 
import subprocess as sub
import urllib.request as ureq
import urllib.parse as uparse
import base64 as b64
import json as js

#devkey="27bfb05d8aa26352ce60ea90cc409147" 
clientid="*************"
clientsecret="************"
refresh_token="*************"
if (len(sys.argv) != 2):
	sys.exit("\nYou must provide one filename as a parameter!\ntry again next time...\n")
else:
	imgpth=sys.argv[1]
#url=ilientid="01c9664ea992654"
clientsecret="5324cb43098453108d3cbcc081dea4a82c31b50f"
refresh_token="f4768dbb7c64a9c827cf8233ee2d198a6d9d47bf"
"http://imgur.com/api/upload.json"
url="https://api.imgur.com/3/upload.json"
#resp_type="pin"
#urlauth="https://api.imgur.com/authorize?client_id="+clientid+"&response_type="+resp_type
urltoken="https://api.imgur.com/oauth2/token"
iurl="http://i.imgur.com/"
iend=".jpg"

class ImgUr():
    def __init__(self,imgpth,url,refurl,clientid,clientsecr,refrtoken):
        self.imgpth=imgpth
        self.url=url
        self.refurl=refurl
        self.refrtoken=refrtoken
        self.clientid=clientid
        self.clientsecr=clientsecr
    def refresh(self):
        dat=uparse.urlencode({"refresh_token":self.refrtoken,"client_id":self.clientid,"client_secret":self.clientsecr,"grant_type":"refresh_token"}).encode('utf-8')
        refreq=ureq.Request(self.refurl,dat)
        refresp=js.loads(ureq.urlopen(refreq).read().decode('utf-8'))
        self.auth=refresp["access_token"]
    def imgdata(self):
        t=open(self.imgpth,"rb")
        return(b64.b64encode(t.read()))
    def parser(self):
        return(uparse.urlencode({"image":self.imgdata()}).encode('utf-8'))
    def imgup(self):
        headrs={"authorization":"Bearer "+self.auth}
        robj=ureq.Request(self.url,data=self.parser(),headers=headrs)
        return(ureq.urlopen(robj).read().decode('utf-8'))
    def jsdo(self):
        return(js.loads(self.imgup()))
    def response(self):
        iid=self.jsdo()["data"]["id"]
        self.sthumb=iurl+iid+"s"+iend
        self.mthumb=iurl+iid+"m"+iend
        self.lthumb=iurl+iid+"l"+iend
        self.url=iurl+iid+iend
        self.forum="[url="+self.url+"][img]"+self.sthumb+"[/img][/url]"

img=ImgUr(imgpth,url,urltoken,clientid,clientsecret,refresh_token)
img.refresh()
img.response()
echofor=sub.Popen(['echo',img.forum],stdin=sub.PIPE,stdout=sub.PIPE)
xclipfor=sub.Popen(['xclip','-i','-se','c'],stdin=echofor.stdout)
echourl=sub.Popen(['echo',img.url],stdin=sub.PIPE,stdout=sub.PIPE)
xclipurl=sub.Popen(['xclip','-i','-se','p'],stdin=echourl.stdout)
print("\nThumbnail (large):\t"+img.lthumb+"\nThumbnail (medium):\t"+img.mthumb+"\nThumbnail (small):\t"+img.sthumb+"\nImageUrl:\t\t"+img.url+"\nForumBBCode:\t\t"+img.forum+"\n\nIt has been xclipped! In the CTRL+V for ForumBBCode, SHIFT-Insert for ImageUrl")


