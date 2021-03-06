Summary:	Mod_chroot makes running Apache in a secure chroot environment easy
Name:		mod_chroot
Version:	0.5
Release:	2%{?dist}
Group:		System Environment/Daemons
URL:		http://core.segfault.pl/~hobbit/mod_chroot/
Source:		http://core.segfault.pl/~hobbit/mod_chroot/dist/%{name}-%{version}.tar.gz
Source1:	mod_chroot.conf
License:	Apache Software License
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	httpd-devel >= 2.0.52
Requires:	httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing httpd-devel)
Requires:       httpd >= %(rpm -q httpd --qf "%%{version}-%%{release}\n")

%description
mod_chroot makes running Apache in a secure chroot environment easy. You don't
need to create a special directory hierarchy containing /dev, /lib, /etc...

%prep
%setup -q

%build
apxs -c %{name}.c
#configure 

#make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/httpd/modules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CAVEATS ChangeLog INSTALL LICENSE README README.Apache20
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/%{name}.so

%changelog
* Mon Sep 15 2008 David Hrbáč <david@hrbac.cz> - 0.5-2
- corrected requires

* Tue Sep  9 2008 David Hrbáč <david@hrbac.cz> - 0.5-1
- initial build
