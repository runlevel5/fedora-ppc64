%global app_id          io.github.riyaniii.Kaori
# The Suwayomi server release that Kaori 0.9.8 ships as src/Suwayomi-Server-*.jar
%global suwayomi_version 2.4.2422

Name:           kaori
Version:        0.9.8
Release:        1%{?dist}
Summary:        Manga and comic reader using a Suwayomi server

# Kaori:                  GPL-3.0-or-later
# Suwayomi-Server.jar:    MPL-2.0, plus the Java libraries it bundles
#                         (mostly Apache-2.0)
License:        GPL-3.0-or-later AND MPL-2.0 AND Apache-2.0
URL:            https://github.com/riyaniii/Kaori
Source0:        %{url}/archive/%{version}/Kaori-%{version}.tar.gz
# The tarball holds only a Git LFS pointer in place of the server jar, so
# fetch the prebuilt jar the pointer refers to. It is not built from source:
# Suwayomi is a Gradle/Kotlin project with dependencies Fedora lacks.
Source1:        https://github.com/Suwayomi/Suwayomi-Server-preview/releases/download/v%{suwayomi_version}/Suwayomi-Server-v%{suwayomi_version}.jar
# Suwayomi refuses to start on architectures it does not list (it throws
# "Unsupported architecture: ppc64le"): add a ppc64 alias to its ARCH class.
Source2:        suwayomi-arch-alias.py

BuildArch:      noarch

BuildRequires:  meson >= 1.0.0
BuildRequires:  blueprint-compiler >= 0.18.0
BuildRequires:  python3-devel
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/appstreamcli
BuildRequires:  /usr/bin/glib-compile-resources
BuildRequires:  /usr/bin/glib-compile-schemas
# blueprint-compiler reads the Gtk and Adw GIR files
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)

Requires:       gtk4
Requires:       hicolor-icon-theme
Requires:       java-headless >= 1:21
Requires:       libadwaita
Requires:       python3-babel
Requires:       python3-diskcache
Requires:       python3-gobject
Requires:       python3-gql
Requires:       python3-httpx
# gql.transport.aiohttp
Requires:       python3-aiohttp

Provides:       bundled(suwayomi-server) = %{suwayomi_version}

%description
Kaori lets you discover, download and read comics with a libadwaita
interface and natural touchpad gestures. It browses and searches comics
from dozens of sources, downloads chapters for offline reading, and reads
them in single-page, double-page or webtoon (continuous scroll) mode.

It uses a Suwayomi server as its backend, either a remote one or the bundled
one, which it runs locally with Java.

%prep
%autosetup -n Kaori-%{version}
jar=$PWD/src/Suwayomi-Server-v%{suwayomi_version}.jar
cp -p %{SOURCE1} $jar
arch_class='suwayomi/tachidesk/server/util/ARCH$RISCV.class'
mkdir suwayomi-patch
pushd suwayomi-patch
unzip -q $jar "$arch_class"
%{python3} %{SOURCE2} "$arch_class" riscv32 ppc64
zip -q $jar "$arch_class"
popd
rm -r suwayomi-patch
find -name __pycache__ -type d -prune -exec rm -rf {} +

%conf
%meson

%build
%meson_build

%install
%meson_install
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/%{name}

%check
%meson_test

%files
%license COPYING
%doc README.md
%{_bindir}/kaori
%{_datadir}/%{name}/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{app_id}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{app_id}-symbolic.svg
%{_metainfodir}/%{app_id}.metainfo.xml

%changelog
* Fri Oct 23 2026 Trung Lê <trung.le@ruby-journal.com> - 0.9.8-1
- Initial package
