Sysmo Operator
==============
[![Build Status](https://travis-ci.org/sysmo-nms/sysmo-operator.svg?branch=master)](https://travis-ci.org/sysmo-nms/sysmo-operator)
[![Build status](https://ci.appveyor.com/api/projects/status/qlg4t5mi9lphvgj1/branch/master?svg=true)](https://ci.appveyor.com/project/ssbx/sysmo-operator-up4v8/branch/master)

This is the repository of Sysmo Operator, the main UI for the Sysmo-core application.

# Documentation

See the [Sysmo-NMS Wiki](https://github.com/sysmo-nms/sysmo-nms.github.io/wiki).

# Howto Deploy Sysmo-Operator

## Windows
Installer are [here](https://github.com/sysmo-nms/sysmo-operator/releases).

## Linux
You can find the repositories for your linux distribution [here](https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator).

Linux users can also use the "unstable" repository to enjoy the latest builds and enhencement [here](https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator)


## Prepare the build environment

### Dependencies
- git
- C++ build tools
- Qt5.X or Qt4.X >= 4.6 development environment
- Java JDK 7 or 8
- CMake

### Dependencies install examples
#### CentOS 7
```sh
$ sudo yum groupinstall 'Development Tools'
$ sudo yum install git qt-devel java-1.7.0-openjdk-devel cmake
```

#### Debian 8
```sh
$ sudo apt-get install git build-essentials qt-jdk openjdk-7-jdk cmake
```

#### MacOSX
```sh
$ brew install git qt java cmake
```

## Build
```sh
$ git clone https://github.com/sysmo-nms/sysmo-operator.git
$ cd sysmo-operator
$ ./bootstrap
$ make
```

## Deploy

### Runtime dependencies
- Qt shared libraries
- Java JRE 7 or 8

Everything is contained in the *build/sysmo-operator* executable. Move it somewhere
in the $PATH and you're done.

