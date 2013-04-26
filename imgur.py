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
import os.path as osp

class ImgUr():
    def __init__(self,imgpth,cfg,url,urlauth,imgurl,imgend):
        self.imgpth=imgpth
        self.imgname=osp.basename(self.imgpth)
        self.url=url
        self.urlauth=urlauth
        self.imgurl=imgurl
        self.imgend=imgend
        self.refresh_token=cfg["refresh_token"]
        self.client_id=cfg["client_id"]
        self.client_secret=cfg["client_secret"]
    def refresh(self):
        dat=uparse.urlencode({"refresh_token":self.refresh_token,"client_id":self.client_id,"client_secret":self.client_secret,"grant_type":"refresh_token"}).encode('utf-8')
        authreq=ureq.Request(self.urlauth,dat)
        authresp=js.loads(ureq.urlopen(authreq).read().decode('utf-8'))
        self.access_token=authresp["access_token"]
    def imgdata(self):
        t=open(self.imgpth,"rb")
        return(b64.b64encode(t.read()))
    def parser(self):
        return(uparse.urlencode({"image":self.imgdata(),"title":self.imgname}).encode('utf-8'))
    def imgup(self):
        headrs={"authorization":"Bearer "+self.access_token}
        robj=ureq.Request(self.url,data=self.parser(),headers=headrs)
        return(ureq.urlopen(robj).read().decode('utf-8'))
    def jsdo(self):
        return(js.loads(self.imgup()))
    def start(self):
        self.imgid=self.jsdo()["data"]["id"]
        self.sthumb=self.imgurl+self.imgid+"s"+self.imgend
        self.mthumb=self.imgurl+self.imgid+"m"+self.imgend
        self.lthumb=self.imgurl+self.imgid+"l"+self.imgend
        self.url=self.imgurl+self.imgid+self.imgend
        self.forum="[url="+self.url+"][img]"+self.sthumb+"[/img][/url]"
def main():
    if (len(sys.argv) != 2):
    	sys.exit("\nYou must provide one filename as a parameter!\ntry again next time...\n")
    else:
    	imgpth=sys.argv[1]
    ## define imgurcfg.json filepath
    cfgfile='****'
    ## load cfgfile and read tokens and ids
    cfg=open(cfgfile,"r").read()
    cfg=js.loads(cfg)
    ## other variables
    url="https://api.imgur.com/3/image"
    urlauth="https://api.imgur.com/oauth2/token"
    imgurl="http://i.imgur.com/"
    imgend=".jpg"
    #create class
    img=ImgUr(imgpth,cfg,url,urlauth,imgurl,imgend)
    # first get auth token
    img.refresh()
    # start upload process
    img.start()
    #xclippin'
    echofor=sub.Popen(['echo',img.forum],stdin=sub.PIPE,stdout=sub.PIPE)
    xclipfor=sub.Popen(['xclip','-i','-se','c'],stdin=echofor.stdout)
    echourl=sub.Popen(['echo',img.url],stdin=sub.PIPE,stdout=sub.PIPE)
    xclipurl=sub.Popen(['xclip','-i','-se','p'],stdin=echourl.stdout)
    # pretty output 
    print("\nThumbnail (large):\t"+img.lthumb+"\nThumbnail (medium):\t"+img.mthumb+"\nThumbnail (small):\t"+img.sthumb+"\nImageUrl:\t\t"+img.url+"\nForumBBCode:\t\t"+img.forum+"\n\nIt has been xclipped! In the CTRL+V for ForumBBCode, SHIFT-Insert for ImageUrl")

if __name__=='__main__':
    main()
