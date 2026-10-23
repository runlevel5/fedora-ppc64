%bcond check 1

%global app_id          garden.tau.Ripples
%global commit          7450d7c21ce84e6323fa4a0db21df3b8b663bdb2
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global commitdate      20261017

Name:           ripples
Version:        0.1.0^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        CD player and ripper for GNOME

# ripples:         GPL-3.0-or-later WITH GStreamer-exception-2008
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-3.0-or-later WITH GStreamer-exception-2008
License:        %{shrink:
    GPL-3.0-or-later WITH GStreamer-exception-2008 AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    Apache-2.0 WITH LLVM-exception AND
    GPL-3.0-or-later AND
    LGPL-3.0-or-later AND
    MIT AND
    (MIT OR Apache-2.0) AND
    (Unlicense OR MIT)
}
URL:            https://codeberg.org/ripples/ripples
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{shortcommit}-vendor.tar.xz
# Rank id3v2mux before checking which encoding profiles are available, or
# MP3 needs id3mux from gst-plugins-bad
Patch0:         ripples-id3-rank.patch

BuildRequires:  blueprint-compiler
BuildRequires:  cargo >= 1.95.0
BuildRequires:  cargo-rpm-macros >= 26
# bindgen, for the discid-sys and libcdio-sys crates
BuildRequires:  clang-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  /usr/bin/glib-compile-schemas
BuildRequires:  meson >= 1.5.0
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glycin-gtk4-2)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0) >= 1.26
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gtk4) >= 4.21.6
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libdiscid) >= 0.6
BuildRequires:  pkgconfig(libsoup-3.0)
%if %{with check}
# The tests check cdparanoiasrc and the encoding profiles
BuildRequires:  gstreamer1-plugins-base
BuildRequires:  gstreamer1-plugins-good
%endif

Requires:       hicolor-icon-theme
# cdparanoiasrc, Opus and Ogg encoding
Requires:       gstreamer1-plugins-base
# FLAC, MP3 (LAME) and ID3 tagging
Requires:       gstreamer1-plugins-good

%description
Ripples plays audio CDs and extracts (rips) their tracks to FLAC, Opus or
MP3 files, with album metadata and cover art from MusicBrainz.

%prep
%autosetup -n %{name} -p1 -a1
%cargo_prep -v vendor

%conf
%meson

%build
# meson runs cargo from the build directory, inside the source tree, so cargo
# finds the .cargo/config.toml that %%cargo_prep wrote for the vendored crates.
%meson_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
%meson_install

%if %{with check}
%check
%meson_test
%endif

%files
%license LICENSES/*.txt LICENSE.dependencies cargo-vendor.txt
%doc readme.md
%{_bindir}/ripples
%{_datadir}/%{name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Fri Oct 23 2026 Trung Lê <trung.le@ruby-journal.com> - 0.1.0^20261017git7450d7c-1
- Initial package
