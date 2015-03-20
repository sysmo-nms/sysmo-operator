# Makefile


JAVA		?= java
JAVAC		?= javac

# DEBUG
JAVA	= /cygdrive/c/Program\ Files/Java/jdk1.8.0_31/bin/java.exe
JAVAC   = /cygdrive/c/Program\ Files/Java/jdk1.8.0_31/bin/javac.exe
JAVAJAR = /cygdrive/c/Program\ Files/Java/jdk1.8.0_31/bin/jar.exe
# DEBUG END

# define java targets
JLIB	= java_lib
JBIN	= java_bin
JSRC	= java_src
JRRD4J	= $(JBIN)/io/sysmo/pyrrd4j/Pyrrd4j.class

JCLASSPATH_TMP  = $(JLIB)/*:$(JBIN)


ifeq ($(CYGW), CYGWIN)
	JCLASSPATH = '$(shell cygpath -awp $(JCLASSPATH_TMP))'
else
	JCLASSPATH = $(JCLASSPATH_TMP)
endif

#DEBUG
JCLASSPATH = '$(shell cygpath -awp $(JCLASSPATH_TMP))'
#DEBUG END

compile: java_lib/Pyrrd4j.jar 

java_lib/Pyrrd4j.jar: $(JRRD4J)
	$(JAVAJAR) cf java_lib/Pyrrd4j.jar -C java_bin io

clean:
	rm -f java_lib/Pyrrd4j.jar
	rm -rf java_bin/io

# java Pyrrd4j target
$(JRRD4J): $(JSRC)/Pyrrd4j.java
	$(JAVAC) -d $(JBIN) -classpath $(JCLASSPATH) $(JSRC)/Pyrrd4j.java

start:
	$(JAVA) -classpath $(JCLASSPATH) io.sysmo.pyrrd4j.Pyrrd4j
