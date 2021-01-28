# TempestClient

Mine cypto for tempest.my.to (minecraft server)
Go to [releases](https://github.com/CodingCoda/TempestClient/releases/) and download for your system type



## Windows 10
### You will need to disable antivirus or create an exception (This script relys on crypto mining). [Steps to disable](https://support.microsoft.com/en-us/windows/turn-off-antivirus-protection-in-windows-security-99e6004f-c54c-8509-773c-a4d776b77960). Make sure to reenable your antivirus when done!

Download the .exe release and double click to run (needs admin privilege)

## Ubuntu / MacOS
Download the .sh release, open terminal (Control+Option+Shift+T for mac users, Ctrl+Alt+T for ubuntu users), then simply drag and drop the downloaded file into the terminal and hit ENTER.
Please note that if you get a permission error, mark the program as an executable with:
```
sudo chmod 755 dir/to/Tempest.sh
```
Change /dir/to/Tempest.sh to where you installed the program or drag and drop it in. 

##### MacOS users will have brew installed when its running

## Python
If you wish, you can run the client with python 3.7 +. First install [python](https://www.python.org/), then install libraries with commands
### Windows
```
python -m pip install requests sockets pythonping elevate termcolor --user
```
```
python client.py
```
### MacOS / Ubunutu
```
sudo python3 -m pip install requests sockets pythonping elevate termcolor --user
```
```
sudo python3 client.py
```
### Embedded (Only with windows)
Download and unzip the embedded version from releases and run with run.bat

