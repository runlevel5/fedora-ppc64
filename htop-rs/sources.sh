#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: vendor the crates pinned by upstream's Cargo.lock, including the
# ncurses-pure git dependency, into Source1, so the RPM builds offline. Crates
# for non-Linux targets are replaced by stubs.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
name=$(rpmspec -q --qf '%{name}\n' "$spec" | head -1)
version=$(rpmspec -q --qf '%{version}\n' "$spec" | head -1)
source0=$(rpmspec -P "$spec" | sed -n 's|^Source0:.*/||p')
vendor=$(rpmspec -P "$spec" | sed -n 's|^Source1:[[:space:]]*||p')

dnf -y install cargo cargo-vendor-filterer

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
tar -xzf "$specdir/$source0" -C "$work"
cd "$work/$name-$version"
cargo vendor-filterer --platform='*-unknown-linux-gnu' --tier=2 vendor
tar -cJf "$specdir/$vendor" vendor
