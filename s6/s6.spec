#
# spec file for package execline
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none
%define _s6_service_path /run/service

Name:	  s6
Version:  2.12.0.3
Release:  1%{?dist}
Summary:  skarnet.org's small & secure supervision software suite
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  s6.service
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
Requires: execline
Requires: %{name}-ipcserver = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: skalibs-devel >= 2.14
BuildRequires: execline-devel
BuildRequires: systemd-rpm-macros

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
# change s6-svscan path in s6.service
sed -i "s|@@S6_SVSCAN_PATH@@|%{_bindir}|" %{SOURCE1}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -D -m 0755 %{SOURCE1} "%{buildroot}%{_unitdir}/s6.service"
cat %{SOURCE1}

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_bindir}/*
%exclude %{_bindir}/s6-applyuidgid
%exclude %{_bindir}/s6-ipcserver
%exclude %{_bindir}/s6-ipcserver-socketbinder
%exclude %{_bindir}/s6-ipcserverd
%{_libdir}/*.so.*
%config %{_unitdir}/s6.service

%files ipcserver
%{_bindir}/s6-applyuidgid
%{_bindir}/s6-ipcserver
%{_bindir}/s6-ipcserver-socketbinder
%{_bindir}/s6-ipcserverd

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}/*

%files devel-static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%pre
if [ $1 -eq 1 ]; then
	# package install
	echo "mark : pre install(done)"
	mkdir -p %{_s6_service_path}/
elif [ $1 -gt 1 ]; then
	# package upgrade
	echo "mark : pre upgrade"
fi
exit 0

%post
/sbin/ldconfig
%systemd_post %{name}.service
echo "mark : post install(done)"

%preun
%systemd_preun %{name}.service
echo "mark : pre uninstall(done)"

%postun
if [ $1 -eq 0 ]; then
	rm -rf %{_s6_service_path}/
fi
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service
echo "mark : post uninstall(done)"

%transfiletriggerin -- /run/service
echo "mark 4"
/bin/execlineb -P <<EOF
s6-svscanctl -an /run/service
EOF
echo "mark 5"

%transfiletriggerpostun -p /bin/execlineb -P -- /run/service
s6-svscanctl -an /run/service

%changelog
* Thu Apr 4 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
