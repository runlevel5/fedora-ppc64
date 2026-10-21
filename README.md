# fedora-ppc64

RPM spec files for Fedora packages carrying ppc64le (POWER8+, little-endian)
improvements, built in COPR.

## Installing

The built packages are in the COPR project
[`tle/power`](https://copr.fedorainfracloud.org/coprs/tle/power/). To use
them, enable it:

    sudo dnf copr enable tle/power

Packages based on Fedora's keep Fedora's version and release (see
[Release numbering](#release-numbering)), so give the COPR repository a higher
priority than Fedora's (lower number; the default is 99) for dnf to pick its
builds, then reinstall the packages to switch an existing install:

    sudo dnf config-manager setopt copr:copr.fedorainfracloud.org:tle:power.priority=50
    sudo dnf reinstall <package>

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

6. Later changes build automatically, see
   [Automatic rebuilds](#automatic-rebuilds).

## Automatic rebuilds

A push to `rawhide` or `f45` that changes a package directory rebuilds that
package in COPR:

1. The `COPR` GitHub workflow (`.github/workflows/copr.yml`) lists the
   top-level directories the push changed that hold a `<dir>/<dir>.spec`.
2. For each, it posts a GitHub push event to COPR's webhook for that package,
   `<webhook URL><package>/`.
3. COPR rebuilds the package if it has auto-rebuild on and its committish is
   the pushed branch (so a push to `rawhide` does not rebuild a package that
   follows `f45`). The build runs in all of the project's chroots, except
   those the spec's `ExclusiveArch`/`ExcludeArch` rule out.

Setup:

- Auto-rebuild must be on for each package: check "Auto-rebuild" when
  creating it (Packages → New package → SCM) or later (Packages → `<package>`
  → Edit), or with `copr-cli`:

      copr-cli edit-package-scm tle/power --name <package> --webhook-rebuild on

- The webhook URL is in the repository secret `COPR_WEBHOOK_URL`, without a
  package name. It is shown in COPR under Settings → Integrations → GitHub;
  if it changes there, update the secret:

      gh secret set COPR_WEBHOOK_URL -R runlevel5/fedora-ppc64

To rebuild a package without a change, run the workflow by hand, from the
Actions tab (COPR → Run workflow) or with:

    gh workflow run COPR -R runlevel5/fedora-ppc64 --ref f45 -f package=<package>

Changes outside package directories, such as `.copr/Makefile`, trigger no
builds; rebuild the affected packages by hand.
