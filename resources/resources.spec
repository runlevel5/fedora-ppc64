%bcond check 1

%global gtk4_version 4.12.0
%global libadwaita_version 1.8.0

%global major_version %%(cut -d "." -f 1 <<<%{version})

Name:           resources
Version:        51.0
Release:        1%{?dist}
Summary:        Monitor your system resources and processes

# resources:       GPL-3.0-or-later
# vendored crates: see the license summary printed in %%build
SourceLicense:  GPL-3.0-or-later
License:        %{shrink:
    GPL-3.0-or-later AND
    Apache-2.0 AND
    Apache-2.0 WITH LLVM-exception AND
    BSD-3-Clause AND
    CC0-1.0 AND
    ISC AND
    MIT AND
    Unicode-3.0 AND
    (Apache-2.0 OR MIT) AND
    (Unlicense OR MIT)
}
URL:            https://apps.gnome.org/app/org.gnome.Resources/
# The release tarball (meson dist) has the crates pinned by Cargo.lock
# vendored into vendor/.
Source0:        https://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{version}.tar.xz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  gcc
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(libadwaita-1) >= %{libadwaita_version}

Requires:       dmidecode
Requires:       hicolor-icon-theme
Requires:       polkit

%description
Resources is a simple yet powerful monitor for your system resources and
processes, written in Rust and using GTK 4 and libadwaita for its GUI. It's
capable of displaying usage and details of your CPU, memory, GPUs, network
interfaces and block devices. It's also capable of listing and terminating
running graphical applications as well as processes.


%prep
%autosetup -p1
# Replace upstream's cargo vendor config with the one %%cargo_prep writes.
rm -r .cargo
%cargo_prep -v vendor


%build
# meson runs cargo from the build directory, inside the source tree, so cargo
# finds the .cargo/config.toml that %%cargo_prep wrote for the vendored crates.
%meson
%meson_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}


%install
%meson_install
%find_lang %{name} --with-gnome


%check
%if %{with check}
%meson_test
%endif

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/symbolic/apps/*-symbolic.svg
%{_datadir}/polkit-1/actions/org.gnome.Resources.policy
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/%{name}-*
%{_metainfodir}/*.metainfo.xml


%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 51.0-1
- Update to 51.0, now a GNOME Incubator app (app ID org.gnome.Resources)
- Build from the GNOME release tarball, which has the crates vendored

* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 1.10.2-2
- Build offline from vendored crates, with their licenses and a vendor manifest
- Fix the %%meson line swallowing %%meson_build
- Run the tests

* Sat Mar 08 2026 Local Build <tle@localhost> - 1.10.2-1
- Bump to 1.10.2

* Sat Mar 29 2025 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.0-1
- chore: Update to latest release

* Mon Dec 09 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.1-1
- chore: Update to latest release

* Sun Dec 01 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.0-1
- chore: Update to latest release

* Sun Jul 07 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.1-1
- chore: Update to latest release

* Sun Jun 23 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.0-1
- chore: Update to latest release

* Sun Apr 14 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.0-1
- chore: Update to latest release

* Mon Feb 26 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-2
- build: Switch to default profile

* Sun Dec 24 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-1
- chore: Update to latest release

* Tue Oct 31 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.0-1
- Update to latest version

* Mon Oct 16 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.0-1
- Initial
