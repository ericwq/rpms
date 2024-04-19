# rpms

This project contains rpm spec and instructions to build rpm packages for Fedora, Centos, Redhat. Now it contains rpm spec for: [skalibs](https://skarnet.org/software/skalibs), [execline](https://skarnet.org/software/execline), [s6](https://skarnet.org/software/s6/), [s6-dns](https://skarnet.org/software/s6-dns/)

With the help of fedora linux container, you can reproduce the rpm building process as you follow the instruction. The container is created according to [RPM Packaging Guide](https://rpm-packaging-guide.github.io/#introduction).

 The container contains:
- the container is based on fedora:39.
- packages `gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools`.
- packages `sudo dnf-plugins-core tree git wget which ripgrep fzf pkgconfig`.
- packages `mock mock-scm createrepo_c`, refer to [Building package using Mock](https://developer.fedoraproject.org/deployment/rpm/about.html).
- `packager` user is created and added to sudo list.
- PID 1 is `/sbin/init`.

## requirement
To reproduce the buing process, you need `git` and `docker` on your local system.

## prepare the container
Build the container first. Note: only one of the `docker build` is needed. The main difference is the former will use docker cache.
```sh
git clone https://github.com/ericwq/rpms.git
cd rpms
docker build -t rpm-builder:0.2.0 -f fedora.dockerfile .
docker build --no-cache --progress plain -t rpm-builder:0.2.0 -f fedora.dockerfile .
```
## run the container
Run the container as packager user. Note: here I mount the local directory:`/Users/qiwang/dev` to the container's directory `/home/packager/develop`. This container also setup the timezone to shanghai,PRC. You can change it to mount your local directory and timezone.

start the container as daemon.
```sh
docker run --env TZ=Asia/Shanghai --tty --privileged --volume /sys/fs/cgroup:/sys/fs/cgroup:rw \
    --mount source=proj-vol,target=/home/packager/proj \
    --mount type=bind,source=/Users/qiwang/dev,target=/home/packager/develop \
    -h rpm-builder --name rpm-builder -d \
    rpm-builder:0.2.0
```

login the container as packager or root.
```sh
docker exec -u packager -it rpm-builder bash
docker exec -u root -it rpm-builder bash
```

## build rpm packages
Next, follow the instructions for individual project. Note, you must follow the following order (top -> down) to build indivial rpm packages, there are dependency rule.
- [skalibs](skalibs/readme.md)👌
- [execline](execline/readme.md)👌
- [s6](s6/readme.md)👌
- [utmps](utmps/readme.md)❌
- [s6-dns](s6-dns/readme.md)👌
- [s6-networking](s6-networking/readme.md)👌
- [s6-rc](s6-rc/readme.md)👌
- [tipidee](tipidee/readme.md)🏗

## license
[ISC](https://en.wikipedia.org/wiki/ISC_license)

## reference
- [s6 packaging for debian](https://github.com/multiplexd/s6-packaging)
- [How to handle dynamic and static libraries in Linux](https://opensource.com/article/20/6/linux-libraries)
