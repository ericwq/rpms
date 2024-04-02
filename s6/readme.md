
## build s6

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/skalibs/s6.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/skalibs/{s6-svscanboot,s6.initd,s6.pre-install,s6.pre-upgrade,s6.trigger} ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/s6.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6.spec
rpmbuild -bs ~/rpmbuild/SPECS/s6.spec
rpmbuild -bb ~/rpmbuild/SPECS/s6.spec
```
check package information, contents, dependencies for rpm
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/
rpm -ql ~/rpmbuild/RPMS/x86_64/
rpm -qpR ~/rpmbuild/RPMS/x86_64/
sudo dnf remove -y s6
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
