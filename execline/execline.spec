#
# spec file for package execline
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  execline
Version:  2.9.5.1
Release:  1%{?dist}
Summary:  A small scripting language, to be used in place of a shell in non-interactive scripts.
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Libraries

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: skalibs >= 2.14.1.1
BuildRequires: pkgconfig(skalibs) >= 2.14.1.1
BuildRequires: gcc pkgconfig
BuildRequires: make >= 3.81

%description
execline is a (non-interactive) scripting language, like sh - but its
syntax is quite different from a traditional shell syntax. The
execlineb program is meant to be used as an interpreter for a text
file; the other commands are essentially useful inside an execlineb script.

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
%license COPYING

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}/*

%files devel-static
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/*

%changelog
* Mon Apr 1 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
