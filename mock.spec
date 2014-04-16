# TODO
# - pldize (drop usermode/consoleapps), check deps
# - kill configure bashism
# - bash completion subpackage
Summary:	Builds packages inside chroots
Name:		mock
Version:	1.1.38
Release:	0.3
License:	GPL v2+
Group:		Development/Tools
Source0:	https://git.fedorahosted.org/cgit/mock.git/snapshot//%{name}-%{version}.tar.xz
# Source0-md5:	dc3d5c4ed6657d158a30d949f7baac88
URL:		https://fedoraproject.org/wiki/Projects/Mock
BuildRequires:	perl-base
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xz
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	bash
Requires:	createrepo
Requires:	pigz
Requires:	python >= 1:2.6
Requires:	python-decoratortools
Requires:	tar
Requires:	usermode
Requires:	yum >= 2.4
Requires:	yum-utils >= 1.1.9
Provides:	group(mock)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mock creates chroots and builds packages in them. Its only task is to
reliably populate a chroot and attempt to build a package in that
chroot.

%prep
%setup -q

# keep for reference to build pld files
install -d sample-configs
mv etc/mock/{fedora,epel}-*.cfg sample-configs

%build
mkdir build
%{__aclocal}
%{__automake}
%{__autoconf} --force
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
%groupadd -r -g 208 mock

%postun
if [ "$1" = "0" ]; then
	%groupremove mock
fi

%files
%defattr(644,root,root,755)
%doc sample-configs
%attr(755,root,root) %{_bindir}/mock
%attr(755,root,root) %{_bindir}/mockchain
%attr(755,root,root) %{_sbindir}/mock
%{_mandir}/man1/mock*.1*

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) /etc/pam.d/%{name}
%config(noreplace) /etc/security/console.apps/%{name}
/etc/bash_completion.d/mock

%dir %{py_sitescriptdir}/mockbuild
%{py_sitescriptdir}/mockbuild/*.py[co]
%dir %{py_sitescriptdir}/mockbuild/plugins
%{py_sitescriptdir}/mockbuild/plugins/*.py[co]

# build dir
%attr(2775, root, mock) %dir /var/lib/mock

# cache dir
%attr(2775, root, mock) %dir /var/cache/mock
