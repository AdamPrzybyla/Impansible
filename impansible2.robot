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
