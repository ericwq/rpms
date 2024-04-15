#
# spec file for package s6-dns
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  s6-dns
Version:  2.3.7.1
Release:  1%{?dist}
Summary:  skarnet.org's DNS client libraries and command-line DNS client utilities
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  s6-dns.pc
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: skalibs-devel >= 2.14
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}

%description
s6-dns is a suite of DNS client programs and libraries for Unix systems,
as an alternative to the BIND, djbdns or other DNS clients.

%package  devel
Summary:  Development files for %{name}
Group:	  Development/C
Requires: %{name} = %{version}
Provides: pkgconfig(%{name}) = %{version}-%{release}
Provides: %{name}-devel = %{version}
Obsoletes:%{name}-devel < %{version}
%description devel
This package contains development files for %{name}.

%package  devel-static
Summary:  Static %{name} library
Group:	  Development/C
Provides: %{name}-devel-static = %{version}
Obsoletes:%{name}-devel-static < %{version}
%description devel-static
This package contains static library for %{name}.

%package  doc
Summary:  Document for %{name}
%description doc
This package contains document for %{name}.

%prep
%autosetup
sed -i "s|@@VERSION@@|%{version}|" %{SOURCE1}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -D -m 0644 %{SOURCE1} "%{buildroot}%{_libdir}/pkgconfig/s6-dns.pc"

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
%{_libdir}/pkgconfig/*.pc

%files devel-static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%changelog
* Sat Apr 13 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
