#!/bin/bash
# shellcheck disable=2181
#
# Create the Electron overlay source tarball.
#
# This produces a tarball containing only Electron-specific sources
# (electron, node, nan, node_modules, yarn deps) that are extracted
# on top of the Chromium source tree during %prep.
#
# The Chromium source comes separately from the chromium package.
#
# dnf install git-core nodejs tar zstd curl python3

set -euo pipefail

missing=()
for cmd in git python3 curl tar zstd node base64 rpm; do
    command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
done
if [ ${#missing[@]} -gt 0 ]; then
    echo "ERROR: missing required tools: ${missing[*]}" >&2
    echo "Install with: dnf install git-core python3 curl tar zstd nodejs coreutils rpm" >&2
    exit 1
fi

# With no argument, take the version from the spec file; an explicit argument
# still overrides it.
if [ "$#" -ge 1 ]; then
    ELECTRON_VERSION="$1"
else
    ELECTRON_VERSION="$(rpm --specfile nodejs-electron.spec --qf '%{VERSION}\n' | head -n1)"
    if [ -z "$ELECTRON_VERSION" ]; then
        echo "ERROR: could not determine version from nodejs-electron.spec" >&2
        echo "Usage: $0 [electron-version]" >&2
        exit 1
    fi
fi
ELECTRON_PKGDIR="$(pwd)"
ELECTRON_TMPDIR="$(mktemp --tmpdir -d electron-overlay-XXXXXXXX)"

echo "ELECTRON VERSION: $ELECTRON_VERSION"
echo "TMPDIR:           $ELECTRON_TMPDIR"

cleanup_tmpdir() {
    popd 2>/dev/null || true
    rm -rf "$ELECTRON_TMPDIR"
}
trap cleanup_tmpdir SIGINT

cleanup_and_exit() {
    cleanup_tmpdir
    if test "$1" = 0 -o -z "$1" ; then
        exit 0
    else
        exit "$1"
    fi
}

pushd "$ELECTRON_TMPDIR" || cleanup_and_exit 1

# === Phase 1: Clone Electron and read pinned versions ===
echo ">>>>>> Cloning Electron v${ELECTRON_VERSION}"
git clone --depth=1 --branch=v"${ELECTRON_VERSION}" \
    https://github.com/electron/electron electron
if [ $? -ne 0 ]; then
    echo "ERROR: git clone electron failed"
    cleanup_and_exit 1
fi

CHROMIUM_VERSION=$(python3 -c "
import ast, re
with open('electron/DEPS') as f:
    content = f.read()
m = re.search(r\"vars\s*=\s*(\{.*?\n\})\", content, re.DOTALL)
vars_dict = ast.literal_eval(m.group(1))
print(vars_dict['chromium_version'])
")
NODE_VERSION=$(python3 -c "
import ast, re
with open('electron/DEPS') as f:
    content = f.read()
m = re.search(r\"vars\s*=\s*(\{.*?\n\})\", content, re.DOTALL)
vars_dict = ast.literal_eval(m.group(1))
print(vars_dict['node_version'])
")
NAN_VERSION=$(python3 -c "
import ast, re
with open('electron/DEPS') as f:
    content = f.read()
m = re.search(r\"vars\s*=\s*(\{.*?\n\})\", content, re.DOTALL)
vars_dict = ast.literal_eval(m.group(1))
print(vars_dict['nan_version'])
")

echo "Chromium version: $CHROMIUM_VERSION"
echo "Node version:     $NODE_VERSION"
echo "NAN version:      $NAN_VERSION"

# === Phase 2: Clone Node.js and NAN ===
echo ">>>>>> Cloning Node.js ${NODE_VERSION}"
git clone --depth=1 --branch="${NODE_VERSION}" \
    https://github.com/nodejs/node.git third_party/electron_node
if [ $? -ne 0 ]; then
    echo "ERROR: git clone node failed"
    cleanup_and_exit 1
fi

echo ">>>>>> Cloning NAN ${NAN_VERSION}"
git clone https://github.com/nodejs/nan.git third_party/nan
(cd third_party/nan && git checkout "${NAN_VERSION}")

# === Phase 3: Install Electron's yarn dependencies ===
echo ">>>>>> Installing Electron node modules"
pushd electron || cleanup_and_exit 1
if [ -f .yarnrc.yml ]; then
    node .yarn/releases/yarn-*.cjs install --immutable --mode=skip-build
else
    yarn install --frozen-lockfile --ignore-engines --ignore-platform --ignore-scripts --link-duplicates
fi
if [ $? -ne 0 ]; then
    echo "ERROR: yarn install failed"
    cleanup_and_exit 1
fi
popd || cleanup_and_exit 1

# === Phase 4: Download Chromium's node_modules ===
echo ">>>>>> Downloading Chromium node_modules"
NODE_MODULES_SHA1=$(curl -sL \
    "https://chromium.googlesource.com/chromium/src/+/${CHROMIUM_VERSION}/third_party/node/node_modules.tar.gz.sha1?format=TEXT" \
    | base64 -d)
if [ -z "$NODE_MODULES_SHA1" ]; then
    echo "ERROR: Could not fetch node_modules SHA1 for Chromium ${CHROMIUM_VERSION}"
    cleanup_and_exit 1
fi
echo "node_modules SHA1: $NODE_MODULES_SHA1"
mkdir -p third_party/node/node_modules
curl -L -o third_party/node/node_modules.tar.gz \
    "https://storage.googleapis.com/chromium-nodejs/${NODE_MODULES_SHA1}"
if [ $? -ne 0 ]; then
    echo "ERROR: node_modules download failed"
    cleanup_and_exit 1
fi
tar --no-same-owner -xf third_party/node/node_modules.tar.gz -C third_party/node/node_modules
rm third_party/node/node_modules.tar.gz

# === Phase 5: Clean up non-distributable content ===
echo ">>>>>> Cleaning up"
find . -type d -name .git -print0 | xargs -0 rm -rf
find . -type d -name __pycache__ -print0 | xargs -0 rm -rf
find . -type f -name '*.pyc' -print -delete
find . -type f -name "*.exe" -print -delete
find . -type f -name "*.dll" -print -delete
find . -type f -name "*.dylib" -print -delete

echo ">>>>>> Removing empty directories"
find . -type d -empty -print -delete

# === Phase 7: Write metadata ===
echo "$ELECTRON_VERSION" > electron/.electron-version
echo "$CHROMIUM_VERSION" > electron/.chromium-version
echo "$NODE_VERSION" > electron/.node-version
echo "$NAN_VERSION" > electron/.nan-version

popd || cleanup_and_exit 1

# === Phase 8: Create tarball ===
TARBALL="electron-${ELECTRON_VERSION}.tar.zst"
echo ">>>>>> Creating ${TARBALL}"
ZSTD_CLEVEL=19 ZSTD_NBTHREADS=$(nproc) tar --zstd --sort=name \
    --owner=0 --group=0 -Scf \
    "${ELECTRON_PKGDIR}/${TARBALL}" -C "$ELECTRON_TMPDIR" \
    electron third_party/electron_node third_party/nan third_party/node
if [ $? -ne 0 ]; then
    echo "ERROR: tar creation failed"
    cleanup_and_exit 1
fi

echo ">>>>>> Done: ${TARBALL}"
echo "Chromium version required: ${CHROMIUM_VERSION}"

cleanup_and_exit 0
