Build dependencies
------------------
- C++/Qt5 development environment including QtCore, QtGui, QtNetwork and QtXml
- java JDK >= 7

Build procedure
---------------
Clone the repository:
```sh
$ git clone https://github.com/sysmo-nms/sysmo-operator.git
$ cd sysmo-operator
$ export REPOSITORY_ROOT=$(pwd)
```

### Java Part
```sh
$ cd rrd4qt/
$ ./gradlew installDist
```

### C++ Part
Will build the *sysmo-operator* target wich embed all required ressources (images, Java jars):
```sh
cd $REPOSITORY_ROOT
qmake -config release
make
```

For package mainteners: *make install* will only install the target in $INSTALL_ROOT/bin. For example to install *sysmo-operator* binary in /home/user/bin:
```sh
export INSTALL_ROOT=~
make install
```
If INSTALL_ROOT is ommited, *make install* will try to install in /bin wich is certainly not what you want.

Runtime dependencies
--------------------
- Qt5 (QtCore,QtGui,QtNetwork,QtXml) shared libraries
- Java >= 7