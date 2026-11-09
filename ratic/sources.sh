#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1. GitLab refuses non-browser downloads of this project's archives, and
# they would hold Git LFS pointers in place of the SVG icons, so make Source0
# from a clone of the release tag with its LFS files. Then vendor the crates
# pinned by upstream's Cargo.lock into Source1, so the RPM builds offline.
# Crates for non-Linux targets are replaced by stubs.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
url=$(rpmspec -q --srpm --qf '%{url}' "$spec")
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")
source0=$(rpmspec -P "$spec" | sed -n 's|^Source0:[[:space:]]*||p')
vendor=$(rpmspec -P "$spec" | sed -n 's|^Source1:[[:space:]]*||p')

dnf -y install cargo cargo-vendor-filterer git-core git-lfs

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git clone --quiet --depth 1 --branch "v$version" "$url.git" "$work/ratic"
git -C "$work/ratic" lfs pull
tar -czf "$specdir/$source0" -C "$work" --exclude=.git --sort=name \
    --owner=0 --group=0 --numeric-owner --mtime=@"$(git -C "$work/ratic" log -1 --format=%ct)" \
    --transform="s|^ratic|ratic-$version|" ratic
cd "$work/ratic"
cargo vendor-filterer --platform='*-unknown-linux-gnu' --tier=2 vendor
tar -cJf "$specdir/$vendor" vendor
