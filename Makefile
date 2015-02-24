PYTHON_EXE   = /cygdrive/c/Python27/python.exe
DIST_DIR     = dist
BUILD_DIR    = build
RELEASE_NAME = noctopus-win32
RELEASE_VERSION = 0.1
QT_PLUGINS_DIR  = /cygdrive/c/Python27/Lib/site-packages/PySide/plugins

compile: win32Binary

win32Binary: clean
	$(PYTHON_EXE) setup.py py2exe
	cp -r html $(DIST_DIR)
	cp -r graphics $(DIST_DIR)
	cp -r $(QT_PLUGINS_DIR) $(DIST_DIR)
	cp qt.conf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	mv $(DIST_DIR) $(RELEASE_NAME)-$(RELEASE_VERSION)

clean:
	rm -rf dist
	rm -rf build
	rm -rf $(RELEASE_NAME)-$(RELEASE_VERSION)
	find . -name "*.pyc" -print | xargs rm -f
	find . -name "__pycache__" -print | xargs rm -rf

translate: 
	@R="`find . -name "*.py" -exec echo -n "{} " \;`"; \
	echo "SOURCES=$$R" > noctopus.pro; \
	echo "TRANSLATIONS=fr_FR.ts" >> noctopus.pro
	@pyside-lupdate noctopus.pro
	@ echo "Launching qt-linguist..."
	@ echo "Do not forget to release the file when finished (File->Release)"
	@linguist-qt4 fr_FR.ts

translate-clean:
	rm -f noctopus.pro
	rm -f *.ts
