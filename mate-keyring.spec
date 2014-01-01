Summary:	Keep passwords and other user's secrets
Name:		mate-keyring
Version:	1.6.1
Release:	1
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	3691d4d42ce7db525e6374b1e6505677
URL:		http://wiki.mate-desktop.org/mate-keyring
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gtk+-devel
BuildRequires:	libmatekeyring-devel
BuildRequires:	libtool
Requires(post,preun):	glib-gio-gsettings
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The library libgnome-keyring is used by applications to integrate with
the GNOME keyring system.

%package libs
Summary:	GNOME keyring library
Group:		Libraries

%description libs
GNOME keyring library.

%package devel
Summary:	Headers for GNOME keyring library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for GNOME keyring library.

%package apidocs
Summary:	GNOME keyring API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME keyring API documentation.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile		\
	--disable-silent-rules			\
	--disable-static			\
	--with-html-dir=%{_gtkdocdir}		\
	--with-pam-dir=%{_libdir}/security	\
	--with-root-certs=/etc/certs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-pam	\
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*,*/*}.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mate-keyring/{devel,standalone}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%preun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-keyring
%attr(755,root,root) %{_bindir}/mate-keyring-daemon

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/devel
%dir %{_libdir}/%{name}/standalone
%attr(755,root,root) %{_libexecdir}/devel/*-standalone.so
%attr(755,root,root) %{_libexecdir}/mate-keyring-prompt
%attr(755,root,root) %{_libexecdir}/standalone/*-standalone.so
%attr(755,root,root) %{_libdir}/pkcs11/mate-keyring-pkcs11.so
%attr(755,root,root) %{_libdir}/security/pam_mate_keyring.so

%{_datadir}/dbus-1/services/org.mate.keyring.service
%{_datadir}/dbus-1/services/org.mate-freedesktop.secrets.service
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/mate-keyring
%{_datadir}/mategcr
%{_sysconfdir}/xdg/autostart/mate-keyring-gpg.desktop
%{_sysconfdir}/xdg/autostart/mate-keyring-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/mate-keyring-secrets.desktop
%{_sysconfdir}/xdg/autostart/mate-keyring-ssh.desktop

%{_mandir}/man1/mate-keyring-daemon.1*
%{_mandir}/man1/mate-keyring.1*

%files libs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%attr(755,root,root) %ghost %{_libdir}/libmategc*.so.?
%attr(755,root,root) %{_libdir}/libmategc*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmategc*.so
%{_includedir}/gck
%{_includedir}/mate-gck
%{_includedir}/mategcr
%{_pkgconfigdir}/mate*-0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gck
%{_gtkdocdir}/gcr-0

