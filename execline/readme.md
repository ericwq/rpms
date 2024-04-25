
## build execline

- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rpmdev-setuptree
cp ~/develop/rpms/execline/execline.spec ~/rpmbuild/SPECS/
rpmlint -v ~/rpmbuild/SPECS/execline.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/execline.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/execline.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/execline.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/execline.spec     #build RPMS
rpmbuild -ba ~/rpmbuild/SPECS/execline.spec     #build RPMS and source RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/execline-2.9.5.1-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/execline-2.9.5.1-1.fc39.x86_64.rpm
rpm -qp --provides ~/rpmbuild/RPMS/x86_64/execline-devel-2.9.5.1-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/execline-devel-2.9.5.1-1.fc39.x86_64.rpm
```
install, update, remove and check rpm installed.
```sh
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/execline-devel-2.9.5.1-1.fc39.x86_64.rpm
sudo rpm -Uvh ~/rpmbuild/RPMS/x86_64/execline-devel-2.9.5.1-1.fc39.x86_64.rpm
sudo dnf remove -y execline #remove a particular pacakage
yum list installed          #list all installed packages
rpm -qa                     #list all installed rpm packages.
rpm -q {package_name}       #list a particular package
```
is shared library ready?
```sh
ldconfig -p | grep execline
```
List the direct dependencies of the named package.
```sh
dnf repoquery --requires <package name>
dnf repoquery --deplist <package name>
dnf repoquery --installed --whatrequires <package name>
```
use the following command to find out which package provides a perticular file.
```sh
rpm -qf {/path/to/file_name}
rpm -q --whatprovides {/path/to/file_name}
```
## prepare build dependencies
for this project, we already have all the dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/execline.spec
```
