# Fallout 2 game data from your own copy of the game, installed where the
# fallout2-ce launcher looks for it (/usr/share/fallout2-ce, mirrored into
# each user's game directory). The data is not redistributable, so this
# package is built locally, not in COPR. Copy one of these next to this
# spec and build
#
#   rpmbuild -bb --define "_sourcedir $PWD" fallout2-ce-data.spec
#
# - GOG's offline installer, as setup_fallout2.exe (unpacked with
#   innoextract), or
# - a tarball of an installed copy (GOG, Steam or CD), made with
#   tar -C /path/to/the/game -czf fallout2.tar.gz .
#
# The installer is used when both are there. Only the files the engine
# reads are taken: the DAT archives, the data and sound directories, and
# fallout2.cfg, f2_res.ini and ddraw.ini (the engine migrates the high
# resolution patch and sfall settings from the last two). The Windows
# executables and libraries, and GOG's launcher, are left out.

%global gog_installer setup_fallout2.exe
%global with_gog %{lua: print(posix.access(rpm.expand("%{_sourcedir}/%{gog_installer}")) and 1 or 0)}

Name:           fallout2-ce-data
Version:        1.02
Release:        1%{?dist}
Summary:        Fallout 2 game data for fallout2-ce
License:        LicenseRef-Proprietary
URL:            https://www.gog.com/en/game/fallout_2
%if %{with_gog}
Source0:        %{gog_installer}
%else
Source1:        fallout2.tar.gz
%endif

BuildArch:      noarch
%if %{with_gog}
BuildRequires:  innoextract
%endif
# Owns /usr/share/fallout2-ce and mirrors it into the game directory
Requires:       fallout2-ce

%description
The game data of Fallout 2 1.02 (the DAT archives, the data and sound
directories and the game's configuration), packaged from a locally owned
copy of the game for the Fallout 2 CE engine. This package is not
redistributable.

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
# The game directory is the one with master.dat
gamedir=$(find . -iname master.dat -printf '%h\n' | sort | head -n 1)
if [ -z "$gamedir" ]; then
    echo "error: no master.dat in the source; is it a copy of Fallout 2?" >&2
    exit 1
fi
find "$gamedir" -mindepth 1 -maxdepth 1 \( \
    \( -type f \( -iname '*.dat' -o -iname fallout2.cfg \
                  -o -iname f2_res.ini -o -iname ddraw.ini \) \
       -not -iname ce.dat \) \
    -o \( -type d \( -iname data -o -iname sound \) \) \) \
    -printf '%f\0' > game.list
for f in critter.dat patch000.dat fallout2.cfg; do
    if ! grep -qzix "$f" game.list; then
        echo "error: no $f next to master.dat in the source" >&2
        exit 1
    fi
done
# The file list, as the names' case varies between copies of the game
tr '\0' '\n' < game.list | sed 's|.*|"%{_datadir}/fallout2-ce/&"|' > files.list
# The manuals and the licence, if the copy has them
for f in manual.pdf refcard.pdf licence.txt; do
    doc=$(find "$gamedir" -mindepth 1 -maxdepth 1 -type f -iname $f)
    [ -n "$doc" ] || continue
    cp -p "$doc" .
    case $f in
        licence.txt) echo "%%license $(basename "$doc")" ;;
        *) echo "%%doc $(basename "$doc")" ;;
    esac >> files.list
done

%install
install -d %{buildroot}%{_datadir}/fallout2-ce
(cd "$(find . -iname master.dat -printf '%h\n' | sort | head -n 1)" &&
    xargs -0 -a "$OLDPWD/game.list" \
        cp -r --preserve=timestamps -t %{buildroot}%{_datadir}/fallout2-ce)
# The archives can come with odd permissions from installers and CDs
find %{buildroot}%{_datadir}/fallout2-ce -type d -exec chmod 0755 {} +
find %{buildroot}%{_datadir}/fallout2-ce -type f -exec chmod 0644 {} +

%files -f files.list

%changelog
* Wed Nov 18 2026 Trung Lê <8@tle.id.au> - 1.02-1
- Package the DAT archives, the data and sound directories and the
  configuration of a local copy, from GOG's offline installer or an
  installed copy
