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

`Release:` is Fedora's release, unchanged, e.g. `2` for Fedora's `2`. A
package that is not in Fedora starts at `1`. Each change gets a static
`%changelog` entry.

## Building in COPR

Packages are built in the COPR project
[`tle/power`](https://copr.fedorainfracloud.org/coprs/tle/power/). Each COPR
package uses the SCM source type:

- Clone URL: `https://github.com/runlevel5/fedora-ppc64.git`
- Committish: the branch for the chroot (`rawhide` or `f45`)
- Subdirectory: the package directory
- Spec file: `<package>.spec`
- Build SRPM with: `make_srpm`

`make_srpm` runs `.copr/Makefile`, which downloads the spec's sources with
`spectool` and builds the SRPM. To do the same locally:

    make -f <package>/.copr/Makefile srpm outdir=/tmp/srpm spec=$PWD/<package>/<package>.spec

## Adding a package

1. Create `<package>/` as in [Layout](#layout): the spec, with `Release:`
   numbered as in [Release numbering](#release-numbering), the local patches, and the `.copr` symlink:

       ln -s ../.copr <package>/.copr

2. Check that the SRPM builds and the patches apply:

       make -f <package>/.copr/Makefile srpm outdir=/tmp/srpm spec=$PWD/<package>/<package>.spec
       rpmbuild -rp --nodeps /tmp/srpm/<package>-*.src.rpm

3. Commit and push to each branch the package is built for (`rawhide`, `f45`).

4. Add the package to COPR, either in the web UI (Packages → New package →
   SCM, with the settings in [Building in COPR](#building-in-copr) and
   "Auto-rebuild" checked) or with
   `copr-cli` (`dnf install copr-cli`, with an API token from
   https://copr.fedorainfracloud.org/api/ in `~/.config/copr`):

       copr-cli add-package-scm tle/power \
           --name <package> \
           --clone-url https://github.com/runlevel5/fedora-ppc64.git \
           --commit f45 \
           --subdir <package> \
           --spec <package>.spec \
           --type git \
           --method make_srpm \
           --webhook-rebuild on

   `--commit` is the branch matching the project's chroots (`f45` for the
   `fedora-45-*` chroots).

5. Build it. The project has chroots for several architectures; build only the
   ones the package is meant for, usually ppc64le:

       copr-cli build-package tle/power --name <package> --chroot fedora-45-ppc64le

   or, in the web UI, Packages → `<package>` → Rebuild, selecting the chroots.

6. Later changes build automatically: on a push to `rawhide` or `f45`, the
   `COPR` GitHub workflow (`.github/workflows/copr.yml`) calls COPR's webhook
   for each package directory the push changed. COPR rebuilds the package if
   its committish is the pushed branch, in all of the project's chroots. A
   package can also be rebuilt by hand from the workflow's "Run workflow"
   button, or as in step 5.

   The webhook URL (COPR: Settings → Integrations → GitHub, without a package
   name) is in the repository secret `COPR_WEBHOOK_URL`.
