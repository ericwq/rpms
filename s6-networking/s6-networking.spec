#
# spec file for package s6-networking
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  s6-networking
Version:  2.7.0.2
Release:  1%{?dist}
Summary:  skarnet.org's UCSPI TCP and TLS tools, access control tools, and network time management utilities
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: skalibs >= 2.14.1.0
Requires: execline >= 2.9.4.0
Requires: s6 >= 2.12.0.3
Requires: s6-dns >= 2.3.7.1
BuildRequires: pkgconfig(skalibs) >= 2.14.1.0
BuildRequires: execline-devel >= 2.9.4.0
BuildRequires: s6-devel >= 2.12.0.3
BuildRequires: pkgconfig(s6-dns) >= 2.3.7.1
BuildRequires: openssl-devel
BuildRequires: libretls-devel >= 3.8.1
BuildRequires: gcc pkgconfig
BuildRequires: make >= 3.81

%description
s6-networking is a suite of small networking utilities for Unix systems.
It includes command-line client and server management, TCP access
control, privilege escalation across UNIX domain sockets, IDENT protocol
management and clock synchronization. Optionally, it also includes
command-line TLS/SSL tools for secure communications.

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

%prep
%autosetup

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps \
	--enable-ssl=libtls
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_bindir}/*
%{_libdir}/*.so.*
%license COPYING

%files devel
%{_libdir}/*.so
%{_includedir}/*

%files devel-static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%changelog
* Mon Apr 15 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
