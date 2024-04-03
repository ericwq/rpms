
## build s6

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/s6/s6.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/s6/{s6-svscanboot,s6.initd,s6.pre-install,s6.pre-upgrade,s6.trigger} ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/s6.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/s6.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/s6.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/s6.spec     #build RPMS
```
check package information, contents, dependencies for rpm
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/s6-devel-2.12.0.3-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/s6-2.12.0.3-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/s6-ipcserver-2.12.0.3-1.fc39.x86_64.rpm
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/s6-devel-static-2.12.0.3-1.fc39.x86_64.rpm
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
