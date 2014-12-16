Name: dns-flood-detector
Version: 1.20
Release: 1%{?dist}
Summary: detect abusive usage levels on high traffic nameservers

Group: System Environment/Daemons
License: GPLv2
URL: http://www.adotout.com/
Source0: http://www.adotout.com/dnsflood-%{version}.tgz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: libpcap-devel
Requires: rsyslog, libpcap
Requires(post): chkconfig


%description
This package provides the dns-flood-detector daemon.
It was developed to detect abusive usage levels on high traffic nameservers
and to enable quick response in halting the use of one's nameserver to
facilitate spam.
It uses libpcap (in non-promiscuous mode) to monitor incoming dns queries to a
nameserver. The tool may be run in one of two modes, either daemon mode or
"bindsnap" mode. In daemon mode, the tool will alarm via syslog. In bindsnap
mode, the user is able to get near-real-time stats on usage to aid in more
detailed troubleshooting.

%prep
%setup -q

%build
./configure.pl Linux

make %{?_smp_mflags}
gzip redhat/dns-flood-detector.8

%install
install -D -m 0755 dns_flood_detector $RPM_BUILD_ROOT%{_bindir}/dns-flood-detector
install -D -m 0644 redhat/dns-flood-detector.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/dns-flood-detector
install -D -m 0755 redhat/dns-flood-detector.init $RPM_BUILD_ROOT%{_initrddir}/dns-flood-detector
install -D -m 0755 redhat/dns-flood-detector.rsyslog $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.d/dns-flood-detector.conf
install -D -m 0644 redhat/dns-flood-detector.8.gz $RPM_BUILD_ROOT%{_mandir}/man8/dns-flood-detector.8.gz

%post
/sbin/chkconfig --add dns-flood-detector

%preun
if [ $1 = 0 ]; then
    /sbin/service dns-flood-detector stop > /dev/null 2>&1
    /sbin/chkconfig --del dns-flood-detector
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_bindir}/dns-flood-detector
%{_sysconfdir}/sysconfig/dns-flood-detector
%{_initrddir}/dns-flood-detector
%{_sysconfdir}/rsyslog.d/dns-flood-detector.conf
%{_mandir}/man8/dns-flood-detector.8*

%changelog
* Tue Dec 16 2014 xingxing <itxx00@gmail.com> - 1.20-1
- rebuilt for CentOS

