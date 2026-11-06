#!/bin/bash
# Generate the langpack tarball next to the spec from Mozilla's release
# directory: firefox-esr-langpacks-<version>esr.tar.xz holding
# firefox-langpacks/<locale>.xpi for every locale except en-US.
# FIREFOX_ESR_XPI_URL overrides the xpi directory (e.g. a candidates build).
set -euo pipefail
spec=$1
dir=$(cd "$(dirname "$spec")" && pwd)
ver=$(sed -n 's/^Version:[[:space:]]*//p' "$spec" | head -n 1)esr
out=$dir/firefox-esr-langpacks-$ver.tar.xz
[ -s "$out" ] && exit 0
url=${FIREFOX_ESR_XPI_URL:-https://archive.mozilla.org/pub/firefox/releases/$ver/linux-x86_64/xpi/}
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/firefox-langpacks"
curl -sSfL "$url" | grep -o 'href="[^"]*\.xpi"' | sed -e 's/^href="//' -e 's/"$//' -e 's|.*/||' | grep -v '^en-US\.xpi$' | sort -u > "$tmp/list"
[ -s "$tmp/list" ] || { echo "sources.sh: no langpacks found at $url" >&2; exit 1; }
while read -r xpi; do
  curl -sSfL -o "$tmp/firefox-langpacks/$xpi" "$url$xpi"
done < "$tmp/list"
tar -C "$tmp" -cJf "$out" firefox-langpacks
echo "sources.sh: wrote $out ($(wc -l < "$tmp/list") langpacks)"
