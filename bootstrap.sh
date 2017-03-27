#!/bin/sh

CFLAGS="-g3 -gdwarf-2"
CXXFLAGS="-g3 -gdwarf-2"

for var in "$@"; do
    varname=$(echo $var | cut -s -f 1 -d =)
    if [ $varname = 'CFLAGS' ]; then
        CFLAGS=$(echo $var | cut -f 2 -d =)
        continue
    fi
    if [ $varname = 'CXXFLAGS' ]; then
        CXXFLAGS=$(echo $var | cut -f 2 -d =)
        continue
    fi
done

# cleanup build dir if exist
git submodule update --init
rm -rf _build

# create Unix Makefiles project
mkdir _build && cd _build && cmake -DCMAKE_CXX_FLAGS="${CXXFLAGS}" -DCMAKE_C_FLAGS="${CFLAGS}" ..; cd ..

echo -n "
.PHONY: all clean_all packages

all:
	make -C _build all

clean_all:
	rm -rf _build; rm Makefile
	rm -f Makefile
	rm -f code/config.h
	rm -f support/packages/obs/_service
	rm -f ressources/rrdio.qrc

%:
	make -C _build $@

packages:
	@echo "Trigger linux packages build from the current git repository revision"
	osc service remoterun home:sysmo:unstable sysmo-operator
	@echo "See result at: https://build.opensuse.org/package/show/home:sysmo:unstable/sysmo-operator"
" > Makefile

echo "You can now run \"make\""

