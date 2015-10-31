Sysmo operator
==============

This is the repository of Sysmo Operator, the main UI for the Sysmo-core application.

Build procedure with QtCreator
------------------------------

First clone the repository:
```sh
$ git clone https://github.com/sysmo-nms/sysmo-operator.git
```

### Java Part
There is some java in this project. Build it as is:
```sh
cd sysmo-operator/rrd4qt/
./gradlew installDist
```

### C++ Part
Sysmo require a complete Qt5 dev library installed.
```sh
cd ..
qmake -config release
make
```