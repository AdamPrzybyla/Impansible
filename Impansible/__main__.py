#!/usr/bin/env python
import sys
if (sys.version_info > (3, 0)):
	from .Impansible3 import Impansible3 as Impansible
else:
	from .Impansible import Impansible

def main():
	import pprint
	print(pprint.pformat(getattr(Impansible(),sys.argv[1])(*sys.argv[2:])))
main()
