# To build a static RPM, add
#     --define "static 1"
# to the rpmbuild command line.

%define name nmap
%define version 4.76
%define release 1
%define _prefix /usr

Summary: Network exploration tool and security scanner
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 2
License: http://nmap.org/man/man-legal.html
Group: Applications/System
Source0: http://nmap.org/dist/%{name}-%{version}.tgz
URL: http://nmap.org

# RPM can't be relocatable until I stop storing path info in the binary.
# Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root

%description
Nmap is a utility for network exploration or security auditing. It
supports ping scanning (determine which hosts are up), many port
scanning techniques, version detection (determine service protocols
and application versions listening behind ports), and TCP/IP
fingerprinting (remote host OS or device identification). Nmap also
offers flexible target and port specification, decoy/stealth scanning,
sunRPC scanning, and more. Most Unix and Windows platforms are
supported in both GUI and commandline modes. Several popular handheld
devices are also supported, including the Sharp Zaurus and the iPAQ.

%prep
%setup -q

%build
%configure --without-openssl --without-zenmap --with-libdnet=included --with-libpcap=included --with-libpcre=included --with-liblua=included
%if "%{static}" == "1"
make static
%else
make
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
strip $RPM_BUILD_ROOT%{_bindir}/* || :
gzip $RPM_BUILD_ROOT%{_mandir}/man1/* || :

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc COPYING
%doc docs/README
%doc docs/nmap.usage.txt
%doc %{_prefix}/share/man/man1/nmap.1.gz
%{_bindir}/nmap
%{_datadir}/nmap

%changelog

* Mon Sep 08 2008 David Fifield (david(a)bamsoftware.com)
- Build with --with-openssl rather than --without-openssl.

* Thu Nov 08 2007 David Fifield (david(a)bamsoftware.com)
- Split the zenmap subpackage into its own spec file.

* Tue Nov 06 2007 David Fifield (david(a)bamsoftware.com)
- Fix the Zenmap build on 64-bit architectures (where %{_libdir} is
  "/usr/lib64" but Python modules may not be installed there) and make
  it work with different versions of Python.

* Sun Nov 04 2007 David Fifield (david(a)bamsoftware.com)
- Add a zenmap subpackage.

* Wed Oct 31 2007 David Fifield (david(a)bamsoftware.com)
- Remove references to buildfe (build the NmapFE frontend).

* Sat Sep 01 2004 Stephane Loeuillet (stephane.loeuillet(a)tiscali.fr)
- Place .desktop file under ${prefix}/share/applications rather than
  ${prefix}/share/gnome/apps/Utilities

* Mon Dec 16 2002 Matthieu Verbert (mve(a)zurich.ibm.com)
- Place man pages under ${prefix}/share/man rather than ${prefix}/man

* Fri Jun 01 2001 GOMEZ Henri (hgomez(a)slib.fr)
- Patch which checks that $RPM_BUILD_ROOT is not "/" before rm'ing it.

* Tue Mar 06 2001 Ben Reed <ben(a)opennms.org>
- changed spec to handle not building the frontend

* Thu Dec 30 1999 Fyodor (fyodor(a)insecure.org)
- Updated description
- Eliminated source1 (nmapfe.desktop) directive and simply packaged it with Nmap
- Fixed nmap distribution URL (source0)
- Added this .rpm to base Nmap distribution

* Mon Dec 13 1999 Tim Powers <timp(a)redhat.com>
- based on origional spec file from
	http://nmap.org/download.html
- general cleanups, removed lots of commenrts since it made the spec hard to
	read
- changed group to Applications/System
- quiet setup
- no need to create dirs in the install section, "make
	prefix=$RPM_BUILD_ROOT&{prefix} install" does this.
- using defined %{prefix}, %{version} etc. for easier/quicker maint.
- added docs
- gzip man pages
- strip after files have been installed into buildroot
- created separate package for the frontend so that Gtk+ isn't needed for the
	CLI nmap 
- not using -f in files section anymore, no need for it since there aren't that
	many files/dirs
- added desktop entry for gnome

* Sun Jan 10 1999 Fyodor (fyodor(a)insecure.org)
- Merged in spec file sent in by Ian Macdonald <ianmacd(a)xs4all.nl>

* Tue Dec 29 1998 Fyodor (fyodor(a)insecure.org)
- Made some changes, and merged in another .spec file sent in
  by Oren Tirosh <oren(a)hishome.net>

* Mon Dec 21 1998 Riku Meskanen (mesrik(a)cc.jyu.fi)
- initial build for RH 5.x
