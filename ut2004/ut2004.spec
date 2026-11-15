# Unreal Tournament 2004 with OldUnreal's patch, installed per user. Epic
# lets OldUnreal host the game, but its terms (the Epic Games Terms of
# Service) give no one else the right to redistribute it, so this package ships
# no part of the game: ut2004 starts it from ~/.local/share/OldUnreal/UT2004,
# running ut2004-installer first if it is not there yet, or not with the
# patch below. The installer downloads the game's DVD image from OldUnreal,
# after the user accepts the Epic Games Terms of Service, unpacks it, and
# applies the patch (the engine, built for x86_64, aarch64 and ppc64le).
#
# ut2004-installer is this package's own, as OldUnreal's installer has no
# license and always applies the latest patch. It does what that does for
# UT2004 with OldUnreal's image, without the desktop entries.
#
# To update to another patch, set patch_tag (the release's tag), patch_file
# and patch_sha256 (from https://github.com/OldUnreal/UT2004Patches/releases,
# the Linux tarball); Version follows patch_tag, with ~ for -.
%global patch_tag 3374-rc3
%global patch_file OldUnreal-UT2004Patch3374-Linux-fc0484d6.tar.bz2
%global patch_sha256 d79eb45fda3ace2b7a68e6a0b9730b7d6602004b111e0b16f3f7cc28f3111572
%global patch_url https://github.com/OldUnreal/UT2004Patches/releases/download/%{patch_tag}/%{patch_file}

Name:           ut2004
Version:        %{lua: print((rpm.expand("%{patch_tag}"):gsub("-", "~")))}
Release:        1%{?dist}
Summary:        Unreal Tournament 2004 launcher and installer
License:        MIT
URL:            https://github.com/OldUnreal/UT2004Patches
Source0:        ut2004
Source1:        ut2004-installer
Source2:        ut2004.desktop

BuildArch:      noarch
# The architectures OldUnreal's UT2004 patch is built for
ExclusiveArch:  x86_64 aarch64 ppc64le noarch

BuildRequires:  desktop-file-utils

# ut2004 and ut2004-installer; the installer runs in a terminal, which
# ut2004 opens when started from the desktop entry
Requires:       bash
Requires:       coreutils
Requires:       curl
Requires:       findutils
Requires:       sed
Requires:       util-linux
Requires:       xdg-terminal-exec
Recommends:     dialog
# Unpacking the image, its cabinets and the patch
Requires:       7zip
Requires:       bzip2
Requires:       tar
Requires:       unshield
# Used by the game in place of the patch's copies, which the installer
# removes
Requires:       SDL3
Requires:       openal-soft

%description
Unreal Tournament 2004, with OldUnreal's patch %{patch_tag}, installed for the
current user on first start.

The game may not be redistributed, so this package does not contain it:
it holds the ut2004 command and its desktop entry, which start the game
from ~/.local/share/OldUnreal/UT2004, and ut2004-installer, which puts it
there. The installer downloads the game (3 GB) and the patch from OldUnreal,
needs 9.5 GB free while it installs, and asks you to accept the Epic Games
Terms of Service, which apply to the game:
https://legal.epicgames.com/en-US/epicgames/tos

Removing this package leaves the game in ~/.local/share/OldUnreal/UT2004,
and its settings in ~/.ut2004; run ut2004-installer --uninstall first to
remove them.

%install
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_bindir}/ut2004
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_bindir}/ut2004-installer
sed -i \
    -e 's|@PATCH_VERSION@|%{patch_tag}|' \
    -e 's|@PATCH_URL@|%{patch_url}|' \
    -e 's|@PATCH_SHA256@|%{patch_sha256}|' \
    %{buildroot}%{_bindir}/ut2004-installer
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE2}

%files
%{_bindir}/ut2004
%{_bindir}/ut2004-installer
%{_datadir}/applications/ut2004.desktop

%changelog
* Sun Nov 15 2026 Trung Lê <8@tle.id.au> - 3374~rc3-1
- Launch Unreal Tournament 2004 from the user's installation, installing
  it, or updating it to OldUnreal's patch 3374-rc3, on first start
