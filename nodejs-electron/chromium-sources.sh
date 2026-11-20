#!/bin/bash
# chromium-sources.sh - Generate Chromium source tarball for nodejs-electron
#
# This script generates a Chromium lite tarball from the upstream chromium-tarballs
# project. The lite tarball is significantly smaller (~1.5GB vs ~5GB) as it removes:
# - Mobile platforms (android, ios, chromecast)
# - Test data and some test sources
# - Bundled toolchains
# - Build infrastructure
#
# The electron-lite-excludes.patch allows Electron's patch application to gracefully
# skip hunks that modify files removed from the lite tarball, making this approach
# sustainable without maintaining a custom patch queue.
#
# Usage: ./chromium-sources.sh [version]
# Example: ./chromium-sources.sh 156.0.8078.75

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARBALLS_REPO="chromium-tarballs"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: $0 [chromium-version]"
            echo ""
            echo "Generates a Chromium lite tarball using upstream chromium-tarballs."
            echo "The lite tarball removes mobile platforms, test data, and toolchains."
            echo "electron-lite-excludes.patch allows Electron patches to skip removed files."
            echo ""
            echo "If no version is specified, reads chromium_version from nodejs-electron.spec."
            echo ""
            echo "Example: $0 156.0.8078.75"
            exit 0
            ;;
        *)
            VERSION="$1"
            shift
            ;;
    esac
done

# Default to version from spec if not provided
if [ -z "${VERSION:-}" ]; then
    VERSION=$(grep -oP '(?<=%global chromium_version )\S+' "${SCRIPT_DIR}/nodejs-electron.spec" 2>/dev/null | head -1 || true)
fi

if [ -z "${VERSION:-}" ]; then
    echo "ERROR: No version specified and could not determine chromium_version from nodejs-electron.spec" >&2
    echo "Usage: $0 [chromium-version]"
    echo "Example: $0 156.0.8078.75"
    exit 1
fi

echo "=== Fetching Chromium $VERSION using chromium-tarballs process ==="
echo "Type: Lite tarball (mobile/test data removed, ~1.5GB)"
echo

# Step 1: Ensure chromium-tarballs repo exists
if [ ! -d "$SCRIPT_DIR/$TARBALLS_REPO" ]; then
    echo "Cloning chromium-tarballs repository..."
    git clone https://github.com/gordonmessmer/chromium-tarballs.git "$SCRIPT_DIR/$TARBALLS_REPO"
else
    echo "✓ chromium-tarballs repository already exists"
    echo "  Updating to latest version..."
    pushd "$SCRIPT_DIR/$TARBALLS_REPO" >/dev/null
    git pull --quiet origin clean-hook-only || echo "  (pull failed, using existing version)"
    popd >/dev/null
fi

echo

# Step 2: Create working directory
WORK_DIR="$SCRIPT_DIR/chromium-tarball-build"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "Working directory: $WORK_DIR"
echo

# Step 3: Set up CLEAN_HOOK to remove proprietary content
# chromium-tarballs will call this before creating tarballs
echo "Configuring Fedora clean hook..."

if [ ! -f "$SCRIPT_DIR/$TARBALLS_REPO/fedora-clean-hook.sh" ]; then
    echo "ERROR: fedora-clean-hook.sh not found in $TARBALLS_REPO"
    exit 1
fi

export CLEAN_HOOK="$SCRIPT_DIR/$TARBALLS_REPO/fedora-clean-hook.sh"

echo "✓ CLEAN_HOOK configured (will remove prebuilt binaries/toolchains/codecs)"
echo

# Step 4: Run chromium-tarballs's package_chromium.sh
# This will:
# - Clone depot_tools and build repositories (cached after first run)
# - Configure gclient with @version for optimized fetching
# - Sync Chromium sources with --no-history
# - Run necessary hooks (PGO profiles, etc.)
# - Call CLEAN_HOOK to remove proprietary codecs
# - Export lite tarball (default, no GENERATE_ALL needed)

echo "Running chromium-tarballs package_chromium.sh..."
echo "Generating standard LITE source tarball"
echo "  (Mobile/test data/toolchains removed)"
echo "This will take a while on first run (downloads source)"
echo "Subsequent runs will be faster (depot_tools/build cached)"
echo

"$SCRIPT_DIR/$TARBALLS_REPO/package_chromium.sh" "$VERSION"

# Step 5: Move the generated tarball to package directory
UPSTREAM_TARBALL="out/chromium-${VERSION}-linux.tar.xz"
UPSTREAM_HASHES="out/chromium-${VERSION}-linux.tar.xz.hashes"

if [ ! -f "$UPSTREAM_TARBALL" ]; then
    echo "ERROR: Expected tarball not found: $UPSTREAM_TARBALL"
    echo "Generated files:"
    ls -lh out/chromium-${VERSION}-*.tar.xz 2>/dev/null || echo "  No tarballs found"
    exit 1
fi

echo
echo "=== Moving tarball to package directory ==="

# chromium-tarballs names it chromium-X-linux.tar.xz
# We need chromium-X-clean.tar.xz for compatibility with our spec
mv "$UPSTREAM_TARBALL" "$SCRIPT_DIR/chromium-${VERSION}-clean.tar.xz"

echo "✓ Created: chromium-${VERSION}-clean.tar.xz (lite tarball)"
echo "  Size: $(du -h "$SCRIPT_DIR/chromium-${VERSION}-clean.tar.xz" | cut -f1)"
echo "  electron-lite-excludes.patch will skip hunks for removed files"
echo

# Also move the hashes file if it exists
if [ -f "$UPSTREAM_HASHES" ]; then
    mv "$UPSTREAM_HASHES" \
       "$SCRIPT_DIR/chromium-${VERSION}-clean.tar.xz.hashes"
    echo "✓ Hash file moved"
fi

echo
echo "=== Done! ==="
echo "Tarball: $SCRIPT_DIR/chromium-${VERSION}-clean.tar.xz"
echo
echo "Working directory preserved at: $WORK_DIR"
echo "  depot_tools/ and build/ are cached for future runs"
echo "  To clean: rm -rf $WORK_DIR"
echo
echo "To use in nodejs-electron package:"
echo "  1. Move chromium-${VERSION}-clean.tar.xz to package directory"
echo "  2. Update sources file: sha512sum *.tar.* > sources"
