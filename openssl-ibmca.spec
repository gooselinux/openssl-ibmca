Summary: A dynamic OpenSSL engine for IBMCA
Name: openssl-ibmca
Version: 1.1
Release: 3%{?dist}
License: OpenSSL
Group: System Environment/Libraries
URL: http://sourceforge.net/projects/opencryptoki
Source0: http://downloads.sourceforge.net/opencryptoki/%{name}-%{version}.tar.gz
# fix linking
Patch0: openssl-ibmca-1.1-linking.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=584765
Patch1: openssl-ibmca-1.1-libica-soname.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libica
BuildRequires: libica-devel automake libtool
ExclusiveArch: s390 s390x

%description
A dynamic OpenSSL engine for IBMCA crypto hardware on IBM zSeries machines.


%prep
%setup -q
%patch0 -p1 -b .linking
%patch1 -p1 -b .libica-soname

sh ./bootstrap.sh


%build
%configure 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libibmca.la
mkdir -p $RPM_BUILD_ROOT%{_libdir}/openssl/engines
mv $RPM_BUILD_ROOT%{_libdir}/*.so $RPM_BUILD_ROOT%{_libdir}/openssl/engines

# make the config multilib-compatible
mv openssl.cnf.sample openssl.cnf.sample-%{_arch}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README openssl.cnf.sample-%{_arch}
%{_libdir}/openssl/engines/libibmca.so


%changelog
* Thu Aug  5 2010 Dan Horák <dhorak@redhat.com> - 1.1-3
- make the config multilib-compatible (#621152)
- Resolves: #621152

* Thu Apr 22 2010 Dan Horák <dhorak@redhat.com> - 1.1-2
- fixed opening of the libica library (#584765)
- Resolves: #584765

* Thu Mar  4 2010 Dan Horák <dhorak@redhat.com> - 1.1-1
- rebased to 1.1 instead of patching
- Resolves: #568847

* Thu Feb 18 2010 Dan Horák <dhorak@redhat.com> - 1.0.0-5
- added patch with port to libica 2.x API
- Related: #543948

* Wed Feb 10 2010 Dan Horák <dhorak@redhat.com> - 1.0.0-4
- added explicit dependency on libica, because it's dlopened
- Related: #543948

* Tue Jan 12 2010 Dan Horák <dhorak@redhat.com> - 1.0.0-3
- rebuild
- Related: #543948

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Dan Horak <dan[at]danny.cz - 1.0.0-1
- update to final 1.0.0
- spec file cleanup

* Thu Jun 21 2007 Phil Knirsch <pknirsch@redhat.com> - 1.0.0rc2-1.el5.4
- Fixed several issues with failure of using ibmca engine (#227644)

* Tue Dec 12 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.0rc2-1.el5.3
- Added missing symlinks for libs (#215735)
- Added samle config file (#215735)

* Thu Nov 23 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.0rc2-1.el5.2
- Necessary fix so openssl finds the module properly (#215735)

* Thu May 11 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.0rc2
- Initial package.
