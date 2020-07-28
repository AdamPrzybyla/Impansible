#!/usr/bin/python
from __future__ import absolute_import, division, print_function
import importlib,os,re,sys,yaml,time,pprint
from ansible import modules
amodules_map={}
amodules_docs={}
r=os.path.dirname(modules.__file__)
rr=len(r)-15
del modules
results={}
for i in os.walk(r):
	mo=[m[:-3] for m in i[2] if m[-2:]=='py' and m!='__init__.py']
	for m in mo: amodules_map[m]=i[0][rr:].replace('/','.')

tm=0
for l in amodules_map:
                d=getattr(__import__(amodules_map[l]+"."+l, fromlist=["DOCUMENTATION"]),"DOCUMENTATION","Removed keyword")
		if d!='Removed keyword':
			da=yaml.safe_load(d)
			#print (d)
			if "description" not in da:
				d=da["short_description"]
			else:
				d=da["description"]
			ds=da["short_description"]
			if "options" not in da:
				dk=[]
			else:
				dk=da["options"].keys()
			if isinstance(d,list): d="\n".join(d)
                amodules_docs[l]=ds+"\n\nArguments: "+(", ".join(dk))+"\n\n"+d
print ("amodules_docs=",end ="")
pprint.pprint(amodules_docs)
