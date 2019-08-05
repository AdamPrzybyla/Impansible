*** settings ***
library  Impansible
library  Collections

*** variables ***
${MYGLOB}		OK
${hostname}		1.2.3.4
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
    ${x}=  Vmware Host Facts
    ${x}=  Get From Dictionary  ${x}  ansible_facts
    ${x}=  Get From Dictionary  ${x}  ansible_hostname
    should contain  ${x}   agare

test impossible with parameter
    ${x}=  Vmware Host Facts  hostname=2.3.4.5
    ${x}=  Get From Dictionary  ${x}  ansible_facts
    ${x}=  Get From Dictionary  ${x}  ansible_hostname
    should contain  ${x}   menas

test ping
    ${x}=  ping
    ${x}=  Get From Dictionary  ${x}  ping
    should be equal  ${x}   pong

test ping bang
    ${x}=  Ping  data=Bang!
    ${x}=  Get From Dictionary  ${x}  ping
    should be equal  ${x}   Bang!

test ping with suite variables
    Set My Ping Setup
    ${x}=  Ping
    ${x}=  Get From Dictionary  ${x}  ping
    should be equal  ${x}   Pif!

test python 
    ${x}=  Python Requirements Facts
    ${x}=  Get From Dictionary  ${x}  python_version
    ${y}=  Evaluate  sys.version  modules=sys
    should be equal  ${x}   ${y}

test python and picker
    ${x}=  Python Requirements Facts
    ${x}=  Picker  python_version
    ${y}=  Evaluate  sys.version  modules=sys
    should be equal  ${x}   ${y}

test xml
    ${x}=  Xml  path=bar.xml  xpath=/business/beers/beer  count=yes
    ${x}=  Get From Dictionary  ${x}  count
    should be equal  ${x}   ${3}


*** Keywords ***
Set My Ping Setup
    set suite variable   ${data}   Pif!
