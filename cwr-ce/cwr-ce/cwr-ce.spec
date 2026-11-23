%global commit      0667ada4d4d3fa57efc2d8168f8cf9fec34b17f4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261121

# Upstream builds with Clang only
%global toolchain   clang

Name:           cwr-ce
Version:        1.0.0^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Community edition of the Poseidon game engine

# Main license:                                GPL-3.0-or-later, with
#   additional terms under its Section 7 (see LICENSE): no trademark rights,
#   modified versions must not use Bohemia Interactive's trademarks
# thirdparty/glad (generated OpenGL loader):   (WTFPL OR CC0-1.0) AND Apache-2.0
# thirdparty/renderdoc (in-application API):   MIT
License:        GPL-3.0-or-later AND (WTFPL OR CC0-1.0) AND Apache-2.0 AND MIT
URL:            https://github.com/ofpisnotdead-com/CWR-CE
Source0:        %{url}/archive/%{commit}/CWR-CE-%{commit}.tar.gz
Source1:        %{name}.desktop
# Launcher, pointing the engine at the game data in %%{_datadir}/%%{name}
Source2:        %{name}.sh
# Find FreeType, libcurl, Opus, stb and mimalloc as distributions ship them
# (upstream uses vcpkg), CLI::IsMember in newer CLI11, and an option to
# leave out the Studio UI tests, which need the non-free Dear ImGui Test
# Engine (not upstream yet)
Patch:          %{name}-system-libs.patch
# Set the port and a valid address when the local host name does not resolve,
# as on COPR's builders (not upstream yet)
Patch:          %{name}-local-address.patch

BuildRequires:  clang
# clang-format, which configuring requires (for the Format targets)
BuildRequires:  clang-tools-extra
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  icoutils
BuildRequires:  ninja-build
BuildRequires:  cmake(Catch2) >= 3
BuildRequires:  cmake(CLI11)
BuildRequires:  cmake(cJSON)
BuildRequires:  cmake(enkiTS)
BuildRequires:  cmake(glslang)
BuildRequires:  cmake(imgui)
BuildRequires:  cmake(mimalloc)
BuildRequires:  cmake(Ogg)
BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(SDL3)
BuildRequires:  cmake(spdlog)
BuildRequires:  cmake(Vorbis)
BuildRequires:  cmake(zstd)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_resize2-devel
BuildRequires:  stb_image_write-devel

# OpenAL is loaded with dlopen()
Requires:       openal-soft%{?_isa}
Requires:       hicolor-icon-theme
# The game data, built locally from your own copy of the game (see the
# cwr-ce-data spec)
Recommends:     cwr-ce-data

Provides:       bundled(glad) = 2

# Other architectures have upstream builds
ExclusiveArch:  ppc64le

BuildSystem:    cmake
BuildOption:    -GNinja
BuildOption:    -DCMAKE_BUILD_TYPE=Release
# Fedora's build flags warn where upstream's don't
BuildOption:    -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF
BuildOption:    -DCWR_BUILD_STUDIO_UI_TESTS=OFF

%description
CWR-CE is the community edition of Poseidon, the engine of Bohemia
Interactive's 2001 Cold War military simulation, released under the GPL:
modernized to C++20, with SDL 3, OpenGL 4.5 and OpenAL, and built here for
ppc64le.

This package contains the game (cwr-ce) and the dedicated server
(cwr-ce-server). They contain no game data: build the cwr-ce-data package
from your own copy of the remastered game, which installs it to
%{_datadir}/%{name}, where they look for it.

%package tools
Summary:        Asset tools for the Poseidon game engine
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools for the game data of the Poseidon engine: PoseidonTools, a
command-line tool to list, extract and pack PBO archives and to convert and
inspect textures, models, sounds and terrain, and PoseidonStudio, a
graphical asset browser.

%build -p
# The version tag, which the game and server compare in multiplayer; upstream
# takes it from git otherwise
export OFPR_BUILD_VERSION_TAG=%{shortcommit}

%install -a
# The game and server look for the data in their working directory, so the
# binaries go in %%{_libexecdir} and are run from launchers passing -C
dist=dist/$(basename %{__cmake_builddir})
install -Dpm 0755 -t %{buildroot}%{_libexecdir}/%{name} \
    $dist/PoseidonGame $dist/PoseidonServer
install -pm 0755 $dist/PoseidonStudio %{buildroot}%{_bindir}/
for b in cwr-ce:PoseidonGame cwr-ce-server:PoseidonServer; do
    sed -e "s|@BINARY@|${b#*:}|g" \
        -e "s|@LIBEXECDIR@|%{_libexecdir}/%{name}|g" \
        -e "s|@DATADIR@|%{_datadir}/%{name}|g" \
        %{SOURCE2} > %{buildroot}%{_bindir}/${b%%:*}
    chmod 0755 %{buildroot}%{_bindir}/${b%%:*}
done
mkdir -p %{buildroot}%{_datadir}/%{name}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
icotool -x -o . resources/icon-game.ico
for png in icon-game_*.png; do
    size=$(echo $png | sed 's/^icon-game_[0-9]*_\([0-9]*\)x.*/\1/')
    install -Dpm 0644 $png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%check
# Without the game data, the tests that need it are left out
%ctest

%files
%license LICENSE
%doc README.md CREDITS.md THIRD_PARTY_NOTICES.md
%{_bindir}/%{name}
%{_bindir}/%{name}-server
%{_libexecdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files tools
%{_bindir}/PoseidonStudio
%{_bindir}/PoseidonTools

%changelog
* Mon Nov 23 2026 Trung Lê <8@tle.id.au> - 1.0.0^20261121git0667ada-1
- Update to git 0667ada, which has the ppc64le build support
- Keep the port when the local host name does not resolve, which failed a
  test on COPR's builders
- Set the version tag, which was "unknown"

* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 1.0.0^20261112git62ac4ff-2
- Build-require clang-tools-extra: configuring fails without clang-format

* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 1.0.0^20261112git62ac4ff-1
- Initial package of CWR-CE (git 62ac4ff), built with the system libraries
- Add the ppc64le build support from runlevel5/CWR-CE linux-ppc64le
