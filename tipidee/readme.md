
## build tipidee

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/tipidee/tipidee.spec ~/rpmbuild/SPECS/
rpmlint -v ~/rpmbuild/SPECS/tipidee.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/tipidee.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/tipidee.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/tipidee.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/tipidee.spec     #build RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi <rpm file>
rpm -ql <rpm file>
rpm -qpR <rpm file>
rpm -qp --provides <rpm file>
```
install and remove rpm
```sh
sudo rpm -ivh <rpm files>
sudo dnf remove -y s6       #remove a particular pacakage
yum list installed          #list all installed packages
rpm -qa                     #list all installed rpm packages.
rpm -q {package_name}       #list a particular package
```
is shared library ready?
```sh
ldconfig -p | grep tipidee
```
List the direct dependencies of the named package.
```sh
dnf repoquery --requires <package name>
dnf repoquery --deplist <package name>
dnf repoquery --installed --whatrequires <package name>
```
use the following command to find out which pa provides a perticular file.
```sh
rpm -qf {/path/to/file_name}
rpm -q --whatprovides {/path/to/file_name}
```
## prepare build dependencies
for this project, we already have all the dependencies.
```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/tipidee.spec
```
