# Master of Orion II game data from your own copy of the game, installed
# where orion2re looks for it (/usr/share/orion2re/game, the orion2re/game
# directory under $XDG_DATA_DIRS). The data is not redistributable, so this
# package is built locally, not in COPR. Copy one of these next to this
# spec and build
#
#   rpmbuild -bb --define "_sourcedir $PWD" orion2re-data.spec
#
# - GOG's offline installer, as setup_master_of_orion_2.exe (unpacked with
#   innoextract), or
# - a tarball of an installed copy (GOG, Steam or CD), made with
#   tar -C /path/to/the/game -czf master_of_orion_2.tar.gz .
#
# The installer is used when both are there. Only the files orion2re reads
# are taken, the LBX archives and ORIONCD.INI (which it requires at
# startup): the DOS and Windows executables and drivers, GOG's DOSBox setup
# and the 1.50 patch (orion2re carries its own as mods) are left out.
#
# For the icon of orion2re's launcher, also copy a square PNG, such as
# 256x256 box art, as orion2re.png; without it the launcher has no icon.
# The icon is artwork of the game, so it is supplied locally too.

%global gog_installer setup_master_of_orion_2.exe
%global with_gog %{lua: print(posix.access(rpm.expand("%{_sourcedir}/%{gog_installer}")) and 1 or 0)}
%global with_icon %{lua: print(posix.access(rpm.expand("%{_sourcedir}/orion2re.png")) and 1 or 0)}

Name:           orion2re-data
Version:        1.31
Release:        1%{?dist}
Summary:        Master of Orion II game data for orion2re
License:        LicenseRef-Proprietary
URL:            https://www.gog.com/en/game/master_of_orion_1_2
%if %{with_gog}
Source0:        %{gog_installer}
%else
Source1:        master_of_orion_2.tar.gz
%endif
%if %{with_icon}
Source2:        orion2re.png
%endif

BuildArch:      noarch
%if %{with_gog}
BuildRequires:  innoextract
%endif
# Owns /usr/share/orion2re and looks for the data in its game directory
Requires:       orion2re
%if %{with_icon}
Requires:       hicolor-icon-theme
%endif

%description
The game data of Master of Orion II 1.31 (the LBX archives and
ORIONCD.INI), packaged from a locally owned copy of the game for the
orion2re engine, and the icon of orion2re's launcher if one was supplied.
This package is not redistributable.

%prep
%setup -q -c -T
%if %{with_gog}
innoextract --silent --exclude-temp %{SOURCE0}
%else
if [ ! -f %{SOURCE1} ]; then
    echo "error: copy GOG's offline installer as %{gog_installer}, or a tarball of an installed copy as $(basename %{SOURCE1}), next to the spec" >&2
    exit 1
fi
tar -xf %{SOURCE1}
%endif
# The game directory is the one with MAINMENU.LBX; the 1.50 patch keeps
# its replacement archives in a subdirectory, which is not taken
gamedir=$(find . -iname MAINMENU.LBX -printf '%h\n' | sort | head -n 1)
if [ -z "$gamedir" ]; then
    echo "error: no MAINMENU.LBX in the source; is it a copy of Master of Orion II?" >&2
    exit 1
fi
find "$gamedir" -maxdepth 1 -type f \( -iname '*.lbx' -o -iname orioncd.ini \) \
    -print0 > game.list
if ! grep -qzi '/orioncd\.ini$' game.list; then
    echo "error: no ORIONCD.INI next to MAINMENU.LBX in the source" >&2
    exit 1
fi

%install
install -d %{buildroot}%{_datadir}/orion2re/game
xargs -0 -a game.list install -pm 0644 -t %{buildroot}%{_datadir}/orion2re/game
%if %{with_icon}
size=$(file -b %{SOURCE2} | sed -n 's/^PNG image data, \([0-9]*\) x \1,.*/\1/p')
if [ -z "$size" ]; then
    echo "error: orion2re.png is not a square PNG image" >&2
    exit 1
fi
install -Dpm 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/orion2re.png
%endif

%files
%{_datadir}/orion2re/game/
%if %{with_icon}
%{_datadir}/icons/hicolor/*/apps/orion2re.png
%endif

%changelog
* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 1.31-1
- Package the LBX archives and ORIONCD.INI of a local copy, from GOG's
  offline installer or an installed copy, and optionally the icon of
  orion2re's launcher
