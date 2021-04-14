#!/bin/bash

curl -fL https://getcli.jfrog.io | sh

cd wheelhouse/audited/ || exit 1
export PATH_PREFIX=luxonis-python-snapshot-local/depthai

../../jfrog config add --artifactory-url=$ARTIFACTORY_URL --user=$ARTIFACTORY_USER --password=$ARTIFACTORY_PASS
../../jfrog rt u "*" "$PATH_PREFIX/"
