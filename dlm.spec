Summary:	General-purpose distributed lock manager
Summary(pl):	Zarz±dca rozproszonych blokad ogólnego przeznaczenia
Name:		dlm
%define	snap	20040625
Version:	0.0.0.%{snap}.1
Release:	1
License:	GPL
Group:		Libraries
Source0:	%{name}.tar.gz
# Source0-md5:	2aad29664265c6d2b4ab43276d4a45fd
Patch0:		%{name}-DESTDIR.patch
URL:		http://sources.redhat.com/cluster/
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
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for DLM.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty dla DLM-a.

%package static
Summary:	Static DLM library
Summary(pl):	Statyczna biblioteka DLM
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static DLM library.

%description static -l pl
Statyczna biblioteka DLM.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
./configure \
	--incdir=%{_includedir} \
	--kernel_src=%{_kernelsrcdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
