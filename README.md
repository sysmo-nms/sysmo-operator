Sysmo Operator
==============
[![Build Status](https://travis-ci.org/sysmo-nms/sysmo-operator.svg?branch=master)](https://travis-ci.org/sysmo-nms/sysmo-operator)
[![Appveyor Build Status](https://ci.appveyor.com/api/projects/status/github/sysmo-nms/sysmo-operator?branch=master&svg=true)](https://ci.appveyor.com/project/ssbx/sysmo-operator)

This is the repository of Sysmo Operator, the main UI for the Sysmo-core application.

Runtime dependencies
--------------------
- Qt shared libraries
- Java 7 or 8

Build dependencies
------------------
- C++ build tools
- Qt5.X or Qt4.X >= 4.6 development environment
- CMake

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
$ git submodule update --init
$ mkdir build
$ cd build
$ cmake ..
$ make
```

Deploying
---------
Everything is contained in the *build/sysmo-operator* executable. Move it somewhere
in your $PATH and you're done.

TODO
----
- Splash screen with application startup progress
- Timeline
- modify probe
- modify target
- status buttons and filters
