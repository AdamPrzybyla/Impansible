Robotframework library to access all ansible internal modules.
All Ansible modules are available as Robotframework's keywords.
The Impansible library can be used without Robotframework.

Example:
```
*** Variables ***
${PAC}   mtr
${ansible_password}  secret

*** Settings ***
library  Impansible
library  Collections
library  OperatingSystem

*** Test Cases ***
test 1
        ${x}=   Setup  localhost
        ${y}=   get from dictionary  ${x}   ansible_facts
        ${h}=   get from dictionary  ${y}   ansible_hostname
        ${z}=   get from dictionary  ${y}   ansible_distribution
        Should be Equal  ${z}  Ubuntu
        Should Contain   ${h}  tester
test 2
        [Timeout]    600
        ${x}=   apt    localhost   package=${PAC}   state=present
        ${x}=   get from dictionary  ${x}   invocation
        ${y}=   get from dictionary  ${x}   module_args
        ${s}=   get from dictionary  ${y}   state
        Should be Equal  ${s}  present
        ${w}=   Run     which ${PAC}
        Should Contain  ${w}  ${PAC}

test 3
        [Timeout]    600
        ${x}=   apt   localhost   package=${PAC}   state=absent
        ${x}=   get from dictionary  ${x}   invocation
        ${y}=   get from dictionary  ${x}   module_args
        ${s}=   get from dictionary  ${y}   state
        Should be Equal  ${s}  absent
        ${w}=   Run     which ${PAC}
        Should not Contain  ${w}  ${PAC}

test 4
        ${x}=   apt    localhost   package=python-openssl   state=present
        ${c}=   get certificate   localhost  host=www.onet.pl   port=443  proxy_host=1.1.1.1
        ${e}=   get from dictionary  ${c}   expired
        Should not be True   ${e}

test 5
        ${x}=  nitz2
        log  ${x}

test 6
        ${w}=   command   localhost   uname -a
        ${w}=   get from dictionary  ${w}   stdout
        Should Contain  ${w}  GNU/Linux
```

# sudo access example:

```

*** settings ***
Library  Impansible
Library  Collections

*** variables ***
${hostname}   localhost
# without sudo
#${ansible_password}  root_password
# with sudo
${ansible_user}  user_name
${ansible_become_password}  user_password

*** test cases ***
test 1
	${x}=   Setup  ${hostname}
        ${y}=   get from dictionary  ${x}   ansible_facts
        ${z}=   get from dictionary  ${y}   ansible_distribution
        Should be Equal  ${z}  Ubuntu
test 2
	${x}=   command  ${hostname}  id
	${x}=   get from dictionary  ${x}  stdout
        Should Contain   ${x}  root

```

# Requirements for selenium tests
```
*** Variables ***
${BROWSER}  firefox
${ansible_password}  XXXXXXX
${DBHost}  localhost
${DBName}  w3schools
${DBUser}  XXXXXX
${DBPass}  XXXXXX
${DBPort}  3306
${DBFile}  w3schools.sql
${Furl}    https://raw.githubusercontent.com/AndrejPHP/w3schools-database/master/w3schools.sql
${gr}      /etc/apt/sources.list.d/google-chrome.list
${grep}    http://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/
#${chrome_version}  False
${chrome_version}  google-chrome-stable_81.0.4044.138-1_amd64.deb

*** Settings ***
Library  Impansible
library  Collections
library  OperatingSystem
library  String
#Library  DatabaseLibrary
Libarary  SeleniumLibrary

*** Test Cases ***
do wp.pl tests
	[Setup]   Requirements
	Open Browser  http://wp.pl  ${BROWSER}
	${t}=  Get Title 
	Should contain  ${t}  Wirtualna
	

*** Keywords ***
Requirements
	The Operating System should be Ubuntu
	The Firefox browser should be installed if needed
	The Geckodriver should be installed if needed
	The google repo should be available
	The Chrome should be installed if needed
	The Chromedriver should be installed if needed
	#The MySQL server should be installed
	#Python should have MySQL support
	#The MySQL user have all privileges
	#Mysql should have no database imported
	#Mysql should have database imported

The Operating System should be Ubuntu
	${x}=	Setup  localhost
	${y}=	get from dictionary  ${x}   ansible_facts
	${z}=	get from dictionary  ${y}   ansible_distribution
	Should be Equal  ${z}  Ubuntu
	
The Firefox browser should be installed if needed
	[Timeout]    600
	${x}=  Convert To Lower Case  ${BROWSER}
	${x}=  Run Keyword and return status  Should Contain  ${x}  firefox
	Return from keyword if  not ${x}
	${x}=	apt    localhost   package=firefox   state=present
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  present
	${w}=	Run	which firefox
	Should Contain  ${w}  firefox

The Geckodriver should be installed if needed
	[Timeout]    600
	${x}=  Convert To Lower Case  ${BROWSER}
	${x}=  Run Keyword and return status  Should Contain  ${x}  firefox
	Return from keyword if  not ${x}
	${x}=	apt    localhost   package=firefox-geckodriver   state=present
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  present
	${w}=	Run	which geckodriver
	Should Contain  ${w}  geckodriver

The Chrome should be installed if needed
	[Timeout]    600
	${x}=  Convert To Lower Case  ${BROWSER}
	${x}=  Run Keyword and return status  Should Contain  ${x}  chrome
	       Return from keyword if  not ${x}
	${w}=	Run	which google-chrome-stable
	${x}=   run keyword and return status  Should Contain  ${w}  google-chrome-stable
	        Return from keyword if  ${x}
		run keyword if  "${chrome_version}"!="False"  apt  localhost  deb="${grep}${chrome_version}"
	${x}=	apt    localhost   package=google-chrome-stable   state=present
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  present
	${w}=	Run	which google-chrome-stable
	Should Contain  ${w}  google-chrome-stable

The Chromedriver should be installed if needed
	[Timeout]    600
	${x}=  Convert To Lower Case  ${BROWSER}
	${x}=  Run Keyword and return status  Should Contain  ${x}  chrome
	Return from keyword if  not ${x}
	${x}=	apt    localhost   package=chromium-chromedriver   state=present
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  present
	${w}=	Run	which chromedriver
	Should Contain  ${w}  chromedriver

The MySQL server should be installed
	[Timeout]    600
	${x}=	apt    localhost   package=mysql-server   state=present
	${x}=	get from dictionary  ${x}   invocation
	${y}=	get from dictionary  ${x}   module_args
	${s}=	get from dictionary  ${y}   state
		Should be Equal  ${s}  present
	${w}=	Run	which mysqld
		Should Contain  ${w}  mysqld

Python should have MySQL support
	[Timeout]    600
	${x}=	apt    localhost   package=python-mysqldb   state=present
	${x}=	get from dictionary  ${x}   invocation
	${y}=	get from dictionary  ${x}   module_args
	${s}=	get from dictionary  ${y}   state
		Should be Equal  ${s}  present

The MySQL user have all privileges
	[Timeout]    600
	${x}=	apt    localhost   package=python-mysqldb   state=present
	${x}=	get from dictionary  ${x}   invocation
	${y}=	get from dictionary  ${x}   module_args
	${s}=	get from dictionary  ${y}   state
		Should be Equal  ${s}  present
		mysql_user  localhost  name=${DBUser}  password=${DBPass}  priv=*.*:ALL

Mysql should have no database imported
	[Timeout]    600
	mysql db  localhost  name=${DBName}  state=absent

Mysql should have database imported
	[Timeout]    600
	mysql db  localhost  name=${DBName}  state=present
	Get url   localhost  url=${Furl}     dest=/tmp/${DBFile}
	mysql db  localhost  name=${DBName}  state=import  target=/tmp/${DBFile}

Mysql requirements
	The MySQL server should be installed
	Python should have MySQL support
	Mysql should have no database imported
	Mysql should have database imported
	The MySQL user have all privileges

The google repo should be available
	[Timeout]    600
	${x}=	Stat  localhost  path="${gr}"
        ${x}=   get from dictionary  ${x}   stat
        ${x}=   get from dictionary  ${x}   exists
		run keyword if  not ${x}  Copy  localhost  content='deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main'  dest="${gr}"
		run keyword if  not ${x}  shell  localhost  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
		run keyword if  not ${x}  apt  localhost  update_cache=yes
	${x}=	Stat  localhost  path="${gr}"
        ${x}=   get from dictionary  ${x}   stat
        ${x}=   get from dictionary  ${x}   exists
	Should be true  ${x}   "The google repo is not available"
```
