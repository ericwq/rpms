
## build s6-rc

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/s6-rc/s6-rc.spec ~/rpmbuild/SPECS/
rpmlint -v ~/rpmbuild/SPECS/s6-rc.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6-rc.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/s6-rc.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/s6-rc.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/s6-rc.spec     #build RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/s6-rc-doc-0.5.4.2-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/s6-rc-0.5.4.2-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/s6-rc-devel-0.5.4.2-1.fc39.x86_64.rpm
```
install and remove rpm
```sh
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/s6-rc-devel-static-0.5.4.2-1.fc39.x86_64.rpm
sudo dnf remove -y s6
```
is shared library ready?
```sh
ldconfig -p | grep s6rc
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
sudo dnf builddep -y ~/rpmbuild/SPECS/s6.spec
```
