Name: tendrl-gluster-integration
Version: 0.0.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Gluster Integration
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/gluster_integration

BuildRequires: systemd
BuildRequires: python2-devel
BuildRequires: pytest
BuildRequires: python-mock
BuildRequires: python-dateutil
BuildRequires: python-gevent
BuildRequires: python-greenlet

Requires: python-etcd
Requires: python-dateutil
Requires: python-gevent
Requires: python-greenlet
Requires: pytz
Requires: tendrl-common
Requires: systemd

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
install -m  0755 --directory $RPM_BUILD_ROOT%{_var}/log/tendrl/gluster_integration
install -m  0755  --directory $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/gluster_integration
install -Dm 0644 tendrl-glusterd.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-glusterd.service
install -Dm 0755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT%{_datadir}/tendrl/gluster_integration/tendrl.conf.sample
install -Dm 0644 etc/logging.yaml.timedrotation.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/gluster_integration_logging.yaml

%post
%systemd_post tendrl-glusterd.service

%preun
%systemd_preun tendrl-glusterd.service

%postun
%systemd_postun_with_restart tendrl-glusterd.service

%check
py.test -v tendrl/gluster_integration/tests || :

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl/gluster_integration
%dir %{_sysconfdir}/tendrl/gluster_integration
%doc README.rst
%license LICENSE
%{_datarootdir}/tendrl/gluster_integration/tendrl.conf.sample
%{_unitdir}/tendrl-glusterd.service
%{_sysconfdir}/tendrl/gluster_integration_logging.yaml


%changelog
* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.