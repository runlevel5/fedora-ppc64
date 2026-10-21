Name:    dosbox-staging
Version: 0.83.0
Release: 1%{?dist}
Summary: Modern continuation of DOSBox with advanced features
URL:     https://www.dosbox-staging.org/

# Bundled dependencies bring their licenses with them.
# Breakdown is given here.
#
# src/libs/decoders/std.h is another bundled dependency,
# but apparently not used.
# It is removed in %%prep to be sure.
#
# Main license:      GPL-2.0-or-later
# archive:           Unlicense
# dr_libs:           MIT-0 OR Unlicense
# enet:              MIT
# gulrak-filesystem: MIT
# src/libs/gui_tk:   GPL-3.0-or-later
# libsidplayfp:      GPL-2.0-or-later
# src/lib/loguru:    LicenseRef-Fedora-Public-Domain
# src/lib/ppscale:   Fair
# src/lib/nuked:     LGPL-2.1-or-later
# stb_vorbis:        MIT OR Unlicense
# src/libs/whereami: MIT OR WTFPL
# xxhash.h:          BSD-2-Clause
License: GPL-2.0-or-later AND Unlicense AND (MIT-0 OR Unlicense) AND MIT AND GPL-3.0-or-later AND LicenseRef-Fedora-Public-Domain AND Fair AND LGPL-2.1-or-later AND (MIT OR Unlicense) AND (MIT OR WTFPL) AND BSD-2-Clause

Source: https://github.com/dosbox-staging/dosbox-staging/archive/v%{version}/%{name}-%{version}.tar.gz
# ppc64le: dynamic recompiler (dynrec) backend, from
# https://github.com/runlevel5/dosbox-staging-ppc64/releases/tag/v%{version}-ppc64le
Patch:  dosbox-staging-%{version}-ppc64le.patch
# This package is a drop-in replacement for dosbox
Provides:  dosbox = %{version}-%{release}

BuildRequires: alsa-lib-devel
BuildRequires: asio-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: fluidsynth-devel >= 2.0
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: iir1-devel
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libpng-devel
BuildRequires: libslirp-devel
BuildRequires: libXi-devel
BuildRequires: make
BuildRequires: mt32emu-devel
BuildRequires: opusfile-devel
BuildRequires: pkgconfig(gl)
BuildRequires: SDL2_image-devel
BuildRequires: SDL2-devel >= 2.0.5
BuildRequires: speexdsp-devel
BuildRequires: zlib-ng-devel

Requires: hicolor-icon-theme
Requires: fluid-soundfont-gm

# Some libraries are loaded at runtime, see rhbz#2176658
Requires: libEGL

# src/lib/enet
# Based on fork github.com/lsalzman/enet
Provides: bundled(enet)
# src/lib/ghc
Provides: bundled(gulrak-filesystem)
# src/lib/gui_tk
# Not in Fedora, upstream seems to have disappeared completely
Provides: bundled(gui_tk)
# src/lib/loguru
# Not in Fedora, upstream https://github.com/emilk/loguru
Provides: bundled(loguru)
# src/lib/nuked
# Not in Fedora, upstream https://github.com/nukeykt/Nuked-OPL3
Provides: bundled(nuked-opl3)
# src/lib/residfp
# Not the whole library, just the residfp part
Provides: bundled(libsidplayfp)
# src/lib/whereami
# Not in Fedora, upstream https://github.com/gpakosz/whereami
Provides: bundled(gpakosz-whereami)
# src/lib/decoders/archive.h
# Not in Fedora, upstream github.com/voidah/archive
Provides: bundled(archive)
# src/lib/decoders/dr_{flac,mp3,wav}.h
Provides: bundled(dr_libs)
# src/lib/decoders/stb_vorbis.h
Provides: bundled(stb_vorbis)
# src/lib/decoders/xxhash.h
Provides: bundled(xxhash)

# Automated Tests in Bodhi failed the textrel test for i686, see
# https://sourceware.org/annobin/annobin.html/Test-textrel.html
ExcludeArch: %{ix86}

%global with_ctest 1
BuildSystem: cmake
BuildOption: -DCMAKE_SKIP_RPATH:BOOL=TRUE
BuildOption: --preset=release-linux
BuildOption(build): --preset=release-linux
BuildOption(check): --preset=release-linux

%description
DOSBox Staging is a modern continuation of DOSBox with advanced features and
current development practices.

It is a (mostly) drop-in replacement for older DOSBox versions — your existing
configurations will continue to work, and you will have access to many advanced
features.

DOSBox Staging comes with sensible defaults, so you’ll need to write a lot less
configuration than with older DOSBox versions. Most games and applications
require no tweaking and will work fine with the stock settings. However, the
extensive configuration options and advanced features are available if you wish
to delve deeper.

%prep
%autosetup -C -p1
# Remove unused file
rm src/libs/decoders/stb.h

%install -a
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
mv %{buildroot}%{_datadir}/doc/%{name}/{licenses/*,LICENSE} %{buildroot}%{_datadir}/licenses/%{name}/
rmdir %{buildroot}%{_datadir}/doc/%{name}/licenses

mv %{buildroot}%{_datadir}/%{name}/resources/* %{buildroot}%{_datadir}/%{name}/
rmdir %{buildroot}%{_datadir}/%{name}/resources

%check -a
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml

%files
%license %{_datadir}/licenses/%{name}/*
%doc docs/AUTHORS README.md docs/THANKS docs/DOCUMENTATION.md
%{_bindir}/dosbox
%{_mandir}/man1/dosbox.*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/org.dosbox_staging.*
%{_metainfodir}/*

%changelog
* Thu Oct 22 2026 Trung Le <8@tle.id.au> - 0.83.0-1
- Based on Fedora's dosbox-staging, with the 0.83.0 update from
  src.fedoraproject.org/forks/lnvso/rpms/dosbox-staging (033807f)
- Add the ppc64le dynamic recompiler backend
