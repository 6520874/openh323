Summary:	OpenH323 Library
Name:		openh323
Version:	1.1pl1
Release:	1
License:	MPL
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.openh323.org/bin/%{name}_%{version}.tar.gz
Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-asnparser.patch
Patch2:		%{name}-no_samples.patch
URL:		http://www.openh323.org/
BuildRequires:	pwlib-devel
#BuildRequires:	pwlib-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
he OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%package devel
Summary:	OpenH323 development files
Summary(pl):	Pliki dla developerów OpenH323
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and libraries for developing applications that use
OpenH323.

%description -l pl devel
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OpenH323.

%package static
Summary:	OpenH323 static libraries
Summary(pl):	Biblioteki statyczne OpenH323
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
OpenH323 static libraries.

%description -l pl static
Biblioteki statyczne OpenH323.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPENH323DIR=`pwd`; export OPENH323DIR
%{__make} both OPTCCFLAGS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/openh323,%{_bindir},%{_datadir}/misc}

install lib/lib* $RPM_BUILD_ROOT%{_libdir}
install include/*.h $RPM_BUILD_ROOT%{_includedir}/openh323
#install samples/simple/obj_linux_x86_r/simph323 $RPM_BUILD_ROOT%{_bindir}

sed -e's@\$(OPENH323DIR)/include@&/openh323@' < openh323u.mak \
	> $RPM_BUILD_ROOT%{_datadir}/misc/openh323u.mak

gzip -9nf *.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/misc/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
