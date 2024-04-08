#
# spec file for package execline
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none

Name:	  s6
Version:  2.12.0.3
Release:  1%{?dist}
Summary:  skarnet.org's small & secure supervision software suite
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  s6-svscanboot
Source2:  s6.pre-install
Source3:  s6.pre-upgrade
Source4:  s6.trigger
Source5:  s6.service
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
Requires: execline
Requires: %{name}-ipcserver = %{version}-%{release}
BuildRequires: skalibs-devel >= 2.14
BuildRequires: execline-devel
BuildRequires: systemd-rpm-macros

%global _pre_install $(cat %SOURCE2)
%global _pre_upgrade $(cat %SOURCE3)
%global _file_trigger $(cat %SOURCE4)

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
# change s6-svscanboot path in s6.service
sed -i "s|@@S6_SVSCANBOOT_PATH@@|%{_libdir}|" %{SOURCE5}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -D -m 0755 %{SOURCE1} "%{buildroot}%{_libdir}/s6/s6-svscanboot"
install -D -m 0755 %{SOURCE5} "%{buildroot}%{_unitdir}/s6.service"
cat %{SOURCE5}

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
%{_libdir}/s6/s6-svscanboot
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
if [ "$1" = "1" ]; then
%{_pre_install}
echo "RPM is getting installed"
elif [ "$1" == "2" ]; then
%{_pre_upgrade}
echo "RPM is getting upgraded"
fi
ldconfig

%preun
%systemd_preun %{name}.service

%post
ldconfig
%systemd_post %{name}.service

%postun
ldconfig
%systemd_postun_with_restart %{name}.service

%filetriggerin — /run/service
echo "*****%{_file_trigger}"
%{_file_trigger}

%filetriggerun — /run/service
echo "*****%{_file_trigger}"
%{_file_trigger}

%license COPYING

%changelog
* Thu Apr 4 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
