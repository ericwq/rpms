# rpms

With the help of fedora linux container, you can reproduce the rpm building process as you follow the instruction. The container is created according to [RPM Packaging Guide](https://rpm-packaging-guide.github.io/#introduction).

 The container contains:
- packages `gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools`.
- packages `sudo dnf-plugins-core tree git wget which ripgrep fzf pkgconfig`.
- create `packager` user and add packager to sudo list.

## requirement
To reproduce the buing process, you need `git` and `docker` on your local system.

## prepare container
Build the container first. Note: only one of the `docker build` is needed. The main difference is the former will use docker cache.
```sh
git clone https://github.com/ericwq/rpms.git
cd rpms
docker build -t rpm-builder:0.2.0 -f fedora.dockerfile .
docker build --no-cache --progress plain -t rpm-builder:0.2.0 -f fedora.dockerfile .
```
## run the container
Run the container as packager user. Note: I mount the local directory:`/Users/qiwang/dev` to the container's directory `/home/packager/develop`. this container also setup the timezone to shanghai,PRC. You can change it to mount you local directory and timezone.
```sh
docker run -u packager --rm -ti -h rpm-builder --env TZ=Asia/Shanghai --name rpm-builder --privileged \
        --mount type=bind,source=/Users/qiwang/dev,target=/home/packager/develop \
        rpm-builder:0.2.0
```

Next, follow the instructions for individual project.
- [skalibs](skalibs/readme.md) ready for test.
- [utmps](utmps/readme.md) not ready.
