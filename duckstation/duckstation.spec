# DuckStation is CC-BY-NC-ND-4.0 with an additional packaging restriction: it may
# not be packaged without the copyright holder's permission. This package is
# built with that permission.

%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%else
%global toolchain gcc
%endif

# ppc64le-jit branch: PPC64LE host support, VSX GSVector and the ppc64le
# recompiler (Power ISA 2.07, so POWER8 and later).
%global commit ded42d03dad1b85e9d662d1d00a0c9d45d27ab19
%global shortcommit %(c=%{commit}; echo ${c:0:9})
%global commitdate 20261022
%global commitdate_iso 2026-10-22T16:02:24+11:00
%global branch ppc64le-jit
# git describe --tags --match 'v0.1-*'
%global upstream_tag v0.1-11894
%global upstream_distance 499

# Bundled: not in Fedora, built differently (no SoundTouch C wrapper), or a
# fork with API that Fedora's lacks (shaderc). Versions match upstream's
# dependency pack (duckstation/dependencies, release-20261010).
%global libbacktrace_commit 6f8310e238fc3ce68f42f391cbe93fd156bb2c23
%global cpuinfo_commit d236f716399426388eb302236d0f3168ed83834a
%global spirv_cross_tag vulkan-sdk-1.4.357.0
%global shaderc_commit 4984f691acbbb22d5b11b786330c4b6e6c4a9820
%global discord_rpc_commit cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global soundtouch_commit 463ade388f3a51da078dc9ed062bf28e4ba29da7

# Installed next to the binary, which finds them through RUNPATH $ORIGIN.
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^lib(backtrace|cpuinfo|spirv-cross-c-shared|shaderc_shared|discord-rpc|soundtouch)\\.so.*$

# The binary needs RUNPATH $ORIGIN for the bundled libraries.
%global _cmake_skip_rpath %{nil}

Name:           duckstation
Version:        0.1.11894^%{commitdate}git%{shortcommit}
Release:        4%{?dist}
Summary:        PlayStation 1 emulator
# DuckStation: CC-BY-NC-ND-4.0
# dep/ (statically linked): MIT (fmt, imgui, rapidyaml, rcheevos, zydis,
#   biscuit, glad), BSD-3-Clause (vixl, xbyak, libchdr, reshadefx, speex),
#   BSD-2-Clause (xxhash), ISC (cubeb), Zlib (minizip), Apache-2.0 OR MIT
#   (vulkan headers), public domain (lzma)
# Bundled: BSD-3-Clause (libbacktrace), BSD-2-Clause (cpuinfo), Apache-2.0
#   (SPIRV-Cross, shaderc, glslang, SPIRV-Tools), MIT (discord-rpc),
#   LGPL-2.1-or-later (SoundTouch)
License:        CC-BY-NC-ND-4.0 AND MIT AND BSD-2-Clause AND BSD-3-Clause AND Apache-2.0 AND ISC AND Zlib AND LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain
URL:            https://www.duckstation.org/
Source0:        https://github.com/runlevel5/duckstation-ppc64/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/ianlancetaylor/libbacktrace/archive/%{libbacktrace_commit}/libbacktrace-%{libbacktrace_commit}.tar.gz
Source2:        https://github.com/stenzek/cpuinfo/archive/%{cpuinfo_commit}/cpuinfo-%{cpuinfo_commit}.tar.gz
Source3:        https://github.com/KhronosGroup/SPIRV-Cross/archive/refs/tags/%{spirv_cross_tag}.tar.gz#/SPIRV-Cross-%{spirv_cross_tag}.tar.gz
Source4:        https://github.com/stenzek/shaderc/archive/%{shaderc_commit}/shaderc-%{shaderc_commit}.tar.gz
Source5:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_commit}/discord-rpc-%{discord_rpc_commit}.tar.gz
Source6:        https://github.com/stenzek/soundtouch/archive/%{soundtouch_commit}/soundtouch-%{soundtouch_commit}.tar.gz
# Replaces CMakeModules/DuckStationDependencies.cmake: use Fedora's libraries
# and the bundled ones above instead of upstream's prebuilt dependency pack.
Source10:       DuckStationDependencies.cmake
# Fedora's libpng has no APNG patch: build without animated PNG support
# (single-frame read and write) instead of failing to load libpng at all.
Patch0:         duckstation-libpng-without-apng.patch
# Fedora's libsqlite3 soname is libsqlite3.so.0, not .so.3.
Patch1:         duckstation-sqlite-soname.patch
# fastjmp.cpp is only a top-level asm() block, which GCC LTO drops from the
# static library's symbol table: build it without LTO.
Patch2:         duckstation-fastjmp-no-lto.patch
# Upstream refuses to start when installed under /usr/, failing with an empty
# "Process Startup Failed" message box.
Patch3:         duckstation-allow-usr.patch

# Other architectures have upstream builds.
ExclusiveArch:  ppc64le

BuildRequires:  cmake >= 3.19
BuildRequires:  ninja-build
BuildRequires:  make
%if "%{toolchain}" == "gcc"
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
%if "%{toolchain}" == "clang"
BuildRequires:  clang
BuildRequires:  lld
%endif
# SPIRV-Tools (in shaderc) generates sources with Python.
BuildRequires:  python3
BuildRequires:  extra-cmake-modules
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

BuildRequires:  cmake(Qt6Core) >= 6.11
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng16)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libsharpyuv)
BuildRequires:  pkgconfig(libwebpdecoder)
BuildRequires:  pkgconfig(libwebpdemux)
BuildRequires:  pkgconfig(libwebpmux)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(plutosvg)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)

# Qt private API (GuiPrivate) is tied to the exact Qt version.
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
# Loaded at runtime with dlopen(), so not found by the dependency generator.
Requires:       freetype%{?_isa}
Requires:       harfbuzz%{?_isa}
Requires:       libjpeg-turbo%{?_isa}
Requires:       libpng%{?_isa}
Requires:       libwebp%{?_isa}
Requires:       libzip%{?_isa}
Requires:       plutosvg%{?_isa}
Requires:       sqlite-libs%{?_isa}
Requires:       SDL3%{?_isa}
Requires:       libxcb%{?_isa}
Requires:       libglvnd-egl%{?_isa}
Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme
# Video capture
Recommends:     libavcodec-free%{?_isa}
Recommends:     libavformat-free%{?_isa}
Recommends:     libavutil-free%{?_isa}
Recommends:     libswresample-free%{?_isa}
Recommends:     libswscale-free%{?_isa}

Provides:       bundled(libbacktrace) = 0^git%(c=%{libbacktrace_commit}; echo ${c:0:7})
Provides:       bundled(cpuinfo) = 0^git%(c=%{cpuinfo_commit}; echo ${c:0:7})
Provides:       bundled(spirv-cross) = %(t=%{spirv_cross_tag}; echo ${t#vulkan-sdk-})
Provides:       bundled(shaderc) = 0^git%(c=%{shaderc_commit}; echo ${c:0:7})
Provides:       bundled(glslang)
Provides:       bundled(spirv-tools)
Provides:       bundled(discord-rpc) = 3.4.0^git%(c=%{discord_rpc_commit}; echo ${c:0:7})
Provides:       bundled(soundtouch) = 0^git%(c=%{soundtouch_commit}; echo ${c:0:7})

%description
DuckStation is a simulator/emulator of the Sony PlayStation(TM) console,
focusing on playability, speed, and long-term maintainability.

This build is from the ppc64le-jit branch, which adds a ppc64le (POWER8 and
later) recompiler and VSX vector code.


%prep
%autosetup -p1 -n %{name}-ppc64-%{commit}

mkdir bundled
for s in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
  tar -C bundled -xf "$s"
done

cp -p %{SOURCE10} CMakeModules/DuckStationDependencies.cmake

# The version comes from git, which the tarball does not have.
cat > src/scmversion/gen_scmversion.sh << 'EOF'
#!/bin/sh
cat > scmversion.cpp << EOT
const char* g_scm_hash_str = "%{commit}";
const char* g_scm_branch_str = "%{branch}";
const char* g_scm_tag_str = "%{upstream_tag}-%{upstream_distance}-g%{shortcommit}";
const char* g_scm_version_str = "%{upstream_tag}-%{upstream_distance}";
const char* g_scm_date_str = "%{commitdate_iso}";
EOT
EOF

sed -e 's/@GIT_VERSION@/%{upstream_tag}-%{upstream_distance}/' \
    -e 's/@GIT_DATE@/%(d=%{commitdate}; echo ${d:0:4}-${d:4:2}-${d:6:2})/' \
    -e 's/@GIT_HASH@/%{commit}/' \
    scripts/appimage/org.duckstation.DuckStation.metainfo.xml.in \
    > org.duckstation.DuckStation.metainfo.xml


%build
%set_build_flags
bundled_prefix="$PWD/bundled/prefix"

# Bundled libraries, built shared into a local prefix.
bundled_cmake() {
  src="$1"; shift
  cmake -S "$src" -B "$src/build" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS_RELEASE=-DNDEBUG \
    -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
    -DCMAKE_INSTALL_PREFIX="$bundled_prefix" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    "$@"
  cmake --build "$src/build" %{?_smp_mflags}
  cmake --install "$src/build"
}

pushd bundled/libbacktrace-%{libbacktrace_commit}
./configure --prefix="$bundled_prefix" --libdir="$bundled_prefix/lib" \
  --enable-shared --disable-static --with-pic
%make_build
make install
popd

bundled_cmake bundled/cpuinfo-%{cpuinfo_commit} \
  -DCPUINFO_LIBRARY_TYPE=shared \
  -DCPUINFO_RUNTIME_TYPE=shared \
  -DCPUINFO_LOG_LEVEL=error \
  -DCPUINFO_LOG_TO_STDIO=ON \
  -DCPUINFO_BUILD_TOOLS=OFF \
  -DCPUINFO_BUILD_UNIT_TESTS=OFF \
  -DCPUINFO_BUILD_MOCK_TESTS=OFF \
  -DCPUINFO_BUILD_BENCHMARKS=OFF \
  -DUSE_SYSTEM_LIBS=ON

bundled_cmake bundled/SPIRV-Cross-%{spirv_cross_tag} \
  -DSPIRV_CROSS_SHARED=ON \
  -DSPIRV_CROSS_STATIC=OFF \
  -DSPIRV_CROSS_CLI=OFF \
  -DSPIRV_CROSS_ENABLE_TESTS=OFF \
  -DSPIRV_CROSS_ENABLE_GLSL=ON \
  -DSPIRV_CROSS_ENABLE_HLSL=OFF \
  -DSPIRV_CROSS_ENABLE_MSL=OFF \
  -DSPIRV_CROSS_ENABLE_CPP=OFF \
  -DSPIRV_CROSS_ENABLE_REFLECT=OFF \
  -DSPIRV_CROSS_ENABLE_C_API=ON \
  -DSPIRV_CROSS_ENABLE_UTIL=ON

# glslang and SPIRV-Tools come vendored in third_party/ and are linked in
# statically.
bundled_cmake bundled/shaderc-%{shaderc_commit} \
  -DBUILD_SHARED_LIBS=OFF \
  -DSHADERC_SKIP_TESTS=ON \
  -DSHADERC_SKIP_EXAMPLES=ON \
  -DSHADERC_SKIP_EXECUTABLES=ON \
  -DSHADERC_SKIP_COPYRIGHT_CHECK=ON \
  -DSHADERC_ENABLE_HLSL=OFF \
  -DSHADERC_ENABLE_WERROR_COMPILE=OFF

bundled_cmake bundled/discord-rpc-%{discord_rpc_commit} \
  -DBUILD_SHARED_LIBS=ON

bundled_cmake bundled/soundtouch-%{soundtouch_commit} \
  -DSOUNDTOUCH_DLL=ON

# The host page size is a compile-time constant unless a range is given; Fedora
# ppc64le kernels use 64K pages, others may use 4K.
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DDS_BUNDLED_PREFIX="$bundled_prefix" \
  -DHOST_MIN_PAGE_SIZE=4096 \
  -DHOST_MAX_PAGE_SIZE=65536
%cmake_build


%install
install -d %{buildroot}%{_libdir}/%{name}
cp -a %{_vpath_builddir}/bin/. %{buildroot}%{_libdir}/%{name}/
cp -P bundled/prefix/lib/*.so* %{buildroot}%{_libdir}/%{name}/

# Resources and translations are found relative to the real path of the
# binary, so a symlink is enough.
install -d %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{name}/duckstation-qt %{buildroot}%{_bindir}/duckstation-qt

install -Dpm 0644 scripts/appimage/org.duckstation.DuckStation.desktop \
  %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop
install -Dpm 0644 scripts/appimage/org.duckstation.DuckStation.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png
install -Dpm 0644 org.duckstation.DuckStation.metainfo.xml \
  %{buildroot}%{_metainfodir}/org.duckstation.DuckStation.metainfo.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/org.duckstation.DuckStation.metainfo.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/duckstation-qt
%{_libdir}/%{name}/
%{_datadir}/applications/org.duckstation.DuckStation.desktop
%{_datadir}/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png
%{_metainfodir}/org.duckstation.DuckStation.metainfo.xml


%changelog
* Fri Oct 23 2026 Trung Lê <trung.le@ruby-journal.com> - 0.1.11894^20261022gitded42d03d-4
- Allow running from /usr, fixing the empty "Process Startup Failed" message
  box at startup.

* Thu Oct 22 2026 Trung Lê <trung.le@ruby-journal.com> - 0.1.11894^20261022gitded42d03d-3
- Build fastjmp.cpp without LTO, fixing undefined fastjmp_set/fastjmp_jmp
  when linking with GCC LTO.

* Thu Oct 22 2026 Trung Lê <trung.le@ruby-journal.com> - 0.1.11894^20261022gitded42d03d-2
- Fetch the source from runlevel5/duckstation-ppc64 (the repository was
  renamed), whose tarball unpacks to duckstation-ppc64-<commit>.

* Thu Oct 22 2026 Trung Lê <trung.le@ruby-journal.com> - 0.1.11894^20261022gitded42d03d-1
- Initial package, from the ppc64le-jit branch (ppc64le recompiler).
- Use Fedora's libraries instead of upstream's prebuilt dependency pack;
  bundle libbacktrace, cpuinfo, SPIRV-Cross, shaderc, discord-rpc and
  SoundTouch, which Fedora lacks or builds differently.
