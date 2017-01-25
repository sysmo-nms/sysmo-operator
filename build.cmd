::

@echo prepare
call support\packages\win\bin\build_prepare.cmd

@echo run
call support\packages\win\bin\build_run.cmd

@echo build installer
call _build\build_installer.cmd
