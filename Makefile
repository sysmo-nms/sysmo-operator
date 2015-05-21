PYTHON_EXE   = /cygdrive/c/Python34/python.exe
DIST_DIR     = dist
BUILD_DIR    = build
RELEASE_NAME = sysmo-operator-win32
QT_PLUGINS_DIR  = /cygdrive/c/Python34/lib/site-packages/PyQt5/plugins
EXECUTABLE = $(RELEASE_NAME)/sysmo.exe

compile: py2exeBuild pyrrd4jBuild

pyrrd4jBuild:
	make -C pyrrd4j compile

py2exeBuild: clean
	$(PYTHON_EXE) setup.py py2exe --include sip,ctypes,PyQt5.QtWebKit,PyQt5.QtPrintSupport,readline
	cp -r html dist
	cp -r graphics dist
	mkdir dist/pyrrd4j
	cp -r pyrrd4j/java_lib dist/pyrrd4j/
	cp -r $(QT_PLUGINS_DIR) dist
	cp qt.conf dist

clean:
	rm -rf dist
	rm -rf build
	find . -name "*.pyc" -print | xargs rm -f
	find . -name "__pycache__" -print | xargs rm -rf

translate: 
	@R="`find . -name "*.py" -exec echo -n "{} " \;`"; \
	echo "SOURCES=$$R" > sysmo.pro; \
	echo "TRANSLATIONS=fr_FR.ts" >> sysmo.pro
	@pyside-lupdate sysmo.pro
	@ echo "Launching qt-linguist..."
	@ echo "Do not forget to release the file when finished (File->Release)"
	@linguist-qt4 fr_FR.ts

translate-clean:
	rm -f sysmo.pro
	rm -f *.ts

exe:
	cd build; ./sysmo.exe
