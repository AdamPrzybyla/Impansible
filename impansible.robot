*** settings ***
library  Impansible
library  Collections

*** variables ***
${MYGLOB}		OK
${hostname}		ubu
${password}		passwod
${datacenter}		vc01
${username}		root
${validate_certs}	${False}
&{networks}		VM Network=VM Network SB

*** test cases ***
test log
    log  works!

test dir
    ${x}=   nitz2   a=12  b=13  c=45
    ${x}=   Get From Dictionary  ${x}  \${SUITE_NAME}
    should be equal  ${x}   Impansible

test dict
    ${x}=   nitz2
    Log  ${x}
    ${x}=  Get From Dictionary  ${x}  \&{networks}
    ${x}=  Get From Dictionary  ${x}  VM Network
    should be equal  ${x}   VM Network SB

test possible
    set global variable  ${YY}   123
    set suite variable  ${YY1}   123
    ${x}=   nitz
    should be equal  ${x}   OK

test impossible
    ${x}=  vmware host facts  ${hostname}  hostname=h1 password=pas username=root validate_certs=no esxi_hostname=dmnode
    ${x}=  Get From Dictionary  ${x}  ansible_facts
    ${x}=  Get From Dictionary  ${x}  ansible_hostname
    should contain  ${x}   node

test ping
    ${x}=  Ping  ${hostname}
    ${x}=  Get From Dictionary  ${x}  ping
    should be equal  ${x}   pong

test python 
    ${x}=  Python Requirements Info  ${hostname}
    ${x}=  Get From Dictionary  ${x}  python_version
    should contain  ${x}   GCC

test python and picker
    ${x}=  Python Requirements Info  ${hostname}
    ${x}=  Picker  ${x}  python_version
    should contain  ${x}   GCC


test 1
	${x}=	Setup  ${hostname}
	${y}=	get from dictionary  ${x}   ansible_facts
	${h}=	get from dictionary  ${y}   ansible_hostname
	${z}=	get from dictionary  ${y}   ansible_distribution
	Should be Equal  ${z}  Ubuntu
	Should Contain   ${h}  tester
test 2
	${x}=	apt    ${hostname}   package=mtr   state=present
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  present
test 3
	${x}=	apt   ${hostname}   package=mtr   state=absent
        ${x}=	get from dictionary  ${x}   invocation
        ${y}=	get from dictionary  ${x}   module_args
        ${s}=	get from dictionary  ${y}   state
        Should be Equal  ${s}  absent

test 4
	${c}=	get certificate   ${hostname}  host=www.google.com   port=443  proxy_host=10.1.1.1
	${e}=	get from dictionary  ${c}   expired
	Should not be True   ${e}
