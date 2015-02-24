#!/bin/sh

export QT_QPA_PLATFORM_PLUGIN_PATH="C:\Python34\Lib\site-packages\PyQt5\plugins\platforms"
#export QT_QPA_PLATFORM_PLUGIN_PATH="C:\Windows\System32"

echo $QT_QPA_PLATFORM_PLUGIN_PATH
/cygdrive/c/Python34/python.exe ./sysmo.py
