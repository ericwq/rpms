#
# spec file for package tipidee
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  tipidee
Version:  0.0.4.0
Release:  1%{?dist}
Summary:  A web server from skarnet.org
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: skalibs-devel >= 2.14.1.0
BuildRequires: s6-networking-devel >= 2.7.0.1
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}

%description
tipidee is a web server. It supports HTTP 1.0 and 1.1. It aims to be
compliant with RFC 9112: while it only implements a very limited subset
of the optional functionality in HTTP 1.1, it implements all the
mandatory parts. It is usable with both HTTP and HTTPS.

%package  devel
Summary:  Development files for %{name}
Group:	  Development/C
Requires: %{name} = %{version}
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

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir}/%{name} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

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

%changelog
* Mon Apr 15 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
