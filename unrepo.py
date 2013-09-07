#!/usr/bin/python

import sys
import string
import xml.etree.ElementTree as et

if len(sys.argv) < 2 :
   print "Usage: {} <manifest.xml>".format(sys.argv[0])
   exit()

manifest = sys.argv[1]
f=open(manifest, 'r')
text = f.read()

remotes = {}

print 'git init .'
print 'MYPWD=$(pwd)'

tree = et.fromstring(text)
for r in tree.iterfind('remote') :
   name = r.attrib['name']
   url  = r.attrib['fetch']
   remotes[name] = url

for p in tree.iterfind('project') :
   name     = p.attrib['name']
   remote   = p.attrib['remote']
   path     = p.attrib['path']
   revision = p.attrib['revision']
   url = remotes[remote]
   print 'git submodule add {}/{} {}'.format(url,name,path) 
   print 'cd {} && git checkout {}; cd "$MYPWD"'.format(path,revision)
   print 'git add {}'.format(name)

print 'git submodule update'
print 'git commit -m\"results of unrepo.py for {}\"'.format(manifest)
