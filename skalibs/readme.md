
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
spectool -g -R ~/rpmbuild/SPECS/skalibs.spec    #download the source
rpmbuild -bp ~/rpmbuild/SPECS/skalibs.spec      #build through %prep 
rpmbuild -bs ~/rpmbuild/SPECS/skalibs.spec      #build the sourece RPMS
rpmbuild -bb ~/rpmbuild/SPECS/skalibs.spec      #build the RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/skalibs-2.14.1.1-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/skalibs-devel-2.14.1.1-1.fc39.x86_64.rpm
rpm -qp --provides ~/rpmbuild/RPMS/x86_64/skalibs-devel-2.14.1.1-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/skalibs-devel-static-2.14.1.1-1.fc39.x86_64.rpm
```
install, update, remove and check rpm installed.
```sh
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/skalibs-devel-2.14.1.0-1.fc39.x86_64.rpm
sudo rpm -Uvh ~/rpmbuild/RPMS/x86_64/skalibs-devel-2.14.1.0-1.fc39.x86_64.rpm
sudo dnf remove -y skalibs  #remove a particular pacakage
yum list installed          #list all installed packages
rpm -qa                     #list all installed rpm packages.
rpm -q {package_name}       #list a particular package
```
is pkg-config package ready?
```sh
pkg-config --list-all
pkg-config --print-provides skalibs
```
is shared library ready?
```sh
ldconfig -p | grep skarnet
```
use the following command to find out which package provides a perticular file.
```sh
rpm -qf {/path/to/file_name}
rpm -q --whatprovides {/path/to/file_name}
```
## prepare build dependencies
for this project, we already have all the dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/skalibs.spec
```
