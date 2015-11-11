Runtime dependencies
--------------------
- Qt shared libraries
- Java 7 or 8

Build dependencies
------------------
- C++ build tools
- Qt5.X or Qt4.X >= 4.6 development environment

#### CentOS 7 dependency install example
```sh
$ sudo yum groupinstall 'Development Tools'
$ sudo yum install qt-devel
```

#### Debian 8 dependency install example
```sh
$ sudo apt-get install build-essentials qt-jdk
```

Building
--------
```sh
$ git clone https://github.com/sysmo-nms/sysmo-operator.git
$ cd sysmo-operator
$ qmake -config release
$ make
```

Deploying
---------
For package mainteners: *make install* will only install the target in $INSTALL_ROOT/bin. For example to install *sysmo-operator* binary in /home/user/bin:
```sh
export INSTALL_ROOT=~
make install
```
If INSTALL_ROOT is ommited, *make install* will try to install in /bin wich is certainly not what you want.
