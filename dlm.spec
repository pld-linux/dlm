Summary:	General-purpose distributed lock manager
Summary(pl):	Zarz±dca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
%define	_pre	pre21
Version:	1.0
Release:	0.%{_pre}.3
License:	LGPL v2+
Group:		Libraries
Source0:	http://people.redhat.com/cfeist/cluster/tgz/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	37d5b471549af746ff93af7cac3b5a55
# from dlm-kernel CVS
Source1:	%{name}.h
# NoSource1-md5: 3a0b53233a22384762742d9b3b277969 (rev 1.12)
Source2:	%{name}_device.h
# NoSource2-md5: f2c1ed74c31b43b13581c48b1834e3c2 (rev 1.4)
URL:		http://sources.redhat.com/cluster/dlm/
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The DLM lock manager is a kernel-based VMS-like distributed lock
manager. It is general purpose and not specific to only GFS or CLVM.
Kernel and userspace locking API's are available.

%description -l pl
Zarz±dca blokad DLM to oparty na j±drze zarz±dca rozproszonych blokad
w stylu VMS. Jest ogólnego przeznaczenia, przeznaczonym nie tylko dla
GFS-a czy CLVM-a. Dostêpne s± API blokowania w j±drze i przestrzeni
u¿ytkownika.

%package devel
Summary:	Header files and development documentation for DLM
Summary(pl):	Pliki nag³ówkowe i dokumentacja programisty dla DLM-a
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for DLM.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty dla DLM-a.

%package static
Summary:	Static DLM library
Summary(pl):	Statyczna biblioteka DLM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DLM library.

%description static -l pl
Statyczna biblioteka DLM.

%prep
%setup -q -n %{name}-%{version}-%{_pre}

install -d include/cluster
cp -f %{SOURCE1} %{SOURCE2} include/cluster

%{__perl} -pi -e 's/-g -O/%{rpmcflags}/' lib/Makefile

%build
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
