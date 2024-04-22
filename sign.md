## Creating a New Public/Private PGP Key Pair
First create a batch template by running the following command.
```sh
mkdir -p ~/signed-rpm && echo "%echo Generating PGP key for rpm pacakges
Key-Type: RSA
Key-Length: 4096
Name-Real: Wang Qi
Name-Email: ericwq057@qq.com
Expire-Date: 0
%no-ask-passphrase
%no-protection
%commit" > ~/signed-rpm/pgp-key.batch
```
then generate it.
```sh
export GNUPGHOME="$(mktemp -d ~/signed-rpm/pgpkeys-XXXXXX)" && \
gpg --no-tty --batch --gen-key ~/signed-rpm/pgp-key.batch
```
We can also view all of our loaded keys with:
```sh
gpg --list-keys
```
exporting the public key.
```sh
gpg --armor --export "Wang Qi" > ~/signed-rpm/pgp-key.public
```
verify only a single key was exported by running:
```sh
cat ~/signed-rpm/pgp-key.public | gpg --list-packets
```
let’s export the private key so we can back it up somewhere safe.
```sh
gpg --armor --export-secret-keys "Wang Qi" > ~/signed-rpm/pgp-key.private
```
## Creating a yum Repository
import our private key, so we have access to it for signing the repo:
```sh
gpg --import ~/signed-rpm/pgp-key.private
```
configure the rpm tools to use this key for signing our packages and repository:
Don’t forget to replace E1933532750E9EEF with your key’s ID.
```sh
echo "%_signature gpg
%_gpg_name 7FCD29065EDF808E" > ~/.rpmmacros
```
Let’s create a directory for our packages:
```sh
mkdir -p ~/signed-rpm/packages/
```
Then copy our rpm(s) into this directory:
```sh
cp ~/rpmbuild/RPMS/x86_64/*.rpm ~/signed-rpm/packages/
```
We can add a signature to rpm packages by running:
```sh
rpm --addsign ~/signed-rpm/packages/*.rpm
```
Once all the packages are signed, we will use createrepo to create the repository:
```sh
cd ~/signed-rpm/packages/
createrepo .
```
Finally, we will sign the repodata metadata by running:
```sh
gpg --detach-sign --armor ./repodata/repomd.xml
```

## Testing the Repository
Note: we assume that rpm repo is served by tipidee.

copy public key to tipidee
```sh
sudo cp ~/signed-rpm/pgp-key.public /home/www/localhost/pgp-key.public
```
create a url for pacakges
```sh
sudo cp -r ~/signed-rpm/packages /home/www/localhost/packages
```
We will create a config for this server:
```sh
cd ~/signed-rpm/
echo "[skarnet-repo]
name=Skarnet.org Repo
baseurl=http://localhost/packages/
enabled=1
gpgcheck=1
gpgkey=http://localhost/pgp-key.public" > ~/signed-rpm/skarnet.repo
```
copy skarnet.repo to tipidee
```sh
sudo cp ~/signed-rpm/skarnet.repo /home/www/localhost/
```
configure our machine to use this new repository:
```sh
dnf config-manager --add-repo http://localhost/skarnet.repo
```
## Refer

- [Creating a New Public/Private PGP Key Pair](https://earthly.dev/blog/creating-and-hosting-your-own-deb-packages-and-apt-repo/)
- [Creating and hosting your own deb packages and apt repo](https://earthly.dev/blog/creating-and-hosting-your-own-deb-packages-and-apt-repo/)
- [create local dnf repos](https://blog.cykerway.com/posts/2020/06/09/create-local-dnf-repos.html)
- [Guide to Establishing and Hosting a Remote Yum Repository on GitHub](https://medium.com/debugging-diaries/guide-to-establishing-and-hosting-a-remote-yum-repository-on-github-b8326b60ac68)
- [HowTo Setup a Local YUM/DNF RPM Repository](https://github.com/taw00/howto/blob/master/howto-setup-a-local-yum-dnf-repository.md)
- [How to sign your custom RPM package with GPG key - chinese](https://gist.github.com/Rtoax/2fc39c6699e75185c25b53e0960425d7)
- [How to sign your custom RPM package with GPG key](https://gist.github.com/fernandoaleman/1376720)
