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
Group:	  System Environment/Libraries
%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
BuildRequires: skalibs >= 2.14

%description
execline is a (non-interactive) scripting language, like sh - but its syntax is quite different from a traditional shell syntax. The execlineb program is meant to be used as an interpreter for a text file; the other commands are essentially useful inside an execlineb script.

%package  devel
Summary:  A small scripting language, to be used in place of a shell in non-interactive scripts. (development files)
Group:	  Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
This subpackage holds the development headers and sysdeps files for the library.

%package  static
Summary:  A small scripting language, to be used in place of a shell in non-interactive scripts. (static library)
Group:	  Development/Libraries
%description static
This subpackage contains the static version of the library used for development.

%package  doc
Summary:  A small scripting language, to be used in place of a shell in non-interactive scripts. (document)
Requires: %{name} = %{version}-%{release}
%description doc
This subpackage contains document for %{name}.

%prep
%autosetup -n %{name}-%{version}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --with-dynlib=%{_libdir} --enable-multicall \
	--sysdepdir=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
ln -s ../../bin/execlineb "%{buildroot}/usr/bin/execlineb"


# move doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%defattr(-,root,root,0755)
%{_libdir}/libskarnet.so.*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libskarnet.so
%{_includedir}/skalibs/*
%{_libdir}/skalibs/sysdeps
%{_libdir}/pkgconfig/skalibs.pc

%files static
%defattr(-,root,root,0755)
%{_libdir}/libskarnet.a

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/*

%post
ldconfig

%postun
ldconfig

%license COPYING

%changelog
* Fri Mar 29 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
