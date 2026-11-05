%global commit      52088b9eae247d8e321c8dc1fb49a879652854f9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261104

Name:           ioquake3
Version:        1.36^%{commitdate}git%{shortcommit}
Release:        4%{?dist}
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
# Vulkan renderer from vkQuake3, and a Graphics API spinner (OpenGL 1, OpenGL 2,
# Vulkan) in place of the GL Driver one in the System menu
# https://github.com/ioquake/ioq3/pull/861 (b5c48d39), the PR's diff without
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
BuildRequires:  zip

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
# The game modules are built as QVMs, with the bundled lcc (see %%prep)
BuildOption:    -DBUILD_GAME_LIBRARIES=OFF
BuildOption:    -DBUILD_GAME_QVMS=ON

%description
ioquake3 is a free and open-source first person shooter engine based on the
Quake III Arena and Quake III: Team Arena source code, with bug and security
fixes, SDL 2, OpenAL and Ogg Vorbis/Opus audio, VoIP, IPv6, HTTP downloads
and OpenGL 2 and Vulkan renderers (cl_renderer opengl2, the default, or
vulkan).

This package contains the engine (ioquake3), the dedicated server (ioq3ded)
and ioquake3's game modules (QVMs) in zz-ioquake3-qvms.pk3, whose System
menu has a Graphics API setting to choose the renderer. It contains no game data:
to play Quake III Arena, copy the pak?.pk3 files of the original game to
/usr/share/quake3/baseq3 (see the quake3-data spec). Files under
~/.local/share/Quake3/baseq3 take precedence over /usr/share/quake3/baseq3,
so if the game data lives there, copy or symlink zz-ioquake3-qvms.pk3 next
to it, or the menus come from pak8. On pure servers the server's game
modules are used, as always.

%prep
%autosetup -n ioq3-%{commit} -p1
# Bundled libraries (the system ones are used). The bundled lcc stays: it
# compiles the game modules to QVM bytecode. Its licence forbids selling it,
# which rules it out of Fedora itself, but it is a build tool only and
# nothing of it is shipped.
rm -r code/thirdparty

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

# The game modules go in a pk3 in the data directory, named to sort after
# pak8.pk3 so that it takes precedence; loose vm/*.qvm files would be
# ignored in pure games, including local ones (sv_pure defaults to 1)
for d in baseq3 missionpack; do
    mkdir -p %{buildroot}%{_datadir}/quake3/$d
    (cd %{buildroot}%{_libdir}/%{name}/$d && \
        zip -X -D -9 -r %{buildroot}%{_datadir}/quake3/$d/zz-ioquake3-qvms.pk3 vm)
    rm -r %{buildroot}%{_libdir}/%{name}/$d
done

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
%{_datadir}/quake3/baseq3/zz-ioquake3-qvms.pk3
%dir %{_datadir}/quake3/missionpack
%{_datadir}/quake3/missionpack/zz-ioquake3-qvms.pk3
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/org.ioquake3.ioquake3.metainfo.xml

%changelog
* Fri Nov 06 2026 Trung Le <8@tle.id.au> - 1.36^20261104git52088b9-4
- Update the Vulkan renderer patch to PR 861 at b5c48d39: the GFX API setting
  in the System menu is now called Graphics API

* Thu Nov 05 2026 Trung Le <8@tle.id.au> - 1.36^20261104git52088b9-3
- Build and ship the game modules (QVMs) as /usr/share/quake3/*/zz-ioquake3-qvms.pk3
- Update the Vulkan renderer patch to PR 861 at d8945897, which replaces the
  GL Driver setting in the System menu with GFX API (OpenGL 1, OpenGL 2 or
  Vulkan)

* Thu Nov 05 2026 Trung Le <8@tle.id.au> - 1.36^20261104git52088b9-2
- Update the Vulkan renderer patch to PR 861 at 9faee827

* Thu Nov 05 2026 Trung Le <8@tle.id.au> - 1.36^20261104git52088b9-1
- Initial package of ioquake3 (git 52088b9), built with the system libraries
- Add the ppc64le VM JIT support from upstream PR 860
- Add the Vulkan renderer from upstream PR 861
- Quit from the main loop on SIGTERM and SIGINT
