::
:: Appveyor script utility
::

:: Build CMake project
:build_cmake
@if exist build rmdir build /s /q
@set qt_path="C:\Qt\Qt5.7.0\5.7\msvc2015_64"
@set cmake_gen="Visual Studio 14 2015 Win64"
cmake -H. -Bbuild -G %cmake_gen% -DCMAKE_PREFIX_PATH=%qt_path% 

:: Build project
:build_project
@set ms_build="C:\Program Files (x86)\MSBuild\14.0\Bin\MSBuild.exe"
%ms_build% ".\build\sysmo-operator.sln" /p:configuration=release

:: Build installer component
:build_installer
@cd ".\build"
cpack

:: Build installer bundle
:build_bundle
@set ressources="%HOMEPATH%\SYSMO_OPERATOR_RESSOURCES"
@if not exist %ressources% mkdir %ressources%

@set vcredist_installer="%ressources%\msvc2015_vcredist_64.exe"
@set vcredist_location="http://www.sysmo.io/runtime/msvc2015/vc_redist.x64.exe"
if not exist %vcredist_installer% curl -fsSL -o %vcredist_installer% %vcredist_location%

@set java_installer="%ressources%\jre8_64.exe"
@set java_location="http://www.sysmo.io/runtime/jre/jre-8u111-windows-x64.exe"
if not exist %java_installer% curl -fsSL -o %java_installer% %java_location%

