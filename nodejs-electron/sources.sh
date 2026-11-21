#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: download the parts of the Chromium tarball (Source0) from the release
# holding the other generated sources (Source20), join them and check the
# result against the sources file.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
parsed=$(rpmspec -P "$spec")
tarball=$(echo "$parsed" | sed -n 's/^Source0:[[:space:]]*//p')
url=$(echo "$parsed" | sed -n 's/^Source20:[[:space:]]*//p')
url=${url%/*}

cd "$specdir"
check() { grep -F "($tarball)" sources | sha512sum -c - >/dev/null 2>&1; }
check && exit 0

command -v curl >/dev/null || dnf -y install curl
: > "$tarball"
part=0
while curl -sSfL --retry 3 -o "$tarball.part" "$url/$tarball.part$part"; do
  cat "$tarball.part" >> "$tarball"
  part=$((part + 1))
done 2>/dev/null
rm -f "$tarball.part"
check || { echo "sources.sh: $tarball does not match the sources file ($part parts)" >&2; exit 1; }
echo "sources.sh: wrote $specdir/$tarball ($part parts)"
