#
# spec file for package utmps
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  utmps
Version:  0.1.2.2
Release:  1%{?dist}
Summary:  A secure utmp/wtmp implementation
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System Environment/Libraries

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  utmps.pc
Patch0:	  0001-add-stub-utmp.h.patch
Requires: s6-ipcserver >= 2.12
BuildRequires: skalibs-devel >= 2.14
BuildRequires: gcc make pkgconfig
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}

%description
utmps is a secure implementation of user accounting, using
a daemon as the only authority to manage the utmp and wtmp
data; programs running utmp functions are just clients to
this daemon.

%package  libs
Summary:  A secure utmp/wtmp implementation (libraries)
Group:	  Development/C
Requires: skalibs >= 2.14
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}

%description libs
This package holds the runtime library.

%package  devel
Summary:  A secure utmp/wtmp implementation (development files)
Group:	  Development/C
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig(skalibs-2.14.1.1)
Provides: %{name}-devel = %{version}
Obsoletes:%{name}-devel < %{version}

%description devel
This package holds the development headers for the library.

%package  static
Summary:  A secure utmp/wtmp implementation (static library)
Group:	  Development/C
Requires: skalibs-static
Provides: %{name}-static = %{version}
Obsoletes:%{name}-static < %{version}

%description static
This package contains the static library for %{name}.

%package  doc
Summary:  A secure utmp/wtmp implementation (documentation)

%description doc
This package contains document for %{name}.

%prep
# -N disables automatic patch
%autosetup -N
# use -p1 to remove the b/
# use -P 0 to apply patch 0
%patch -p 1 -P 0
sed -i "s|@@VERSION@@|%{version}|" %{SOURCE1}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# copy pkgconfig
install -D -m 0644 "%{SOURCE1}" "%{buildroot}%{_libdir}/pkgconfig/utmps.pc"

# move doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_bindir}/*
#%%{_sbindir}/*

%files libs
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/utmps.pc

%files static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%post
ldconfig

%postun
ldconfig

%license COPYING

%changelog
* Fri Apr 12 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
