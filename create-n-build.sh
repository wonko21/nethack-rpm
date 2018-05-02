#!/bin/bash

rm -rf ~/rpmbuild
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp ./nethack-361-src.tgz ~/rpmbuild/SOURCES
cp ./nethack.desktop ~/rpmbuild/SOURCES
cp ./*.patch ~/rpmbuild/SOURCES
rpmbuild -ba ./nethack.spec

