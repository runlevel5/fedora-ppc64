# ARMA: Cold War Assault Remastered game data from your own copy of the GOG
# release, installed where the cwr-ce package looks for it
# (/usr/share/cwr-ce). The data is not redistributable, so this package is
# built locally, not in COPR: copy GOG's offline installer next to this spec
# as setup_arma_cold_war_assault.exe and build
#
#   rpmbuild -bb --define "_sourcedir $PWD" cwr-ce-data.spec
#
# The installer is unpacked with innoextract; only the Remastered folder is
# taken (GOG's Windows and x64 Linux binaries in it are left out), plus the
# manual. The version is the date of the Remastered release's files.

%global gog_game_id 1207658661

Name:           cwr-ce-data
Version:        20260829
Release:        1%{?dist}
Summary:        ARMA: Cold War Assault Remastered game data
# Bohemia Interactive's game data:             LicenseRef-Proprietary
# fonts/ (Source Sans, Serif and Code Pro):    OFL-1.1
License:        LicenseRef-Proprietary AND OFL-1.1
URL:            https://www.gog.com/en/game/arma_cold_war_assault
Source0:        setup_arma_cold_war_assault.exe

BuildArch:      noarch
BuildRequires:  innoextract
# Owns /usr/share/cwr-ce and looks for the data there
Requires:       cwr-ce

%description
The game data of ARMA: Cold War Assault Remastered (models, textures,
sounds, music, voices, islands, campaigns, missions and the remastered
interface), packaged from a locally owned copy of the GOG release for the
cwr-ce engine, with the game's manual. This package is not
redistributable.

%prep
if [ ! -f %{SOURCE0} ]; then
    echo "error: copy GOG's offline installer next to the spec as $(basename %{SOURCE0})" >&2
    exit 1
fi
id=$(innoextract --gog-game-id %{SOURCE0} | sed -n 's/^GOG.com game ID is //p')
if [ "$id" != %{gog_game_id} ]; then
    echo "error: $(basename %{SOURCE0}) is not the GOG installer of the game (game ID '$id', not %{gog_game_id})" >&2
    exit 1
fi
%setup -q -c -T
innoextract --silent --exclude-temp \
    --include Remastered --include ArmaCWA_manUK.pdf %{SOURCE0}
# The Windows binaries, OpenAL for Windows and GOG's x64 Linux builds of
# the engine
rm Remastered/*.exe Remastered/*.dll Remastered/OpenAL-Soft-LGPL.txt \
    Remastered/PoseidonGame Remastered/PoseidonServer
mv Remastered/fonts/OFL.txt .

%install
mkdir -p %{buildroot}%{_datadir}/cwr-ce
cp -pr Remastered/. %{buildroot}%{_datadir}/cwr-ce/

%files
%license OFL.txt
%doc ArmaCWA_manUK.pdf
%{_datadir}/cwr-ce/AddOns
%{_datadir}/cwr-ce/BIN
%{_datadir}/cwr-ce/Campaigns
%{_datadir}/cwr-ce/DTA
%{_datadir}/cwr-ce/dtaExt
%{_datadir}/cwr-ce/fonts
%{_datadir}/cwr-ce/Missions
%{_datadir}/cwr-ce/MPMissions
%{_datadir}/cwr-ce/SPTemplates
%{_datadir}/cwr-ce/Templates
%{_datadir}/cwr-ce/Worlds

%changelog
* Tue Nov 17 2026 Trung Lê <8@tle.id.au> - 20260829-1
- Package the Remastered data of a local copy of the GOG release
