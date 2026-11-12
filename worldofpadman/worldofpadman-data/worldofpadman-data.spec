# World of PADMAN game data, from the official release, installed where the
# worldofpadman package looks for it (/usr/share/worldofpadman). The data may
# be copied and distributed for non-commercial purposes only (see
# COPYING.md and LICENSES.md), which rules it out of Fedora and COPR, so
# this package is built locally: fetch the release zip next to this spec and
# build
#
#   spectool -g worldofpadman-data.spec
#   rpmbuild -bb --define "_sourcedir $PWD" worldofpadman-data.spec
#
# The pk3 files are shipped exactly as released, so that their checksums
# match those of pure servers running 1.7.0, and because some of the music
# (CC-BY-NC-ND) may not be modified. They include the game modules
# (wop_vm_1.7.0.pk3).

Name:           worldofpadman-data
Version:        1.7.0
Release:        1%{?dist}
Summary:        World of PADMAN game data
# PadWorld Entertainment's own artwork:        LicenseRef-WorldofPadman
#   (COPYING.md: non-commercial copying, distribution and presentation)
# Third-party content, listed in LICENSES.md:  CC-BY-3.0, CC-BY-NC-3.0,
#   CC-BY-NC-ND-4.0, CC-BY-NC-SA-4.0, CC0-1.0, CC Sampling+ 1.0, and the
#   terms of use of Sound Jay and PacDV (sound effects)
License:        LicenseRef-WorldofPadman AND CC-BY-3.0 AND CC-BY-NC-3.0 AND CC-BY-NC-ND-4.0 AND CC-BY-NC-SA-4.0 AND CC0-1.0 AND LicenseRef-CC-Sampling-Plus-1.0 AND LicenseRef-SoundJay AND LicenseRef-PacDV
URL:            https://worldofpadman.net/
Source0:        https://github.com/PadWorld-Entertainment/worldofpadman/releases/download/v%{version}/wop-%{version}-unified.zip
# Based on upstream's misc/linux/wop.desktop.in
Source1:        worldofpadman.desktop

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  unzip
# Looks for the data in /usr/share/worldofpadman
Requires:       worldofpadman
Requires:       hicolor-icon-theme

%description
The game data of World of PADMAN %{version} (maps, models, textures,
sounds, music and menus) and its game modules, for the worldofpadman
engine, with the desktop entry and the HTML manual.

The data may be copied and distributed for non-commercial purposes only;
see COPYING.md and LICENSES.md.

%prep
%setup -q -c -T
# The release zip holds the binaries of every platform as well; only the
# data and documents are taken
unzip -q %{SOURCE0} 'wop/*.pk3' 'wop/*.cfg' \
    COPYING.md LICENSES.md README.md CHANGELOG.md \
    XTRAS/wop.svg XTRAS/readme.html 'XTRAS/readme/*'
# The zip's directories are group-writable
chmod -R u=rwX,go=rX .
sed -i 's/\r$//' CHANGELOG.md README.md XTRAS/readme/readme.css

%install
install -Dpm 0644 -t %{buildroot}%{_datadir}/worldofpadman/wop wop/*.pk3 wop/*.cfg
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
install -Dpm 0644 XTRAS/wop.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/worldofpadman.svg

%files
%license COPYING.md LICENSES.md
%doc CHANGELOG.md README.md XTRAS/readme.html XTRAS/readme
%dir %{_datadir}/worldofpadman
%{_datadir}/worldofpadman/wop
%{_datadir}/applications/worldofpadman.desktop
%{_datadir}/icons/hicolor/scalable/apps/worldofpadman.svg

%changelog
* Fri Nov 13 2026 Trung Lê <8@tle.id.au> - 1.7.0-1
- Package the data of the World of PADMAN 1.7.0 release
