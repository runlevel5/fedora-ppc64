#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: vendor the crates pinned by upstream's Cargo.lock into Source1, so the
# RPM builds offline. Crates for non-Linux targets are replaced by stubs.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")

dnf -y install cargo cargo-vendor-filterer

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
tar -xzf "$specdir/amberol-$version.tar.gz" -C "$work"
cd "$work/amberol-$version"
cargo vendor-filterer --platform='*-unknown-linux-gnu' --tier=2 vendor
tar -cJf "$specdir/amberol-$version-vendor.tar.xz" vendor
