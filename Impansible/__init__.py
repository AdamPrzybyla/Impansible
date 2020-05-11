#!/usr/bin/env python
import sys,os
os.environ["ANSIBLE_HOST_KEY_CHECKING"]="False"
if (sys.version_info > (3, 0)):
	from .Impansible3 import Impansible3 as Impansible
else:
	from .Impansible import Impansible



