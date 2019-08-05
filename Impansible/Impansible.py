#!/usr/bin/python
from __future__ import absolute_import, division, print_function
import importlib,os,re,sys
from robot.libraries.BuiltIn import BuiltIn,RobotNotRunningError
from robot.api import logger
from ansible import modules
from .picker2 import picker2
amodules_map={}
r=os.path.dirname(modules.__file__)
rr=len(r)-15
del modules
for i in os.walk(r):
	mo=[m[:-3] for m in i[2] if m[-2:]=='py' and m!='__init__.py']
	for m in mo: amodules_map[m]=i[0][rr:].replace('/','.')

class genImpansible(type):
	def __init__(cls, name, bases, nmspc):
		super(genImpansible, cls).__init__(name, bases, nmspc)
		#[setattr(cls,n,(lambda k: lambda self,*p7: self.call_impansible(k,*p7))(n))
		#for n in amodules_map.keys()]
		[setattr(cls,n,(lambda k: lambda self,*p7,**p8: self.call_impansible(k,*p7,**p8))(n))
		for n in amodules_map.keys()]
			
class Impansible(object):
	__metaclass__ = genImpansible
	def call_impansible(self,*p,**p2):
		class myExcept(Exception):
			pass
		def MyhackFun(**p):
			def __new__(cls, *args, **kwargs):
				cls.instance = super(MyAnsibleHack2, cls).__new__(cls, *args, **kwargs)
				return cls.instance
			def __init__(self, argument_spec, bypass_checks=False, no_log=False,
				check_invalid_arguments=None, mutually_exclusive=None, 
				required_together=None, required_one_of=None, 
				add_file_common_args=False, supports_check_mode=False,
				required_if=None, required_by=None):
				self.check_mode=p.get('check_mode',False)
				if 'showmetheparms' in p: raise myExcept(argument_spec)
				p1={a:argument_spec[a].get('default','') for a in argument_spec}
				self.params=p1
				try:
					pb=BuiltIn().get_variables()
					for k in argument_spec.keys():
						if "${"+k+"}" in pb:
							self.params[k]=pb["${"+k+"}"]
						if "&{"+k+"}" in pb:
							self.params[k]=pb["&{"+k+"}"]
				except RobotNotRunningError:
					pass
				self.params.update(p)
			def exit_json(self,**e):
				self.output=e
				raise myExcept(e)
				return e
			def fail_json(self,**e):
				e['ERROR']=True
				self.output=e
				return e
			__name__='MyAnsibleHack2'
			_diff=False
			return type('MyAnsibleHack2',(object,),locals())
		if "http_proxy" in os.environ:
			del os.environ["http_proxy"]
		if "https_proxy" in os.environ:
			del os.environ["https_proxy"]
		para=p2
		argi=p
		w=["=" in x for x in argi]
		m=p[0]
		l=amodules_map[m]
		if any(w):
			k=w.index(True)
			argi=argi[k:]
			para.update(dict([x.split("=") for x in argi]))
		for k in para:
			if isinstance(para[k],basestring) and re.match('{.*}',para[k]):
				para[k]=eval(para[k])
		MyAnsibleHack2=MyhackFun(**para)
		mod=importlib.import_module("."+m,l)
		mod.AnsibleModule=MyAnsibleHack2
		try:
			mod.main()
		except myExcept as e:
			self._status=e.args[0]
			return e.args[0]
			#return e.args
		self._status=MyAnsibleHack2.instance.output
		return MyAnsibleHack2.instance.output

	def nitz(self):
		w = BuiltIn().get_variable_value("${MYGLOB}")
		return w

	def nitz2(self,**e):
		return BuiltIn().get_variables()

	def picker(self,*p):
		return picker2(self._status,p)

if __name__ == '__main__':
	x=Impansible()
	print(x.vmware_host_facts(*sys.argv[1:]))
