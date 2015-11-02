Build dependencies
------------------
- C++/Qt5.X or Qt4.8 development environment,
- java JDK >= 7 development tools.

### CentOS 7 exemple
```sh
$ sudo yum groupinstall 'Development Tools'
$ sudo yum install qt-devel java-1.7.0-openjdk-devel
$ git clone https://github.com/sysmo-nms/sysmo-operator.git
$ cd sysmo-operator
$ cd rrd4qt/
$ ./gradlew installDist
$ cd ..
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

### Runtime dependencies
- Qt shared libraries (QtCore,QtGui,QtNetwork,QtXml),
- Java >= 7