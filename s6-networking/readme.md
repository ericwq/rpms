
## build s6-networking

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/s6-networking/s6-networking.spec ~/rpmbuild/SPECS/
rpmlint -v ~/rpmbuild/SPECS/s6-networking.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6-networking.spec   #download the source
rpmbuild -bp ~/rpmbuild/SPECS/s6-networking.spec     #just prepre
rpmbuild -bc ~/rpmbuild/SPECS/s6-networking.spec     #just compile
rpmbuild -bb ~/rpmbuild/SPECS/s6-networking.spec     #build RPMS
```
check package information, contents, dependencies, provides for rpm.
```sh
rpm -qi <local rpm file>
rpm -ql <local rpm file>
rpm -qpR <local rpm file>
rpm -qp --provides <local rpm file>
```

install and remove rpm
```sh
sudo rpm -ivh <local rpm file>
sudo dnf remove -y s6
```

list install/erase scriptlets from package(s)
```sh
rpm --scripts -qp <local rpm file
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
download project dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/s6-networking.spec
```
