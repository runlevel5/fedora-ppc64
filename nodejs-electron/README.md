# nodejs-electron

The nodejs-electron package

This package is based on rpms/chromium.git. To make cherry-picking and merging changes easier, the
chromium.git history can be grafted onto this history like this:

    git remote add upstream https://src.fedoraproject.org/rpms/chromium.git
    git fetch upstream
    git replace 259974d740d6515b33e25e5f6d90001167373419 c8703774ad2e8a3ced4b1194c1a88b23a3670604

Then you can directly cherry-pick commit ranges from the chromium package. Use cherry-pick.sh, which
automates some of the conflict resolution:

    ./cherry-pick.sh UPSTREAM_COMMIT

We cherry-pick all upstream commits that touch the spec file anywhere that has not been removed,
even if the changes are irrelevant to the Electron build (e.g. ppc64le fixes, since that arch is not
supported by Electron). This helps keep the file in sync and reduce conflicts later on.

