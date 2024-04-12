## NOTICE: cancel this package

As the author of utmps Laurent said on skaware mail list:
```
All of that being said, however, my opinion is that you *should not*
package utmps for Fedora. utmp management is a distro-wide decision:
the utmp database is unique and accessed by several components in the
system. Fedora uses glibc, and glibc has its own utmp implementation,
and all the existing Fedora packages expect utmp to be managed by the
glibc implementation. Adding utmps, and packages that will use utmps,
will introduce conflict, and break things. (The utmp databases won't
have the correct permissions, glibc will access the files directly
without the locking that utmps does and concurrent access will cause
file corruption, etc.)

utmps isn't something that you can add like this and have some packages
depend on it and others not. It has to be a concerted effort by the whole
distribution, to decide if they switch to it or not. Alpine uses it
because musl doesn't provide a real utmp implementation; the transition
could be done incrementally without conflicting. glibc-based distros are
another story, a transition would need to be done atomically. And unless
you submit a proposal to Fedora and it is discussed and accepted by the
Powers That Be, it's not happening.
```
## build utmps

- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rpmdev-setuptree
cp ~/develop/rpms/utmps/utmps.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/utmps/{utmps.pc,0001-add-stub-utmp.h.patch} ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/utmps.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/utmps.spec
rpmbuild -bp ~/rpmbuild/SPECS/utmps.spec
rpmbuild -bc ~/rpmbuild/SPECS/utmps.spec
rpmbuild -bb ~/rpmbuild/SPECS/utmps.spec
```
check package information, contents, dependencies, provides for rpm
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/utmps-libs-0.1.2.2-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/utmps-0.1.2.2-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/utmps-devel-0.1.2.2-1.fc39.x86_64.rpm
rpm -qp --provides ~/rpmbuild/RPMS/x86_64/utmps-devel-0.1.2.2-1.fc39.x86_64.rpm
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
## reference

- [Automating patch application in specs %autosetup description](https://rpm-software-management.github.io/rpm/manual/autosetup.html)
- [spec file format](https://rpm-software-management.github.io/rpm/manual/spec.html)
