#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: packs the benchmarks the ppc64le PGO training runs (Speedometer 2.1
# and JetStream 2, from WebKit's PerformanceTests at the release tag) into
# Source3, so the RPM builds offline.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")
training=$(rpmspec -P "$spec" | sed -n 's|^Source3:[[:space:]]*||p')
[ -f "$specdir/$training" ] && exit 0

dnf -y install git-core

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git -C "$work" init -q webkit
cd "$work/webkit"
git sparse-checkout set --no-cone /PerformanceTests/Speedometer2.1/ /PerformanceTests/JetStream2/
git fetch -q --depth 1 --filter=blob:none https://github.com/WebKit/WebKit.git "refs/tags/webkitgtk-$version"
git checkout -q FETCH_HEAD
tar -cJf "$specdir/$training" --owner=0 --group=0 --transform "s|^PerformanceTests|${training%.tar.xz}|" \
    PerformanceTests/Speedometer2.1 PerformanceTests/JetStream2
