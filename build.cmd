::

@echo prepare
call support\packages\win\bin\configure.cmd

@echo run
call support\packages\win\bin\make.cmd

@echo build installer
call _build\generate_bundle.cmd
