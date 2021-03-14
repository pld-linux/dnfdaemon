Summary:	DBus daemon for dnf package actions
Name:		dnfdaemon
Version:	0.3.20
Release:	1
License:	GPL v2+
Source0:	https://github.com/manatools/dnfdaemon/releases/download/dnfdaemon-%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	45f02532eb3d114793aa5076ce6e5e11
URL:		https://github.com/manatools/dnfdaemon
BuildRequires:	python3-modules
BuildRequires:	systemd-devel
Requires:	dnf >= 4.3.6
Requires:	polkit
Requires:	python3-dbus
Requires:	python3-gobject
Requires(post,preun,postun):	systemd-units >= 38
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dbus daemon for performing package actions with the dnf package
manager

%package -n python3-%{name}
Summary:	Python 3 api for communicating with the dnf-daemon DBus service
Requires:	%{name} = %{version}-%{release}

%description -n python3-%{name}
Python API for communicating with the dnf-daemon DBus service.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	DATADIR=%{_datadir} \
	SYSCONFDIR=%{_datadir} \
	SYSTEMDSYSTEMUNITDIR=%{systemdunitdir} \
	PYLIBDIR3=$(echo %{py3_sitescriptdir} | sed 's/\/site-packages//')

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}/dnfdaemon
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}/dnfdaemon

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(644,root,root,755)
%doc README.md ChangeLog
%{_datadir}/dbus-1/system-services/org.baseurl.Dnf*
%{_datadir}/dbus-1/services/org.baseurl.Dnf*
%{_datadir}/polkit-1/actions/org.baseurl.Dnf*
%{_datadir}/dbus-1/system.d/org.baseurl.Dnf*
%{_datadir}/%{name}
%dir %{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}/*.py
%{py3_sitescriptdir}/%{name}/__pycache__
%{py3_sitescriptdir}/%{name}/server
%{systemdunitdir}/%{name}.service

%files -n  python3-%{name}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{name}/client
