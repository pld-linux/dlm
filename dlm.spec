Summary:	General-purpose distributed lock manager
Summary(pl.UTF-8):	Zarządca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
Version:	4.3.0
Release:	1
License:	LGPL v2.1+, GPL v2
Group:		Libraries
Source0:	https://releases.pagure.org/dlm/%{name}-%{version}.tar.gz
# Source0-md5:	6d6c65aff64971c7eceea2c00c73ecbd
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Source4:	%{name}.conf
Patch0:		old_udev_dir.patch
URL:		http://www.sourceware.org/cluster/dlm/
BuildRequires:	corosync-devel >= 3.1
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pacemaker-devel >= 1.1.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	systemd-devel >= 1:209
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Requires:	systemd-units >= 1:208-8
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	cluster-dlm < 4
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
Group:		Libraries
Obsoletes:	cluster-dlm-libs < 4

%description libs
DLM libraries.

%description libs -l pl.UTF-8
Biblioteki DLM.

%package devel
Summary:	Header files and development documentation for DLM
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	cluster-dlm-devel < 4

%description devel
Header files and development documentation for DLM.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla DLM-a.

%prep
%setup -q
%patch -P0 -p1

%if "%{cc_version}" < "8"
%{__sed} -i -e 's/-fstack-clash-protection//' {dlm_controld,dlm_tool,fence,libdlm}/Makefile
%endif

%build
%{__make} \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir} \
	CC="%{__cc} %{rpmcflags} %{rpmcppflags} %{rpmldflags}"

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

cp -p init/%{name}.service $RPM_BUILD_ROOT%{systemdunitdir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.license README.rst
%attr(755,root,root) %{_sbindir}/dlm_controld
%attr(755,root,root) %{_sbindir}/dlm_stonith
%attr(755,root,root) %{_sbindir}/dlm_tool
%dir %{_sysconfdir}/%{name}
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
/lib/udev/rules.d/51-dlm.rules
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%verify(not md5 mtime size) %config(noreplace) /etc/sysconfig/%{name}
%{_mandir}/man8/dlm_*.8*
%{_mandir}/man5/dlm.conf.5*
%{systemdunitdir}/%{name}.service
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/run/dlm

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdlm.so.3.*
%attr(755,root,root) %ghost %{_libdir}/libdlm.so.3
%attr(755,root,root) %{_libdir}/libdlm_lt.so.3.*
%attr(755,root,root) %ghost %{_libdir}/libdlm_lt.so.3
%attr(755,root,root) %{_libdir}/libdlmcontrol.so.3.*
%attr(755,root,root) %ghost %{_libdir}/libdlmcontrol.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdlm.so
%attr(755,root,root) %{_libdir}/libdlm_lt.so
%attr(755,root,root) %{_libdir}/libdlmcontrol.so
%{_includedir}/libdlm.h
%{_includedir}/libdlmcontrol.h
%{_pkgconfigdir}/libdlm.pc
%{_pkgconfigdir}/libdlm_lt.pc
%{_pkgconfigdir}/libdlmcontrol.pc
%{_mandir}/man3/dlm_*.3*
%{_mandir}/man3/libdlm.3*
