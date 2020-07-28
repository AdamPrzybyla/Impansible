*** Settings ***
Library  Impansible
Library  Collections
Library  OperatingSystem
library  String

*** Test Cases ***
test 1  
        ${x}=   Setup  local
        ${y}=   get from dictionary  ${x}   ansible_facts
        ${z}=   get from dictionary  ${y}   ansible_distribution
        	Should be Equal  ${z}  Ubuntu
test 2  
	${u}=  Get Environment Variable  USER
        ${x}=   command  local  id
        ${x}=   get from dictionary  ${x}  stdout
        	Should Contain   ${x}  ${u}

test 3  
        	Copy  local  content="ala ma kota"   dest=xxxx0
        	Copy  local  src=xxxx0   dest=xxxx1
        ${x}=   Get File  xxxx1
        	Copy  local  content="${x}"   dest=xxxx2
        	Copy  local  src=xxxx2   dest=xxxx3
        ${x}=   Get File  xxxx3
        	Should be Equal   ala ma kota  ${x}

test 4  
        ${x}=   Setup  local
        	log   ${x}   formatter=repr
        ${y}=  command  local  pip freeze --no-python-version-warning
        ${y}=   get from dictionary  ${y}   stdout
        	log   ${y}   formatter=repr
        	Should Contain  ${y}   impansible  impansible3.robot
