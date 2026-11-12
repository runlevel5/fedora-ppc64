#!/bin/sh
# Run by .copr/Makefile, with the spec as $1: make Source0, the source tree at
# the spec's commit without the game's artwork, which is not free (see
# COPYING.md) and so must not end up in the SRPM. Only the code is checked
# out, from a partial clone, so the artwork is not even downloaded. Left out:
# the pk3dirs (maps, models, textures, sounds, music, menus), XTRAS (manual,
# box art), the icons in misc, the prebuilt tools (glslangValidator, unused)
# and the bundled libraries that the system ones replace.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
commit=$(sed -n 's/^%global commit  *\([0-9a-f]\{40\}\)$/\1/p' "$spec")
name=worldofpadman-$commit

command -v git > /dev/null || dnf -y install git-core

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git clone --quiet --filter=blob:none --no-checkout \
    https://github.com/PadWorld-Entertainment/worldofpadman.git "$work/$name"
cd "$work/$name"
git sparse-checkout set --no-cone \
    '/*' \
    '!/wop/*.pk3dir/' \
    '!/xmas/*.pk3dir/' \
    '!/XTRAS/' \
    '!/tools/' \
    '!/misc/*.icns' '!/misc/*.ico' '!/misc/*.svg' \
    '!/misc/*.iconset/' '!/misc/*.winico/' '!/misc/nsis/*.bmp' \
    '!/libs/SDL2/' '!/libs/jpeg-9e/' '!/libs/libogg-*/' '!/libs/libvorbis-*/' \
    '!/libs/libtheora-*/' '!/libs/opus-*/' '!/libs/opusfile-*/' '!/libs/zlib/' \
    '!/libs/libs/'
git checkout --quiet "$commit"
rm -rf .git
cd "$work"
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner \
    -cJf "$specdir/$name-noassets.tar.xz" "$name"
