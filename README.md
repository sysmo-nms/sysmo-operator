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
...
```
Will build the java executable,

```sh
...
cd ..
rake java_ressource
```
Will place it where Qt can find it as ressource.

### C++ Part
Open the sysmo-operator.pro file with QtCreator, and build the project.

Sysmo-operator is developed with QtCreator 3.4 and built with Qt-5.4.1-GCC under Linux Ubuntu.14.LTS.


Build procedure using Qt libraries from major Linux distributions
-----------------------------------------------------------------
Any help is wellcome!
