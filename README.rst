Impansible
===============

.. contents::

Introduction
------------

Impansible_ is a `Robot Framework`_ test
library for access to all Ansible internal modules.
All Ansible modules are available as Robotframework's keywords.
The Impansible library can be used without Robotframework.


Impansible is operating system independent and supports Python 2.7 as well
as Python 3.x or newer. 

Documentation
-------------

See `keyword documentation`_ for available keywords and more information
about the library in general.

For general information about using test libraries with Robot Framework, see
`Robot Framework User Guide`_.

Installation
------------

The recommended installation method is using pip_::

    pip install --upgrade robotframework-impansible

With recent versions of ``pip`` it is possible to install directly from the
GitHub_ repository. To install latest source from the master branch, use
this command::

    pip install git+https://github.com/AdamPrzybyla/Impansible.git

Alternatively you can download the source distribution from PyPI_, extract
it, and install it using one of the following depending are you using
Python or Jython::

    python setup.py install

Usage
-----

The library can be used localy if teh first parametr is set to "local"
or remotly if the first parameter is set to hostname.
You need to export ssh keys or provide the propper credentials.
if you have root access you need to set the ansible_password variable
but for sudo access you neeed to set ansible_become_password and ansible_user 
variables.

The keywors documenatation can be found on this site: `keyword Documentation`_

.. code:: robotframework

	*** variables ***
	${PAC}   mtr
	#${ansible_password}  xxxxxxx
	${ansible_become_password}  xxxxxxxxx
	${ansible_user}  user_user

	*** settings ***
	library  Impansible
	library  Collections
	library  OperatingSystem

	*** test cases ***
	test 1
		${x}=	Setup  localhost
			log  ${x}
		${y}=	get from dictionary  ${x}   ansible_facts
		${h}=	get from dictionary  ${y}   ansible_hostname
		${z}=	get from dictionary  ${y}   ansible_distribution
			Should be Equal  ${z}  Ubuntu
			Should Contain   ${h}  tester
	test 2
		[Timeout]    600
		${x}=	apt    localhost   package=${PAC}   state=present
		${x}=	get from dictionary  ${x}   invocation
		${y}=	get from dictionary  ${x}   module_args
		${s}=	get from dictionary  ${y}   state
			Should be Equal  ${s}  present
		${w}=	Run	which ${PAC}
			Should Contain  ${w}  ${PAC}

	test 3
		[Timeout]    600
		${x}=	apt   localhost   package=${PAC}   state=absent
		${x}=	get from dictionary  ${x}   invocation
		${y}=	get from dictionary  ${x}   module_args
		${s}=	get from dictionary  ${y}   state
			Should be Equal  ${s}  absent
		${w}=	Run	which ${PAC}
			Should not Contain  ${w}  ${PAC}

	test 4
		${x}=	apt    localhost   package=python-openssl   state=present
		${c}=	get certificate   localhost  host=www.onet.pl   port=443  proxy_host=1.1.2.2
		${e}=	get from dictionary  ${c}   expired
			Should not be True   ${e}

	test 5
		${x}=  nitz2
			log  ${x}

	test 6
		${w}=	command   localhost   uname -a
		${w}=	get from dictionary  ${w}   stdout
			Should Contain  ${w}  GNU/Linux

	test 7
		${x}= 	python requirements info  localhost
		${x}=	get from dictionary  ${x}   ansible_facts
		${x}=	get from dictionary  ${x}   discovered_interpreter_python
			Should Contain  ${x}  python

Support
-------

If the provided documentation is not enough, there are various support forums
available:

- `robotframework-users`_ mailing list

.. _Impansible: https://github.com/AdamPrzybyla/Impansible
.. _github: https://github.com/AdamPrzybyla/Impansible
.. _Robot Framework: http://robotframework.org
.. _Robot Framework User Guide: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-test-libraries
.. _PyPI: https://pypi.python.org/pypi/robotframework-impansible
.. _keyword Documentation: https://adamprzybyla.github.io/robotframework-Impansible.html
.. _pip: http://pip-installer.org
.. _robotframework-users: http://groups.google.com/group/robotframework-users
