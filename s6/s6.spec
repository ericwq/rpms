#
# spec file for package execline
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}

Name:	  s6
Version:  2.12.0.2
Release:  1%{?dist}
Summary:  skarnet.org's small & secure supervision software suite.
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  s6-svscanboot
Source2:  s6.initd
Source3:  s6.pre-install
Source4:  s6.pre-upgrade
Source5:  s6.trigger
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
Requires: execline
Requires: %{name}-ipcserver = %{version}-%{release}
BuildRequires: skalibs-devel >= 2.14
BuildRequires: execline-devel

%description
s6 is a small suite of programs for UNIX, designed to allow process
supervision (a.k.a service supervision), in the line of daemontools
and runit, as well as various operations on processes and daemons.
It is meant to be a toolbox for low-level process and service
administration, providing different sets of independent tools that
can be used within or without the framework, and that can be
assembled together to achieve powerful functionality with a very
small amount of code.

%package  ipcserver
Summary:  Local service management and access control
Group:	  System/Base
Provides: %{name}-devel = %{version}
Obsoletes:%{name}-devel < %{version}
%description ipcserver
s6-ipcserver is an UCSPI server tool for Unix domain sockets, i.e.
a super-server. It accepts connections from clients, and forks a
program to handle each connection.

%package  devel
Summary:  Development environment for %{name}
Group:	  Development/C
Requires: %{name} = %{version}-%{release}
Provides: %{name}-devel = %{version}
Obsoletes:%{name}-devel < %{version}
%description devel
This package holds the development files for %{name}.

%package  devel-static
Summary:  Static %{name} library
Group:	  Development/C
Provides: %{name}-devel-static = %{version}
Obsoletes:%{name}-devel-static < %{version}
%description devel-static
This package contains the static version of the library used for development.

%package  doc
Summary:  Document for %{name}
%description doc
This package contains document for %{name}.

%prep
%autosetup -n %{name}-%{version}

%build
./configure --enable-shared --enable-static --disable-allstatic --enable-multicall \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps --enable-pedantic-posix
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

# rebuild the conflicted files (filesystem, bash package) in /usr/sbin
mkdir -p %{buildroot}%{_sbindir}
rm %{buildroot}%{_bindir}/{cd,umask,wait}
cd %{buildroot}%{_sbindir}
ln -s ../bin/execline cd
ln -s ../bin/execline umask
ln -s ../bin/execline wait

%files
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}/*

%files devel-static
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/*

%post
ldconfig

%postun
ldconfig

%license COPYING

%changelog
* Mon Apr 1 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
