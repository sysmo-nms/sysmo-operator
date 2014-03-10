PYTHON_EXE   = /cygdrive/c/Python27/python.exe
DIST_DIR     = dist
BUILD_DIR    = build
RELEASE_NAME = noctopus-win32
RELEASE_VERSION = 0.1
QT_PLUGINS_DIR  = /cygdrive/c/Python27/Lib/site-packages/PySide/plugins

win32Binary: clean
	$(PYTHON_EXE) setup.py py2exe
	cp -r html $(DIST_DIR)
	cp -r icons $(DIST_DIR)
	cp -r style $(DIST_DIR)
	cp -r $(QT_PLUGINS_DIR) $(DIST_DIR)
	cp qt.conf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	mv $(DIST_DIR) $(RELEASE_NAME)-$(RELEASE_VERSION)

clean:
	rm -rf dist
	rm -rf build
	rm -rf $(RELEASE_NAME)-$(RELEASE_VERSION)
	rm -f *.pyc
