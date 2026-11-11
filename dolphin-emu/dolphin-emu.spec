# Upstream master, with the ppc64le patch of the matching
# https://github.com/runlevel5/dolphin-ppc64 release.
%global commit 41799046d68b2e5ea7cfde91f122320a472b7a61
%global shortcommit %(c=%{commit}; echo ${c:0:9})
%global commitdate 20261108
# git describe --tags
%global upstream_tag 2609
%global upstream_distance 197

# Submodules. The GitHub archive carries none, so the ones that are built from
# Externals are fetched separately: upstream has no system option for them
# (imgui, implot, tinygltf, watcher, cpp-optparse, cpp-ipc, rcheevos, the
# Vulkan headers and VulkanMemoryAllocator), or Fedora's is too old (SFML:
# upstream needs 3.0, Fedora has 2.6). Everything else comes from Fedora, and
# the in-tree Externals that have no submodule cover the rest.
%global imgui_commit 45acd5e0e82f4c954432533ae9985ff0e1aad6d5
%global implot_commit 3da8bd34299965d3b0ab124df743fe3e076fa222
%global tinygltf_commit c5641f2c22d117da7971504591a8f6a41ece488b
%global watcher_commit b03bdcfc11549df595b77239cefe2643943a3e2f
%global cpp_optparse_commit 2265d647232249a53a03b411099863ceca35f0d3
%global cpp_ipc_commit b6cbbc940e25ff898f09a40b107781cef6027b13
%global vulkan_headers_commit 39f924b810e561fd86b2558b6711ca68d4363f68
%global vma_commit 3bab6924988e5f19bf36586a496156cf72f70d9f
%global rcheevos_commit 926e4608f8dca7989267c787bbefb3ab1c835ac5
%global sfml_commit 0fa201c969e48ecc253581c5841ce73f44d42f49

Name:           dolphin-emu
Version:        %{upstream_tag}^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        GameCube and Wii emulator
# Dolphin itself: GPL-2.0-or-later
# Externals built into it, in-tree: LGPL-2.1-or-later (Bochs_disasm),
#   GPL-2.0-or-later (FreeSurround), MIT (expr, picojson, discord-rpc),
#   BSD-1-Clause (FatFs), CC0-1.0 (ed25519), Apache-2.0 (mbedtls)
# Externals built into it, fetched here: MIT (imgui, implot, tinygltf, watcher,
#   cpp-optparse, cpp-ipc, rcheevos, VulkanMemoryAllocator), Zlib (SFML),
#   Apache-2.0 (Vulkan-Headers)
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND BSD-1-Clause AND CC0-1.0 AND Apache-2.0 AND Zlib
URL:            https://dolphin-emu.org/
Source0:        https://github.com/dolphin-emu/dolphin/archive/%{commit}/dolphin-%{shortcommit}.tar.gz
Source1:        https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source2:        https://github.com/epezent/implot/archive/%{implot_commit}/implot-%{implot_commit}.tar.gz
Source3:        https://github.com/syoyo/tinygltf/archive/%{tinygltf_commit}/tinygltf-%{tinygltf_commit}.tar.gz
Source4:        https://github.com/e-dant/watcher/archive/%{watcher_commit}/watcher-%{watcher_commit}.tar.gz
Source5:        https://github.com/weisslj/cpp-optparse/archive/%{cpp_optparse_commit}/cpp-optparse-%{cpp_optparse_commit}.tar.gz
Source6:        https://github.com/mutouyun/cpp-ipc/archive/%{cpp_ipc_commit}/cpp-ipc-%{cpp_ipc_commit}.tar.gz
Source7:        https://github.com/KhronosGroup/Vulkan-Headers/archive/%{vulkan_headers_commit}/Vulkan-Headers-%{vulkan_headers_commit}.tar.gz
Source8:        https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/archive/%{vma_commit}/VulkanMemoryAllocator-%{vma_commit}.tar.gz
Source9:        https://github.com/RetroAchievements/rcheevos/archive/%{rcheevos_commit}/rcheevos-%{rcheevos_commit}.tar.gz
Source10:       https://github.com/SFML/SFML/archive/%{sfml_commit}/SFML-%{sfml_commit}.tar.gz
# The 13 commits of https://github.com/runlevel5/dolphin-ppc64/pull/1, squashed
# and rebased onto the commit above: a JIT for ppc64le hosts, the Power ISA
# paths of the vertex loader and the texture hash, and the FIFO, MMU and timing
# fixes that go with them.
Patch0:         https://github.com/runlevel5/dolphin-ppc64/releases/download/ppc64-%{upstream_tag}-%{upstream_distance}/dolphin-%{upstream_tag}-%{upstream_distance}-ppc64le.patch

# The patch is the point of this build; upstream covers the other
# architectures.
ExclusiveArch:  ppc64le

BuildRequires:  cmake >= 3.13
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gettext

BuildRequires:  cmake(Qt6Core) >= 6.2
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Svg)
# For qplatformnativeinterface.h, with Qt 6.10 and later
BuildRequires:  cmake(Qt6GuiPrivate)
BuildRequires:  qt6-linguist
BuildRequires:  llvm-devel
# No pkgconfig file; upstream looks for the header and the library.
BuildRequires:  cubeb-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bluez)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(minizip-ng)
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  pkgconfig(spng)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  glslang-devel
BuildRequires:  hidapi-devel
BuildRequires:  lzo-devel
BuildRequires:  miniupnpc-devel

Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(imgui) = 0^git%(c=%{imgui_commit}; echo ${c:0:7})
Provides:       bundled(implot) = 0^git%(c=%{implot_commit}; echo ${c:0:7})
Provides:       bundled(tinygltf) = 0^git%(c=%{tinygltf_commit}; echo ${c:0:7})
Provides:       bundled(watcher) = 0^git%(c=%{watcher_commit}; echo ${c:0:7})
Provides:       bundled(cpp-optparse) = 0^git%(c=%{cpp_optparse_commit}; echo ${c:0:7})
Provides:       bundled(cpp-ipc) = 0^git%(c=%{cpp_ipc_commit}; echo ${c:0:7})
Provides:       bundled(vulkan-headers) = 0^git%(c=%{vulkan_headers_commit}; echo ${c:0:7})
Provides:       bundled(vulkanmemoryallocator) = 0^git%(c=%{vma_commit}; echo ${c:0:7})
Provides:       bundled(rcheevos) = 0^git%(c=%{rcheevos_commit}; echo ${c:0:7})
Provides:       bundled(SFML) = 3.0^git%(c=%{sfml_commit}; echo ${c:0:7})
Provides:       bundled(mbedtls) = 2.28
Provides:       bundled(discord-rpc)

%description
Dolphin is an emulator for the Nintendo GameCube and Wii. It runs games at
full HD with several enhancements, and supports the GameCube controller and
the Wii Remote.

This build adds a ppc64le (POWER8 and later) JIT, so that games are
recompiled to host code instead of interpreted, with VSX paths for the vertex
loader and the texture hash on Power ISA 3.0 (POWER9 and later).


%prep
%autosetup -p1 -n dolphin-%{commit}

# Submodules, which the archive does not carry.
untar() {
  mkdir -p "$2"
  tar -xf "$1" --strip-components=1 -C "$2"
}
untar %{SOURCE1} Externals/imgui/imgui
untar %{SOURCE2} Externals/implot/implot
untar %{SOURCE3} Externals/tinygltf/tinygltf
untar %{SOURCE4} Externals/watcher/watcher
untar %{SOURCE5} Externals/cpp-optparse/cpp-optparse
untar %{SOURCE6} Externals/cpp-ipc/cpp-ipc
untar %{SOURCE7} Externals/Vulkan-Headers
untar %{SOURCE8} Externals/VulkanMemoryAllocator
untar %{SOURCE9} Externals/rcheevos/rcheevos
untar %{SOURCE10} Externals/SFML/SFML

# The archive is not a git checkout, and upstream asks git for the version
# whenever it finds it, which leaves the version as "2609.0 (no further
# info)". Keep it from looking, so that it uses the values passed below.
sed -i 's/^find_package(Git)$/set(GIT_FOUND FALSE)/' CMakeLists.txt


%build
# The version comes from git, which the archive does not have: pass what
# ScmRevGen.cmake would have asked git for.
# Dolphin links its parts together statically, and they refer to each other:
# as shared libraries they are a dependency cycle, which Fedora's cmake macro
# would ask for.
%cmake -G Ninja \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DDISTRIBUTOR="COPR tle/power" \
    -DGIT_FOUND=FALSE \
    -DDOLPHIN_WC_REVISION=%{commit} \
    -DDOLPHIN_WC_DESCRIBE=%{upstream_tag}-%{upstream_distance} \
    -DDOLPHIN_WC_BRANCH=master \
    -DENABLE_AUTOUPDATE=OFF \
    -DENABLE_NOGUI=ON \
    -DENABLE_TESTS=ON \
    -DUSE_MGBA=OFF \
    -DAPPROVED_VENDORED_DEPENDENCIES="sfml;mbedtls"

%cmake_build


%install
%cmake_install

# Written by the build; upstream installs it only in the Flatpak.
install -Dpm 0644 %{_vpath_builddir}/Flatpak/org.DolphinEmu.dolphin-emu.metainfo.xml \
  %{buildroot}%{_metainfodir}/org.DolphinEmu.dolphin-emu.metainfo.xml

%find_lang %{name}


%check
# The unit tests are not part of the default target, and they are registered
# in the subdirectory that enables testing.
%cmake_build --target tests
ctest --test-dir %{_vpath_builddir}/Source/UnitTests --output-on-failure
desktop-file-validate %{buildroot}%{_datadir}/applications/dolphin-emu.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/org.DolphinEmu.dolphin-emu.metainfo.xml


%files -f %{name}.lang
%license COPYING LICENSES
%doc Readme.md
%{_bindir}/dolphin-emu
%{_bindir}/dolphin-emu-nogui
%{_bindir}/dolphin-tool
%{_datadir}/dolphin-emu/
%{_datadir}/applications/dolphin-emu.desktop
%{_datadir}/icons/hicolor/scalable/apps/dolphin-emu.svg
%{_datadir}/icons/hicolor/256x256/apps/dolphin-emu.png
%{_metainfodir}/org.DolphinEmu.dolphin-emu.metainfo.xml
%{_mandir}/man6/dolphin-emu.6*
%{_mandir}/man6/dolphin-emu-nogui.6*


%changelog
* Tue Nov 10 2026 Trung Lê <trung.le@ruby-journal.com> - 2609^20261108git41799046d-1
- Update to upstream master 41799046d (2609-197), with the ppc64le patch of
  the dolphin-ppc64 ppc64-2609-197 release, fetched from the release; the
  ppc64le backend is unchanged
- Build require bzip2 and Qt's private GUI headers, which upstream needs
  and the spec did not list
- Drop the bundled(lzo) provide, as LZO comes from Fedora

* Fri Nov 06 2026 Trung Lê <trung.le@ruby-journal.com> - 2609^20261105git322d8b8d8-1
- Initial package, from upstream master 322d8b8d8 with the ppc64le backend of
  runlevel5/dolphin-ppc64#1: a JIT for ppc64le hosts, Power ISA 3.0 vertex
  loading and texture hashing, and the FIFO, MMU and timing fixes that go
  with them.
