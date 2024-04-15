
## build s6

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/s6/s6.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/s6/{s6.service,s6.svscan-boot,s6.preset} ~/rpmbuild/SOURCES/
rpmlint -v ~/rpmbuild/SPECS/s6.spec
```
run `rpmbuild` to build rpm.
```sh
spectool -g -R ~/rpmbuild/SPECS/s6.spec   #download the source
rpmbuild -bc ~/rpmbuild/SPECS/s6.spec     #just compile
rpmbuild -bs ~/rpmbuild/SPECS/s6.spec     #build source RPMS
rpmbuild -bb ~/rpmbuild/SPECS/s6.spec     #build RPMS
```
check package information, contents, dependencies for rpm.
```sh
rpm -qi ~/rpmbuild/RPMS/x86_64/s6-devel-2.12.0.3-1.fc39.x86_64.rpm
rpm -ql ~/rpmbuild/RPMS/x86_64/s6-2.12.0.3-1.fc39.x86_64.rpm
rpm -qpR ~/rpmbuild/RPMS/x86_64/s6-ipcserver-2.12.0.3-1.fc39.x86_64.rpm
```
is shared library ready?
```sh
sudo ldconfig -p | grep s6
```
install and remove rpm
```sh
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/s6-2.12.0.3-1.fc39.x86_64.rpm
sudo dnf remove -y s6
```

list install/erase scriptlets from package(s)
```sh
rpm --scripts -qp ~/rpmbuild/RPMS/x86_64/s6-2.12.0.3-1.fc39.x86_64.rpm
```
list filetrigger scriptlets from package(s)
```sh
rpm --filetriggers -qp ~/rpmbuild/RPMS/x86_64/s6-2.12.0.3-1.fc39.x86_64.rpm
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

## unit manage
list services
```sh
systemctl list-units                        #list running units
systemctl list-units --all                  #list all units
systemctl list-units --all --state=inactive #list all inactive units
systemctl list-units --type=service         #list all, running service units
systemctl list-units --failed               #list failed units
```
start/stop service
```sh
systemctl status s6.service                 #check service status
sudo systemctl enable s6.service            #enable service
sudo systemctl start s6.service             #start service
sudo systemctl restart s6.service           #restart service
sudo systemctl stop s6.service              #stop service
```
check the service log
```sh
sudo journalctl -u s6.service               #only show s6.service log
sudo journalctl -f -u s6.service            #keep reading the latest s6.service log
journalctl --dmesg                          #only show kernel message
```
send message to systemd journald
```sh
echo 'info message   ' | systemd-cat -p info
echo 'warning message' | systemd-cat -p warning
echo 'emerg message  ' | systemd-cat -p emerg
```
## reference

- [How to run systemd in a container](https://developers.redhat.com/blog/2019/04/24/how-to-run-systemd-in-a-container#enter_podman)
- [Understanding Systemd Units and Unit Files](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)
- [Packaging Guidelines: scriptlets: systemd](https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd)
- [File triggers](https://rpm-software-management.github.io/rpm/manual/file_triggers.html)
- [How to execute a script at %pre while installing/upgrading an rpm](https://www.golinuxhub.com/2018/05/how-to-execute-script-at-pre-post-preun-postun-spec-file-rpm/)
- [RPM + writing script in the spec file](https://stackoverflow.com/questions/5625382/rpm-writing-script-in-the-spec-file)
- [Support for File triggers](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/packaging_and_distributing_software/new-features-in-rhel-8_packaging-and-distributing-software#support-for-file-triggers_new-features-in-rhel-8)
- [Layout of the sysdeps Directory Hierarchy](https://www.gnu.org/software/libc/manual/html_node/Hierarchy-Conventions.html)
- [RPM Macros](https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/)
- [Install/Erase-time Scripts](https://ftp.osuosl.org/pub/rpm/max-rpm/s1-rpm-inside-scripts.html#S4-RPM-INSIDE-POST-SCRIPT)
- [s6](https://skarnet.org/software/s6/)
- [RPM scriptlet recipes](https://docs.pagure.org/packaging-guidelines/Packaging%3AScriptlets.html)
- [Maximum RPM](http://ftp.rpm.org/max-rpm/index.html)
- [Tutorial: Logging with journald](https://sematext.com/blog/journald-logging-tutorial/)
- [man journald.conf](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html)
- [man systemd-system.conf](https://www.freedesktop.org/software/systemd/man/latest/systemd-system.conf.html#)
- [man systemd.preset](https://www.freedesktop.org/software/systemd/man/latest/systemd.preset.html#)
- [Getting started with execline scripting](https://danyspin97.org/blog/getting-started-with-execline-scripting/)
- [Enable a systemd service at rpm installation](https://stackoverflow.com/questions/53435822/enable-a-systemd-service-at-rpm-installation)
