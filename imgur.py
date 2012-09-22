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

devkey="27bfb05d8aa26352ce60ea90cc409147" 
if (len(sys.argv) != 2):
	sys.exit("\nYou must provide one filename as a parameter!\ntry again next time...\n")
else:
	imgpth=sys.argv[1]
url="http://imgur.com/api/upload.json"

class ImgUr():
	def __init__(self,imgpth,url,key):
		self.imgpth=imgpth
		self.key=key
		self.url=url
	def imgdata(self):
		t=open(self.imgpth,"rb")
		return(b64.b64encode(t.read()))
	def parser(self):
		return(uparse.urlencode({"image":self.imgdata(),"key":self.key}).encode('utf-8'))
	def imgup(self):
		robj=ureq.Request(self.url,self.parser())
		return(ureq.urlopen(robj).read().decode('utf-8'))
	def jsdo(self):
		return(js.loads(self.imgup()))
	def response(self):
		out=self.jsdo()["rsp"]["image"]
		self.thumb=out["large_thumbnail"]
		self.url=out["original_image"]
		self.forum="[url="+self.url+"][img]"+self.thumb+"[/img][/url]"

img=ImgUr(imgpth,url,devkey)
img.response()
echofor=sub.Popen(['echo',img.forum],stdin=sub.PIPE,stdout=sub.PIPE)
xclipfor=sub.Popen(['xclip','-i','-se','c'],stdin=echofor.stdout)
echourl=sub.Popen(['echo',img.url],stdin=sub.PIPE,stdout=sub.PIPE)
xclipurl=sub.Popen(['xclip','-i','-se','p'],stdin=echourl.stdout)
print("Thumbnail:\t"+img.thumb+"\nImageUrl:\t"+img.url+"\nForumBBCode:\t"+img.forum+"\n\nIt has been xclipped! In the CTRL+V for ForumBBCode, SHIFT-Insert for ImageUrl")


