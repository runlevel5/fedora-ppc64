#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: vendor the crates pinned by upstream's Cargo.lock into Source1, so the
# RPM builds offline. Crates for non-Linux targets are replaced by stubs.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
source0=$(rpmspec -P "$spec" | sed -n 's|^Source0:.*#/||p')
vendor=$(rpmspec -P "$spec" | sed -n 's|^Source1:[[:space:]]*||p')

dnf -y install cargo cargo-vendor-filterer

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
tar -xzf "$specdir/$source0" -C "$work"
cd "$work/ripples"
cargo vendor-filterer --platform='*-unknown-linux-gnu' --tier=2 vendor
tar -cJf "$specdir/$vendor" vendor
