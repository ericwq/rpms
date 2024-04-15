#
# spec file for package s6-rc
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  s6-rc
Version:  0.5.4.2
Release:  1%{?dist}
Summary:  Service manager for s6-based systems
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: skalibs-devel >= 2.14
BuildRequires: execline-devel >= 2.9.4.0
BuildRequires: s6-devel >= 2.12
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}

%description
s6-rc is a service manager for s6-based systems, i.e. a suite of
programs that can start and stop services, both long-running daemons
and one-time initialization scripts, in the proper order according
to a dependency tree. It ensures that long-running daemons are
supervised by the s6 infrastructure, and that one-time scripts are
also run in a controlled environment.

%package  devel
Summary:  Development files for %{name}
Group:	  Development/C
Requires: %{name} >= %{version}
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
* Thu Apr 11 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
