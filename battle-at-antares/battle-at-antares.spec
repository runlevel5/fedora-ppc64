# Godot's name for the architecture, the key of the game's library in its
# GDExtension file
%ifarch x86_64
%global godot_arch x86_64
%endif
%ifarch aarch64
%global godot_arch arm64
%endif
%ifarch ppc64le
%global godot_arch ppc64
%endif
%ifarch riscv64
%global godot_arch rv64
%endif

Name:           battle-at-antares
Version:        0.5.1
Release:        1%{?dist}
Summary:        Master of Orion II with a new interface

# Battle at Antares, Orion2 Redone:            GPL-3.0-or-later
# src/game/scalers/hqx.cpp:                    ISC
# src/game/scalers/mmpx.cpp:                   MIT
# vendors/godot-cpp:                           MIT
# vendors/libsmacker:                          LGPL-2.1-or-later
# Saira Semi Condensed (Glass theme):          OFL-1.1
License:        GPL-3.0-or-later AND ISC AND MIT AND LGPL-2.1-or-later AND OFL-1.1
URL:            https://github.com/Crono141/battle-at-antares
# The source of the release, with the submodules
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}-source.tar.gz
# Launcher, running the game in a per-user game directory mirroring the
# shared files and the Master of Orion II files of orion2re-data
Source1:        %{name}.sh
# The game with its own interface, run by the system's Godot
Source2:        antares-godot.sh
Source3:        %{name}.desktop

# Build with the system SDL3, Dear ImGui, Lua, libuv, libwebp, lz4, miniz,
# stb_vorbis and yyjson (ORION2RE_USE_SYSTEM_PACKAGES)
Patch:          battle-at-antares-0.5.1-system-libs.patch
# Inspect Lua chunks through lua_dump instead of Lua's private headers,
# which the system Lua does not ship (from Orion2 Redone)
Patch:          battle-at-antares-0.5.1-lua-public-api.patch

BuildRequires:  cmake >= 3.20
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  zip
BuildRequires:  cmake(imgui) >= 1.92.8
BuildRequires:  cmake(miniz)
BuildRequires:  cmake(SDL3) >= 3.4
# The editor exports the game's pack
BuildRequires:  godot >= 4.7
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(libwebpdecoder)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(lua) >= 5.5
BuildRequires:  pkgconfig(yyjson) >= 0.12
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_vorbis-devel

# Runs the game's pack: Fedora's godot-runner is built without path
# overrides, so it cannot load a pack other than its own
Requires:       godot >= 4.7
# The Master of Orion II files, built from your own copy of the game
Suggests:       orion2re-data

# godot-cpp 10.0.0 (Godot 4.7 API) and libsmacker are not packaged
Provides:       bundled(godot-cpp) = 10.0.0
Provides:       bundled(libsmacker) = 1.1.1

# The game's library is loaded by Godot, not linked
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

ExclusiveArch:  x86_64 aarch64 ppc64le riscv64

%description
Battle at Antares is an HD remaster of Master of Orion II, built on Orion2
Redone: the original game's rules, races and AI, played from a galaxy map
you can pan and zoom, with the game's screens as panels over it. The
original interface is one setting away.

It does not include the original game data. Install orion2re-data, built
from your own copy of Master of Orion II 1.31 (GOG or Steam), or copy the
game's files to ~/.local/share/%{name}, the game directory
the %{name} launcher runs the game in. HD art packs and
other packages go in its data/mods.

%prep
%autosetup -n %{name}-%{version}-source -p1
# The system libraries are used instead; godot-cpp and libsmacker are not
# packaged
find vendors -mindepth 1 -maxdepth 1 ! -name godot-cpp ! -name libsmacker \
    -exec rm -r {} +
cp -p vendors/godot-cpp/LICENSE.md LICENSE.godot-cpp
cp -p vendors/libsmacker/COPYING COPYING.libsmacker
cp -p frontend/godot/project/packages/antares-ui-glass/fonts/OFL-Saira.txt .
# Executable in the upstream tree
chmod -x README.md LICENSE COPYING.libsmacker

%conf
# The configuration bindings are generated, as the source has none. The
# Godot library links the system libstdc++, not a static copy.
%cmake -GNinja \
    -DANTARES_BUILD_GODOT=ON \
    -DANTARES_GODOT_BIN_DIR=%{__cmake_builddir}/godot-bin \
    -DGODOTCPP_USE_STATIC_CPP=OFF \
    -DORION2RE_BUILD_CONFIG_TOOL=ON \
    -DORION2RE_USE_SYSTEM_PACKAGES=ON

%build
%cmake_build --target orion2re antares-launcher antares_godot

# The game's Godot pack, exported as the release's: the project without the
# editor cache, the development library and the themes, which are packages
# of their own. The pack loads the game's library as bin/libantares.so,
# relative to the working directory: antares-godot runs in
# %%{_libdir}/%%{name}.
stage=$PWD/godot-stage
rm -rf $stage
mkdir -p $stage/bin
(cd frontend/godot/project && tar --exclude ./.godot --exclude ./bin \
    --exclude ./.gitignore -cf - .) | tar -C $stage -xf -
for pkg in $stage/packages/*/; do
    [ "$(basename $pkg)" = antares-ui ] || rm -r $pkg
done
cp -p %{__cmake_builddir}/godot-bin/libantares.so $stage/bin/
cat >> $stage/antares.gdextension <<EOF
linux.debug.%{godot_arch} = "res://bin/libantares.so"
linux.release.%{godot_arch} = "res://bin/libantares.so"
EOF
sed -i 's/^binary_format\/architecture="x86_64"$/binary_format\/architecture="%{godot_arch}"/' \
    $stage/export_presets.cfg
export HOME=$PWD/godot-home
# Godot 4.7 aborts at the end of the first headless import of a project
# with a GDExtension
godot --headless --path $stage --import || :
godot --headless --path $stage --import
godot --headless --path $stage --export-pack Linux $PWD/antares-godot.pck

# The Glass theme, packaged as the release's: the package's files, and its
# Godot files in godot/<id>.zip. The Chrome theme carries art cut from the
# original game, which its source does not have.
theme=antares-ui-glass
themes=$PWD/themes
rm -rf $themes && mkdir -p $themes/$theme/godot
(cd frontend/godot/project && zip -qrX $themes/$theme/godot/$theme.zip packages/$theme)
cp -p frontend/godot/project/packages/$theme/{README.md,mod.json5} $themes/$theme/
cp -rp frontend/godot/project/packages/$theme/config $themes/$theme/
(cd $themes/$theme && zip -qrX ../$theme.zip README.md mod.json5 godot config)

%install
install -Dpm 0755 -t %{buildroot}%{_libexecdir}/%{name} \
    %{__cmake_builddir}/antares %{__cmake_builddir}/antares-launcher
install -Dpm 0755 -t %{buildroot}%{_libdir}/%{name}/bin \
    %{__cmake_builddir}/godot-bin/libantares.so
install -Dpm 0644 -t %{buildroot}%{_datadir}/%{name} antares-godot.pck
install -Dpm 0644 -t %{buildroot}%{_datadir}/%{name}/data \
    %{__cmake_builddir}/data/base.zip data/antares.cfg
install -Dpm 0644 -t %{buildroot}%{_datadir}/%{name}/data/mods \
    %{__cmake_builddir}/data/mods/*.zip themes/antares-ui-glass.zip
install -d %{buildroot}%{_bindir}
for script in %{SOURCE1}:%{_bindir}/%{name} \
              %{SOURCE2}:%{_libexecdir}/%{name}/antares-godot; do
    sed -e "s|@NAME@|%{name}|g" \
        -e "s|@DATADIR@|%{_datadir}/%{name}|g" \
        -e "s|@MOO2DIR@|%{_datadir}/orion2re/game|g" \
        -e "s|@LIBEXECDIR@|%{_libexecdir}/%{name}|g" \
        -e "s|@LIBDIR@|%{_libdir}/%{name}|g" \
        ${script%%:*} > %{buildroot}${script#*:}
    chmod 0755 %{buildroot}${script#*:}
done
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE3}

%files
%license LICENSE LICENSE.godot-cpp COPYING.libsmacker OFL-Saira.txt
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Nov 18 2026 Trung Lê <8@tle.id.au> - 0.5.1-1
- Initial package of Battle at Antares 0.5.1, with the system SDL3, Dear
  ImGui, Lua, libuv, libwebp, lz4, miniz, stb_vorbis and yyjson, and the
  Godot interface run by the system's Godot
