Name:           cache-api
Version:        1.0.0
Release:        1%{?dist}
Summary:        Cache Proxy API for cachegate

License:        MIT
BuildArch:      noarch
Requires:       python3, redis

%description
Flask proxy API that caches backend responses in Redis.

%prep
%setup -q -c -T

%install
mkdir -p %{buildroot}/opt/cache-api
mkdir -p %{buildroot}/etc/cache-api
mkdir -p %{buildroot}/etc/sysconfig
mkdir -p %{buildroot}/etc/systemd/system

install -m 0644 %{_sourcedir}/app.py %{buildroot}/opt/cache-api/app.py
install -m 0644 %{_sourcedir}/config.yaml %{buildroot}/etc/cache-api/config.yaml
install -m 0644 %{_sourcedir}/cache-api.env %{buildroot}/etc/sysconfig/cache-api
install -m 0644 %{_sourcedir}/cache-api.service %{buildroot}/etc/systemd/system/cache-api.service

%post
python3 -m venv /opt/cache-api/venv
/opt/cache-api/venv/bin/pip install --no-cache-dir flask redis requests pyyaml
systemctl daemon-reload
systemctl enable cache-api || true

%preun
if [ $1 -eq 0 ]; then
    systemctl stop cache-api || true
    systemctl disable cache-api || true
fi

%files
/opt/cache-api/app.py
/etc/cache-api/config.yaml
/etc/sysconfig/cache-api
/etc/systemd/system/cache-api.service

%changelog
* Wed Mar 11 2026 Alexandr alexander19schmid@gmail.com - 1.0.0-1
- Initial package