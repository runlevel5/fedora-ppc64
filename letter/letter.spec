%global app_id  io.github.stalvatero.Letter

Name:           letter
Version:        1.7.0
Release:        1%{?dist}
Summary:        Email client for GNOME

License:        GPL-3.0-or-later
URL:            https://github.com/stalvatero/letter
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 1.3
BuildRequires:  vala >= 0.56.11
BuildRequires:  blueprint-compiler
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  pkgconfig(camel-1.2) >= 3.50
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.42
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.80
BuildRequires:  pkgconfig(glib-2.0) >= 2.80
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gnutls) >= 3.6
BuildRequires:  pkgconfig(goa-1.0) >= 3.50
BuildRequires:  pkgconfig(gsound) >= 1.0
BuildRequires:  pkgconfig(gtk4) >= 4.16
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.6
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(libebook-1.2) >= 3.50
BuildRequires:  pkgconfig(libecal-2.0) >= 3.50
BuildRequires:  pkgconfig(libedataserver-1.2) >= 3.50
BuildRequires:  pkgconfig(libedataserverui4-1.0) >= 3.50
BuildRequires:  pkgconfig(libical-glib)
BuildRequires:  pkgconfig(libsoup-3.0) >= 3.0
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.44

# Accounts come only from GNOME Online Accounts, and mail from the Evolution
# Data Server registry.
Requires:       evolution-data-server
Requires:       gnome-online-accounts
Requires:       hicolor-icon-theme
# Spell checking while composing, and attachment previews
Recommends:     hunspell
Recommends:     sushi
# Needed for Microsoft 365 and Exchange accounts, but pulls in Evolution
Suggests:       evolution-ews

%description
Letter is a GTK 4 and libadwaita email client for the GNOME desktop. It
uses the accounts set up in GNOME Online Accounts (Google, Microsoft 365,
Exchange, IMAP/SMTP) and reads and sends mail through Evolution Data Server,
like GNOME Calendar and Contacts.

%prep
%autosetup

%conf
%meson -Dprofile=default

%build
%meson_build

%install
%meson_install
%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%license COPYING
%doc README.md CHANGELOG.md
%{_bindir}/letter
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/glib-2.0/schemas/io.github.stalvatero.Mail.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu Oct 22 2026 Trung Lê <trung.le@ruby-journal.com> - 1.7.0-1
- Initial package
