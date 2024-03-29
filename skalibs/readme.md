
## setup build environment
```sh
rpmdev-setuptree
cp /home/packager/develop/aprilsh/build/skalibs/skalibs.spec ~/rpmbuild/SPECS/
cp /home/packager/develop/aprilsh/build/skalibs/skalibs.pc ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/skalibs.spec
```

## download build dependencies
```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/skalibs.spec
```

## build rpm package
```sh
rpmbuild -bb ~/rpmbuild/SPECS/skalibs.spec
rm ~/rpmbuild/SOURCES/*.tar.gz
```
