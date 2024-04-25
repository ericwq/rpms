
## build s6-dns

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/s6-dns/s6-dns.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/s6-dns/s6-dns.pc ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/s6-dns.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6-dns.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/s6-dns.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/s6-dns.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/s6-dns.spec     #build RPMS
rpmbuild -ba ~/rpmbuild/SPECS/s6-dns.spec     #build RPMS and source RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi <local rpm file>
rpm -ql <local rpm file>
rpm -qpR <local rpm file>
rpm -qp --provides <local rpm file>
```
is pkg-config package ready?
```sh
pkg-config --list-all
pkg-config --print-provides s6-dns
```
is shared library ready?
```sh
ldconfig -p | grep -E 's6dns|skadns'
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
for this project, we already have all the dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/s6-dns.spec
```
