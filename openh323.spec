
%define _snap 20040223
%define _snapver 02

Summary:	OpenH323 Library
Summary(pl.UTF-8):   Biblioteka OpenH323
Name:		openh323
Version:	1.13.1
Release:	0.%{_snap}.1
License:	MPL 1.0
Group:		Libraries
Source0:	http://snapshots.seconix.com/cvs/archive/%{name}-cvs_%{_snap}-%{_snapver}.tar.gz
# Source0-md5:	f8354a21dc5aacda9decc2a2de46316c
Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-asnparser.patch
Patch2:		%{name}-no_samples.patch
Patch3:		%{name}-lib.patch
Patch4:		%{name}-system-libs.patch
Patch5:		%{name}-ffmpeg.patch
Patch6:		%{name}-configure_fix.patch
Patch7:		%{name}-speex-float-sint-conv.patch
URL:		http://www.openh323.org/
BuildRequires:	autoconf
BuildRequires:	ffmpeg-devel >= 0.4.6
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	libstdc++-devel
BuildRequires:	lpc10-devel >= 1.5
BuildRequires:	pwlib-devel >= 1.5.0
BuildRequires:	speex-devel >= 1.0
%requires_eq	pwlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl.UTF-8
Celem projektu OpenH323 jest stworzenie w pełni funkcjonalnej i
wyposażonej implementacji protokołu telekonferencyjnego ITU H.323,
który może być używany przez użytkowników prywatnych i komercyjnych
bez opłat.

%package devel
Summary:	OpenH323 development files
Summary(pl.UTF-8):   Pliki dla developerów OpenH323
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	ffmpeg-devel
Requires:	pwlib-devel

%description devel
Header files and libraries for developing applications that use
OpenH323.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OpenH323.

%package static
Summary:	OpenH323 static libraries
Summary(pl.UTF-8):   Biblioteki statyczne OpenH323
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OpenH323 static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenH323.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0

%build
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPENH323DIR=`pwd`; export OPENH323DIR
OPENH323_BUILD="yes"; export OPENH323_BUILD
touch src/asnparser.version
%{__autoconf}
%configure


%{__make} -C src %{?debug:debugshared}%{!?debug:optshared} \
	CC=%{__cc} \
	CPLUS=%{__cxx} \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

#%%{__make} -C samples/simple %{?debug:debugshared}%{!?debug:optshared} \
#	CC=%{__cc} \
#	CPLUS=%{__cxx} \
#	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/openh323,%{_bindir},%{_datadir}/openh323}

# using cp as install won't preserve links
cp -d lib/lib* $RPM_BUILD_ROOT%{_libdir}
install include/*.h $RPM_BUILD_ROOT%{_includedir}/openh323
install version.h $RPM_BUILD_ROOT%{_includedir}/openh323
#install samples/simple/obj_*/simph323 $RPM_BUILD_ROOT%{_bindir}

sed -e's@\$(OPENH323DIR)/include@&/openh323@' < openh323u.mak \
	> $RPM_BUILD_ROOT%{_datadir}/openh323/openh323u.mak

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.txt
#%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/openh323

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
