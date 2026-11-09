%bcond check 1

%global app_id  org.skaven.ratic

Name:           ratic
Version:        0.5.0
Release:        1%{?dist}
Summary:        Music player for GNOME

# ratic:           GPL-3.0-or-later
# metadata:        CC-BY-SA-4.0
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-3.0-or-later AND CC-BY-SA-4.0
License:        %{shrink:
    GPL-3.0-or-later AND CC-BY-SA-4.0 AND
    (0BSD OR MIT OR Apache-2.0) AND
    Apache-2.0 AND
    (Apache-2.0 OR GPL-2.0-only) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    BSD-2-Clause AND
    (BSD-2-Clause OR Apache-2.0 OR MIT) AND
    BSD-3-Clause AND
    (BSD-3-Clause OR Apache-2.0) AND
    CC0-1.0 AND
    (CC0-1.0 OR Apache-2.0) AND
    MIT AND
    (MIT OR Apache-2.0) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    (MIT OR Apache-2.0 OR Zlib) AND
    (MIT OR Zlib OR Apache-2.0) AND
    MPL-2.0 AND
    NCSA AND
    Unicode-3.0 AND
    (Unlicense OR MIT) AND
    (Zlib OR Apache-2.0 OR MIT)
}
URL:            https://gitlab.gnome.org/ratcornu/ratic
# The v%%{version} tag and the crates pinned by upstream's Cargo.lock;
# sources.sh creates both when the SRPM is built.
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
# glib-compile-resources and glib-compile-schemas, for build.rs
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.26
BuildRequires:  pkgconfig(gstreamer-audio-1.0) >= 1.26
BuildRequires:  pkgconfig(gstreamer-play-1.0) >= 1.26
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       hicolor-icon-theme
# Decoders for common audio formats
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free

%description
Ratic is a GTK 4 and Adwaita music player for local music libraries,
playing through GStreamer. It sorts and groups the library by album and
artist, with full-text search, keeps a play queue with several play modes,
reads M3U playlists and supports MPRIS controls.

%prep
%autosetup -a1
%cargo_prep -v vendor

%build
%cargo_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
# As upstream's Flatpak manifest, except that the settings schema is
# installed for the system to compile.
install -Dpm0755 target/rpm/ratic %{buildroot}%{_bindir}/ratic
install -Dpm0644 -t %{buildroot}%{_datadir}/glib-2.0/schemas data/%{app_id}.gschema.xml
install -Dpm0644 data/icons/scalable/apps/logo.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
install -Dpm0644 data/icons/scalable/apps/logo_black.svg \
    %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}_black.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps data/icons/symbolic/apps/*.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/applications data/%{app_id}.desktop
install -Dpm0644 -t %{buildroot}%{_metainfodir} data/%{app_id}.metainfo.xml

%if %{with check}
%check
%cargo_test
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
%endif

%files
%license LICENCE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/ratic
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}_black.svg
%{_datadir}/icons/hicolor/symbolic/apps/append-random-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/insert-next-random-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/insert-next-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/replace-random-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/replace-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Mon Nov 09 2026 Trung Lê <trung.le@ruby-journal.com> - 0.5.0-1
- Initial package
