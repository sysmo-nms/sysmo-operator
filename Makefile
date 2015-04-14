PYTHON_EXE   = /cygdrive/c/Python34/python.exe
DIST_DIR     = dist
BUILD_DIR    = build
RELEASE_NAME = sysmo-operator-win32
REL_VER	     ?= 1
QT_PLUGINS_DIR  = /cygdrive/c/Python34/lib/site-packages/PyQt5/plugins
EXECUTABLE = $(RELEASE_NAME)-$(REL_VER)/sysmo.exe

compile: $(EXECUTABLE) pyrrd4j/java_lib/Pyrrd4j.jar

pyrrd4j/java_lib/Pyrrd4j.jar:
	make -C pyrrd4j compile

$(EXECUTABLE): clean
	$(PYTHON_EXE) setup.py py2exe --include sip,ctypes,PyQt5.QtWebKit,PyQt5.QtPrintSupport,readline
	cp -r html $(DIST_DIR)
	cp -r graphics $(DIST_DIR)
	mkdir $(DIST_DIR)/pyrrd4j
	cp -r pyrrd4j/java_lib $(DIST_DIR)/pyrrd4j/
	cp -r $(QT_PLUGINS_DIR) $(DIST_DIR)
	cp qt.conf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	mv $(DIST_DIR) $(RELEASE_NAME)-$(REL_VER)

clean:
	rm -rf dist
	rm -rf build
	rm -rf $(RELEASE_NAME)-$(REL_VER)
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
	cd $(RELEASE_NAME)-$(REL_VER); ./sysmo.exe
