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
$ git tag
```
Pick the latest release tag, in our case v1.1.1:
```sh
$ git checkout v1.1.1
$ qmake -config release
$ make
```

Deploying
---------
Everything is contained in the *sysmo-operator* executable. Move it somewhere
in your $PATH and you're done.
