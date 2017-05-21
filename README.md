# NAO-ALDEBARAN
## INSTALL C++ SDK - ALDEBARAN


### 0) Install: Choregraphe
```
-> Online : https://developer.softbankrobotics.com/us-en/downloads/pepper </br>
```


### 1) The pre-requisites </br>
```
-> sudo apt-get install build-essential checkinstall </br>
-> sudo apt-get install gcc-multilib libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libc6-i386 libbz2-dev </br>
```


### 2) Install: Python 2.7 (only) + CMake + QTCreator </br>
```
-> sudo apt-get install gcc cmake qtcreator </br>
-> cd /usr/src </br>
-> wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz </br>
-> tar xzf Python-2.7.13.tgz </br>
-> cd Python-2.7.13 </br>
-> sudo ./configure </br>
-> sudo make altinstall </br>
```


### 3) Install: SDK Naoqi </br>
```
-> Online : https://developer.softbankrobotics.com/us-en/downloads/pepper </br>
```

### 4) Install: qiBuild </br>
```
-> sudo apt install python-pip </br>
-> pip install qibuild </br>
```
```
  If qiBuild doesn't launch: 
	-> gedit ~/.bashrc and in the end of the file add: export PATH=${PATH}:${HOME}/.local/bin
```


### 5) Configuration: qiBuild Toolchains </br>
```
-> qibuild init --interactive </br>
-> qitoolchain create linux <path/to/cpp/sdk>/toolchain.xml -- default </br>
-> qitoolchain create mytoolchain <path/to/cpp/sdk>/toolchain.xml -- default </br>
-> qitoolchain info </br>
```


### 6) Workspace : Helloworld </br>
```
-> cd /usr/src/workspace
-> qibuild configure
-> qibuild make
```


### 7) Compilation </br>
```
-> cd /usr/src/areacompilation
-> ./helloworld --pip <robot_ip> --pport <robot_port>
```


Link: https://www.uv.mx/anmarin/papers/NAO_Tutorial.pdf
Link: http://dhrc.snu.ac.kr/nao-1-14-installation-guide-on-ubuntu-12-04/
