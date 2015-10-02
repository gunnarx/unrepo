#!/usr/bin/python
#
# This file is part of unrepo.py
#
# Author: Gunnar Andersson
# License: CC-BY 4.0 https://creativecommons.org/licenses/by/4.0/
#
# I'm not a big fan of the "repo" tool with its XML-based manifest.
# (But I can see that it might play a useful part in really big projects,
# like AOSP).
#
# git submodules are kind of quirky too, but with them I only need to learn
# and use git. They work fine for small/medium sized projects in my opinion.
#
# Some use "repo" even for small projects, to collect up a working
# configuration of a few different git repositories.  I don't see the point
# when git submodules (or git subtree) can be used.
#
# This simple script removes useless use of "repo" and turns it into a
# simple git-only setup.
#
# I have only tested this on relatively simple flat repo setups. I have not
# studied the full capabilities of repo to see if this script handles every
# feature of repo.  This is probably for small projects only.
# Please report bugs... or fix them yourself, and let me know.
#
# Usage: unrepo.py prints commands to recreate (kind of) what repo would have
#        created if you run it on the manifest, but this also registers the
#        individual git repositories as submodules instead.  
#        You can pipe the output of the script to sh/bash.

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

print '#'
print '# unrepo: printing commands to recreate (kind of)'
print '#         what repo would create from manifest {}'.format(manifest)
print '#         but using git submodules.'
print '#         (Pipe this output to sh/bash)'
print '#'
print 'git init .'
print 'MYDIR=\"$PWD\"'

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
   print 'cd {} && git checkout {}; cd "$MYDIR"'.format(path,revision)
   print 'git add {}'.format(name)
   for c in p.iterfind('copyfile') :
      src  = c.attrib['src']
      dest = c.attrib['dest']
      print 'cp {}/{} {}'.format(path,src,dest)

print 'git submodule update'
print 'git commit -m\"results of unrepo.py for {}\"'.format(manifest)
