%global commit      d9d35a3f66bd16b1f8aba8bb08a1a6b9b13cb682
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20261102

Name:           worldofpadman
Version:        1.7.1~%{commitdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        World of PADMAN game engine

# Main license:                                GPL-2.0-or-later
# code/qcommon/{unzip,ioapi}.c (minizip):      Zlib
# code/renderercommon/puff.c:                  Zlib
# code/client/libmumblelink.c:                 Zlib
# libs/backward (backward-cpp):                MIT
# code/qcommon/md5.c:                          LicenseRef-Fedora-Public-Domain
License:        GPL-2.0-or-later AND Zlib AND MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://worldofpadman.net/
# Made by sources.sh from https://github.com/PadWorld-Entertainment/worldofpadman
# at %%{commit}, without the game's artwork, which is not free
Source0:        %{name}-%{commit}-noassets.tar.xz
# ppc64le and ppc64 support for the VM JIT (vm_powerpc.c, from ioquake3 with
# its ppc64le work), VSX renderer and sound paths, and fixes for building on
# big-endian ppc64
# https://github.com/runlevel5/worldofpadman/commit/65e11767
Patch:          %{name}-ppc64-jit.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(zlib)

# HTTP downloads dlopen() libcurl.so.4
Requires:       libcurl%{?_isa}
Provides:       bundled(backward-cpp)

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE=Release
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name}
BuildOption:    -DDEFAULT_BASEDIR=%{_datadir}/%{name}
BuildOption:    -DUSE_INTERNAL_LIBS=OFF
BuildOption:    -DUSE_OPENAL_DLOPEN=OFF

%description
World of PADMAN is a cartoon-style fun shooter, built on
ioquake3. This package contains the engine (worldofpadman) and the
dedicated server (wopded), with a JIT compiler for the game modules (QVMs)
on ppc64le and ppc64 as well as x86 and ARM.

It contains no game data, which is not free (non-commercial use only) and
so is packaged separately: build the worldofpadman-data package from the
spec next to this one, or put the wop/*.pk3 and wop/*.cfg files of the
World of PADMAN 1.7.0 release in /usr/share/worldofpadman/wop. The game
modules come with the data, in wop_vm_1.7.0.pk3.

%prep
%autosetup -n %{name}-%{commit} -p1
# The bundled lcc stays: it compiles the test QVMs for %%check. Its licence
# forbids selling it, but it is a build tool only and nothing of it is
# shipped.

%install -a
# The client looks for the renderers next to it, so it stays in
# %%{_libdir}/%%{name} and is started from a wrapper. The binaries are named
# after the architecture (wop.ppc64le, wopded.ppc64le, ...).
cd %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mv wopded.* %{buildroot}%{_bindir}/wopded
client=$(echo wop.*)
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
exec %{_libdir}/%{name}/$client "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}
# The map compiler is a mapping tool, not part of the game
rm wopbspc.*
# The game modules come with the data, in wop_vm_1.7.0.pk3: pure servers,
# including local games, only load them from the pk3 the server has, so
# the native ones and the loose QVMs installed here are not shipped
rm -r wop

%check
# The VM tests run their QVMs through the interpreter and the JIT
%ctest -R woptest-vm

%files
%license COPYING.md GPL-2.0.md
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_bindir}/wopded
%{_libdir}/%{name}

%changelog
* Fri Nov 13 2026 Trung Lê <8@tle.id.au> - 1.7.1~20261102gitd9d35a3-1
- Initial package of the World of PADMAN engine (git d9d35a3), built with the
  system libraries, from a source tree without the game's artwork
- Add ppc64le and ppc64 support for the VM JIT
