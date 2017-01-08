:: Build CMake project

@if exist build rmdir build /s /q
git submodule update --init --recursive

@if not DEFINED PLATFORM (
    set qt_path=C:\Qt\Qt5.7.0\5.7\msvc2015_64
    set cmake_gen="Visual Studio 14 2015 Win64"
) else (
    @if /I "%PLATFORM%" == "Win32" (
        set qt_path=C:\Qt\5.7\msvc2015
        set cmake_gen="Visual Studio 14 2015"
    ) else (
        set qt_path=C:\Qt\5.7\msvc2015_64
        set cmake_gen="Visual Studio 14 2015 Win64"
    )
)

@set PATH=%qt_path%\bin;%PATH%

cmake -H. -Bbuild -G %cmake_gen% -DCMAKE_PREFIX_PATH=%qt_path%

