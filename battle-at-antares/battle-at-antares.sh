#!/bin/sh
# Runs the Battle at Antares launcher on the user's game directory,
# $ANTARES_GAME_DIR or ${XDG_DATA_HOME:-~/.local/share}/@NAME@: the game reads
# the Master of Orion II files, and writes its configuration and saved games,
# there. The game directory mirrors the game's shared files in @DATADIR@ and,
# with orion2re-data, the Master of Orion II files in @MOO2DIR@: its
# directories are made and its files linked, except configuration files,
# which are copied for the game to change. Files already in the game
# directory are kept, so the Master of Orion II files can also be copied
# there, and HD art and other packages go in its data/mods.
datadir=@DATADIR@
moo2dir=@MOO2DIR@
gamedir=${ANTARES_GAME_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/@NAME@}

mkdir -p "$gamedir/data" || exit 1
# Links to shared files that are gone, e.g. after a package was removed
find "$gamedir" -xtype l \( -lname "$datadir/*" -o -lname "$moo2dir/*" \
    -o -lname "@LIBEXECDIR@/*" \) -delete
cp -p --update=none "$datadir/data/antares.cfg" "$gamedir/data/"
cp -rs --update=none "$datadir/." "$gamedir/" || exit 1
if [ -d "$moo2dir" ]; then
    cp -rs --update=none "$moo2dir/." "$gamedir/" || exit 1
fi
# The launcher starts the game as antares-godot, or antares, in the game
# directory
for exe in antares antares-godot; do
    ln -sfn "@LIBEXECDIR@/$exe" "$gamedir/$exe"
done

if ! ls "$gamedir" | grep -qix mainmenu.lbx; then
    echo "@NAME@: no Master of Orion II files in $gamedir: install" \
        "orion2re-data, built from your copy of the game, or copy the" \
        "game's files (the .LBX files and ORIONCD.INI) there" >&2
    exit 1
fi

exec @LIBEXECDIR@/antares-launcher -game-dir "$gamedir" "$@"
