%global commit      52088b9eae247d8e321c8dc1fb49a879652854f9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261104

Name:           ioquake3
Version:        1.36^%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        Free and open-source Quake 3 engine

# Main license:                                GPL-2.0-or-later
# code/qcommon/{unzip,ioapi}.c (minizip):      Zlib
# code/renderercommon/puff.c:                  Zlib
# code/client/libmumblelink.c:                 Zlib
# code/qcommon/md5.c, code/sys/sys_autoupdater.c:
#                                              LicenseRef-Fedora-Public-Domain
License:        GPL-2.0-or-later AND Zlib AND LicenseRef-Fedora-Public-Domain
URL:            https://ioquake3.org/
Source0:        https://github.com/ioquake/ioq3/archive/%{commit}/ioq3-%{commit}.tar.gz
# Based on Fedora's quake3.desktop, launching the engine instead of the demo
Source1:        %{name}.desktop
# Fedora's quake3.png
Source2:        %{name}.png
# ppc64le (ELFv2) support for the VM JIT and interpreter, VSX renderer and
# sound paths, POWER8 GPR<->FPR moves for VM float conversions
# https://github.com/ioquake/ioq3/pull/860 (d2eef0c1)
Patch:          %{name}-ppc64le-jit.patch
# Vulkan renderer from vkQuake3
# https://github.com/ioquake/ioq3/pull/861 (9faee827), the PR's diff without
# its copy of the Vulkan headers (the system ones are used) and its
# pre-compiled SPIR-V shaders (they are compiled in %%conf)
Patch:          %{name}-vulkan-renderer.patch
# Quit from the main loop on SIGTERM and SIGINT, rather than in the signal
# handler, where the Vulkan renderer's shutdown can deadlock (not upstream
# yet)
Patch:          %{name}-quit-signal.patch
# DEFAULT_BASEDIR cmake option, to look for game data in /usr/share/quake3
# rather than next to the binaries
Patch:          %{name}-default-basedir.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  glslang
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers

# HTTP downloads dlopen() libcurl.so.4
Requires:       libcurl%{?_isa}
Requires:       hicolor-icon-theme
# The Vulkan renderer loads libvulkan.so.1 through SDL
Requires:       vulkan-loader%{?_isa}

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE=Release
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name}
BuildOption:    -DPRODUCT_VERSION=1.36_g%{shortcommit}
BuildOption:    -DDEFAULT_BASEDIR=%{_datadir}/quake3
BuildOption:    -DUSE_INTERNAL_LIBS=OFF
BuildOption:    -DUSE_OPENAL_DLOPEN=OFF
BuildOption:    -DBUILD_RENDERER_VULKAN=ON
# Game logic comes as QVMs in the game data. QVMs would need lcc, which
# is not free software and is removed in %%prep.
BuildOption:    -DBUILD_GAME_LIBRARIES=OFF
BuildOption:    -DBUILD_GAME_QVMS=OFF

%description
ioquake3 is a free and open-source first person shooter engine based on the
Quake III Arena and Quake III: Team Arena source code, with bug and security
fixes, SDL 2, OpenAL and Ogg Vorbis/Opus audio, VoIP, IPv6, HTTP downloads
and OpenGL 2 and Vulkan renderers (cl_renderer opengl2, the default, or
vulkan).

This package contains the engine (ioquake3) and the dedicated server
(ioq3ded), but no game data. To play Quake III Arena, copy the pak?.pk3 files
of the original game to /usr/share/quake3/baseq3 or
~/.local/share/Quake3/baseq3.

%prep
%autosetup -n ioq3-%{commit} -p1
# Bundled libraries (the system ones are used) and lcc, which is not free
# software
rm -r code/thirdparty code/tools/lcc

%conf -p
# The Vulkan renderer's SPIR-V shaders, as its shaders/compile.sh does
pushd code/renderer_vulkan/shaders
gcc -o bintoc bintoc.c
mkdir Compiled
for f in *.vert *.frag; do
    n=${f%%.*}_${f##*.}
    glslangValidator -V $f -o Compiled/$n.spv
    ./bintoc Compiled/$n.spv ${n}_spv > Compiled/$n.c
done
popd

%install -a
# The client looks for the renderers next to it, so it stays in
# %%{_libdir}/%%{name} and is started from a wrapper
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_libdir}/%{name}/ioq3ded %{buildroot}%{_bindir}/
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/sh
exec %{_libdir}/%{name}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/quake3/baseq3

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
install -Dpm 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -Dpm 0644 misc/quake3.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dpm 0644 misc/linux/org.ioquake3.ioquake3.metainfo.xml \
    %{buildroot}%{_metainfodir}/org.ioquake3.ioquake3.metainfo.xml

%check
appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/org.ioquake3.ioquake3.metainfo.xml

%files
%license COPYING.txt
%doc ChangeLog README.md docs/id-readme.txt docs/opengl2-readme.md
%doc docs/voip-readme.txt docs/vulkan-readme.md
%{_bindir}/%{name}
%{_bindir}/ioq3ded
%{_libdir}/%{name}
%dir %{_datadir}/quake3
%dir %{_datadir}/quake3/baseq3
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/org.ioquake3.ioquake3.metainfo.xml

%changelog
* Thu Nov 05 2026 Trung Le <8@tle.id.au> - 1.36^20261104git52088b9-1
- Initial package of ioquake3 (git 52088b9), built with the system libraries
- Add the ppc64le VM JIT support from upstream PR 860
- Add the Vulkan renderer from upstream PR 861
- Quit from the main loop on SIGTERM and SIGINT
