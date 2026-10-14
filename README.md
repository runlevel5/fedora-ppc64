# fedora-ppc64

RPM spec files for Fedora packages carrying ppc64le (POWER8+, little-endian)
improvements, built in COPR.

## Layout

One directory per package, named as the COPR package:

    <package>/<package>.spec   spec, based on Fedora's
    <package>/*.patch          patches and other local sources
    <package>/.copr            symlink to ../.copr

Remote sources (`Source:` URLs) are not stored here; they are fetched when the
SRPM is built.

## Branches

As in Fedora dist-git: `rawhide` and `f45`, one per Fedora release. A change
for a release goes to its branch.

## Release numbering

`Release:` is Fedora's release followed by `.ppc64.N`, e.g. `2.ppc64.1` for
Fedora's `2`. It sorts above the Fedora build it is based on, and below
Fedora's next release.

## Building in COPR

Each COPR package uses the SCM source type:

- Clone URL: `https://github.com/runlevel5/fedora-ppc64.git`
- Committish: the branch for the chroot (`rawhide` or `f45`)
- Subdirectory: the package directory
- Spec file: `<package>.spec`
- Build SRPM with: `make_srpm`

`make_srpm` runs `.copr/Makefile`, which downloads the spec's sources with
`spectool` and builds the SRPM. To do the same locally:

    make -f <package>/.copr/Makefile srpm outdir=/tmp/srpm spec=$PWD/<package>/<package>.spec

## Packages

| Package | Change |
| --- | --- |
| `webkitgtk` | JavaScriptCore JIT and WebAssembly for ppc64le, Skia VSX paths ([patches](https://github.com/runlevel5/WebKit/releases/tag/webkitgtk-2.54.1-ppc64)) |
