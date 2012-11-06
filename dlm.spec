# Conditional build:
%bcond_without	dlm_stonith	# build without fencing helper
#
Summary:	General-purpose distributed lock manager
Summary(pl.UTF-8):	Zarządca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
Version:	3.99.5
Release:	5
License:	LGPL v2.1+, GPL v2
Group:		Libraries
Source0:	http://people.redhat.com/teigland/%{name}-%{version}.tar.gz
# Source0-md5:	cad4999d0c42000bf5898af34f587728
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Source4:	dlm.conf
Patch0:		%{name}-link_order.patch
Patch1:		%{name}-after_configfs.patch
Patch2:		%{name}_stonith-build.patch
Patch3:		%{name}-mem_init.patch
Patch4:		%{name}-signals.patch
Patch5:		0003-dlm_controld-remove-fence_all-from-cli.patch
Patch6:		dlm_stonith-reboot.patch
Patch7:		dlm-startup_notify.patch
URL:		http://sources.redhat.com/cluster/dlm/
BuildRequires:	corosync-devel >= 2.0
%{?with_dlm_stonith:BuildRequires:	pacemaker-devel >= 1.1}
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	systemd-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	cluster-dlm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The DLM lock manager is a kernel-based VMS-like distributed lock
manager. It is general purpose and not specific to only GFS or CLVM.
Kernel and userspace locking API's are available.

%description -l pl.UTF-8
Zarządca blokad DLM to oparty na jądrze zarządca rozproszonych blokad
w stylu VMS. Jest ogólnego przeznaczenia, przeznaczonym nie tylko dla
GFS-a czy CLVM-a. Dostępne są API blokowania w jądrze i przestrzeni
użytkownika.

%package libs
Summary:	DLM libraries
Summary(pl.UTF-8):	Biblioteki DLM
Group:		Development/Libraries
Obsoletes:	cluster-dlm-libs

%description libs
DLM libraries.

%description libs -l pl.UTF-8
Biblioteki DLM.

%package devel
Summary:	Header files and development documentation for DLM
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	cluster-dlm-devel

%description devel
Header files and development documentation for DLM.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla DLM-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%{__make} \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir} \
	CC="%{__cc} %{rpmcflags} %{rpmcppflags} %{rpmldflags}"

%if %{with dlm_stonith}
%{__make} -C fence \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir} \
	CC="%{__cc} %{rpmcflags} %{rpmcppflags} %{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{systemdunitdir},/etc/{rc.d/init.d,sysconfig}} \
               $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
               $RPM_BUILD_ROOT{/var/run/dlm,%{systemdtmpfilesdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir}

%if %{with dlm_stonith}
%{__make} -C fence install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir}
%endif

install init/%{name}.service $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.license
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/%{name}
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
/lib/udev/rules.d/51-dlm.rules
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%verify(not md5 mtime size) %config(noreplace) /etc/sysconfig/%{name}
%{_mandir}/man8/*.8*
%{_mandir}/man5/dlm.conf.5*
%{systemdunitdir}/%{name}.service
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/run/dlm

%files libs
%defattr(644,root,root,755)
%ghost %{_libdir}/libdlm.so.3
%attr(755,root,root) %{_libdir}/libdlm.so.3.*
%ghost %{_libdir}/libdlm_lt.so.3
%attr(755,root,root) %{_libdir}/libdlm_lt.so.3.*
%ghost %{_libdir}/libdlmcontrol.so.3
%attr(755,root,root) %{_libdir}/libdlmcontrol.so.3.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdlm.so
%attr(755,root,root) %{_libdir}/libdlm_lt.so
%attr(755,root,root) %{_libdir}/libdlmcontrol.so
%{_includedir}/libdlm.h
%{_includedir}/libdlmcontrol.h
%{_mandir}/man3/dlm_*.3*
%{_mandir}/man3/libdlm.3*
%{_pkgconfigdir}/libdlm.pc
%{_pkgconfigdir}/libdlm_lt.pc

