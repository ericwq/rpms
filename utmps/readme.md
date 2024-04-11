
## build utmps

- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rpmdev-setuptree
cp ~/develop/rpms/utmps/utmps.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/utmps/utmps.pc ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/utmps.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/utmps.spec
rpmbuild -bs ~/rpmbuild/SPECS/utmps.spec
rpmbuild -bb ~/rpmbuild/SPECS/utmps.spec
```
check package information, contents, dependencies for rpm
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/utmps-libs-0.1.2.2-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/utmps-0.1.2.2-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/utmps-devel-0.1.2.2-1.fc39.x86_64.rpm
```
install and remove rpm
```sh
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/utmps-libs-0.1.2.2-1.fc39.x86_64.rpm
sudo dnf remove -y utmps
```
use the following command to find out which pa provides a perticular file.
```sh
rpm -qf {/path/to/file_name}
rpm -q --whatprovides {/path/to/file_name}
```
## prepare build dependencies
for this project, we already have all the dependencies.

```sh
sudo dnf builddep -y ~/rpmbuild/SPECS/utmps/utmps.spec
```
