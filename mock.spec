# TODO
# - add system user
# - pldize (drop usermode/consoleapps), check deps
# - kill configure bashism
Summary:	Builds packages inside chroots
Name:		mock
Version:	1.0.3
Release:	0.1
License:	GPL v2+
Group:		Development/Tools
Source0:	https://fedorahosted.org/mock/attachment/wiki/MockTarballs/%{name}-%{version}.tar.gz?format=raw
# Source0-md5:	6a7f44a5ad8358e0111f76f4ad1234d2
URL:		http://fedoraproject.org/wiki/Projects/Mock
BuildRequires:	perl-base
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	bash
Requires:	createrepo
Requires:	pigz
Requires:	python >= 1:2.4
Requires:	python-ctypes
Requires:	python-decoratortools
Requires:	python-hashlib
Requires:	tar
Requires:	usermode
Requires:	yum >= 2.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mock creates chroots and builds packages in them. Its only task is to
reliably populate a chroot and attempt to build a package in that
chroot.

%prep
%setup -q

%build
bash %configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT/var/lib/mock
install -d $RPM_BUILD_ROOT/var/cache/mock
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/mock

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -r mock

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/mock
%attr(755,root,root) %{_sbindir}/mock
%{_mandir}/man1/mock.1*

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) /etc/pam.d/%{name}
%config(noreplace) /etc/security/console.apps/%{name}
#/etc/bash_completion.d/*

%dir %{py_sitescriptdir}/%{name}
%dir %{py_sitescriptdir}/%{name}/plugins
%{py_sitescriptdir}/%{name}/plugins/*.py[co]
%{py_sitescriptdir}/%{name}/*.py[co]

# build dir
%attr(2775, root, mock) %dir /var/lib/mock

# cache dir
%attr(2775, root, mock) %dir /var/cache/mock
