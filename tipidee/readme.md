
## build tipidee

- clean rpmbuild directory.
- run `rpmdev-setuptree` to create necessary directorys.
- copy build control files to `SPECS` and `SOURCES` directory.
- run `rpmlint` to check the spec file.

```sh
rm -rf rpmbuild
rpmdev-setuptree
cp ~/develop/rpms/tipidee/tipidee.spec ~/rpmbuild/SPECS/
cp ~/develop/rpms/tipidee/{tipidee.sysusers,index.html} ~/rpmbuild/SOURCES/
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
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/tipidee-0.0.4.0-1.fc39.x86_64.rpm
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/tipidee-s6-example-0.0.4.0-1.fc39.x86_64.rpm
sudo dnf remove -y tipidee-s6-example
sudo dnf remove -y tipidee              #remove a particular pacakage
yum list installed                      #list all installed packages
rpm -qa | grep 'tipidee'                #list all installed rpm packages.
rpm -q {package_name}                   #list a particular package
```
is shared library ready?
```sh
ldconfig -p | grep tipidee
```
check user/group is created.
```sh
getent passwd www wwwlog
getent group www
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
check tipidee server
```sh
curl http://localhost/index.html
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
