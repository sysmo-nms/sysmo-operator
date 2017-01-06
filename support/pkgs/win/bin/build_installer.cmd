:: Build installer component
@cd ".\build"
cpack

:: Build installer bundle
@set ressources="%HOMEPATH%\SYSMO_OPERATOR_RESSOURCES"
@if not exist %ressources% mkdir %ressources%
::
::@if "%PLATFORM%" == "Win32" (
::    @set VCREDIST_INSTALLER="%ressources%\msvc2015_vcredist_64.exe"
::    @set JAVA_INSTALLER="%ressources%\jre8_586.exe"
::    @set vcredist_location="http://www.sysmo.io/runtime/msvc2015/vc_redist.x64.exe"
::    @set java_location="http://www.sysmo.io/runtime/jre/jre-8u111-windows-586.exe"
::) else (
::    @set VCREDIST_INSTALLER="%ressources%\msvc2015_vcredist_32.exe"
::    @set JAVA_INSTALLER="%ressources%\jre8_64.exe"
::    @set vcredist_location="http://www.sysmo.io/runtime/msvc2015/vc_redist.x86.exe"
::    @set java_location="http://www.sysmo.io/runtime/jre/jre-8u111-windows-x64.exe"
::)
::if not exist %VCREDIST_INSTALLER% curl -fsSL -o %VCREDIST_INSTALLER% %vcredist_location%
::if not exist %JAVA_INSTALLER%     curl -fsSL -o %JAVA_INSTALLER%     %java_location%
::
:::: wix bundle
::@set PATH=C:\Program Files (x86)\Wix Toolset v3.10\bin;%PATH%
::@set wix_opts= -nologo -ext WixNetFxExtension -ext WixBalExtension -ext WixUtilExtension -ext WixFirewallExtension -ext WixUIExtension
::
::candle.exe %wix_opts% -o build\bundle.wixobj support\pkgs\win\bundle.wxs
::light.exe %wix_opts% -o build\Sysmo-Operator.exe build\bundle.wixobj
::
