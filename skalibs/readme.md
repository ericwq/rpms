
## build skalibs

- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rpmdev-setuptree
cp ~/develop/rpms/skalibs/skalibs.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/skalibs/skalibs.pc ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/skalibs.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/skalibs.spec
rpmbuild -bs ~/rpmbuild/SPECS/skalibs.spec
rpmbuild -bb ~/rpmbuild/SPECS/skalibs.spec
```
check package information, contents, dependencies for rpm
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/skalibs-2.14.1.1-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/skalibs-devel-2.14.1.1-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/skalibs-static-2.14.1.1-1.fc39.x86_64.rpm
```

use the following command to find out which pa provides a perticular file.
```sh
rpm -qf {/path/to/file_name}
rpm -q --whatprovides {/path/to/file_name}
```
## prepare build dependencies
for this project, we already have all the dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/skalibs.spec
```
