Summary:	General-purpose distributed lock manager
Summary(pl.UTF-8):	Zarządca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
Version:	3.99.5
Release:	2
License:	LGPL v2.1+, GPL v2
Group:		Libraries
Source0:	http://people.redhat.com/teigland/%{name}-%{version}.tar.gz
# Source0-md5:	cad4999d0c42000bf5898af34f587728
Patch0:		%{name}-link_order.patch
URL:		http://sources.redhat.com/cluster/dlm/
BuildRequires:	corosync-devel
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
Requires:	%{name} = %{version}-%{release}

%description libs
DLM libraries.

%description libs -l pl.UTF-8
Biblioteki DLM.

%package devel
Summary:	Header files and development documentation for DLM
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Obsoletes:	cluster-dlm-devel
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and development documentation for DLM.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla DLM-a.

%prep
%setup -q
%patch0 -p1

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
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBNUM=%{_lib} \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	MANDIR=%{_mandir} \
	HDRDIR=%{_includedir}


%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.license
%attr(755,root,root) %{_sbindir}/*
/lib/udev/rules.d/51-dlm.rules
%{_mandir}/man8/*.8*
%{_mandir}/man5/dlm.conf.5*

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

