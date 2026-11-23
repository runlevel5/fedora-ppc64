Name:           orion2re
Version:        2.0.2
Release:        1%{?dist}
Summary:        Restoration of the Master of Orion II game engine

# orion2re:                     GPL-3.0-or-later
# src/game/scalers/hqx.cpp:     ISC
# src/game/scalers/mmpx.cpp:    MIT
License:        GPL-3.0-or-later AND ISC AND MIT
URL:            https://github.com/orion2re/orion2re
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Its icon (the game's box art, so not redistributable) comes with
# orion2re-data
Source1:        %{name}.desktop

BuildRequires:  cmake >= 3.20
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake(miniz)
# With the fonts in /usr/share/imgui/fonts
BuildRequires:  imgui-devel >= 1.92.8-2
BuildRequires:  lua-devel >= 5.5
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat) >= 58.76
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(sdl3) >= 3.4
BuildRequires:  pkgconfig(yyjson) >= 0.12

%description
orion2re (Orion2 Redone) is a restoration of the Master of Orion II game
engine, with an online multiplayer router, scalers and supported mods.

It does not include the original game data. Install the files of a
legitimate copy of Master of Orion II (GOG or Steam) in
~/.local/share/orion2re/game, or system-wide in
%{_datadir}/%{name}/game with the orion2re-data package built from your
own copy.

%prep
%autosetup
# Executable in the upstream tree
chmod -x LICENSE
# Not used: the cinematics are decoded with FFmpeg, as Fedora does not
# package libsmacker
rm -r vendors/libsmacker

%conf
# doctest is only for the tests
%cmake \
    -DORION2RE_USE_FFMPEG_SMACKER=ON \
    -DORION2RE_USE_SYSTEM_IMGUI=ON \
    -DORION2RE_USE_SYSTEM_LIBUV=ON \
    -DORION2RE_USE_SYSTEM_LUA=ON \
    -DORION2RE_USE_SYSTEM_LZ4=ON \
    -DORION2RE_USE_SYSTEM_MINIZ=ON \
    -DORION2RE_USE_SYSTEM_SDL3=ON \
    -DORION2RE_USE_SYSTEM_YYJSON=ON

%build
%cmake_build

%install
%cmake_install
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%license LICENSE
%doc README.md
%{_bindir}/orion2re
%{_bindir}/orion2re-router
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/

%changelog
* Mon Nov 23 2026 Trung Lê <8@tle.id.au> - 2.0.2-1
- Update to 2.0.2
- Drop the patches, all merged upstream (the cinematics are still decoded
  with FFmpeg)

* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 2.0.1^20261116git6081749-1
- Update to the 20261116 snapshot (6081749), after 2.0.1
- Build with the system Dear ImGui, Lua, libuv, lz4, miniz, SDL3 and
  yyjson through upstream's ORION2RE_USE_SYSTEM_* options
- Decode the cinematics with FFmpeg instead of the bundled libsmacker
- Install with upstream's install rules; the game files go in
  ~/.local/share/orion2re/game or, with orion2re-data,
  /usr/share/orion2re/game
- Add a desktop launcher
- Keep an index of the directories searched for the game files, so loading
  a screen does not list /usr/bin hundreds of times

* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 2.0.0-1
- Initial package
