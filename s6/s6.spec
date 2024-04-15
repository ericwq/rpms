#
# spec file for package s6
#
# Contributor: Wang Qi <ericwq057@qq.com>
#

%define debug_package %{nil}
%define _build_id_links none
%define _s6_scan_dir %{_sharedstatedir}/s6/service

Name:	  s6
Version:  2.12.0.4
Release:  1%{?dist}
Summary:  skarnet.org's small & secure supervision software suite
License:  ISC
URL:	  https://skarnet.org/software/%{name}
Group:	  System/Base

%undefine _disable_source_fetch
Source0:  https://skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:  s6.service
Source2:  s6.svscan-boot
Source3:  s6.preset
Provides: %{name} = %{version}
Obsoletes:%{name} < %{version}
Requires: execline >= 2.9.4.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: skalibs-devel >= 2.14.1.0
BuildRequires: execline-devel >= 2.9.4.0
BuildRequires: systemd-rpm-macros

%description
s6 is a small suite of programs for UNIX, designed to allow process
supervision (a.k.a service supervision), in the line of daemontools
and runit, as well as various operations on processes and daemons.

Note: the scan directory is %{_s6_scan_dir}.

s6 managed services need to create their own service directories,
and symlink them to the scan directory.

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
# change s6.svscan-boot path and scan dir for s6
sed -i "s|@@S6_SVSCANBOOT_PATH@@|%{_libdir}\/s6|" %{SOURCE1}
sed -i "s|@@S6_SCAN_DIR@@|%{_s6_scan_dir}|" %{SOURCE1}

%build
./configure --enable-shared --enable-static --disable-allstatic \
	--libdir=%{_libdir} --dynlibdir=%{_libdir} --bindir=%{_bindir} \
	--libexecdir=%{_libexecdir} \
	--with-sysdeps=%{_libdir}/skalibs/sysdeps
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -D -m 0644 %{SOURCE1} "%{buildroot}%{_unitdir}/s6.service"
install -D -m 0755 %{SOURCE2} "%{buildroot}%{_libdir}/s6/s6.svscan-boot"
install -D -m 0644 %{SOURCE3} "%{buildroot}%{_presetdir}/50-s6.preset"

# move html doc
mkdir -p %{buildroot}%{_docdir}
mv "doc/" "%{buildroot}%{_docdir}/%{name}/"

%files
%{_bindir}/*
%{_libdir}/s6/*
%{_libdir}/*.so.*
%{_presetdir}/50-s6.preset
%config %{_unitdir}/s6.service
%license COPYING

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}/*

%files devel-static
%{_libdir}/*.a

%files doc
%{_docdir}/%{name}/*

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
if [ $1 -eq 0 ]; then
	rm -rf %{_s6_scan_dir}/
fi

%transfiletriggerin -- %{_s6_scan_dir}
s6-svscanctl -an %{_s6_scan_dir}
# echo 'trigger s6-svscan' | systemd-cat -p info

%transfiletriggerpostun -- %{_s6_scan_dir}
s6-svscanctl -an %{_s6_scan_dir}

%changelog
* Thu Apr 11 2024 Wang Qi <ericwq057@qq.com> - v0.1
- First version being packaged
