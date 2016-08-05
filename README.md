Sysmo Operator
==============

This is the repository of Sysmo Operator, the main UI for the Sysmo-core application.

Runtime dependencies
--------------------
- Qt shared libraries
- Java JRE 7 or 8

Build dependencies
------------------
- C++ build tools
- Qt5.X or Qt4.X >= 4.6 development environment
- Java JDK 7 or 8
- CMake

#### CentOS 7 dependency install example
```sh
$ sudo yum groupinstall 'Development Tools'
$ sudo yum install qt-devel cmake
```

#### Debian 8 dependency install example
```sh
$ sudo apt-get install build-essentials qt-jdk cmake
```

Building
--------
```sh
$ ./configure
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
