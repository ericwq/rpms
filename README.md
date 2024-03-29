# rpms

## prepare container for rpm package

create container according to [RPM Packaging Guide](https://rpm-packaging-guide.github.io/#introduction). The container insatll `gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools` packages. create `packager` user.

fedora: with newer protobuf-compiler and dnf
```sh
docker build -t rpm-builder:0.2.0 -f fedora.dockerfile .
docker build --no-cache --progress plain -t rpm-builder:0.2.0 -f fedora.dockerfile .
```
run fedora 39 container as packager
```sh
docker run -u packager --rm -ti -h rpm-builder --env TZ=Asia/Shanghai --name rpm-builder --privileged \
        --mount source=proj-vol,target=/home/packager/proj \
        --mount type=bind,source=/Users/qiwang/dev,target=/home/packager/develop \
        rpm-builder:0.2.0
```

build rpm for public repository
