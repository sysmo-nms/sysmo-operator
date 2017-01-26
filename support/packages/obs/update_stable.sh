#!/bin/bash

echo "Release"

SOURCE_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TMP_DIR=$(mktemp -d)
function cleanup {
  rm -rf $TMP_DIR
}
trap cleanup EXIT

cd $TMP_DIR

osc checkout home:sysmo

cd home:sysmo/sysmo-operator/
cp $SOURCE_DIR/_service .
osc up
osc commit -m "_service file update for the Release repo"

