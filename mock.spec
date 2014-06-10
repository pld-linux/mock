# TODO
# - pldize (drop usermode/consoleapps), check deps
# - kill configure bashism
Summary:	Builds packages inside chroots
Name:		mock
Version:	1.1.38
Release:	0.5
License:	GPL v2+
Group:		Development/Tools
Source0:	https://git.fedorahosted.org/cgit/mock.git/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	dc3d5c4ed6657d158a30d949f7baac88
URL:		https://fedoraproject.org/wiki/Projects/Mock
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	perl-base
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
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
Requires:	yum-utils >= 1.1.31
Suggests:	bash-completion-%{name}
Provides:	group(mock)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mock creates chroots and builds packages in them. Its only task is to
reliably populate a chroot and attempt to build a package in that
chroot.

%package scm
Summary:	Mock SCM integration module
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	cvs
Requires:	git-core
Requires:	subversion
Requires:	tar

%description scm
Mock SCM integration module.

%package -n bash-completion-%{name}
Summary:	bash-completion for Mock
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion >= 2.0

%description -n bash-completion-%{name}
bash-completion for Mock.

%prep
%setup -q

# keep for reference to build pld files
install -d sample-configs
mv etc/mock/{fedora,epel}-*.cfg sample-configs

%build
install -d build
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

install -d $RPM_BUILD_ROOT/var/{lib,cache}/%{name}
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
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/security/console.apps/%{name}
%attr(755,root,root) %{_bindir}/mock
%attr(755,root,root) %{_bindir}/mockchain
%attr(755,root,root) %{_sbindir}/mock
%{_mandir}/man1/mock*.1*

%dir %{py_sitescriptdir}/mockbuild
%{py_sitescriptdir}/mockbuild/*.py*
%dir %{py_sitescriptdir}/mockbuild/plugins
%{py_sitescriptdir}/mockbuild/plugins/*.py*

# build dir
%attr(2775, root, mock) %dir /var/lib/mock

# cache dir
%attr(2775, root, mock) %dir /var/cache/mock

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/mock
%{bash_compdir}/mockchain
