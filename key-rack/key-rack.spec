%bcond check 1

%global app_id          app.drey.KeyRack
# Upstream did not tag 0.6.0; this is its "Release 0.6.0" commit.
%global commit          274afb41a192297176f80cc7e6234a51076b65e5

Name:           key-rack
Version:        0.6.0
Release:        1%{?dist}
Summary:        View and edit passwords and other secrets stored by apps

# key-rack:        GPL-3.0-or-later
# metadata:        CC-BY-SA-4.0
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-3.0-or-later AND CC-BY-SA-4.0
License:        %{shrink:
    GPL-3.0-or-later AND CC-BY-SA-4.0 AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    BSD-3-Clause AND
    MIT AND
    (MIT OR Apache-2.0) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    Unicode-3.0 AND
    (Unlicense OR MIT)
}
URL:            https://gitlab.gnome.org/World/key-rack
Source0:        %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 1.0
BuildRequires:  pkgconfig(gtk4) >= 4.20
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8

Requires:       hicolor-icon-theme

%description
Key Rack views and edits keys, like passwords or tokens, stored by apps. It
supports the secrets of Flatpak apps as well as the system-wide secrets of the
Secret Service (GNOME Keyring, KeePassXC and others).

%prep
%autosetup -n %{name}-%{commit} -a1
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
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
%endif

%files -f %{name}.lang
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/key-rack
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Mon Nov 09 2026 Trung Lê <trung.le@ruby-journal.com> - 0.6.0-1
- Initial package
