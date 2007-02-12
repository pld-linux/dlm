Summary:	General-purpose distributed lock manager
Summary(pl.UTF-8):   Zarządca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
Version:	1.03.00
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	8eea23df70d2007c4fb8c234cfea49cf
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
Summary(pl.UTF-8):   Pliki nagłówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for DLM.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla DLM-a.

%package static
Summary:	Static DLM library
Summary(pl.UTF-8):   Statyczna biblioteka DLM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DLM library.

%description static -l pl.UTF-8
Statyczna biblioteka DLM.

%prep
%setup -q -n cluster-%{version}
install -d %{name}/include/cluster
install %{name}-kernel/src/{dlm.h,dlm_device.h} %{name}/include/cluster

cd %{name}
%{__perl} -pi -e 's/-g -O/%{rpmcflags}/' lib/Makefile

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}

%{__make} \
	CC="%{__cc}" \
	incdir=`pwd`/include

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/cluster
install include/cluster/*.h $RPM_BUILD_ROOT%{_includedir}/cluster

mv $RPM_BUILD_ROOT%{_libdir}/libdlm.so.*.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libdlm.so.*.*) \
        $RPM_BUILD_ROOT%{_libdir}/libdlm.so

mv $RPM_BUILD_ROOT%{_libdir}/libdlm_lt.so.*.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libdlm_lt.so.*.*) \
        $RPM_BUILD_ROOT%{_libdir}/libdlm_lt.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libdlm*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_libdir}/libdlm*.so
%{_includedir}/libdlm.h
%{_includedir}/cluster

%files static
%defattr(644,root,root,755)
%{_libdir}/libdlm*.a
