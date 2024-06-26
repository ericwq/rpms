## creating a new PGP key pair
check exist keys.
```sh
gpg --list-keys
```
create keys using the interactive prompt:
```sh
gpg --full-generate-key
```
view all of our loaded keys with:
```sh
gpg --list-keys
```
exporting the public key.
```sh
gpg --armor --export "Wang Qi" > ~/repo/RPM-GPG-KEY-wangqi
```
import your public key to your RPM DB
```sh
sudo rpm --import ~/repo/RPM-GPG-KEY-wangqi
```
verify the list of gpg public keys in RPM DB
```sh
rpm -q gpg-pubkey
rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'
```
## sign rpm packages with PGP key
prepare rpmmacros:
```sh
echo "%_signature gpg
%_gpg_name Wang Qi" > ~/.rpmmacros
```
then copy our rpm(s) into this directory:
```sh
mkdir -p ~/repo/
cp -r ~/rpmbuild/SRPMS/ ~/repo/
cp -r ~/rpmbuild/RPMS/ ~/repo/
```
we can add a signature to rpm packages by running:
```sh
rpm --addsign ~/repo/SRPMS/*.rpm
rpm --addsign ~/repo/RPMS/x86_64/*.rpm
```
check the signature to make sure it was signed:
```sh
rpm --checksig <rpm file>
rpm -v --checksig <rpm file>
```

## creating a yum/dnf repository
Once all the packages are signed, we will use createrepo to create the repository:
```sh
cd ~/repo/
createrepo .
```
Finally, we will sign the repodata metadata by running:
```sh
gpg --detach-sign --armor ./repodata/repomd.xml
```

## test the repository
create a web server to serve the contents of our repository:
```sh
python3 -m http.server
```
We will create a config for this server:
```sh
echo "[skarnet-repo]
name=Skarnet.org Repo
baseurl=http://localhost:8000/
enabled=1
gpgcheck=1
gpgkey=http://localhost:8000/RPM-GPG-KEY-wangqi" > ~/repo/skarnet.repo
```
start tipidee web server, refer to [this instruction to install tipidee](tipidee/readme.md). copy repo to tipidee
```sh
sudo cp -r ~/repo/ /home/www/localhost/repo
sudo chown -R www:www /home/www/localhost/repo
sudo cp skarnet.repo  /home/www/localhost/repo
sudo chown www:www /home/www/localhost/repo/skarnet.repo
```
setup dnf to use this new repository:
```sh
sudo dnf clean metadata         #clean repo metadata
sudo dnf clean packages         #clean local cache
sudo dnf config-manager --add-repo http://localhost:8000/skarnet.repo
```
## publish to github pages
copy public key to repo
```sh
cp ~/develop/RPM-GPG-KEY-wangqi ~/repo/
```
create config for github page
```sh
echo "[skarnet-repo]
name=Skarnet.org Repo
baseurl=https://ericwq.github.io/rpms/repo
enabled=1
gpgcheck=1
gpgkey=https://ericwq.github.io/rpms/repo/RPM-GPG-KEY-wangqi" > ~/repo/skarnet.repo
```
clear previous rpms/repo, copy new repo content to rpms/repo.
```sh
cd ~/repo/
cp -r RPMS/ ~/develop/rpms/repo/
cp -r SRPMS/ ~/develop/rpms/repo/
cp -r repodata/ ~/develop/rpms/repo/
```
## back up and restore private key
let’s export the private key so we can back it up somewhere safe.
```sh
gpg --armor --export-secret-keys "Wang Qi" > ~/pgp-key.private
```
import the private key, so we can restore it from backup.
```sh
gpg --import ~/pgp-key.private
```

## delete PGP key pair
delete private key and public key.
```sh
gpg --delete-secret-keys "Wang Qi"
gpg --delete-keys "Wang Qi"
```
## Reference

- [Creating and hosting your own rpm packages and yum repo](https://earthly.dev/blog/creating-and-hosting-your-own-rpm-packages-and-yum-repo/)
- [Creating a New Public/Private PGP Key Pair](https://earthly.dev/blog/creating-and-hosting-your-own-deb-packages-and-apt-repo/)
- [Creating and hosting your own deb packages and apt repo](https://earthly.dev/blog/creating-and-hosting-your-own-deb-packages-and-apt-repo/)
- [create local dnf repos](https://blog.cykerway.com/posts/2020/06/09/create-local-dnf-repos.html)
- [Guide to Establishing and Hosting a Remote Yum Repository on GitHub](https://medium.com/debugging-diaries/guide-to-establishing-and-hosting-a-remote-yum-repository-on-github-b8326b60ac68)
- [HowTo Setup a Local YUM/DNF RPM Repository](https://github.com/taw00/howto/blob/master/howto-setup-a-local-yum-dnf-repository.md)
- [How to sign your custom RPM package with GPG key - chinese](https://gist.github.com/Rtoax/2fc39c6699e75185c25b53e0960425d7)
- [How to sign your custom RPM package with GPG key](https://gist.github.com/fernandoaleman/1376720)
