%bcond check 1

%global app_id  io.github.pixdevsapps.Sealwax

Name:           sealwax
Version:        1.3.0
Release:        1%{?dist}
Summary:        Fast, minimal, keyboard-first email client

# sealwax:         MIT
# vendored crates: see the license summary printed in %%build
# Sign in with Microsoft needs a client ID: build one in with
# --define "microsoft_client_id <id>" (upstream gives theirs to packagers on
# request), or users put their own registration's in config.toml.
# Each test binary is linked with thin LTO: at 32 jobs, %%check runs out of
# memory on a 64 GB machine
%constrain_build -m 4096
SourceLicense:  MIT
License:        %{shrink:
    MIT AND
    (Apache-2.0 OR MIT) AND BSD-3-Clause AND
    (MIT OR Apache-2.0) AND Apache-2.0 AND
    (MIT OR Apache-2.0) AND Unicode-3.0 AND
    Apache-2.0 AND
    Apache-2.0 AND ISC AND
    (Apache-2.0 OR GPL-2.0-only) AND
    (Apache-2.0 OR ISC OR MIT) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    BSD-3-Clause AND
    CDLA-Permissive-2.0 AND
    ISC AND
    (MIT OR Apache-2.0) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    MPL-2.0 AND
    Unicode-3.0 AND
    (Unlicense OR MIT) AND
    Zlib AND
    (Zlib OR Apache-2.0 OR MIT)
}
URL:            https://github.com/PixDevsApps/sealwax
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# The crates pinned by upstream's Cargo.lock; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo >= 1.92
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  pkgconfig(gio-2.0) >= 2.80
BuildRequires:  pkgconfig(glib-2.0) >= 2.80
BuildRequires:  pkgconfig(gtk4) >= 4.18
BuildRequires:  pkgconfig(javascriptcoregtk-6.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.9
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(sqlite3) >= 3.43
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.52

Requires:       hicolor-icon-theme
# The store refuses an SQLite without FTS5 or contentless_delete
Requires:       sqlite-libs >= 3.43
# Passwords and sign-in tokens are kept only in a Secret Service
Recommends:     (gnome-keyring or kwallet6 or keepassxc)
# Spell checking in the composer
Recommends:     hunspell

%description
Sealwax is a fast, minimal email client written in Rust with GTK 4 and
libadwaita, made for Omarchy but usable on any desktop. It supports IMAP with
IDLE push and an offline copy of mail, POP3, Sign in with Microsoft for
Outlook.com and Microsoft 365, Sieve rules, local search and a keyboard-first
interface. No script in a message ever runs, and nothing remote loads until
it is allowed.

%prep
%autosetup -p1 -a1
%cargo_prep -v vendored-crates

%build
%{?microsoft_client_id:export SEALWAX_MICROSOFT_CLIENT_ID=%{microsoft_client_id}}
%cargo_build -- -p sealwax
# Licenses of the crates linked into the app only, not those of the workspace's
# test and development tools
cd app
%cargo_license_summary
%{cargo_license} > ../LICENSE.dependencies
cd ..
%cargo_vendor_manifest

%install
install -Dpm 0755 target/rpm/sealwax %{buildroot}%{_bindir}/sealwax
install -Dpm 0644 packaging/%{app_id}.desktop \
    %{buildroot}%{_datadir}/applications/%{app_id}.desktop
install -Dpm 0644 packaging/%{app_id}.metainfo.xml \
    %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
sed 's|^Exec=/usr/bin/|Exec=%{_bindir}/|' packaging/%{app_id}.service > %{app_id}.service
install -Dpm 0644 %{app_id}.service \
    %{buildroot}%{_datadir}/dbus-1/services/%{app_id}.service
for size in 16 24 32 48 64 128 256 512; do
    install -Dpm 0644 packaging/icons/hicolor/${size}x${size}/apps/%{app_id}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{app_id}.png
done
install -Dpm 0644 packaging/icons/hicolor/scalable/apps/%{app_id}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg

%if %{with check}
%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
# Only the crates without GTK, as upstream does: a clean build has no display
# for the app's self-tests.
%cargo_test -- -p sealwax-domain -p sealwax-infrastructure -p sealwax-engine
%endif

%files
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md CHANGELOG.md INSTALL.md docs/INTEGRATIONS.md docs/USER_GUIDE.md
%{_bindir}/sealwax
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/icons/hicolor/*/apps/%{app_id}.png
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Thu Nov 12 2026 Trung Lê <trung.le@ruby-journal.com> - 1.3.0-1
- Initial package
