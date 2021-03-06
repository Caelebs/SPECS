%{!?tcp_wrappers:%define tcp_wrappers 1}
%define _generatorsdir %{_prefix}/lib/systemd/system-generators

Name: vsftpd
Version: 3.0.3
Release: 33%{?dist}
Summary: Very Secure FTP Daemon

Group: System Environment/Daemons
# OpenSSL link exception
License: GPLv2 with exceptions
URL: https://security.appspot.com/vsftpd.html
Packager: 24h 
Source0: https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
Source1: vsftpd.xinetd
Source2: vsftpd.pam
Source3: vsftpd.ftpusers
Source4: vsftpd.user_list
Source5: vsftpd.init
Source6: vsftpd_conf_migrate.sh
Source7: vsftpd.service
Source8: vsftpd@.service
Source9: vsftpd.target
Source10: vsftpd-generator

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pam-devel
BuildRequires: libcap-devel
BuildRequires: openssl-devel
BuildRequires: systemd
%if %{tcp_wrappers}
BuildRequires: tcp_wrappers-devel
%endif

Requires: logrotate

# Build patches
# Patch1: vsftpd-2.1.0-libs.patch
# Patch2: vsftpd-2.1.0-build_ssl.patch
# Patch3: vsftpd-2.1.0-tcp_wrappers.patch

# Use /etc/vsftpd/ instead of /etc/
# Patch4: vsftpd-2.1.0-configuration.patch

# These need review
# Patch5: vsftpd-2.1.0-pam_hostname.patch
# Patch6: vsftpd-close-std-fds.patch
# Patch7: vsftpd-2.1.0-filter.patch
# Patch9: vsftpd-2.1.0-userlist_log.patch

# Patch10: vsftpd-2.1.0-trim.patch
# Patch12: vsftpd-2.1.1-daemonize_plus.patch
# Patch14: vsftpd-2.2.0-wildchar.patch

# Patch16: vsftpd-2.2.2-clone.patch
# Patch19: vsftpd-2.3.4-sd.patch
# Patch20: vsftpd-2.3.4-sqb.patch
# Patch21: vsftpd-2.3.4-listen_ipv6.patch
# Patch22: vsftpd-2.3.5-aslim.patch
# Patch23: vsftpd-3.0.0-tz.patch
# Patch24: vsftpd-3.0.0-xferlog.patch
# Patch25: vsftpd-3.0.0-logrotate.patch
# Patch26: vsftpd-3.0.2-seccomp.patch
# Patch27: vsftpd-3.0.2-mrate.patch
# Patch28: vsftpd-3.0.2-wnohang.patch
# Patch29: vsftpd-3.0.2-dh.patch
# Patch30: vsftpd-3.0.2-ecdh.patch
# Patch31: vsftpd-2.0.5-fix_qm.patch
# Patch32: vsftpd-3.0.2-reverse-lookup.patch
# Patch33: vsftpd-3.0.2-del-upl.patch
# Patch34: vsftpd-2.2.2-nfs-fail.patch
# Patch35: vsftpd-2.2.2-man-pages.patch
# Patch36: vsftpd-3.0.2-uint-uidgid.patch
# Patch37: vsftpd-2.2.2-blank-chars-overflow.patch
# Patch38: vsftpd-2.2.2-syslog.patch
# Patch39: vsftpd-3.0.2-docupd.patch
# Patch40: vsftpd-2.2.2-tlsv1_2.patch
# Patch41: vsftpd-3.0.2-defaulttls.patch

%description
VSFTPD is a Very Secure FTP daemon. It was written completely from
scratch.

%package sysvinit
Group: System Environment/Daemons
Summary: SysV initscript for vsftpd daemon
Requires: %{name} = %{version}-%{release}
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description sysvinit
The vsftpd-sysvinit contains SysV initscritps support.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

# %patch1 -p1 -b .libs
# %patch2 -p1 -b .build_ssl
# %if %{tcp_wrappers}
# %patch3 -p1 -b .tcp_wrappers
# %endif
# %patch4 -p1 -b .configuration
# %patch5 -p1 -b .pam_hostname
# %patch6 -p1 -b .close_fds
# %patch7 -p1 -b .filter
# %patch9 -p1 -b .userlist_log
# %patch10 -p1 -b .trim
# %patch12 -p1 -b .daemonize_plus
# %patch14 -p1 -b .wildchar
# %patch16 -p1 -b .clone
# %patch19 -p1 -b .sd
# %patch20 -p1 -b .sqb
# %patch21 -p1 -b .listen_ipv6
# %patch22 -p1 -b .aslim
# %patch23 -p1 -b .tz
# %patch24 -p1 -b .xferlog
# %patch25 -p1 -b .logrotate
# %patch26 -p1 -b .seccomp
# %patch27 -p1 -b .mrate
# %patch28 -p1 -b .wnohang
# %patch29 -p1 -b .dh
# %patch30 -p1 -b .ecdh
# %patch31 -p1 -b .fix_qm
# %patch32 -p1 -b .reverse-lookup
# %patch33 -p1 -b .del-upl
# %patch34 -p1 -b .nfs-fail
# %patch35 -p1 -b .man_pages
# %patch36 -p1 -b .uint-uidgid
# %patch37 -p1 -b .blank-char-overflow
# %patch38 -p1 -b .syslog
# %patch39 -p1 -b .docup
# %patch40 -p1 -b .tls_version
# %patch41 -p1 -b .defaulttls

%build
%ifarch s390x sparcv9 sparc64
make CFLAGS="$RPM_OPT_FLAGS -fPIE -pipe -Wextra -Werror" \
%else
make CFLAGS="$RPM_OPT_FLAGS -fpie -pipe -Wextra -Werror" \
%endif
        LINK="-pie -lssl" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{vsftpd,pam.d,logrotate.d,rc.d/init.d}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_generatorsdir}
install -m 755 vsftpd  $RPM_BUILD_ROOT%{_sbindir}/vsftpd
install -m 600 vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd.conf
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 RedHat/vsftpd.log $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/vsftpd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vsftpd
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/ftpusers
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/user_list
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/vsftpd
install -m 744 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_generatorsdir}
                  
mkdir -p $RPM_BUILD_ROOT/%{_var}/ftp/pub

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post vsftpd.service

%preun
%systemd_preun vsftpd.service
%systemd_preun vsftpd.target

%postun
%systemd_postun_with_restart vsftpd.service 

%files
%defattr(-,root,root,-)
%{_unitdir}/*
%{_generatorsdir}/*
%{_sbindir}/vsftpd
%dir %{_sysconfdir}/vsftpd
%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
%config(noreplace) %{_sysconfdir}/vsftpd/ftpusers
%config(noreplace) %{_sysconfdir}/vsftpd/user_list
%config(noreplace) %{_sysconfdir}/vsftpd/vsftpd.conf
%config(noreplace) %{_sysconfdir}/pam.d/vsftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/vsftpd
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD
%doc SPEED TODO BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE vsftpd.xinetd
%{_mandir}/man5/vsftpd.conf.*
%{_mandir}/man8/vsftpd.*
%{_var}/ftp

%files sysvinit
%{_sysconfdir}/rc.d/init.d/vsftpd

%changelog
* Thu Mar 23 2017 Zdenek Dohnal <zdohnal@redhat.com> - 3.0.2-22
- Resolves: #1432054 - secure ftp stopped working with default TLS settings in the new vsftpd package
