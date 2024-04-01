#
# spec file for package execline
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}

Name:	  execline
Version:  2.9.4.0
Release:  1%{?dist}
Summary:  A small scripting language, to be used in place of a shell in non-interactive scripts.
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Libraries

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
BuildRequires: pkgconfig(skalibs)

%description
execline is a (non-interactive) scripting language, like sh - but its
syntax is quite different from a traditional shell syntax. The
execlineb program is meant to be used as an interpreter for a text
file; the other commands are essentially useful inside an execlineb script.

%package  devel
Summary:  Development environment for %{name}
Group:	  Development/C
Requires: %{name} = %{version}-%{release}
Provides: %{name}-devel = %{version}
Obsoletes:%{name}-devel < %{version}
%description devel
This package holds the development headers and sysdeps files for the library.

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
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_sbindir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps --enable-pedantic-posix
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_sbindir}
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
