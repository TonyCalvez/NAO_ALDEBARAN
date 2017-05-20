# NAO-ALDEBARAN
INSTALL C++ SDK - ALDEBARAN

0) The pre-requisites
sudo apt-get install gcc-multilib libc6-dev libc6-i386

1) Install: Python 2.7 (only) + CMake + QTCreator
-> sudo apt-get install build-essential checkinstall
-> sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
-> sudo apt-get install gcc cmake qtcreator
-> cd /usr/src
-> wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
-> tar xzf Python-2.7.13.tgz
-> cd Python-2.7.13
-> sudo ./configure
-> sudo make altinstall

2) Install: SDK Naoqi -> Online :https://developer.softbankrobotics.com/us-en/downloads/pepper

3) Install: qiBuild -> pip install qibuild

4) Configuration: qiBuild Toolchains
-> qibuild init --interactive
-> qitoolchain create linux <path/to/cpp/sdk>/toolchain.xml --
default
-> qitoolchain info

5) Workspace : Helloworld

6) Compilation 



Link: https://www.uv.mx/anmarin/papers/NAO_Tutorial.pdf
Link: http://dhrc.snu.ac.kr/nao-1-14-installation-guide-on-ubuntu-12-04/
