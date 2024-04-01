#
# spec file for package skalibs
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}

Name:	  skalibs
Version:  2.14.1.1
Release:  1%{?dist}
Summary:  Set of general-purpose C programming libraries for skarnet.org software.
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Libraries

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  skalibs.pc
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
BuildRequires: gcc make pkgconfig

%description
skalibs is a package centralizing the free software / open source C 
development files used for building all software at skarnet.org: it
contains essentially general-purpose libraries. You will need to 
install skalibs if you plan to build skarnet.org software.

%package  devel
Summary:  Development environment for %{name}
Group:	  Development/C
Requires: pkgconfig
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
This package contains html document for %{name}.

%prep
%autosetup -n %{name}-%{version}
sed -i "s|@@VERSION@@|%{version}|" -i %{SOURCE1}

%build
./configure  --libdir=%{_libdir} --dynlibdir=%{_libdir} \
	--sysdepdir=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# copy pkgconfig
install -D -m 0644 %{SOURCE1} "%{buildroot}%{_libdir}/pkgconfig/skalibs.pc"

# move doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/skalibs/sysdeps
%{_libdir}/pkgconfig/skalibs.pc

%files devel-static
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/*

%post
ldconfig

%postun
ldconfig

%changelog
* Mon Apr 01 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
