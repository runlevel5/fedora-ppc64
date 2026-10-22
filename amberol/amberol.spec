%bcond check 1

Name:           amberol
Version:        2026.1
Release:        1%{?dist}
Summary:        Plays music, and nothing else

# amberol:         GPL-3.0-or-later
# icons:           CC-BY-SA-3.0
# metadata:        CC0-1.0
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-3.0-or-later AND CC-BY-SA-3.0 AND CC0-1.0
License:        %{shrink:
    GPL-3.0-or-later AND CC-BY-SA-3.0 AND CC0-1.0 AND
    Apache-2.0 AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    Apache-2.0 WITH LLVM-exception AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (BSD-2-Clause OR Apache-2.0 OR MIT) AND
    MIT AND
    (MIT OR Apache-2.0) AND
    (MIT OR Zlib OR Apache-2.0) AND
    MPL-2.0 AND
    Unicode-3.0 AND
    (Unlicense OR MIT) AND
    (0BSD OR MIT OR Apache-2.0)
}
URL:            https://gitlab.gnome.org/World/amberol
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  blueprint-compiler
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-audio-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-bad-audio-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-play-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0) >= 1.20
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.20
BuildRequires:  pkgconfig(gtk4) >= 4.19.5
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8

Requires:       hicolor-icon-theme
# Decoders for common audio formats
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free
# CD playback
Suggests:       gstreamer1-plugins-ugly-free

%description
Amberol is a music player with no delusions of grandeur. If you just want to
play music available on your local system then Amberol is the music player you
are looking for.

%prep
%autosetup -p1 -a1
%cargo_prep -v vendor

%build
# meson runs cargo from the build directory, inside the source tree, so cargo
# finds the .cargo/config.toml that %%cargo_prep wrote for the vendored crates.
%meson
%meson_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
%meson_install
%find_lang %{name}

%if %{with check}
%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.bassi.Amberol.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/io.bassi.Amberol.metainfo.xml
%endif

%files -f %{name}.lang
%license LICENSES/*.txt LICENSE.dependencies cargo-vendor.txt
%doc README.md CHANGES.md
%{_bindir}/amberol
%{_datadir}/amberol/
%{_datadir}/applications/io.bassi.Amberol.desktop
%{_datadir}/dbus-1/services/io.bassi.Amberol.service
%{_datadir}/glib-2.0/schemas/io.bassi.Amberol.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/io.bassi.Amberol.svg
%{_datadir}/icons/hicolor/symbolic/apps/io.bassi.Amberol-symbolic.svg
%{_metainfodir}/io.bassi.Amberol.metainfo.xml

%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 2026.1-1
- Build offline from vendored crates, with their licenses and a vendor manifest
- Build with Fedora's default flags and debuginfo
- Validate the desktop file and AppStream metadata

* Sun Apr 12 2026 Trung Lê <8@tle.id.au> - 2026.1-0
- New release

* Sun Apr 13 2025 Trung Lê <8@tle.id.au> - 2025.1-0
- New release

* Fri Feb 28 2025 Trung Lê <8@tle.id.au> - 2024.2-0
- New release

* Tue Jun 18 2024 Trung Lê <8@tle.id.au> - 0.10.3-2
- Initial build
