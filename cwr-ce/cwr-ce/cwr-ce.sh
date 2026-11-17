#!/bin/sh
# Runs @BINARY@ on the game data in @DATADIR@ (the cwr-ce-data package),
# unless a data directory is given with -C or --work-dir
for arg in "$@"; do
    case $arg in
        -C*|--work-dir|--work-dir=*) exec @LIBEXECDIR@/@BINARY@ "$@" ;;
    esac
done
exec @LIBEXECDIR@/@BINARY@ -C @DATADIR@ "$@"
