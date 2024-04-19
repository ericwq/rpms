#
# spec file for package tipidee
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none
%define _s6_service_dir %{_sharedstatedir}/s6/tipidee
%define _domain_name example.com
%define _doc_root /home/www

Name:	  tipidee
Version:  0.0.4.0
Release:  1%{?dist}
Summary:  A web server from skarnet.org
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  tipidee.sysusers
Source2:  index.html
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: skalibs >= 2.14.1.1
Recommends: s6-networking >= 2.7.0.2
BuildRequires: pkgconfig(skalibs) >= 2.14.1.1

%description
tipidee is a web server. It supports HTTP 1.0 and 1.1. It aims to be
compliant with RFC 9112: while it only implements a very limited subset
of the optional functionality in HTTP 1.1, it implements all the
mandatory parts. It is usable with both HTTP and HTTPS.

%package  devel
Summary:  Development files for %{name}
Group:	  Development/C
Requires: %{name} = %{version}
%description devel
This package contains development files for %{name}.

%package  devel-static
Summary:  Static %{name} library
Group:	  Development/C
%description devel-static
This package contains static library for %{name}.

%package  doc
Summary:  Document for %{name}
%description doc
This package contains document for %{name}.

%package  s6-example
Summary:  example %{name} configured as s6 service for http(s) and ivp(4|6).
Requires: %{name} = %{version}
BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}
%description s6-example
This package contains example configuration for %{name}.

configuration: %{_s6_service_dir}
document root: %{_doc_root}
tipidee log  : /home/www
%prep
%autosetup

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir}/%{name} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

# fix v2 bug for run script
sed -i "s|v2|v|" "examples/s6/httpd-4/run"

# prepare files for example
mkdir -p %{buildroot}%{_s6_service_dir}
cp -r "examples/s6/httpd-4" "%{buildroot}%{_s6_service_dir}"
cp -r "examples/s6/httpd-6" "%{buildroot}%{_s6_service_dir}"
cp -r "examples/s6/httpsd-4" "%{buildroot}%{_s6_service_dir}"
cp -r "examples/s6/httpsd-6" "%{buildroot}%{_s6_service_dir}"
cp "examples/tipidee.conf" "%{buildroot}%{_s6_service_dir}"

# prepare files for tipidee document root
mkdir -p "%{buildroot}%{_doc_root}/%{_domain_name}"
cd "%{buildroot}%{_doc_root}"
ln -s "%{_domain_name}" "%{_domain_name}:80"
ln -s "%{_domain_name}" "%{_domain_name}:443"
cp %{SOURCE2} .

# create symlink for tipidee s6 service
mkdir -p "%{buildroot}%{_sharedstatedir}/s6/service"
cd "%{buildroot}%{_sharedstatedir}/s6/service"
ln -s "../%{name}/httpd-4" "%{name}-httpd-4"
ls -al "%{buildroot}%{_sharedstatedir}/s6/service"

%pre s6-example
%sysusers_create_compat %{SOURCE1}
# fix log directory bug for log.run script
mkdir -p  /var/log/httpd-4
chown -R wwwlog:wwwlog /var/log/httpd-4

%post s6-example
# :> /etc/tipidee.conf && tipidee-config
tipidee-config -i "%{_s6_service_dir}/tipidee.conf"

%files
%{_bindir}/*
%{_libdir}/*.so.*
%{_libexecdir}/%{name}/*
%license COPYING

%files devel
%{_libdir}/*.so
%{_includedir}/*

%files devel-static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%files s6-example
%{_sysusersdir}/%{name}.conf
%{_s6_service_dir}/
%{_doc_root}/
%{_sharedstatedir}/s6/service/%{name}*

%changelog
* Mon Apr 15 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
