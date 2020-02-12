Robotframework library to access all ansible internal modules.
All Ansible modules are available as Robotframework's keywords.
The Impansible library can be used without Robotframework.

Example:

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
