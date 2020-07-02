Code and docs for the individual raspberrypis that capture photos

# Initial setup

- Raspi-config
	```
  	sudo raspi-config
  	```
  	- Interfaces
		- Enable VNC
		- Enable camera
	- Advanced Options
		- Resolution
	```
  	sudo reboot
	```
	Note: Install VNC if it's not listed
	```
	sudo apt update
  	sudo apt install realvnc-vnc-server realvnc-vnc-viewer
	```
- Test headless VNC with VNC Viewer
- Update system 
	```
	sudo apt update
	sudo apt full-upgrade
	sudo reboot
	```
- Change Host Name
	```
	sudo nano /etc/hostname
	sudo nano /etc/hosts
	```
- Setup github ssh
	```
	eval "$(ssh-agent -s)"
	ssh-keygen -t rsa -b 4096 -C "atlasrider@gmail.com"
	ssh-add ~/.ssh/id_rsa
	cat ~/.ssh/id_rsa.pub
	```
	Add key to github account: https://github.com/settings/keys
- Clone repo
	```
	mkdir ~/dev
	cd ~/dev
	git clone git@github.com:AtlasRider/timelapse-pi.git
	```
- Python alias
	Add following line to `.bashrc`:
	```
	alias py="python3"
	```
- Install AWS CLI
	Install awscli
	```
 	py -m pip install awscli
	```
	Add following line to  `.bashrc`: 
	```
	export PATH=$PATH:~/.local/bin
	```
	Verify AWS is installed with:
	```
	aws --version
	```
	Configure AWS Credentials with:
	```
	aws configure
	```
	Check your local `~/dev/keys` folder for `campi.csv`. If it's not there, you can create a new key and use that.
- Install Python boto3 (AWS SDK)
	Run:
	```
	py -m pip install boto3
	```
- Reboot so hostname changes are applied
	```
	sudo reboot
	```
- Test script
	```
	py /home/pi/dev/timelapse-pi/client/scripts/main.py
	```
	Verify file was uploaded here: https://s3.console.aws.amazon.com/s3/buckets/atlascampi/?region=us-east-1&tab=overview
- Add cron job
	```
    crontab -e
	```
	Add line:
	```
	* * * * * python3 /home/pi/dev/timelapse-pi/client/scripts/main.py >/dev/null 2>&1
	```

# Troubleshooting

- Test script:
  ```
  python3 /home/pi/dev/timelapse-pi/client/scripts/main.py
  ```
- Checking CRON log:
	```
	grep CRON /var/log/syslog
	```
- Focusing camera
  ```
	raspistill -o hi.jpg && aws s3 cp hi.jpg s3://atlascampi
	```
