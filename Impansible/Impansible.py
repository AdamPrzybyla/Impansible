#!/usr/bin/python
from __future__ import absolute_import, division, print_function
import importlib,os,re,sys
from robot.libraries.BuiltIn import BuiltIn,RobotNotRunningError
from robot.api import logger
from ansible import modules
from .picker2 import picker2
from ansible.cli.adhoc import AdHocCLI as mycli
from ansible.plugins.callback import CallbackBase
from ansible import context
ansible_password=False
ansible_become_password=False
ansible_user=False
amodules_map={}
r=os.path.dirname(modules.__file__)
rr=len(r)-15
del modules
results={}
for i in os.walk(r):
	mo=[m[:-3] for m in i[2] if m[-2:]=='py' and m!='__init__.py']
	for m in mo: amodules_map[m]=i[0][rr:].replace('/','.')

class mycli2(mycli):
    def parse(self):
        self.init_parser()
	options = self.parser.parse_args(self.args[1:])
        options = self.post_process_args(options)
        context.CLIARGS=context.CLIArgs(vars(options))

class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
	global results
	results = result._result

class genImpansible(type):
	def __init__(cls, name, bases, nmspc):
		super(genImpansible, cls).__init__(name, bases, nmspc)
		#[setattr(cls,n,(lambda k: lambda self,*p7,**p8: 
		#self.call_impansible(k,*p7,**p8))(n)) for n in amodules_map.keys()]
		[setattr(cls,n,(lambda k: lambda self,*p7: 
		self.call_impansible(k,*p7))(n)) for n in amodules_map.keys()]
			
class Impansible(object):
	__metaclass__ = genImpansible
	def call_impansible(self,*p):
		global results
		global ansible_password
		global ansible_user
		global ansible_become_password
		args=[u'ansible', u'-u', u'root',u'all', 
			u'--inventory=%s,' % p[1], u'-m', p[0]]
		if p[2:]: args+=[u'-a',u" ".join(p[2:])]
		try:
			pa = BuiltIn().get_variable_value("${ansible_password}")
		except:
			pa=ansible_password
		if ansible_become_password:
			args+=["-e","ansible_become=yes","-e",
				"ansible_become_password=%s" % ansible_become_password,
				"-e", "ansible_user=%s" % ansible_user]
		else:
			try:
				bpa = BuiltIn().get_variable_value("${ansible_become_password}")
				buz = BuiltIn().get_variable_value("${ansible_user}")
				if bpa:
					args+=["-e","ansible_become=yes","-e",
					"ansible_become_password=%s" % bpa,
					"-e", "ansible_user=%s" % buz]
					if not pa: pa=bpa
			except:
				pass
		if pa: args+=[u'-e',u"ansible_password=%s"%pa]
		results_callback = ResultCallback()
		cli = mycli2(args,results_callback)
		exit_code = cli.run()
		return results

	def nitz(self):
		w = BuiltIn().get_variable_value("${MYGLOB}")
		return w

	def nitz2(self,**e):
		return BuiltIn().get_variables()

	def picker(self,w,*p):
		return picker2(w,p)

	def set_internals(self,n,v):
		globals()[n]=v

if __name__ == '__main__':
	x=Impansible()
	print(x.vmware_host_facts(*sys.argv[1:]))
