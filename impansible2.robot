*** settings ***
Library  Impansible
Library  Collections
Library  OperatingSystem

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

test 3
        
        Copy  localhost  content="ala ma kota"   dest=/tmp/xxxx0
        Copy  localhost  src=nitz   dest=/tmp/xxxx1
        ${x}=   Get File  nitz2
        Copy  localhost  content="${x}"   dest=/tmp/xxxx2
        Copy  localhost  src=x.robot   dest=/root/x.robot
