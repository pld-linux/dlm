Summary:	General-purpose distributed lock manager
Summary(pl.UTF-8):	Zarządca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
Version:	2.03.10
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	379b560096e315d4b52e238a5c72ba4a
URL:		http://sources.redhat.com/cluster/dlm/
BuildRequires:	perl-base
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

%package devel
Summary:	Header files and development documentation for DLM
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for DLM.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla DLM-a.

%package static
Summary:	Static DLM library
Summary(pl.UTF-8):	Statyczna biblioteka DLM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DLM library.

%description static -l pl.UTF-8
Statyczna biblioteka DLM.

%prep
%setup -q -n cluster-%{version}

%build
./configure \
	--cc="%{__cc}" \
	--cflags="%{rpmcflags} -Wall" \
	--ldflags="%{rpmldflags}" \
	--incdir=%{_includedir} \
	--ncursesincdir=%{_includedir}/ncurses \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--without_gfs \
	--without_gfs2 \
	--without_gnbd \
	--without_kernel_modules

%{__make} -C %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} -C %{name} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/cluster

mv $RPM_BUILD_ROOT%{_libdir}/libdlm.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libdlm.so.*.*) \
        $RPM_BUILD_ROOT%{_libdir}/libdlm.so

mv $RPM_BUILD_ROOT%{_libdir}/libdlm_lt.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libdlm_lt.so.*.*) \
        $RPM_BUILD_ROOT%{_libdir}/libdlm_lt.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libdlm.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libdlm.so.2
%attr(755,root,root) /%{_lib}/libdlm_lt.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libdlm_lt.so.2
%attr(755,root,root) %{_sbindir}/dlm_tool
#/etc/udev/rules.d/51-dlm.rules
%{_mandir}/man8/dlm_tool.8*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_libdir}/libdlm.so
%attr(755,root,root) %{_libdir}/libdlm_lt.so
%{_includedir}/libdlm.h
%{_mandir}/man3/dlm_*.3*
%{_mandir}/man3/libdlm.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libdlm.a
%{_libdir}/libdlm_lt.a
