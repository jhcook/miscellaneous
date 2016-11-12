Name:       rhlfdigester
Version:    0.01b
Release:    1%{?dist}
Summary:    Consumes log files from individual hosts via SSH
Group:      Applications/Archiving
License:    GPL3
URL:        https://github.com/jhcook/rhlfdigester/tree/master
Source0:    %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   python
Requires:       fabric

%description
This utility fetches log files from hosts specified in 
/etc/rhlfdigester/main.cfg to a local directory for futher consumption
by other processes.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/rhlfdigester/
mkdir -p %{buildroot}%{_bindir}/
%{__install} -m0755 rhlfdigester %{buildroot}%{_bindir}/
%{__install} -m0644 main.cfg %{buildroot}%{_sysconfdir}/rhlfdigester/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %attr(644,root,root) /etc/rhlfdigester/main.cfg
%doc

%changelog
* Mon Sep 23 2013 Justin Cook <jhcook@gmail.com> - 0.01b
- Created this package
