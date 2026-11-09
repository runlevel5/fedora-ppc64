%bcond check 1

%global app_id  net.donnybeelo.Convey

Name:           convey
Version:        51.0
Release:        1%{?dist}
Summary:        Email client for GNOME built around conversations

# Based on Fedora's geary spec; Convey is a hard fork of Geary.
# convey:          LGPL-2.1-or-later
# sqlite3-unicodesn: LicenseRef-Fedora-Public-Domain
# icons:           CC-BY-3.0, CC-BY-SA-3.0 or public domain (COPYING.icons)
# sound:           CC-BY-SA-3.0 (COPYING.sounds)
# metadata:        CC0-1.0
License:        LGPL-2.1-or-later AND CC-BY-3.0 AND CC-BY-SA-3.0 AND CC0-1.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://gitlab.gnome.org/donnybeelo/convey
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 1.7
BuildRequires:  vala >= 0.56
# primary deps
BuildRequires:  pkgconfig(glib-2.0) >= 2.80
BuildRequires:  pkgconfig(gmime-3.0) >= 3.2.4
BuildRequires:  pkgconfig(gtk4) >= 4.16.0
BuildRequires:  pkgconfig(sqlite3) >= 3.24
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.40
# secondary deps
BuildRequires:  libstemmer-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(enchant-2) >= 2.1
BuildRequires:  pkgconfig(folks) >= 0.11
BuildRequires:  pkgconfig(gck-2)
BuildRequires:  pkgconfig(gcr-4)
BuildRequires:  pkgconfig(gee-0.8) >= 0.8.5
BuildRequires:  pkgconfig(gio-2.0) >= 2.80
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-play-1.0)
BuildRequires:  pkgconfig(gthread-2.0) >= 2.80
BuildRequires:  pkgconfig(icu-uc) >= 60
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(javascriptcoregtk-6.0) >= 2.40
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.0
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7
BuildRequires:  pkgconfig(libpeas-2)
BuildRequires:  pkgconfig(libsecret-1) >= 0.11
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libunwind) >= 1.1
BuildRequires:  pkgconfig(libunwind-generic) >= 1.1
BuildRequires:  pkgconfig(libxml-2.0) >= 2.7.8
BuildRequires:  pkgconfig(libytnef) >= 1.9.3
BuildRequires:  pkgconfig(webkitgtk-web-process-extension-6.0) >= 2.40

BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  python3

Requires:       hicolor-icon-theme
Recommends:     gnome-keyring

%description
Convey is an email application built around conversations, for the GNOME
desktop. It allows you to read, find and send email with a straightforward,
modern interface. It is a hard fork of Geary, ported to GTK 4 and Adwaita.

%prep
%autosetup -p1

%conf
%meson -Dprofile=release -Drevno=%{version} -Dvaladoc=disabled

%build
%meson_build

%install
%meson_install
%find_lang %{name} --with-gnome

%if %{with check}
%check
# Not client-tests and js-tests: they start WebKit web processes, and
# WebKit's bubblewrap sandbox cannot start in the build root.
%meson_test vala-unit:tests desktop-file-validate %{app_id}.metainfo.xml-validate engine-tests
%endif

%files -f %{name}.lang
%license COPYING COPYING.icons COPYING.sounds
%doc AUTHORS NEWS README.md THANKS
%{_bindir}/convey
%{_libdir}/convey/
%{_datadir}/convey/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/applications/convey-autostart.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{app_id}*
%{_datadir}/icons/hicolor/scalable/actions/*
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Mon Nov 09 2026 Trung Lê <trung.le@ruby-journal.com> - 51.0-1
- Initial package
