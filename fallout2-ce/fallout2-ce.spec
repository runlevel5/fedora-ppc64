%global commit      ec2fe498acfcebd42aa8a9111ee7acbc413f77cc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261116

# The bundled fpattern's shared libraries are private
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude      ^libfpattern

Name:           fallout2-ce
Version:        1.3.0^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Community edition of the Fallout 2 engine

# Main license:                                SUL-1.0 (Sustainable Use
#   License: non-commercial use and free-of-charge distribution only)
# third_party/fpattern:                        MIT
# third_party/lodepng:                         Zlib
License:        SUL-1.0 AND MIT AND Zlib
URL:            https://github.com/fallout2-ce/fallout2-ce
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        %{name}.desktop
# Launcher, running the engine in a per-user game directory mirroring the
# shared data in %%{_datadir}/%%{name}
Source2:        %{name}.sh

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  icoutils
BuildRequires:  ninja-build
BuildRequires:  stb_vorbis-devel
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme

Provides:       bundled(fpattern) = 1.0.0
Provides:       bundled(lodepng)

# Other architectures have upstream builds
ExclusiveArch:  ppc64le

BuildSystem:    cmake
BuildOption:    -GNinja
BuildOption:    -DCMAKE_BUILD_TYPE=Release
# SDL 2 and zlib from the system instead of the copies upstream downloads
BuildOption:    -DFALLOUT_VENDORED=OFF
BuildOption:    -DFALLOUT_STB_VORBIS_DIR=%{_includedir}
# The bundled fpattern is built as shared libraries, which go in a private
# directory in %%{_libdir}, found by the binaries' runpath
BuildOption:    -DBUILD_SHARED_LIBS=ON
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH=%{_libdir}/%{name}

%description
Fallout 2 Community Edition is a re-implementation of the engine of
Interplay's 1998 role-playing game, with high resolution support,
quality-of-life improvements and many bug fixes, built here for ppc64le
with the system SDL 2 and zlib.

This package contains no game data. Copy the files of your own copy of
Fallout 2 (master.dat, critter.dat, patch000.dat and the data folder) to
%{_datadir}/%{name}, shared by all users, or to your game directory,
~/.local/share/%{name}: the fallout2-ce launcher runs the game there,
mirroring the shared data, and the game keeps its configuration and saved
games there.

%package tools
Summary:        Modding tools for the Fallout 2 engine
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools for the Fallout 2 CE engine: mapper-ce, the map editor, run in a
game directory like the game; ce-dat-tool, to list, extract and create DAT
archives; and ce-frm2png, to convert FRM images to PNG.

%prep -a
# The system's stb_vorbis is used instead
rm -r third_party/stb_vorbis
cp -p third_party/fpattern/LICENSE LICENSE.fpattern
cp -p third_party/lodepng/LICENSE LICENSE.lodepng
# The version shown in the main menu, which upstream takes from git (the
# build fails without its date)
sed -i -e 's|@AUTHOR@||' -e 's|@BRANCH@|main|' \
    -e 's|@HASH@|%{shortcommit}|' -e 's|@LATEST_TAG@|v1.3.0|' \
    -e "s|@DATE@|\"$(LC_ALL=C date -u -d %{commitdate} '+%%b %%d %%Y')\"|" \
    src/platform/git_version.h.in

%build -a
# The engine's base mod, which upstream ships with its Linux builds
LD_LIBRARY_PATH=%{__cmake_builddir}/third_party/fpattern \
    %{__cmake_builddir}/ce-dat-tool create files/ce.dat ce.dat

%install -a
# The game reads its data, and writes its configuration and saved games, in
# its working directory, so the binary goes in %%{_libexecdir}, run from a
# launcher in the user's game directory
install -Dpm 0755 -t %{buildroot}%{_libexecdir}/%{name} \
    %{__cmake_builddir}/fallout2-ce
install -Dpm 0755 -t %{buildroot}%{_libdir}/%{name} \
    %{__cmake_builddir}/third_party/fpattern/libfpattern-static.so \
    %{__cmake_builddir}/third_party/fpattern/libfpattern-windows-static.so
install -Dpm 0755 -t %{buildroot}%{_bindir} \
    %{__cmake_builddir}/mapper-ce \
    %{__cmake_builddir}/ce-dat-tool \
    %{__cmake_builddir}/ce-frm2png
sed -e "s|@LIBEXECDIR@|%{_libexecdir}/%{name}|g" \
    -e "s|@DATADIR@|%{_datadir}/%{name}|g" \
    -e "s|@NAME@|%{name}|g" \
    %{SOURCE2} > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 -t %{buildroot}%{_datadir}/%{name} ce.dat

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
icotool -x -o . os/windows/%{name}.ico
for png in %{name}_*x32.png; do
    size=$(echo $png | sed 's/^%{name}_[0-9]*_\([0-9]*\)x.*/\1/')
    install -Dpm 0644 $png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%files
%license LICENSE.md LICENSE.fpattern LICENSE.lodepng
%doc README.md SFALL_COMPATIBILITY.md files/fallout2.cfg
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ce.dat
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files tools
%{_bindir}/mapper-ce
%{_bindir}/ce-dat-tool
%{_bindir}/ce-frm2png

%changelog
* Wed Nov 18 2026 Trung Lê <8@tle.id.au> - 1.3.0^20261116gitec2fe49-1
- Initial package of Fallout 2 CE (git ec2fe49), built with the system
  SDL 2, zlib and stb_vorbis
