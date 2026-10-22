%global imgui_version 1.92.9b

Name:           orion2re
Version:        2.0.0
Release:        1%{?dist}
Summary:        Restoration of the Master of Orion II game engine

# orion2re:            GPL-3.0-or-later
# vendors/imgui:       MIT (including the embedded ProggyTiny font)
# vendors/libsmacker:  LGPL-2.1-only
License:        GPL-3.0-or-later AND MIT AND LGPL-2.1-only
URL:            https://github.com/orion2re/orion2re
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# The vendors/imgui submodule at the commit v2.0.0 pins (v1.92.9b); Dear
# ImGui is not packaged in Fedora.
Source1:        https://github.com/ocornut/imgui/archive/v%{imgui_version}/imgui-%{imgui_version}.tar.gz

# Build with Fedora's SDL3, libuv, lz4, miniz, yyjson and Lua instead of the
# vendors/ submodules
Patch:          orion2re-2.0.0-system-libs.patch

BuildRequires:  cmake >= 3.20
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(lua) >= 5.5
BuildRequires:  pkgconfig(miniz)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  pkgconfig(yyjson) >= 0.12

Provides:       bundled(imgui) = %{imgui_version}
Provides:       bundled(libsmacker) = 1.1.1

%description
orion2re (Orion2 Redone) is a restoration of the Master of Orion II game
engine, with an online multiplayer router, scalers and supported mods.

It does not include the original game data: run it from the directory of a
legitimate copy of Master of Orion II (GOG or Steam), after linking the data
files from %{_datadir}/%{name}/data into that directory's data/ folder.

%prep
%autosetup -p1 -a1
rmdir vendors/imgui
mv imgui-%{imgui_version} vendors/imgui

%conf
%cmake -DORION2RE_USE_SYSTEM_LIBS=ON

%build
%cmake_build

%install
install -Dpm 0755 %{__cmake_builddir}/orion2re %{buildroot}%{_bindir}/orion2re
install -Dpm 0755 %{__cmake_builddir}/orion2re-router %{buildroot}%{_bindir}/orion2re-router
install -d %{buildroot}%{_datadir}/%{name}/data/mods
install -pm 0644 %{__cmake_builddir}/data/base.zip \
    %{__cmake_builddir}/data/orion2re.cfg \
    %{buildroot}%{_datadir}/%{name}/data/
install -pm 0644 %{__cmake_builddir}/data/mods/*.zip \
    %{buildroot}%{_datadir}/%{name}/data/mods/

%files
%license LICENSE
%license vendors/imgui/LICENSE.txt
%license vendors/libsmacker/COPYING
%doc README.md
%{_bindir}/orion2re
%{_bindir}/orion2re-router
%{_datadir}/%{name}/

%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 2.0.0-1
- Initial package
