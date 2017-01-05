
@if exist build rmdir build /s /q

@set qt_path="C:\Qt\Qt5.7.0\5.7\msvc2015_64"
@set cmake_gen="Visual Studio 14 2015 Win64"
cmake -H. -Bbuild -G %cmake_gen% -DCMAKE_PREFIX_PATH=%qt_path% 

@set ms_build="C:\Program Files (x86)\MSBuild\14.0\Bin\MSBuild.exe"
%ms_build% ".\build\sysmo-operator.sln" /p:configuration=release

@cd ".\build"
cpack
