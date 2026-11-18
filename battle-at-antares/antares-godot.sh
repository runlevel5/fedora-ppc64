#!/bin/sh
# The game with its own interface: the system's Godot with the game's pack,
# run by the launcher in the game directory. The pack loads the game's
# library as bin/libantares.so, relative to the working directory, so Godot
# runs in @LIBDIR@; the game finds the game directory in
# ANTARES_GAME_DIR. The game's options go after "--", where the engine
# leaves them to the game.
export ANTARES_GAME_DIR="${ANTARES_GAME_DIR:-$PWD}"
cd @LIBDIR@ || exit 1
exec /usr/bin/godot --main-pack @DATADIR@/antares-godot.pck -- "$@"
