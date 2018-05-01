#!/bin/bash

rm -rf ~/rpmbuild
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp ./NetHack-3.6.1_Release.tar.gz ~/rpmbuild/SOURCES
cp ./nethack.desktop ~/rpmbuild/SOURCES
cp ./*.patch ~/rpmbuild/SOURCES
cp ./nethack.spec ~/rpmbuild/SPECS
pushd ~/rpmbuild/SPECS
rpmbuild -ba ./nethack.spec
popd
