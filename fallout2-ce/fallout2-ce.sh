#!/bin/sh
# Runs Fallout 2 CE in the user's game directory, $FALLOUT2_CE_DIR or
# ${XDG_DATA_HOME:-~/.local/share}/@NAME@: the game reads its data, and
# writes its configuration and saved games, in its working directory.
# The game directory mirrors the shared data in @DATADIR@: its directories
# are made and its files linked, except configuration files, which are
# copied for the game to change. Files already in the game directory are
# kept, so the game can also be installed there, or point it at an existing
# installation with FALLOUT2_CE_DIR.
datadir=@DATADIR@
gamedir=${FALLOUT2_CE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/@NAME@}

mkdir -p "$gamedir" || exit 1
# Links to shared files that are gone, e.g. after the data was removed
find "$gamedir" -xtype l -lname "$datadir/*" -delete
for f in "$datadir"/*.cfg "$datadir"/*.ini; do
    [ -f "$f" ] && cp -p --update=none "$f" "$gamedir/"
done
cp -rs --update=none "$datadir/." "$gamedir/" || exit 1

if ! ls "$gamedir" | grep -qix master.dat; then
    echo "@NAME@: no Fallout 2 game data in $gamedir: copy the files of your" \
        "copy of the game (master.dat, critter.dat, patch000.dat and the data" \
        "folder) there or to $datadir" >&2
    exit 1
fi

cd "$gamedir" && exec @LIBEXECDIR@/fallout2-ce "$@"
