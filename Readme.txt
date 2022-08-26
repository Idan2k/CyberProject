To launch this project run these commands on a kali linux distro:

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install sqlmap
sudo pip install -r requirements.txt
sudo pip3 install git+https://github.com/DanMcInerney/pymetasploit3.git#egg=pymetasploit3

To use nmap vulnerability scan script download this: https://github.com/vulnersCom/nmap-vulners
Place the files in a folder named nmap-vulners in /usr/share/nmap/scripts/
Add --vul to the command line arguments when launching the project.