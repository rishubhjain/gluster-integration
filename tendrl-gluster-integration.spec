Name: tendrl-gluster-integration
Version: 1.4.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Gluster Integration
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/gluster-integration

BuildRequires: systemd
BuildRequires: python2-devel
BuildRequires: pytest
BuildRequires: python-mock

Requires: tendrl-commons
Requires: systemd
Requires: gstatus

%description
Python module for Tendrl gluster bridge to manage gluster tasks.

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m  0755 --directory $RPM_BUILD_ROOT%{_var}/log/tendrl/gluster-integration
install -m  0755  --directory $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/gluster-integration
install -Dm 0644 tendrl-gluster-integration.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-gluster-integration.service
install -Dm 0644 etc/tendrl/gluster-integration/gluster-integration.conf.yaml.sample $RPM_BUILD_ROOT%{_datadir}/tendrl/gluster-integration/gluster-integration.conf.yaml
install -Dm 0644 etc/tendrl/gluster-integration/logging.yaml.timedrotation.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/gluster-integration/gluster-integration_logging.yaml
install -Dm 644 etc/tendrl/gluster-integration/*.sample $RPM_BUILD_ROOT%{_datadir}/tendrl/gluster-integration/

%post
%systemd_post tendrl-gluster-integration.service

%preun
%systemd_preun tendrl-gluster-integration.service

%postun
%systemd_postun_with_restart tendrl-gluster-integration.service

%check
py.test -v tendrl/gluster_integration/tests || :

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl/gluster-integration
%dir %{_sysconfdir}/tendrl/gluster-integration
%doc README.rst
%license LICENSE
%config %{_datadir}/tendrl/gluster-integration/gluster-integration.conf.yaml
%{_unitdir}/tendrl-gluster-integration.service
%config %{_sysconfdir}/tendrl/gluster-integration/gluster-integration_logging.yaml
%{_datadir}/tendrl/gluster-integration


%changelog
* Thu Jun 08 2017 Rohan Kanade <rkanade@redhat.com> - 1.4.1-1
- Release tendrl-gluster-integration v1.4.1

* Fri Jun 02 2017 Rohan Kanade <rkanade@redhat.com> - 1.4.0-1
- Release tendrl-gluster-integration v1.4.0

* Thu May 18 2017 Rohan Kanade <rkanade@redhat.com> - 1.3.0-1
- Release tendrl-gluster-integration v1.3.0

* Tue Apr 18 2017 Rohan Kanade <rkanade@redhat.com> - 1.2.3-1
- Release tendrl-gluster-integration v1.2.3

* Tue Apr 11 2017 Rohan Kanade <rkanade@redhat.com> - 1.2.2-1
- Release tendrl-gluster-integration v1.2.2

* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
