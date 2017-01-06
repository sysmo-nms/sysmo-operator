:: wix bundle
::

@set PATH=C:\Program Files (x86)\Wix Toolset v3.10\bin;%PATH%
@set wix_opts= -nologo -ext WixNetFxExtension -ext WixBalExtension -ext WixUtilExtension -ext WixFirewallExtension -ext WixUIExtension

candle.exe %wix_opts% -o build\bundle.wixobj support\pkgs\win\bundle.wxs
light.exe %wix_opts% -o build\Sysmo-Operator.exe build\bundle.wixobj

