# TempestClient

Mine cypto for tempest.my.to (minecraft server)
Go to [releases](https://github.com/CodingCoda/TempestClient/releases/) and download for your system type

## Windows - 10
Download the .exe release and double click to run

## Ubuntu / MacOS
Download the .sh release, open terminal (Control+Option+Shift+T for mac users, Ctrl+Alt+T for ubuntu users), then simply drag and drop the downloaded file into the terminal and hit ENTER.
Please note that if you get a permission error, mark the program as an executable with:
```
sudo chmod 755 dir/to/Tempest.sh
```
Change /dir/to/Tempest.sh to where you installed the program or drag and drop it in

## Python
If you wish, you can run the client with python 3.7 +. First install [python](https://www.python.org/), then install libraries with command
```
python -m pip install requests sockets pythonping elevate termcolor --user
```
and
```
python client.py
```
on windows or on MacOS / Ubunutu
```
python3 -m pip install requests sockets pythonping elevate termcolor --user
```
and
```
python client.py
```
